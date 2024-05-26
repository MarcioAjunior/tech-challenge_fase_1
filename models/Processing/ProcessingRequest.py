from fastapi import HTTPException
from enum import Enum
from typing import Optional
from pydantic import Field
from models.Scraping import Scraping
from models.SQLAlchemy import SQLAlchemyManager
from models.Processing.Processing import LBProcessing
from bs4 import BeautifulSoup
from helpers.parse_float import parse_float
from models.Processing.ProcessingEnum import EnumClassification

URLS = {
        "processamento" : {
                'url': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03',
                'filtros' : {
                    'Viníferas' : '&subopcao=subopt_01',
                    'Americanas e híbridas' : '&subopcao=subopt_02',
                    'Uvas de mesa' : '&subopcao=subopt_03',
                    'Sem classificação' : '&subopcao=subopt_04'
                }
            }
    }

class ProcessingRequest(Scraping):
    year: int = Field(ge=1970, le=2022)
    classification: Optional[EnumClassification] = None
    
    @classmethod
    def save_many_processing(cls, processings = []):
        with SQLAlchemyManager() as session:
            try:
                session.bulk_insert_mappings(mapper=LBProcessing,mappings=processings)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
                raise HTTPException(status_code= 500,detail='Erro interno')

    def verify_need_scraping(self) -> bool:
        with SQLAlchemyManager() as session:
            processing_year = session.query(LBProcessing).filter_by(year = self.year).first()
            if processing_year:
                return False
            return True
    
    def scraping(self):
        year_param = '&ano=%s' % self.year
        
        url = URLS['processamento']['url'] + year_param
        
        urls = [(key, url+value) for key, value in URLS['processamento']['filtros'].items()]
        
        all_processings = []
        
        for classification, url in urls:
            
            html = ProcessingRequest.make_request(url)
        
            soup = BeautifulSoup(html, 'html.parser')
        
            table = soup.find('table', class_='tb_dados')
            if not table:
                raise HTTPException(status_code= 504, detail='Destino do scraping não alcançável')
        
            lines = table.find_all('tr')[1:-1]
            if not lines:
                raise HTTPException(status_code= 503, detail='Não foi possível obter o resultado do scraping')

            processings = []
            current_type  = ''
            for line in lines:
                cells = line.find_all('td')
                if not cells:
                    continue
                cultive = cells[0].get_text(strip=True)
                is_type = cells[0].get('class', []) == ['tb_item']
                quantity = cells[1].get_text(strip=True) if len(cells) > 1 else None
            
                if is_type:
                    current_type = cultive        
            
                processing = {
                        'cultive': cultive,
                        'quantity': quantity + ' Kg',
                        'quantity_numeric': parse_float(quantity),
                        'is_type': is_type,
                        'type': current_type,
                        'classification' : classification,
                        'year': self.year
                    }
            
                processings.append(processing)
                
            all_processings = all_processings + processings
        
        return ProcessingRequest.save_many_processing(all_processings)
    
    def load(self):
        with SQLAlchemyManager() as session:
            if self.classification is None:
                productions_year = session.query(LBProcessing).filter_by(year = self.year).all()
            else:
                productions_year = session.query(LBProcessing).filter_by(year = self.year, classification = self.classification).all()
            if productions_year:
                return productions_year
            return []