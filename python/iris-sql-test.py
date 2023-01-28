import iris
import sketch
import numpy as np
import pandas as pd

def ask(prompt_str, df):
    print('-------')
    print(f'ask: {prompt_str}')
    resp = df.sketch.ask(prompt_str, call_display=False)
    print(resp)

def howto(prompt_str, df, execute_on_df = False):
    print('-------')
    print(f'howto: {prompt_str}')
    resp = df.sketch.howto(prompt_str, call_display=False)
    print(resp)
    if (execute_on_df):
        print('executing suggested code...')
        exec(resp)
    return resp

def test_iris_prompts():
    # had to cast float to varchar in order to workaround convertion error in method dataframe() from resultset class when the float column has a null value
    sample_query = \
            'SELECT TOP 100 ID, Actual, cast(AmountOfSale as varchar) AmountOfSale, Channel, Comment, DateOfSale, cast(Discount as varchar) Discount, cast(Latitude as varchar) Latitude, cast(Longitude as varchar) Longitude, Outlet->City OutletCity, Outlet->Country->Name OutletCountry, Product, cast(TargetAmount as varchar) TargetAmount, UnitsSold, ZipCode '\
            'FROM HoleFoods.SalesTransaction'
    sample_rs = iris.sql.exec(sample_query)
    sample_df = sample_rs.dataframe()\
        .set_index('id')
    sample_rs._Close()

    query = \
            'SELECT ID, Actual, cast(AmountOfSale as varchar) AmountOfSale, Channel, Comment, DateOfSale, cast(Discount as varchar) Discount, cast(Latitude as varchar) Latitude, cast(Longitude as varchar) Longitude, Outlet->City OutletCity, Outlet->Country->Name OutletCountry, Product, cast(TargetAmount as varchar) TargetAmount, UnitsSold, ZipCode '\
            'FROM HoleFoods.SalesTransaction'
    rs = iris.sql.exec(query)
    df = rs.dataframe()\
        .set_index('id')

    print('original dataframe:')
    print(sample_df)

    prompt_str = 'What columns might have PII information in them?'
    ask(prompt_str, sample_df)

    prompt_str = 'Can you give me friendly names for each column?'
    ask(prompt_str, sample_df)

    prompt_str = 'Infer columns type based on their values?'
    ask(prompt_str, sample_df)

    # this prompt causes error convertion when the column has a empty string value...
    # prompt_str = 'Convert data type of columns amountofsale to float'
    # output: 
    # # Convert data type of columns amountofsale to float
    # df['amountofsale'] = df['amountofsale'].astype(float)
    # ... so, just change the prompt adding a constraint to handle such empty values!
    prompt_str = 'Convert data type of columns amountofsale to float, converting empty strings to None'
    code = howto(prompt_str, sample_df, execute_on_df=True)
    exec(code, {"df": df})

    prompt_str = 'Get the top 5 grossing cities?'
    code = howto(prompt_str, sample_df)
    exec(code, {"df": df})

    prompt_str = 'Get the top 5 grossing products, per city?'
    code = howto(prompt_str, sample_df)
    exec(code, {"df": df})

    prompt_str = 'Creata a new column called dataofsale_formatted from the conversion of the dateofsale column to DD/MM/YYYY?'
    code = howto(prompt_str, sample_df)
    exec(code, {"df": df})
    print(df[['dateofsale','dataofsale_formatted']])

    prompt_str = 'Create new column called full_address combining columns OutletCity, OutletCountry and ZipCode separated by comma.'
    code = howto(prompt_str, sample_df)
    exec(code, {"df": df})
    print(df['full_address'])

    # não funcionou
    # prompt_str = 'Leave just the outliers amountofsales'
    # code = howto(prompt_str, sample_df)
    # exec(code, {"df": df, "np": np})
    # print(df[['dateofsale','dataofsale_formatted']])

    # não funcionou
    # prompt_str = 'Drop lines where column comment is NA'
    # code = howto(prompt_str, sample_df)
    # exec(code, {"df": df})
    # print(df)

