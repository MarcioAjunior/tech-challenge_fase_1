docs_production = {
    200: {
        "description": "OK",
        "content": {"application/json": {"example": {"detal" :[{
            "product": "VINHO DE MESA",
            "quantity": "154.264.651 L",
            "is_type": True,
            "year": 1971,
            "quantity_numeric": 154264.651,
            "id": 52,
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