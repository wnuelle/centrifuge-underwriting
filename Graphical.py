import Loan
import Underwriter
import Pool
import matplotlib.pyplot as plt

def uwTinPlot(Underwriters,Pool):
	data = {Underwriters[index].uwId : Underwriters[index].tin[Pool]  for index in range(len(Underwriters))}

	#plt.bar(data.keys(),data.values())
	#plt.ylim(0,10000)
	#plt.show()

def PoolPayoutPlot(Pool):
	fig, (ax1,ax2) = plt.subplots(1, 2)
	ax1.plot([i for i in range(365)],Pool.seniorROIHist,color='b',linewidth=3,label='Senior Tranche % ROI')
	ax1.plot([i for i in range(365)],Pool.juniorROIHist,color='r',linewidth=3,label='Junior Tranche % ROI')
	ax1.set_ylabel('Cash-on-cash % return')
	ax1.set_ylim(-1.02,0.4)
	ax1.legend()
	ax1.set_title('Cash ROI for Senior/Junior Tranche')

	ax2.plot([i for i in range(365)],Pool.defaultCountHist,linewidth=3)
	ax2.set_ylabel('Pool defaults')
	ax2.set_ylim(-0.02,2)
	ax2.set_title('Default Count')
	fig.suptitle(f'{Pool.name} core metrics')
	plt.show()
