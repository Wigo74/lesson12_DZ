import logging


def creat_logger():

    logger = logging.getLogger("basic")
    logger.setLevel("DEBUG")

    console_handler = logging.StreamHandler()
    formatter_basic = logging.Formatter("%(levelname)s : %(asctime)s : %(message)s")
    console_handler.setFormatter(formatter_basic)
    file_handler = logging.FileHandler("logs/basic.txt")
    file_handler.setFormatter(formatter_basic)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.info("Приложение запущено")


