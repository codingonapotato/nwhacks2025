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
        try:
            public_key = self.request_sender.getKey()
            if public_key["status"] != 200:
                raise Exception(f"server returned status code {public_key['status']} when trying to get public key")
            with open("public_key.pem", "w") as f:
                    f.write(public_key)
        except Exception as e:
            print(e) # :( aur naur
            self.close()

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
                with open('public_key.pem', "rb") as f:    # read in binary 
                    public_key = f.read()
                    public_key = serialization.load_pem_public_key(public_key)
                encrypted_password = public_key.encrypt(
                    valid_password.encode(),  # Convert password to bytes
                    padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                    ))
                encrypted_password_base64 = base64.b64encode(encrypted_password).decode('utf-8')

                register_response = self.request_sender.registration(self.user_email_field.text(), encrypted_password_base64 = base64.b64encode(encrypted_password).decode('utf-8'))
                # public_key = register_response['message']['public_key']
                # print(public_key)
                # with open("public_key.pem", "w") as f:
                #     f.write(public_key)
                # print("Public key saved locally")
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

    # First password screen 
    def setPassword1(self):
        passwordWidget_1 = QWidget()
        # passwordPage = QVBoxLayout() # Create vertical box layout
        passwordPage = QFormLayout()
        
        
        infoLabel_1 = QLabel("Select 4 possible symbols to work with")
        passwordPage.addRow(infoLabel_1)
        passwordPage.addRow(QLabel()) # for spacing
        
        
        # FIRST VALUE
        symbol_label_0 = QLabel("Symbol for Value of 0:")
        # passwordPage.addWidget(symbol_label_1)
        passwordPage.addRow(symbol_label_0)
        
        hand_0 = QComboBox()
        hand_0.addItem("Right Hand")
        hand_0.addItem("Left Hand")
        # passwordPage.addWidget(hand_1)
        passwordPage.addRow(hand_0)
        
        symbol_1 = QComboBox()
        symbol_1.addItem("Peace")
        symbol_1.addItem("Infinity")
        symbol_1.addItem("Six")
        symbol_1.addItem("Spider")
        passwordPage.addRow(symbol_1)
        passwordPage.addRow(QLabel()) # for spacing
        
        
        #SECOND VALUE
        symbol_label_1 = QLabel("Symbol for Value of 1:")
        # passwordPage.addWidget(symbol_label_1)
        passwordPage.addRow(symbol_label_1)
        
        hand_1 = QComboBox()
        hand_1.addItem("Right Hand")
        hand_1.addItem("Left Hand")
        # passwordPage.addWidget(hand_1)
        passwordPage.addRow(hand_1)
        
        symbol_1 = QComboBox()
        symbol_1.addItem("Peace")
        symbol_1.addItem("Infinity")
        symbol_1.addItem("Six")
        symbol_1.addItem("Spider")
        passwordPage.addRow(symbol_1)
        passwordPage.addRow(QLabel()) # for spacing
        
        #THIRD VALUE
        symbol_label_2 = QLabel("Symbol for Value of 2:")
        # passwordPage.addWidget(symbol_label_1)
        passwordPage.addRow(symbol_label_2)
        
        hand_2 = QComboBox()
        hand_2.addItem("Right Hand")
        hand_2.addItem("Left Hand")
        # passwordPage.addWidget(hand_1)
        passwordPage.addRow(hand_2)
        
        symbol_2 = QComboBox()
        symbol_2.addItem("Peace")
        symbol_2.addItem("Infinity")
        symbol_2.addItem("Six")
        symbol_2.addItem("Spider")
        passwordPage.addRow(symbol_2)
        passwordPage.addRow(QLabel()) # for spacing
        
        #FOURTH VALUE
        symbol_label_3 = QLabel("Symbol for Value of 3:")
        # passwordPage.addWidget(symbol_label_1)
        passwordPage.addRow(symbol_label_3)
        
        hand_3 = QComboBox()
        hand_3.addItem("Right Hand")
        hand_3.addItem("Left Hand")
        # passwordPage.addWidget(hand_1)
        passwordPage.addRow(hand_3)
        
        symbol_3 = QComboBox()
        symbol_3.addItem("Peace")
        symbol_3.addItem("Infinity")
        symbol_3.addItem("Six")
        symbol_3.addItem("Spider")
        passwordPage.addRow(symbol_3)
        passwordPage.addRow(QLabel()) # for spacing
        
        
        passwordWidget_1.setLayout(passwordPage) 
        
        self.stackedWidget.addWidget(passwordWidget_1)
        
        self.stackedWidget.setCurrentWidget(passwordWidget_1)
        
app = QApplication(sys.argv) 
window = MainWindow()
window.show()
sys.exit(app.exec_())