Class dc.python.ObjectScript
{

ClassMethod Test() As %Status
{
    set a=42 
    write "It works!",!
    return a
}

ClassMethod ConvertDate(df) [ Language = python ]
{
    df['dateofsale_formatted'] = df['dateofsale'].dt.strftime('%d/%m/%Y')
}

ClassMethod Teste() [ Language = python ]
{
    import iris
    import pandas as pd
    
    sample_query = \
            'SELECT TOP 100 ID, Actual, cast(AmountOfSale as varchar) AmountOfSale, Channel, Comment, DateOfSale, cast(Discount as varchar) Discount, cast(Latitude as varchar) Latitude, cast(Longitude as varchar) Longitude, Outlet->City OutletCity, Outlet->Country->Name OutletCountry, Product, cast(TargetAmount as varchar) TargetAmount, UnitsSold, ZipCode '\
            'FROM HoleFoods.SalesTransaction'
    sample_rs = iris.sql.exec(sample_query)
    sample_df = sample_rs.dataframe()\
        .set_index('id')
    sample_rs._Close()

    print(sample_df)
    iris.cls('dc.python.ObjectScript').ConvertDate(sample_df)
    print(sample_df)
}

ClassMethod TestPythonCode() [ Language = python ]
{
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

original_date = "2022-04-15"
print(f'original: {original_date}, converted: {convert_date(original_date)}')
test_convert_date()
}

}
