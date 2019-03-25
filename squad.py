#!/usr/bin/python

from itertools import combinations
from recruit import Recruit
import csv

trainingPoints = 400
maxTraining = 6
noTraining = False
#csvfile = 'squad.csv'
csvfile = '/cygdrive/e/Downloads/squad - squad.csv'

dividerSquad = 'Squad'
dividerMission = 'Missions'
dividerTraining = 'Initial Training'

squad = []
goals = []
initialTraining = None

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
		if opt.getLevel() > maxTraining:
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
				v.setHistory(opt.getHistory() + [opt])
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
	res = abs(int(round(a[2] - b[2])))
	if res:
		return res
	dist = abs(int(round(trainingDistance(a[1], initialTraining) - trainingDistance(b[1], initialTraining))))
	if dist:
		return dist
	return abs(sum([x.getLevel() for x in a[0]]) - sum([x.getLevel() for x in b[0]]))

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
		
		for win in wins:
			for x in win[0]:
				mvp[x.getName()] += 1
			print "   Best training: Physical={}, Mental={}, Tactical={} Diff={} Effort={}".format(
				win[1].getPhys(),win[1].getMent(),win[1].getTact(), win[2], win[1].getLevel())
			if win[1].getHistory():
				for h in win[1].getHistory():
					print "      {}".format(h)
			print "   Best team of {}: {}".format(len(wins), ', '.join([x.getName()+' ('+str(x.getLevel())+')' for x in win[0]]))
			break
		print

print "MVPs:"
print

squadScore = [(mvp[s],s) for s in mvp]
squadScore.sort(reverse = True)

for score, name in squadScore:
	print '{:4} {}'.format(score, name)


