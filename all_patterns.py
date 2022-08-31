from tqdm import tqdm
import pandas as pd
import get_data

from configparser import ConfigParser

configs = ConfigParser()
configs.read('config.ini')


def get_next_range(df, start_index, range, gap):
    nstart = start_index + 1 + gap
    return df.loc[nstart:nstart+range - 1]


def get_patterns(df, campeonato, resultado, range, gap):
    ndf = df.loc[df.Campeonato == campeonato].sort_values(
        ['Data']).reset_index(drop=True).reset_index()
    pattern = ndf.loc[ndf.Resultado == resultado]
    to_return = []
    for index, row in pattern.iterrows():
        r = {
            'campeonato': row.Campeonato,
            'horario_inicio_padrao': row.Horario,
            'casa': row.TimeA,
            'visitante': row.TimeB,
            'resultado': row.Resultado,
            'jogos_apos': gap + 1,
            'range': range,
            'tiros': [],
            'casa_vence': [],
            'ambas_marcam': [],
            'over_2_5': [],
            'over_3_5': [],
            'ambas_marcam_odds': [],
            'over_2_5_odds': [],
            'over_3_5_odds': [],
            'prox_resultados': [],
            'confrontos': [],
        }
        next_range = get_next_range(ndf, row['index'], range, gap)
        for nindex, nrow in next_range.iterrows():
            r['tiros'].append(nrow.Horario)
            r['ambas_marcam'].append(nrow.ambas_marcam)
            r['casa_vence'].append(nrow.casa_vence)

            r['over_2_5'].append(nrow.over_2_5)
            r['over_3_5'].append(nrow.over_3_5)
            r['ambas_marcam_odds'].append(nrow.ambas_marcam_odd)
            r['over_2_5_odds'].append(nrow.over_2_5_odd)
            r['over_3_5_odds'].append(nrow.over_3_5_odd)
            r['prox_resultados'].append(nrow.Resultado)
            r['confrontos'].append(
                {'casa': nrow.TimeA, 'visitante': nrow.TimeB})
        to_return.append(r)
    return to_return


def analise_mercados(df, mercado):
    to_return = {'mercado': mercado,
                 }
    cont_green = 0
    an_green = []
    an_red = []
    cont_aux_green = 0
    cont_aux_red = 0
    total = 0
    for index, row in df.iterrows():

        if True in row[mercado]:
            cont_aux_red = 0
            cont_green += 1
            cont_aux_green += 1
            an_green.append(cont_aux_green)
        else:
            cont_aux_green = 0
            cont_aux_red += 1
            an_red.append(cont_aux_red)
    an_green.sort()
    an_red.sort()

    to_return['campeonato'] = df.campeonato.iloc[0]
    to_return['jogos_apos'] = df.jogos_apos.iloc[0]
    to_return['resultado'] = df.resultado.iloc[0]
    to_return['range'] = df.range.iloc[0]

    to_return['amostragem'] = df.campeonato.count()
    to_return['greens'] = cont_green
    if len(an_green) > 0:
        to_return['max_green_consec'] = an_green[-1]
    else:
        to_return['max_green_consec'] = 0

    if len(an_red) > 0:
        to_return['max_red_consec'] = an_red[-1]
    else:
        to_return['max_red_consec'] = 0

    to_return['% acerto'] = round(
        to_return['greens'] / to_return['amostragem'] * 100, 2)
    return to_return


def main():
    try:
        pd.DataFrame().to_excel('patterns.xlsx')
        pd.DataFrame().to_excel('resultados.xlsx')

    except PermissionError:
        raise Exception('Favor fechar o arquivo "patterns.xsls" e/ou "resultados.xlsx')

    get_data.main(5, int(configs['bbtips']['horas']), False)

    df = pd.read_excel('data.xlsx')

    camps = ['EURO', "COPA", "SUPER", "PREMIER"]
    dfs = {}

    for camp in camps:
        dfs[camp] = df.loc[df.Campeonato == camp]

    mercados = [
        # 'ambas_marcam', 
        # 'over_2_5',
        'over_3_5',
        # 'casa_vence']


    n_dfs = []
    data = []
    for df in dfs:
        print(f'Analisando {df}')
        ndf = dfs[df]
        ndf = ndf.sort_values('Resultado')
        for resultado in tqdm(ndf.Resultado.unique()):
            for i in range(0, int(configs['bbtips']['gap'])):
                patters_n = get_patterns(
                    ndf, df, resultado, int(configs['bbtips']['range']), i)
                df3 = pd.DataFrame(patters_n)
                n_dfs.extend(patters_n)
                for mercado in mercados:
                    analise = analise_mercados(df3, mercado)
                    if analise['% acerto'] >= int(configs['bbtips']['min_acert']) and analise['amostragem'] > int(configs['bbtips']['min_amostragem']):
                        data.append(analise)

    if len(data) > 0:
        pd.DataFrame(data).sort_values('amostragem', ascending=False).to_excel(
            'patterns.xlsx', index=False)
    else:
        print('Nenhum padrão encontrado')


    pd.DataFrame(n_dfs).to_excel('resultados.xlsx', index=False)



if __name__ == '__main__':
    main()
