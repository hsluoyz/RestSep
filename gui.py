# coding=gbk

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import settings
import main


data = {'col1': ['1', '2', '3'], 'col2': ['4', '5', '6'], 'col3': ['7', '8', '9']}


class LPTable(QTableWidget):
    def __init__(self, matrix):
        QTableWidget.__init__(self, settings.case_count, settings.api_count)
        self.matrix = matrix
        self.set_data()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        for i in range(9):
            self.setColumnWidth(i, 22)


    def set_data(self):
        #self.setHorizontalHeaderLabels(settings.api_list)
        vlist = []
        for i in range(settings.case_count):
            vlist.append(str(i) + ": " + settings.case_list[i])
        self.setVerticalHeaderLabels(vlist)

        vheader = self.verticalHeader()
        vheader.setFixedWidth(340)

        row_size, col_size = self.matrix.shape
        for i in range(row_size):
            for j in range(col_size):
                value = self.matrix[i, j]
                new_item = QTableWidgetItem(str(value))
                if value == 1:
                    new_item.setBackground(QColor(255, 0, 0))
                new_item.setToolTip("aaa")
                self.setItem(i, j, new_item)


def run_gui(args):
    app = QApplication(args)
    table = LPTable(settings.test_matrix)
    table.showMaximized()
    # table.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main.do_init()
    run_gui(sys.argv)
