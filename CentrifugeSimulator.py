import pandas as pd
from Loan import Loan
from Pool import Pool
from Investor import Investor
from Underwriter import Underwriter
import Graphical
import random
import util

import matplotlib.pyplot as plt

def passEpoch(Pool):
	Pool.loanRepayments()
	Pool.tracker()

def generatePortfolio(Pool):

	loanFound = True
	loanMissedCount = 0
	while loanMissedCount < 5:
		for _ in range(10):

			if len(Pool.hopper) < 100:
				notionalAmount = random.randint(10000,250000)
				duration = 365
				TruePoD = random.randint(0,500)/10000
				TrueLGD = random.randint(100,900)/1000
				l = Loan(Pool,notionalAmount,duration,TruePoD,TrueLGD)
				Pool.newLoanProposal(l)

		[uw.evalProposals(Pool) for uw in Underwriters]
		decision = Pool.selectLoan()
		if not decision:
			loanMissedCount+=1
		print()
		print()
		Pool.printDetails()

	Pool.cashOut = Pool.cashReserve
	Pool.cashReserve = 0

def simulate():

	global Underwriters
	Underwriters = [Underwriter() for _ in range(20)]

	Inv1 = Investor()
	ns3 = Pool('NS3','NewSilver',0.034,Underwriters)
	Inv1.buyTin(ns3,100000)
	Inv1.buyDrop(ns3,900000)
	[uw.buyTin(ns3,amt=random.randint(0,10000)) for uw in Underwriters]

	Graphical.uwTinPlot(Underwriters,ns3)
	generatePortfolio(ns3)

	
	for i in range(365):
	#while True:
		print(f'--------------------- EPOCH {i+1} ---------------------')
		passEpoch(ns3)
		ns3.printDetails()
		Graphical.uwTinPlot(Underwriters,ns3)

	Graphical.PoolPayoutPlot(ns3)
	"""
	for uw in Underwriters:
		print(uw.uwId)
		print(uw.tin)
		print(uw.stakedTin)
		print(uw.notionalBalHist)
		print(len(uw.notionalBalHist))
		print()
	"""

if __name__ == '__main__':
	for _ in range(5):
		simulate()
