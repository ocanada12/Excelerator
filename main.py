import sys
import serial
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import numpy as np
import cv2
import threading
import time
import sys
from PyQt5 import uic
import time

import pyautogui
import keyboard
from PIL import ImageGrab, Image
import io
import qimage2ndarray
import cv2
import numpy as np
from PIL import Image
import time
import pyautogui
import keyboard
import io
from PIL import ImageGrab
from PIL import Image

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
motorstep = 0
flag1 = 0
flag2 = 0
flag3 = 0
flag4 = 0
a1 = 100
a2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
a3 = 0
a4 = [100, 50, 10]
a5 = 100
seconds = 0
lists = [500, 500, 500, 500, 500, 500, 500, 500, 100]
escape2 = 10
list1 = ["A","B","C","D","E","F","G","H","I","J"]

class mainWindow(QMainWindow):

    def __init__(self):
        global ser
        super().__init__()
        loadUi("untitled.ui", self)
        self.pushButton_Ready.clicked.connect(self.Ready)
        self.pushButton_Start.clicked.connect(self.Start)
        self.pushButton_Setting.clicked.connect(self.Setting)
        self.pushButton_cameraStart.clicked.connect(self.actionFunction1)
        self.pushButton_cameraStop.clicked.connect(self.stopActionFunction1)
        self.pushButton_secondsStart.clicked.connect(self.actionFunction2)
        self.pushButton_secondsStop.clicked.connect(self.stopActionFunction2)
        self.pushButton.clicked.connect(self.savePicture)
        self.pushButton_2.clicked.connect(self.savePicture)
        self.pushButton_loadimage.clicked.connect(self.loadimage)
        self.read()
        self.show()

    def loadimage(self):
        try:
            print("이미지로드")
            pyautogui.keyDown('alt')
            pyautogui.press('printscreen')
            pyautogui.keyUp('alt')
            im = ImageGrab.grabclipboard()
            print(im.size)
            numpy_image = np.array(im)
            print(len(numpy_image))
            numpy_image = numpy_image[0:100,0:100]
            qimage_var = qimage2ndarray.array2qimage(numpy_image, normalize=False)
            qpixmap_var = QPixmap.fromImage(qimage_var)
            self.pixmap.setPixmap(qpixmap_var)
            print("이미지로드완성")
        except Exception as e:
            print(e)

    def Setting(self):
        print("세팅창 뜨기")
        self.setting = setting()
        self.setting.show()
        ## 시그널 받는곳 + 시그널 함수 연결
        self.setting.signal3.connect(self.signal3_emitted)

    def read(self):
        global a4
        f = open('C:/Exopert/level.txt', 'r')
        for i in range(0, 3):
            a4[i] = int(f.readline().strip())
        print(a4)
        f.close()

    def Ready(self):
        global motorstep
        motorstep = -3600
        print("1번튜브로")

    #        global ser
    #        val = "CC@;"
    #        val = val.encode('utf-8')
    #        ser.write(val)

    def Start(self):
        global a2
        print("레디")
        print(a2)

    def actionFunction1(self):
        global flag1
        if flag1 == 0:
            self.Thread1 = Thread1()
            self.Thread1.start()
            self.Thread1.signal1.connect(self.signal1_emitted)
            flag1 = 1
        else:
            print("1번 이미 실행중임")

    def stopActionFunction1(self):
        global flag1
        global a3
        a3 = 0
        quit_msg = "끌꺼임?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.Thread1.stop()
            flag1 = 0
        else:
            print("계속")

    def savePicture(self):
        quit_msg = "사진찍을래?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.Thread1.savePic()
        else:
            print("계속")

            # 경주마2 출발 버튼을 눌렀을 때 실행 될 메서드

    def actionFunction2(self):
        global flag2
        if flag2 == 0:
            self.Thread2 = Thread2()
            self.Thread2.start()
            self.Thread2.signal2.connect(self.signal2_emitted)
            flag2 = 1
        else:
            print("2번 이미 실행중임")

    def stopActionFunction2(self):
        global flag2
        quit_msg = "끌꺼임?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.Thread2.stop()
            flag2 = 0
        else:
            print("계속")

    @pyqtSlot(int)
    def signal1_emitted(self, level):
        global motorstep
        global a3
        global flag1
        global flag2
        self.label.setText(str(level))
        self.label_2.setText(str(motorstep))
        if a3 == 8:
            self.Thread2.stop()
            self.Thread1.stop()
            flag2 = 0
            flag1 = 0
            motorstep = 0
            a3 = 0

    @pyqtSlot(int)
    def signal2_emitted(self, seconds):
        self.label_3.setText(str(seconds))

    ## 시그널 받기
    @pyqtSlot(list)
    def signal3_emitted(self, lists):
        global a2
        a2 = lists
        print(a2)


