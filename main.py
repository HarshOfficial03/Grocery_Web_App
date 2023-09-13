from Webapp import create_app
from flask_restful import Api

app=create_app()
# create_database(app)

if __name__ == '__main__':
    app.run(debug=True)
