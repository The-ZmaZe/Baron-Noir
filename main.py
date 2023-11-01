import numpy as np
import random
import datetime

def count_votes(ballot):
    ret = dict()
    for vote in ballot:
        if vote in ret.keys():
            ret[vote] += 1
        else:
            ret[vote] = 1
    return ret


class Political_Spectrum:
    def __init__(self, social=0.00, institutional=0.00, economical=0.00):
        self.social = social
        self.institutional = institutional
        self.economical = economical

    def ch_social(self, value):
        if ((self.social + value) >= -1) and ((self.social + value) <= 1):
            self.social += value

    def ch_institutional(self, value):
        if ((self.institutional + value) >= -1) and ((self.institutional + value) <= 1):
            self.institutional += value

    def ch_economical(self, value):
        if ((self.economical + value) >= -1) and ((self.economical + value) <= 1):
            self.economical += value

    @classmethod
    def compatibility_relative(cls, s1: cls, s2: cls):
        return (
        abs(s1.social - s2.social),
        abs(s1.institutional - s2.institutional),
        abs(s1.economical - s2.economical),
    )

    @classmethod
    def mean(cls, *args):
        social, institutional, economical = []
        for spectrum in args:
            social.append(spectrum.social)
            institutional.append(spectrum.institutional)
            economical.append(spectrum.economical)
        social, institutional, economical = *map(lambda x: sum(x)/len(x), [social, institutional, economical])
        return cls(social, institutional, economical)

class Country:
    def __init__(self, name, population):
        self.name = name
        self.population = population
        self.president = None

class Party:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.leader = None
        self.spectrum = Political_Spectrum()


class Actor:
    def __init__(self, surname, name, age=random.randint(0, 76)):
        self.surname = surname
        self.name = name
        self.age = age
        self.spectrum = Political_Spectrum()
        self.party = None

    def fullname(self):
        return f"{self.surname} {self.name}"


class Engine:
    def __init__(self):
        self.turn = datetime.date(2022, 12, 31)
        self.calendar = dict()

        self.actors = [Actor("Jean-Luc", "Mélenchon", 72), Actor("Emmanuel", "Macron", 45), Actor("Marine", "Le Pen", 55)]
        self.actors[0].spectrum = Political_Spectrum(0.4, 0.5, 0,4)
        self.actors[1].spectrum = Political_Spectrum(0.00, -0.5, -0.7)
        self.actors[3].spectrum = Political_Spectrum(-0.5, -0.4, -0.7)

        self.parties = [Party("LFI", "La France Insoumise"), Party("RE", "Renaissance"), Party("RN", "Rassemblement National")]
        self.countries = [Country("France")]

        self.parties[0].leader = self.actors[0]
        self.parties[1].leader = self.actors[1]
        self.parties[2].leader = self.actors[2]

    def update_parties_spectrum(self):
        parties_members = dict()
        for party in self.parties:
            parties_members[party] = set()

        for actors in self.actors:


        for party in self.parties:
            if parties_members[party]:
                party.spectrum = Political_Spectrum.mean(*map(lambda x: x.spectrum, self.parties_members[party]))
            else:
                party.spectrum = Political_Spectrum()

    def presidential_elections(self, candidates):
        print("Élections Présidentielles")
        electors = 
        print(electors, "électeurs")
        abstention = round(0.5 + (1/100) * np.random.standard_normal(), 3)
        print(f"{abstention * 100}% d'abstention")
        n_abstention = round(abstention * electors)
        votes = electors - n_abstention

        ballot = []
        for i in range(votes):
            ballot.append(random.choice(candidates))
        results = count_votes(ballot)
        
        winner = None
        ordered_results = list(results.items())
        ordered_results.sort(key=lambda x: x[1], reverse=1)
        for i, result in enumerate(ordered_results):
            print(f"{result[0].fullname()} - {round(result[1] * 100 / votes, 2)}%")
            if result[1] > (votes // 2):
                winner = result[0]
        
        if winner:
            print(f"{winner.fullname()} est élu")
            self.countries[0].president = winner

        else:
            self.presidential_elections([ordered_results[0][0], ordered_results[1][0]])



    def next_turn(self):
        self.turn += datetime.timedelta(days=1)

        for party in self.parties:
            if party.leader.party != party:
                party.leader.party = party


if __name__ == "__main__":
    engine = Engine()
    candidates = [engine.actors[0], engine.actors[1], engine.actors[2]]

    engine.presidential_elections(candidates)
