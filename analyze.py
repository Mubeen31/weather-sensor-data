import pandas as pd

# url = 'https://api.thingspeak.com/channels/2007583/feeds.csv?days=2'
# df = pd.read_csv(url)
# df.rename(columns={'created_at': 'Date Time', 'entry_id': 'Id', 'field1': 'Humidity',
#                    'field2': 'Temperature', 'field3': 'Light Intensity', 'field4': 'CO2 Level'}, inplace=True)
# df['Date Time'] = pd.to_datetime(df['Date Time'])
# df['Date Time'] = pd.to_datetime(df['Date Time']).dt.strftime('%Y-%m-%d %H:%M:%S')
# FileName = 'weather data'
# FileExtension = '.csv'
# file = str(str(FileName) + str(FileExtension))
# print(type(file))
