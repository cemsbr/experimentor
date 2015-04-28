from .runnable import Runnable
import subprocess
from subprocess import CalledProcessError
import logging


class Shell(Runnable):
    """
    :param str cmd: Command with arguments to be run.
    :param bool stdout: Capture standard output? Default: *False*.
    :param bool stderr: Capture standard error? Default: *True*.
    :param str title: Task title. Default: :attr:`cmd`.
    :param str logger: Logger name. Default: this class name.
    """

    def __init__(self, cmd,
                 stdout=False,
                 stderr=True,
                 title=None,
                 logger_name=None):
        self._cmd = self._redirect_outputs(cmd, stdout, stderr)
        if title is None:
            title = self._cmd
        if logger_name is None:
            logger_name = 'shell'
        super().__init__(title=title, logger_name=logger_name)

        self._stdout, self._stderr = stdout, stderr
        self.failure_level = logging.ERROR

    def _redirect_outputs(self, cmd, stdout, stderr):
        """
        Can reduce the amount of output in the logs (and transfers in the
        network, if using SSH)
        """
        suffix = ''
        if not stdout:
            suffix += ' 1>/dev/null'
        if not stderr:
            suffix += ' 2>/dev/null'

        return cmd + suffix

    def run(self):
        """If the command exits 0, returns 0 or selected (stdout/stderr) output.
        Otherwise, logs the error and raises CalledProcessError.

        :return: shell return code (0) or selected output.
        :rtype: int or str
        :raises CalledProcessError: if shell return code is not 0.
        """
        self.run_pre()

        kwargs = {'shell': True, 'universal_newlines': True}
        if self._stderr:
            kwargs['stderr'] = subprocess.STDOUT

        try:
            if not (self._stdout or self._stderr):
                output = subprocess.check_call(self._cmd, **kwargs)
            else:
                output = subprocess.check_output(self._cmd, **kwargs).strip()
            self._logger.success(self.title)
        except CalledProcessError as e:
            self._logger.failure(self.title, exception=e,
                                 level=self.failure_level)
            raise e
        finally:
            self.run_pos()

        return output

    def is_successful(self):
        """Runs the command and returns whether its return code is 0.

        :return: whether the command was successful.
        :rtype: bool
        """
        try:
            self.run()
            return True
        except:
            return False

    def fails(self):
        """Runs the command and returns whether the return code differs from 0.

        :return: whether the command has failed.
        :rtype: bool
        """
        return not self.is_successful()
