import pandas as pd
import time


##################################################################################

# start record time
start_time = time.time()

# read dataset
df_real = pd.read_excel('input_dataset/dataset_real.xlsx')

# stop record time
end_time = time.time()

print('\nReading dataset time execution is: %.2f' %(end_time - start_time))

##################################################################################

# start record time
start_time = time.time()

# convert message_timestamp data type from categorical into float
df_real['message_timestamp'] = df_real['message_timestamp'].astype(float, errors='ignore')

# convert message_timestamp data type from float into datetime
df_real['message_timestamp'] = pd.to_datetime(df_real['message_timestamp'], unit="s", errors='ignore')

# drop null values in messages column
# df_real_no_na = df_real.dropna(subset=['message'])

# drop duplicate messages in messages column
df_clean_message = df_real.drop_duplicates(subset=['message'])

# drop invalid rows
df_clean = df_clean_message[~df_clean_message['message_timestamp'].apply(lambda x: isinstance(x, str))]

# stop record time
end_time = time.time()

print('Pre-processing time execution is: %.2f' %(end_time - start_time))

##################################################################################

# export dataset
df_clean.to_excel('output_dataset/clean_dataset_real.xlsx', index=False)