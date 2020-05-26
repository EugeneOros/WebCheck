import webbrowser
from time import sleep
import login
import email_send

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
                            QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QTimer)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
                           QPixmap, QRadialGradient, QMovie)
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QFrame,
                               QStackedWidget, QGridLayout, QLabel, QSpacerItem, QSizePolicy, QGroupBox,
                               QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QRadioButton, QScrollArea,
                               QAbstractScrollArea, QMessageBox)
import sys
from selenium.common.exceptions import InvalidArgumentException

from ui import stylesheet as styles
import os
import read_write_data as data
import monitoring
import multiprocessing

path = os.path.dirname(os.path.abspath(__file__))
# p2 = multiprocessing.Process(target=monitoring_main.start_monitor)
# p2.start()
# p2.join()


class SitesFrame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setStyleSheet("""QFrame{background-color:#83a836;}""")


class NavFrame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setStyleSheet("""QFrame{ background-color:#43454f;}""")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        self.frame_nav = QFrame(self)
        self.frame_nav.setMinimumSize(QSize(220, 300))
        self.frame_nav.setStyleSheet("""QFrame{ background-color:#43454f;}""")
        self.frame_nav.setFrameShape(QFrame.StyledPanel)
        self.frame_nav.setFrameShadow(QFrame.Raised)

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(11, -1, 11, -1)
        self.gridLayout.addWidget(self.frame_nav, 3, 0, 1, 4)

        # set program img and name
        self.label_img = QLabel(self)
        self.label_img.setFixedSize(QSize(60, 60))
        self.label_img.setPixmap(QPixmap(os.path.join(path, 'img/icon.png')))
        # self.label_img.setPixmap(QPixmap("../img/icon.png"))
        self.label_img.setScaledContents(True)
        self.gridLayout.addWidget(self.label_img, 2, 1, 1, 1)

        self.label_name = QLabel("WebCheck        ", self)
        self.label_name.setStyleSheet(styles.label_icon_name)
        self.gridLayout.addWidget(self.label_name, 2, 2, 1, 1)

        self.spacer_name_l = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer_name_r = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer_name_t = QSpacerItem(20, 70, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.gridLayout.addItem(self.spacer_name_l, 2, 0, 1, 1)
        self.gridLayout.addItem(self.spacer_name_r, 2, 3, 1, 1)
        self.gridLayout.addItem(self.spacer_name_t, 1, 1, 1, 2)

        # set bottom layout for keeping gb in it
        self.gridLayout_b = QGridLayout(self.frame_nav)
        self.spacer_gb_l = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer_gb_r = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer_gb_t = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.spacer_gb_b = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_b.addItem(self.spacer_gb_l, 1, 2, 1, 1)
        self.gridLayout_b.addItem(self.spacer_gb_r, 1, 0, 1, 1)
        self.gridLayout_b.addItem(self.spacer_gb_t, 0, 1, 1, 1)
        self.gridLayout_b.addItem(self.spacer_gb_b, 2, 1, 1, 1)

        # set gb and radio buttons
        self.groupBox = QGroupBox("", self.frame_nav)
        self.gridLayout_b.addWidget(self.groupBox, 1, 1, 1, 1)
        self.groupBox.setMinimumSize(QSize(220, 350))
        self.groupBox.setStyleSheet("""QGroupBox{background-image: url(ui/img/radioline.png);  border: none;}""")
        self.verticalLayout_gb = QVBoxLayout(self.groupBox)

        self.radioButton_add = QRadioButton(" Add", self.groupBox)
        self.radioButton_add.setStyleSheet(styles.btn_radio)
        self.verticalLayout_gb.addWidget(self.radioButton_add)

        self.radioButton_monitored = QRadioButton(" Monitored", self.groupBox)
        self.radioButton_monitored.setStyleSheet(styles.btn_radio)
        self.verticalLayout_gb.addWidget(self.radioButton_monitored)

        self.radioButton_options = QRadioButton(" Options", self.groupBox)
        self.radioButton_options.setStyleSheet(styles.btn_radio)
        self.verticalLayout_gb.addWidget(self.radioButton_options)

        self.radioButton_about = QRadioButton(" About", self.groupBox)
        self.radioButton_about.setStyleSheet(styles.btn_radio)
        self.verticalLayout_gb.addWidget(self.radioButton_about)


class PageLoading(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.gridLayout = QGridLayout(self)
        parent.addWidget(self)
        self.label_animation = QLabel("Loading...", self)
        self.gridLayout.addWidget(self.label_animation, 1, 1, 1, 1)
        self.label_animation.setStyleSheet("""QLabel{font-size: 20px; color: #43454f; font: 23pt "Corbel"}""")

        self.spacer_l = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.spacer_l, 1, 0, 1, 1)
        self.spacer_r = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.spacer_r, 1, 2, 1, 1)
        self.spacer_t = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.spacer_l, 0, 1, 1, 2)
        self.spacer_b = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.spacer_r, 2, 1, 1, 2)


