#!/usr/bin/python
from flask import Flask, jsonify
from flask_restx import Api, Resource, fields
from model_deployment import clf_gender_movie

app = Flask(__name__)

api = Api(
    app, 
    version='1.0', 
    title='API de Modelo de Clasificacion de Genero de Peliculas',
    description='Modelo de clasificacion de generos de peliculas realizado por G26 para MIAD')

ns = api.namespace('classifier', 
     description='Gender Movie Classifier API')
   
parser = api.parser()

# Parametros de la API
parser.add_argument(
    'year', 
    type=int, 
    required=True, 
    help='year of the movie', 
    location='args')

parser.add_argument(
    'title', 
    type=str, 
    required=True, 
    help='title of the movie', 
    location='args')

parser.add_argument(
    'plot', 
    type=str, 
    required=True, 
    help='plot of the movie', 
    location='args')

resource_fields = api.model('Resource', {
  "p_Action": fields.Float,
  "p_Adventure": fields.Float,
  "p_Animation": fields.Float,
  "p_Biography": fields.Float,
  "p_Comedy": fields.Float,
  "p_Crime": fields.Float,
  "p_Documentary": fields.Float,
  "p_Drama": fields.Float,
  "p_Family": fields.Float,
  "p_Fantasy": fields.Float,
  "p_Film-Noir": fields.Float,
  "p_History": fields.Float,
  "p_Horror": fields.Float,
  "p_Music": fields.Float,
  "p_Musical": fields.Float,
  "p_Mystery": fields.Float,
  "p_News": fields.Float,
  "p_Romance": fields.Float,
  "p_Sci-Fi": fields.Float,
  "p_Short": fields.Float,
  "p_Sport": fields.Float,
  "p_Thriller": fields.Float,
  "p_War": fields.Float,
  "p_Western": fields.Float
})

@app.errorhandler(500)
def internal_server_error(error):
    response = {
        'message': 'Internal Server Error',
        'error_code': 500
    }
    return jsonify(response), 500

@ns.route('/')
class PredictApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        result = clf_gender_movie(args['year'], args['title'], args['plot']) 
        return result, 200
        
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8888)
