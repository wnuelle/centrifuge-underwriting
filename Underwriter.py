import pandas as pd
from Loan import Loan
from Pool import Pool
import random

class Underwriter:
	def __init__(self):
		self.uwId = f'uw{random.randint(0,100)}'
		self.tin = {}
		self.stakedTin = {}
		self.Pools = {}

		self.notionalBal = 0
		self.notionalBalHist = []  

	def updateNotionalBal(self):
		self.notionalBal = sum(list(self.tin.values())) + sum(list(self.stakedTin.values()))

	def buyTin(self,Pool,amt):
		### Distribution
		amt=random.randint(0,10000)
		Pool.newInvestment(amt,senior=False,junior=True)
		if Pool in self.tin.keys():
			tin_ = self.tin[Pool]
			tin_ += amt
			self.tin[Pool] = tin_
		else:
			tin_ = 0
			tin_ += amt
			self.tin[Pool] = tin_
		self.stakedTin[Pool] = 0.0

	def evalProposals(self,Pool):

		### Random staking strategy, uw stakes all on a single Loan
		if not self.tin[Pool] == 0:
			index = random.randint(0,len(Pool.hopper)-1)
			loan = Pool.hopper[index]
			loan.proposalStake[self] = self.tin[Pool]

	def stakeTin(self,Pool,loan,amt):
		self.stakedTin[Pool] = self.stakedTin.get(Pool, 0) + amt
		self.tin[Pool] -= amt
		self.Pools[Pool] = {loan:amt}

	def tracker(self):
		self.notionalBalHist.append(self.notionalBal)