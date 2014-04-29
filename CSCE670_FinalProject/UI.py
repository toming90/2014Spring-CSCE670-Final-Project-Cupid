# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 16:18:53 2014

@author: LimingYe, YangSong, Yuanxing Yin
"""
#==============================================================================
#   import modules including:
#   PySide, sys, math, numpy, scipy, re, os, glob, cjson, shutil, random, yelpapi
#==============================================================================

from PySide import QtCore, QtGui  #用来搭建界面的两个主要包
import sys
import math, numpy as np
import scipy
from scipy.spatial import distance #用于vector space模型计算
info = {} #info作为用户输入数据存储的dictionary
info["interests"] = '' #以下是默认用户输入，可以稍作修改
info["pets"] = ['dogs']
info["height"] = []

#==============================================================================
#   user information interface
#==============================================================================

class SlidersGroup(QtGui.QGroupBox): #用户输入界面，该类实现右侧用户兴趣填写界面
    def __init__(self, orientation, title, parent=None):
        super(SlidersGroup, self).__init__(title, parent)

        slidersLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        self.setTitle("Your Interests")
        self.textEdit = QtGui.QLineEdit()
        self.textEdit.textChanged.connect(self.textChange)
        self.resize(500,500)
        self.textEdit.sizeHint()
        slidersLayout.addWidget(self.textEdit)
        self.interestEdit = QtGui.QTextEdit()
        self.interestEdit.append("Camping , Coffee and conversation , Cooking , Dining out , Fishing/Hunting , Hobbies and crafts , Movies/Videos , Music and concerts , Exploring new areas , Nightclubs/Dancing , Playing sports , Religion/Spiritual , Shopping/Antiques , Travel/Sightseeing , Video games , Watching sports , Museums and art , Wine tasting , Playing cards")
        self.submit= QtGui.QPushButton("submit")
        slidersLayout.addWidget(self.interestEdit)
        self.submit.clicked.connect(self.buttomClicked)
        slidersLayout.addWidget((self.submit))
        self.search = QtGui.QPushButton("Review Document")
        self.search.clicked.connect(self.buttomClicked)
        slidersLayout.addWidget(self.search)
        self.setLayout(slidersLayout)

#==============================================================================
#   触发函数, include document review buttom & search function buttom
#==============================================================================

    def buttomClicked(self): #触发函数
        sender = self.sender()
        if sender.text() == 'Review Document': #you can review the document in your disk
            review = reviewWindow()
            if review.exec_():
                pass
        if sender.text() == "submit": #search for Mr/Ms Right
            re = result()
            if re.exec_():
                pass
    def textChange(self, text):
        info["interests"] = str(text)

#==============================================================================
#   user interface including all the basic information the user need to fill in
#==============================================================================

class Window(QtGui.QWidget):#该类实现左边用户基本信息填写界面
    def __init__(self):
        super(Window, self).__init__()

        self.horizontalSliders = SlidersGroup(QtCore.Qt.Horizontal,
                "Horizontal")

        self.stackedWidget = QtGui.QStackedWidget()
        self.stackedWidget.addWidget(self.horizontalSliders)

        self.createControls("Controls")


        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.controlsGroup)
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)

        self.setWindowTitle("Sliders")

    def createControls(self, title):
        self.controlsGroup = QtGui.QGroupBox(title)

        NameLabel = QtGui.QLabel("Name:")
        self.NameSpinBox = QtGui.QLineEdit()
        self.NameSpinBox.textChanged.connect(self.line_edit_text_changed)

        AgeLabel = QtGui.QLabel("Age:")

        HeightLabel = QtGui.QLabel("Height:")
        self.feetSpinBox = QtGui.QLineEdit()
        self.feetSpinBox.textChanged.connect(self.feet_edit_text_changed)
        self.inchSpinBox = QtGui.QLineEdit()
        self.inchSpinBox.textChanged.connect(self.inch_edit_text_changed)

        invertedAppearance = QtGui.QCheckBox("Have Married ?")
        invertedAppearance.toggled.connect(self.setMarried)

        self.AgeSpinBox = QtGui.QSpinBox()
        self.AgeSpinBox.valueChanged[int].connect(self.setAge)
        self.AgeSpinBox.setRange(0, 100)
        self.AgeSpinBox.setSingleStep(1)

        self.HeightSpinBox = QtGui.QSpinBox()
        self.HeightSpinBox.valueChanged[int].connect(self.setHeight)
        self.HeightSpinBox.setRange(0, 200)
        self.HeightSpinBox.setSingleStep(1)

        PetLabel = QtGui.QLabel("Pets")
        orientationCombo_pet = QtGui.QComboBox()
        orientationCombo_pet.addItem("dogs")
        orientationCombo_pet.addItem("cats")
        orientationCombo_pet.addItem("No")
        orientationCombo_pet.activated[str].connect(self.setPets)

        RelationshipLabel = QtGui.QLabel("Relationship")
        orientationCombo_relationship = QtGui.QComboBox()
        orientationCombo_relationship.addItem("divorced")
        orientationCombo_relationship.addItem("never married")
        orientationCombo_relationship.addItem("currently separated")
        orientationCombo_relationship.addItem("widow / widower")
        orientationCombo_relationship.activated[str].connect(self.setRelationship)

        GenderLabel = QtGui.QLabel("Gender")
        orientationCombo_gender = QtGui.QComboBox()
        orientationCombo_gender.addItem("man")
        orientationCombo_gender.addItem("woman")
        orientationCombo_gender.activated[str].connect(self.setGender)

        HaveKidLabel = QtGui.QLabel("Have kids status")
        orientationCombo_haveK = QtGui.QComboBox()
        orientationCombo_haveK.addItem("i\'ll tell you later")
        orientationCombo_haveK.addItem("no")
        orientationCombo_haveK.addItem("yes, and they sometimes live at home")
        orientationCombo_haveK.addItem("yes, and they live away from home")
        orientationCombo_haveK.addItem("yes, and they live at home")
        orientationCombo_haveK.activated[str].connect(self.setHaveK)

        FaithLabel = QtGui.QLabel("Faith")
        orientationCombo_faith = QtGui.QComboBox()
        orientationCombo_faith.addItem("i\'ll tell you later")
        orientationCombo_faith.addItem("christian / catholic")
        orientationCombo_faith.addItem("christian / other")
        orientationCombo_faith.addItem("christian / protestant")
        orientationCombo_faith.addItem("buddhism")
        orientationCombo_faith.addItem("jewish")
        orientationCombo_faith.addItem("other")
        orientationCombo_faith.addItem("spritual but not religious")
        orientationCombo_faith.activated[str].connect(self.setFaith)

        WantsLabel = QtGui.QLabel("Want kids status")
        orientationCombo_wants = QtGui.QComboBox()
        orientationCombo_wants.addItem("i\'ll tell you later")
        orientationCombo_wants.addItem("no")
        orientationCombo_wants.addItem("probably not")
        orientationCombo_wants.addItem("no, but it\'s ok if my partner has kids")
        orientationCombo_wants.addItem("not sure")
        orientationCombo_wants.addItem("someday")
        orientationCombo_wants.addItem("definitely")
        orientationCombo_wants.activated[str].connect(self.setWants)

        BodyTypeLabel = QtGui.QLabel("Body Type")
        orientationCombo_bodyType = QtGui.QComboBox()
        orientationCombo_bodyType.addItem("i\'ll tell you later")
        orientationCombo_bodyType.addItem("slender")
        orientationCombo_bodyType.addItem("about average")
        orientationCombo_bodyType.addItem("athletic and toned")
        orientationCombo_bodyType.addItem("a few extra pounds")
        orientationCombo_bodyType.addItem("stocky")
        orientationCombo_bodyType.addItem("heavyset")
        orientationCombo_bodyType.addItem("curvy")
        orientationCombo_bodyType.addItem("big and beautiful")
        orientationCombo_bodyType.addItem("full-figured")
        orientationCombo_bodyType.activated[str].connect(self.setbodyT)

        SmokeLabel = QtGui.QLabel("Smoke condition")
        orientationCombo_smoke = QtGui.QComboBox()
        orientationCombo_smoke.addItem("i\'ll tell you later")
        orientationCombo_smoke.addItem("no way")
        orientationCombo_smoke.addItem("occasionally")
        orientationCombo_smoke.addItem("yes, but trying to quit")
        orientationCombo_smoke.addItem("daily")
        orientationCombo_smoke.addItem("cigar aficionado")
        orientationCombo_smoke.activated[str].connect(self.setSmoke)

        DrinkLabel = QtGui.QLabel("Drink status")
        orientationCombo_drink = QtGui.QComboBox()
        orientationCombo_drink.addItem("i\'ll tell you later")
        orientationCombo_drink.addItem("never")
        orientationCombo_drink.addItem("social drinker")
        orientationCombo_drink.addItem("moderately")
        orientationCombo_drink.addItem("regularly")
        orientationCombo_drink.activated[str].connect(self.setDrink)

        EthnicityLabel = QtGui.QLabel("Ethnicity")
        orientationCombo_ethnicity = QtGui.QComboBox()
        orientationCombo_ethnicity.addItem("latino / hispanic")
        orientationCombo_ethnicity.addItem("i\'ll tell you later")
        orientationCombo_ethnicity.addItem("white / caucasian")
        orientationCombo_ethnicity.addItem("black / african descent")
        orientationCombo_ethnicity.addItem("asian")
        orientationCombo_ethnicity.activated[str].connect(self.setEthnicity)

        pic = QtGui.QPixmap("find.PNG")
        picLabel = QtGui.QLabel(self)
        picLabel.setPixmap(pic)
        picLabel.resize(400,400)

        controlsLayout = QtGui.QGridLayout()
        controlsLayout.addWidget(NameLabel, 0, 0)
        controlsLayout.addWidget(picLabel, 0, 5, 8, 6)
        controlsLayout.addWidget(AgeLabel, 1, 0)
        controlsLayout.addWidget(HeightLabel, 2, 0)
        controlsLayout.addWidget(self.NameSpinBox, 0, 1)
        controlsLayout.addWidget(self.AgeSpinBox, 1, 1)
        controlsLayout.addWidget(self.HeightSpinBox, 2, 1)
        controlsLayout.addWidget(self.feetSpinBox, 3, 0)
        controlsLayout.addWidget(self.inchSpinBox, 3, 1)
        controlsLayout.addWidget(invertedAppearance, 0, 2)
        controlsLayout.addWidget(PetLabel, 4, 0)
        controlsLayout.addWidget(orientationCombo_pet, 4, 1, 1, 1)
        controlsLayout.addWidget(WantsLabel, 5, 0)
        controlsLayout.addWidget(orientationCombo_wants, 5 ,1 , 1, 1)
        controlsLayout.addWidget(GenderLabel, 6 , 0)
        controlsLayout.addWidget(orientationCombo_gender, 6, 1 , 1, 1)
        controlsLayout.addWidget(HaveKidLabel, 4, 2)
        controlsLayout.addWidget(orientationCombo_haveK, 4, 3, 1, 1)
        controlsLayout.addWidget(RelationshipLabel, 5, 2)
        controlsLayout.addWidget(orientationCombo_relationship, 5, 3, 1, 1)
        controlsLayout.addWidget(EthnicityLabel, 6 , 2)
        controlsLayout.addWidget(orientationCombo_ethnicity, 6, 3, 1, 1)
        controlsLayout.addWidget(BodyTypeLabel, 7 , 2)
        controlsLayout.addWidget(orientationCombo_bodyType, 7, 3, 1, 1)
        controlsLayout.addWidget(DrinkLabel, 7, 0)
        controlsLayout.addWidget(orientationCombo_drink, 7, 1, 1, 1)
        controlsLayout.addWidget(SmokeLabel, 8, 0)
        controlsLayout.addWidget(orientationCombo_smoke, 8, 1, 1, 1)
        controlsLayout.addWidget(FaithLabel, 8, 2)
        controlsLayout.addWidget(orientationCombo_faith, 8, 3, 1, 1)
        self.controlsGroup.setLayout(controlsLayout)

    def line_edit_text_changed(self, text):
        info["name"] = str(text)

    def feet_edit_text_changed(self, feet):
        info["height"].append(str(feet))

    def inch_edit_text_changed(self, inch):
        info['height'].append(str(inch))

    def setAge(self, age):
        info["age"] = str(age)

    def setHeight(self, height):
        info["height"].append(str(height))

    def setSmoke(self, status):
        info["smoke"] = status

    def setRelationship(self, relationship):
        info['relationship'] = relationship

    def setEthnicity(self, ethnicity):
        info['ethnicity'] = ethnicity

    def setMarried(self, married):
        info["married"] = married

    def setPets(self, pets):
        info["pets"] = []
        info["pets"].append(pets)

    def setbodyT(self, bodyT):
        info['body type'] = bodyT

    def setHaveK(self, HaveK):
        info['have kids'] = HaveK

    def setGender(self, gender):
        info['gender'] = gender

    def setFaith(self, faith):
        info['faith'] = faith

    def setWants(self, wants):
        info['wants kids'] = wants

    def setDrink(self, drink):
        info['drink'] = drink

#==============================================================================
#   review Window for user to review the document
#==============================================================================

class reviewWindow(QtGui.QMainWindow):
    def __init__(self):
        super(reviewWindow, self).__init__()
        self.init()

    def init(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()

    def showDialog(self):
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                    'E://information retrieval')
        f = open(fname, 'r')
        with f:
            data = f.read()
            self.textEdit.setText(data)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

#==============================================================================
#   result window to show the search results with next buttom
#==============================================================================

class result(QtGui.QWidget):
    def __init__(self):
        super(result, self).__init__()
        self.init()

    def init(self):
        import os, glob
        from shutil import copyfile

        result1 = self.searchFor(info, 0)

        NameLabel = QtGui.QLabel("Name:")
        self.Name = QtGui.QLineEdit()
        self.Name.setText(result1["name"])

        AgeLabel = QtGui.QLabel("Age:")
        self.Age = QtGui.QLineEdit()
        self.Age.setText(result1["age"])

        HeightLabel = QtGui.QLabel("Height:")
        self.Height = QtGui.QLineEdit()
        height_text = ''
        for word in result1['height']:
            height_text = height_text + ' ' +  word
        self.Height.setText(height_text.strip())

        GenderLabel = QtGui.QLabel("Gender:")
        self.Gender = QtGui.QLineEdit()
        self.Gender.setText(result1['gender'])

        RelationshipLabel = QtGui.QLabel("Relationship")
        self.Relationship = QtGui.QLineEdit()
        self.Relationship.setText(result1["relationship"])

        HavekidsLabel = QtGui.QLabel("Have kids")
        self.Havekids = QtGui.QLineEdit()
        self.Havekids.setText(result1["have kids"])

        WantkidsLabel = QtGui.QLabel("Wants kids")
        self.Wantskids = QtGui.QLineEdit()
        self.Wantskids.setText(result1["wants kids"])

        EthnicityLabel = QtGui.QLabel("Ethnicity")
        self.Ethnicity = QtGui.QLineEdit()
        self.Ethnicity.setText(result1["ethnicity"])

        BodytypeLabel = QtGui.QLabel("Body type")
        self.Bodytype = QtGui.QLineEdit()
        self.Bodytype.setText(result1['body type'])

        SmokeLabel = QtGui.QLabel("Smoke")
        self.Smoke = QtGui.QLineEdit()
        self.Smoke.setText(result1['smoke'])

        FaithLable = QtGui.QLabel("Faith")
        self.Faith = QtGui.QLineEdit()
        self.Faith.setText(result1['faith'])

        DrinkLabel = QtGui.QLabel("Drink")
        self.Drink = QtGui.QLineEdit()
        self.Drink.setText(result1['drink'])

        InterestLabel = QtGui.QLabel("Interests")
        self.Interest = QtGui.QLineEdit()
        string1 = ""
        for word in result1['interests']:
            string1 = string1 + word + " "
        self.Interest.setText(string1.strip())

        string2 = ""
        PetsLabel = QtGui.QLabel("Pets")
        self.Pets = QtGui.QLineEdit()
        for word in result1["pets"]:
            string2 = string2 + word + ' '
        self.Pets.setText(string2.strip())

        #==============================================================================
        #   Here you should change the dir to your photo folder
        #   The stringTemp is your whole documents folder + result1['name'] = (exact folder)
        #   stringStr = the exact picture of candidata
        #   stringDes = copy the exact picture to exact picture under the base dir (the same with QtGui.Qpixmap)
        #==============================================================================

        stringTemp = 'C:/Users/michael/PycharmProjects/test/.idea/.idea/1/' + result1['name']
        for file in glob.glob(stringTemp + '/*.jpeg'):
             stringName =  os.path.basename(file)
        stringStr = stringTemp + '/' + stringName
        stringDes = 'C:/Users/michael/PycharmProjects/test/.idea/.idea/' + result1['name'] + '.jpeg'
        copyfile(stringStr, stringDes)

        pic = QtGui.QPixmap(result1['name']+'.jpeg')
        picLabel = QtGui.QLabel(self)
        picLabel.setPixmap(pic)
        picLabel.resize(400,400)

        nextButtom = QtGui.QPushButton("Dating Place")
        nextButtom.setToolTip('push this to <b>Recommend a place to date</b>')
        nextButtom.resize(nextButtom.sizeHint())
        nextButtom.clicked.connect(self.buttomClicked)

        nextButtom1 = QtGui.QPushButton("Next")
        nextButtom1.setToolTip('<b>push to see next candidate</b>')
        nextButtom1.resize(nextButtom1.sizeHint())
        nextButtom1.clicked.connect(self.buttomClicked)

        controlsLayout = QtGui.QGridLayout()
        controlsLayout.addWidget(NameLabel, 0, 0)
        controlsLayout.addWidget(AgeLabel, 1, 0)
        controlsLayout.addWidget(picLabel, 0, 2, 11, 11)
        controlsLayout.addWidget(nextButtom, 12, 12)
        controlsLayout.addWidget(nextButtom1,12, 10)
        controlsLayout.addWidget(HeightLabel, 2, 0)
        controlsLayout.addWidget(RelationshipLabel, 3, 0)
        controlsLayout.addWidget(HavekidsLabel, 4 , 0)
        controlsLayout.addWidget(WantkidsLabel, 5, 0)
        controlsLayout.addWidget(EthnicityLabel, 6, 0)
        controlsLayout.addWidget(BodytypeLabel, 7, 0)
        controlsLayout.addWidget(SmokeLabel, 8, 0)
        controlsLayout.addWidget(DrinkLabel, 9, 0)
        controlsLayout.addWidget(InterestLabel, 10, 0)
        controlsLayout.addWidget(PetsLabel, 11, 0)
        controlsLayout.addWidget(FaithLable, 12, 0)
        controlsLayout.addWidget(self.Name, 0, 1)
        controlsLayout.addWidget(self.Age, 1, 1)
        controlsLayout.addWidget(self.Height, 2, 1)
        controlsLayout.addWidget(self.Relationship, 3, 1)
        controlsLayout.addWidget(self.Havekids, 4, 1)
        controlsLayout.addWidget(self.Wantskids, 5, 1)
        controlsLayout.addWidget(self.Ethnicity, 6, 1)
        controlsLayout.addWidget(self.Bodytype, 7, 1)
        controlsLayout.addWidget(self.Smoke, 8 , 1)
        controlsLayout.addWidget(self.Drink, 9 ,1)
        controlsLayout.addWidget(self.Interest, 10, 1)
        controlsLayout.addWidget(self.Pets, 11, 1)
        controlsLayout.addWidget(self.Faith, 12, 1)
        self.setLayout(controlsLayout)
        self.show()

    def buttomClicked(self):
        sender = self.sender()
        if sender.text() == "Dating Place":
            date = place()
            if date.exec_():
                pass
        if sender.text() == 'Next':
            second = sec()
            if second.exec_():
                pass

#==============================================================================
#   search algorithm
#   you should change the dataCollection.txt dir in your own disk
#==============================================================================

    def searchFor(self, info, rank):
        from scipy.spatial import distance
        import cjson
        import numpy as np
        import math

        index = 1
        total = {}
        with open("E:/information retrieval/finalProject/670FinalProjectData/dataCollection.txt", "r") as f:
            for line in f:
                data = cjson.decode(line)
                total[index] = data
                index += 1

        #==============================================================================
        #assign weight to every thing
        #==============================================================================
        haveK = {}
        haveK['i\'ll tell you later'] = -2
        haveK['no'] = -1
        haveK['yes, and they sometimes live at home'] = 0
        haveK['yes, and they live away from home'] = 1
        haveK['yes, and they live at home'] = 2

        wantK = {}
        wantK['i\'ll tell you later'] = -3
        wantK['no'] = -2
        wantK['probably not'] = -1
        wantK['no, but it\'s ok if my partner has kids'] = 0
        wantK['not sure'] = 1
        wantK['someday'] = 2
        wantK['definitely'] = 3

        body = {}
        body['i\'ll tell you later'] = -3
        body['slender'] = -2
        body['about average'] = -1
        body['athletic and toned'] = 0
        body['a few extra pounds'] = 1
        body['stocky'] = 2
        body['heavyset'] = 3
        body['curvy'] = 4
        body['big and beautiful'] = 5
        body['full-figured'] = -4

        smoke = {}
        smoke['i\'ll tell you later'] = -2
        smoke['no way'] = -1
        smoke['occasionally'] = 0
        smoke['yes, but trying to quit'] = 1
        smoke['daily'] = 2
        smoke['cigar aficionado'] = 3

        drink = {}
        drink['i\'ll tell you later'] = -2
        drink['never'] = -1
        drink['social drinker'] = 0
        drink['moderately'] = 1
        drink['regularly'] = 2

        #==============================================================================
        # begin to process
        #==============================================================================
        finalScore = {}
        for index,record in total.iteritems():
            TOTALSCORE = 0.0
            if info['gender'] == record['gender']:#如果同性,直接跳过
                continue
            if info['relationship'] == record['relationship']:#如果婚状相同,则加1,权重可以自行调整
                TOTALSCORE += 1
            if info['ethnicity'] == record['ethnicity']:#如果民族相同,则加1,权重可以自行调整
                TOTALSCORE += 1
            if info['faith'] == record['faith']:#如果信仰相同,则加1,权重可以自行调整
                TOTALSCORE += 1

            if math.fabs(body[info['body type']] - body[record['body type']]) != 0: #身体状况, 越远则权重越小
                TOTALSCORE += 1/math.fabs(body[info['body type']] - body[record['body type']])
            else:
                TOTALSCORE += 1

            if math.fabs(smoke[info['smoke']] - smoke[record['smoke']]) != 0: #抽烟状况,越远则权重越小
                TOTALSCORE += 1/math.fabs(smoke[info['smoke']] - smoke[record['smoke']])
            else:
                TOTALSCORE += 1

            if math.fabs(drink[info['drink']] - drink[record['drink']]) != 0:#喝酒状况,越远则权重越小
                TOTALSCORE += 1/math.fabs(drink[info['drink']] - drink[record['drink']])
            else:
                TOTALSCORE += 1

            if math.fabs(haveK[info['have kids']] - haveK[record['have kids'].split('(')[0].strip()]) != 0:#有孩子状况,越远则权重越小
                TOTALSCORE += 1/math.fabs(haveK[info['have kids']] - haveK[record['have kids'].split('(')[0].strip()])
            else:
                TOTALSCORE += 1

            if math.fabs(wantK[info['wants kids']] - wantK[record['wants kids']]) != 0:#想孩子状况,越远则权重越小
                TOTALSCORE += 1/math.fabs(wantK[info['wants kids']] - wantK[record['wants kids']])
            else:
                TOTALSCORE += 1

            if math.fabs(int(info['age']) - int(record['age'])) != 0:#年龄,差距越大则权重越小
                TOTALSCORE += 1/math.fabs(int(info['age']) - int(record['age']))
            else:
                TOTALSCORE += 1

            if math.fabs(int(info['height'][2]) - int(record['height'][2])) != 0:#身高,差距越大则权重越小
                TOTALSCORE += 1/math.fabs(int(info['height'][2]) - int(record['height'][2]))
            else:
                TOTALSCORE += 1

            for animal in info['pets']:#对于宠物, 每有一只相同宠物就多加1点,权重可以改变,必须是birds dogs cats exotic pets fish horses
                if animal in record['pets']:
                    TOTALSCORE += 1


            interest = []# stores the interest list
            lisRecord = []
            for word in info['interests'].split(","):#兴趣爱好由单一string存储
                interest.append(word.strip().lower())
                lisRecord.append(1)
            lis = []#if the word in input is in her interests, then it is 1, if not, it is 0
            for word in interest:
                if word in record["interests"]:
                    lis.append(1)
                elif word not in total[index]["interests"]:
                    lis.append(0)

            match = np.array(lisRecord)#match is the array for the input
            interestScore = np.array(lis)

            if math.isnan(1- distance.cosine(match, interestScore)):
                TOTALSCORE += 0
            else:
                TOTALSCORE += (1- distance.cosine(match, interestScore))

            finalScore[index] = TOTALSCORE

        #==============================================================================
        # sort the final result
        #==============================================================================
        finalScore_1= sorted(finalScore.iteritems(), key=lambda d:d[1], reverse = True)#排好序号后的finalScore_1是list

        return total[finalScore_1[rank][0]]


#==============================================================================
#   second result of searching function
#==============================================================================

class sec(QtGui.QWidget):
    def __init__(self):
        super(sec, self).__init__()
        self.init()

    def init(self):
        import os, glob
        from shutil import copyfile

        result1 = self.searchFor(info, 1)

        NameLabel = QtGui.QLabel("Name:")
        self.Name = QtGui.QLineEdit()
        self.Name.setText(result1["name"])

        AgeLabel = QtGui.QLabel("Age:")
        self.Age = QtGui.QLineEdit()
        self.Age.setText(result1["age"])

        HeightLabel = QtGui.QLabel("Height:")
        self.Height = QtGui.QLineEdit()
        height_text = ''
        for word in result1['height']:
            height_text = height_text + ' ' +  word
        self.Height.setText(height_text.strip())

        GenderLabel = QtGui.QLabel("Gender:")
        self.Gender = QtGui.QLineEdit()
        self.Gender.setText(result1['gender'])

        RelationshipLabel = QtGui.QLabel("Relationship")
        self.Relationship = QtGui.QLineEdit()
        self.Relationship.setText(result1["relationship"])

        HavekidsLabel = QtGui.QLabel("Have kids")
        self.Havekids = QtGui.QLineEdit()
        self.Havekids.setText(result1["have kids"])

        WantkidsLabel = QtGui.QLabel("Wants kids")
        self.Wantskids = QtGui.QLineEdit()
        self.Wantskids.setText(result1["wants kids"])

        EthnicityLabel = QtGui.QLabel("Ethnicity")
        self.Ethnicity = QtGui.QLineEdit()
        self.Ethnicity.setText(result1["ethnicity"])

        BodytypeLabel = QtGui.QLabel("Body type")
        self.Bodytype = QtGui.QLineEdit()
        self.Bodytype.setText(result1['body type'])

        SmokeLabel = QtGui.QLabel("Smoke")
        self.Smoke = QtGui.QLineEdit()
        self.Smoke.setText(result1['smoke'])

        FaithLable = QtGui.QLabel("Faith")
        self.Faith = QtGui.QLineEdit()
        self.Faith.setText(result1['faith'])

        DrinkLabel = QtGui.QLabel("Drink")
        self.Drink = QtGui.QLineEdit()
        self.Drink.setText(result1['drink'])

        InterestLabel = QtGui.QLabel("Interests")
        self.Interest = QtGui.QLineEdit()
        string1 = ""
        for word in result1['interests']:
            string1 = string1 + word + " "
        self.Interest.setText(string1.strip())

        string2 = ""
        PetsLabel = QtGui.QLabel("Pets")
        self.Pets = QtGui.QLineEdit()
        for word in result1["pets"]:
            string2 = string2 + word + ' '
        self.Pets.setText(string2.strip())

        stringTemp = 'C:/Users/michael/PycharmProjects/test/.idea/.idea/1/' + result1['name']
        for file in glob.glob(stringTemp + '/*.jpeg'):
             stringName =  os.path.basename(file)
        stringStr = stringTemp + '/' + stringName
        stringDes = 'C:/Users/michael/PycharmProjects/test/.idea/.idea/' + result1['name'] + '.jpeg'
        copyfile(stringStr, stringDes)

        pic = QtGui.QPixmap(result1['name']+'.jpeg')
        picLabel = QtGui.QLabel(self)
        picLabel.setPixmap(pic)
        picLabel.resize(400,400)

        nextButtom = QtGui.QPushButton("Dating Place")
        nextButtom.setToolTip('push this to <b>Recommend a place to date</b>')
        nextButtom.resize(nextButtom.sizeHint())
        nextButtom.clicked.connect(self.buttomClicked)


        controlsLayout = QtGui.QGridLayout()
        controlsLayout.addWidget(NameLabel, 0, 0)
        controlsLayout.addWidget(AgeLabel, 1, 0)
        controlsLayout.addWidget(picLabel, 0, 2, 11, 11)
        controlsLayout.addWidget(nextButtom, 12, 12)
        controlsLayout.addWidget(HeightLabel, 2, 0)
        controlsLayout.addWidget(RelationshipLabel, 3, 0)
        controlsLayout.addWidget(HavekidsLabel, 4 , 0)
        controlsLayout.addWidget(WantkidsLabel, 5, 0)
        controlsLayout.addWidget(EthnicityLabel, 6, 0)
        controlsLayout.addWidget(BodytypeLabel, 7, 0)
        controlsLayout.addWidget(SmokeLabel, 8, 0)
        controlsLayout.addWidget(DrinkLabel, 9, 0)
        controlsLayout.addWidget(InterestLabel, 10, 0)
        controlsLayout.addWidget(PetsLabel, 11, 0)
        controlsLayout.addWidget(FaithLable, 12, 0)
        controlsLayout.addWidget(self.Name, 0, 1)
        controlsLayout.addWidget(self.Age, 1, 1)
        controlsLayout.addWidget(self.Height, 2, 1)
        controlsLayout.addWidget(self.Relationship, 3, 1)
        controlsLayout.addWidget(self.Havekids, 4, 1)
        controlsLayout.addWidget(self.Wantskids, 5, 1)
        controlsLayout.addWidget(self.Ethnicity, 6, 1)
        controlsLayout.addWidget(self.Bodytype, 7, 1)
        controlsLayout.addWidget(self.Smoke, 8 , 1)
        controlsLayout.addWidget(self.Drink, 9 ,1)
        controlsLayout.addWidget(self.Interest, 10, 1)
        controlsLayout.addWidget(self.Pets, 11, 1)
        controlsLayout.addWidget(self.Faith, 12, 1)
        self.setLayout(controlsLayout)
        self.show()

    def buttomClicked(self):
        sender = self.sender()
        if sender.text() == "Dating Place":
            date = place()
            if date.exec_():
                pass
#==============================================================================
#   search algorithm
#   you should change the dataCollection.txt dir in your own disk
#==============================================================================

    def searchFor(self, info, rank):
        from scipy.spatial import distance
        import cjson
        import numpy as np
        import math

        index = 1
        total = {}
        with open("E:/information retrieval/finalProject/670FinalProjectData/dataCollection.txt", "r") as f:
            for line in f:
                data = cjson.decode(line)
                total[index] = data
                index += 1

        #==============================================================================
        #assign weight to every thing
        #==============================================================================
        haveK = {}
        haveK['i\'ll tell you later'] = -2
        haveK['no'] = -1
        haveK['yes, and they sometimes live at home'] = 0
        haveK['yes, and they live away from home'] = 1
        haveK['yes, and they live at home'] = 2

        wantK = {}
        wantK['i\'ll tell you later'] = -3
        wantK['no'] = -2
        wantK['probably not'] = -1
        wantK['no, but it\'s ok if my partner has kids'] = 0
        wantK['not sure'] = 1
        wantK['someday'] = 2
        wantK['definitely'] = 3

        body = {}
        body['i\'ll tell you later'] = -3
        body['slender'] = -2
        body['about average'] = -1
        body['athletic and toned'] = 0
        body['a few extra pounds'] = 1
        body['stocky'] = 2
        body['heavyset'] = 3
        body['curvy'] = 4
        body['big and beautiful'] = 5
        body['full-figured'] = -4

        smoke = {}
        smoke['i\'ll tell you later'] = -2
        smoke['no way'] = -1
        smoke['occasionally'] = 0
        smoke['yes, but trying to quit'] = 1
        smoke['daily'] = 2
        smoke['cigar aficionado'] = 3

        drink = {}
        drink['i\'ll tell you later'] = -2
        drink['never'] = -1
        drink['social drinker'] = 0
        drink['moderately'] = 1
        drink['regularly'] = 2

        #==============================================================================
        # begin to process
        #==============================================================================
        finalScore = {}
        for index,record in total.iteritems():
            TOTALSCORE = 0.0
            if info['gender'] == record['gender']:#如果同性,直接跳过
                continue
            if info['relationship'] == record['relationship']:#如果婚状相同,则加1,权重可以自行调整
                TOTALSCORE += 1
            if info['ethnicity'] == record['ethnicity']:#如果民族相同,则加1,权重可以自行调整
                TOTALSCORE += 1
            if info['faith'] == record['faith']:#如果信仰相同,则加1,权重可以自行调整
                TOTALSCORE += 1

            if math.fabs(body[info['body type']] - body[record['body type']]) != 0: #身体状况, 越远则权重越小
                TOTALSCORE += 1/math.fabs(body[info['body type']] - body[record['body type']])
            else:
                TOTALSCORE += 1

            if math.fabs(smoke[info['smoke']] - smoke[record['smoke']]) != 0: #抽烟状况,越远则权重越小
                TOTALSCORE += 1/math.fabs(smoke[info['smoke']] - smoke[record['smoke']])
            else:
                TOTALSCORE += 1

            if math.fabs(drink[info['drink']] - drink[record['drink']]) != 0:#喝酒状况,越远则权重越小
                TOTALSCORE += 1/math.fabs(drink[info['drink']] - drink[record['drink']])
            else:
                TOTALSCORE += 1

            if math.fabs(haveK[info['have kids']] - haveK[record['have kids'].split('(')[0].strip()]) != 0:#有孩子状况,越远则权重越小
                TOTALSCORE += 1/math.fabs(haveK[info['have kids']] - haveK[record['have kids'].split('(')[0].strip()])
            else:
                TOTALSCORE += 1

            if math.fabs(wantK[info['wants kids']] - wantK[record['wants kids']]) != 0:#想孩子状况,越远则权重越小
                TOTALSCORE += 1/math.fabs(wantK[info['wants kids']] - wantK[record['wants kids']])
            else:
                TOTALSCORE += 1

            if math.fabs(int(info['age']) - int(record['age'])) != 0:#年龄,差距越大则权重越小
                TOTALSCORE += 1/math.fabs(int(info['age']) - int(record['age']))
            else:
                TOTALSCORE += 1

            if math.fabs(int(info['height'][2]) - int(record['height'][2])) != 0:#身高,差距越大则权重越小
                TOTALSCORE += 1/math.fabs(int(info['height'][2]) - int(record['height'][2]))
            else:
                TOTALSCORE += 1

            for animal in info['pets']:#对于宠物, 每有一只相同宠物就多加1点,权重可以改变,必须是birds dogs cats exotic pets fish horses
                if animal in record['pets']:
                    TOTALSCORE += 1


            interest = []# stores the interest list
            lisRecord = []
            for word in info['interests'].split(","):#兴趣爱好由单一string存储
                interest.append(word.strip().lower())
                lisRecord.append(1)
            lis = []#if the word in input is in her interests, then it is 1, if not, it is 0
            for word in interest:
                if word in record["interests"]:
                    lis.append(1)
                elif word not in total[index]["interests"]:
                    lis.append(0)

            match = np.array(lisRecord)#match is the array for the input
            interestScore = np.array(lis)

            if math.isnan(1- distance.cosine(match, interestScore)):
                TOTALSCORE += 0
            else:
                TOTALSCORE += (1- distance.cosine(match, interestScore))

            finalScore[index] = TOTALSCORE

        #==============================================================================
        # sort the final result
        #==============================================================================
        finalScore_1= sorted(finalScore.iteritems(), key=lambda d:d[1], reverse = True)#排好序号后的finalScore_1是list

        return total[finalScore_1[rank][0]]

#==============================================================================
#   place we recommend for dating
#==============================================================================

class place(QtGui.QWidget):
    def __init__(self):
        super(place, self).__init__()
        self.init()
    def init(self):
        result = self.chooseArea()

        NameLabel = QtGui.QLabel("Name:")
        self.Name = QtGui.QLineEdit()
        self.Name.setText(result[0])

        string = ''
        i = 1
        AddressLabel = QtGui.QLabel("Address:")
        while(i < len(result) - 1):
            string = string + result[i]
            i = i + 1
        self.Address = QtGui.QLineEdit()
        self.Address.setText(string)

        PhoneLabel = QtGui.QLabel("Phone:")
        self.Phone = QtGui.QLineEdit()
        self.Phone.setText(result[len(result) - 1])

        string1 = ''
        string1 = result[0] + '1.PNG'
        pic = QtGui.QPixmap(string1)
        picLabel = QtGui.QLabel(self)
        picLabel.setPixmap(pic)
        picLabel.resize(300,300)

        string2 = ''
        string2 = result[0] + '2.PNG'
        picTwo = QtGui.QPixmap(string2)
        picTwoLabel = QtGui.QLabel(self)
        picTwoLabel.setPixmap(picTwo)
        picTwoLabel.resize(300,300)

        YelpButtom = QtGui.QPushButton("More from Yelp")
        YelpButtom.setToolTip('push this to <b>search a place to date</b>')
        YelpButtom.resize(YelpButtom.sizeHint())
        YelpButtom.clicked.connect(self.buttomClicked)
        self.YelpSpinBox = QtGui.QLineEdit()
        self.YelpSpinBox.textChanged.connect(self.line_edit_text_changed)


        controlsLayout = QtGui.QGridLayout()
        controlsLayout.addWidget(NameLabel, 0, 0)
        controlsLayout.addWidget(AddressLabel, 1, 0)
        controlsLayout.addWidget(picLabel, 3, 0, 2, 2)
        controlsLayout.addWidget(picTwoLabel,0, 7, 4, 4)
        controlsLayout.addWidget(PhoneLabel, 2, 0)
        controlsLayout.addWidget(self.Name, 0, 1)
        controlsLayout.addWidget(self.Address, 1, 1)
        controlsLayout.addWidget(self.Phone, 2, 1)
        controlsLayout.addWidget(YelpButtom, 6, 0)
        controlsLayout.addWidget(self.YelpSpinBox, 6, 1)
        self.setLayout(controlsLayout)
        self.show()

    def line_edit_text_changed(self, text):
        info["yelp"] = str(text)


    def buttomClicked(self):
        sender = self.sender()
        if sender.text() == "More from Yelp":
            Yelp = yelp()
            if Yelp.exec_():
                pass

#==============================================================================
#   the interface of Yelp API
#==============================================================================

    def chooseArea(self):
        from random import randint
        file = open("E://information retrieval/finalProject/place.txt", "r")
        all_text = file.readlines()
        lis = []
        for line in all_text:
            lis.append(line)
        file.close()

        result = {}
        index = 0
        for string in lis:
            record = []
            for word in string.split(","):
                record.append(word)
            result[index] = record
            index = index + 1

        num = randint(0, index)
        return result[num]

#==============================================================================
#   Yelp api for dating place
#==============================================================================

class yelp(QtGui.QWidget):
    def __init__(self):
        super(yelp, self).__init__()
        self.init()
    def init(self):
        result = self.YelpGain()

        Name1Label = QtGui.QLabel("Name:")
        self.Name1 = QtGui.QLineEdit()
        self.Name1.setText(result[1]["name"])

        id1Label = QtGui.QLabel("id:")
        self.id1 = QtGui.QLineEdit()
        self.id1.setText(result[1]["id"])

        rating1Label = QtGui.QLabel("rating:")
        self.rating1 = QtGui.QLineEdit()
        self.rating1.setText(result[1]["rating"])

        address1Label = QtGui.QLabel("address:")
        self.address1 = QtGui.QLineEdit()
        self.address1.setText(result[1]["address"])

        Name2Label = QtGui.QLabel("Name:")
        self.Name2 = QtGui.QLineEdit()
        self.Name2.setText(result[2]["name"])

        id2Label = QtGui.QLabel("id:")
        self.id2 = QtGui.QLineEdit()
        self.id2.setText(result[2]["id"])

        rating2Label = QtGui.QLabel("rating:")
        self.rating2 = QtGui.QLineEdit()
        self.rating2.setText(result[2]["rating"])

        address2Label = QtGui.QLabel("address:")
        self.address2 = QtGui.QLineEdit()
        self.address2.setText(result[2]["address"])

        Name3Label = QtGui.QLabel("Name:")
        self.Name3 = QtGui.QLineEdit()
        self.Name3.setText(result[3]["name"])

        id3Label = QtGui.QLabel("id:")
        self.id3 = QtGui.QLineEdit()
        self.id3.setText(result[3]["id"])

        rating3Label = QtGui.QLabel("rating:")
        self.rating3 = QtGui.QLineEdit()
        self.rating3.setText(result[3]["rating"])

        address3Label = QtGui.QLabel("address:")
        self.address3 = QtGui.QLineEdit()
        self.address3.setText(result[3]["address"])

        Name4Label = QtGui.QLabel("Name:")
        self.Name4 = QtGui.QLineEdit()
        self.Name4.setText(result[4]["name"])

        id4Label = QtGui.QLabel("id:")
        self.id4 = QtGui.QLineEdit()
        self.id4.setText(result[4]["id"])

        rating4Label = QtGui.QLabel("rating:")
        self.rating4 = QtGui.QLineEdit()
        self.rating4.setText(result[4]["rating"])

        address4Label = QtGui.QLabel("address:")
        self.address4 = QtGui.QLineEdit()
        self.address4.setText(result[4]["address"])

        Name5Label = QtGui.QLabel("Name:")
        self.Name5 = QtGui.QLineEdit()
        self.Name5.setText(result[5]["name"])

        id5Label = QtGui.QLabel("id:")
        self.id5 = QtGui.QLineEdit()
        self.id5.setText(result[5]["id"])

        rating5Label = QtGui.QLabel("rating:")
        self.rating5 = QtGui.QLineEdit()
        self.rating5.setText(result[5]["rating"])

        address5Label = QtGui.QLabel("address:")
        self.address5 = QtGui.QLineEdit()
        self.address5.setText(result[5]["address"])


        pic = QtGui.QPixmap('yelp.PNG')
        picLabel = QtGui.QLabel(self)
        picLabel.setPixmap(pic)
        picLabel.resize(100,100)


        controlsLayout = QtGui.QGridLayout()
        controlsLayout.addWidget(Name1Label, 3, 0)
        controlsLayout.addWidget(self.Name1, 4, 0)
        controlsLayout.addWidget(id1Label, 5, 0)
        controlsLayout.addWidget(self.id1, 6, 0)
        controlsLayout.addWidget(rating1Label, 7 , 0)
        controlsLayout.addWidget(self.rating1, 8, 0)
        controlsLayout.addWidget(address1Label, 9, 0)
        controlsLayout.addWidget(self.address1, 10, 0)
        controlsLayout.addWidget(Name2Label, 3, 2)
        controlsLayout.addWidget(self.Name2, 4, 2)
        controlsLayout.addWidget(id2Label, 5, 2)
        controlsLayout.addWidget(self.id2, 6, 2)
        controlsLayout.addWidget(rating2Label, 7 , 2)
        controlsLayout.addWidget(self.rating2, 8, 2)
        controlsLayout.addWidget(address2Label, 9, 2)
        controlsLayout.addWidget(self.address2, 10, 2)
        controlsLayout.addWidget(Name3Label, 3, 4)
        controlsLayout.addWidget(self.Name3, 4, 4)
        controlsLayout.addWidget(id3Label, 5, 4)
        controlsLayout.addWidget(self.id3, 6, 4)
        controlsLayout.addWidget(rating3Label, 7 , 4)
        controlsLayout.addWidget(self.rating3, 8, 4)
        controlsLayout.addWidget(address3Label, 9, 4)
        controlsLayout.addWidget(self.address3, 10, 4)
        controlsLayout.addWidget(Name4Label, 3, 6)
        controlsLayout.addWidget(self.Name4, 4, 6)
        controlsLayout.addWidget(id4Label, 5, 6)
        controlsLayout.addWidget(self.id4, 6, 6)
        controlsLayout.addWidget(rating4Label, 7 , 6)
        controlsLayout.addWidget(self.rating4, 8, 6)
        controlsLayout.addWidget(address4Label, 9, 6)
        controlsLayout.addWidget(self.address4, 10, 6)
        controlsLayout.addWidget(Name5Label, 3, 8)
        controlsLayout.addWidget(self.Name5, 4, 8)
        controlsLayout.addWidget(id5Label, 5, 8)
        controlsLayout.addWidget(self.id5, 6, 8)
        controlsLayout.addWidget(rating5Label, 7 , 8)
        controlsLayout.addWidget(self.rating5, 8, 8)
        controlsLayout.addWidget(address5Label, 9, 8)
        controlsLayout.addWidget(self.address5, 10, 8)
        controlsLayout.addWidget(picLabel, 0, 0, 2, 4)
        self.setLayout(controlsLayout)
        self.show()

    def YelpGain(self):
        from yelpapi import YelpAPI
        MY_CONSUMER_KEY = 'dae5HXBIXTb0ChnDZkzB3w'
        MY_CONSUMER_SECRET = 'qanTfPX5tMyh2hUFOMv-GgHgEUQ'
        MY_ACCESS_TOKEN = '60i6KZ_lUoOMuqZKb1yUsQ4EuRZweqS5'
        MY_ACCESS_SECRET = '0__YQm18_g2jUsMcbu6THu3edpA'

        yelp_api = YelpAPI(consumer_key=MY_CONSUMER_KEY,
                    consumer_secret=MY_CONSUMER_SECRET,
                    token=MY_ACCESS_TOKEN,
                    token_secret=MY_ACCESS_SECRET)

        yelpResult = {}
        index = 1
        response = yelp_api.search_query(term=info['yelp'], location='college station, tx', sort=2, limit=5)
        for business in response['businesses']:
            result = {}
            result['name'] = str(business['name'])
            result['id'] = str(business['id'])
            result['rating'] = str(business['rating'])+ "(" + str(business['review_count'])+'reviews' + ")"
            result['address'] = ', '.join(business['location']['display_address'])
            yelpResult[index] = result
            index = index + 1
        return yelpResult


#==============================================================================
#   Main function
#==============================================================================

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())