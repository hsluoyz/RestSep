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


class HeaderViewFilter(QObject):
    def __init__(self, parent, header, *args):
        super(HeaderViewFilter, self).__init__(parent, *args)
        self.header = header
        self.prev_logical_index = -1

    def eventFilter(self, object, event):
        if event.type() == QEvent.HoverMove:
            logical_index = self.header.logicalIndexAt(event.pos())
            if self.prev_logical_index != logical_index:
                # print "haha " + str(logical_index)
                QToolTip.hideText()
                QToolTip.showText(QCursor.pos(), settings.api_list[logical_index])
            self.prev_logical_index = logical_index
        elif event.type() == QEvent.HoverLeave:
            QToolTip.hideText()
            self.prev_logical_index = -1
        return False
            # you could emit a signal here if you wanted


class LPTable(QTableWidget):
    def __init__(self, matrix):
        QTableWidget.__init__(self, settings.case_count, settings.api_count)
        self.matrix = matrix
        self.set_data()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        # headerView = RotatedHeaderView()
        # self.setHorizontalHeader(headerView)
        for i in range(settings.api_count):
            self.setColumnWidth(i, 20)

        # self.setMouseTracking(True)
        #
        # self.current_hover = [0, 0]
        # self.itemEntered.connect(self.header_hover)
        # self.horizontalHeader().enterEvent.connect(self.header_hover)

        self.filter = HeaderViewFilter(self, self.horizontalHeader())
        self.horizontalHeader().setMouseTracking(True)
        self.horizontalHeader().installEventFilter(self.filter)

    # def header_hover(self, row):
    #     print str(row)
    #
    #     QToolTip.hideText()
    #     QToolTip.showText(QCursor.pos(), "aaa")
    #
    # def cell_hover(self, row, column):
    #     item = self.item(row, column)
    #     print str(row) + ", " + str(column)
    #     old_item = self.item(self.current_hover[0], self.current_hover[1])
    #     if self.current_hover != [row, column]:
    #         old_item.setBackground(QBrush(QColor('white')))
    #         item.setBackground(QBrush(QColor('yellow')))
    #     self.current_hover = [row, column]
    #
    #     QToolTip.hideText()
    #     QToolTip.showText(QCursor.pos(), "aaa")

    def set_data(self):
        # Column header
        hlist = []
        self.setHorizontalHeaderLabels(settings.api_list)
        for i in range(settings.api_count):
            hlist.append(str(i))
            # hlist.append(str(i) + ":" + settings.api_list[i])
        self.setHorizontalHeaderLabels(hlist)

        # for i in range(settings.api_count):
        #     header_item = self.horizontalHeaderItem(i)
        #     header_item.setForeground(QColor(255, 0, 0))

        # Row header
        vlist = []
        for i in range(settings.case_count):
            vlist.append(str(i) + ":" + settings.case_list[i])
        self.setVerticalHeaderLabels(vlist)

        # for i in range(settings.case_count):
        #     header_item = self.verticalHeaderItem(i)
        #     header_item.setToolTip(settings.case_list[i])

        vheader = self.verticalHeader()
        vheader.setFixedWidth(350)

        # Items
        row_size, col_size = self.matrix.shape
        for i in range(row_size):
            for j in range(col_size):
                value = self.matrix[i, j]
                new_item = QTableWidgetItem(str(value))
                if value == 1:
                    new_item.setBackground(QColor(255, 50, 50))
                # new_item.setToolTip("aaa")
                self.setItem(i, j, new_item)


class LPHeaderTable(QTableWidget):
    def __init__(self):
        QTableWidget.__init__(self, settings.case_count, settings.api_count)
        self.set_data()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        # headerView = RotatedHeaderView()
        # self.setHorizontalHeader(headerView)
        for i in range(settings.api_count):
            self.setColumnWidth(i, 20)

        # self.setMouseTracking(True)
        #
        # self.current_hover = [0, 0]
        # self.itemEntered.connect(self.header_hover)
        # self.horizontalHeader().enterEvent.connect(self.header_hover)

        # self.filter = HeaderViewFilter(self, self.horizontalHeader())
        # self.horizontalHeader().setMouseTracking(True)
        # self.horizontalHeader().installEventFilter(self.filter)

    def set_data(self):
        # Column header
        hlist = []
        self.setHorizontalHeaderLabels(settings.api_list)
        for i in range(settings.api_count):
            hlist.append(str(i))
            # hlist.append(str(i) + ":" + settings.api_list[i])
        self.setHorizontalHeaderLabels(hlist)

        # for i in range(settings.api_count):
        #     header_item = self.horizontalHeaderItem(i)
        #     header_item.setForeground(QColor(255, 0, 0))

        vheader = self.verticalHeader()
        vheader.setFixedWidth(350)

        self.setRowCount(0)


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        # self.statusBar().showMessage('Ready')
        # self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('RestSep')
        # textEdit = QTextEdit()
        # self.setCentralWidget(textEdit)

        self.connect(self, SIGNAL('closeEmitApp()'), SLOT('close()'))

        table_header = LPHeaderTable()
        # self.setCentralWidget(table_header)
        # table_header.setFixedWidth(1920)
        table_header.setFixedHeight(21)

        table = LPTable(settings.test_matrix)
        # self.setCentralWidget(table)
        # table.setFixedWidth(1920)
        # table.setFixedHeight(1080 - 60)
        table.setCornerButtonEnabled(False)
        # table.setGeometry(QRect(0, 0, 200, 200))

        main_layout = QVBoxLayout()
        # main_layout = self.layout()
        main_layout.setMargin(0)
        main_layout.setSpacing(0)
        main_layout.setSizeConstraint(QLayout.SetMaximumSize)

        # pushbutton_1 = QPushButton(self)
        # pushbutton_1.setText('First')
        # main_layout.addWidget(pushbutton_1)

        main_layout.addWidget(table_header)
        main_layout.addWidget(table)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # self.setLayout(main_layout)

        self.showMaximized()
        # self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.emit(SIGNAL('closeEmitApp()'))


def run_gui(args):
    app = QApplication(args)

    main_window = MyMainWindow()

    # table = LPTable(settings.test_matrix)
    # table.showMaximized()
    # table.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main.do_init()
    run_gui(sys.argv)
