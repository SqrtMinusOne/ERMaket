import logging.config
import os
import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from ermaket.api import Config
from ermaket.ui import HierachyEditor

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = Config()
    Path(
        os.path.dirname(
            config.Logging['handlers']['file_handler']['filename']
        )
    ).mkdir(parents=True, exist_ok=True)
    logging.config.dictConfig({**config.Logging, **config.GUILogging})

    editor = HierachyEditor()
    editor.show()

    sys.exit(app.exec_())
