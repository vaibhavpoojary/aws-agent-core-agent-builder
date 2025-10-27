import logging, sys, json
def get_logger(name="agent_platform"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        fmt = json.dumps({"time":"%(asctime)s","level":"%(levelname)s","name":"%(name)s","message":"%(message)s"})
        handler.setFormatter(logging.Formatter(fmt))
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
