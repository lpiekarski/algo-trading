from commons.env import getenv
from commons.exceptions import ArgumentError


class Config:
    __conf = {
        "CACHE_DIR": './.cache',
        "TEMP_DIR": './.tmp',
        "DRIVE": 'local',
        "GIT_DRIVE_MAX_FILE_SIZE": '100000000',
    }

    __env_list = ["CACHE_DIR", "TEMP_DIR", "TEMP_DIR", "DRIVE", "GIT_DRIVE_MAX_FILE_SIZE","LOG_LEVEL", "FILE_LOG_LEVEL", "GIT_PASSWORD", "GIT_DRIVE_MAX_FILE_SIZE"]

    @staticmethod
    def get_param(name):
        return Config.__conf.get(name.upper())

    @staticmethod
    def exist(name):
        return name.upper() in Config.__conf

    @staticmethod
    def set_param(name, value):
        Config.__conf[name.upper()] = value

    @staticmethod
    def set_params_from_file(filename):
        # TODO: config form file
        pass

    @staticmethod
    def set_params_from_env():
        for var in Config.__env_list:
            value = getenv(var)
            if value:
                Config.set_param(var, value)

    @staticmethod
    def init(filename=None):
        Config.set_params_from_env()
        Config.set_params_from_file(filename)

    @staticmethod
    def require_param(name):
        if Config.exist(name):
            return Config.get_param(name)
        raise ArgumentError(f"Missing environment variable '{name}'")

    # def __getattr__(self, key):
    #     try:
    #         return Config.__conf[key]
    #     except KeyError as k:
    #         raise AttributeError(k)


Config.init(filename=None)

