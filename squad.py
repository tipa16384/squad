#/usr/bin/python

from itertools import combinations

goal = (140,225,325)
#goal = (315,325,340)
#goal = (455,190,315)
#training = (120,120,40)
training = (100,160,20)

squad = {
	'Cecily': (24,118,32,'Hyur'),
	'Nanasomi': (38,25,113,'Lalafell'),
	'Hastaloeya': (108,25,45,'Roegadyn'),
	'Elchi': (52,24,91,'Au Ra'),
	'Totodi': (57,34,69,'Lalafell'),
	'Rivienne': (22,112,28,'Elezen'),
	'Sofine': (23,83,58,'Elezen'),
	'Saiun': (101,23,40,'Au Ra')
}

maxscore = 10000
best = 'Nobody'
bestZeroes = 0

def tacticalScore(a,b,c,d):
	numHasta = sum([1 for x in [a,b,c,d] if x == 'Hastaloeya'])
	#print [squad[x][3] for x in [a,b,c,d]]
	numRoe = sum([1 for x in [a,b,c,d] if squad[x][3] == 'Roegadyn'])
	tacticalScore = sum([squad[x][2] for x in [a,b,c,d]])
	#print [a,b,c,d], numHasta, numRoe
	
	if numHasta is 1 and numRoe is 1:
		bonus = sum([squad[x][2] * 0.1 for x in [a,b,c,d] if x == 'Hastaloeya'])
		tacticalScore += bonus
		#print "bonus of {}".format(bonus)
	
	return tacticalScore

for a1,b1,c1,d1 in combinations(squad, 4):
	a = squad[a1]
	b = squad[b1]
	c = squad[c1]
	d = squad[d1]

	s0 = max(0,goal[0] - training[0] - a[0] -  b[0] - c[0] - d[0])
	s1 = max(0,goal[1] - training[1] - a[1] -  b[1] - c[1] - d[1])
	s2 = max(0,goal[2] - training[2] - tacticalScore(a1,b1,c1,d1))
	score = s0 + s1 + s2
	zeroes = 0 if s0 else 1
	zeroes += 0 if s1 else 1
	zeroes += 0 if s2 else 1
	if zeroes < bestZeroes:
		continue
	elif zeroes > bestZeroes:
		maxscore = 10000
	bestZeroes = zeroes
	if score < maxscore:
		best = (a1,b1,c1,d1)
		maxscore = score
		print s0,s1,s2,best,score,zeroes

print best,maxscore
