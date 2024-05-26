docs_importation = {
    200: {
        "description": "OK",
        "content": {"application/json": {"example": {"detal" :[{
            "id": 1,
            "quantity_numeric": 522.733,
            "value_numeric": 1732.85,
            "year": 2023,
            "country": "Africa do Sul",
            "quantity": "522.733 Kg",
            "value": "1.732.850 US$",
            "classification": "Vinhas de mesa"
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