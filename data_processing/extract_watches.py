# import libraries
import pandas as pd
import re
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

##################################################################################

# read dataset
df_mockup = pd.read_excel('input_dataset/chat_message_dataset.xlsx',parse_dates=['timestamp']).drop_duplicates(subset=['messages']).reset_index(drop=True)

##################################################################################

# watches, models, conditions directory
brand_names = ['Audemars Piquet', 'Rolex', 'Franck Muller']

# detect brand patterns
aa_brand_patterns = ['Audemars Piquet', 'ap']
rolex_brand_patterns = ['Rolex', 'rlx']
pp_brand_patterns = ['Franck Muller', 'FM', 'fm']

# detect brand models
ap_models    = ['Royal Oak 34 77350ST', 'Royal Oak 41 26615TI Perpetual Calendar Salmon Dial', 'Royal Oak Offshore 43 26420TI Blue', 'Royal Oak 41 15500ST Blue']
rolex_models = ['Cosmograph Daytona 40 116506', 'Cosmograph Daytona 40 116515 Choco', 'Daytona 40 116509 Blue', 'Cosmograph Daytona 40 116515 Choco', 'Daydate 36 128345RBR', 'Datejust 36 126234 Green Palm Jubilee']
fm_models    = ['Long Island 952 QZ Col Drm D 1R (AC) Pink', 'Curvex 2852 QZ D 1R (AC)', 'Curvex 2852 B QZ (AC)', 'Galet 3002 L QZ R D 1R (AC)', 'Master Square 6002 M QZ R D 1R (AC)', 'Master Square 6002 M QZ D 1R (5N)']
conditions   = ['Pre-owned', 'Mint', 'Unworn']

##################################################################################

# extract elements from chats
chats = []
brands = []
models = []
conds = []
prices = []

# currency patterns
expr = 'USD[0-9]+'

# create date & time columns
df_mockup['date'] = ''
df_mockup['time'] = ''

for i in range(len(df_mockup)):
    text = df_mockup['messages'][i]
    df_mockup['date'][i] = df_mockup['timestamp'][i].date()
    df_mockup['time'][i] = df_mockup['timestamp'][i].time()
    price = re.findall(expr, text)

    for j in range(len(brand_names)):
        if text.find(brand_names[j]) != -1:
            start_brand = text.find(brand_names[j])
            end_brand = start_brand + len(brand_names[j])
            brand = text[start_brand:end_brand]

            if brand == 'Audemars Piquet':
                for k in range(len(ap_models)):
                    if text.find(ap_models[k]) != -1:
                        start_model = text.find(ap_models[k])
                        end_model = start_model + len(ap_models[k])
                        model = text[start_model:end_model]


            elif brand == 'Rolex':
                for k in range(len(rolex_models)):
                    if text.find(rolex_models[k]) != -1:
                        start_model = text.find(rolex_models[k])
                        end_model = start_model + len(rolex_models[k])
                        model = text[start_model:end_model]

            elif brand == 'Franck Muller':
                for k in range(len(fm_models)):
                    if text.find(fm_models[k]) != -1:
                        start_model = text.find(fm_models[k])
                        end_model = start_model + len(fm_models[k])
                        model = text[start_model:end_model]

    for j in range(len(conditions)):
        if text.find(conditions[j]) != -1:
            start_condition = text.find(conditions[j])
            end_condition = start_condition + len(conditions[j])
            condition = text[start_condition:end_condition]

    chats.append(text)
    conds.append(condition)
    models.append(model)
    brands.append(brand)
    prices.extend(price)


# merge into one table
df_extract = pd.DataFrame({'Message':chats, 'Brand':brands, 'Model':models, 'Condition':conds, 'Price':prices, 'Date':df_mockup['date'], 'Time':df_mockup['time']})

##################################################################################

# export dataset
df_extract.to_excel('output_dataset/dataset_extract.xlsx', index=False)