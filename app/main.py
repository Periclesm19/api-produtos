from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import requests

app = FastAPI(title="Projeto", version="1.0")
URL_BASE = "https://servicodados.ibge.gov.br/api/v1/produtos"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/api/v1/token")
def obter_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.get("/api/v1/produtos", tags=["Produtos"], summary="Obter todos os produtos.")    
def obter_produtos():
    response = requests.get(URL_BASE)
    produtos = []

    if response.status_code == 200:
        dados = response.json()
            
        for produto in dados:
            produtos.append(produto)
                
    return produtos     


@app.get("/api/v1/produtos/portipo/{tipo}", tags=["Produtos"])    
def obter_produtos_por_tipo(tipo: str):  
    response = requests.get(URL_BASE)
    produtos = []

    if response.status_code == 200:
        dados = response.json()
            
        for produto in dados:
            if produto["tipo"] == tipo:
                produtos.append(produto)
                
    return produtos


@app.get("/api/v1/produtos/porcatid/{cat_id}", tags=["Produtos"])    
def obter_produtos_por_cat_id(cat_id: int):  
    response = requests.get(URL_BASE)
    produtos = []

    if response.status_code == 200:
        dados = response.json()
            
        for produto in dados:
            if produto["catId"] == cat_id:
                produtos.append(produto)
                
    return produtos


@app.get("/api/v1/produtos/semsigla", tags=["Produtos"])    
def obter_produtos_sem_sigla():  
    response_estatisticas = requests.get(f"{URL_BASE}/estatisticas")
    response_geociencias = requests.get(f"{URL_BASE}/geociencias")
    produtos = []

    if response_estatisticas.status_code == 200 and response_geociencias.status_code == 200:
        dados_estatisticas = response_estatisticas.json()
        dados_geociencias = response_geociencias.json()

        produtos_estatisticas = []
        for produto in dados_estatisticas:
            if produto["sigla"] == "":
                produtos_estatisticas.append(produto)


        produtos_geociencias = []
        for produto in dados_geociencias:
            if produto["sigla"] == "":
                produtos_geociencias.append(produto)

        produtos = produtos_estatisticas + produtos_geociencias

    return produtos       


@app.get("/api/v1/produtos/portipo/{tipo}/ordenadoporid", tags=["Produtos"])    
def obter_produtos_por_tipo_ordenado_por_id(tipo: str):  
    response = requests.get(URL_BASE)
    produtos = []

    if response.status_code == 200:
        dados = response.json()
            
        for produto in dados:
            if produto["tipo"] == tipo:
                produtos.append(produto)
               
    produtos_ordenados = sorted(produtos, key=lambda prd: prd["id"])
    return produtos_ordenados

     