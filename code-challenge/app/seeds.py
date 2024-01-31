import random
from app import app
from models import db
from models import Hero
from models import Power
from models import HeroPower


hero_list = [
  {"name" : "Kamala Khan", "super_name" : "Ms. Marvel" },
  {"name" : "Doreen Green", "super_name" : "Squirrel Girl" },
  {"name" : "Gwen Stacy", "super_name" : "Spider-Gwen" },
  {"name" : "Janet Van Dyne", "super_name" : "The Wasp" },
  {"name" : "Wanda Maximoff", "super_name" : "Scarlet Witch" },
  {"name" : "Carol Danvers", "super_name" : "Captain Marvel" },
  {"name" : "Jean Grey", "super_name" : "Dark Phoenix" },
  {"name" : "Ororo Munroe", "super_name" : "Storm" },
  {"name" : "Kitty Pryde", "super_name" : "Shadowcat" },
  {"name" : "Elektra Natchios", "super_name" : "Elektra" }
]

hero_powers = [
  {"name" : "super strength", "description" : "gives the wielder super-human strengths" },
  {"name" : "flight", "description" : "gives the wielder the ability to fly through the skies at supersonic speed" },
  {"name" : "super human senses", "description" : "allows the wielder to use her senses at a super-human level" },
  {"name" : "elasticity", "description" : "can stretch the human body to extreme lengths" }
]

strengths = [
    'Strong',
    'Weak', 
    'Average'
]


if __name__ == '__main__':
    with app.app_context():

        Hero.query.delete()
        Power.query.delete()
        HeroPower.query.delete()

        print("🦸‍♀️ Seeding heroes...")
        all_heroes = []
        for hero_data in hero_list:
            hero = Hero(
                name=hero_data["name"], 
                super_name=hero_data["super_name"]
            )

            all_heroes.append(hero)
            db.session.add(hero)

        print("🦸‍♀️ Seeding powers...")
        powers = []
        for power_data in hero_powers:
            power = Power(
                name=power_data["name"], 
                description=power_data["description"]
                )
            
            powers.append(power)
            db.session.add(power)

        db.session.commit()

        print("🦸‍♀️ Adding powers to heroes...")
        all_hero_powers = []
        for hero in all_heroes:
            for i in range(random.randint(1, 2)):
                 hero_power = HeroPower(
                    strength=random.choice(strengths),
                    hero_id=hero.id,
                    power_id=random.choice(powers).id
                )

                 all_hero_powers.append(hero_power)
                 db.session.add(hero_power)

        db.session.add_all(all_hero_powers)

        db.session.commit()

        print("Db seeded successfully.")