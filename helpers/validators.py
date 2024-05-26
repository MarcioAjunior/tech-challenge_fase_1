from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

async def validations(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_error = {
        'missing' : 'Campo %s é obrigatório',
        'string_too_short' : 'O campo %s deve ter pelo menos 5 caracteres',
        'string_too_long'  : 'O campo %s deve ter no máximo 20 caracteres',
        'string_pattern_mismatch' : 'O campo %s deve ser um email válido',
        'int_parsing' : 'O campo %s precisa ser um inteiro válido',
        'greater_than_equal' : 'O campo %s precisa ser maior que 1969',
        'less_than_equal' : 'O campo %s precisa ser menor que 2024'
    }
    
    custom_errors = []
    for error in errors:
        fields = [name for name in error["loc"] if name != 'body']

        if error["type"] == 'json_invalid' :
            custom_errors.append({
                "error": 'JSON inválido'
            })
        elif error["type"] == 'less_than_equal':
            value = error.get('ctx').get('le')
            custom_errors.append({
                "error" : 'O campo %s não pode ser maior que %s' % (','.join(fields), value)    
            })
        elif error["type"] == 'enum':
            expected = error.get('ctx').get('expected')
            custom_errors.append({
                    "error" : 'O campo classification espera um valor entre %s' % expected     
                })
        elif error["type"] in custom_error:
            custom_errors.append({
            "error": custom_error.get(error["type"], error["msg"]) % ','.join(fields)
        })
        else:
             custom_errors.append({
                "error": (error["msg"])
            })
    
    return JSONResponse(
        status_code=422,
        content={"detail": custom_errors}
    )
