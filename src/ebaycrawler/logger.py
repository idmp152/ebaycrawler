import logging

logging.SUCCESS = logging.INFO

class ColoredFormatter(logging.Formatter):
    """Colored logging formatter"""

    OUTPUT_FORMAT = "\u21B3 {0} %(message)s \u001b[0m"

    FORMATS = {
        logging.DEBUG: OUTPUT_FORMAT.format(''),
        logging.INFO: OUTPUT_FORMAT.format(''),
        logging.WARNING: OUTPUT_FORMAT.format("\u001b[33m"),
        logging.ERROR: OUTPUT_FORMAT.format("\u001b[31;1m"),
        logging.CRITICAL: OUTPUT_FORMAT.format("\u001b[31m"),
        logging.SUCCESS: OUTPUT_FORMAT.format("\u001b[32m")
    }

    def format(self, record):
        log_fmt = self.FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class ExtendedLogger(logging.Logger):
    """Custom logger extension"""
    def success(self, msg: str, *args, **kwargs):
        """
        Log 'msg % args' with severity 'SUCCESS'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if self.isEnabledFor(logging.SUCCESS):
            self._log(logging.SUCCESS, msg, args, **kwargs)


logging.setLoggerClass(ExtendedLogger)
logger = logging.getLogger("ebaycrawler")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(ColoredFormatter())

logger.addHandler(ch)
