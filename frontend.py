import base64
import os
import re
from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QMessageBox, QComboBox, QFormLayout
import sys
import backend.slapper as slapper #TODO: update name 
import json
import helper.requestSender as requestSender
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.request_sender = requestSender.RequestSender("http://127.0.0.1:5000")
        self.request_sender = requestSender.RequestSender("http://52.91.85.117:5000")    # connect to EC2 instance 

        self.setWindowTitle("Hand Gesture Login") # TODO: COME UP WITH A CREATIVE NAME 
        
        self.resize(1000,600)
        
        # init stacked widget
        self.stackedWidget = QStackedWidget()     
        self.setMainMenu()
        
        # Set up the stacked widget as the first one 
        init_Layout = QVBoxLayout()
        init_Layout.addWidget(self.stackedWidget)
        self.setLayout(init_Layout)
        
    
    
    # Function to set the Main Menu (initial screen)    
    def setMainMenu(self):
        mainMenuWidget = QWidget()
        mainLayout = QVBoxLayout()
        # Log In Flow 
        loginLabel = QLabel("Returning users can log in below:")
        mainLayout.addWidget(loginLabel)
        loginFlowButton = QPushButton("Log In")
        loginFlowButton.clicked.connect(self.setLoginPageUsername)
        mainLayout.addWidget(loginFlowButton)
        
        # Register Flow Label
        registerLabel = QLabel("New User? Create an account:")
        mainLayout.addWidget(registerLabel)
        registerFlowButton = QPushButton("Register")
        registerFlowButton.clicked.connect(self.createRegisterUserPage)
        mainLayout.addWidget(registerFlowButton)
        
        mainMenuWidget.setLayout(mainLayout)
        
        self.stackedWidget.addWidget(mainMenuWidget)

        # self.setLayout(self.mainLayout) # important 
    
    
    # Function to set the Login page to enter username     
    def setLoginPageUsername(self):
        loginWidget_1 = QWidget()
        login1 = QVBoxLayout() # Create vertical box layout
        
        userLabel = QLabel("Enter Email below")
        login1.addWidget(userLabel)
        self.usernameField = QLineEdit()
        login1.addWidget(self.usernameField)
        loginFlowButton = QPushButton("Next")
        login1.addWidget(loginFlowButton)
        loginFlowButton.clicked.connect(self.checkUserExists) # check user exists function then checks
        
        goBackButton = QPushButton("Cancel")
        login1.addWidget(goBackButton)
        goBackButton.clicked.connect(self.goBackToMainMenu)

        loginWidget_1.setLayout(login1) 
        
        self.stackedWidget.addWidget(loginWidget_1)
        
        self.stackedWidget.setCurrentWidget(loginWidget_1)
        
    
    # Function to go back to main menu screen 
    def goBackToMainMenu(self):
        self.stackedWidget.setCurrentIndex(0)
    
        
    # TODO: Add implementation so that it checks that the username exists    
    def checkUserExists(self):
        # self.setPassword1()
        email = self.usernameField.text().strip()
        try: 
            password = slapper.main()
            # password = "1230"
            with open('public_key.pem', "rb") as f:    # read in binary 
                public_key = f.read()
                public_key = serialization.load_pem_public_key(public_key)
            encrypted_password = public_key.encrypt(
                password.encode(),  # Convert password to bytes
                padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
                )
    )
            encrypted_password_base64 = base64.b64encode(encrypted_password).decode('utf-8')
            login_response = self.request_sender.login(email, encrypted_password_base64)
            if login_response['status'] == 200:
                login_success_Notif = QMessageBox()
                login_success_Notif.setText("Login successful, congrads!!")
                login_success_Notif.setIcon(QMessageBox.Information)
                login_success_Notif.exec_()
                self.goBackToMainMenu()
            else:
                login_fail_Notif = QMessageBox()
                login_fail_Notif.setText("Login failed, try again!")
                login_fail_Notif.setIcon(QMessageBox.Critical)
                login_fail_Notif.exec_()
                self.goBackToMainMenu()
            print(login_response)
        except Exception as e: 
            print(e)
        
        # TODO: make it call the next screen
        
    # Function to set the Registration page   
    def createRegisterUserPage(self):
        registerWidget = QWidget()
        registerPage = QVBoxLayout() # Create vertical box layout
        
        userLabel_1 = QLabel("Enter Email below:")
        registerPage.addWidget(userLabel_1)
        self.user_email_field = QLineEdit()
        registerPage.addWidget(self.user_email_field)
        
        userLabel_2 = QLabel("Confirm your email:")
        registerPage.addWidget(userLabel_2)
        self.user_email_confirmation = QLineEdit()
        registerPage.addWidget(self.user_email_confirmation)

        userLabel_3 = QLabel("Enter your password:")
        registerPage.addWidget(userLabel_3)
        self.user_password_registration = QLineEdit()
        registerPage.addWidget(self.user_password_registration)

        userLabel_4 = QLabel("Confirm your password:")
        registerPage.addWidget(userLabel_4)
        self.user_password_confirmation = QLineEdit()
        registerPage.addWidget(self.user_password_confirmation)
        
        
        nextButton = QPushButton("Next")
        registerPage.addWidget(nextButton)
        nextButton.clicked.connect(self.checkValidRegistration)
        
        goBackButton = QPushButton("Cancel")
        registerPage.addWidget(goBackButton)
        goBackButton.clicked.connect(self.goBackToMainMenu)
        
        
        
        # loginFlowButton = QPushButton("Next")
        # login1.addWidget(loginFlowButton)
        # loginFlowButton.clicked.connect(self.checkUserExists) # check user exists function then checks

        registerWidget.setLayout(registerPage) 
        
        self.stackedWidget.addWidget(registerWidget)
        
        self.stackedWidget.setCurrentWidget(registerWidget)
    
    def checkValidRegistration(self):
        valid_email = self.checkValidEmail()
        valid_password = self.checkValidPassword()
        if (valid_email and valid_password):
            try: 
                register_response = self.request_sender.registration(self.user_email_field.text(), self.user_password_registration.text())
                public_key = register_response['message']['public_key']
                print(public_key)
                with open("public_key.pem", "w") as f:
                    f.write(public_key)
                print("Public key saved locally")
                register_success_Notif = QMessageBox()
                register_success_Notif.setText("Registration successful, redirecting back to home page.")
                register_success_Notif.setIcon(QMessageBox.Information)
                register_success_Notif.exec_()
                self.goBackToMainMenu()
            except Exception as e: 
                register_fail_Notif = QMessageBox()
                register_fail_Notif.setText("Registration failed, redirecting back to home page.")
                register_fail_Notif.setIcon(QMessageBox.Critical)
                register_fail_Notif.exec_()
                self.goBackToMainMenu()
                print(e)
        # TODO redirect to main page after successful registraton
        


    def checkValidPassword(self):
        pattern = r'[4-9]'
        first_user_password = self.user_password_registration.text()
        second_user_password = self.user_password_confirmation.text()
        if re.search(pattern, first_user_password):
            invalid_Notif = QMessageBox()
            invalid_Notif.setText("Invalid password detected. Can only set from digits 0 to 3")
            invalid_Notif.setIcon(QMessageBox.Critical)
            invalid_Notif.exec_()
            return False
        if first_user_password == "" or second_user_password == "":
            invalid_Notif = QMessageBox()
            invalid_Notif.setText("Invalid password detected. Please try again")
            invalid_Notif.setIcon(QMessageBox.Critical)
            invalid_Notif.exec_()
            return False
        elif first_user_password != second_user_password:
            mismatch_Notif = QMessageBox()
            mismatch_Notif.setText("Password do not match! Please try again")
            mismatch_Notif.setIcon(QMessageBox.Critical)
            mismatch_Notif.exec_()
            return False
        return True
        
    def checkValidEmail(self):
        first_user_email = self.user_email_field.text()
        second_user_email = self.user_email_confirmation.text()
        if first_user_email == "" or second_user_email == "":
            invalid_Notif = QMessageBox()
            invalid_Notif.setText("Invalid email detected. Please try again")
            invalid_Notif.setIcon(QMessageBox.Critical)
            invalid_Notif.exec_()
            return False
        elif first_user_email != second_user_email:
            mismatch_Notif = QMessageBox()
            mismatch_Notif.setText("Emails do not match! Please try again")
            mismatch_Notif.setIcon(QMessageBox.Critical)
            mismatch_Notif.exec_()
            return False
        else:
             ## TODO: add case to check if email exists 
            # email = {
            #     "email": first_user_email
            # }
            # valToSend = json.dumps(email)

            try: 
                login_response = self.request_sender.check_user(first_user_email)
                # print(login_response)
                if login_response['status'] == 200:
                    invalid_Notif = QMessageBox()
                    invalid_Notif.setText("Email already in use. Please try another one")
                    invalid_Notif.setIcon(QMessageBox.Critical)
                    invalid_Notif.exec_()
                    return False
            except Exception as e: 
                print(e)
                return False
            # TODO: call function to check if emai exists 
            # print("Match!")
        return True
            