class PageAllegroAdd(QWidget):
    def __init__(self, parent=None, shared_dict=None):
        QWidget.__init__(self, parent)
        parent.addWidget(self)
        self.shared_dict = shared_dict
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout.setRowStretch(4, 1)
        self.gridLayout.setRowStretch(5, 1)
        self.gridLayout.setRowStretch(6, 1)
        self.gridLayout.setRowStretch(7, 1)
        self.gridLayout.setRowStretch(8, 1)
        self.gridLayout.setRowStretch(9, 1)
        self.gridLayout.setRowStretch(10, 1)
        self.gridLayout.setRowStretch(11, 1)
        self.gridLayout.setRowStretch(12, 1)
        self.gridLayout.setRowStretch(13, 1)
        self.gridLayout.setRowStretch(14, 2)
        self.gridLayout.setRowStretch(15, 1)
        self.gridLayout.setColumnStretch(0, 5)
        self.gridLayout.setColumnStretch(1, 5)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 2)
        self.gridLayout.setColumnStretch(4, 1)
        self.gridLayout.setColumnStretch(5, 2)
        self.gridLayout.setColumnStretch(6, 1)
        self.gridLayout.setColumnStretch(7, 2)
        self.gridLayout.setColumnStretch(8, 3)
        self.gridLayout.setColumnStretch(9, 5)

        # create lineEdits
        self.lineEdit_login = QLineEdit(self)
        self.lineEdit_login.setMinimumSize(QSize(0, 60))
        self.lineEdit_login.setSizeIncrement(QSize(40, 40))
        self.lineEdit_login.setStyleSheet(styles.lineEdit)
        self.lineEdit_login.setMaxLength(32767)
        self.gridLayout.addWidget(self.lineEdit_login, 4, 1, 1, 3)
        self.lineEdit_login.setPlaceholderText("login or email of your account")

        self.lineEdit_password = QLineEdit(self)
        self.lineEdit_password.setMinimumSize(QSize(20, 60))
        self.lineEdit_password.setStyleSheet(styles.lineEdit)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password.setReadOnly(False)
        self.gridLayout.addWidget(self.lineEdit_password, 7, 1, 1, 3)
        self.lineEdit_password.setPlaceholderText("password of your account")

        self.lineEdit_email = QLineEdit(self)
        self.lineEdit_email.setMinimumSize(QSize(0, 60))
        self.lineEdit_email.setStyleSheet(styles.lineEdit)
        self.lineEdit_email.setFrame(True)
        self.lineEdit_email.setEchoMode(QLineEdit.Normal)
        self.gridLayout.addWidget(self.lineEdit_email, 7, 5, 1, 4)
        self.lineEdit_email.setPlaceholderText("email to which the notification will be sent")

        self.lineEdit_link = QLineEdit(self)
        self.lineEdit_link.setMinimumSize(QSize(0, 60))
        self.lineEdit_link.setStyleSheet(styles.lineEdit)
        self.gridLayout.addWidget(self.lineEdit_link, 10, 1, 1, 8)
        self.lineEdit_link.setPlaceholderText("link to the page that you want to monitor")

        self.lineEdit_price = QLineEdit(self)
        self.lineEdit_price.setMinimumSize(QSize(0, 60))
        self.lineEdit_price.setStyleSheet(styles.lineEdit)
        self.gridLayout.addWidget(self.lineEdit_price, 13, 1, 1, 1)
        self.lineEdit_price.setPlaceholderText("Price below which to notificate")

        self.lineEdit_xpath = QLineEdit(self)
        self.lineEdit_xpath.setMinimumSize(QSize(0, 60))
        self.lineEdit_xpath.setStyleSheet(styles.lineEdit)
        self.gridLayout.addWidget(self.lineEdit_xpath, 13, 3, 1, 3)
        self.lineEdit_xpath.setPlaceholderText("XPATH of element with the price")

        self.lineEdit_time = QLineEdit(self)
        self.lineEdit_time.setMinimumSize(QSize(0, 60))
        self.lineEdit_time.setStyleSheet(styles.lineEdit)
        self.gridLayout.addWidget(self.lineEdit_time, 13, 7, 1, 2)
        self.lineEdit_time.setPlaceholderText("interval between refreshes")

        # Create Labels
        self.label_title = QLabel("Add new monitoring object", self)
        self.label_title.setStyleSheet(styles.label_title)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_title, 0, 1, 1, 8)

        self.label_info = QLabel("", self)
        self.label_info.setStyleSheet(styles.label_info_wrong)
        self.label_info.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.label_info, 1, 1, 1, 8)

        self.label_login = QLabel("Allegro login", self)
        self.label_login.setStyleSheet(styles.label_lineEdit)
        self.gridLayout.addWidget(self.label_login, 3, 1, 1, 3)

        self.label_password = QLabel("Allegro password", self)
        self.label_password.setStyleSheet(styles.label_lineEdit)
        self.gridLayout.addWidget(self.label_password, 6, 1, 1, 3)

        self.label_email = QLabel("Email to notificate", self)
        self.label_email.setStyleSheet(styles.label_lineEdit)
        self.gridLayout.addWidget(self.label_email, 6, 5, 1, 4)

        self.label_link = QLabel("Product link", self)
        self.label_link.setStyleSheet(styles.label_lineEdit)
        self.gridLayout.addWidget(self.label_link, 9, 1, 1, 8)

        self.label_price = QLabel("Price", self)
        self.label_price.setStyleSheet(styles.label_lineEdit)
        self.gridLayout.addWidget(self.label_price, 12, 1, 1, 1)

        self.label_xpath = QLabel("Monitored element", self)
        self.label_xpath.setStyleSheet(styles.label_lineEdit)
        self.gridLayout.addWidget(self.label_xpath, 12, 3, 1, 3)

        self.label_time = QLabel("Refresh time[s]", self)
        self.label_time.setStyleSheet(styles.label_lineEdit)
        self.gridLayout.addWidget(self.label_time, 12, 7, 1, 2)

        self.pushButton_search = QPushButton(self)
        self.pushButton_search.clicked.connect(lambda: webbrowser.open('https://allegro.pl/'))
        icon = QIcon()
        icon.addFile(os.path.join(path, "img/search.png"), QSize(), QIcon.Selected, QIcon.Off)
        self.pushButton_search.setIcon(icon)
        self.pushButton_search.setIconSize(QSize(100, 100))
        self.pushButton_search.setStyleSheet("""QPushButton{border:none;}""")
        self.pushButton_search.setCursor(QCursor(Qt.PointingHandCursor))
        self.gridLayout.addWidget(self.pushButton_search, 3, 7, 3, 1)

        # Create spacers
        self.spacer_search_l = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.spacer_search_l, 5, 5, 1, 2)

        self.spacer_search_r = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.spacer_search_r, 5, 8, 1, 1)

        self.spacer_search_t = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.spacer_search_t, 2, 1, 1, 8)

        self.spacer_search_b = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.spacer_search_b, 5, 1, 1, 8)

        self.spacer_email_l = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.spacer_email_l, 7, 4, 1, 1)

        self.spacer_link_l = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.spacer_link_l, 13, 0, 1, 1)

        self.spacer_link_r = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.gridLayout.addItem(self.spacer_link_r, 13, 9, 1, 1)

        self.spacer_link_t = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.spacer_link_t, 8, 1, 1, 8)

        self.spacer_link_b = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.spacer_link_b, 11, 1, 1, 8)

        self.spacer_price_b = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.spacer_price_b, 14, 1, 1, 7)

        # create frame bottom
        self.frame_bottom = QFrame(self)
        self.frame_bottom.setStyleSheet("""QFrame{background-color: #fff; padding: 10px;}""")
        self.frame_bottom.setFrameShape(QFrame.StyledPanel)
        self.frame_bottom.setFrameShadow(QFrame.Raised)
        self.gridLayout.addWidget(self.frame_bottom, 15, 0, 1, 10)
        self.horizontalLayout_frame_bottom = QHBoxLayout(self.frame_bottom)

        self.spacer_frame_bottom_l = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_frame_bottom.addItem(self.spacer_frame_bottom_l)

        self.pushButton_bn = QPushButton("Buy when price drops", self.frame_bottom)
        self.pushButton_bn.setMinimumSize(QSize(0, 40))
        self.pushButton_bn.setStyleSheet(styles.btn_light)
        self.horizontalLayout_frame_bottom.addWidget(self.pushButton_bn)
        self.pushButton_bn.setShortcut("Return")

        self.spacer_frame_bottom_c = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_frame_bottom.addItem(self.spacer_frame_bottom_c)

        self.pushButton_monitor = QPushButton("Monitor", self.frame_bottom)
        self.pushButton_monitor.clicked.connect(lambda: self.new_link_handler(True))
        self.pushButton_monitor.setMinimumSize(QSize(0, 40))
        self.pushButton_monitor.setStyleSheet(styles.btn_dark)
        self.horizontalLayout_frame_bottom.addWidget(self.pushButton_monitor)

        self.spacer_frame_bottom_r = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_frame_bottom.addItem(self.spacer_frame_bottom_r)

        self.horizontalLayout_frame_bottom.setStretch(0, 1)
        self.horizontalLayout_frame_bottom.setStretch(1, 1)
        self.horizontalLayout_frame_bottom.setStretch(2, 2)
        self.horizontalLayout_frame_bottom.setStretch(3, 1)
        self.horizontalLayout_frame_bottom.setStretch(4, 1)
        self.timer = QTimer(self)

        auto_login, auto_pwd, auto_email, auto_time = data.get_autofill()
        self.lineEdit_login.setText(auto_login)
        self.lineEdit_password.setText(auto_pwd)
        self.lineEdit_email.setText(auto_email)
        self.lineEdit_time.setText(str(auto_time))

    def new_link_handler(self, is_monitoring):
        # check if fields were filled properly
        no_warnings = True
        is_email = False
        link = ""
        login = ""
        email = ""
        password = ""
        xpath = ""
        price = 0
        time = 60
        if self.lineEdit_email.text() == "":
            self.lineEdit_email.setStyleSheet(styles.lineEdit_warning)
            no_warnings = False
        else:
            self.lineEdit_email.setStyleSheet(styles.lineEdit)
            email = self.lineEdit_email.text()
            for symbol in email:
                if symbol == '@':
                    is_email = True
            if not is_email:
                self.lineEdit_email.setStyleSheet(styles.lineEdit_warning)
                no_warnings = False
        if self.lineEdit_login.text() == "":
            self.lineEdit_login.setStyleSheet(styles.lineEdit_warning)
            no_warnings = False
        else:
            self.lineEdit_login.setStyleSheet(styles.lineEdit)
            login = self.lineEdit_login.text()
        if self.lineEdit_link.text() == "":
            self.lineEdit_link.setStyleSheet(styles.lineEdit_warning)
            no_warnings = False
        else:
            self.lineEdit_link.setStyleSheet(styles.lineEdit)
            link = self.lineEdit_link.text()

        if self.lineEdit_password.text() == "":
            self.lineEdit_password.setStyleSheet(styles.lineEdit_warning)
            no_warnings = False
        else:
            self.lineEdit_password.setStyleSheet(styles.lineEdit)
            password = self.lineEdit_password.text()

        if self.lineEdit_price.text() == "":
            self.lineEdit_price.setStyleSheet(styles.lineEdit_warning)
            no_warnings = False
        else:
            self.lineEdit_price.setStyleSheet(styles.lineEdit)
            price = float(self.lineEdit_price.text())

        if self.lineEdit_xpath.text() == "":
            self.lineEdit_xpath.setStyleSheet(styles.lineEdit_warning)
            no_warnings = False
        else:
            self.lineEdit_xpath.setStyleSheet(styles.lineEdit)
            xpath = self.lineEdit_xpath.text()

        if self.lineEdit_time.text() == "":
            self.lineEdit_time.setStyleSheet(styles.lineEdit_warning)
            no_warnings = False
        else:
            self.lineEdit_time.setStyleSheet(styles.lineEdit)
            time = int(self.lineEdit_time.text())

        if no_warnings:
            self.lineEdit_login.clear()
            self.lineEdit_password.clear()
            self.lineEdit_email.clear()
            self.lineEdit_link.clear()
            self.lineEdit_price.clear()
            self.lineEdit_xpath.clear()
            self.lineEdit_time.clear()
            try:
                data.add_monitored_elements(login, email, password, link, price, xpath, time, is_monitoring)
                self.shared_dict['isTerminatedP2'] = True
            except InvalidArgumentException:
                self.set_info_text("Warning. Wrong link submitted", True)
            except KeyError:
                self.set_info_text("Error. This page has already monitored", True)
            else:
                self.set_info_text("Info. Object was successfully added", False)
                self.lineEdit_login.setText(self.auto_login)
                self.lineEdit_password.setText(self.auto_pwd)
                self.lineEdit_email.setText(self.auto_email)
                self.lineEdit_time.setText(self.auto_time)
                self.lineEdit_link.clear()
                self.lineEdit_price.clear()
                self.lineEdit_xpath.clear()
        else:
            self.set_info_text("Warning. Fill all field properly", True)
        return data.get_element(link)

    # def on_monitor(self):
    #     new_price = monitoring.check_if_price_lower(self.label_link, self.label_xpath, self.label_price, self.label_time)
    #     email_send.send_email(self.label_email, self.label_link, new_price)

    def set_info_text(self, text, is_warning):
        self.label_info.setText(text)
        if is_warning:
            self.label_info.setStyleSheet(styles.label_info_wrong)
        else:
            self.label_info.setStyleSheet(styles.label_info_right)
        self.timer.setInterval(5000)
        self.timer.timeout.connect(lambda: self.label_info.setText(""))
        self.timer.start()


