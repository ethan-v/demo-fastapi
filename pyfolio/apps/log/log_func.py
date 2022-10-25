from pyfolio.configs.app import appConfigs


def write_log(message: str):
    with open(f"{appConfigs.APP_PATH}/logs/log.txt", mode="a") as log:
        log.write(message + "\n")
