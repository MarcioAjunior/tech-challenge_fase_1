# Tech Challenge - API FastAPI

## Descrição

Este é um projeto desenvolvido como parte do desafio da pós-graduação, referente à atividade da 1ª fase do curso. O projeto é uma API construída com FastAPI e documentada com Swagger. A API realiza um scraping no site da Embrapa (http://vitibrasil.cnpuv.embrapa.br/).

## Funcionalidades

- Realiza scraping de dados do site da Embrapa.
- Documentação interativa com Swagger.

## Pré-requisitos

- Python 3.10 ou superior

## Instalação

### Linux e macOS

1. Clone o repositório:
   ```sh
   git clone git@github.com:MarcioAjunior/tech-challenge_fase_1.git
   cd  tech-challenge_fase_1


2. Crie um ambiente virtual:
   ```sh
   python3 -m venv venv

3. Ative o ambiente virtual:
   ```sh
   source venv/bin/activate

4. Instale as dependencias:
   ```sh
   pip install -r requirements.txt

### Windows

1. Clone o repositório:
   ```sh
   git clone git@github.com:MarcioAjunior/tech-challenge_fase_1.git
   cd  tech-challenge_fase_1

2. Crie um ambiente virtual:
   ```sh
   python -m venv venv

3. Ative o ambiente virtual:
   ```sh
   .\venv\Scripts\activate

4. Instale as dependencias:
   ```sh
   pip install -r requirements.txt

## Sobre esse projeto

É uma API simples que realiza um scraping no site da emprapa. A api possúi 5 endpoints get simples com os dados capturados, além das duas rotas para criação e autenticação de um usuário. Após a captura dos dados as informações são salvas em um banco de dados SQLite. Esse banco relacional segue as regras definidas pelo Diagrama de Entidade e Relacionamento abaixo:


![Descrição da Imagem](DEER.png)


Sobre as rotas:

A documentação interativa está disponívem em http://localhost:8000/docs

### /register

Rota utilizada para cadastrar um usuário, utilizando as informações de _username_, _email_ e _password_ informadas no corpo da requisição, sendo todos os parâmetros obirgatórios, seguindo também algumas validações como email válido, quantidade de caractéres, e unicidade do username.

### /token

Rota que retorna o token de acesso, permitindo acessar as rotas protegidas, é unica rota que utiliza-se de uma requisição _x-www-form-urlencoded_, conforme documentação do fastapi, para autenticação, utiliza o email e password informados na rota register para criação de um token jwt.

### /production

Rota que recebe um parametro query, informada no cabeçalho da requisição. O parâmetro informado é o ano, que obedece algumas validações como o ano estar entre 1970 e 2023, anos em que o site da embrapa possúi dados gerados.

### /processing

Rota que recebe dois parâmetros, sendo somente um deles obrigatório, o ano, que assim como na rota de prodution, deve estar entre um ano inicio e um ano fim conforme a disponibilidade dos dados no site da embrapa. O parâmetro classification é opcional, quando não informado retorna todas as informações indiferente da classificação. Quando informado, filtra o resultado pela classificação informada.

Embora seja possível filtar a busca com o classification, caso o ano informado não tenha informações salvas no banco, o scraping será realizado para todas as classificações dessse ano, salvando-as no banco, e somente o reultado final será filtrado.

### /commercialization

Rota que recebe o parâmetro ano como query do cabeçalho. obedece algumas validações, e consulta no site da emprapa quando não possui os dados salvos no banco local, caso possua somente retorna os dados já carregados anteriormente.

### /importation

Rota que retorna as importações referente ao ano informado como parâmetro, caso ainda não tenho no banco local realiza o scraping. Além do ano, recebe o parâmetro opcinal da classificação.

### /exportation

Rota que retornar as exportações refernte ao ano informado, manteando também o parâmetro opcional de classficação, filtriando por ele quando informado.

## Arquitetura da aplicação

A arquitetura imaginada para o deploy de api foi imaginado conforme modelo c4 abaixo.

![Descrição da Imagem](DEER.png)

A arquitetura é baseada em microserviços, e compõem inicialente de 5 containers, sendo eles:

### 1 Proxy reverso.

Um container Ngix operando em proxy reverso, distribuindo as requisições entre as solicitações realizadas para a API e as solicitações realizadas pra o modelo ML. É o ponto de entrada de toda a arquitetura.

### 2 API.

A API recebe as requisições redirecionadas pelo proxy, recebendo as informações da requisição como _year_ e _classification_, usados para filtrar o resultado da requisição inicial, as informações do parâmetros utilizados estão documentadas em /docs. Caso a informação solicitada encontre-se no banco de dados a api apenas consulta e retornar o resultado conforme parâmetro informados, caso as informações solicitadas ainda não existam no banco de dados, a api realiza um processo de scraping no site da embrapa http://vitibrasil.cnpuv.embrapa.br/ para primeiramente salvar as novas informações e posteriormente retornar para a solicitação inicial.

os detalhes de possíveis resposta da api podem ser visualizados em _/docs_.

### Master DB.

O Master DB é o primeiro banco de dados da aplicação, utilizada pela api para escrita dos resultados da consulta do site da EMBRAPA, e utilizado pela api para consultar por resultados já buscados anteriormente. Este banco de dados é utilizado somente pela API.

### Slave DB.

O slave DB opera justamente como um banco slave, tendo o Master DB como banco princapal, master. É um banco de dados réplica utilizado somente pelo modelo ML para realização de calculos correlação precisão além de predição e análise descritiva dos dados já coletados. 

### Modelo ML.

O container do modelo irá apenas expor os resultados do modelo, que irá realizar predições e análises descritivas realizadas. O modeo também irá operar atrás do proxy, recebendo as requisições que lhe forem redirecionadas. Para receber as requisições o artefado do modelora irá utilizar-se de uma api no container. que irá intermediar a comunicação entre os containers do banco slave e proxy.