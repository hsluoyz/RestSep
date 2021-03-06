# coding: UTF-8

import sys
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import settings
import main
import cPickle as pickle

app = None
main_window = None

is_running = False

def get_path_head(api_name):
    api_item_list = api_name.split('|')[0].split('/')
    return api_item_list[0].strip()


def get_method(api_name):
    api_item_list = api_name.split('| ')
    return api_item_list[-1]


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
        self.parent = parent
        self.header = header
        self.prev_logical_index = -1

    def eventFilter(self, object, event):
        # print "haha " + str(event.type())
        # if event.type() == QEvent.HoverMove:
        #     logical_index = self.header.logicalIndexAt(event.pos())
        #     if self.prev_logical_index != logical_index:
        #         # print "haha " + str(logical_index)
        #         QToolTip.hideText()
        #         QToolTip.showText(QCursor.pos(), settings.api_list[logical_index])
        #     self.prev_logical_index = logical_index
        # elif event.type() == QEvent.HoverLeave:
        #     QToolTip.hideText()
        #     self.prev_logical_index = -1

        # print "haha " + str(event.type())
        if event.type() == QEvent.CursorChange or event.type() == QEvent.Enter:
            local_pos = self.header.mapFromGlobal(QCursor.pos())
            # print local_pos
            logical_index = self.header.logicalIndexAt(local_pos)
            # print "prev_logical_index = %d, logical_index = %d" %(self.prev_logical_index, logical_index)
            if self.prev_logical_index != logical_index:
                QToolTip.hideText()
                QToolTip.showText(QCursor.pos(), settings.api_list[logical_index])
            self.prev_logical_index = logical_index
        elif event.type() == QEvent.Leave:
            QToolTip.hideText()
            self.prev_logical_index = -1
        return False
        # you could emit a signal here if you wanted


class GroupHeaderViewFilter(QObject):
    def __init__(self, parent, header, *args):
        super(GroupHeaderViewFilter, self).__init__(parent, *args)
        self.parent = parent
        self.header = header
        self.prev_logical_index = -1

    def eventFilter(self, object, event):
        # print "haha " + str(event.type())
        if event.type() == QEvent.CursorChange or event.type() == QEvent.Enter:
            local_pos = self.header.mapFromGlobal(QCursor.pos())
            # print local_pos
            logical_index = self.header.logicalIndexAt(local_pos)
            # print "prev_logical_index = %d, logical_index = %d" %(self.prev_logical_index, logical_index)
            if self.prev_logical_index != logical_index:
                QToolTip.hideText()
                QToolTip.showText(QCursor.pos(), self.parent.hlist_combined_name[logical_index])
            self.prev_logical_index = logical_index
        elif event.type() == QEvent.Leave:
            QToolTip.hideText()
            self.prev_logical_index = -1
        return False
        # you could emit a signal here if you wanted


