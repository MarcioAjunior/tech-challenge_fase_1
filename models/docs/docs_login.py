docs_login = {
    200: {
        "description": "OK",
        "content": {"application/json": {"example": {"name": "Nome", "email": "name@example", "token": "hashedToken"}}}
        },
    404: {
        "description": "Error: Not Found",
        "content": {"application/json": {"example": {"detail": "Não encontrado uma conta para o usuário : samename"}}}
        },
    404: {
        "description": "Error: Not Found",
        "content": {"application/json": {"example": {"detail": "Username ou senha incorretos !"}}}
        },
    500: {
        "description": "Internal Error",
        "content": {"application/json": {"example": {"detail": "Erro interno"}}}
        },
}