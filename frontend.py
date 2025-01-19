from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QMessageBox
import sys
import slapper

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("<INSERT NAME HERE>") # TODO: COME UP WITH A CREATIVE NAME 
        
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
        # userName = self.usernameField.text()
        # print(userName)
        try: 
            slapper.main()
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
        
        nextButton = QPushButton("Next")
        registerPage.addWidget(nextButton)
        nextButton.clicked.connect(self.checkValidEmail)
        
        goBackButton = QPushButton("Cancel")
        registerPage.addWidget(goBackButton)
        goBackButton.clicked.connect(self.goBackToMainMenu)
        
        
        
        # loginFlowButton = QPushButton("Next")
        # login1.addWidget(loginFlowButton)
        # loginFlowButton.clicked.connect(self.checkUserExists) # check user exists function then checks

        registerWidget.setLayout(registerPage) 
        
        self.stackedWidget.addWidget(registerWidget)
        
        self.stackedWidget.setCurrentWidget(registerWidget)
        
        
    def checkValidEmail(self):
        first_user_email = self.user_email_field.text()
        second_user_email = self.user_email_confirmation.text()
        if first_user_email == "" or second_user_email == "":
            invalid_Notif = QMessageBox()
            invalid_Notif.setText("Invalid email detected. Please try again")
            invalid_Notif.setIcon(QMessageBox.Critical)
            invalid_Notif.exec_()
        elif first_user_email != second_user_email:
            mismatch_Notif = QMessageBox()
            mismatch_Notif.setText("Emails do not match! Please try again")
            mismatch_Notif.setIcon(QMessageBox.Critical)
            mismatch_Notif.exec_()
        ## TODO: add case to check if email exists 
        else:
            print("Match!")
        
    



app = QApplication(sys.argv) # sys.argv makes it so that it can accept command line arguments but is optional
window = MainWindow()
window.show()
sys.exit(app.exec_())