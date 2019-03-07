#!/usr/bin/python

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

def mission(xyz, training, initialTraining, goal, goalZeroes):
	phys = sum([x.getPhys(xyz, goal) for x in xyz])
	ment = sum([x.getMent(xyz, goal) for x in xyz])
	tact = sum([x.getTact(xyz, goal) for x in xyz])
	
	dphys = max(0,goal.getPhys() - training.getPhys() - phys)
	dment = max(0,goal.getMent() - training.getMent() - ment)
	dtact = max(0,goal.getTact() - training.getTact() - tact)
	
	diff = dphys + dment + dtact
	zeroes = sum([1 for z in [dphys, dment, dtact] if not z])
	
	if zeroes == goalZeroes:
		return (xyz,training,diff)
	else:
		return None
		
def trainingDistance(t1,t2):
	p = t1.getPhys() - t2.getPhys()
	m = t1.getMent() - t2.getMent()
	t = t1.getTact() - t2.getTact()
	return pow(pow(p,2)+pow(m,2)+pow(t,2), 0.5)

squad = [
	Recruit('Cecily', 51, 28, 131, 37, 'Hyur Conjurer', 'Archer > 1', 'score * 0.3'),
	Recruit('Nanasomi', 51, 45, 28, 123, 'Lalafell Archer', 'Hyur > 0', 'ment * 0.1'),
	Recruit('Hastaloeya', 52, 120, 28, 50, 'Roegadyn Marauder', 'Roegadyn < 2', 'tact * 0.1'),
	Recruit('Elchi', 51, 61, 28, 107, 'AuRa Lancer', 'Pugilist > 0', 'score * 0.1'),
	Recruit('Totodi', 42, 63, 37, 78, 'Lalafell Pugilist', 'Level > 50', 'ment * 0.15'),
	Recruit('Rivienne', 44, 26, 122, 34, 'Elezen Conjurer', 'Elezen > 0', 'score * 0.1'),
	Recruit('Sofine', 44, 26, 91, 65, 'Elezen Arcanist'),
	Recruit('Koenbryda', 44, 99, 26, 57, 'Roegadyn Gladiator', 'Rogue > 0', 'phys * 0.15')
]

goals = [
	#Recruit('Flagged Mission: Crystal Recovery', 40, 315, 325, 340),
	Recruit('Frontline Support', 20, 410, 270, 145, 'AuRa Marauder'),
	Recruit('Officer Escort', 20, 415, 275, 150, 'Miqote'),
	Recruit('Border Patrol', 25, 280, 450, 140, 'Gladiator'),
	Recruit('Stronghold Recon', 30, 155, 465, 295),
	Recruit('Allied Maneuvers', 35, 185, 310, 465),
	Recruit('Search and Rescue', 35, 310, 185, 465, 'Arcanist'),
	#Recruit('Flagged Mission: Sapper Strike', 50, 370, 355, 345, 'Conjurer Elezen'),
	Recruit('Black Market Crackdown', 40, 530, 385, 275, 'Pugilist Arcanist'),
	Recruit('Imperial Recon', 40, 385, 560, 245, 'Conjurer'),
	Recruit('Imperial Pursuit', 40, 265, 385, 540, 'Lancer Miqote'),
	Recruit('Imperial Feint', 40, 530, 275, 385, 'Roegadyn Hyur'),
	Recruit('Criminal Pursuit', 40, 265, 385, 540, 'Rogue'),
	Recruit('Primal Recon', 50, 275, 520, 430, 'Pugilist Elezen'),
	Recruit('Counter-magitek Exercises', 50, 590, 305, 430),
	Recruit('Infiltrate and Rescue', 50, 295, 430, 600, 'Gladiator Roegadyn'),
	Recruit('Cult Crackdown', 50, 590, 305, 430, 'Arcanist Pugilist'),
	Recruit('Supply Wagon Destruction', 40, 530, 275, 385, 'Marauder Hyur Lancer'),
	Recruit('Voidsent Elimination', 50, 295, 430, 600, 'Miqote AuRa Hyur'),
	Recruit('Armor Annihilation', 50, 430, 620, 275),
	Recruit('Invasive Testing', 50, 590, 430, 305, 'Rogue'),
	Recruit('Imposter Alert', 50, 430, 295, 600, 'Conjurer'),
	Recruit('Outlaw Subjugation', 50, 590, 430, 305),
	Recruit('Supply Line Disruption', 40, 245, 560, 385, 'Lancer'),
	Recruit('Chimerical Elimination', 40, 245, 560, 385, 'Hyur Thaumaturge'),
	Recruit('Stronghold Assault', 40, 385, 265, 540, 'Lancer')
]

def getWins(initialTraining, goal, goalZeroes = 3):
	platoon = [x for x in squad if x.getLevel() >= goal.getLevel()]
	
	for xyz in combinations(platoon, 4):
		for training in getTraining(trainingPoints):
			win = mission(xyz, training, initialTraining, goal, goalZeroes)
			if win:
				yield win


initialTraining = Recruit('Initial Training', 3, 220, 120, 60)

def wincmp(a,b):
	global initialTraining
	res = int(round(a[2] - b[2]))
	if res:
		return res
	return int(round(trainingDistance(a[1], initialTraining) - trainingDistance(b[1], initialTraining)))
				
goals.sort(key = lambda x: x.getLevel(), reverse = True)

for goal in goals:
	totalVictory = True
	for goalZeroes in range(3,1,-1):
		wins = [win for win in getWins(initialTraining, goal, goalZeroes)]
		if wins:
			break
		totalVictory = False
	
	if wins:
		print "Lv.{} mission: {}".format(goal.getLevel(), goal.getName())
		if totalVictory:
			print "   TOTAL VICTORY!!!!!!!!!!!"
		if goal.getLabels():
			print "   Affinities: {}".format(goal.getLabels())
		wins.sort(cmp = wincmp)
		for win in wins:
			print "   Best training: Physical={}, Mental={}, Tactical={} Diff={}".format(
				win[1].getPhys(),win[1].getMent(),win[1].getTact(), win[2])
			print "   Best team of {}: {}".format(len(wins), ', '.join([x.getName()+' ('+str(x.getLevel())+')' for x in win[0]]))
			break
		print


