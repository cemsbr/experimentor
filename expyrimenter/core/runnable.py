from .expylogger import ExpyLogger


class Runnable:
    def __init__(self, title=None, logger_name=None):
        if title is None:
            title = '{} {:d}'.format(type(self).__name__, id(self))
        self.title = title

        self._logger = ExpyLogger.getLogger(logger_name)

    def run(self):
        raise NotImplementedError('Runnable.run not implemented')

    def run_pre(self):
        self._logger.start(self.title)

    def run_pos(self):
        self._logger.end(self.title)