# 카메라 쓰레드
class Thread1(QThread):
    signal1 = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.power = True

    def savePic(self):
        global flag3
        print("ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
        flag3 = 1
        print(flag3)
        print("ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")

    def sendmotor(self):
        global motorstep
        motorstep += 400

    def stop(self):
        self.power = False
        self.quit()
        self.wait(3000)

    def run(self):
        global flag3
        global flag4
        global seconds
        global capture
        global a1
        global a2
        global a3
        global a4
        global a5
        global escape2
        global list1
        while self.power:
            time.sleep(0.2)
            ret, frame = capture.read()
            if flag3 == 1:
                img_capture = cv2.imwrite(list1[flag4]+'.png',frame)
                flag3 = 0
                print(flag3)
                print("사진찍기 완료")
                flag4 += 1
                print(flag4)
            if cv2.waitKey(10) > 0:
                break
            bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            max = 0;
            escape = 10;
            level = 480
            print(str(a3) + "번 튜브")

            if escape2 == 0:
                self.sendmotor()
                seconds = 0
                a3 += 1
                escape2 = 10
            else:
                print("아직 아님")

            if a2[a3] == 500:
                a5 = a4[0]
            elif a2[a3] == 1000:
                a5 = a4[1]
            else:
                a5 = a4[2]

            for i in range(1, 180):
                if (bw[i + 10].sum() - bw[i].sum()) >= 5000:
                    escape -= 1
                if escape <= 0:
                    level = i
                    self.signal1.emit(level)
                    if level >= a5:
                        if seconds <= 200:
                            escape = 10
                        else:
                            print(escape2)
                            escape2 -= 1
                            break


# 시간 표시 쓰레드
class Thread2(QThread):
    signal2 = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.power = True

    def stop(self):
        seconds = 0
        self.power = False
        self.quit()
        self.wait(100)

    def run(self):
        global seconds
        seconds = 0
        while self.power:
            time.sleep(0.1)
            seconds += 1
            self.signal2.emit(seconds)


class setting(QWidget):
    ## 시그널 보내는 곳에서 생성
    signal3 = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        loadUi("setting.ui", self)
        self.pushButton.clicked.connect(self.jundal)
        self.pushButton_1.clicked.connect(lambda: self.tube(0))
        self.pushButton_2.clicked.connect(lambda: self.tube(1))
        self.pushButton_3.clicked.connect(lambda: self.tube(2))
        self.pushButton_4.clicked.connect(lambda: self.tube(3))
        self.pushButton_5.clicked.connect(lambda: self.tube(4))
        self.pushButton_6.clicked.connect(lambda: self.tube(5))
        self.pushButton_7.clicked.connect(lambda: self.tube(6))
        self.pushButton_8.clicked.connect(lambda: self.tube(7))
        self.show()

    def jundal(self):
        global lists
        ## 시그널 보내기
        self.signal3.emit(lists)
        self.close()

    def tube(self, no):
        global lists
        if lists[no] == 500:
            lists[no] = 1000
        elif lists[no] == 1000:
            lists[no] = 1500
        else:
            lists[no] = 500


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())