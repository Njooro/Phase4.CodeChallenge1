#!/usr/bin/env python3

from flask import Flask, make_response, render_template
from flask_migrate import Migrate
from flask_restx import Api, Namespace, Resource, fields
from flask_marshmallow import Marshmallow

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.dbf'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)
ma = Marshmallow(app)

api.init_app(app)

ns = Namespace("/")
api.add_namespace(ns)

@app.route('/')
def home():
    return ''

class HeroesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Hero
        ordered=True

    id = ma.auto_field()
    name = ma.auto_field()
    super_name = ma.auto_field()

heroes_schema = HeroesSchema(many=True)

class PowersSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Power
        ordered=True

    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()

power_schema = PowersSchema()
powers_schema = PowersSchema(many=True)


# RESTx Models
power_model = api.model(
    "Power Input", {
        "description": fields.String,
    }
)

hero_powers_model = api.model(
    "Hero Powers Input", {
        "strength" : fields.String,
        "power_id" : fields.Integer,
        "hero_id" : fields.Integer,
    }
)

@app.route('/')
@app.route('/<int:id>')
def index(id=0):
    return render_template("index.html")


@ns.route('/heroes')
class Heroes(Resource):

    def get(self):
        heroes = Hero.query.all()

        if not heroes:
            return {
                "error": "No heroes not found"
            }, 404
        else:
            return heroes_schema.dump(heroes), 200
        
@ns.route('/heroes/<int:id>')
class HeroesByID(Resource):

    def get(self, id):
        hero = Hero.query.get(id)

        if not hero:
            return {
                "error": "Hero not found"
            }, 404
        else:
            powers = Power.query.join(HeroPower).filter(HeroPower.hero_id == id).all()

            res_body = {
                "id" : hero.id,
                "name" : hero.name,
                "super_name" : hero.super_name,
                "powers" : []
            }

            for power in powers:
                power_details = {
                    "id": power.id,
                    "name": power.name,
                    "description": power.description
                }
                res_body["powers"].append(power_details)

            return res_body, 200


@ns.route('/powers')
class Powers(Resource):

    def get(self):
        all_powers = Power.query.all()

        if not all_powers:
            return {
                "error": "No powers not found"
            }, 404
        else:
            return powers_schema.dump(all_powers), 200

@ns.route('/powers/<int:id>')
class PowersByID(Resource):

    def get(self, id):
        powr = Power.query.get(id)

        if not powr:
            return {
                "error": "Power not found"
            }, 404
        else:
            return power_schema.dump(powr), 200

    @ns.expect(power_model)
    def patch(self, id):
        powr = Power.query.get(id)

        if powr:
            powr.description = ns.payload['description']
        
            db.session.commit()
            
            return power_schema.dump(powr), 200
        
        else:
            return {
                "error": "Power not found"
            }, 404

@ns.route('/hero_powers')
class HeroPowersByID(Resource):

    @ns.expect(hero_powers_model)
    def post(self):

        new_hero_power = HeroPower(
            strength = ns.payload['strength'],
            power_id = ns.payload['power_id'],
            hero_id = ns.payload['hero_id']
        )

        hero = Hero.query.filter(Hero.id == int(ns.payload["hero_id"])).first()
        power = Power.query.filter(Power.id == int(ns.payload["power_id"])).first()

        if not hero and not power:
            return { 
                "error": "Hero and power not found."
                }, 404
            
        elif not hero:
            return {
                "error": "Hero not found."
                }, 404
        
        elif not power:
            return {
                "error": "Power not found."
                }, 404
        else:
            db.session.add(new_hero_power)
            db.session.commit()        

            powers = Power.query.join(HeroPower).filter(HeroPower.hero_id == int(ns.payload["hero_id"])).all()

            res_body = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": []
            }

            for power in powers:
                power_details = {
                    "id": power.id,
                    "name": power.name,
                    "description": power.description
                }
                res_body["powers"].append(power_details)

            return res_body, 201
if __name__ == '__main__':
    app.run(port=5555)
