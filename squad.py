#/usr/bin/python

from itertools import combinations

def countLabels(squad, tag):
	return sum([1 for x in squad if tag in x.getLabels()])

class Recruit():
	def __init__(self, name, phys, ment, tact, labels='', chemistry='', effect=''):
		self.name = name
		self.phys = phys
		self.ment = ment
		self.tact = tact
		self.labels = labels
		self.chemistry = chemistry
		self.effect = effect
	
	def __str__(self):
		return self.name
	
	def __repr__(self):
		return self.name
	
	def getName(self):
		return self.name
	
	def getLabels(self):
		return self.labels

	def getChemistry(self):
		return self.chemistry

	def getPhys(self, squad=None):
		return self.phys

	def getMent(self, squad=None):
		return self.ment

	def getTact(self, squad=None):
		bonus = 0
		if squad and 'tact' in self.effect:
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
				bonus = self.tact * float(toks[2])
				#print "applying bonus",bonus
		return self.tact + bonus

goal = Recruit('Squadron Mission', 315, 325, 340)
training = Recruit('Training', 80, 140, 60)

squad = [
	Recruit('Cecily', 25, 119, 32, 'Hyur Conjurer', 'Conjurer < 4', 'score * 0.2'),
	Recruit('Nanasomi', 39, 25, 114, 'Lalafell Archer', 'Lancer > 0', 'score * 0.1'),
	Recruit('Hastaloeya', 108, 26, 46, 'Roegadyn Marauder', 'Roegadyn < 2', 'tact * 0.1'),
	Recruit('Elchi', 55, 24, 93, 'AuRa Lancer', 'Miqote > 0', 'score * 0.1'),
	Recruit('Totodi', 58, 34, 70, 'Lalafell Pugilist'),
	Recruit('Rivienne', 23, 113, 28, 'Elezen Conjurer', 'Lalafell > 0', 'score * 0.1'),
	Recruit('Sofine', 23, 84, 59, 'Elezen Arcanist'),
	Recruit('Saiun', 102, 23, 41, 'AuRa Marauder')
]

maxdiff = 10000
best = 'Nobody'
bestZeroes = 0

for xyz in combinations(squad, 4):
	phys = sum([x.getPhys(xyz) for x in xyz])
	ment = sum([x.getMent(xyz) for x in xyz])
	tact = sum([x.getTact(xyz) for x in xyz])
	
	dphys = max(0,goal.getPhys() - training.getPhys() - phys)
	dment = max(0,goal.getMent() - training.getMent() - ment)
	dtact = max(0,goal.getTact() - training.getTact() - tact)
	
	#print xyz, dphys, dment, dtact

	diff = dphys + dment + dtact
	zeroes = sum([1 for z in [dphys, dment, dtact] if not z])
	
	if zeroes < bestZeroes:
		continue
	elif zeroes > bestZeroes:
		maxdiff = 10000
	bestZeroes = zeroes
	if diff < maxdiff:
		best = xyz
		maxdiff = diff
		print dphys,dment,dtact,best,diff,zeroes

print best,maxdiff
