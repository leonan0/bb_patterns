import pandas as pd
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import configparser
import requests

config = configparser.ConfigParser()
configs = config.read('./config.ini')
try:
    bbtips = config['bbtips']
except KeyError:
    import generate_config_file
    generate_config_file.main()
    raise Exception('Favor executar novamente')

class Campeonatos(Enum):
    EURO = 1
    COPA = 2
    PREMIER = 3
    SUPER = 4
    TODOS = 5


class Jogo(BaseModel):
    Campeonato: str
    Horario: str
    Hora: int
    Minuto: int
    TimeA: str
    TimeB: str
    Resultado: Optional[str] = None
    Resultado_FT: Optional[str] = None
    Resultado_HT: Optional[str] = None
    Odds: List[float]
    Odd: str
    PrimeiroMarcar: str
    UltimoMarcar: str
    Vencedor_HT_FT: Optional[str] = None
    Resultado_HT_Odd: Optional[str] = None
    Id: Optional[int]
    timedelta: float = 0
    Data: Optional[datetime] = None
    casa_vence: Optional[bool] = False
    visitante_vence: Optional[bool] = False
    dia: Optional[int]

    casa_vence: Optional[bool] = False
    ambas_marcam: Optional[bool] = False
    over_1_5: Optional[bool] = False
    over_2_5: Optional[bool] = False
    over_3_5: Optional[bool] = False

    ambas_marcam_odd: Optional[float] = None
    over_1_5_odd: Optional[float] = None
    over_2_5_odd: Optional[float] = None
    over_3_5_odd: Optional[float] = None

    casa: Optional[int] = None
    visitante: Optional[int] = None

    def __init__(self, **data):
        data = self.correct_data(**data)
        super().__init__(**data)
        self.correct_date()
        self.set_results()

    @staticmethod
    def correct_data(**data):
        try:
            data['Minuto'] = int(data['Minuto'])
            if 'Odds' in data.keys():
                data['Odds'] = [float(x) if len(
                    x) > 0 else 0.0 for x in data['Odds'].split('|')]
            else:
                data['Odds'] = [12*0]

            data['Hora'] = int(data['Hora'])
            return data
        except Exception as ex:
            print(ex)
            return data

    def correct_date(self):
        self.Data = datetime.today().replace(
            hour=self.Hora, minute=self.Minuto, second=0, microsecond=0) - timedelta(days=self.timedelta)
        self.dia = self.Data.day

    def set_results(self):
        if self.Resultado != None:
            self.casa = int(self.Resultado.split('-')[0][0])
            self.visitante = int(self.Resultado.split('-')[1][0])
            if self.casa > self.visitante:
                self.casa_vence = True
            elif self.visitante > self.casa:
                self.visitante_vence = True
            self.validate_ambas()
            self.validate_over()
        self.set_odds()

    def validate_casa_vence(self):
        if self.casa and self.visitante:
            if self.casa > self.visitante:
                self.casa_vence = True

    def validate_ambas(self):
        if self.casa and self.visitante:
            if self.casa > 0 and self.visitante > 0:
                self.ambas_marcam = True

    def set_odds(self):
        self.ambas_marcam_odd = float(self.Odds[8])
        self.over_1_5_odd = float(self.Odds[1])
        self.over_2_5_odd = float(self.Odds[2])
        self.over_3_5_odd = float(self.Odds[3])

    def validate_over(self):
        if self.casa and self.visitante:
            total = self.casa + self.visitante
            if total > 3.5:
                self.over_3_5 = True
            if total > 2.5:
                self.over_2_5 = True
            if total > 1.5:
                self.over_1_5 = True
        else:
            pass

def get_futebol_data(liga=5, futuro=False, horas=3, tipo_odd=''):
    headers = {
        'authorization': bbtips['auth_token'],
        'content-type': 'application/json',
    }
    print(f'getting data from {Campeonatos(liga).name}')
    print(f'qtd hrs {horas}')
    url = f"{bbtips['futebol_virtual_url']}?liga={liga}&futuro={futuro}&Horas=Horas{horas}&tipoOdd={tipo_odd}"

    response = requests.request("GET", url, headers=headers)
    return response

def main(liga=5, horas=48, futuro=True):
    r = get_futebol_data(liga=liga, horas=horas, futuro=futuro)

    jogos = []
    for camp_index, camp in enumerate(r.json()):
        count_horas = 0
        for index, linha in enumerate(camp['Linhas']):
            for jogo in linha['Colunas']:
                if 'Odds' in jogo.keys():
                    jogos.append(
                        Jogo(**jogo, timedelta=count_horas, Campeonato=Campeonatos(camp_index+1)._name_).__dict__)
                    
            if 'Hora' not in linha.keys():
                count_horas += 1
                    
    print(f'salvos {len(jogos)} jogos')

    pd.DataFrame(jogos).to_excel('data.xlsx', index=False)
    # pd.DataFrame(jogos).to_parquet('data.parquet', index=False)

    print('Save')


if __name__ == '__main__':
    main(5,48,True)
