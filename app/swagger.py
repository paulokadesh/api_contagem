from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_swagger_ui import get_swaggerui_blueprint

# Configuração do Swagger
SWAGGER_URL = '/docs'  # URL para acessar a UI do Swagger
API_URL = '/static/swagger.json'  # Onde o Swagger vai buscar as especificações

# Configuração do Swagger UI Blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API de Controle de Inventário"
    }
)

# Criação da especificação da API
spec = APISpec(
    title="API de Controle de Inventário",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[MarshmallowPlugin()],
    info={
        "description": "API para gerenciamento de inventário e controle de conferência de produtos",
        "contact": {"email": "seu-email@exemplo.com"}
    }
)

# Definições dos schemas
verificar_codigo_schema = {
    "type": "object",
    "properties": {
        "codigoBarras": {"type": "string", "description": "Código de barras do produto"},
        "usuario": {"type": "string", "description": "Identificador do usuário"}
    },
    "required": ["codigoBarras", "usuario"]
}

verificar_produto_caixa_schema = {
    "type": "object",
    "properties": {
        "numeroCaixa": {"type": "string", "description": "Número da caixa"},
        "codigoProduto": {"type": "string", "description": "Código do produto"},
        "id_caixa": {"type": "string", "description": "ID da caixa"}
    },
    "required": ["numeroCaixa", "codigoProduto", "id_caixa"]
}

carregar_caixa_schema = {
    "type": "object",
    "properties": {
        "numeroCaixa": {"type": "string", "description": "Número da caixa"},
        "usuario": {"type": "string", "description": "Identificador do usuário"}
    },
    "required": ["numeroCaixa", "usuario"]
}

# Adicionando as definições à especificação
spec.components.schema("VerificarCodigo", verificar_codigo_schema)
spec.components.schema("VerificarProdutoCaixa", verificar_produto_caixa_schema)
spec.components.schema("CarregarCaixa", carregar_caixa_schema)

# Documentação das rotas
spec.path(
    path="/verificar_codigo",
    operations={
        "post": {
            "tags": ["Inventário"],
            "summary": "Verifica e registra a conferência de um produto",
            "requestBody": {
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/VerificarCodigo"}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Produto verificado com sucesso",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "mensagem": "Produto verificado com sucesso!",
                                "dados": {
                                    "codigo_barras": "123456789",
                                    "referencia": "REF001",
                                    "descricao": "Produto Exemplo",
                                    "data_conferencia": "2024-03-18T10:00:00",
                                    "usuario": "user123",
                                    "numero": "001",
                                    "item": "001"
                                }
                            }
                        }
                    }
                },
                "400": {"description": "Dados inválidos"},
                "404": {"description": "Produto não encontrado"},
                "500": {"description": "Erro interno do servidor"}
            }
        }
    }
)

spec.path(
    path="/verificar_produto_caixa",
    operations={
        "post": {
            "tags": ["Inventário"],
            "summary": "Verifica se um produto pertence a uma determinada caixa",
            "requestBody": {
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/VerificarProdutoCaixa"}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Produto verificado com sucesso",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "mensagem": "Produto verificado com sucesso",
                                "dados": {}
                            }
                        }
                    }
                },
                "400": {"description": "Dados inválidos"},
                "404": {"description": "Produto ou caixa não encontrado"},
                "500": {"description": "Erro interno do servidor"}
            }
        }
    }
)

spec.path(
    path="/carregar_caixa",
    operations={
        "post": {
            "tags": ["Inventário"],
            "summary": "Carrega informações de uma caixa específica",
            "requestBody": {
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/CarregarCaixa"}
                    }
                }
            },
            "responses": {
                "200": {
                    "description": "Caixa carregada com sucesso",
                    "content": {
                        "application/json": {
                            "example": {
                                "success": True,
                                "mensagem": "Caixa carregada com sucesso",
                                "dados": {}
                            }
                        }
                    }
                },
                "400": {"description": "Dados inválidos"},
                "404": {"description": "Caixa não encontrada"},
                "500": {"description": "Erro interno do servidor"}
            }
        }
    }
) 