class ElementAllegroMonitored(QFrame):

    def __init__(self, name, link, is_done, price, xpath, time, is_monitoring, parent=None, shared_dict=None):
        QFrame.__init__(self, parent)
        self.shared_dict = shared_dict
        self.setMinimumSize(QSize(0, 300))
        self.setStyleSheet("""QFrame{border-bottom: 0.5px solid #aaa;}""")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self)

        # create description frame and layout
        self.frame_description = QFrame(self)
        self.frame_description.setMinimumSize(QSize(440, 16777215))
        self.frame_description.setStyleSheet("""QFrame{border: none;}""")
        self.frame_description.setFrameShape(QFrame.StyledPanel)
        self.frame_description.setFrameShadow(QFrame.Raised)
        self.gridLayout_description = QGridLayout(self.frame_description)
        self.horizontalLayout.addWidget(self.frame_description)
        self.gridLayout_description.setColumnStretch(0, 1)
        self.gridLayout_description.setColumnStretch(1, 2)
        self.gridLayout_description.setColumnStretch(2, 3)
        self.gridLayout_description.setColumnStretch(3, 1)
        self.gridLayout_description.setColumnStretch(4, 6)

        # fill description layout
        self.label_name = QLabel(name, self.frame_description)
        self.label_name.setStyleSheet(styles.label_allegro_monitored_name)
        self.label_name.setTextFormat(Qt.MarkdownText)
        self.label_name.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)
        self.label_name.setWordWrap(False)
        self.gridLayout_description.addWidget(self.label_name, 0, 0, 1, 5)

        url_link = "<a href=\"" + link + "\" style = \" color: #838836; text-decoration: none; font-family:corbel; title=\"Go to monitored page\"\">check product</a>"
        self.label_monitored_link = QLabel(url_link, self.frame_description)
        self.label_monitored_link.setStyleSheet(styles.label_allegro_monitored_link)
        self.gridLayout_description.addWidget(self.label_monitored_link, 1, 1, 2, 2)
        self.label_monitored_link.setOpenExternalLinks(True)

        self.label_stat = QLabel(self.frame_description)
        self.label_stat.setStyleSheet(styles.label_allegro_monitored_stat)
        self.gridLayout_description.addWidget(self.label_stat, 1, 4, 1, 1)

        self.label_is_on = QLabel(self.frame_description)
        self.label_is_on.setStyleSheet(styles.label_allegro_monitored_stat)
        self.gridLayout_description.addWidget(self.label_is_on, 5, 0, 1, 2)

        self.label_new_time = QLabel("Actual refresh time[s]: " + str(time)+" s", self.frame_description)
        self.label_new_time.setStyleSheet(styles.label_allegro_monitored_stat)
        self.gridLayout_description.addWidget(self.label_new_time, 4, 0, 1, 3)

        self.lineEdit_new_time = QLineEdit(self.frame_description)
        self.lineEdit_new_time.setMinimumSize(QSize(0, 33))
        self.lineEdit_new_time.setStyleSheet(styles.lineEdit)
        self.gridLayout_description.addWidget(self.lineEdit_new_time, 4, 3, 1, 2)
        self.lineEdit_new_time.setPlaceholderText("Set new interval")

        self.label_new_price = QLabel("Actual price: " + str(price), self)
        self.label_new_price.setStyleSheet(styles.label_allegro_monitored_stat)
        self.gridLayout_description.addWidget(self.label_new_price, 3, 0, 1, 3)

        self.lineEdit_new_price = QLineEdit(self)
        self.lineEdit_new_price.setMinimumSize(QSize(0, 35))
        self.lineEdit_new_price.setStyleSheet(styles.lineEdit)
        self.gridLayout_description.addWidget(self.lineEdit_new_price, 3, 3, 1, 2)
        self.lineEdit_new_price.setPlaceholderText("Set new price")

        self.label_img_link = QLabel(self.frame_description)
        self.label_img_link.setMaximumSize(QSize(20, 20))
        self.label_img_link.setStyleSheet("""QLabel{border: none;}""")
        self.label_img_link.setPixmap(QPixmap(os.path.join(path, "img/link.png")))
        self.label_img_link.setScaledContents(True)
        self.gridLayout_description.addWidget(self.label_img_link, 1, 0, 2, 1)

        self.label_img_stat = QLabel("done", self.frame_description)
        if is_done:
            self.label_stat.setText("done")
            self.label_img_stat.setPixmap(QPixmap(os.path.join(path, "img/check.png")))
        else:
            self.label_stat.setText("in progress")
            self.label_img_stat.setPixmap(QPixmap(os.path.join(path, "img/loading.png")))
        self.label_img_stat.setMaximumSize(QSize(20, 20))
        self.label_img_stat.setStyleSheet("""QLabel{border: none;}""")
        self.label_img_stat.setScaledContents(True)
        self.gridLayout_description.addWidget(self.label_img_stat, 1, 3, 1, 1)

        self.label_img_monitor = QLabel("done", self.frame_description)
        if is_monitoring:
            monitor_text = "I am just monitoring"
            self.label_img_monitor.setPixmap(QPixmap(os.path.join(path, "img/monitoring.png")))
        else:
            monitor_text = "I am going to buy"
            self.label_img_monitor.setPixmap(QPixmap(os.path.join(path, "img/buy.png")))
        self.label_is_monitoring = QLabel(monitor_text, self)
        self.label_is_monitoring.setStyleSheet(styles.label_allegro_monitored_stat)
        self.gridLayout_description.addWidget(self.label_is_monitoring, 2, 4, 1, 1)

        self.label_img_monitor.setMaximumSize(QSize(20, 20))
        self.label_img_monitor.setStyleSheet("""QLabel{border: none;}""")
        self.label_img_monitor.setScaledContents(True)
        self.gridLayout_description.addWidget(self.label_img_monitor, 2, 3, 1, 1)





        # create spacer and delete btn
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.spacer)

        self.pushButton_delete = QPushButton(self)
        # self.pushButton_delete.clicked.connect( lambda: self.deleteLater())
        self.pushButton_delete.clicked.connect(lambda: self.on_delete(link))
        icon = QIcon()
        icon.addFile(os.path.join(path, "img/delete.png"), QSize(), QIcon.Selected, QIcon.Off)
        # icon.Active.addFile(os.path.join(path, "img/icon.png"), QSize(), QIcon.Selected, QIcon.Off)
        self.pushButton_delete.setIcon(icon)
        self.pushButton_delete.setIconSize(QSize(50, 50))
        self.pushButton_delete.setStyleSheet("""QPushButton{border:none; }""")
        self.pushButton_delete.setCursor(QCursor(Qt.PointingHandCursor))
        # self.pushButton_delete.ico
        self.horizontalLayout.addWidget(self.pushButton_delete)

        self.is_on = data.get_switch_state(link)
        self.pushButton_switch = QPushButton(self)
        self.pushButton_switch.clicked.connect(lambda: self.on_switch(link))
        self.icon_on = QIcon()
        self.icon_off = QIcon()
        self.icon_on.addFile(os.path.join(path, "img/switch_on.png"), QSize(), QIcon.Selected, QIcon.On)
        self.icon_off.addFile(os.path.join(path, "img/switch_off.png"), QSize(), QIcon.Selected, QIcon.Off)
        if self.is_on:
            self.label_is_on.setText("Disable")
            self.pushButton_switch.setIcon(self.icon_on)
        else:
            self.label_is_on.setText("Enable")
            self.pushButton_switch.setIcon(self.icon_off)
        self.pushButton_switch.setIconSize(QSize(100, 40))
        self.pushButton_switch.setStyleSheet("""QPushButton{border:none; }""")
        self.pushButton_switch.setCursor(QCursor(Qt.PointingHandCursor))
        self.gridLayout_description.addWidget(self.pushButton_switch, 5, 2, 1, 1)

        self.pushButton_save_changes = QPushButton("Save", self)
        self.pushButton_save_changes.clicked.connect(lambda: self.on_save_changes(link))
        self.pushButton_save_changes.setIconSize(QSize(100, 20))
        self.pushButton_save_changes.setStyleSheet(styles.btn_dark)
        self.pushButton_save_changes.setCursor(QCursor(Qt.PointingHandCursor))
        self.gridLayout_description.addWidget(self.pushButton_save_changes, 5, 3, 1, 2)

    def on_delete(self, link):
        data.delete_monitored_element(link)
        self.deleteLater()
        self.shared_dict['isTerminatedP2'] = True

    def on_save_changes(self, link):
        data.change_price_time(link, self.lineEdit_new_price.text(), self.lineEdit_new_time.text())
        if self.lineEdit_new_price.text() != '':
            self.label_new_price.setText("Actual price: " + self.lineEdit_new_price.text())
        if self.lineEdit_new_time.text() != '':
            self.label_new_time.setText("Actual refresh time[s]: " + self.lineEdit_new_time.text() + " s")
        self.lineEdit_new_time.clear()
        self.lineEdit_new_price.clear()
        self.shared_dict['isTerminatedP2'] = True

    def on_switch(self, link):
        # m.stop_run_monitor()
        if self.is_on:
            self.label_is_on.setText("Enable")
            self.pushButton_switch.setIcon(self.icon_off)
            self.is_on = False
            data.switch_state(self.is_on, link)
        else:
            self.label_is_on.setText("Disable")
            self.pushButton_switch.setIcon(self.icon_on)
            self.is_on = True
            data.switch_state(self.is_on, link)
        self.shared_dict['isTerminatedP2'] = True


