#!/usr/bin/python

from itertools import combinations
import csv

trainingPoints = 400
noTraining = False
csvfile = 'squad.csv'

dividerSquad = 'Squad'
dividerMission = 'Missions'
dividerTraining = 'Initial Training'

squad = []
goals = []
initialTraining = None

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

def validTraining(training, trainingPoints):
	#print 'testing',training,trainingPoints
	
	p = training.getPhys()
	m = training.getMent()
	t = training.getTact()
	
	if (p + m + t) > trainingPoints:
		#print p,m,t,'greater than',trainingPoints
		return False
	
	if p < 0 or m < 0 or t < 0:
		#print p,m,t,'something feels negative'
		return False
	
	return True

def getTraining(initialTraining,trainingPoints):
	options = [initialTraining]
	optIndex = 0
	optLen = 1
	
	while optIndex < optLen:
		opt = options[optIndex]
		optIndex += 1
		yield opt
		
		# max of three training sessions
		if opt.getLevel() >= 3:
			continue
		
		newLevel = opt.getLevel()+1
		newName = 'Training {}'.format(newLevel)
		
		variants = []
		variants.append(Recruit(newName, newLevel, opt.getPhys()+40, opt.getMent()-20, opt.getTact()-20))
		variants.append(Recruit(newName, newLevel, opt.getPhys()-20, opt.getMent()+40, opt.getTact()-20))
		variants.append(Recruit(newName, newLevel, opt.getPhys()-20, opt.getMent()-20, opt.getTact()+40))
		variants.append(Recruit(newName, newLevel, opt.getPhys()-40, opt.getMent()+20, opt.getTact()+20))
		variants.append(Recruit(newName, newLevel, opt.getPhys()+20, opt.getMent()-40, opt.getTact()+20))
		variants.append(Recruit(newName, newLevel, opt.getPhys()+20, opt.getMent()+20, opt.getTact()-40))
		
		for v in variants:
			if validTraining(v, trainingPoints) and v not in options:
				#print '### adding',v,'from',opt
				options.append(v)
		
		optLen = len(options)

def mission(xyz, training, initialTraining, goal, goalZeroes):
	if noTraining and (training != initialTraining):
		return None
		
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

def getWins(initialTraining, goal, goalZeroes = 3):
	platoon = [x for x in squad if x.getLevel() >= goal.getLevel()]
	
	for xyz in combinations(platoon, 4):
		for training in getTraining(initialTraining, trainingPoints):
			win = mission(xyz, training, initialTraining, goal, goalZeroes)
			if win:
				yield win

def wincmp(a,b):
	global initialTraining
	res = int(round(a[2] - b[2]))
	if res:
		return res
	dist = int(round(trainingDistance(a[1], initialTraining) - trainingDistance(b[1], initialTraining)))
	if dist:
		return dist
	return sum([x.getLevel() for x in a[0]]) - sum([x.getLevel() for x in b[0]])

def writeCsv():
	with open(csvfile, 'w') as f:
		fieldnames = ['type', 'name', 'level', 'physical', 'mental', 'tactical', 'labels', 'chemistry', 'effect']
		writer = csv.DictWriter(f, fieldnames = fieldnames)
		writer.writeheader()
		writer.writerow(initialTraining.toDict(dividerTraining))
		for s in squad:
			writer.writerow(s.toDict(dividerSquad))
		for g in goals:
			writer.writerow(g.toDict(dividerMission))

def readCsv():
	global initialTraining, goals, squad
	
	with open(csvfile, 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			rec = Recruit(row['name'], int(row['level']), int(row['physical']), int(row['mental']), 
				int(row['tactical']), row['labels'], row['chemistry'], row['effect'])
			type = row['type']
		
			if type == dividerTraining:
				initialTraining = rec
			elif type == dividerSquad:
				squad.append(rec)
			elif type == dividerMission:
				goals.append(rec)

readCsv()
			
goals.sort(key = lambda x: x.getLevel(), reverse = True)

mvp = {}
for s in squad:
	mvp[s.getName()] = 0

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
		
		if totalVictory:
			for win in wins:
				for x in win[0]:
					mvp[x.getName()] += 1

		for win in wins:
			print "   Best training: Physical={}, Mental={}, Tactical={} Diff={} Effort={}".format(
				win[1].getPhys(),win[1].getMent(),win[1].getTact(), win[2], win[1].getLevel())
			print "   Best team of {}: {}".format(len(wins), ', '.join([x.getName()+' ('+str(x.getLevel())+')' for x in win[0]]))
			break
		print

print "MVPs:"
print

squadScore = [(mvp[s],s) for s in mvp]
squadScore.sort(reverse = True)

for score, name in squadScore:
	print '{:4} {}'.format(score, name)


