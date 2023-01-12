import pandas as pd

rent_df = pd.read_csv(r".\rent_12_Jan.csv",encoding='UTF-8')

#Função para separar as informações em um dicionário
def get_infos(var: str):
  response = {
      'Price':None,
      'Condo+IPTU':None,
      'Address':None,
      'Size':None,
      'Bedrooms':None,
      'Parking_Spots':None,
      'Bathrooms':None
  }

  infos_list = var.split('\n')

  for info in infos_list:
    if 'mês' in info:
      response.update({'Price':info})
    elif ('condomínio' in info)|('IPTU' in info):
      response.update({'Condo+IPTU':info})
    elif ',' in info:
      response.update({'Address':info})
    elif 'area' in info:
      response.update({'Size':info})
    elif 'bedroom' in info:
      response.update({'Bedrooms':info})
    elif 'parking' in info:
      response.update({'Parking_Spots':info})
    elif 'bathroom' in info:
      response.update({'Bathrooms':info})
  return response

#Separa as informações de cada linha e as separa por colunas
rent_df['0'] = rent_df['0'].apply(lambda row: get_infos(row))
rent_df['Price'] = rent_df['0'].apply(lambda row: row['Price'])
rent_df['Condo+IPTU'] = rent_df['0'].apply(lambda row: row['Condo+IPTU'])
rent_df['Address'] = rent_df['0'].apply(lambda row: row['Address'])
rent_df['Size'] = rent_df['0'].apply(lambda row: row['Size'])
rent_df['Bedrooms'] = rent_df['0'].apply(lambda row: row['Bedrooms'])
rent_df['Parking_Spots'] = rent_df['0'].apply(lambda row: row['Parking_Spots'])
rent_df['Bathrooms'] = rent_df['0'].apply(lambda row: row['Bathrooms'])
#Retira a coluna original
rent_df = rent_df.drop(['0'], axis=1)

#Limpeza de cada coluna
rent_df['Price'] = rent_df['Price'].apply(
    lambda row: row if row == None else row.split('/')[0]
    )
rent_df['Price'] = rent_df['Price'].apply(
    lambda row: row if row == None else row.split('R$')[-1].strip()
    )
rent_df['Price'] = rent_df['Price'].apply(
    lambda row: row if row == None else int(row.replace('.',''))
    )

rent_df['Bedrooms'] = rent_df['Bedrooms'].apply(
    lambda row: row if row == None else int(
        row.split('bedroom')[-1].strip()
        )
    )

rent_df['Parking_Spots'] = rent_df['Parking_Spots'].apply(
    lambda row: row if row == None else int(
        row.split('parking')[-1].strip()
        )
    )
rent_df['Bathrooms'] = rent_df['Bathrooms'].apply(
    lambda row: row if row == None else int(
        row.split('bathroom')[-1].strip()
        )
    )

rent_df['Size'] = rent_df['Size'].apply(
    lambda row: row if row == None else row.split('area')[-1].strip()
    )
rent_df['Size'] = rent_df['Size'].apply(
    lambda row: row if row == None else int(
        row.split('m')[0].strip()
        )
    )

#Função para separar o condomínio e IPTU
def split_condo (var:str):
  response = {
      'Condo' : None,
      'IPTU' : None
  }

  if var is None:
    response.update({
      'Condo' : None,
      'IPTU' : None
  })
  elif ('condomínio' in var) & ('IPTU' in var):
    split_info = var.split('IPTU')
    iptu = split_info[-1].strip()
    iptu = iptu.split('R$')[-1].strip()
    iptu = int(iptu.replace('.',''))
    condo = split_info[0].split('R$')[-1].strip()
    condo = int(condo.replace('.',''))
    response.update({
        'Condo' : condo,
        'IPTU' : iptu
    })
  elif ('condomínio' not in var) & ('IPTU' in var):
    iptu = var.split('R$')[-1].strip()
    iptu = int(iptu.replace('.',''))
    response.update({
        'IPTU' : iptu
    })
  elif ('condomínio' in var) & ('IPTU' not in var):
    condo = var.split('R$')[-1].strip()
    condo = int(condo.replace('.',''))
    response.update({
        'Condo' : condo
    })

  return response