def test_fixed_columns_dataset():
    input = """
id   actual amountofsale channel comment dateofsale discount  outletcity outletcountry  product targetamount unitssold zipcode
1      True         2.95                 2022-11-07        0    New York           USA  SKU-192                      1   13778
2      True         6.32       2         2018-11-16       .2       Tokyo         Japan  SKU-709                      2
3      True         3.95       2         2020-01-23        0    Shanghai         China  SKU-203                      1
4      True         4.76       2         2022-04-15       .2      Mumbai         India  SKU-222                      1
5      True         4.25       1         2018-06-20        0       Tokyo         Japan  SKU-204                      1
96     True        119.7       2         2022-12-28        0    Santiago         Chile  SKU-199                      6
97     True         1.04                 2022-11-06       .1       Osaka         Japan  SKU-451                      1
98     True         1.95       2         2022-11-15        0        Rome         Italy  SKU-287                      1
99     True        15.84       1         2018-02-10       .2      Mumbai         India  SKU-708                      4
100    True         3.96       2         2021-10-29       .2       Tokyo         Japan  SKU-708                      1"""
    df = pd.DataFrame(data={'input': input.split("\n")[1:]})
    print(df)
    
    # howto('Extract columns from values in column input into a new dataframe called ret_df.', df)
    # ret_df = df['input'].str.split(expand=True)
    # ret_df.columns = ['id', 'actual', 'amountofsale', 'channel', 'comment', 'dateofsale', 'discount', 'outletcity', 'outletcountry', 'product', 'quantity', 'salesperson', 'status']
    # print(ret_df)

    # howto('Create a new dataframe from the column input parsing it as a fixed column dataset with a header.', df)
    # # Split the input column into separate columns
    # df[['id', 'actual', 'amountofsale', 'channel', 'comment', 'dateofsale', 'discount', 'outletcity', 'outletcountry', 'product', 'quantity']] = df['input'].str.split(' ', expand=True)
    # # Set the column names as the header
    # df.columns = df.iloc[0]
    # # Drop the first row since it is now the header
    # df = df.drop(df.index[0])

    # howto('Create a function called parse_fixed_coluns that receives a string parameter called input_dataframe and returns a new dataframe generated by extracting columns from the column called input in the function parameter.', df)
    # print(parse_fixed_columns(df))

    # howto(f"""
    #     give me a function that receives on string parameter called original_date
    #     this parameter has dates in the format of the ones presented in the dateofsale column
    #     the function must return the convertion of dates in the dd/mm/yyyy format
    #     the code must refer to all needed imports
    #     after, give me a unit test for this function
    # """, df)
    original_date = "2022-04-15"
    print(f'original: {original_date}, converted: {convert_date(original_date)}')
    test_convert_date()

    # howto('create function in ObjectScript that calc the standard deviation from an array of floats', df)

def parse_fixed_columns(df):
    # Get the length of the input column
    input_len = len(df['input'].iloc[0])

    # Calculate the boundaries of the columns
    column_boundaries = []
    for i in range(input_len):
        column_boundaries.append(i)

    # Print the boundaries
    print(column_boundaries)

# imports
import datetime

# function
def convert_date(original_date):
    """
    This function receives a string parameter called original_date, which has dates in the format of the ones presented in the dateofsale column.
    The function returns the convertion of dates in the dd/mm/yyyy format.
    """
    date_object = datetime.datetime.strptime(original_date, '%Y-%m-%d')
    return date_object.strftime('%d/%m/%Y')

# unit test
def test_convert_date():
    assert convert_date('2022-11-07') == '07/11/2022'
    assert convert_date('2018-11-16') == '16/11/2018'
    assert convert_date('2020-01-23') == '23/01/2020'
    assert convert_date('2022-04-15') == '15/04/2022'

# test_iris_prompts()
test_fixed_columns_dataset()