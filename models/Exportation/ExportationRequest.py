from fastapi import HTTPException
from enum import Enum
from typing import Optional
from pydantic import Field
from models.Scraping import Scraping
from models.SQLAlchemy import SQLAlchemyManager
from models.Exportation.Exportation import LBExportation
from bs4 import BeautifulSoup
from helpers.parse_float import parse_float

URLS = {
        "exportacao" : {
            'url' : 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06',
            'filtros' : {
                'Vinhas de mesa' : '&subopcao=subopt_01',
                'Espumantes' : '&subopcao=subopt_02',
                'Uvas frescas' : '&subopcao=subopt_03',
                'Suco de uva' : '&subopcao=subopt_04'
            }
        }
    }

class EnumClassification(str, Enum):
    vinhos_de_mesa = "Vinhas de mesa"
    espumantes = "Espumantes"
    uvas_frescas = "Uvas frescas"
    suco_de_uva = 'Suco de uva'
    
class ExportationRequest(Scraping):
    year: int = Field(ge=1970, le=2023)
    classification: Optional[EnumClassification] = None
    
    @classmethod
    def save_many_exportations(cls, exportations = []):
        with SQLAlchemyManager() as session:
            try:
                session.bulk_insert_mappings(mapper=LBExportation,mappings=exportations)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
                raise HTTPException(status_code= 500,detail='Erro interno')
    
    def verify_need_scraping(self) -> bool:
        with SQLAlchemyManager() as session:
            exportation_year = session.query(LBExportation).filter_by(year = self.year).first()
            if exportation_year:
                return False
            return True
    
    def scraping(self):
        year_param = '&ano=%s' % self.year
        
        url = URLS['exportacao']['url'] + year_param
        
        urls = [(key, url+value) for key, value in URLS['exportacao']['filtros'].items()]
        
        all_exportations = []
        
        for classification, url in urls:
            
            html = ExportationRequest.make_request(url)
        
            soup = BeautifulSoup(html, 'html.parser')
        
            table = soup.find('table', class_='tb_dados')
            if not table:
                raise HTTPException(status_code= 504, detail='Destino do scraping não alcançável')
        
            lines = table.find_all('tr')[1:-1]
            if not lines:
                raise HTTPException(status_code= 503, detail='Não foi possível obter o resultado do scraping')

            exportations = []
            for line in lines:
                cells = line.find_all('td')
                if not cells:
                    continue
                country = cells[0].get_text(strip=True)
                quantity = cells[1].get_text(strip=True) if len(cells) > 1 else None
                value = cells[2].get_text(strip=True) if len(cells) > 2 else None  
            
                exportation = {
                        'country': country,
                        'quantity': quantity,
                        'quantity_numeric': parse_float(quantity),
                        'value': value,
                        'value_numeric': parse_float(value),
                        'classification' : classification,
                        'year': self.year
                    }
            
                exportations.append(exportation)
                
            all_exportations = all_exportations + exportations
            
        return ExportationRequest.save_many_exportations(all_exportations)
    
    def load(self):
        with SQLAlchemyManager() as session:
            if self.classification is None:
                exportation_year = session.query(LBExportation).filter_by(year = self.year).all()
            else:
                exportation_year = session.query(LBExportation).filter_by(year = self.year, classification = self.classification).all()
            if exportation_year:
                return exportation_year
            return []    
        