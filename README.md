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

