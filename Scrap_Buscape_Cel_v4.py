
"""
Script para pegar os dados de celulares do Buscapé a partir de uma lista pré definida
Data: Fev/2022
Autor: André Serpa

Esse script poderá parar de funcionar se tiver alguma alteração no código do Buscapé
Esse script procura pelo Json da página e recupera as informações de lá, sendo mais performático dessa maneira
"""

#Bibliotecas
import requests as rq
import json
import pandas as pd
from pynotifier import Notification


#Configura o display do pandas
pd.options.display.max_columns = 99
pd.options.display.max_rows = 99

#Inicio printando na Tela
print("\n")
print("*****************************")
print("* DataCell WebCrawler v0.1b *")
print("*****************************")
print("\n")
print("Qual diretório deseja salvar o arquivo?")
vDir = input("Dir: ")
#Pega o diretorio passado no argumento

#Imita um navegador para passar restricoes
user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'
headers = {'User-Agent': user_agent}


#Cria a lista com os celulares
#Caso tenha novos celulares, acrescentar na lista abaixo
vListaMarca = ['iphone','samsung','LG','Motorola','Xiaomi','Asus','Multilaser','Realme','Positivo','Nokia','TCL','Huawei','Philco',
               'Lenovo','Sony','Tecno','Umidigi','Blu','Caterpillar','Alcatel','Google','Oneplus','Quantum','CCE','Fly','Qbex','Semp',
               'TecToy', 'Ulefone', 'ZTE']


#Cria o dicionario
dfs = {}

#Contador da pagina
vPag = 1
vPagFim = 2
                
#Pega o site a ser scrapeado
#Pra cada item da lista acessa a pagina
#for vMarca in vListaMarca:
while vPag <= vPagFim:
    
    vURL = 'https://www.buscape.com.br/celular/smartphone?page=' + str(vPag) +'&pageTitle=Smartphone&q=&sortBy=price_asc'
    
    #Adiciona mais celulares
    #if vMarca == 'iphone':
    #    vURL = 'https://www.buscape.com.br/search?q=iphone&refinements[0][id]=filterFacets.S%C3%A9rie&refinements[0][values][0]=&refinements[1][id]=filterFacets.Tipo de Aparelho&refinements[1][values][0]=Smartphone'
    #elif vMarca == 'samsung':
    #    vURL = 'https://www.buscape.com.br/search?q=samsung&refinements[0][id]=filterFacets.S%C3%A9rie&refinements[0][values][0]='
    #else:
    #    vURL = 'https://www.buscape.com.br/search?q=' + vMarca + '&refinements[0][id]=categoryId&refinements[0][values][0]=7'


    print('Lendo os dados de pagina ' + str(vPag))
    print(vURL)
    print('\n')
        
    #Verifica se o site esta respondendo
    vResp = rq.get(vURL,headers=headers)
    vStat = vResp.status_code
        
        
    #Se o site estiver ok
    if vStat == 200:
                      
        #Coloca o conteudo do html na variavel
        vHTML = vResp.text
            
        #Limpa o Html deixando apenas o Json com as informacoes
        vHTML = vHTML.split('"hits":{',1)[1]
        vHTML = vHTML.split(',"pagination":{"hitsPerPage"',1)[0]
        vHTML = '{' + vHTML + '}'
            
        #Carrega o json no formato de json
        j = json.loads(vHTML)
                   
        #Cria a lista
        vListaURL = []
            
        #Pra cada item do json, recupera o Nome e o Preço e coloca na lista
        for i in j['hits']:
            vListaURL.append(i['url'])
        
        
        for url in vListaURL:
            vRespURL = rq.get('https://www.buscape.com.br' + url,headers=headers)
            
            #Coloca o conteudo do html na variavel
            vHTML = vResp.text
            
            #Limpa o Html deixando apenas o Json com as informacoes
            vHTML = vHTML.split('"hits":{',1)[1]
            vHTML = vHTML.split(',"pagination":{"hitsPerPage"',1)[0]
            vHTML = '{' + vHTML + '}'
            
            #Carrega o json no formato de json
            j = json.loads(vHTML)
            
            #Joga no Dataframe
            df = pd.json_normalize(j['hits'])
           
            #Cria a entrada variavel no dicionario
            dfs['df_' + str(vPag)] = df['url']
            
            #print(df)
    
    vPag = vPag+1
    
#Cria a lista 
vAcaoFimLista = []
 
           
#Para cada entrada dinamica criada no Dicionário, adiciona na lista
for i in dfs.keys(): 
    #print(i)
    vAcaoFimLista.append(dfs[i])
            
    #Concatena os dados da lista em um unico dataframe
    df_Cels = pd.concat(vAcaoFimLista, sort=False)
            
#Remove os dados de lead e Usados
df_Cels = (df_Cels[~df_Cels.str.contains("/lead?")])
df_Cels = (df_Cels[~df_Cels.str.contains("usado")])


