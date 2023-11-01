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
    def compatibility_relative(cls, s1, s2):
        return (
        abs(s1.social - s2.social),
        abs(s1.institutional - s2.institutional),
        abs(s1.economical - s2.economical),
    )

    @classmethod
    def compatibility_absolute(cls, s1, s2):
        return sum(cls.compatibility_relative(s1, s2)) / 3

    @classmethod
    def mean(cls, *args):
        social, institutional, economical = []
        for spectrum in args:
            social.append(spectrum.social)
            institutional.append(spectrum.institutional)
            economical.append(spectrum.economical)
        ret = tuple(map(lambda x: sum(x)/len(x), [social, institutional, economical]))
        return cls(ret[0], ret[1], ret[2])

class Country:
    def __init__(self, name):
        self.name = name
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
        self.actors[0].spectrum = Political_Spectrum(0.4, 0.5, 0.4)
        self.actors[1].spectrum = Political_Spectrum(0.00, -0.5, -0.7)
        self.actors[2].spectrum = Political_Spectrum(-0.5, -0.4, -0.7)

        self.parties = [Party("LFI", "La France Insoumise"), Party("RE", "Renaissance"), Party("RN", "Rassemblement National")]
        self.countries = [Country("France")]

        self.parties[0].leader = self.actors[0]
        self.parties[1].leader = self.actors[1]
        self.parties[2].leader = self.actors[2]

    def update_parties_spectrum(self):
        parties_members = dict()
        for party in self.parties:
            parties_members[party] = set()

        for actor in self.actors:
            if actor.party:
                parties_members[actor.party].add(actor)

        for party in self.parties:
            if parties_members[party]:
                party.spectrum = Political_Spectrum.mean(*map(lambda x: x.spectrum, self.parties_members[party]))
            else:
                party.spectrum = Political_Spectrum()

    def presidential_elections(self, candidates):
        print("Élections Présidentielles")
        electors = list(actor for actor in self.actors if actor.age >= 18)
        print(len(electors), "électeurs")

        ballot = []
        for actor in self.actors:
            compatibility = list((candidate, Political_Spectrum.compatibility_absolute(actor.spectrum, candidate.spectrum)) for candidate in candidates)
            ballot.append(min(compatibility, key=lambda x: x[1])[0])

        results = count_votes(ballot)

        winner = None
        ordered_results = list(results.items())
        ordered_results.sort(key=lambda x: x[1], reverse=1)
        for i, result in enumerate(ordered_results):
            print(f"{result[0].fullname()} - {round(result[1] * 100 / len(self.actors), 2)}%")
            if result[1] > (len(self.actors) // 2):
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
