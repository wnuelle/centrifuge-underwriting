import pandas as pd
import Loan
import json

MINIMUM_TIN_THRESHOLD = 5000

class Pool:
	def __init__(self,name,assetOriginator,seniorAPR):
		### Overview
		self.name = name
		self.assetOriginator = assetOriginator
		self.defaultCount = 0

		### Investors 
		self.principalInvested = 0
		self.seniorTrancheNot = 0 
		self.juniorTrancheNot = 0
		self.stkJuniorTrancheNot = 0
		self.cashReserve = 0
		self.cashOut = 0
		self.duration = 365

		### Loans
		self.assetValue = 0
		self.seniorAPR = seniorAPR
		self.assets = []
		self.hopper = []

		### Metrics
		self.poolValue = self.assetValue + self.cashReserve
		if self.poolValue == 0:
			self.tinBuffer = 0
		else:
			self.tinBuffer = self.juniorTrancheNot / self.poolValue

		if self.poolValue == 0:
			self.cashDrag = 0
		else:
			self.cashDrag = self.cashReserve / self.poolValue

		self.seniorROI = 0
		self.juniorROI = -1.0
		self.printDetails()

		### Historical tracker
		self.seniorROIHist = []
		self.juniorROIHist = []
		self.defaultCountHist = []

	def calculateJuniorAPR(self):
		#self.juniorAPR = self.principalInvested*self.
		return 0

	def addLoan(self,Loan):
		self.assets.append(Loan)
		self.assetValue += Loan.notionalAmount
		self.cashReserve -= Loan.notionalAmount
		self.cashDrag = self.cashReserve / self.poolValue
		#self.stkJuniorTrancheNot += Loan.proposalStake
		#self.juniorTrancheNot -= Loan.proposalStake

	def newLoanProposal(self,Loan):
		self.hopper.append(Loan)

	def resetProposalWeights(self):
		for loan in self.hopper:
			loan.proposalStake = {}

	def selectLoan(self):
		maxStake = 0
		
		hopperRank = {self.hopper[i]:sum(list(self.hopper[i].proposalStake.values())) for i in range(len(self.hopper))}

		hopperRank = dict(sorted(hopperRank.items(), key=lambda item: item[1])[::-1])
		_hopper = list(hopperRank.keys())

		print('##### PROPOSAL WEIGHTS #####')
		for i in range(len(hopperRank.keys())):
			print(i+1,'Loan ID',_hopper[i].loanId,'Notional amount: $',_hopper[i].notionalAmount,'Underwriter stake: $',sum(list(_hopper[i].proposalStake.values())))

		index = 0
		dec = True
		while True:

			### Threshold ruleset implemented
			if  list(hopperRank.keys())[index].notionalAmount < self.cashReserve and sum(list(_hopper[index].proposalStake.values())) > MINIMUM_TIN_THRESHOLD:
				winningLoan = list(hopperRank.keys())[index]
				print(f'DECISION: Loan {winningLoan.loanId} included this epoch')
				dec = True
				self.addLoan(winningLoan)
				self.hopper.remove(winningLoan)

				for uw in winningLoan.proposalStake.keys():
					amt = winningLoan.proposalStake[uw]
					uw.stakeTin(self,winningLoan,amt)
					winningLoan.loanStake[uw] = amt
				break
			else:
				if index < len(hopperRank.keys())-1:
					index += 1
				else:
					print('DECISION: No Loans included this Epoch')
					dec = False
					break

		self.resetProposalWeights()
		return dec

	def approveLoan(self,Loan):
		if Loan in self.hopper:
			return True

	def newInvestment(self,amt,senior=True,junior=False):
		if senior and junior:
			raise Error('Cant invest in both senior and junior')
		if senior:
			self.seniorTrancheNot += amt
		if junior:
			self.juniorTrancheNot += amt
		self.principalInvested += amt
		self.cashReserve += amt
		self.poolValue = self.assetValue + self.cashReserve
		self.tinBuffer = self.juniorTrancheNot / self.poolValue
		self.cashDrag = self.cashReserve / self.poolValue

		if senior:
			text = 'SENIOR'
		else:
			text = 'JUNIOR'

		print(f'-- NEW INVESTMENT ({text} TRANCHE)--')
		self.printDetails()

	def loanRepayments(self):
		#print('##### LOAN PAYMENTS #####')
		
		for asset in self.assets:
			asset.repay()

	def tracker(self):
		self.seniorROIHist.append(self.seniorROI)
		self.juniorROIHist.append(self.juniorROI)
		self.defaultCountHist.append(self.defaultCount)

	def printDetails(self):
		print()
		print('##################### POOL #####################')
		print(f'                NAME: {self.name}              ')
		print(f'          POOL VALUE: ${self.poolValue}        ')
		print(f'  PRINCIPAL INVESTED: ${self.principalInvested}')
		print(f'         ASSET VALUE: ${self.assetValue}       ')
		print(f'        CASH RESERVE: ${self.cashReserve}      ')
		print(f'            DROP APR: {round(100*self.seniorAPR,2)}%')
		print(f'          TIN BUFFER: {round(100*self.tinBuffer,2)}%')
		print(f'        TIN NOTIONAL: ${self.juniorTrancheNot} ')
		#print(f' STAKED TIN NOTIONAL: ${self.stkJuniorTrancheNot}')
		print(f'       DROP NOTIONAL: ${self.seniorTrancheNot} ')
		print(f'           CASH DRAG: {round(100*self.cashDrag,2)}%')
		print(f'            CASH OUT: ${round(self.cashOut,2)}')
		print(f'          SENIOR ROI: {round(self.seniorROI*100,2)}%')
		print(f'          JUNIOR ROI: {round(self.juniorROI*100,2)}%')
		print()
		for i in range(len(self.assets)):
			loan = self.assets[i]
			print(f'{i+1}	     Loan ID: {loan.loanId} | Loan amount: ${round(loan.initialBalance,2)}		')
		print('################################################')
		print()
