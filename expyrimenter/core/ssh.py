from .shell import Shell
from .expylogger import ExpyLogger
from time import sleep
import random
from shlex import quote


class SSH(Shell):
    """
    :param str params: shell SSH params (at least, the hostname).
    :param str remote_cmd: Command to be run in remote host through SSH.
    :param bool stdout: Capture standard output? Default: *False*.
    :param bool stderr: Capture standard error? Default: *True*.
    :param str title: Task title. Default: whole shell command,
                      including :attr:`remote_cmd`.
    :param str logger: Logger name. Default: this class name.
    """

    def __init__(self, params, remote_cmd,
                 stdout=False,
                 stderr=True,
                 title=None,
                 logger_name=None):
        remote_cmd = self._redirect_outputs(remote_cmd, stdout, stderr)
        cmd = 'ssh {} {}'.format(params, quote(remote_cmd))
        if logger_name is None:
            logger_name = 'ssh'
        super().__init__(cmd, stdout, stderr, title, logger_name)

    @classmethod
    def await_availability(cls, params,
                           interval=5,
                           max_rand=1,
                           title=None,
                           logger_name=None):
        """Periodically tries SSH until it is successful.
        This function is very useful in cloud environmentes, because
        there can be a considerable amount of time after a VM is running
        and before SSH connections are available.

        :param str params: shell SSH params (at least the hostname).
        :param num interval: Time in seconds to wait before new trial.
        :param num max_rand: A float random number between 0 and ``max_rand``
                             will be added to ``interval``.
        :param str title: Task title. Default: 'SSH test ":attr:`remote_cmd`"'
        :param str logger_name: Logger name. Default: this class name.
        """
        if title is None:
            title = 'SSH test on {}'.format(params)
        if logger_name is None:
            logger_name = 'ssh'

        logger = ExpyLogger.getLogger(logger_name)
        ssh = SSH(params, 'exit', title=title, logger_name=logger_name)
        ssh.failure_level = ExpyLogger.DEBUG
        while ssh.fails():
            sleep(random.uniform(0, max_rand))
            logger.debug('Will try "ssh %s" again in %d + [0, %.2f) sec' %
                         (params, interval, max_rand))
            sleep(interval)
