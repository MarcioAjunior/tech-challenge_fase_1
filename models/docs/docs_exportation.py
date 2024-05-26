docs_exportation = {
    200: {
        "description": "OK",
        "content": {"application/json": {"example": {"detal" :[{
            "quantity": "-",
            "value": "-",
            "country": "Afeganistão",
            "classification": "Vinhas de mesa",
            "quantity_numeric": 0,
            "id": 1,
            "value_numeric": 0,
            "year": 2023
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