#Joga as urls do dataframe para a lista
vLista_df_Cels = df_Cels.values.tolist()



######################## Inicio pegando das ofertas ###########################
#Cria o novo dicionario para as ofertas
dfs_Ofertas = {}

#Cria contador
vContOfertas = 0

print('\n')
print('----------- Pegando dados das URLs -----------')

#Faz o loop para cada pagina de celular no dataframe
for url in vLista_df_Cels:
    
    print(url)

    vRespURL = rq.get('https://www.buscape.com.br' + url,headers=headers)
    
    #print(vRespURL)
    #Coloca o conteudo do html na variavel
    vHTML = vRespURL.text
    
    #Limpa o Html deixando apenas o Json com as informacoes
    vHTML = vHTML.split('id="__NEXT_DATA__"',1)[1]
    vHTML = vHTML.split('</script>',1)[0]
    vHTML = vHTML.replace('type="application/json">','')
    #vHTML = vHTML.replace('"','')

    
    #Carrega o json no formato de json
    j = json.loads(vHTML)
    
    #Joga no Dataframe
    df_Ofertas = pd.json_normalize(j['props']['initialReduxState']['offers']['offerList'])

    #Incrementa o contador
    vContOfertas = vContOfertas + 1
    
    #Cria a entrada variavel no dicionario
    dfs_Ofertas['df_Ofertas_' + str(vContOfertas)] = df_Ofertas
    

#Cria a lista 
vAcaoFimLista = []
            
#Para cada entrada dinamica criada no Dicionário, adiciona na lista
for i in dfs_Ofertas.keys(): 
    #print(i)
    vAcaoFimLista.append(dfs_Ofertas[i])
            
    #Concatena os dados da lista em um unico dataframe
    df_Ofertas = pd.concat(vAcaoFimLista, sort=False) 
    
    #Retira as duplicadas do Dataframe
    df_Ofertas = df_Ofertas.drop_duplicates(subset='id')
    
    #Cria a coluna com a marca
    #for vMarca in vListaMarca:
    df_Ofertas['brand'] = df_Ofertas['name'].str.upper().map(lambda x: 'IPHONE' if 'IPHONE' in x else 'SAMSUNG' if 'SAMSUNG' in x else 
                                                             'LG' if 'LG' in x else 'MOTOROLA' if 'MOTOROLA' in x else 
                                                             'XIAOMI' if 'XIAOMI' in x else 'ASUS' if 'ASUS' in x else 
                                                             'MULTILASER' if 'MULTILASER' in x else 'REALME' if 'REALME' in x else 
                                                             'POSITIVO' if 'POSITIVO' in x else 'NOKIA' if 'NOKIA' in x else 
                                                             'TCL' if 'TCL' in x else 'HUAWEI' if 'HUAWEI' in x else
                                                             'PHILCO' if 'PHILCO' in x else 'LENOVO' if 'LENOVO' in x else
                                                             'SONY' if 'SONY' in x else 'TECNO' if 'TECNO' in x else
                                                             'UMIDIGI' if 'UMIDIGI' in x else 'BLU' if 'BLU' in x else
                                                             'CATERPILLAR' if 'CATERPILLAR' in x else 'ALCATEL' if 'ALCATEL' in x else
                                                             'GOOGLE' if 'GOOGLE' in x else 'ONEPLUS' if 'ONEPLUS' in x else
                                                             'QUANTUM' if 'QUANTUM' in x else 'CCE' if 'CCE' in x else 'Outros') 
                                                
    
    #Lista de colunas a serem removidas
    listaColunas = ['imageUrl','categoryID','productID','merchantId','sellerID','sellerLogoURL',
                    'sellerRoundedLogoURL','sellerIsMarketplace','cashback','paymentMethod',
                    'loweringPercentage','numParcels','parcelValue','totalParceledValue','totalPrice']
    
    #Remove colunas
    for vCol in listaColunas:
        df_Ofertas.drop(vCol, 1, inplace=True)
    
    df_Ofertas['name'] = df_Ofertas['name'].str.replace('"','')
    
    #Exporta pra csv, usando encoding do windows
    df_Ofertas.to_csv(vDir + '\dataCels.csv', sep=';', index=False, encoding="utf-8-sig")

print('\n')
print('----------------------------------------------------')    
print('Arquivo gerado com sucesso ' + vDir + '\dataCels.csv')
print('----------------------------------------------------')


#Envia notificação
Notification(
	title='DataCell Crawler v0.1',
	description='Arquivo gerado com sucesso ' + vDir + '\dataCels.csv',
	#icon_path='/absolute/path/to/image/icon.png', # On Windows .ico is required, on Linux - .png
	duration=5,                                   # Duration in seconds
	urgency='normal'
).send()