class LPTable(QTableWidget):
    def __init__(self, header_table):
        QTableWidget.__init__(self, settings.case_count, settings.api_count)
        self.header_table = header_table
        self.set_headers()
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

        # Add the tooltips
        self.filter = HeaderViewFilter(self, self.horizontalHeader())
        self.horizontalHeader().setMouseTracking(True)
        self.horizontalHeader().installEventFilter(self.filter)

        # self.header_table.horizontalScrollBar().setMinimum(self.horizontalScrollBar().minimum())
        # self.header_table.horizontalScrollBar().setMaximum(self.horizontalScrollBar().maximum())

        self.connect(self.horizontalScrollBar(), SIGNAL("valueChanged(int)"), self.sync_scroll)

    def sync_scroll(self):
        slide_value = self.horizontalScrollBar().value()

        # self.header_table.horizontalScrollBar().setMinimum(self.horizontalScrollBar().minimum())
        # self.header_table.horizontalScrollBar().setMaximum(self.horizontalScrollBar().maximum())
        #
        # print "hmin = %d, hmax = %d, hcur = %d, hstep = %d" %\
        #       (self.header_table.horizontalScrollBar().minimum(), self.header_table.horizontalScrollBar().maximum(), self.header_table.horizontalScrollBar().value(), self.header_table.horizontalScrollBar().singleStep())
        # print "min = %d, max = %d, cur = %d, step = %d" %\
        #       (self.horizontalScrollBar().minimum(), self.horizontalScrollBar().maximum(), slide_value, self.horizontalScrollBar().singleStep())
        self.header_table.horizontalScrollBar().setValue(slide_value)
        # self.sliderBar2.setValue(slide_value)

    def set_headers(self):
        # Column header
        hlist = []
        # self.setHorizontalHeaderLabels(settings.api_list)
        for i in range(settings.api_count):
            hlist.append(str(i))
            # hlist.append(str(i) + ":" + settings.api_list[i])
        self.setHorizontalHeaderLabels(hlist)

        for i in range(settings.api_count):
            header_item = self.horizontalHeaderItem(i)
            self.horizontalHeader()
            if get_method(settings.api_list[i]) == 'GET':
                # Red
                header_item.setBackground(QColor(255, 0, 0))
            elif get_method(settings.api_list[i]) == 'POST':
                # Green
                header_item.setBackground(QColor(0, 255, 0))
            elif get_method(settings.api_list[i]) == 'PUT':
                # Blue
                header_item.setBackground(QColor(0, 0, 255))
            elif get_method(settings.api_list[i]) == 'DELETE':
                # Yellow
                header_item.setBackground(QColor(255, 255, 0))
            elif get_method(settings.api_list[i]) == 'HEAD':
                # Purple
                header_item.setBackground(QColor(255, 0, 255))
            else:
                # Black
                header_item.setBackground(QColor(0, 0, 0))

        # Row header
        vlist = []
        for i in range(settings.case_count):
            vlist.append(str(i) + ":" + settings.case_list[i])
        self.setVerticalHeaderLabels(vlist)

        for i in range(settings.case_count):
            header_item = self.verticalHeaderItem(i)
            header_item.setToolTip(settings.case_list[i])

        vheader = self.verticalHeader()
        vheader.setFixedWidth(350)

    def set_data(self, matrix):
        # Items
        row_size, col_size = matrix.shape
        for i in range(row_size):
            for j in range(col_size):
                value = matrix[i, j]
                new_item = QTableWidgetItem(str(value))
                if value == 1:
                    new_item.setBackground(QColor(255, 50, 50))
                elif value == 2:
                    new_item.setBackground(QColor(255, 220, 220))
                # new_item.setToolTip("aaa")
                self.setItem(i, j, new_item)


