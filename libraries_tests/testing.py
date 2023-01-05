from commons.data.dataset import Dataset
from collector.technical_indicators.technical_indicators import add_technical_indicators
from libraries_tests.strategies import MyStrategy, INDICATORS2
import talipp as tp

libs = ['ta_old', 'ta_strategy', 'talipp']

#load and cut 2ata
ds = Dataset.load('../data/M1')
ds.df = ds.df.head(10000)


#add technical indicators old way
if 'ta_old' in libs: add_technical_indicators(ds, time_tag=f"{ds.interval.total_seconds():.0f}s", indicators=INDICATORS2)

#add technical indicators in pandas_ta with custom strategy
if 'ta_strategy' in libs: ds.df.ta.strategy(MyStrategy, timed=True)


# save to csv
# x.to_csv('files/technical_indicators.csv')

