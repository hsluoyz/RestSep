# coding=gbk

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import settings
import main


class RotatedHeaderView(QHeaderView):
    def __init__(self, parent=None):
        super(RotatedHeaderView, self).__init__(Qt.Horizontal, parent)
        self.setMinimumSectionSize(20)

    def paintSection(self, painter, rect, logicalIndex ):
        painter.save()
        # translate the painter such that rotate will rotate around the correct point
        # painter.translate(rect.x()+rect.width(), rect.y())
        # painter.rotate(90)
        # painter.translate(rect.x(), rect.y()+rect.height())
        # painter.rotate(-90)
        # and have parent code paint at this location
        newrect = QRect(0, 0, rect.height(), rect.width())
        super(RotatedHeaderView, self).paintSection(painter, newrect, logicalIndex)
        painter.restore()

    def minimumSizeHint(self):
        size = super(RotatedHeaderView, self).minimumSizeHint()
        size.transpose()
        return size

    def sectionSizeFromContents(self, logicalIndex):
        size = super(RotatedHeaderView, self).sectionSizeFromContents(logicalIndex)
        size.transpose()
        return size


class LPTable(QTableWidget):
    def __init__(self, matrix):
        QTableWidget.__init__(self, settings.case_count, settings.api_count)
        self.matrix = matrix
        self.set_data()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        # headerView = RotatedHeaderView()
        # self.setHorizontalHeader(headerView)
        for i in range(9):
            self.setColumnWidth(i, 22)

    def set_data(self):
        # Column header
        hlist = []
        self.setHorizontalHeaderLabels(settings.api_list)
        for i in range(settings.api_count):
            hlist.append(str(i))
            # hlist.append(str(i) + ":" + settings.api_list[i])
        self.setHorizontalHeaderLabels(hlist)

        for i in range(settings.api_count):
            header_item = self.horizontalHeaderItem(i)
            header_item.setToolTip(settings.api_list[i])

        # Row header
        vlist = []
        for i in range(settings.case_count):
            vlist.append(str(i) + ":" + settings.case_list[i])
        self.setVerticalHeaderLabels(vlist)

        for i in range(settings.case_count):
            header_item = self.verticalHeaderItem(i)
            header_item.setToolTip(settings.case_list[i])

        vheader = self.verticalHeader()
        vheader.setFixedWidth(255)

        # Items
        row_size, col_size = self.matrix.shape
        for i in range(row_size):
            for j in range(col_size):
                value = self.matrix[i, j]
                new_item = QTableWidgetItem(str(value))
                if value == 1:
                    new_item.setBackground(QColor(255, 0, 0))
                # new_item.setToolTip("aaa")
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
