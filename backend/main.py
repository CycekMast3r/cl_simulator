from flask import request, jsonify
from config import app, db
from models import Team, Match
import random
from  collections import defaultdict

teams_dictionary = {
    'AC Milan': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 2},
    'Arsenal': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 2},
    'Aston Villa': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 3},
    'Atalanta': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 2},
    'Atlético Madrid': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 2},
    'FC Barcelona': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 1},
    'Bayer Leverkusen': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 2},
    'Bayern Munich': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 1},
    'Benfica': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 2},
    'Bologna': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 4},
    'Borussia Dortmund': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 1},
    'Brest': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 4},
    'Celtic': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 3},
    'Club Brugge': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 2},
    'Feyenord': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 3},
    'Girona FC': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 4},
    'Inter': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 1},
    'Juventus': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 2},
    'Liverpool': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 1},
    'Manchester City': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 1},
    'AS Monaco': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 3},
    'PSG': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 1},
    'PSV': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 3},
    'RB Leipzig': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 1},
    'Real Madrid': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 1},
    'Shakhtar Donetsk': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 2},
    'Sporting CP': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 3},
    'Sturm Graz': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 4},
    'VFB Stuttgart': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 4},
    'Slovan Bratislava': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 4},
    'Dinamo Zagreb': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 3},
    'Jagiellonia': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 4},
    'Malmo': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 4},
    'Slavia Praga': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 3},
    'Rangers': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 3},
    'Sparta Barłogi': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'points': 0, 'pot': 4},
}

def get_team_rivals(team_name):
    matches_as_team1 = Match.query.filter_by(team1=team_name).all()
    matches_as_team2 = Match.query.filter_by(team2=team_name).all()
    
    rivals = set()
    
    for match in matches_as_team1:
        rivals.add(match.team2)

    for match in matches_as_team2:
        rivals.add(match.team1)
    
    return rivals

def update_pots(pot, team):
    match pot:
        case 1:
            team.rivals_pot1 += 1
        case 2: 
            team.rivals_pot2 += 1
        case 3:
            team.rivals_pot3 +=1
        case 4: 
            team.rivals_pot4 += 1
        case _:
            return jsonify({"message", "No such pot"}), 404
        
    try:
        db.session.commit()  
    except Exception as e:
        db.session.rollback()
        print(f"Error updating team rivals: {e}")
        return jsonify({"message": "Error updating team rivals"}), 500


def add_teams_to_database():
    if Team.query.count() == 0:
        for team_name, stats in teams_dictionary.items():
            adding_team = Team(
                name=team_name,
                played=stats['played'],
                wins=stats['wins'],
                draws=stats['draws'],
                losses=stats['losses'],
                points=stats['points'],
                pot=stats['pot']
            )
            db.session.add(adding_team)
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding teams: {e}")

@app.before_request
def initialize():
    db.create_all()
    add_teams_to_database()

@app.route("/teams", methods=["GET"])
def get_teams():
    add_teams_to_database()

    teams = Team.query.all()
    json_teams = [team.to_json() for team in teams]

    return jsonify({"teams": json_teams})

#generate pairings
@app.route("/generate_pairings", methods=["POST"])
def generate_pairings():
    get_teams()
    teams = Team.query.all()
    pots = defaultdict(list)
    round_counter = 1 

    for team in teams:
        pots[team.pot].append(team)
        team_rivals = []

        while round_counter <= 8:
            
            drawing_pot = random.choice(list(pots.keys()))
            print(drawing_pot)
            team_rivals = get_team_rivals(team)
            team_reference =  Team.query.filter_by(name=team).first()
            team_pot = team_reference.pot
            possible_rivals = [t for t in pots[drawing_pot] if t.name != team.name]
            rival_name = random.choice(possible_rivals)

            if not possible_rivals:
                raise Exception("There are no rivals avalibe")
            
            while rival_name in team_rivals:
                rival_name = random.choice(possible_rivals)
            
            rival_reference = Team.query.filter_by(name=rival_name).first()
            rival_pot = rival_reference.pot
            #match rival_pots 1,2,3,4 
            '''
            if (rival_pot == 1 and (rival_reference.rivals_pot1 == 2 or team_reference.rivals_pot1 == 2)) or \
               (rival_pot == 2 and (rival_reference.rivals_pot2 == 2 or team_reference.rivals_pot2 == 2)) or \
               (rival_pot == 3 and (rival_reference.rivals_pot3 == 2 or team_reference.rivals_pot3 == 2)) or \
               (rival_pot == 4 and (rival_reference.rivals_pot4 == 2 or team_reference.rivals_pot4 == 2)):

                available_pots = [pot for pot in pots.keys() if len([r for r in team_rivals if r.pot == pot]) < 2]
                possible_rivals = [t for t in pots[available_pots] if t.name != team.name]
                
                if not possible_rivals:
                    raise Exception("There are no rivals available after filtering")

                rival_name = random.choice(possible_rivals)
                rival_reference = Team.query.filter_by(name=rival_name.name).first()
                rival_pot = rival_reference.pot 
                '''
            update_pots(team_pot, rival_name)
            update_pots(rival_pot, team)

            round_counter += 1 
            

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        generate_pairings()
        
    app.run(debug=True)

#results
#submit results
#rounds
#show rounds 
#update table 
#comparing old scores 