import logging

__all__ = ['StatusBarHandler']


class StatusBarHandler(logging.Handler):
    def __init__(self, statusbar, timeout=0):
        super(StatusBarHandler, self).__init__()
        self.statusbar = statusbar
        self.timeout = timeout
        self.statusbar.destroyed.connect(self._on_destroyed)

    def emit(self, record):
        msg = self.format(record)
        self.statusbar.showMessage(msg, self.timeout)

    def _on_destroyed(self):
        logger = logging.getLogger()
        logger.removeHandler(self)
