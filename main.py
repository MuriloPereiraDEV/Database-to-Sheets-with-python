from __future__ import print_function
from operator import index
from bancoDeDados import bancoSql, DATE
from dadosSheets import SCOPES, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME
import pandas as pd
import time
import os.path
import schedule
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    #Validação de Credenciais
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    #Pega arquivo inteiro
    sheet = service.spreadsheets()
    #Lê a planilha
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()

    #Pega os valores
    values = result.get('values', [])

    lengthValues = 0
    for i in values:
        if i[0] >= DATE:
            lengthValues += 1

    valuesDF = pd.DataFrame(values)

    if len(valuesDF)==0:
        header = [
            ['datadopagamento', 'codigo', 'fornecedorrelatorio', 'CPFCNPJ', 'itemDeDespesa', 'projetorelatorio', 'valordasolicitacao']
        ]
        sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                   range='Página1!A1', valueInputOption="USER_ENTERED", body={"values":header}).execute()
        
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()

        #Pega os valores
        values = result.get('values', [])

        valuesDF = pd.DataFrame(values)

    dados = bancoSql()

    dados['datadopagamento'] = dados['datadopagamento'].fillna("vazio")
    dados['codigo'] = dados['codigo'].fillna("vazio")
    dados['fornecedorrelatorio'] = dados['fornecedorrelatorio'].fillna("vazio")
    dados['CPFCNPJ'] = dados['CPFCNPJ'].fillna("vazio")
    dados['itemDeDespesa'] = dados['itemDeDespesa'].fillna("vazio")
    dados['projetorelatorio'] = dados['projetorelatorio'].fillna("vazio")
    dados['valordasolicitacao'] = dados['valordasolicitacao'].fillna("vazio")

    #Verifica se a planilha está de acordo com o banco 
    if len(dados)==(lengthValues-1):
        print("Já está atualizada!")
    else:
        rangeAux = dados.shape[0] - (lengthValues-1)
        sizeValuesDF = lengthValues
        for i in range(rangeAux):
            indexAux = len(dados) - rangeAux + i
            string = str(sizeValuesDF + i + 1)
            
            valores_adicionar = [
                dados.iloc[indexAux].tolist()
            ]
    
            #Adiciona ou edita valores
            sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                   range='Página1!A'+string, valueInputOption="USER_ENTERED", body={"values":valores_adicionar}).execute()
            time.sleep(2)
        print("Nova Atualização!")

schedule.every(1).seconds.do(main)

while 1:
    schedule.run_pending()
    time.sleep(1)
