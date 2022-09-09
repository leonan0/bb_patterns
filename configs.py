from configparser import ConfigParser

configs = ConfigParser()

configs.read('config.ini')

try:
    bbconf = configs['bbtips']
except KeyError:
    import generate_config_file
    generate_config_file.main()
    raise Exception('Favor executar novamente')

HORAS = int(bbconf['horas'])
RANGE = int(bbconf['range'])
GAP = int(bbconf['gap'])
MIN_AMOSTRAGEM = int(bbconf['min_amostragem'])
MERCADOS = [x.strip() for x in bbconf['mercados'].split(',')]

MIN_ACERT = int(bbconf['min_acert'])

PATH_TO_SAVE = bbconf['file_paths']

if __name__ == '__main__':
    print(f'''
          Horas para busca {HORAS}
          mercados analisados {MERCADOS}
          range de tiros {RANGE}
          gap de jogos 0 - {GAP}
          amostragem minima {MIN_AMOSTRAGEM}
          acertividade minima {MIN_ACERT}
          caminho dos arquivos {PATH_TO_SAVE}
          ''')