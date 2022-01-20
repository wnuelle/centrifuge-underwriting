import pandas as pd
from Loan import Loan
from Pool import Pool
from Underwriter import Underwriter
import Graphical
import random
import util

def passEpoch(Pool):
	Pool.loanRepayments()

def generatePortfolio(Pool):

	loanFound = True
	loanMissedCount = 0
	while loanMissedCount < 5:
		for _ in range(10):

			if len(ns3.hopper) < 100:
				notionalAmount = random.randint(10000,250000)
				duration = 365
				TruePoD = random.randint(0,500)/10000
				TrueLGD = random.randint(100,900)/1000
				l = Loan(ns3,notionalAmount,duration,TruePoD,TrueLGD)
				ns3.newLoanProposal(l)

		[uw.evalProposals(ns3) for uw in Underwriters]
		decision = Pool.selectLoan()
		if not decision:
			loanMissedCount+=1
		print()
		print()
		Pool.printDetails()

	Pool.cashOut = Pool.cashReserve
	Pool.cashReserve = 0

if __name__ == '__main__':

	ns3 = Pool('NS3','NewSilver',0.034)
	ns3.newInvestment(900000,senior=True,junior=False)
	ns3.newInvestment(100000,senior=False,junior=True)

	Underwriters = [Underwriter() for _ in range(20)]
	[uw.buyTin(ns3,amt=random.randint(0,10000)) for uw in Underwriters]
	
	Graphical.uwTinPlot(Underwriters,ns3)
	generatePortfolio(ns3)

	
	for i in range(365):
	#while True:
		print(f'--------------------- EPOCH {i+1} ---------------------')
		passEpoch(ns3)
		ns3.printDetails()
		Graphical.uwTinPlot(Underwriters,ns3)

	print('Defaults:',ns3.defaultCount)
	
