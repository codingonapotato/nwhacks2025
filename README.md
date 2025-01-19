# nwhacks2025
Best project ever

# Steps to set-up virtual environment environment
1. **In the root directory**, run `source venv/bin/activate` to run the virtual environment
2. Run `pip install -r requirements.txt` to install any packages that have been added

# Steps when introducing new package dependency
1. **In the root directory**, run `pip freeze >> requirements.txt`... Note that this will overwrite the contents of `requirements.txt` for all project members

# Steps to deactivate virtual environment
1. Run `deactivate`