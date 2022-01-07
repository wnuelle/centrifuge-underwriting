import random
import matplotlib.pyplot as plt

def bernoulli(p):
	r = random.uniform(0,1)
	if r <= p:
		return 1
	else:
		return 0

def probabilitySanityCheck(truePoD):
	print()
	print('Annualized PoD:',truePoD)
	daily_PoD = 1 - (1 - truePoD)**(1/365)
	print('Daily PoD:',daily_PoD)
	
	defaultTracker = {}
	numDefaults = 0
	for i in range(10000):
		for _ in range(365):
			if util.bernoulli(daily_PoD) == 1:
				numDefaults += 1
				print(numDefaults)
				break
			else:
				pass
		if not i == 0:
			defaultTracker[i] = numDefaults / i

	plt.plot(defaultTracker.keys(),defaultTracker.values())
	plt.show()