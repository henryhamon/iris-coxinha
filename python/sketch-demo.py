import sketch
import pandas as pd
import os

file_name = 'sales_demo_with_pii_and_all_states.csv'
if (not os.path.isfile(file_name)):
    print('file not found, downloading...')
    sales_data = pd.read_csv('https://gist.githubusercontent.com/bluecoconut/9ce2135aafb5c6ab2dc1d60ac595646e/raw/c93c3500a1f7fae469cba716f09358cfddea6343/sales_demo_with_pii_and_all_states.csv')
    sales_data.to_csv(file_name)
else:
    sales_data = pd.read_csv(file_name)

print('original dataframe:')
print(sales_data)

# PII - Personal Identifiable Information
prompt_str = 'What columns might have PII information in them?'
print('-------')
print(f'ask: {prompt_str}')
resp = sales_data.sketch.ask(prompt_str, call_display=False)
print(resp)

prompt_str = 'Can you give me friendly names for each column?'
print('-------')
print(f'ask: {prompt_str}')
resp = sales_data.sketch.ask(prompt_str, call_display=False)
print(resp)

prompt_str = 'Can you give me friendly names for each column in pt-BR?'
print('-------')
print(f'ask: {prompt_str}')
resp = sales_data.sketch.ask(prompt_str, call_display=False)
print(resp)

prompt_str = 'Create some derived features from the address?'
print('-------')
print(f'howto: {prompt_str}')
resp = sales_data.sketch.howto(prompt_str, call_display=False)
print(resp)
print('executing suggested code...')
exec(resp)
print('dataframe:')
print(sales_data)

prompt_str = 'Get the top 5 grossing states?'
print('-------')
print(f'howto: {prompt_str}')
resp = sales_data.sketch.howto(prompt_str, call_display=False)
print(resp)
print('executing suggested code...')
exec(resp)


prompt_str = 'Get the best an the worst sales in states?'
print('-------')
print(f'howto: {prompt_str}')
resp = sales_data.sketch.howto(prompt_str, call_display=False)
print(resp)
print('executing suggested code...')
exec(resp)