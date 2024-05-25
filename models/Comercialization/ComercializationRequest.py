from fastapi import HTTPException
from pydantic import Field
from models.Scraping import Scraping
from models.SQLAlchemy import SQLAlchemyManager
from models.Comercialization.Comercialization import LBComercialization
from bs4 import BeautifulSoup
from helpers.parse_float import parse_float

URLS = {
        "comercializacao" : {
            'url' : 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04'
        }
    }

class ComercializationRequest(Scraping):
    year: int = Field(ge=1970, le=2023)
    
    @classmethod
    def save_many_commercialization(cls, comercializations = []):
        with SQLAlchemyManager() as session:
            try:
                session.bulk_insert_mappings(mapper=LBComercialization,mappings=comercializations)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
                raise HTTPException(status_code= 500,detail='Erro interno')
    
    def verify_need_scraping(self) -> bool:
        with SQLAlchemyManager() as session:
            comercialization_year = session.query(LBComercialization).filter_by(year = self.year).first()
            if comercialization_year:
                return False
            return True
        
    def scraping(self):
        year_param = '&ano=%s' % self.year
        
        url = URLS['comercializacao']['url'] + year_param
        
        html = ComercializationRequest.make_request(url)
        
        soup = BeautifulSoup(html, 'html.parser')
        
        table = soup.find('table', class_='tb_dados')
        if not table:
            raise ValueError("A tabela de dados não foi encontrada no HTML.")
        
        lines = table.find_all('tr')[1:-1]
        if not lines:
            raise ValueError("Linhas da tabela não foram encontradas ou a tabela está vazia.")

        commercializations = []
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
                
            commercialization = {
                    'product': product,
                    'quantity': quantity,
                    'quantity_numeric': parse_float(quantity),
                    'is_type': is_type,
                    'type': current_type,
                    'year': self.year
                }
            
            commercializations.append(commercialization)
        
        return ComercializationRequest.save_many_commercialization(commercializations)
        
    def load(self):
        with SQLAlchemyManager() as session:
            commercializations_year = session.query(LBComercialization).filter_by(year = self.year).all()
            if commercializations_year:
                return commercializations_year
            return []
