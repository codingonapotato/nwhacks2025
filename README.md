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
1. On MacOs run: open "/Applications/Python <YOUR PYTHON VERSION>/Install Certificates.command"
2. On Windows run:
       pip install certifi
       python -c "import certifi; print(certifi.where())"
   with path in Flask file:
      from pymongo import MongoClient
      client = MongoClient(
          "mongodb+srv://<your-username>:<your-password>@gesture-pw-db.zu1ec.mongodb.net/<your-database>",
          ssl=True,
          tlsCAFile="C:<path to your certifi>\\certifi\\cacert.pem"
      )

# Flask Server IP
http://52.91.85.117:5000

# Default network settings
1. On EC2 Under Security add Inbound rule to allow **port 5000** on your EC2 instance from **any IP address (0.0.0.0/0)**, using the **TCP** protocol
2. On EC2 Windows modify firewall configuration
          Open Windows Firewall -> find Windows Defender Firewall
          Create new Inbound Rule:
                 Rule Type: Select Port and click Next
                 Protocol and Ports: Select TCP
                 local ports field: enter port 5000
                 Click Next -> Allow Domain, Private and Public
                 Save the rule
          
4. Under MongoDB, Security -> Network Access -> add Access List Entry :**0.0.0.0/0**
