import sys, re
from PyQt5 import QtGui
from PyQt5.QtCore import ( Qt)

from PyQt5.QtWidgets import * 
from PyQt5.QtWidgets import QGraphicsDropShadowEffect 
import matplotlib.pyplot as plt 
import numpy as np
from ui_main import *
WINDOW_SIZE = 0 

# Main class
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint) 
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 92, 157, 150)) 
        self.inputData = []
        self.inputHot1 = []
        self.inputHot2 = []
        self.inputHotCP = []
        self.inputCold1 = []
        self.inputCold2 = []
        self.inputColdCP = [] 
        self.heatTransfer = []
        self.flowRate = []
        self.initialHotHeatLoad = 0
        self.initialColdHeatLoad = 0
        self.inputListRowIndex = 0 
        self.outputListRowIndex = 0  
        self.ccPlotXHot = []
        self.ccPlotYHot = []
        self.ccPlotXCold = []
        self.ccPlotYCold = []
        self.gccPlotX = []
        self.gccPlotY = []
        print("Welcome to the Pinch Point Calculator Project.") 
        self.ui.centralwidget.setGraphicsEffect(self.shadow) 
        self.ui.minimizeButton.clicked.connect(lambda: self.showMinimized()) 
        self.ui.closeButton.clicked.connect(lambda: self.close()) 
        self.ui.restoreButton.clicked.connect(lambda: self.restore_or_maximize_window())  
        self.ui.stackedWidget.setCurrentWidget(self.ui.controlOption)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ui Buttons ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
        self.ui.DataHeaderBtn.clicked.connect( lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.controlOption))
        self.ui.calculateBtn.clicked.connect(self.gotoCalculate)
        self.ui.calculateHeaderBtn.clicked.connect(self.gotoCalculate) 
        self.ui.addBtn.clicked.connect(self.addData)
        self.ui.clearBtn.clicked.connect(self.clearInput)
        self.ui.ccPlotBtn.clicked.connect(self.showCCPlot)
        self.ui.gccPlotBtn.clicked.connect(self.showGCCPlot)
        self.ui.ClearPlotBtn.clicked.connect(self.clearOutput)
        
        self.InputTableLineEdit = (self.ui.supplyTempLE, self.ui.targetTempLE, self.ui.cpLE, self.ui.hLE) 
        for lineEdit in self.InputTableLineEdit:
            lineEdit.returnPressed.connect(self.addData)
            
        def moveWindow(e):
            if self.isMaximized() == False:
                if e.buttons() == Qt.LeftButton:  
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()

        self.ui.main_header.mouseMoveEvent = moveWindow
        self.show()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def restore_or_maximize_window(self):
        global WINDOW_SIZE
        win_status = WINDOW_SIZE
        if win_status == 0:
            WINDOW_SIZE = 1 
            self.showMaximized()
        else:
            WINDOW_SIZE = 0 
            self.showNormal()

    def addData(self):
        inputColumnsNumber = 5
        pattern = r'^[-+]?[0-9]*\.?[0-9]+$'
        type = self.ui.comboBox.currentText()
        temp1 = self.ui.supplyTempLE.text()
        temp2 = self.ui.targetTempLE.text()
        cp = self.ui.cpLE.text()
        h = self.ui.hLE.text()
        if h == "":
            h = "0"
        if (type == "" or temp1 == "" or temp2 == "" or cp == ""):
            self.ui.message.setText("---------------- Please Fill All fields --------------") 
        else:
            if not (re.match(pattern, temp1) and re.match(pattern, temp2) and re.match(pattern, cp) and re.match(pattern, h)): 
                self.ui.message.setText("---------------- Input Data is not valid --------------") 
                return 
            if type == "Hot" and float(temp1) < float(temp2): 
                self.ui.message.setText("---------------- Hot Supply Temp must be bigger than the Target Temp --------------") 
                return  
            if type == "Cold" and float(temp1) > float(temp2): 
                self.ui.message.setText("---------------- Cold Supply Temp must be Smaller than the Target Temp --------------") 
                return 
            self.inputData.append((type,temp1,temp2,cp,h))  
            self.ui.inputList.setRowCount(0)
            for i in range(self.inputListRowIndex+1): 
                self.ui.inputList.insertRow(i) 
                for j in range(inputColumnsNumber):
                    item = QtWidgets.QTableWidgetItem(self.inputData[i][j]) 
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.inputList.setItem(i, j, item) 
            self.inputListRowIndex += 1 
            for lineEdit in self.InputTableLineEdit:
                lineEdit.clear() 

    def gotoCalculate(self): 
        if (self.checkInputItem()):
            if self.checkDelta():
                self.calculateData() 
                self.ui.stackedWidget.setCurrentWidget(self.ui.ringMeasurement)
            else:
                self.ui.message.setText("----------------  ΔT is not valid ----------------")   
        else:
            self.ui.message.setText("---------------- Input Data is not valid ----------------") 

    def checkInputItem(self): 
        if len(self.inputData) < 2:
            return False
        validHot = 0
        validCold = 0
        for item in self.inputData:
            if item[0] == 'Hot':
                validHot += 1
            elif item[0] == 'Cold':
                validCold += 1
        if validCold < 1 or validHot < 1:
            return False
        for data in self.inputData:
            for item in data:
                if item == '':
                    return False                   
        return True 
    
    def checkDelta(self): 
        pattern = r'^[-+]?[0-9]*\.?[0-9]+$'
        self.deltaT = self.ui.lineEdit_deltaT.text()
        if self.deltaT == '' or not re.match(pattern, self.deltaT): 
            return False
        return True

    def clearOutput(self):  
        self.ui.outputList.setRowCount(0)
        self.outputListRowIndex = 0 
        self.ui.qhLabel.clear()
        self.ui.qcLabel.clear()
        self.ui.AminLabel.clear()
        self.ui.pinchLabel.clear()

    def clearInput(self):
        for lineEdit in self.InputTableLineEdit:
            lineEdit.clear()
        self.ui.inputList.setRowCount(0)
        self.inputListRowIndex = 0
        self.inputData.clear()

    def calculateData(self):
        hotList, coldList = self.extractData() 
        hotFactors, coldFactors = self.calculateFacators(hotList, coldList)
        squareList = (self.calculateSquareField(hotList, coldList, hotFactors, coldFactors))  
        Qhmin, Qcmin, pinch = self.calculateQ(hotList, coldList, squareList)
        Amin, deltaTlm = self.calculateAmin()
        self.showOutputData(hotList, coldList, squareList, Qhmin, Qcmin, Amin, pinch)
        self.defineCCPlot()
        self.defineGCCPlot(hotList, coldList, squareList, Qhmin)
        self.printData(hotList, coldList, hotFactors, coldFactors, squareList, deltaTlm)

    def extractData(self):
        self.inputHot1.clear()
        self.inputHot2.clear()
        self.inputHotCP.clear()
        self.inputCold1.clear()
        self.inputCold2.clear()
        self.inputColdCP.clear()
        self.heatTransfer.clear()
        self.flowRate.clear()
        self.initialColdHeatLoad = 0
        self.initialHotHeatLoad = 0
        for item in self.inputData:
            if item[0] == "Hot":
                self.inputHot1.append(float(item[1]))
                self.inputHot2.append(float(item[2]))
                self.inputHotCP.append(float(item[3]))  
                self.initialHotHeatLoad = self.initialHotHeatLoad + ((float(item[1])-float(item[2]))*float(item[3]))
            else:
                self.inputCold1.append(float(item[1]))
                self.inputCold2.append(float(item[2]))
                self.inputColdCP.append(float(item[3]))
                self.initialColdHeatLoad = self.initialColdHeatLoad + ((float(item[2])-float(item[1]))*float(item[3]))
            self.heatTransfer.append(float(item[4]))
            self.flowRate.append(abs(float(item[3])*(float(item[2])-float(item[1]))))
        deltaT = float(self.deltaT)
 
        hotSet = set(self.inputHot1)
        for item in self.inputHot2:
            hotSet.add(item)
        for item in self.inputCold1:
            hotSet.add(item+deltaT)
        for item in self.inputCold2:
            hotSet.add(item+deltaT) 
        hotSet = sorted(hotSet, reverse=True)

        coldSet = set(self.inputCold1)
        for item in self.inputCold2:
            coldSet.add(item)
        for item in self.inputHot1:
            coldSet.add(item-deltaT)
        for item in self.inputHot2:
            coldSet.add(item-deltaT) 
        coldSet = sorted(coldSet, reverse=True)
        return list(hotSet), list(coldSet)

    def calculateFacators(self, hotList, coldList): 
        hotFactors = [[[] for j in range(len(hotList))] for i in range(len(self.inputHotCP))]  
        coldFactors = [[[] for j in range(len(coldList))] for i in range(len(self.inputColdCP))]
         
        for i, temp in enumerate(hotList):
            for j in range (len(self.inputHotCP)):
                if temp <= self.inputHot1[j] and temp >= self.inputHot2[j]:
                    hotFactors[j][i] = self.inputHotCP[j]
                else:
                    hotFactors[j][i] = 0

        for i, temp in enumerate(coldList):
            for j in range (len(self.inputColdCP)):
                if temp >= self.inputCold1[j] and temp <= self.inputCold2[j]:
                    coldFactors[j][i] = self.inputColdCP[j]
                else:
                    coldFactors[j][i] = 0
        return hotFactors, coldFactors 

    def calculateSquareField(self, hotList, coldList, hotFactors, coldFactors):
        squareList = []   
        hotFactorsFinal = [[[] for j in range(len(hotList)-1)] for i in range(len(self.inputHotCP))]  
        coldFactorsFinal = [[[] for j in range(len(coldList)-1)] for i in range(len(self.inputColdCP))]
        
        n = len(hotFactorsFinal)  
        m = len(hotFactorsFinal[0])  
        for i in range(n):   
            for j in range(m): 
                if hotFactors[i][j] == hotFactors[i][j+1]:
                    hotFactorsFinal[i][j] = hotFactors[i][j]
                else:
                    hotFactorsFinal[i][j] = 0
        
        n = len(coldFactorsFinal)  
        m = len(coldFactorsFinal[0])  
        for i in range(n):   
            for j in range(m): 
                if coldFactors[i][j] == coldFactors[i][j+1]:
                    coldFactorsFinal[i][j] = coldFactors[i][j]
                else:
                    coldFactorsFinal[i][j] = 0 
        
        for index in range(0, len(hotList) -1): 
            hotSum = 0
            coldSum = 0
            for j in range(len(hotFactorsFinal)):
                hotSum = hotSum + hotFactorsFinal[j][index]
            
            for j in range(len(coldFactorsFinal)):
                coldSum = coldSum + coldFactorsFinal[j][index]
            x = (hotSum*(hotList[index]-hotList[index+1])) - (coldSum*(coldList[index]-coldList[index+1]))
            squareList.append(round(x,3))
        return squareList

    def calculateQ(self, hotList, coldList, squareList):  
        sum = 0
        Qhmin = 0
        Qcmin = 0 
        for index in range(0, len(squareList)):
            sum = sum + squareList[index]
            if sum < 0: 
                Qhmin = abs(sum) + Qhmin
                sum = 0
                PinchIndex = index + 1
                if index + 1 == len(squareList):
                    break  

        if (sum>0) and (Qhmin == 0): 
            Qhmin = 0
            Qcmin = 0
            pinch = "There is no Pinch"
        else:  
            sum = 0
            if PinchIndex != len(squareList): 
                for index in range(PinchIndex, len(squareList)):
                    sum = sum + squareList[index]
                Qcmin = sum 
            pinch = "Hot: "+ str(hotList[PinchIndex]) + " Cold: " + str(coldList[PinchIndex])
        Qhmin = round(Qhmin, 3)
        Qcmin = round(Qcmin, 3)
        return Qhmin, Qcmin, pinch 

    def calculateAmin(self):
        Amin = 0
        self.inputHot1Sorted = sorted(self.inputHot1, reverse=True)
        self.inputHot2Sorted = sorted(self.inputHot2, reverse=False)
        self.inputCold1Sorted = sorted(self.inputCold1, reverse=False)
        self.inputCold2Sorted = sorted(self.inputCold2, reverse=True)
        Thmax = self.inputHot1Sorted[0]
        Thmin = self.inputHot2Sorted[0]
        Tcmax = self.inputCold2Sorted[0]
        Tcmin = self.inputCold1Sorted[0]
        Tdiffmin = Thmin - Tcmin
        Tdiffmax = Thmax - Tcmax
        deltaTlm = round((Tdiffmin - Tdiffmax)/np.log(Tdiffmin/Tdiffmax), 3)

        sum = 0 
        for index in range(len(self.heatTransfer)):
            if self.heatTransfer[index] == 0:
                Amin = "Input h is not Valid!" 
                break
            sum = sum + (self.flowRate[index]/self.heatTransfer[index])
        if Amin == 0:
            Amin = round((1/deltaTlm)*sum, 3)  
        return Amin, deltaTlm

    def showOutputData(self, hotList, ColdList, squareList, Qhmin, Qcmin, Amin, pinch):
        self.ui.outputList.setRowCount(0)
        index = 0
        for i in range(len(hotList)):
            self.ui.outputList.insertRow(i)
            self.ui.outputList.insertRow(i)  
        for i in range(len(hotList)):   
            item = QtWidgets.QTableWidgetItem(str(hotList[i])) 
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.outputList.setItem(index, 0, item) 
            item = QtWidgets.QTableWidgetItem(str(ColdList[i])) 
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.outputList.setItem(index, 2, item) 
            self.outputListRowIndex += 1
            index += 2

        index = 1
        for i in range(len(squareList)):   
            item = QtWidgets.QTableWidgetItem(str(squareList[i])) 
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.outputList.setItem(index, 1, item)  
            index += 2
    


        self.ui.qhLabel.setText(str(Qhmin))
        self.ui.qcLabel.setText(str(Qcmin))
        self.ui.AminLabel.setText(str(Amin))
        self.ui.pinchLabel.setText(pinch)  

    def printData(self, hotList, coldList, hotFactors, coldFactors, squareList, deltaTlm):
        print ("hotList: ", hotList)
        print ("coldList: ", coldList)
        print ("hotFactors: ", hotFactors)
        print ("coldFactors: ", coldFactors) 
        print ("squareList: ", squareList)  
        print("heatTransfer: ", self.heatTransfer)
        print("flowRate: ", self.flowRate) 
        print("deltaTlm: ", deltaTlm) 
        print("gccPlotX", self.gccPlotX)
        print("gccPlotY", self.gccPlotY)

    def defineCCPlot(self):  
        hotHeatLoad = []   
        coldHeatLoad = []  
        hotStream = self.inputHot1 + self.inputHot2 
        hotStream = set(hotStream)
        hotStream = list(hotStream)
        hotStream = sorted(hotStream, reverse=True)
        coldStream = self.inputCold1 + self.inputCold2 
        coldStream = set(coldStream)
        coldStream = list(coldStream)
        coldStream = sorted(coldStream, reverse=True)

        hotHeatLoad.append(self.initialHotHeatLoad)
        coldHeatLoad.append(self.initialColdHeatLoad)
 
        hotFactors = [[[] for j in range(len(hotStream))] for i in range(len(self.inputHotCP))]  
        coldFactors = [[[] for j in range(len(coldStream))] for i in range(len(self.inputColdCP))]
        
        for i, temp in enumerate(hotStream):
            for j in range (len(self.inputHotCP)):
                if temp <= self.inputHot1[j] and temp >= self.inputHot2[j]:
                    hotFactors[j][i] = self.inputHotCP[j]
                else:
                    hotFactors[j][i] = 0

        for i, temp in enumerate(coldStream):
            for j in range (len(self.inputColdCP)):
                if temp >= self.inputCold1[j] and temp <= self.inputCold2[j]:
                    coldFactors[j][i] = self.inputColdCP[j]
                else:
                    coldFactors[j][i] = 0 
        

        hotFactorsFinal = [[[] for j in range(len(hotStream)-1)] for i in range(len(self.inputHotCP))]  
        coldFactorsFinal = [[[] for j in range(len(coldStream)-1)] for i in range(len(self.inputColdCP))]
        
        n = len(hotFactorsFinal)  
        m = len(hotFactorsFinal[0])  
        for i in range(n):   
            for j in range(m): 
                if hotFactors[i][j] == hotFactors[i][j+1]:
                    hotFactorsFinal[i][j] = hotFactors[i][j]
                else:
                    hotFactorsFinal[i][j] = 0
        
        n = len(coldFactorsFinal)  
        m = len(coldFactorsFinal[0])  
        for i in range(n):   
            for j in range(m): 
                if coldFactors[i][j] == coldFactors[i][j+1]:
                    coldFactorsFinal[i][j] = coldFactors[i][j]
                else:
                    coldFactorsFinal[i][j] = 0  

        finalHotFactors = []
        finalColdFactors = []
        for index in range(len(hotStream) -1):  
            hotSum = 0
            for j in range(len(hotFactorsFinal)):
                hotSum = hotSum + hotFactorsFinal[j][index]
            finalHotFactors.append(hotSum)
        for index in range(len(coldStream) - 1):  
            coldSum = 0      
            for j in range(len(coldFactorsFinal)):
                coldSum = coldSum + coldFactorsFinal[j][index]
            finalColdFactors.append(coldSum)

        for index in range(0, len(hotStream)-1):
            hotHeatLoad.append(hotHeatLoad[index] + ((hotStream[index+1] - hotStream[index]) * finalHotFactors[index]))

        for index in range(0, len(coldStream)-1):
            coldHeatLoad.append(coldHeatLoad[index] + ((coldStream[index+1] - coldStream[index]) * finalColdFactors[index]))

        print("finalHotFactors: ", finalHotFactors)
        print("hotStream: ", hotStream)
        print("hotHeatLoad: ", hotHeatLoad)
        print("finalColdFactors: ", finalColdFactors)
        print("coldStream: ", coldStream)
        print("coldHeatLoad: ", coldHeatLoad)

        self.ccPlotXHot = hotHeatLoad
        self.ccPlotYHot = hotStream
        self.ccPlotXCold = coldHeatLoad
        self.ccPlotYCold = coldStream

    def defineGCCPlot(self, hotList, coldList, squareList, Qhmin):   
        self.gccPlotX.clear()
        self.gccPlotY.clear()
        self.gccPlotX.append(Qhmin)
        for index in range(0, len(squareList)):
            self.gccPlotX.append(round((self.gccPlotX[index] + squareList[index]), 3))
        for index in range(0, len(hotList)):
            self.gccPlotY.append(round((hotList[index]+coldList[index])/2,3))

    def showCCPlot(self):   
        plt.plot(self.ccPlotXHot, self.ccPlotYHot, 'ro-')
        plt.plot(self.ccPlotXCold, self.ccPlotYCold, 'bo-')
        plt.title("Composite Curve")
        plt.xlabel("H")
        plt.ylabel("T")
        plt.show()  
    
    def showGCCPlot(self):
        xmin = 0
        index = 0
        for y in self.gccPlotY:
            plt.hlines(y, xmin, self.gccPlotX[index], colors='g', linestyles='dotted', linewidth=0.8) 
            index += 1  
        for y in self.gccPlotY:
            plt.annotate(str(y), xy=(xmin, y), xytext=(xmin-4, y), ha='right', va='center')
        plt.plot(self.gccPlotX, self.gccPlotY, 'bo-')
        plt.title("Cascade Diagram")
        plt.xlabel("H")
        plt.ylabel("T")
        plt.show() 
 
if __name__ == "__main__": 
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

else:
	print(__name__, "is Failed")


