import util
import pandas as pd
from datetime import datetime, timedelta
import random

class Loan:
	def __init__(self,pool,notionalAmount,duration,truePod,trueLGD):
		self.pool = pool
		self.loanId = f"loan{random.randint(1000,9999)}"
		self.initialBalance = notionalAmount
		self.notionalAmount = notionalAmount
		self.interestRate = 0.06
		self.truePod = truePod
		self.trueLGD = trueLGD
		self.expectedLoss = -self.truePod*self.trueLGD
		self.financingFee = 0
		self.financingDate = datetime.now() + timedelta(days=0)
		self.initialDuration = duration
		self.duration = duration
		self.outstanding = self.notionalAmount
		self.paidPrincipal = 0
		self.paidInterest = 0
		self.EPOCH = 1
		self.proposalStake = {}
		self.loanStake = {}
		self.totalRepay = 0
	
	def calculateRepayAmount(self):
		

		P = self.initialBalance
		n = self.initialDuration
		r = self.interestRate
		
		return P*(1+r)**(n/365) / 365

	def repay(self):
		daily_PoD = 1 - (1 - self.truePod)**(1/365)
		if util.bernoulli(daily_PoD) == 1:
			self.pool.defaultCount += 1
			self.duration = 0
			loss = -self.trueLGD*self.notionalAmount
			print('Loss incurred:',loss)
			print('Prev UW balances:',self.loanStake)
			self.loanStake = {uw:0 for uw in self.loanStake.keys()}
			print('New UW balances:',self.loanStake)
			self.pool.assets.remove(self)
		else:
			#self.outstanding
			pmt = self.calculateRepayAmount()

			#print('Loan balance:',self.initialBalance)
			#print('Interest rate:',self.interestRate)
			#print('Payment amt:',pmt)
			#print('Remaining duration:',self.duration)
			self.notionalAmount -= pmt
			self.duration -= self.EPOCH
			self.totalRepay += pmt
			#print('Total repaid:',self.totalRepay)
			if self.pool.cashOut < (self.pool.seniorTrancheNot*(1+self.pool.seniorAPR)**(self.pool.duration/365)):
				self.pool.cashOut += pmt
				#print('Cashout:',self.pool.cashOut)
				#print('Initial notional:',self.pool.seniorTrancheNot)
				self.pool.seniorROI = self.pool.cashOut / self.pool.seniorTrancheNot - 1
			#else:



			"""
			for stkr in self.loanStake.keys():
				print(stkr.uwId)
				print(stkr.stakedTin)
			"""