# Goal: To determine the number of features to select for K_best selection using Genetic Algorithms
# Thanks to DEAP for their library to do this in

from deap import algorithms, base, creator, tools
import simplejson as json
from collections import OrderedDict
from openpyxl import load_workbook, Workbook
from urllib2 import Request, urlopen, URLError
import numpy as np
from scipy import interp
from scipy.sparse import csr_matrix
from sklearn import datasets, neighbors, linear_model, cross_validation, feature_selection, svm
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import time as t
import random

def main():

	optimize()
	# fitness([1,0,0,0,0,0,0,0,0,0])

# fitness function: optimizes based on the AUC provided
def fitness(cpd_signal, cpd_zscores, letter, individual):

	n_param = 0
	fitness = 0

	for i in range(len(individual)-1, -1, -1):

		n_param += (2**(9-i))*individual[i]

	if n_param > 640 or n_param<1:

		return (fitness,)

	X = []
	Y = []

	for cpd in cpd_signal:

		Y.append(cpd_signal[cpd][letter])
		X.append(cpd_zscores[cpd])

	X = np.asarray(X)
	Y = np.asarray(Y)

	clf = linear_model.LogisticRegression(C=1e5)

	# clf.fit(X, Y)
	cv = cross_validation.LeaveOneOut(80)

	# total = 0
	# mean_tpr = 0.0
	# mean_fpr = np.linspace(0, 1, 100)

	# print(letter)

	probas_ = []

	for i, (train, test) in enumerate(cv):

		current = X[train]
		# print(current)
		# attempted to use feature selection, but wasn't sure if doing it right
		sel = feature_selection.GenericUnivariateSelect(feature_selection.f_regression, mode='k_best', param = n_param)
		sel.fit(current, Y[train])
		current = sel.transform(current)
		proba_ = clf.fit(current, Y[train]).predict_proba(sel.transform(X[test]))[0][1]
		# print(proba_)
		probas_.append(proba_)
		# total += roc_auc
		
	# avg = total/4

	# # print(ws2[letter+"1"].value + ": " + str(avg))


	fpr, tpr, threshhold = roc_curve(Y, probas_)
	roc_auc = auc(fpr,tpr)

	fitness += roc_auc


	# plt.plot(fpr, tpr, lw=1, label='LOOCV Area = %0.2f' % (roc_auc))


	# ws3["A" + str(ind)].value = ws2[letter + "1"].value
	# ws3["B" + str(ind)].value = roc_auc
	# ind += 1

	# plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')
	# plt.plot(mean_fpr, mean_tpr, 'k--',
#        label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)

	# plt.xlabel('False Positive Rate')
	# plt.ylabel('True Positive Rate')
	# plt.title('ROC-LOOCV Curve for ' + str(ws2[letter + "1"].value))
	# plt.legend(loc="lower right")
	# plt.xlim([-0.05, 1.05])
	# plt.ylim([-0.05, 1.05])
	# plt.show()

	return (fitness,)





# does 3 trials each, and I looked at the results and chose which had a better AUC
def optimize():

	wb = load_workbook("dimensionMatrix.xlsx")
	ws1 = wb["Sheet1"]
	ws2 = wb["Sheet2"]
	ws3 = wb["Sheet3"]
	ws4 = wb["Sheet4"]
	unique_ccl = []

	for i in range(2,44758):

		ccl = int(ws1["C" + str(i)].value)

		if ccl not in unique_ccl:

			unique_ccl.append(ccl)

	unique_ccl = sorted(unique_ccl)

	cpd_signal = {} 

	letters = ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W"]

	for i in range(2,82):

		cpd = int(ws2["A" + str(i)].value)

		if cpd not in cpd_signal:

			cpd_signal[cpd] = {}

		for letter in letters:

			cpd_signal[cpd][letter] = ws2[letter + str(i)].value

	cpd_zscores = {}

	for i in range(2,44758):

		cpd = int(ws1["A" + str(i)].value)

		if cpd not in cpd_zscores:

			cpd_zscores[cpd] = csr_matrix((1, 642)).toarray()[0]

		ccl = int(ws1["C" + str(i)].value)
		current = cpd_zscores[cpd]
		z_score = ws1["E" + str(i)].value

		current[unique_ccl.index(ccl)] = z_score

	letters = ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W"]
	for letter in letters:

		print(letter + "!!!!!")

		results = []

		for k in range(3):

			random.seed(k)

			creator.create("FitnessMax", base.Fitness, weights=(1.0,))
			creator.create("Individual", list, fitness=creator.FitnessMax)

			toolbox = base.Toolbox()
			toolbox.register("attr_bool", random.randint, 0, 1)
			toolbox.register("individual", tools.initRepeat, creator.Individual,
			                 toolbox.attr_bool, n=10)
			toolbox.register("population", tools.initRepeat, list, 
			                 toolbox.individual)
			toolbox.register("evaluate", fitness, cpd_signal, cpd_zscores, letter)
			toolbox.register("mate", tools.cxUniform, indpb = .5)
			toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
			toolbox.register("select", tools.selTournament, tournsize=3)

			pop = toolbox.population(n=15)
			result = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, 
			                             ngen=25, verbose=False)
			results.append(tools.selBest(pop, k=1)[0])

		print('Current best fitnesses for ' + str(ws2[letter + "1"].value) + ': ')
		for j in range(len(results)):

			ind = results[j]
			n_param = 0

			for x in range(len(ind)-1, -1, -1):

				n_param += (2**(9-x))*ind[x]

			print(n_param)

		print("~~~~~~~~~~~")

main()
