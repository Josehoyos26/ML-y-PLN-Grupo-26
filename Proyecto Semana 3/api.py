#!/usr/bin/python
from flask import Flask
from flask_restx import Api, Resource, fields
import joblib
from model_deployment import predict_price

app = Flask(__name__)

api = Api(
    app, 
    version='1.0', 
    title='Predictor of Vehicle Prices API',
    description='El "Predictor of Vehicle Prices API" es un modelo disponible para predecir precios de vehiculos.')

ns = api.namespace('Forecaster', 
     description='Vehicle Price Forecaster API')
   
parser = api.parser()

# Parametros de la API
parser.add_argument(
    'Year', 
    type=int, 
    required=True, 
    help='Year of the Vehicle', 
    location='args')

parser.add_argument(
    'Mileage', 
    type=int, 
    required=True, 
    help='Mileage of the Vehicle', 
    location='args')

parser.add_argument(
    'State', 
    type=str, 
    required=True, 
    help='State of the Vehicle', 
    location='args')

parser.add_argument(
    'Make', 
    type=str, 
    required=True, 
    help='Make of the Vehicle', 
    location='args')

parser.add_argument(
    'Model', 
    type=str, 
    required=True, 
    help='Model of the Vehicle', 
    location='args')

resource_fields = api.model('Resource', {
    'result': fields.String,
})

@ns.route('/')
class PredictApi(Resource):

    @api.doc(parser=parser)
    @api.marshal_with(resource_fields)
    def get(self):
        args = parser.parse_args()
        
        return {
         "result": predict_price(args['Year'], args['Mileage'], args['State'], args['Make'], args['Model'])
        }, 200
    
    
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8888)