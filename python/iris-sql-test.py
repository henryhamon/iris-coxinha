import iris
import sketch

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