#Separa o condomínio e IPTU em colunas
rent_df['Condo+IPTU'] = rent_df['Condo+IPTU'].apply(lambda row: split_condo(row))
rent_df['Condo'] = rent_df['Condo+IPTU'].apply(lambda row: row['Condo'])
rent_df['IPTU'] = rent_df['Condo+IPTU'].apply(lambda row: row['IPTU'])
rent_df = rent_df.drop(['Condo+IPTU'], axis=1)

#Função para separar o endereço em cidade e bairro
def split_address(var: str):
    response = {
        'Neighborhood': None,
        'City': None
    }

    if var is None:
        response.update({
            'Neighborhood': None,
            'City': None
        })
    elif 'Rio de Janeiro' in var:
        split_info = var.split(',')
        response.update({
            'Neighborhood': split_info[0],
            'City': split_info[1]
        })
    elif 'Rio de Janeiro' not in var:
        split_info = var.split(',')
        response.update({
            'Neighborhood': split_info[1],
            'City': 'Rio de Janeiro'
        })

    return response

#Separa a cidade e bairro em colunas
rent_df['Address'] = rent_df['Address'].apply(lambda row: split_address(row))
rent_df['Neighborhood'] = rent_df['Address'].apply(lambda row: row['Neighborhood'])
rent_df['City'] = rent_df['Address'].apply(lambda row: row['City'])
rent_df = rent_df.drop(['Address'], axis=1)
rent_df['Neighborhood'] = rent_df['Neighborhood'].apply(lambda row: row.strip())

#Definição de lista de bairros para definir as regiões
centro = [
    'São Cristóvão','Benfica','Caju','Catumbi','Centro','Cidade Nova','Estácio',
    'Gamboa','Lapa','Mangueira','Paquetá','Rio Comprido','Santa Teresa',
    'Santo Cristo','Saúde','Vasco da Gama'
    ]
sul = ['Botafogo' , 'Catete' , 'Copacabana' , 'Cosme Velho' , 'Flamengo' ,
       'Gávea' , 'Glória' , 'Humaitá' , 'Ipanema' , 'Jardim Botânico' ,'Lagoa',
       'Laranjeiras','Leblon','Leme','São Conrado','Urca','Vidigal','Rocinha'
       ]
oeste = ['Anil','Barra da Tijuca','Camorim','Cidade de Deus','Curicica',
         'Freguesia de Jacarepaguá','Gardênia Azul','Grumari','Itanhangá',
         'Jacarepaguá','Joá','Praça Seca','Pechincha','Recreio dos Bandeirantes',
         'Tanque','Taquara','Vargem Grande','Vargem Pequena','Vila Valqueire',
         'Jardim Sulacap','Bangu','Campo dos Afonsos','Deodoro','Gericinó',
         'Jabour','Magalhães Bastos','Padre Miguel','Realengo','Santíssimo',
         'Senador Camará','Vila Kennedy','Vila Militar','Barra de Guaratiba',
         'Campo Grande','Cosmos','Guaratiba','Inhoaíba','Paciência',
         'Pedra de Guaratiba','Santa Cruz','Senador Vasconcelos','Sepetiba'
         ]
