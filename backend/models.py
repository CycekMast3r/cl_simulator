from  config import db

class Team(db.Model):
    name = db.Column(db.String(30), unique=True, nullable=False, primary_key=True)
    played = db.Column(db.Integer, unique=False, default=0)
    wins = db.Column(db.Integer, unique=False, default=0)
    draws = db.Column(db.Integer, unique=False, default=0)
    losses = db.Column(db.Integer, unique=False, default=0)
    points = db.Column(db.Integer, unique=False, default=0)
    pot = db.Column(db.Integer, unique=False, nullable=False)
    #rivals_pot1 = db.Column(db.Integer, unique=False, default=0)
    #rivals_pot2 = db.Column(db.Integer, unique=False, default=0)
    #rivals_pot3 = db.Column(db.Integer, unique=False, default=0)
    #rivals_pot4 = db.Column(db.Integer, unique=False, default=0)

    def to_json(self):
        return {
            "name": self.name,
            "played": self.played,
            "wins": self.wins,
            "draws": self.draws,
            "losses": self.losses,
            "points": self.points,
            "pot": self.pot,
            #"rivals_pot1": self.rivals_pot1,
            #"rivals_pot2": self.rivals_pot2,
            #"rivals_pot3": self.rivals_pot3,
            #"rivals_pot4": self.rivals_pot4,
        }

class Match(db.Model):
    match_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    round_number = db.Column(db.Integer, nullable=False)
    team1 = db.Column(db.String(30), db.ForeignKey('team.name'), nullable=False)
    team2 = db.Column(db.String(30), db.ForeignKey('team.name'), nullable=False)
    score_team1 = db.Column(db.Integer, unique=False, nullable=False, default=0)
    score_team2 = db.Column(db.Integer, unique=False, nullable=False, default=0)

    def rounds_to_json(self):
        return {
            "matchId": self.match_id,
            "roundNumber": self.round_number,
            "team1": self.team1,
            "team2": self.team2,
            "scoreTeam1": self.score_team1,
            "scoreTeam2": self.score_team2
        }
    
    
