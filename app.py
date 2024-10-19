import os
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Bird

app = Flask(__name__)

# Set the database URI from the environment variable, with a fallback if not set
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URI',
    'postgresql://my_database_7msc_user:Wnx12PRc2u6Mjck3RtkPUv7yp4mja59z@dpg-cs8bcjdsvqrc73bnk560-a.oregon-postgres.render.com/bird_app_db'
)

# Turn off track modifications (saves memory)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Optional: To make the JSON responses more readable (set to False for pretty-printing)
app.json.compact = False

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Initialize the SQLAlchemy database instance with the app
db.init_app(app)

# Initialize Flask-RESTful API
api = Api(app)

# Resource for handling birds
class Birds(Resource):
    def get(self):
        # Query all birds from the database and convert them to a list of dictionaries
        birds = [bird.to_dict() for bird in Bird.query.all()]
        return make_response(jsonify(birds), 200)

# Add the Birds resource to the API with the '/birds' route
api.add_resource(Birds, '/birds')

class BirdByID(Resource):
    def get(self, id):
        bird = Bird.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(bird), 200)

api.add_resource(BirdByID, '/birds/<int:id>')

# Main block to run the app
if __name__ == '__main__':
    app.run(debug=True)
