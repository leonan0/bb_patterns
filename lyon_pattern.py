from datetime import datetime, timedelta
import pandas as pd
import get_data
from tqdm import tqdm
from configparser import ConfigParser

configs = ConfigParser()
configs.read('config.ini')

def get_3_next(df, i):
    return df.iloc[i+1:i+4]


def set_results(row, i, n_entrada, df):
    next_3_games = get_3_next(df, i+n_entrada)
    r = {'data': row.Data,
         'campeonato': row.Campeonato,
         'hora_inicio_padrao': row.Horario,
         'placar_inicio_padrao': row.Resultado,
         'n_jogos': n_entrada,
         f'hora_apos_jogo': df.iloc[i+n_entrada].Horario,
         f'placar_apos_jogo': df.iloc[i+n_entrada].Resultado,
         'pago_ambas': False,
         'pago_over_2_5': False,
         'pago_over_3_5': False
         }
    c = 1
    for _, v in next_3_games.iterrows():
        if v.ambas_marcam:
            r['pago_ambas'] = v.ambas_marcam
        if v.over_2_5:
            r['pago_over_2_5'] = v.over_2_5
        if v.over_3_5:
            r['pago_over_3_5'] = v.over_3_5

        r['tiro-'+str(c)] = {'hora': v.Horario, 'placar': v.Resultado,
                             'ambas_marcam': v.ambas_marcam, 'over_2_5': v.over_2_5, 'over_3_5': v.over_3_5, }
        c += 1
    return r

def main():
    get_data.main(horas=int(configs['bbtips']['horas']))
    df = pd.read_excel('./data.xlsx')


    camp_euro = df.loc[df.Campeonato == 'EURO'].sort_values(
        'Data').reset_index(drop=True)
    camp_copa = df.loc[df.Campeonato == 'COPA'].sort_values(
        'Data').reset_index(drop=True)
    camp_premier = df.loc[df.Campeonato == 'PREMIER'].sort_values(
        'Data').reset_index(drop=True)
    camp_super = df.loc[df.Campeonato == 'SUPER'].sort_values(
        'Data').reset_index(drop=True)




    campeonatos = [camp_euro, camp_copa, camp_super, camp_premier]
    resultados = []
    for camp in tqdm(campeonatos):
        results = []
        for index, row in camp.iterrows():
            if row.casa >= 0 and row.visitante < row.casa:
                try:
                    if camp_euro.iloc[index+1].visitante == 2:  
                        results.append(set_results(row, index, 1, camp))
                    elif camp_euro.iloc[index+2].visitante == 2:  
                        results.append(set_results(row, index, 2, camp))
                except Exception as ex:
                    print(ex)
        df = pd.DataFrame(results)
        df.to_excel(f'dados_{df.campeonato.iloc[0]}.xlsx', index=False)
        resultados.append(df)

    d = []
    for df in resultados:
        ndf = df.loc[df.data > datetime.today() - timedelta(hours=24)]
        camp = ndf.campeonato.iloc[0]
        ambas = ndf.pago_ambas.value_counts()[1] / ndf.pago_ambas.count() * 100
        over = ndf.pago_over_2_5.value_counts()[1] / ndf.pago_over_2_5.count()*100
        data = {'campeonato': camp,
                'over 2.5': round(over, 2),
                'ambas marcam': round(ambas, 2)
                }
        d.append(data)
    pd.DataFrame(d).to_excel('resultados_lyon.xlsx', index=False)
    print('padrões Lyon salvos')


if __name__ == '__main__':
    main()