norte = [
    'Alto da Boa Vista','Andaraí','Grajaú','Maracanã','Praça da Bandeira',
    'Tijuca','Vila Isabel','Abolição','Água Santa','Cachambi','Del Castilho',
    'Encantado','Engenho de Dentro','Engenho Novo','Higienópolis','Jacaré',
    'Jacarezinho','Lins de Vasconcelos','Manguinhos','Maria da Graça','Méier',
    'Piedade','Pilares','Riachuelo','Rocha','Sampaio','São Francisco Xavier',
    'Todos os Santos','Bonsucesso','Bancários','Cacuia',
    'Cidade Universitária','Cocotá','Freguesia','Galeão','Jardim Carioca',
    'Jardim Guanabara','Moneró','Olaria','Pitangueiras','Portuguesa',
    'Praia da Bandeira','Ramos','Ribeira','Tauá','Zumbi','Acari','Anchieta',
    'Barros Filho','Bento Ribeiro','Brás de Pina','Campinho','Cavalcanti',
    'Cascadura','Coelho Neto','Colégio','Complexo do Alemão','Cordovil',
     'Costa Barros','Engenheiro Leal','Engenho da Rainha','Guadalupe',
     'Honório Gurgel','Inhaúma','Irajá','Jardim América','Madureira',
     'Marechal Hermes','Oswaldo Cruz','Parada de Lucas','Parque Anchieta'
     'Parque Colúmbia','Pavuna','Penha','Penha Circular','Quintino Bocaiuva',
     'Ricardo de Albuquerque','Rocha Miranda','Tomás Coelho','Turiaçu',
     'Vaz Lobo','Vicente de Carvalho','Vigário Geral','Vila da Penha',
     'Vila Kosmos','Vista Alegre','Ilha do Governador'
]

centro = list(map(lambda item: item.upper(),centro))
sul = list(map(lambda item: item.upper(),sul))
oeste = list(map(lambda item: item.upper(),oeste))
norte = list(map(lambda item: item.upper(),norte))

#Função para atribuição de regiões por bairro
def get_district (var: str):
  district = ()
  if var is None:
    district = None
  elif var.upper() in centro:
    district = 'centro'
  elif var.upper() in sul:
    district = 'sul'
  elif var.upper() in oeste:
    district = 'oeste'
  elif var.upper() in norte:
    district = 'norte'

  return district

#Função para correção de bairros para o padrão das listas
def correct_neighborhoods (var: str):
  response = ()
  if var is None:
    response = None
  elif var == 'Estacio':
    response = 'Estácio'
  elif var == 'Freguesia- Jacarepaguá':
    response = 'Freguesia de Jacarepaguá'
  elif var == 'Jardim Oceanico':
    response = 'Barra da Tijuca'
  elif var == 'Braz de Pina':
    response = 'Brás de Pina'
  elif var == 'Quintino Bocaiúva':
    response = 'Quintino Bocaiuva'
  elif var == 'Ilha de Guaratiba':
    response = 'Guaratiba'
  elif var == 'Parque Anchieta':
    response = 'Parque Anchieta'
  elif var == 'Cavalcânti':
    response = 'Cavalcanti'
  elif var == 'Peninsula':
    response = 'Barra da Tijuca'
  elif var == 'Fátima':
    response = 'Centro'
  else:
    response = var

  return response

#Corrige os bairros
rent_df['Neighborhood'] = rent_df['Neighborhood'].apply(lambda row: correct_neighborhoods(row))

#Define as regiões
rent_df['District'] = rent_df['Neighborhood'].apply(lambda row: get_district(row))

#Retira linhas com erro nas regiões
rent_df = rent_df.drop(rent_df[rent_df['District'] == ()].index)

#Substitui os valores nulos por zero
rent_df = rent_df.fillna(value={
    'Price':0,'Condo':0,'IPTU':0,'Bedrooms':0,'Parking_Spots':0,'Bathrooms':0
    })

#Conversão dos valores de float para int
rent_df['Price'] = rent_df['Price'].apply(lambda row: int(row))
rent_df['Condo'] = rent_df['Condo'].apply(lambda row: int(row))
rent_df['IPTU'] = rent_df['IPTU'].apply(lambda row: int(row))
rent_df['Bedrooms'] = rent_df['Bedrooms'].apply(lambda row: int(row))
rent_df['Parking_Spots'] = rent_df['Parking_Spots'].apply(lambda row: int(row))
rent_df['Bathrooms'] = rent_df['Bathrooms'].apply(lambda row: int(row))

#Deleta outliers
rent_df = rent_df.drop(rent_df[rent_df['Price'] > 9750].index)
rent_df = rent_df.drop(rent_df[rent_df['Condo'] > 3150].index)
rent_df = rent_df.drop(rent_df[rent_df['IPTU'] > 1898.5].index)

#Salva o arquivo csv
rent_df.to_csv(r".\rent_12_Jan_clean.csv", index=False, encoding="UTF-8")