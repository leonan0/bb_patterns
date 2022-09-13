import get_data
import pandas as pd
from tqdm import tqdm
from utils import get_next_range
get_data.main(5, 24, False)
df = pd.read_excel('./data.xlsx')

odds_guia = df.over_2_5_odd.unique()
camps = ['PREMIER', 'EURO', 'COPA', 'SUPER']


def analise_camp(df, camp):
    df_camp = df.sort_values('timestamp').reset_index(drop=True)
    dados = []
    print(f'start {camp}')
    for index, row in df_camp.iterrows():
        if row.over_2_5_odd in odds_guia:
            cont = 0
            over_3_5 = False
            while not over_3_5:
                try:
                    c = df_camp.iloc[index + cont]  # type: ignore
                    if c.over_3_5 == True:  # type: ignore
                        over_3_5 = True
                        dados.append({
                            'tiro': 0,
                            'horario': row.Horario,
                            'total_gols': row.total_gols,
                            'over_2_5': row.over_2_5,
                            'over_3_5': row.over_3_5,
                            'over_2_5_odd': row.over_2_5_odd,
                            'over_3_5_odd': row.over_3_5_odd,
                            'tirox': cont,
                            'horariox': c.Horario,
                            'total_golsx': c.total_gols,
                            'over_2_5x': c.over_2_5,
                            'over_3_5x': c.over_3_5,
                            'over_2_5_oddx': c.over_2_5_odd,
                            'over_3_5_oddx': c.over_3_5_odd,
                        })
                    cont += 1
                except:
                    over_3_5 = True
                    pass
    # df_camp.query(f'over_2_5_odd in {odds_guia}')[
    #     'over_2_5_odd'].value_counts().to_excel(f'{camp}_count.xlsx')
    pd.DataFrame(dados).groupby(['over_2_5_odd', 'tirox'])[
        'tirox'].count().to_excel(f'{camp}.xlsx')

def main():
    for camp in camps:
        analise_camp(df.loc[df.Campeonato == camp].copy(), camp)


if __name__ == '__main__':
    main()