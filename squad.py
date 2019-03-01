#/usr/bin/python

from itertools import combinations

trainingPoints = 400

def countLabels(squad, tag):
	return sum([1 for x in squad if tag in x.getLabels()])

class Recruit():
	def __init__(self, name, level, phys, ment, tact, labels='', chemistry='', effect=''):
		self.name = name
		self.level = level
		self.phys = phys
		self.ment = ment
		self.tact = tact
		self.labels = labels
		self.chemistry = chemistry
		self.effect = effect
	
	def __str__(self):
		return "{} ({},{},{})".format(self.name,self.phys,self.ment,self.tact)
	
	def __repr__(self):
		return self.name
	
	def getName(self):
		return self.name
	
	def getLevel(self):
		return self.level
	
	def getLabels(self):
		return self.labels

	def getChemistry(self):
		return self.chemistry
	
	def getAffinity(self, goal):
		if not goal or not self.labels or not goal.getLabels():
			return False
		toks = self.labels.split(' ')
		affinities = goal.getLabels().split(' ')
		return len([t for t in toks if t in affinities]) > 0

	def getPhys(self, squad=None, goal=None):
		if squad:
			return self.getStat('phys', lambda x: x.getPhys(), squad, goal)
		return self.phys

	def getMent(self, squad=None, goal=None):
		if squad:
			return self.getStat('ment', lambda x: x.getMent(), squad, goal)
		return self.ment

	def getTact(self, squad=None, goal=None):
		if squad:
			return self.getStat('tact', lambda x: x.getTact(), squad, goal)
		return self.tact
	
	def getStat(self, stat, statter, squad=None, goal=None):
		bonus = 0
		if squad and stat in self.effect:
			toks = self.chemistry.split(' ')
			#print "Chemistry",toks
			count = countLabels(squad, toks[0])
			if toks[1] == '<' and count < int(toks[2]):
				ineffect = True
			elif toks[1] == '>' and count > int(toks[2]):
				ineffect = True
			else:
				ineffect = False;
			if ineffect:
				toks = self.effect.split(' ')
				bonus = statter(self) * float(toks[2])
		if self.getAffinity(goal):
			bonus *= 2
		return statter(self) + bonus

def getTraining(trainingPoints):
	increment = 20
	for phys in range(0,trainingPoints+increment,increment):
		for ment in range(0,trainingPoints+increment,increment):
			if phys + ment > trainingPoints:
				break
			yield Recruit('Training', 0, phys, ment, trainingPoints - phys - ment)

def mission(xyz, training, initialTraining, goal):
	phys = sum([x.getPhys(xyz, goal) for x in xyz])
	ment = sum([x.getMent(xyz, goal) for x in xyz])
	tact = sum([x.getTact(xyz, goal) for x in xyz])
	
	dphys = max(0,goal.getPhys() - training.getPhys() - phys)
	dment = max(0,goal.getMent() - training.getMent() - ment)
	dtact = max(0,goal.getTact() - training.getTact() - tact)
	
	diff = dphys + dment + dtact
	zeroes = sum([1 for z in [dphys, dment, dtact] if not z])
	
	if zeroes == 3:
		return (xyz,training)
	else:
		return None
		
def trainingDistance(t1,t2):
	p = t1.getPhys() - t2.getPhys()
	m = t1.getMent() - t2.getMent()
	t = t1.getTact() - t2.getTact()
	return pow(pow(p,2)+pow(m,2)+pow(t,2), 0.5)

squad = [
	Recruit('Cecily', 45, 26, 124, 34, 'Hyur Conjurer', 'Conjurer < 4', 'score * 0.2'),
	Recruit('Nanasomi', 46, 42, 26, 118, 'Lalafell Archer', 'Lancer > 0', 'score * 0.1'),
	Recruit('Hastaloeya', 47, 115, 27, 46, 'Roegadyn Marauder', 'Roegadyn < 2', 'tact * 0.1'),
	Recruit('Elchi', 44, 58, 26, 98, 'AuRa Lancer', 'Miqote > 0', 'score * 0.1'),
	Recruit('Totodi', 37, 60, 36, 72, 'Lalafell Pugilist'),
	Recruit('Rivienne', 38, 24, 115, 31, 'Elezen Conjurer', 'Lalafell > 0', 'score * 0.1'),
	Recruit('Sofine', 38, 24, 85, 61, 'Elezen Arcanist'),
	Recruit('Koenbryda', 40, 96, 24, 54, 'Roegadyn Gladiator')
]

goals = [
	#Recruit('Flagged Mission: Crystal Recovery', 40, 315, 325, 340),
	Recruit('Frontline Support', 20, 410, 145, 270, 'Conjurer'),
	Recruit('Officer Escort', 20, 130, 440, 270),
	Recruit('Border Patrol', 25, 140, 450, 280, 'Miqote'),
	Recruit('Stronghold Recon', 30, 440, 300, 175, 'Lalafell Hyur'),
	Recruit('Allied Maneuvers', 35, 310, 480, 170, 'Archer'),
	Recruit('Search and Rescue', 35, 185, 310, 465),
	Recruit('Flagged Mission: Sapper Strike', 50, 370, 355, 345, 'Conjurer Elezen'),
	Recruit('Black Market Crackdown', 40, 245, 560, 385, 'Rogue'),
	Recruit('Imperial Recon', 40, 265, 385, 540, 'Marauder'),
	Recruit('Imperial Pursuit', 40, 385, 560, 245, 'Arcanist'),
	Recruit('Imperial Feint', 40, 385, 265, 540, 'AuRa Hyur'),
	Recruit('Criminal Pursuit', 40, 530, 385, 275, 'Lalafell Arcanist Conjurer'),
	Recruit('Primal Recon', 50, 430, 295, 600, 'Marauder Miqote Arcanist'),
	Recruit('Counter-magitek Exercises', 50, 430, 620, 275, 'Conjurer'),
	Recruit('Infiltrate and Rescue', 50, 590, 430, 305, 'Thaumaturge Gladiator'),
	Recruit('Cult Crackdown', 50, 430, 295, 600, 'Miqote Thaumaturge'),
	Recruit('Supply Wagon Destruction', 40, 385, 560, 245, 'Pugilist'),
	Recruit('Outlaw Subjugation', 50, 590, 430, 305),
	Recruit('Supply Line Disruption', 40, 530, 385, 275),
	Recruit('Chimerical Elimination', 40, 385, 265, 540),
	Recruit('Stronghold Assault', 40, 530, 275, 385)
]

def getWins(initialTraining, goal):
	platoon = [x for x in squad if x.getLevel() >= goal.getLevel()]
	
	for xyz in combinations(platoon, 4):
		for training in getTraining(trainingPoints):
			win = mission(xyz, training, initialTraining, goal)
			if win:
				yield win


initialTraining = Recruit('Initial Training', 3, 160, 120, 120)

goals.sort(key = lambda x: x.getLevel(), reverse = True)

for goal in goals:
	wins = [win for win in getWins(initialTraining, goal)]
	
	if wins:
		print "Lv.{} mission: {}".format(goal.getLevel(), goal.getName())
		if goal.getLabels():
			print "   Affinities: {}".format(goal.getLabels())
		wins.sort(key = lambda x: trainingDistance(x[1], initialTraining))
		for win in wins:
			print "   Best training: Physical={}, Mental={}, Tactical={}".format(
				win[1].getPhys(),win[1].getMent(),win[1].getTact())
			print "   Best team of {}: {}".format(len(wins), ', '.join([x.getName()+' ('+str(x.getLevel())+')' for x in win[0]]))
			break
		print


