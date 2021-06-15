from datetime import datetime
import logging


def create_log(name, log_all, log_error):
    #now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    #log_all = log_path + f'ALL_scraping_{now}.log'
    #log_error = log_path + f'ERROR_scraping_{now}.log'

    logging.shutdown()
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_all, mode='a', encoding='utf-8')
    fh.setLevel(logging.INFO)

    # create console handler with a higher log level
    ch = logging.FileHandler(log_error, mode='a', encoding='utf-8')
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s : %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to logger
    log.addHandler(ch)
    log.addHandler(fh)

    log.error('\n||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'
             '\n|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||UPDATE LOG|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'
             '\n||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
    return log

