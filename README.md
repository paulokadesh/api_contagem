# API de Controle de Inventário

API REST desenvolvida em Python com Flask para gerenciamento de inventário e controle de conferência de produtos.

## Estrutura do Projeto

```
.
├── app/
│   ├── database/
│   │   └── connection.py     # Configuração de conexão com o banco de dados
│   ├── models/
│   │   └── inventory.py      # Modelo de dados do inventário
│   └── routes/
│       └── inventory.py      # Rotas da API
├── .env                      # Configurações do ambiente (não versionado)
├── .env.example             # Exemplo de configurações
├── main.py                  # Arquivo principal da aplicação
└── requirements.txt         # Dependências do projeto
```

## Requisitos

- Python 3.8 ou superior
- MySQL Server
- Bibliotecas Python (ver requirements.txt)

## Configuração do Ambiente

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure o arquivo .env:
- Copie o arquivo .env.example para .env
- Preencha as variáveis com suas configurações:
```
DB_HOST=localhost          # Host do banco de dados MySQL
DB_USER=seu_usuario       # Usuário do MySQL
DB_PASSWORD=sua_senha     # Senha do MySQL
DB_NAME=nome_do_banco    # Nome do banco de dados
APP_PORT=8082            # Porta da aplicação
```

## Endpoints da API

### 1. Verificar Código `/verificar_codigo`
- **Método**: POST
- **Descrição**: Verifica e registra a conferência de um produto
- **Payload**:
```json
{
    "codigoBarras": "string",
    "usuario": "string"
}
```
- **Resposta de Sucesso**:
```json
{
    "success": true,
    "mensagem": "Produto verificado com sucesso!",
    "dados": {
        "codigo_barras": "string",
        "referencia": "string",
        "descricao": "string",
        "data_conferencia": "string",
        "usuario": "string",
        "numero": "string",
        "item": "string"
    }
}
```

### 2. Verificar Produto na Caixa `/verificar_produto_caixa`
- **Método**: POST
- **Descrição**: Verifica se um produto pertence a uma determinada caixa
- **Payload**:
```json
{
    "numeroCaixa": "string",
    "codigoProduto": "string",
    "id_caixa": "string"
}
```
- **Resposta de Sucesso**:
```json
{
    "success": true,
    "mensagem": "Produto verificado com sucesso",
    "dados": {
        // Dados do produto e caixa
    }
}
```

### 3. Carregar Caixa `/carregar_caixa`
- **Método**: POST
- **Descrição**: Carrega informações de uma caixa específica
- **Payload**:
```json
{
    "numeroCaixa": "string",
    "usuario": "string"
}
```
- **Resposta de Sucesso**:
```json
{
    "success": true,
    "mensagem": "Caixa carregada com sucesso",
    "dados": {
        // Dados da caixa
    }
}
```

## Tratamento de Erros

A API retorna os seguintes códigos de status HTTP:
- 200: Sucesso
- 400: Erro de validação dos dados enviados
- 404: Recurso não encontrado
- 500: Erro interno do servidor

## Dependências Principais

- Flask (2.2.5): Framework web
- Flask-CORS (4.0.0): Suporte a CORS
- mysql-connector-python (8.1.0): Conexão com MySQL
- python-dotenv (1.0.0): Gerenciamento de variáveis de ambiente
- python-dateutil (2.8.2): Manipulação de datas

## Segurança

- Todas as senhas e configurações sensíveis devem ser armazenadas no arquivo .env
- O arquivo .env não deve ser versionado
- Recomenda-se usar HTTPS em produção

## Desenvolvimento

Para executar em modo desenvolvimento:
```bash
python main.py
```
A API estará disponível em `http://localhost:8082` (ou na porta configurada no .env)

## Suporte

Em caso de dúvidas ou problemas:
1. Verifique se o arquivo .env está configurado corretamente
2. Confirme se o MySQL está em execução
3. Verifique os logs da aplicação para mais detalhes sobre erros 