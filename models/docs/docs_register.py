docs_register = {
    201: {
        "description": "OK",
        "content": {"application/json": {"example": {"username": "SameName", "email": "name@example"}}}
        },
    409: {
        "description": "Error: Conflict",
        "content": {"application/json": {"example": {"detail": "Conflito, username já existe !"}}}  
        },
    422: {
        "description": "Unprocessable Entity",
        "content": {"application/json": {"example": {"detail": [{"detail" : "O campo senha de ver maior que 5 caracteres"}] }}}  
        },
    500: {
        "description": "Internal Error",
        "content": {"application/json": {"example": {"detail": "Erro interno"}}}
        },
}