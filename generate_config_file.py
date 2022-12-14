import configparser
import bb_token

config_file = configparser.ConfigParser()


def write_config(config_file, config_file_path='./config.ini'):
    # SAVE CONFIG FILE
    with open(config_file_path, 'w') as configfileObj:
        config_file.write(configfileObj)
        configfileObj.flush()
        configfileObj.close()

def main():
    try:
        config_file.read('./config.ini')
        if config_file['bbtips']['username'] != '' or config_file['bbtips']['username']:
            write_config(config_file)
    except:
        config_file.add_section("bbtips")
        config_file.set("bbtips", "username", input('digite seu username:\n'))
        config_file.set("bbtips", "password", input('digite sua senha:\n'))
        config_file.set("bbtips", "horas", '48')
        config_file.set("bbtips", "range", '3')
        config_file.set("bbtips", "gap", '30')
        config_file.set("bbtips", "min_amostragem", '30')
        config_file.set("bbtips", "min_acert", '94')
        config_file.set("bbtips", "mercados", 'ambas_marcam, over_2_5, over_3_5, casa_vence')
        config_file.set("bbtips", "file_paths", '.')

        


        config_file.set("bbtips", "login_url", "https://api.bbtips.com.br/api/login/")
        config_file.set("bbtips", "futebol_virtual_url", "https://api.bbtips.com.br/api/futebolvirtual")
        config_file.set("bbtips", "auth_token", "*******")
        write_config(config_file)


    bb_token.set_auth_token()
    print("Config file 'config.ini' created")


if __name__ == '__main__':
    main()
