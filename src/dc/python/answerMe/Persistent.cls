Class dc.python.answerMe.Persistent [ Abstract ]
{

ClassMethod AnswerMe(question As %String)
{
    Set definition = ##class(%Dictionary.CompiledClass).%OpenId($ClassName())
    Set dateProps = ""
    Set rs = ..FindPropertiesFunc( definition.Name, "%Date")
    While rs.%Next() {
        Set $List(dateProps, * + 1) = rs.Prop
    }
    // 
    Do ..Thinking(question, definition.SqlQualifiedNameQ, $ListToString(dateProps, ","))
}

Query FindProperties(className As %String, propType As %String) As %SQLQuery [ SqlProc ]
{
    SELECT IFNULL(SqlFieldName,Name) As Prop
    FROM %Dictionary.PropertyDefinition
	Where parent = :className
        And "Type" = :propType
        And Calculated = 0
        And Deprecated = 0
}

ClassMethod Thinking(question As %String, table As %String, props As %String) [ Language = python ]
{
    import iris
    import sketch

    qr = 'SELECT DateOfSale, Outlet, Product FROM ' + table
    rs = iris.sql.exec(qr)
    df = rs.dataframe()

    props = list(filter(None, props.split(',')))
    for prop in props:
        df[prop.lower()] = df[prop.lower()].dt.strftime('%m/%d/%Y')
    
    print(df.sketch.ask(question))
}

}
