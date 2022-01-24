import pandas as pd
from Loan import Loan
from Pool import Pool
import random

class Investor:
	def __init__(self):
		self.invId = f'inv{random.randint(0,100)}'
		self.tin = {}
		self.drop = {}
		self.Pools = {}
		self.initialInvestmentSenior = 0
		self.initialInvestmentJunior = 0
		self.cashOut = 0


	def updateNotionalBal(self):
		self.notionalBal = sum(list(self.tin.values())) + sum(list(self.stakedTin.values()))

	def buyTin(self,Pool,amt):
		### Distribution
		Pool.newInvestment(self,amt,senior=False,junior=True)
		self.initialInvestmentJunior += amt
		if Pool in self.tin.keys():
			tin_ = self.tin[Pool]
			tin_ += amt
			self.tin[Pool] = tin_
		else:
			tin_ = 0
			tin_ += amt
			self.tin[Pool] = tin_

	def buyDrop(self,Pool,amt):
		### Distribution
		Pool.newInvestment(self,amt,senior=True,junior=False)
		self.initialInvestmentSenior += amt
		if Pool in self.drop.keys():
			drop_ = self.drop[Pool]
			drop_ += amt
			self.drop[Pool] = drop_
		else:
			drop_ = 0
			drop_ += amt
			self.drop[Pool] = drop_

	def tracker(self):
		self.notionalBalHist.append(self.notionalBal)