import pyodbc
import pandas as pd

date = '2022-10-01'

def bancoSql():
    #Dados de Conexão
    server = '18.223.91.130'
    #database = 'SBO_Softex'
    database = 'fusionProd'
    username = 'sa'
    password = 'SOF@2018'
    
    #Conexão ao Banco
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    print("Conexão realizada")
    cursor = cnxn.cursor()
    #
    query = "SELECT [datadopagamento],[codigo],[fornecedorrelatorio],[CPFCNPJ],[itemDeDespesa],[projetorelatorio], [valordasolicitacao]  FROM dbo.D_PagamentoPrincipal WHERE  retornoSAP = 1 AND datadopagamento > '"+ date +"';"
    df = pd.read_sql(query, cnxn)
    dados = pd.DataFrame(df)

    return dados