import logging


class ExpyLogger(logging.getLoggerClass()):
    """Standardizes log messages and simplifies :py:module:`logging`."""

    #: Default logger name for new instances
    name = 'expyrimenter'

    configured = False

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(self, name=None):
        cls = self.__class__
        if not cls.configured:
            cls.config()
        super().__init__(name)

    @classmethod
    def getLogger(cls, name=None):
        old_logger = logging.getLoggerClass()
        logging.setLoggerClass(cls)
        expy_logger = logging.getLogger(name)
        logging.setLoggerClass(old_logger)
        return expy_logger

    @classmethod
    def config(cls, level=None, format=None):
        if level is None:
            level = logging.INFO
        if format is None:
            format = '%(asctime)s|%(levelname)s|%(name)s|%(message)s'

        logging.basicConfig(level=level, format=format)
        cls.configured = True

    def start(self, title, level=logging.INFO):
        self.log(level, 'starting "%s"', title)

    def end(self, title, level=logging.DEBUG):
        self.log(level, 'finished "%s"', title)

    def success(self, title, level=logging.INFO):
        self.log(level, 'success "%s"', title)

    def failure(self, title,
                exception=None,
                extra_msg=None,
                level=logging.ERROR):
        msg, args = 'failure "%s"', [title]
        if exception:
            msg, args = self._add_exception_info(exception, msg, args)
        if extra_msg:
            msg += ', ' + extra_msg
        self.log(level, msg, *args)

    def _add_exception_info(self, exception, msg, args):
        if type(exception).__name__ == 'CalledProcessError':
            msg += ', return code %d'
            args.append(exception.returncode)
            if exception.output:
                msg += ', output "%s"'
                args.append(exception.output.rstrip())
        elif type(exception).__name__ == 'HTTPError':
            msg += ', HTTPError "%s"'
            args.append(exception.read())
        else:
            msg += ', %s'
            args.append(exception)
        return msg, args
