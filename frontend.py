from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("<INSERT NAME HERE>") # TODO: COME UP WITH A CREATIVE NAME 
        
        self.resize(1000,600)
        
        self.setMainMenu()
        
        

    def loginMain(self):
        self.result_label.setText(f"Hello, {username}!")
    
    
    # Function to set the Main Menu (initial screen)    
    def setMainMenu(self):
        self.mainLayout = QVBoxLayout() # Create vertical box layout
        # Log In Flow 
        self.loginLabel = QLabel("Returning users can log in below:")
        self.mainLayout.addWidget(self.loginLabel)
        self.loginFlowButton = QPushButton("Log In")
        # self.submit_button.clicked.connect(self.submit)
        self.mainLayout.addWidget(self.loginFlowButton)
        
        # Register Flow Label
        self.registerLabel = QLabel("New User? Create an account:")
        self.mainLayout.addWidget(self.registerLabel)
        self.registerFlowButton = QPushButton("Register")
        self.mainLayout.addWidget(self.registerFlowButton)

        self.setLayout(self.mainLayout) # important 
    
    
    # Function to set the Login page to enter username     
    def setLoginPageUsername(self):
        self.mainLayout = QVBoxLayout() # Create vertical box layout
        # Log In Flow 
        self.loginLabel = QLabel("Returning users can log in below:")
        self.mainLayout.addWidget(self.loginLabel)
        self.loginFlowButton = QPushButton("Log In")
        # self.submit_button.clicked.connect(self.submit)
        self.mainLayout.addWidget(self.loginFlowButton)
        
        # Register Flow Label
        self.registerLabel = QLabel("New User? Create an account:")
        self.mainLayout.addWidget(self.registerLabel)
        self.registerFlowButton = QPushButton("Register")
        self.mainLayout.addWidget(self.registerFlowButton)

        self.setLayout(self.mainLayout) # important 



app = QApplication(sys.argv) # sys.argv makes it so that it can accept command line arguments but is optional
window = MainWindow()
window.show()
sys.exit(app.exec_())