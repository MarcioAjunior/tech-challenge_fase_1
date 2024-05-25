docs_login = {
    200: {
        "description": "OK",
        "content": {"application/json": {"example": {"name": "Nome", "email": "name@example", "token": "hashedToken"}}}
        },
    404: {
        "description": "Email ou senha incorretos",
        "content": {"application/json": {"example": {"detail": "Email ou senha incorretos"}}}
        },
    422: {
        "description": "Erro de validação dos campos",
        "content": {"application/json": {"example": {"detail": [{"detail" : "Campo email é obrigatório"}] }}}
        },
    500: {
        "description": "Erro interno",
        "content": {"application/json": {"example": {"detail": "Erro interno"}}}
        },
}