# {
# email : "bob@netgear.com",
# password : "blahblahblah"
# }

    #TODO: REMEMBER THAT RIGHT AND LEFT ARE MIRRORED
    # First password screen 
    def setPassword1(self):
        passwordWidget_1 = QWidget()
        # passwordPage = QVBoxLayout() # Create vertical box layout
        passwordPage = QFormLayout()
        
        imageLayout = QHBoxLayout()
        
        images = ["images/infinity.jpg", "images/peace.jpg", "images/six.jpg", "images/spider.jpg"]
        for path in images:
            pixmap = QPixmap(path)

            # Manually rotate the pixmap by 90 degrees clockwise
            # transform = QTransform().rotate(90)
            rotated_pixmap = pixmap.transformed(QTransform().rotate(90))

            # Scale the pixmap and display it in a QLabel
            rotated_pixmap = rotated_pixmap.scaled(80, 80)
            imageLabel = QLabel()
            imageLabel.setPixmap(rotated_pixmap)
            imageLayout.addWidget(imageLabel)
            
        passwordPage.addRow(imageLayout)
        passwordWidget_1.setLayout(passwordPage)
        
        infoLabel_1 = QLabel("Select 4 possible symbols to work with")
        passwordPage.addRow(infoLabel_1)
        passwordPage.addRow(QLabel()) # for spacing
        
        
        # FIRST VALUE
        symbol_label_0 = QLabel("Symbol for Value of 0:")
        # passwordPage.addWidget(symbol_label_1)
        passwordPage.addRow(symbol_label_0)
        
        self.hand_0 = QComboBox()
        self.hand_0.addItem("Right")
        self.hand_0.addItem("Left")
        # passwordPage.addWidget(hand_1)
        passwordPage.addRow(self.hand_0)
        
        self.symbol_0 = QComboBox()
        self.symbol_0.addItem("peace")
        self.symbol_0.addItem("infinity")
        self.symbol_0.addItem("six")
        self.symbol_0.addItem("spider")
        passwordPage.addRow(self.symbol_0)
        passwordPage.addRow(QLabel()) # for spacing
        
        
        #SECOND VALUE
        symbol_label_1 = QLabel("Symbol for Value of 1:")
        # passwordPage.addWidget(symbol_label_1)
        passwordPage.addRow(symbol_label_1)
        
        self.hand_1 = QComboBox()
        self.hand_1.addItem("Right")
        self.hand_1.addItem("Left")
        # passwordPage.addWidget(hand_1)
        passwordPage.addRow(self.hand_1)
        
        self.symbol_1 = QComboBox()
        self.symbol_1.addItem("peace")
        self.symbol_1.addItem("infinity")
        self.symbol_1.addItem("six")
        self.symbol_1.addItem("spider")
        passwordPage.addRow(self.symbol_1)
        passwordPage.addRow(QLabel()) # for spacing
        
        #THIRD VALUE
        symbol_label_2 = QLabel("Symbol for Value of 2:")
        # passwordPage.addWidget(symbol_label_1)
        passwordPage.addRow(symbol_label_2)
        
        self.hand_2 = QComboBox()
        self.hand_2.addItem("Right")
        self.hand_2.addItem("Left")
        # passwordPage.addWidget(hand_1)
        passwordPage.addRow(self.hand_2)
        
        self.symbol_2 = QComboBox()
        self.symbol_2.addItem("peace")
        self.symbol_2.addItem("infinity")
        self.symbol_2.addItem("six")
        self.symbol_2.addItem("spider")
        passwordPage.addRow(self.symbol_2)
        passwordPage.addRow(QLabel()) # for spacing
        
        #FOURTH VALUE
        symbol_label_3 = QLabel("Symbol for Value of 3:")
        # passwordPage.addWidget(symbol_label_1)
        passwordPage.addRow(symbol_label_3)
        
        self.hand_3 = QComboBox()
        self.hand_3.addItem("Right")
        self.hand_3.addItem("Left")
        # passwordPage.addWidget(hand_1)
        passwordPage.addRow(self.hand_3)
        
        self.symbol_3 = QComboBox()
        self.symbol_3.addItem("peace")
        self.symbol_3.addItem("infinity")
        self.symbol_3.addItem("six")
        self.symbol_3.addItem("spider")
        passwordPage.addRow(self.symbol_3)
        passwordPage.addRow(QLabel()) # for spacing
        
        
        submitButton = QPushButton("Submit")
        passwordPage.addWidget(submitButton)
        submitButton.clicked.connect(self.submitGestures)
        
        
        passwordWidget_1.setLayout(passwordPage) 
        
        self.stackedWidget.addWidget(passwordWidget_1)
        
        self.stackedWidget.setCurrentWidget(passwordWidget_1)
        
    def submitGestures(self):
        slot0 = self.symbol_0.currentText()
        slot1 = self.symbol_1.currentText()
        slot2 = self.symbol_2.currentText()
        slot3 = self.symbol_3.currentText()
        
        invalid_Notif = QMessageBox()
        invalid_Notif.setText("Overlap Binding detected. Please ensure that no slots use the same sign")
        invalid_Notif.setIcon(QMessageBox.Critical)

        
        if slot0 == slot1 or slot0 == slot2 or slot0 == slot3:
            print("error") #TODO: HAVE POP UP SAY THAT CAN'T BE THE SAME
            invalid_Notif.exec_()
        elif slot1 == slot2 or slot1 == slot3:
            print("error") #TODO: HAVE POP UP SAY THAT CAN'T BE THE SAME
            invalid_Notif.exec_()
        elif slot2 == slot3:
            print("error")
            invalid_Notif.exec_()
        else:
            self.saveMapping()
            
    def saveMapping(self):
        hand_0 = self.hand_0.currentText()
        hand_1 = self.hand_1.currentText()
        hand_2 = self.hand_2.currentText()
        hand_3 = self.hand_3.currentText()
        
        handList = [hand_0, hand_1, hand_2, hand_3]
        
        #Swap mapping of hands 
        for i in range(len(handList)):
            if handList[i] == "Right":
                handList[i] = "Left"
            else:
                handList[i] = "Right"
                
        hand_0, hand_1, hand_2, hand_3 = handList
        
        sym0 = self.symbol_0.currentText()
        sym1 = self.symbol_1.currentText()
        sym2 = self.symbol_2.currentText()
        sym3 = self.symbol_3.currentText()
        
        slot0 = hand_0 + "_" + sym0
        slot1 = hand_1 + "_" + sym1
        slot2 = hand_2 + "_" + sym2
        slot3 = hand_3 + "_" + sym3
        
        print(slot0, slot1, slot2, slot3)
        
        bindings = {
            slot0: 0,
            slot1: 1,
            slot2: 2,
            slot3: 3,
            "invalid": 5
        }
        
        curr_dir = os.getcwd()
        path_to_gestures = os.path.join(curr_dir,"backend","gesture.txt")
        
        try:
            with open(path_to_gestures, "w") as file:
                json.dump(bindings, file, indent=4)
        except Exception as e:
                print(e)
        
        
        


app = QApplication(sys.argv) 
window = MainWindow()
window.show()
sys.exit(app.exec_())