class LPHeaderTable(QTableWidget):
    def __init__(self):
        QTableWidget.__init__(self)

        self.hlist_combined_name = []
        self.set_headers()
        # self.resizeColumnsToContents()
        # self.resizeRowsToContents()
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # for i in range(settings.api_count):
        #     self.setColumnWidth(i, 20)

        # Add the tooltips
        self.filter = GroupHeaderViewFilter(self, self.horizontalHeader())
        self.horizontalHeader().setMouseTracking(True)
        self.horizontalHeader().installEventFilter(self.filter)

    def set_headers(self):
        # Column header
        hlist_combined = []
        cur = -1
        # self.setHorizontalHeaderLabels(settings.api_list)
        for i in range(settings.api_count):
            # hlist.append(get_path_head(settings.api_list[i]))
            if cur != -1 and hlist_combined[cur][0] == get_path_head(settings.api_list[i]):
                hlist_combined[cur][2] = i + 1
            else:
                hlist_combined.append([get_path_head(settings.api_list[i]), i, i + 1])
                self.hlist_combined_name.append(get_path_head(settings.api_list[i]))
                cur += 1

        self.setColumnCount(len(hlist_combined))
        self.setHorizontalHeaderLabels(self.hlist_combined_name)
        for i in range(len(hlist_combined)):
            self.horizontalHeader().resizeSection(i, 20 * (hlist_combined[i][2] - hlist_combined[i][1]))
            # print hlist_combined[i]


        # for i in range(settings.api_count):
        #     header_item = self.horizontalHeaderItem(i)
        #     header_item.setForeground(QColor(255, 0, 0))

        vheader = self.verticalHeader()
        vheader.setFixedWidth(350)

        self.setRowCount(0)


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()

        self.header_table = None
        self.table = None
        self.init_ui()

    def init_ui(self):
        # self.statusBar().showMessage('Ready')
        # self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('RestSep')
        # textEdit = QTextEdit()
        # self.setCentralWidget(textEdit)

        self.connect(self, SIGNAL('closeEmitApp()'), SLOT('close()'))

        self.header_table = LPHeaderTable()
        # self.setCentralWidget(header_table)
        # header_table.setFixedWidth(1920)
        self.header_table.setFixedHeight(21)

        self.table = LPTable(self.header_table)
        # self.table.set_data(settings.test_matrix)
        # self.setCentralWidget(table)
        # table.setFixedWidth(1920)
        # table.setFixedHeight(1080 - 60)
        self.table.setCornerButtonEnabled(False)
        # table.setGeometry(QRect(0, 0, 200, 200))

        main_layout = QVBoxLayout()
        # main_layout = self.layout()
        main_layout.setMargin(0)
        main_layout.setSpacing(0)
        main_layout.setSizeConstraint(QLayout.SetMaximumSize)

        # pushbutton_1 = QPushButton(self)
        # pushbutton_1.setText('First')
        # main_layout.addWidget(pushbutton_1)

        main_layout.addWidget(self.header_table)
        main_layout.addWidget(self.table)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # stop or resume
        stop_action = QAction('Stop | Resume', self)
        stop_action.setShortcut('Ctrl+Z')
        stop_action.setStatusTip('stop or resume the iteration')
        stop_action.triggered.connect(self.on_stop_or_resume)

        # open
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+X')
        open_action.setStatusTip('open a data file')
        open_action.triggered.connect(self.on_open)

        # save as
        save_as_action = QAction('Save As', self)
        save_as_action.setShortcut('Ctrl+S')
        save_as_action.setStatusTip('save as a data file')
        save_as_action.triggered.connect(self.on_save_as)

        # stop menu bar
        menubar = self.menuBar()
        menu_bar = menubar.addMenu('&Menu')
        menu_bar.addAction(stop_action)
        menu_bar.addAction(open_action)
        menu_bar.addAction(save_as_action)

        self.statusBar().showMessage(u"请先打开一个文件")

        # self.setLayout(main_layout)
        # self.showMaximized()
        # self.show()

    def set_data(self, matrix):
        self.table.clearContents()
        self.table.set_data(matrix)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.emit(SIGNAL('closeEmitApp()'))

    def on_stop_or_resume(self):
        global thread
        global is_running
        if is_running:
            is_running = False
            print("stop clicked")
            thread.stop()
            self.statusBar().showMessage(u"暂停")
        else:
            is_running = True
            print("resume clicked")
            if thread.isAlive():
                thread.stop()
            thread = main.MyThread(set_data, set_title)
            thread.setDaemon(True)
            thread.start()
            self.statusBar().showMessage(u'继续运行')

    def on_stop(self):
        self.on_stop_or_resume()

    def on_resume(self):
        self.on_stop_or_resume()

    def on_open(self):
        open_file_path = QFileDialog.getOpenFileName(self, 'Open file', '.', "files (*.sav)")
        open_file_path = unicode(open_file_path).encode('utf-8')
        if open_file_path == '':
            return

        with open(open_file_path, "r") as resume_file:
            content = resume_file.read().strip()
            if content != "":
                f = file(open_file_path, 'rb')
                data = pickle.load(f)
                main.load_session(data)
            else:
                return

        main.show_session(set_data, set_title)
        # global thread
        # thread.stop()
        # thread = main.MyThread(set_data, set_title, open_file_path)
        # thread.setDaemon(True)
        # thread.start()
        self.statusBar().showMessage(u'打开文件: ' + open_file_path)

    def on_save_as(self):
        save_file_path = QFileDialog.getSaveFileName(self, 'Open file', '.', "files (*.sav)")
        print(save_file_path)
        # global thread
        # thread.serialize(_save_file_path=save_file_path)
        # 构造data对象
        data = main.save_session()
        # 序列化到temp.data
        f = open(save_file_path, 'wb')
        pickle.dump(data, f)
        f.close()
        del data
        print("serialize into file")
        self.statusBar().showMessage(u'保存到文件: ' + save_file_path)


def set_title(title):
    main_window.setWindowTitle('RestSep | %s' % (title))


def set_data(matrix):
    main_window.set_data(matrix)


def start_gui(args):
    global app, main_window

    app = QApplication(args)
    # won't work on windows style.

    # Windows
    # WindowsXP
    # WindowsVista
    # Motif
    # CDE
    # Plastique
    # Cleanlooks
    app.setStyle(QStyleFactory.create('Plastique'))

    main_window = MyMainWindow()

    # table = LPTable(settings.test_matrix)
    # table.showMaximized()
    # table.show()

    # set_data(settings.test_matrix)
    main_window.showMaximized()


def end_gui():
    global app
    sys.exit(app.exec_())


def do_show_test():
    set_data(settings.test_matrix)


def do_compute():
    main.do_init_generation()
    main.do_evolve_generation(set_data, set_title)


if __name__ == "__main__":
    # for style in QStyleFactory.keys():
    #     print style

    main.do_init()
    start_gui(sys.argv)

    is_running = True
    if sys.argv[-1] == "test":
        thread = threading.Thread(target=do_show_test)
    else:
        # thread = threading.Thread(target=do_compute)
        thread = main.MyThread(set_data, set_title)
        thread.init_random_data()
    thread.setDaemon(True)
    thread.start()
    # do_compute()
    end_gui()

    # print get_path_head('os-agents/%NAME% | POST')
    # print get_method('os-agents/%NAME% | POST')
