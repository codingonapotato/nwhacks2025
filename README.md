# nwhacks2025
Best project ever

# Steps to set-up virtual environment environment
1. **In the root directory**, run `source venv/bin/activate` to run the virtual environment
2. Run `pip install -r requirements.txt` to install any packages that have been added

# Steps when introducing new package dependency
1. **In the root directory**, run `pip freeze >> requirements.txt`... Note that this will overwrite the contents of `requirements.txt` for all project members

# Steps to deactivate virtual environment
1. Run `deactivate`

# Steps to setup SSL Certificates
1. On MacOs run: `open "/Applications/Python <YOUR PYTHON VERSION>/Install Certificates.command"`<br>
2. On Windows run:<br>
       - `pip install certifi`<br>
       - `python -c "import certifi; print(certifi.where())"`<br>
       - with path in Flask file:<br>

             from pymongo import MongoClient
             client = MongoClient(
                 "mongodb+srv://&lt;your-username&gt;:&lt;your-password&gt;@gesture-pw-db.zu1ec.mongodb.net/<your-database>",
                 ssl=True,
                 tlsCAFile="C:<path to your certifi>\\certifi\\cacert.pem"
             )<br>

# Flask Server IP
http://52.91.85.117:5000 (changes each time instance run)

# Run locally vs over EC2
1. under ../GitHub/nwhacks2025/server/flaskr/__init__.py <br>
   uncomment the following for running server on EC2 instance <br>
   
    **this is on EC2** <br>
    client = MongoClient( <br>
        os.environ[MONGO_URI], <br>
        ssl=True, <br>
        tlsCAFile="C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\certifi\\cacert.pem" <br>
    ) <br>

    **this locally** <br>
    client = MongoClient( <br>
    os.environ[MONGO_URI] <br>
    ) <br>

2. ../GitHub/nwhacks2025/frontend.py <br>

   **uncomment the following for running locally** <br>
   self.request_sender = requestSender.RequestSender("http://127.0.0.1:5000") <br>

   **this for ec2** <br>
   self.request_sender = requestSender.RequestSender("http://52.91.85.117:5000")    # connect to EC2 instance <br>

# Default network settings
1. On EC2 Under Security add Inbound rule to allow **port 5000** on your EC2 instance from **any IP address (0.0.0.0/0)**, using the **TCP** protocol<br>
2. On EC2 Windows modify firewall configuration<br>
          Open Windows Firewall -> find Windows Defender Firewall<br>
          Create new Inbound Rule:<br>
                 Rule Type: Select Port and click Next<br>
                 Protocol and Ports: Select TCP<br>
                 local ports field: enter port 5000<br>
                 Click Next -> Allow Domain, Private and Public<br>
                 Save the rule<br>
          
4. Under MongoDB, Security -> Network Access -> add Access List Entry :**0.0.0.0/0**
