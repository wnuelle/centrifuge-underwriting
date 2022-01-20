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
			loss = self.trueLGD*self.notionalAmount
			pct_impairment = loss / sum(list(self.loanStake.values()))
			if pct_impairment > 1.0:
				pct_impairment = 1.0
			self.loanStake = {uw:self.loanStake[uw]*(1-pct_impairment) for uw in self.loanStake.keys()}
			for uw in self.loanStake.keys():
				stkTin = uw.stakedTin[self.pool]
				uw.stakedTin[self.pool] = stkTin*(1-pct_impairment)
				uw.Pools[self.pool][self] = stkTin*(1-pct_impairment)
			self.pool.assetValue -= loss
			self.pool.poolValue = self.pool.assetValue + self.pool.cashReserve
			self.pool.assets.remove(self)
		else:
			pmt = self.calculateRepayAmount()
			self.notionalAmount -= pmt
			self.duration -= self.EPOCH
			self.totalRepay += pmt
			if self.pool.cashOut < (self.pool.seniorTrancheNot*(1+self.pool.seniorAPR)**(self.pool.duration/365)):
				self.pool.cashOut += pmt
				self.pool.assetValue -= pmt
				if self.pool.assetValue < 0:
					self.pool.assetValue = 0
				self.pool.seniorROI = self.pool.cashOut / self.pool.seniorTrancheNot - 1
			else:
				self.pool.cashOut += pmt
				self.pool.assetValue -= pmt
				if self.pool.assetValue < 0:
					self.pool.assetValue = 0
				self.pool.juniorROI = (self.pool.cashOut - (self.pool.seniorTrancheNot*(1+self.pool.seniorAPR)**(self.pool.duration/365))) / self.pool.juniorTrancheNot - 1





