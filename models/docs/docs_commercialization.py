docs_commercialization = {
    200: {
        "description": "OK",
        "content": {"application/json": {"example": {"detal" :[{
            "is_type": True,
            "product": "VINHO DE MESA",
            "quantity": "108.031.792",
            "year": 1975,
            "id": 1,
            "quantity_numeric": 108031.792,
            "type": "VINHO DE MESA"
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