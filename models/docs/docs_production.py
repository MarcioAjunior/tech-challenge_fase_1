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
        "description": "Usuario não autenticado",
        "content": {"application/json": {"example": {"detail": {"detail" : "Usuario não autenticado"} }}}
    },
    422: {
        "description": "Erro de validação dos campos",
        "content": {"application/json": {"example": {"detail": [{"detail" : "O campo year precisa ser maior que 1969"}] }}}
        },
    504: {
        "description": "Destino do scraping não alcançável",
        "content": {"application/json": {"example": {"detail": "Destino do scraping não alcançável"}}}
    },
    503: {
        "description": "Não foi possível obter o resultado do scraping",
        "content": {"application/json": {"example": {"detail": "Não foi possível obter o resultado do scraping"}}}
    },
    500: {
        "description": "Erro interno",
        "content": {"application/json": {"example": {"detail": "Erro interno"}}}
    }
}