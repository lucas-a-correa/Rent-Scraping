# Mercado de Aluguéis no Rio de Janeiro
## Web Scraping e Data Analysis do Mercado de Aluguéis na Cidade do Rio

## 1. Sumário

* Contexto
* Extração
* Dados
* Análise
* Conclusão

## 2. Contexto

A cidade do Rio de Janeiro é a segunda maior cidade do Brasil, com mais de 6,7 milhões de habitantes, ou pouco mais de 3% da população brasileira. Como toda cidade altamente urbanizada, um dos desafios a ser enfrentado é a moradia de tal população. De acordo com um [estudo](https://censodemoradia.quintoandar.com.br) do QuintoAndar, cerca de 27% dos brasileiros moram em imóveis alugados, representando uma parcela significativa da população. O presente estudo tem por objetivo analisar a situação atual das ofertas de aluguel na cidade do rio, identificando tendências e padrões.

## 3. Extração

A extração dos dados foi realizada utilizando a ferramenta Selenium, um pacote Python que automatiza interações com um web browser, conforme pode ser verificado no seguinte [script](/selenium_scraping.py). 
Os dados foram extraídos do site [Zap Imóveis](https://www.zapimoveis.com.br), nas datas de 29 Dez 22 e 12 Jan 23

## 4. Dados

Os dados extraídos foram salvos em arquivos CSV e limpos utilizando o seguinte [script Python](/rent_cleaning.py).
Como nem todos os anúncios possuem todas as informações, a extração junta todas as disponíveis em uma mesma célula de um DataFrame, e, para realizar a limpeza, nós separamos cada informação de acordo com o tipo.

```Python
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
```

Os anúncios extraídos possuem, então, os seguintes dados: Valor de aluguel, valor de condomínio, valor de IPTU, área do imóvel e quantidade de quartos, banheiros e vagas de estacionamento. Relembro, entretanto, que nem todos os anúncios possuem todos os valores, seja por não se aplicar ao caso, como valor de condomínio para uma casa que não está em um condomínio, ou por erro no preenchimento.
Além da conversão para os tipos de dado pertinentes, foi adicionada uma coluna para identificar a região da cidade (Centro, Zona Sul, Norte e Oeste) na qual o imóvel está localizado. Também foram excluídos valores muito discrepantes, por provavelmente tratar-se de erro no preenchimento.
Por fim, os dados limpos foram carregados na plataforma Power BI para análise.

## 5. Análise

O dashboard interativo pode ser acompanhado pelo seguinte [arquivo](/Aluguéis.pbix).

![Image]()

A primeira visualização apresenta algumas métricas iniciais dos dados. Após a limpeza e filtragem dos dados, restaram-nos 9684 ofertas na amostra utilizada, com uma média de aluguel de R$ 2,17 mil, R$ 599,30 de condomínio. R$ 143,72 de IPTU e 84,58 m².
Observamso uma grande variação nos valores, com o maior valor de aluguel sendo R$ 9.470,00 mais caro que o menor valor. Isso reflete a grande diversidade de realidades presente na cidade, com regiões muito ricas e regiões muito pobres, conforme será aprofundado na análise.

![Image]()

No gráfico seguinte observamos a distribuição dos preços na amostra. A maior concentração de ofertas encontra-se abaixo da média, com poucos valores mais altos. Verificamos, também, as características dos bairros e regiões, com os bairros mais caros majoritariamente localizados na Zona Sul e os mais baratos na Zona Norte, refletindo as diferenças de renda entre as regiões. Observamos, ainda, que apenas 30 (20,5%) dos bairros apresentam uma média de preços superior a média geral.

![Image]()

A imagem acima mostra em mapas as localizações das ofertas, evidenciando o número de ofertas e o valor médio do aluguel. Vemos que a média de preços da Zona Sul é cerca de 2 vezes maior que as demais regiões e que a maior parte das ofertas está localizada na Zona Norte.

![Image]()

Em seguida, detalhamos as informações de cada região.
Começando pela Zona Sul, vemos que a concentração de renda na região se reflete nos preços. Dos 17 bairros presentes na amostra, apenas 1 apresenta uma média inferior a média geral, o Vidigal, uma comunidade da região, que mesmo sendo uma comunidade apresenta uma média superior ao valor médio do Centro e da Zona Norte. Possui, também, 8 dos 10 bairros mais caros da cidade.
A Zona Sul é uma região pequena, antiga e com poucos bairros e, portanto, com menos espaço para novas moradias. A alta procura e a baixa oferta causam a escalada dos preços, o que reforça a região com a concentração de pessoas com maior poder aquisitivo. A população mais pobre acaba sendo delegada às comunidades da região, que, pela alta procura, também acaba apresentando valores altos em comparação a outras comunidades da cidade. Essa pouca oferta é observada na quantidade de anúncios para a região, apenas 16,9% do total.
Ainda é interessante observar que, embora seja uma região pequena, apresenta o maior tamanho médio das propriedades, provavelmente resultado dos grandes apartamentos e coberturas presentes em alguns dos prédios de luxo da região.

![Image]()

A seguir, a Zona Oeste. De longe a maior região da cidade, ocupando mais de 70% do território municipal, é uma região 'nova', apresentando um aumento na sua população e desenvolvimento no final do século 20. Possui dois dos bairros mais caros da cidade, Barra da Tijuca e Recreio dos Bandeirantes, próximos da Zona Sul e com um desenvolvimento crescente nos últimos anos, diferenciam-se dos demais bairros da região, que são mais distantes do centro e menos desenvolvidos, possuindo 4 dos 10 bairros mais baratos somente 8 com a média acima da média geral de preços. Ainda assim, apresenta a segunda maior média em todos os valores, e 32,6% dos anúncios analisados.
É interessante notar que, embora não possua a maior área média, possui a maior área geral. Existem muitos bairros mais afastados da região que são 'quase rurais', com muitos sítios e área de mata virgem, o que possibilita a existência de propriedades maiores.

![Image]()

Em terceiro, o Centro é a região mais antiga do Rio e a menor, com apenas 14 bairros presentes na amostra e 4,7% dos anúncios. É uma região histórica, mas que vem sofrendo uma diminuição na sua população redidencial. Essa diminuição na quantidade de moradores e o foco nas propriedades comerciais acaba desvalorizando os valores da região, cuja média é a segunda menor da cidade. Somente 2 bairros possuem uma média inferior a média geral, mas nenhum bairro está entre os 10 mais baratos. Outro ponto a se destacar é a área, que tem a menor média da cidade, o que provavelmente é causado pela baixa disponibilidade de locais para a construção de novas propriedades e o pequeno tamanho da região em si.

![Image]()

Por fim, passamos à análise da Zona Norte. A Zona Norte possui a maior população dentre as regiões do Rio, bem como a maior quantidade de bairros, destacando-se também a prevalência de bairros com menor desenvolvimento. Dos 79 bairros presentes na população, apenas 4 estão acima da média geral, e 6 estão entre os 10 mais baratos. Possui a maior parte dos anúncios, com 45,8% do total, e a menor média em todas as métricas, exceto a área.
Por ser a região com maior população, é também a região com maior procura e, consequentemente, maior oferta de propriedades para aluguel. O alto preço das demais regiões também é um fator que leva a população a procurar oportunidades em regiões mais baratas.

## 6. Conclusão
