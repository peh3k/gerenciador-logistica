import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

class DbLink():
    URL_DB = 'https://frete-calculator-default-rtdb.firebaseio.com/'


def post_db(path, dados):
    requisicao = requests.post(f'{DbLink().URL_DB}/{path}/.json', data=json.dumps(dados))


def patch_db(path, dados):
    requisicao = requests.patch(f'{DbLink().URL_DB}/{path}/.json', data=json.dumps(dados))

def get_db(path, id=0, last=False, conflict=False, data=[], names=False, find_name='', find_key_by_name=''):
    requisicao = requests.get(f'{DbLink().URL_DB}/{path}/.json')
    if id != 0:
        items = [item for item in requisicao.json() if requisicao.json()[item]['ID'] == id]

        return items
    if last:
        items = [item for item in requisicao.json()]

        return requisicao.json()[items[-1]]['ID'] + 1

    if conflict:
        items = [requisicao.json()[item]['ID'] for item in requisicao.json()]
        same_values = [value[0] for value in data if value[0] in items]
        
        return same_values

    if names:
        empresas = [requisicao.json()[nome]['nome'] for nome in requisicao.json() ]
        return empresas

    if len(find_name) > 0:
        empresa = [requisicao.json()[nome] for nome in requisicao.json() if requisicao.json()[nome]['nome'] == find_name]

        return empresa[0]
    
    if len(find_key_by_name) > 0:
        key = [chave for chave in requisicao.json() if requisicao.json()[chave]['nome'] == find_key_by_name]

        return key[0]

    return requisicao.json()

def get_excel_rows(excel_file):
    # Ler o arquivo do Excel com pandas
    df = pd.read_excel(excel_file)
    
    df.fillna(value="-", inplace=True)
    rows = df.iloc[0:].values.tolist()
    
    return rows

def delete_db(path):
    requests.delete(f'{DbLink().URL_DB}{path}/.json')






















