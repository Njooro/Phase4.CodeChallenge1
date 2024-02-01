from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

app.json.compact = True

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the superheroes API"})

@app.route('/heroes', methods=['GET'])
def heroes():
    heroes = []
    for hero in Hero.query.all():
        hero_dict = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'created_at': hero.created_at,
            'updated_at': hero.updated_at,
            'powers': [
                {'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description, 'strength': hp.strength} for hp in hero.hero_powers]
        }
        heroes.append(hero_dict)

    response = make_response(
        jsonify(heroes),
        200,
    )
    
    return response

@app.route('/heroes/<int:id>')
def hero_by_id(id):
    hero = Hero.query.filter(Hero.id == id).first()
    if hero:
        hero_dict = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'created_at': hero.created_at,
            'updated_at': hero.updated_at,
            'powers': [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description, 'strength': hp.strength} for hp in hero.hero_powers]
        }
        
        response = make_response(
            jsonify(hero_dict),
            200,
            )
        return response
        
    else:
        response = make_response(
            jsonify({'error': 'Hero not found'}),
            404,
        )

        return response

@app.route('/powers')
def powers():
    powers = []
    for power in Power.query.all():
        power_dict = {
            'id': power.id,
            'name': power.name,
            'description': power.description,
            'created_at': power.created_at,
            'updated_at': power.updated_at,
        }
        powers.append(power_dict)

    response = make_response(
        jsonify(powers),
        200,
    )

    return response

@app.route('/powers/<int:id>', methods=['GET', 'PATCH'])
def power_by_id(id):

    if request.method == 'GET':
        power = Power.query.get(id)
        if power:
            power_dict = {
                'id': power.id,
                'name': power.name,
                'description': power.description,
                'created_at': power.created_at,
                'updated_at': power.updated_at,
            }
            response = make_response(
                jsonify(power_dict),
                200
            )
            return response 
        
        else:
            return jsonify({'error': 'Power not found'}), 404
        
    elif request.method == 'PATCH':
        power = Power.query.get(id)
        if not power:
            return jsonify({'error': 'Power not found'}), 404

        if request.form:
            for attr, value in request.form.items():
                setattr(power, attr, value)

        db.session.commit()
        power_dict = {
            'id': power.id,
            'name': power.name,
            'description': power.description,
            'created_at': power.created_at,
            'updated_at': power.updated_at,
        }

        response = make_response(
            jsonify(power_dict),
            200,
        )

        return response

@app.route('/hero_powers', methods=['POST'])
def add_hero_powers():
    
    power = request.get_json()

    if not power:
        return make_response(jsonify({"error": "Request body must be in JSON format"}), 400)
    
    strength =power.get('strength')
    hero_id = power.get('hero_id')
    power_id = power.get('power_id')

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)
    if not (hero and power):
        return jsonify({"error": "Missing hero or power"}), 400

    
    new_power = HeroPower(
        strength=strength,
        hero_id=hero_id,
        power_id=power_id,
    ) 

    db.session.add(new_power)
    db.session.commit()

    hero_dict = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'created_at': hero.created_at,
            'updated_at': hero.updated_at,
            'powers': [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description, 'strength': hp.strength} for hp in hero.hero_powers]
        }

    response = make_response(
        jsonify(hero_dict),
        201,
    )

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)