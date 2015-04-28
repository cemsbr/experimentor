from .ssh import SSH


class Filesystem:
    def __init__(self, path, host, logger_name=None):
        self._path = path
        self._host = host
        self._logger_name = logger_name

    def mkdir(self, title=None):
        if title is None:
            title = 'mkdir {} in {}'.format(self._path, self._host)

        cmd = self._get_cmd()
        return SSH(self._host, cmd, title=title, logger_name=self._logger_name)

    def _get_cmd(self):
        # Must not use quotes in dir name - no ~/ expansion
        # TODO quoting
        return 'test -d {} || mkdir -p {}'.format(self._path, self._path)