class PageAllegroMonitored(QWidget):
    def __init__(self, parent=None, shared_dict=None):
        QWidget.__init__(self)
        parent.addWidget(self)
        self.shared_dict = shared_dict
        self.parent = parent
        self.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setStyleSheet("""QScrollArea{border: none;}""")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 654, 479))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_scroll_area = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_scroll_area.setSpacing(0)
        self.gridLayout_scroll_area.setContentsMargins(40, 0, 40, -1)

        self.label_title = QLabel("List of your monitored objects", self.scrollAreaWidgetContents)
        self.label_title.setStyleSheet(styles.label_title)
        self.label_title.setAlignment(Qt.AlignCenter)
        self.gridLayout_scroll_area.addWidget(self.label_title)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.load_list()

    def load_list(self):
        elements = data.read_monitored_elements()
        for element in elements:
            e = ElementAllegroMonitored(element['name'], element['link'], element['is_done'], element['price'],
                                        element['xpath'], element['time'], element['is_monitoring'],
                                        self.scrollAreaWidgetContents, self.shared_dict)
            self.gridLayout_scroll_area.addWidget(e)

        self.gridLayout_scroll_area.addItem(self.spacer)

    def add_to_list(self, name, link, is_done, price, xpath, time, is_monitoring):
        self.gridLayout_scroll_area.removeItem(self.spacer)
        e = ElementAllegroMonitored(name, link, is_done, price, xpath, time, is_monitoring)
        self.gridLayout_scroll_area.addWidget(e)
        self.gridLayout_scroll_area.addItem(self.spacer)


class PageAllegroOptions(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.parent = parent
        self.parent.addWidget(self)
        self.auto_login, self.auto_pwd, self.auto_email, self.auto_time = data.get_autofill()
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 7)

        self.pushButton_auto = QPushButton(self)
        self.pushButton_auto.setText("Autofill")
        self.pushButton_auto.setStyleSheet(styles.btn_allegro_ops_auto)
        self.pushButton_auto.setCheckable(True)
        self.pushButton_auto.setChecked(True)
        self.pushButton_auto.clicked.connect(lambda: self.on_auto())
        self.gridLayout.addWidget(self.pushButton_auto, 0, 0, 1, 1)

        self.pushButton_help = QPushButton(self)
        self.pushButton_help.setText("Help")
        self.pushButton_help.setStyleSheet(styles.btn_allegro_ops_auto)
        self.pushButton_help.setCheckable(True)
        self.pushButton_help.setChecked(False)
        self.pushButton_help.clicked.connect(lambda: self.on_help())
        self.gridLayout.addWidget(self.pushButton_help, 1, 0, 1, 1)

        self.spacer_btn_d = QSpacerItem(40, 20, QSizePolicy.Expanding)
        self.gridLayout.addItem(self.spacer_btn_d, 2, 0, 1, 1)

        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.setStyleSheet("""QStackedWidget{background-color: #fff;}""")
        self.gridLayout.addWidget(self.stackedWidget, 0, 1, 3, 1)

        self.widget_auto = QWidget(self.stackedWidget)
        self.widget_auto.setStyleSheet("""QWidget{background-color: #fff;}""")
        self.stackedWidget.addWidget(self.widget_auto)

        self.widget_help = QWidget(self.stackedWidget)
        self.widget_help.setStyleSheet("""QWidget{background-color: #fff;}""")
        self.stackedWidget.addWidget(self.widget_help)

        self.gridLayout_help = QVBoxLayout(self.widget_help)
        self.gridLayout_help.setContentsMargins(50, 50, 50, 50)
        self.gridLayout_help.setSpacing(50)

        self.label_help = QLabel(self.widget_help)
        self.label_help.setStyleSheet(styles.label_lineEdit)
        self.label_help.setWordWrap(True)
        self.label_help.setText(styles.help_text)
        self.gridLayout_help.addWidget(self.label_help)

        self.spacer_help = QSpacerItem(40, 20, QSizePolicy.Expanding)
        self.gridLayout_help.addItem(self.spacer_help)

        self.gridLayout_auto = QGridLayout(self.widget_auto)
        self.gridLayout_auto.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_auto.setSpacing(20)
        self.gridLayout_auto.setColumnStretch(0, 1)
        self.gridLayout_auto.setColumnStretch(1, 1)
        self.gridLayout_auto.setColumnStretch(2, 1)
        self.gridLayout_auto.setColumnStretch(3, 1)
        self.gridLayout_auto.setRowStretch(0, 3)
        self.gridLayout_auto.setRowStretch(1, 1)
        self.gridLayout_auto.setRowStretch(2, 1)
        self.gridLayout_auto.setRowStretch(3, 1)
        self.gridLayout_auto.setRowStretch(4, 1)
        self.gridLayout_auto.setRowStretch(5, 1)
        self.gridLayout_auto.setRowStretch(6, 3)

        self.lineEdit_login = QLineEdit(self.widget_auto)
        self.lineEdit_login.setMinimumSize(QSize(0, 60))
        self.lineEdit_login.setSizeIncrement(QSize(40, 40))
        self.lineEdit_login.setStyleSheet(styles.lineEdit_opt)
        self.gridLayout_auto.addWidget(self.lineEdit_login, 1, 2, 1, 1)
        self.lineEdit_login.setPlaceholderText("login or email of your account")
        self.lineEdit_login.setText(self.auto_login)

        self.lineEdit_password = QLineEdit(self.widget_auto)
        self.lineEdit_password.setMinimumSize(QSize(20, 60))
        self.lineEdit_password.setStyleSheet(styles.lineEdit_opt)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password.setReadOnly(False)
        self.gridLayout_auto.addWidget(self.lineEdit_password, 2, 2, 1, 1)
        self.lineEdit_password.setPlaceholderText("password of your account")
        self.lineEdit_password.setText(self.auto_pwd)

        self.lineEdit_email = QLineEdit(self.widget_auto)
        self.lineEdit_email.setMinimumSize(QSize(0, 60))
        self.lineEdit_email.setStyleSheet(styles.lineEdit_opt)
        self.lineEdit_email.setFrame(True)
        self.lineEdit_email.setEchoMode(QLineEdit.Normal)
        self.gridLayout_auto.addWidget(self.lineEdit_email, 3, 2, 1, 1)
        self.lineEdit_email.setPlaceholderText("email to which the notification will be sent")
        self.lineEdit_email.setText(self.auto_email)

        self.lineEdit_time = QLineEdit(self.widget_auto)
        self.lineEdit_time.setMinimumSize(QSize(0, 60))
        self.lineEdit_time.setStyleSheet(styles.lineEdit)
        self.gridLayout_auto.addWidget(self.lineEdit_time, 4, 2, 1, 1)
        self.lineEdit_time.setPlaceholderText("interval between refreshes")
        self.lineEdit_time.setText(str(self.auto_time))

        self.label_login = QLabel("Allegro login", self)
        self.label_login.setStyleSheet(styles.label_lineEdit)
        self.gridLayout_auto.addWidget(self.label_login, 1, 1, 1, 1)

        self.label_password = QLabel("Allegro password", self)
        self.label_password.setStyleSheet(styles.label_lineEdit)
        self.gridLayout_auto.addWidget(self.label_password, 2, 1, 1, 1)

        self.label_email = QLabel("Email to notificate", self)
        self.label_email.setStyleSheet(styles.label_lineEdit)
        self.gridLayout_auto.addWidget(self.label_email, 3, 1, 1, 1)

        self.label_time = QLabel("Refresh time[s]", self)
        self.label_time.setStyleSheet(styles.label_lineEdit)
        self.gridLayout_auto.addWidget(self.label_time, 4, 1, 1, 1)

        self.pushButton_set = QPushButton("Set", self.widget_auto)
        self.pushButton_set.clicked.connect(lambda: self.on_set())
        self.pushButton_set.setMinimumSize(QSize(0, 40))
        self.pushButton_set.setStyleSheet(styles.btn_dark)
        self.gridLayout_auto.addWidget(self.pushButton_set, 5, 2, 1, 1)

        self.spacer_auto_l = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_auto.addItem(self.spacer_auto_l, 1, 1, 1, 1)

        self.spacer_auto_r = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_auto.addItem(self.spacer_auto_r, 1, 3, 1, 1)

        self.spacer_auto_t = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_auto.addItem(self.spacer_auto_t, 0, 0, 1, 1)

        self.spacer_auto_b = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_auto.addItem(self.spacer_auto_b, 6, 0, 1, 1)

    def on_set(self):
        data.add_autofill(self.lineEdit_login.text(), self.lineEdit_password.text(), self.lineEdit_email.text(), int(self.lineEdit_time.text()))
        auto_login, auto_pwd, auto_email, auto_time = data.get_autofill()
        self.parent.pageAllegroAdd.lineEdit_login.setText(auto_login)
        self.parent.pageAllegroAdd.lineEdit_password.setText(auto_pwd)
        self.parent.pageAllegroAdd.lineEdit_email.setText(auto_email)
        self.parent.pageAllegroAdd.lineEdit_time.setText(str(auto_time))

    def on_auto(self):
        self.pushButton_auto.setChecked(True)
        self.pushButton_help.setChecked(False)
        self.stackedWidget.setCurrentIndex(0)

    def on_help(self):
        self.pushButton_auto.setChecked(False)
        self.pushButton_help.setChecked(True)
        self.stackedWidget.setCurrentIndex(1)


class PageAbout(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self)
        parent.addWidget(self)
        self.gridLayout_about = QGridLayout(self)

        self.frame_about = QFrame(self)
        self.frame_about.setEnabled(True)
        self.frame_about.setStyleSheet(styles.frame_about)
        self.frame_about.setFrameShape(QFrame.StyledPanel)
        self.frame_about.setFrameShadow(QFrame.Raised)
        self.gridLayout_about.addWidget(self.frame_about, 0, 1, 1, 1)

        self.gridLayout_frame_about = QGridLayout(self.frame_about)
        self.gridLayout_frame_about.setContentsMargins(-1, 60, -1, -1)

        self.spacer_about_l = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer_about_r = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.spacer_about_b = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_frame_about.addItem(self.spacer_about_l, 0, 0, 1, 1)
        self.gridLayout_frame_about.addItem(self.spacer_about_r, 0, 2, 1, 1)
        self.gridLayout_frame_about.addItem(self.spacer_about_b, 3, 1, 1, 1)

        self.label_about_name = QLabel("WebCheck", self.frame_about)
        self.label_about_name.setStyleSheet(styles.label_about_name)
        self.label_about_name.setAlignment(Qt.AlignCenter)
        self.gridLayout_frame_about.addWidget(self.label_about_name, 0, 1, 1, 1)

        self.label_about_name = QLabel("Made by Eugene Oros & Michał Piotrowski", self.frame_about)
        self.label_about_name.setStyleSheet(styles.label_about_made)
        self.label_about_name.setAlignment(Qt.AlignCenter)
        self.gridLayout_frame_about.addWidget(self.label_about_name, 1, 1, 1, 1)

        self.label_about_version = QLabel("Version 1.0.0", self.frame_about)
        self.label_about_version.setStyleSheet(styles.label_about_version)
        self.label_about_version.setAlignment(Qt.AlignCenter)
        self.gridLayout_frame_about.addWidget(self.label_about_version, 2, 0, 1, 3)

        self.label_about_c = QLabel("\u00a9 All rights reserved", self.frame_about)
        self.label_about_c.setStyleSheet(styles.label_about_c)
        self.label_about_c.setAlignment(Qt.AlignCenter)
        self.gridLayout_frame_about.addWidget(self.label_about_c, 3, 0, 1, 3)


class StackedWidget(QStackedWidget):
    def __init__(self, parent=None, shared_dict=None):
        QStackedWidget.__init__(self, parent)
        self.setStyleSheet("""QWidget{background-color:#f2ede1;}""")
        self.pageAllegroAdd = PageAllegroAdd(self, shared_dict)
        self.pageAllegroMonitored = PageAllegroMonitored(self, shared_dict)
        self.pageAllegroOptions = PageAllegroOptions(self)
        self.pageAbout = PageAbout(self)
        self.pageLoading = PageLoading(self)

    def go_to_loading(self):
        self.setCurrentIndex(4)


class MainWindow(QMainWindow):
    def __init__(self, shared_dict):
        super(MainWindow, self).__init__()
        self.shared_dict = shared_dict
        self.setStyleSheet(styles.main_window)
        self.centralWidget = QWidget(self)
        self.gridLayout_central = QGridLayout(self.centralWidget)
        self.navFrame = NavFrame(self.centralWidget)
        self.sitesFrame = SitesFrame(self.centralWidget)
        self.stackedWidget = StackedWidget(self.centralWidget, self.shared_dict)
        self.init_window()
        self.set_start_state()

    def set_start_state(self):
        # set nav btn connection
        self.navFrame.radioButton_add.toggled.connect(lambda: self.go_to_page(0))
        self.navFrame.radioButton_monitored.toggled.connect(lambda: self.go_to_page(1))
        self.navFrame.radioButton_options.toggled.connect(lambda: self.go_to_page(2))
        self.navFrame.radioButton_about.toggled.connect(lambda: self.go_to_page(3))
        self.navFrame.radioButton_add.setChecked(True)
        self.stackedWidget.pageAllegroAdd.pushButton_bn.clicked.connect(lambda: self.new_link_handler(False))

    def new_link_handler(self, is_monitor):
        element = self.stackedWidget.pageAllegroAdd.new_link_handler(is_monitor)
        if element is not None:
            self.stackedWidget.pageAllegroMonitored.add_to_list(element["name"], element["link"], element["is_done"], element["price"], element["xpath"], element["time"], element["is_monitoring"])

    def init_window(self):
        # set window
        self.setGeometry(100, 100, 900, 620)
        import os
        self.setWindowIcon(QIcon(os.path.join(path, './img/icon.png')))
        self.setWindowTitle("WebCheck")

        # set centralWidget
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setMinimumSize(QSize(900, 540))
        self.setCentralWidget(self.centralWidget)

        # set grid layout central
        self.gridLayout_central.setSpacing(0)
        self.gridLayout_central.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_central.setRowStretch(0, 1)
        self.gridLayout_central.setRowStretch(1, 10)
        self.gridLayout_central.setColumnStretch(0, 1)
        self.gridLayout_central.setColumnStretch(1, 3)
        self.gridLayout_central.addWidget(self.navFrame, 0, 0, 9, 1)
        self.gridLayout_central.addWidget(self.sitesFrame, 0, 1, 1, 1)
        self.gridLayout_central.addWidget(self.stackedWidget, 1, 1, 1, 1)

    def go_to_page(self, index):
        if index == 0:
            self.stackedWidget.setCurrentIndex(0)
        elif index == 1:
            self.stackedWidget.setCurrentIndex(1)
        elif index == 2:
            self.stackedWidget.setCurrentIndex(2)
        elif index == 3:
            self.stackedWidget.setCurrentIndex(3)
        elif index == 4:
            self.stackedWidget.setCurrentIndex(4)


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
