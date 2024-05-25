from pydantic import BaseModel
from models.SQLAlchemy import SQLAlchemyManager
import requests

URLS = {
        "producao" : {
            'url' : 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02'
        },
        "processamento" : {
                'url': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03',
                'filtros' : {
                    'viniferas' : '&subopcao=subopt_01',
                    'americanas_hibridas' : '&subopcao=subopt_02',
                    'uvas_de_mesa' : '&subopcao=subopt_03',
                    'sem_classificacao' : '&subopcao=subopt_04'
                }
            },
        "comercializacao" : {
            'url' : 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04'
        },
        "importacao" : {
            'url' : 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05',
            'filtros' : {
                'vinho_de_mesa' : '&subopcao=subopt_01',
                'espumantes' : '&subopcao=subopt_02',
                'uvas_frescas' : '&subopcao=subopt_03',
                'uvas_passas' : '&subopcao=subopt_04',
                'suco_de_uva' : '&subopcao=subopt_05'
            }
        },
        "exportacao" : {
            'url' : 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06',
            'filtros' : {
                'vinho_de_mesa' : '&subopcao=subopt_01',
                'espumantes' : '&subopcao=subopt_02',
                'uvas_frescas' : '&subopcao=subopt_03',
                'suco_de_uva' : '&subopcao=subopt_04'
            }
        }
    }

class Scraping(BaseModel):    
    
    @classmethod   
    def make_request(cls, url):
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.text
        print(response.status_code)
        return None
    
                    
            
            
