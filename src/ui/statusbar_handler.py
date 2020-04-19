import logging

__all__ = ['StatusBarHandler']


class StatusBarHandler(logging.Handler):
    def __init__(self, statusbar):
        super(StatusBarHandler, self).__init__()
        self.statusbar = statusbar
        self.statusbar.destroyed.connect(self._on_destroyed)

    def emit(self, record):
        msg = self.format(record)
        self.statusbar.showMessage(msg)

    def _on_destroyed(self):
        logger = logging.getLogger()
        logger.removeHandler(self)
