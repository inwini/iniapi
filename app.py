
from project import create_app, db

app = create_app()

db = db

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
