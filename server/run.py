from flaskr import create_app
from flaskr.db import mongoClient

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) # TODO: Remove debug flag for prod
    mongoClient[0].close()