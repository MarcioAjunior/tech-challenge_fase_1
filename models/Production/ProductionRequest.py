from fastapi import HTTPException
from pydantic import Field
from models.Scraping import Scraping
from models.SQLAlchemy import SQLAlchemyManager
from models.Production.Production import LBProduction
from bs4 import BeautifulSoup
from helpers.parse_float import parse_float


URLS = {
        "producao" : {
            'url' : 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02'
        }
    }

class ProductionRequest(Scraping):
    year: int = Field(ge=1970, le=2023)
    
    @classmethod
    def save_many_production(cls, productions = []):
        with SQLAlchemyManager() as session:
            try:
                session.bulk_insert_mappings(mapper=LBProduction,mappings=productions)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
                raise HTTPException(status_code= 500,detail='Erro interno')
                
    
    def verify_need_scraping(self) -> bool:
        with SQLAlchemyManager() as session:
            production_year = session.query(LBProduction).filter_by(year = self.year).first()
            if production_year:
                return False
            return True
        
    def scraping(self):
        year_param = '&ano=%s' % self.year
        
        url = URLS['producao']['url'] + year_param
        
        html = ProductionRequest.make_request(url)
        
        soup = BeautifulSoup(html, 'html.parser')
        
        table = soup.find('table', class_='tb_dados')
        
        
        if not table:
            raise HTTPException(status_code= 504, detail='Destino do scraping não alcançável')
        
        lines = table.find_all('tr')[1:-1]
        if not lines:
            raise HTTPException(status_code= 503, detail='Não foi possível obter o resultado do scraping')

        produtions = []
        current_type  = ''
        for line in lines:
            cells = line.find_all('td')
            if not cells:
                continue
            product = cells[0].get_text(strip=True)
            is_type = cells[0].get('class', []) == ['tb_item']
            quantity = cells[1].get_text(strip=True) if len(cells) > 1 else None
            
            if is_type:
                current_type = product        
                
            production = {
                    'product': product,
                    'quantity': quantity + ' L',
                    'quantity_numeric': parse_float(quantity), 
                    'is_type': is_type,
                    'type': current_type,
                    'year': self.year
                }
            
            produtions.append(production)
        
        return ProductionRequest.save_many_production(produtions)
        
    def load(self):
        with SQLAlchemyManager() as session:
            productions_year = session.query(LBProduction).filter_by(year = self.year).all()
            if productions_year:
                return productions_year
            return []
    