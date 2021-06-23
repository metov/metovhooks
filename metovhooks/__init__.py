import logging
import coloredlogs

# Set up logging
log = logging.getLogger(__name__)
LOGFMT = "%(programname)s %(filename)s:%(lineno)d %(message)s"
coloredlogs.install(fmt=LOGFMT, datefmt="%H:%M:%S", level="DEBUG", logger=log)
