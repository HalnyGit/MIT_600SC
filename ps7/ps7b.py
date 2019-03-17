import random
import pylab


def rollDice():
	"""
	Imitates a single 6-sided dice
	return: integer between 1 and 6
	"""
	return random.choice([1,2,3,4,5,6])

def roll_n_dices(n):
	"""
	Imitates results of rolling n dices independently
	return: string where each number represents result of one dice
	"""
	result = ''
	for _ in range(n):
		result = result + str(rollDice())
	return result
	
def checkYahtzee(numRolls = 100000):
	"""
	returns the ratio (probability) of getting Yahtzee after n-number of rolls
	of x 6-sided dices
	"""
	results = []
	for _ in range(numRolls):
		results.append(roll_n_dices(5))
	yahtzees = 0.0
	for result in results:
		if len(set(result)) == 1:
			yahtzees += 1
	return float(yahtzees)/numRolls

def simYahtzee(numTrials, numRolls):
	probabilities = []
	for trial in range(numTrials):
		probabilities.append(checkYahtzee(numRolls))
	return probabilities
		
def stDev(X):
	"""
	X - list of numbers
	returns: tuple of (mean, standard deviation, coefficient of variation)
	"""
	mean = sum(X) / float(len(X))
	total = 0.0
	for x in X:
		total += (x - mean)**2
	st_dev = (total / len(X))**0.5
	co_var = st_dev / mean
	return (mean, st_dev, co_var) 

def makeplot(numTrials = 100, numRolls = 100000):		
	probabilities = simYahtzee(numTrials, numRolls)
	mean, st_dev, co_var = stDev(probabilities)
	textstr =  'Mean={0:10.8f}, st.dev={1:10.8f}, coef.var={2:10.8f}'.format(mean, st_dev, co_var)
	pylab.figure()
	pylab.title(str(numTrials) + ' trials of ' + str(numRolls) + ' rolls each' + '\n' + textstr)
	pylab.xlabel('Probabilities of Yahtzee')
	pylab.ylabel('Number of occurance')
	pylab.hist(probabilities, bins = 20)
	pylab.show()
	
makeplot()



