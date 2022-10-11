import collector.technical_indicators.technical_indicators as ti
import pandas as pd
import logging

LOGGER = logging.getLogger(__name__)

def resample_technical_indicators(df, time_tag="1h"):
    ohlc = {
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last'
    }
    result_rows = []
    # Loop on each minutes
    actual_time = None
    past_resample_df = None
    size = len(df.index)
    count = 0
    max_lookback = get_max_lookback()
    for index, row in df.iterrows():
        count += 1
        if actual_time != index.round(time_tag):
            # da się zapamiętać ostatnie.
            actual_time = index.round(time_tag)
            past_supp_df = df.loc[df.index < actual_time]
            # resample past records
            past_resample_df = past_supp_df.resample(time_tag).apply(ohlc)
        # resample actual sample
        mask = (df.index >= actual_time) & (df.index <= index)
        supp_df = df.loc[mask]
        resample_df = supp_df.resample(time_tag).apply(ohlc)
        resample_df = pd.concat([past_resample_df, resample_df])

        if len(resample_df.index) < max_lookback:
            continue
        resample_df = resample_df.tail(max_lookback)
        ti.add_technical_indicators(resample_df, time_tag)

        last_record = resample_df.iloc[-1]
        last_record.name = index

        result_rows.append(last_record)

        progress_bar = count / size
        if count % 500 == 0 or count == size:
            LOGGER.info(f"{count}/{size} = {100 * progress_bar}%")
            LOGGER.info("----")
    result = pd.DataFrame(result_rows)
    result.drop(['Open', 'High', 'Low', 'Close'], axis=1, inplace=True)
    return pd.DataFrame(result_rows)

def get_max_lookback():
    result = 0
    for indicator, params in ti.INDICATORS.items():
        if params is None:
            pass
        else:
            for param in params:
                if isinstance(param, list):
                    result = max(result, param[0])
                elif isinstance(param, dict):
                    result = max(result, param['length'])
                else:
                    result = max(result, param)
    return result