import json
import socket
import logging
import time
import ssl

from core.env import require_env
from core.exceptions import AtfError
from trader.broker_apis import Signal, Trade

LOGGER = logging.getLogger(__name__)

# default connection properites
DEFAULT_XAPI_ADDRESS = 'xapi.xtb.com'
DEFAULT_XAPI_PORT = 5124
DEFUALT_XAPI_STREAMING_PORT = 5125

# API inter-command timeout (in ms)
API_SEND_TIMEOUT = 100

# max connection tries
API_MAX_CONN_TRIES = 3


class TransactionSide(object):
    BUY = 0
    SELL = 1
    BUY_LIMIT = 2
    SELL_LIMIT = 3
    BUY_STOP = 4
    SELL_STOP = 5


class TransactionType(object):
    ORDER_OPEN = 0
    ORDER_CLOSE = 2
    ORDER_MODIFY = 3
    ORDER_DELETE = 4


class JsonSocket(object):
    def __init__(self, address, port, encrypt=False):
        self._ssl = encrypt
        if not self._ssl:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = ssl.wrap_socket(sock)
        self.conn = self.socket
        self._timeout = None
        self._address = address
        self._port = port
        self._decoder = json.JSONDecoder()
        self._receivedData = ''

    def connect(self):
        for i in range(API_MAX_CONN_TRIES):
            try:
                self.socket.connect((self.address, self.port))
            except socket.error as msg:
                LOGGER.error("SockThread Error: %s" % msg)
                time.sleep(0.25)
                continue
            LOGGER.info("Socket connected")
            return True
        return False

    def _send_obj(self, obj):
        msg = json.dumps(obj)
        self._waiting_send(msg)

    def _waiting_send(self, msg):
        if self.socket:
            sent = 0
            msg = msg.encode('utf-8')
            while sent < len(msg):
                sent += self.conn.send(msg[sent:])
                LOGGER.info('Sent: ' + str(msg))
                time.sleep(API_SEND_TIMEOUT / 1000)

    def _read(self, bytes_size=4096):
        if not self.socket:
            raise RuntimeError("socket connection broken")
        while True:
            char = self.conn.recv(bytes_size).decode()
            self._receivedData += char
            try:
                (resp, size) = self._decoder.raw_decode(self._receivedData)
                if size == len(self._receivedData):
                    self._receivedData = ''
                    break
                elif size < len(self._receivedData):
                    self._receivedData = self._receivedData[size:].strip()
                    break
            except ValueError as e:
                continue
        LOGGER.info('Received: ' + str(resp))
        return resp

    def _read_obj(self):
        msg = self._read()
        return msg

    def close(self):
        LOGGER.debug("Closing socket")
        self._close_socket()
        if self.socket is not self.conn:
            LOGGER.debug("Closing connection socket")
            self._close_connection()

    def _close_socket(self):
        self.socket.close()

    def _close_connection(self):
        self.conn.close()

    def _get_timeout(self):
        return self._timeout

    def _set_timeout(self, timeout):
        self._timeout = timeout
        self.socket.settimeout(timeout)

    def _get_address(self):
        return self._address

    def _set_address(self, address):
        pass

    def _get_port(self):
        return self._port

    def _set_port(self, port):
        pass

    def _get_encrypt(self):
        return self._ssl

    def _set_encrypt(self, encrypt):
        pass

    timeout = property(_get_timeout, _set_timeout, doc='Get/set the socket timeout')
    address = property(_get_address, _set_address, doc='read only property socket address')
    port = property(_get_port, _set_port, doc='read only property socket port')
    encrypt = property(_get_encrypt, _set_encrypt, doc='read only property socket port')


class APIClient(JsonSocket):
    def __init__(self, address=DEFAULT_XAPI_ADDRESS, port=DEFAULT_XAPI_PORT, encrypt=True):
        super(APIClient, self).__init__(address, port, encrypt)
        if not self.connect():
            raise AtfError(
                "Cannot connect to " + address + ":" + str(port) + " after " + str(API_MAX_CONN_TRIES) + " retries")

    def execute(self, dictionary):
        self._send_obj(dictionary)
        return self._read_obj()

    def disconnect(self):
        self.close()


# Command templates
def base_command(command_name, **arguments):
    return dict([('command', command_name), ('arguments', arguments)])


def login_command(user_id, password, app_name=''):
    return base_command('login', userId=user_id, password=password, appName=app_name)


client: APIClient | None = None


def initialize(config_dict: dict = None) -> None:
    global client
    if config_dict is not None:
        login = config_dict["login"]
        password = config_dict["password"]
    else:
        login = require_env("XTB_LOGIN")
        password = require_env("XTB_PASSWORD")
    client = APIClient()
    client.timeout = 120.0
    res = client.execute(login_command(user_id=login, password=password))
    if not res["status"]:
        raise AtfError(f"Login failed. Error code: {res['errorCode']}")
    # session_id = res['streamSessionId']


def open_position(trade: Trade) -> int | None:
    LOGGER.info(f"Processing trade: {trade}")
    if trade.trade_type == Signal.NO_ACTION:
        LOGGER.info("Signal is NO_ACTION, skipping opening position.")
        return None
    trade_trans_info = dict(
        cmd=TransactionSide.BUY_LIMIT if trade.trade_type == Signal.BUY else TransactionSide.SELL_LIMIT,
        customComment="",
        offset=0,
        order=0,
        price=round(trade.price, 1),
        sl=round(trade.stop_loss, 1),
        symbol="US500",
        tp=round(trade.take_profit, 1),
        type=0,
        volume=round(trade.volume, 2)
    )
    res = client.execute(base_command("tradeTransaction", tradeTransInfo=trade_trans_info))
    if not res["status"]:
        raise AtfError(f"Trade request failed. Error code: {res['errorCode']}. {res['errorDescr']}")


def dispose() -> None:
    client.disconnect()
