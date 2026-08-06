# TEMP DEBUG - REMOVE AFTER RENDER INVESTIGATION
print("[startup] app.core.logger: before logging import", flush=True)
import logging
print("[startup] app.core.logger: after logging import", flush=True)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger
