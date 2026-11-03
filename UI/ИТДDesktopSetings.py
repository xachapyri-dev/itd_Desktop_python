# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Setings.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt6.QtWidgets import (QApplication, QCheckBox, QCommandLinkButton, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(440, 400)
        MainWindow.setMinimumSize(QSize(440, 400))
        MainWindow.setMaximumSize(QSize(440, 400))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 451, 411))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 50, 121, 21))
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.TextFormat.AutoText)
        self.label.setScaledContents(False)
        self.lineEdit = QLineEdit(self.tab)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(20, 80, 301, 22))
        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(330, 80, 101, 24))
        self.label_6 = QLabel(self.tab)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 110, 121, 21))
        self.label_6.setFont(font)
        self.label_6.setTextFormat(Qt.TextFormat.AutoText)
        self.label_6.setScaledContents(False)
        self.pushButton_2 = QPushButton(self.tab)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(20, 140, 171, 24))
        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 0, 121, 21))
        self.label_8.setFont(font)
        self.label_8.setTextFormat(Qt.TextFormat.AutoText)
        self.label_8.setScaledContents(False)
        self.checkBox_2 = QCheckBox(self.tab)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(20, 30, 101, 20))
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.checkBox = QCheckBox(self.tab_2)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setGeometry(QRect(20, 10, 141, 20))
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.label_2 = QLabel(self.tab_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 0, 301, 21))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.label_2.setFont(font1)
        self.label_4 = QLabel(self.tab_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(30, 70, 351, 41))
        self.label_4.setTextFormat(Qt.TextFormat.PlainText)
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_4.setWordWrap(True)
        self.label_3 = QLabel(self.tab_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 50, 81, 16))
        self.label_3.setFont(font)
        self.verticalLayoutWidget = QWidget(self.tab_3)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 110, 339, 184))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.commandLinkButton = QCommandLinkButton(self.verticalLayoutWidget)
        self.commandLinkButton.setObjectName(u"commandLinkButton")
        self.commandLinkButton.setDefault(False)

        self.verticalLayout.addWidget(self.commandLinkButton)

        self.commandLinkButton_2 = QCommandLinkButton(self.verticalLayoutWidget)
        self.commandLinkButton_2.setObjectName(u"commandLinkButton_2")
        self.commandLinkButton_2.setDefault(False)

        self.verticalLayout.addWidget(self.commandLinkButton_2)

        self.commandLinkButton_3 = QCommandLinkButton(self.verticalLayoutWidget)
        self.commandLinkButton_3.setObjectName(u"commandLinkButton_3")
        self.commandLinkButton_3.setDefault(False)

        self.verticalLayout.addWidget(self.commandLinkButton_3)

        self.commandLinkButton_4 = QCommandLinkButton(self.verticalLayoutWidget)
        self.commandLinkButton_4.setObjectName(u"commandLinkButton_4")
        self.commandLinkButton_4.setDefault(False)

        self.verticalLayout.addWidget(self.commandLinkButton_4)

        self.label_5 = QLabel(self.tab_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 300, 181, 16))
        self.label_5.setFont(font)
        self.commandLinkButton_5 = QCommandLinkButton(self.tab_3)
        self.commandLinkButton_5.setObjectName(u"commandLinkButton_5")
        self.commandLinkButton_5.setGeometry(QRect(30, 330, 221, 41))
        self.label_7 = QLabel(self.tab_3)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 30, 221, 16))
        self.label_7.setFont(font)
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u043f\u043a\u0430 \u0437\u0430\u0433\u0440\u0443\u0437\u043e\u043a", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u043f\u0430\u043f\u043a\u0443", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u041e\u043f\u0430\u0441\u043d\u043e!!!", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435 \u0431\u0440\u0430\u0443\u0437\u0435\u0440\u0430", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u0435", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u0410\u0432\u0442\u043e\u0437\u0430\u043f\u0443\u0441\u043a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 Chromium", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\u0422\u0451\u043c\u043d\u0430\u044f \u0442\u0435\u043c\u0430", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u0422\u0435\u043c\u0430", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0422\u0414 Desktop \u0414\u043b\u044f Linux \u0438 macOS", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0422\u0414 Desktop \u0414\u043b\u044f Linux \u0438 macOS - \u041a\u043b\u0438\u0435\u043d\u0442 \u0441\u043e\u0446.\u0441\u0435\u0442\u0438 \"\u0418\u0422\u0414\" \u0434\u043b\u044f Linux \u0438 macOS \u043d\u0430\u043f\u0438\u0441\u0430\u043d\u043d\u044b\u0439 \u043d\u0430 Python \u0441 PyQt6", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u041e \u043a\u043b\u0438\u0435\u043d\u0442\u0435", None))
        self.commandLinkButton.setText(QCoreApplication.translate("MainWindow", u"GitHub \u0440\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0440\u0438\u0439", None))
        self.commandLinkButton_2.setText(QCoreApplication.translate("MainWindow", u"Github \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a\u0430 \u043a\u043b\u0438\u0435\u043d\u0442-\u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f", None))
        self.commandLinkButton_3.setText(QCoreApplication.translate("MainWindow", u"Telegram-\u043a\u0430\u043d\u0430\u043b nowkie", None))
        self.commandLinkButton_4.setText(QCoreApplication.translate("MainWindow", u"Telegram-\u043a\u0430\u043d\u0430\u043b \u0425\u0430\u0447\u0430\u043f\u0443\u0440\u0438 dev", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438 \u043e\u0448\u0438\u0431\u043a\u0430\u0445 \u0438\u043b\u0438 \u0431\u0430\u0433\u0430\u0445", None))
        self.commandLinkButton_5.setText(QCoreApplication.translate("MainWindow", u"\u0418\u0422\u0414 Desktop Github issue", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0435\u0440\u0441\u0438\u044f: ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u041e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0435", None))
    # retranslateUi

