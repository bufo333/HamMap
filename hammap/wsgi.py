import os 
from project.server import create_app, db
app = create_app(os.getenv('FLASK_CONFIG'))

if __name__ == "__main__":
        app.run()

