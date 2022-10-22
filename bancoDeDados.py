import pyodbc
import pandas as pd
from credenciais import SERVER, DATABASE, USERNAME, PASSWORD, DATE

def bancoSql():
    
    #Conexão ao Banco
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+SERVER+';DATABASE='+DATABASE+';UID='+USERNAME+';PWD='+ PASSWORD)
    print("Conexão realizada")
    cursor = cnxn.cursor()
    
    query = "SELECT [datadopagamento],[codigo],[fornecedorrelatorio],[CPFCNPJ],[itemDeDespesa],[projetorelatorio], [valordasolicitacao]  FROM dbo.D_PagamentoPrincipal WHERE  retornoSAP = 1 AND datadopagamento > '"+ DATE +"';"
    df = pd.read_sql(query, cnxn)
    dados = pd.DataFrame(df)

    return dados
