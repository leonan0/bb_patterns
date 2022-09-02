import get_data
import pandas as pd

get_data.main(horas=24)

df_all = pd.read_excel('./data.xlsx')
camps = df_all.Campeonato.unique()
dfs = []

try:
    pd.DataFrame().to_excel('minutagens.xlsx')
except PermissionError as e:
    raise Exception(f'Favor fechar o arquivo {e.filename}')

for camp in camps:
    df = df_all.loc[df_all.Campeonato == camp].copy()
    df.sort_values('Data', inplace=True)
    s = {'campeonato': camp, 'data': df}
    dfs.append(s)


def set_sequences(minutos, len_seq=4):
    seqs = []
    nminutos = list(minutos.copy())
    nminutos.extend(list(minutos[:3]))
    for index, _ in enumerate(nminutos):
        seq = nminutos[index:index+len_seq]
        if len(seq) < len_seq:
            pass
        else:
            seqs.append(seq)
    return seqs


def get_best_minutes(item_r, mercado, acertividade):
    df = item_r['data']
    result = []
    minutos = df.Minuto.unique()
    horas = df.Hora.unique()
    sequences = set_sequences(minutos)
    h = []
    for seq in sequences:
        f = {'seq': seq,
             mercado: []}
        for hora in horas:
            ambas = [x[0] for x in df.loc[df.Hora == hora].loc[df.Minuto.isin(seq)][[
                mercado]].values]
            f[mercado].append(True in ambas)
        h.append(f)
    
    for item in h:
        t = item[mercado].count(True)
        f = item[mercado].count(False)
        if t/len(item[mercado]) > acertividade/100:
            result.append({
                'campeonato': item_r['campeonato'],
                'mercado': mercado,
                'minutagem': seq,
                '%': round(t/len(item[mercado])*100, 2),
                'greens': t,
                'reds': f,
                'total_lines': len(item[mercado])
            })
    return result


resultado = []
mercados = ['ambas_marcam', 'over_2_5', 'over_3_5']
for camp in dfs:
    for m in mercados:
        resultado.extend(get_best_minutes(camp, m, 50))


pd.DataFrame(resultado).sort_values(
    'campeonato').to_excel('minutagens.xlsx', index=False)
