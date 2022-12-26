
#Bibliotecas
import requests as rq
import json
import pandas as pd
from pandas.io.json import json_normalize
from datetime import datetime


#Configura o display do pandas
pd.options.display.max_columns = 99
pd.options.display.max_rows = 99

#Imita um navegador para passar restricoes
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
headers = {'User-Agent': user_agent}


#Pega o total de paginas

#Pega a pagina
vURLIni = 'https://rj.olx.com.br/rio-de-janeiro-e-regiao/autos-e-pecas/motos/harley-davidson?o=1'

#Joga a pagina na variavel
vRespIni = rq.get(vURLIni,headers=headers)
vHTMLIni = vRespIni.text
vHTMLIni = str(vHTMLIni)

#Faz o corte da pagina para trazer somente o link da ultima
vHTMLIni = vHTMLIni.split('Próxima pagina',1)[1]
vHTMLIni = vHTMLIni.split('Última pagina',1)[0]
vHTMLIni = vHTMLIni.split('href="',1)[1]
vHTMLIni = vHTMLIni.split('" data-lurker-detail="last_page"',1)[0]

#Cria as variaceis
vPagIni = 1
vPagFinal = vHTMLIni.replace('https://rj.olx.com.br/rio-de-janeiro-e-regiao/autos-e-pecas/motos/harley-davidson?o=','')

#Cria o dicionario
dfs = {}
                    
#Itera entre as paginas
while vPagIni <= int(vPagFinal):
                        
    #URL
    vURL = 'https://rj.olx.com.br/rio-de-janeiro-e-regiao/autos-e-pecas/motos/harley-davidson?o=' + str(vPagIni) + '&sf=1'
                    
    print('Pagina: ' + str(vPagIni))
    #print(vURL)
    #Testa o codigo de retorno do site
    print(vURL+'\n')
    vResp = rq.get(vURL,headers=headers)
    vStat = vResp.status_code
                        
                    
    #Se codigo 200, entao vai adiante
    if vStat == 200:
        vHTML = vResp.text
        vHTML = str(vHTML)
                            
        #Valida se a pagina existe ou nao
        vValPag = 'OK' if 'Não encontramos resultados' in vHTML else 'NOK'
                            
        #Continua se a pagina existir
        if vValPag == 'NOK':
                        
            #Pega apenas a parte do Json do codigo fonte
            vHTML = vHTML.replace('&quot;','"')
            vHTML = vHTML.split('"adList":[',1)[1]
            vHTML = vHTML.split(',"searchCategories":[{',1)[0]
            vHTML = '{"adList":[' + vHTML + '}'
            
            #transforma para json
            j = json.loads(vHTML)
            
            #Cria o dataframe do pandas, já normalizando o json
            df = json_normalize(j['adList'])
            
            #Deixa somente as colunas utilizaveis
            df = df[['subject', 'price', 'oldPrice', 'professionalAd', 'isFinanceable', 'url', 'location', 'date', 'properties']]
            df = df.dropna(axis=0)
            df['date'] = pd.to_datetime(df['date'],unit='s')
            df['year'] = df['properties'].iloc[0][2]['value']
            df['mileage'] = df['properties'].iloc[0][3]['value']
            df = df.drop('properties', axis=1)
                     
            
            #Cria a entrada variavel no dicionario
            dfs['df_' + str(vPagIni)] = df
            
            vPagIni = vPagIni + 1
            
        else:
            break
                        
                        
            #vStat = vResp.status_code 
            #Sai do Loop
    else:
        print(vURL)
        print('\n')
        print(vStat)
        break
        
#Cria a lista 
vAcaoFimLista = []
                    
#Para cada entrada dinamica criada no Dicionário, adiciona na lista
for i in dfs.keys():
    #print(i)
    vAcaoFimLista.append(dfs[i])
    
                    
    #Concatena os dados da lista em um unico dataframe
    df_OLX_HD = pd.concat(vAcaoFimLista, sort=False)
                    
    #Exporta pra csv, usando encoding do windows
                
    print('\nCriando o arquivo data_OLX_HD.csv com os dados')
    df_OLX_HD.to_csv('data_OLX_HD.csv', sep=';', index=False)
    print('\nArquivo criado\n')
    print('-----------------------------------------------------')

