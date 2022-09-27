# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

import json
import h5py

QUESTION_JSON = 'val2014/v2_OpenEnded_mscoco_val2014_questions.json'
MYMODEL_JSON = 'val2014/val_answer.json'
ANSWER_JSON = 'val2014/v2_mscoco_val2014_annotations.json'

def get_real_answer(qid):
    global answer_json

    for elem in answer_json['annotations']:
        # criteria: question_id
        if elem['question_id'] == qid:
            return elem['multiple_choice_answer']
    
    return 'NO SUCH QID!!'

def get_mymodel_answer(qid):
    global mymodel_json

    for elem in mymodel_json:
        if elem['question_id'] == qid:
            return elem['answer']

def get_question_sentence(qid):
    global question_json

    for elem in question_json['questions']:
        if elem['question_id'] == qid:
            return elem['question']
    
    return 'no such QID!'

def get_imageId(qid):
    global question_json

    for elem in question_json['questions']:
        if elem['question_id'] == qid:
            return elem['image_id']

class Ui_MainWindow(QtWidgets.QMainWindow):
    
    image_id = 0
    question_id = 0

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1241, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(630, 90, 112, 34))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.button2_event)

        # self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit.setGeometry(QtCore.QRect(260, 50, 321, 31))
        # self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(260, 90, 321, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 290, 800, 500))
        self.graphicsView.setObjectName("graphicsView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 60, 111, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(126, 100, 111, 20))
        self.label_2.setObjectName("label_2")

        # Model's Output
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(840, 290, 311, 81))
        self.textBrowser.setObjectName("textBrowser")

        # Real Answer
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_2.setGeometry(QtCore.QRect(840, 420, 311, 81))
        self.textBrowser_2.setObjectName("textBrowser_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(840, 260, 151, 18))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(840, 390, 151, 18))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 260, 151, 18))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 170, 151, 18))
        self.label_6.setObjectName("label_6")

        # Question
        self.textBrowser_3 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_3.setGeometry(QtCore.QRect(150, 170, 611, 51))
        self.textBrowser_3.setObjectName("textBrowser_3")

        self.textBrowser_4 = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_4.setGeometry(QtCore.QRect(260, 50, 321, 31))
        self.textBrowser_4.setObjectName("textBrowser_4")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1241, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # self.scene = QtWidgets.QGraphicsScene()
        # self.gv.setScene(self.scene)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_2.setText(_translate("MainWindow", "확인"))
        self.label.setText(_translate("MainWindow", "Image ID"))
        self.label_2.setText(_translate("MainWindow", "Question ID"))
        self.label_3.setText(_translate("MainWindow", "Model\'s output"))
        self.label_4.setText(_translate("MainWindow", "Real Answer"))
        self.label_5.setText(_translate("MainWindow", "Image"))
        self.label_6.setText(_translate("MainWindow", "Question"))

    def button_event(self):
        text = self.lineEdit.text() # line_edit text 값 가져오기
        image_id = text
    
    def button2_event(self):
        text = self.lineEdit_2.text() # line_edit text 값 가져오기
        question_id = int(text)

        # print(get_question_sentence(question_id))
        # print(get_mymodel_answer(question_id))
        # print(get_real_answer(question_id))

        self.textBrowser.setPlainText(get_mymodel_answer(question_id))
        self.textBrowser_2.setPlainText(get_real_answer(question_id))
        self.textBrowser_3.setPlainText(get_question_sentence(question_id))
        self.textBrowser_4.setPlainText(str(get_imageId(question_id)))
        
        image_path = 'val2014/COCO_val2014_{img}.jpg'.format(img=str(get_imageId(question_id)).zfill(12))
        print(image_path)
        pix = QtGui.QPixmap(image_path)
        item = QtWidgets.QGraphicsPixmapItem(pix)
        scene = QtWidgets.QGraphicsScene(self)
        scene.addItem(item)
        self.graphicsView.setScene(scene)

if __name__ == "__main__":
    import sys

    print('opening json files ...')
    with open(QUESTION_JSON) as f:
        question_json = json.load(f)
    with open(MYMODEL_JSON) as f:
        mymodel_json = json.load(f)
    with open(ANSWER_JSON) as f:
        answer_json = json.load(f)
    print('finished opening json!')

    print('opening h5py file ...')
    h5py_file = h5py.File('val.hdf5', 'r')
    print(h5py_file.keys())
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

