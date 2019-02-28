#/usr/bin/python

from itertools import combinations

bignum = 10000
maxdiff = bignum
best = 'Nobody'
bestZeroes = 0
bestTraining = None
trainingPoints = 280
bestTrainingDist = bignum

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

def sumstat(squad, goal, statter):
	return sum([statter(x, xyz, goal) for x in xyz])
			
def mission(xyz, training, initialTraining, goal):
	global maxdiff, best, bestZeroes, bestTraining, bestTrainingDist
	
	phys = sumstat(xyz, goal, lambda x,y,z: x.getPhys(y,z))
	ment = sumstat(xyz, goal, lambda x,y,z: x.getMent(y,z))
	tact = sumstat(xyz, goal, lambda x,y,z: x.getTact(y,z))
	
	dphys = max(0,goal.getPhys() - training.getPhys() - phys)
	dment = max(0,goal.getMent() - training.getMent() - ment)
	dtact = max(0,goal.getTact() - training.getTact() - tact)
	
	#print xyz, dphys, dment, dtact

	diff = dphys + dment + dtact
	zeroes = sum([1 for z in [dphys, dment, dtact] if not z])
	
	if zeroes < bestZeroes:
		return
	elif zeroes > bestZeroes:
		maxdiff = bignum
		bestTrainingDist = bignum
		
	bestZeroes = zeroes
	
	trainingDist = trainingDistance(training, initialTraining)
	
	if diff == maxdiff and trainingDist < bestTrainingDist:
		bestTraining = training
		bestTrainingDist = trainingDist
		#print "Better training",training,bestTrainingDist
	elif diff < maxdiff:
		best = xyz
		maxdiff = diff
		bestTraining = training
		bestTrainingDist = trainingDist
		print dphys,dment,dtact,best,diff,zeroes

def trainingDistance(t1,t2):
	p = t1.getPhys() - t2.getPhys()
	m = t1.getMent() - t2.getMent()
	t = t1.getTact() - t2.getTact()
	return pow(pow(p,2)+pow(m,2)+pow(t,2), 0.5)

squad = [
	Recruit('Cecily', 40, 26, 120, 34, 'Hyur Conjurer', 'Conjurer < 4', 'score * 0.2'),
	Recruit('Nanasomi', 40, 41, 26, 115, 'Lalafell Archer', 'Lancer > 0', 'score * 0.1'),
	Recruit('Hastaloeya', 40, 112, 26, 46, 'Roegadyn Marauder', 'Roegadyn < 2', 'tact * 0.1'),
	Recruit('Elchi', 40, 56, 25, 95, 'AuRa Lancer', 'Miqote > 0', 'score * 0.1'),
	Recruit('Totodi', 40, 59, 35, 72, 'Lalafell Pugilist'),
	Recruit('Rivienne', 40, 24, 114, 30, 'Elezen Conjurer', 'Lalafell > 0', 'score * 0.1'),
	Recruit('Sofine', 40, 24, 84, 60, 'Elezen Arcanist'),
	Recruit('Saiun', 40, 103, 24, 43, 'AuRa Marauder')
]

#goal = Recruit('Flagged Mission: Crystal Recovery', 40, 315, 325, 340)
#goal = Recruit('Allied Maneuvers', 40, 310, 480, 170)
#goal = Recruit('Search and Rescue', 40, 185, 310, 465)
#goal = Recruit('Frontline Support', 40, 410, 145, 270, 'Conjurer')
#goal = Recruit('Officer Escort', 40, 130, 440, 270)
#goal = Recruit('Border Patrol', 40, 140, 450, 280, 'Miqote')
goal = Recruit('Stronghold Recon', 40, 440, 300, 175, 'Lalafell Hyur')

initialTraining = Recruit('Initial Training', 40, 80, 140, 60)

for xyz in combinations(squad, 4):
	for training in getTraining(trainingPoints):
		mission(xyz, training, initialTraining, goal)
		
print best,maxdiff,bestTraining
