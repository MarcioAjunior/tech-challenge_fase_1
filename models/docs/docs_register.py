docs_register = {
    201: {
        "description": "OK",
        "content": {"application/json": {"example": {"name": "SameName", "email": "name@example"}}}
        },
    409: {
        "description": "Email já cadastrado",
        "content": {"application/json": {"example": {"detail": "Email já cadastrado"}}}  
        },
    422: {
        "description": "Erro de validação dos campos",
        "content": {"application/json": {"example": {"detail": [{"detail" : "O campo senha de ver maior que 5 caracteres"}] }}}  
        },
    500: {
        "description": "Erro interno",
        "content": {"application/json": {"example": {"detail": "Erro interno do servidor"}}}
        },
}