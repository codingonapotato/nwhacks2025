from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QStackedWidget
import sys

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
        
        

    def loginMain(self):
        self.result_label.setText(f"Hello, {username}!")
    
    
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
        usernameField = QLineEdit()
        login1.addWidget(usernameField)
        loginFlowButton = QPushButton("Next")
        login1.addWidget(loginFlowButton)
        # self.submit_button.clicked.connect(self.submit)

        loginWidget_1.setLayout(login1) 
        
        self.stackedWidget.addWidget(loginWidget_1)
        
        self.stackedWidget.setCurrentWidget(loginWidget_1)
        
    def 



app = QApplication(sys.argv) # sys.argv makes it so that it can accept command line arguments but is optional
window = MainWindow()
window.show()
sys.exit(app.exec_())