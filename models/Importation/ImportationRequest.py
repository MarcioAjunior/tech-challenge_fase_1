from fastapi import HTTPException
from enum import Enum
from typing import Optional
from pydantic import Field
from models.Scraping import Scraping
from models.SQLAlchemy import SQLAlchemyManager
from models.Importation.Importation import LBImportation
from bs4 import BeautifulSoup
from helpers.parse_float import parse_float

URLS = {
        "importacao" : {
            'url' : 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05',
            'filtros' : {
                'Vinhas de mesa' : '&subopcao=subopt_01',
                'Espumantes' : '&subopcao=subopt_02',
                'Uvas frescas' : '&subopcao=subopt_03',
                'Uvas passas' : '&subopcao=subopt_04',
                'Suco de uva' : '&subopcao=subopt_05'
            }
        }
    }

class EnumClassification(str, Enum):
    vinhos_de_mesa = "Vinhas de mesa"
    espumantes = "Espumantes"
    uvas_frescas = "Uvas frescas"
    uvas_passas = "Uvas passas"
    suco_de_uva = 'Suco de uva'
    
class ImportationRequest(Scraping):
    year: int = Field(ge=1970, le=2023)
    classification: Optional[EnumClassification] = None
    
    @classmethod
    def save_many_importations(cls, imporations = []):
        with SQLAlchemyManager() as session:
            try:
                session.bulk_insert_mappings(mapper=LBImportation,mappings=imporations)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
                raise HTTPException(status_code= 500,detail='Erro interno')
    
    def verify_need_scraping(self) -> bool:
        with SQLAlchemyManager() as session:
            importation_year = session.query(LBImportation).filter_by(year = self.year).first()
            if importation_year:
                return False
            return True
    
    def scraping(self):
        year_param = '&ano=%s' % self.year
        
        url = URLS['importacao']['url'] + year_param
        
        urls = [(key, url+value) for key, value in URLS['importacao']['filtros'].items()]
        
        all_importations = []
        
        for classification, url in urls:
            
            html = ImportationRequest.make_request(url)
        
            soup = BeautifulSoup(html, 'html.parser')
        
            table = soup.find('table', class_='tb_dados')
            if not table:
                raise HTTPException(status_code= 504, detail='Destino do scraping não alcançável')
        
            lines = table.find_all('tr')[1:-1]
            if not lines:
                raise HTTPException(status_code= 503, detail='Não foi possível obter o resultado do scraping')

            importations = []
            for line in lines:
                cells = line.find_all('td')
                if not cells:
                    continue
                country = cells[0].get_text(strip=True)
                quantity = cells[1].get_text(strip=True) if len(cells) > 1 else None
                value = cells[2].get_text(strip=True) if len(cells) > 2 else None  
            
                importation = {
                        'country': country,
                        'quantity': quantity + ' Kg',
                        'quantity_numeric': parse_float(quantity),
                        'value': value + ' US$',
                        'value_numeric': parse_float(value),
                        'classification' : classification,
                        'year': self.year
                    }
            
                importations.append(importation)
                
            all_importations = all_importations + importations
            
        return ImportationRequest.save_many_importations(all_importations)
    
    def load(self):
        with SQLAlchemyManager() as session:
            if self.classification is None:
                imporatation_year = session.query(LBImportation).filter_by(year = self.year).all()
            else:
                imporatation_year = session.query(LBImportation).filter_by(year = self.year, classification = self.classification).all()
            if imporatation_year:
                return imporatation_year
            return []    
        