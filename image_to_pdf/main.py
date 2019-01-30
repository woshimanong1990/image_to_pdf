# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function

import sys
from PyQt5 import QtWidgets

from image_to_pdf.main_window import CustomMainWindow
from image_to_pdf.logging_config import setup_logging_config


def main():
    setup_logging_config()
    app = QtWidgets.QApplication(sys.argv)
    main_window = CustomMainWindow()
    main_window.show()
    app.exec_()


if __name__ == '__main__':
    main()