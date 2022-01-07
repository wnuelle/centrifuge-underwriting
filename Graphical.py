import Loan
import Underwriter
import Pool
import matplotlib.pyplot as plt

def uwTinPlot(Underwriters,Pool):
	data = {Underwriters[index].uwId : Underwriters[index].tin[Pool]  for index in range(len(Underwriters))}

	#plt.bar(data.keys(),data.values())
	#plt.ylim(0,10000)
	#plt.show()