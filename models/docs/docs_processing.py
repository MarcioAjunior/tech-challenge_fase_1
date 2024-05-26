docs_processing = {
    200: {
        "description": "OK",
        "content": {"application/json": {"example": {"detal" :[{
            "quantity_numeric": 24795.507,
            "id": 1,
            "type": "TINTAS",
            "year": 1990,
            "cultive": "TINTAS",
            "quantity": "24.795.507 Kg",
            "is_type": True,
            "classification": "Viníferas"
    }]}}}
        },
    401 : {
        "description": "Unauthorized",
        "content": {"application/json": {"example": {"detail": {"detail" : "Usuario não autenticado"} }}}
    },
    504: {
        "description": "Gateway Timeout",
        "content": {"application/json": {"example": {"detail": "Destino do scraping não alcançável"}}}
    },
    503: {
        "description": "Service Unavailable",
        "content": {"application/json": {"example": {"detail": "Não foi possível obter o resultado do scraping"}}}
    },
    500: {
        "description": "Internal Error",
        "content": {"application/json": {"example": {"detail": "Erro interno"}}}
    }
}