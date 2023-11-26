import configparser

def config(filename="database.ini", section = "postgresql"):

    config = configparser.ConfigParser()
    config.read(filename)
    db = {}
    if config.has_section(section):
        params = config.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Данный параметр не найден")
    return db