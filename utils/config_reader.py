import configparser


def get_config(section_name: str):
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config[section_name]
