#!/usr/bin/python

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
		self.history = []
		
	def __eq__(self, other):
		#print "Compare {} to {}".format(self, other)
		if self.phys != other.phys:
			return False
		if self.ment != other.ment:
			return False
		if self.tact != other.tact:
			return False
		return True
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
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
	
	def getHistory(self):
		return self.history
	
	def setHistory(self, history):
		self.history = history
	
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
			
			if toks[0] == 'Level':
				count = self.getLevel()
			
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
	
	def toDict(self, type):
		dict = {}
		# ['type', 'name', 'level', 'physical', 'mental', 'tactical', 'labels', 'chemistry', 'effect']
		dict['type'] = type
		dict['name'] = self.name
		dict['level'] = self.level
		dict['physical'] = self.phys
		dict['mental'] = self.ment
		dict['tactical'] = self.tact
		dict['labels'] = self.labels
		dict['chemistry'] = self.chemistry
		dict['effect'] = self.effect
		return dict

def countLabels(squad, tag):
	return sum([1 for x in squad if tag in x.getLabels()])
