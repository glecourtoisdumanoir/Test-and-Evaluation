from DynSys import dynsys
from switch_controllerTKTv1 import switch_ctrl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from Bayes_Ex import expected_improvement, propose_location
from Bayes_Ex import plot_approximation, plot_acquisition
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import ConstantKernel, Matern
import os
import pdb
# jeff added this part
import loggerTKTv1 as logger
import pandas as pd
from datetime import datetime
# down to here


def compare(example_1, example_2):
	fig1 = plt.figure()
	lims = (0,5)
	ax1 = fig1.add_subplot(111, aspect='equal')
	ax1.add_patch(
	        patches.Rectangle((0,2.01),0.98,0.98,color=(0.5,0.85,0.5)))
	ax1.add_patch(
	        patches.Rectangle((5,2.01),-0.98,0.98,color=(0.5,0.85,0.5)))
	ax1.add_patch(
	        patches.Rectangle((2.01,0),0.98,0.98,color=(0.5,0.85,0.5)))
	ax1.add_patch(
	        patches.Rectangle((2.01,5),0.98,-0.98,color=(0.5,0.85,0.5)))
	ax1.add_patch(
	        patches.Rectangle((2.01,2.01),0.98,0.98,color=(0.85,0.5,0.5)))
	ax1.add_patch(
	    patches.Rectangle((0, 0), 2, 2,color='black'))
	ax1.add_patch(
	    patches.Rectangle((0, 5), 2, -2,color='black'))
	ax1.add_patch(
	    patches.Rectangle((5, 5), -2, -2,color='black'))
	ax1.add_patch(
	    patches.Rectangle((5, 0), -2, 2,color='black'))
	plt.ylim(lims)
	plt.xlim(lims)
	total_frames = min((example_1.xhist.shape[1],example_2.xhist.shape[1]))

	indicator1, = ax1.plot([],[],'o',lw=3,color='blue')
	indicator2, = ax1.plot([],[],'o',lw=3,color='red')

	def init():
		indicator1.set_data([],[])
		indicator2.set_data([],[])
		return indicator1, indicator2, 

	def animate(i):
		indicator1.set_data(example_1.xhist[0,i],example_1.xhist[1,i])
		indicator2.set_data(example_2.xhist[0,i],example_2.xhist[1,i])
		return indicator1, indicator2, 

	anim = FuncAnimation(fig1, animate, init_func=init,
                               frames=total_frames, interval=30, blit=True)

	anim.save('Petter_Gifs/surveil_error.gif', writer='imagemagick')

def plot_run(example, figname):
	fig1 = plt.figure()
	lims = (0,5)
	ax1 = fig1.add_subplot(111, aspect='equal')
	ax1.add_patch(
	        patches.Rectangle((0,2.01),0.98,0.98,color=(0.5,0.85,0.5)))
	ax1.add_patch(
	        patches.Rectangle((5,2.01),-0.98,0.98,color=(0.5,0.85,0.5)))
	ax1.add_patch(
	        patches.Rectangle((2.01,0),0.98,0.98,color=(0.5,0.85,0.5)))
	ax1.add_patch(
	        patches.Rectangle((2.01,5),0.98,-0.98,color=(0.5,0.85,0.5)))
	ax1.add_patch(
	        patches.Rectangle((2.01,2.01),0.98,0.98,color=(0.85,0.5,0.5)))
	ax1.add_patch(
	    patches.Rectangle((0, 0), 2, 2,color='black'))
	ax1.add_patch(
	    patches.Rectangle((0, 5), 2, -2,color='black'))
	ax1.add_patch(
	    patches.Rectangle((5, 5), -2, -2,color='black'))
	ax1.add_patch(
	    patches.Rectangle((5, 0), -2, 2,color='black'))
	plt.ylim(lims)
	plt.xlim(lims)
	total_frames = example.xhist.shape[1]

	indicator, = ax1.plot([],[],'o',lw=3,color='blue')

	def init():
		indicator.set_data([],[])
		return indicator,

	def animate(i):
		indicator.set_data(example.xhist[0,i],example.xhist[1,i])
		return indicator,


# jeff added this part
# v20210224
	# i=0
	# while (i < example.xhist[0].size) :
	# 	if (i == a) or (i == b) :
	# 		logger.logger.info('SWITCH at time step {}.'.format(i))
	# 		logger.logger.info('x = {}, y = {}, time step {}.'.format(example.xhist[0,i],example.xhist[1,i],i))
	# 	else :
	# 		logger.logger.info('x = {}, y = {}, time step {}.'.format(example.xhist[0,i],example.xhist[1,i],i))
	# 	i+=1
# v20210225
	# i=0
	# logger.logger.info('start, t = {}.'.format(i))
	# while (i < example.xhist[0].size) :
	# 	if (i == a) or (i == b) :
	# 		logger.logger.info('switch, t = {}.'.format(i))
	# 		logger.logger.info('x = {}, y = {}, t = {}.'.format(example.xhist[0,i],example.xhist[1,i],i))
	# 	else :
	# 		logger.logger.info('x = {}, y = {}, t = {}.'.format(example.xhist[0,i],example.xhist[1,i],i))
	# 	i+=1
	# logger.logger.info('end, t = {}.'.format(i))	
# v20210225 v2
	# i=0
	# logger.logger.info('ccc')
	# logger.logger.info('aaa"OBJ_TYPE" : "COMMAND", "Type" : "PetterEx", "Name" : "startSimulation", "Time" : {}bbb'.format(i))
	# while (i < example.xhist[0].size) :
	# 	if (i == a) or (i == b) :
	# 		logger.logger.info('aaa"OBJ_TYPE" : "EVR", "Dispatch" : "switch", "Time" : {}bbb'.format(i))
	# 		logger.logger.info('aaa"OBJ_TYPE" : "EVR", "xPosition" : {}, "yPosition" : {}, "Time" : {}bbb'.format(example.xhist[0,i],example.xhist[1,i],i))
	# 	else :
	# 		logger.logger.info('aaa"OBJ_TYPE" : "EVR", "xPosition" : {}, "yPosition" : {}, "Time" : {}bbb'.format(example.xhist[0,i],example.xhist[1,i],i))
	# 	i+=1
	# logger.logger.info('ddd')
# v20210228
	#i=0
	#logger.logger.info('START')
	#logger.logger.info('aaa"OBJ_TYPE" : "COMMAND", "Type" : "PetterEx", "Name" : "startSimulation", "Time" : {}bbb'.format(i))
	# while (i < example.xhist[0].size) :
	# 	if (i == a) or (i == b) :
	# 		logger.logger.info('switch;{}'.format(i))
	# 		logger.logger.info('{};{};{}'.format(example.xhist[0,i],example.xhist[1,i],i))
	# 	else :
	# 		logger.logger.info('{};{};{}'.format(example.xhist[0,i],example.xhist[1,i],i))
	# 	i+=1
	# logger.logger.info('STOP')
# down to here

	anim = FuncAnimation(fig1, animate, init_func=init,
		frames=total_frames, interval=30, blit=True)

	# jeff added this part
	# logger.logger.info('# PetterExample V1')
	# logger.logger.info('# {}'.format(datetime.now().strftime("%m%d%Y%H%M%S")))
	# logger.logger.info('# a : {}'.format(a))
	# logger.logger.info('# b : {}'.format(b))
	print ("[a,b]:",end = "")
	print ("[",end ="")
	print (a,end ="")
	print (",",end ="")
	print (b,end ="")
	print ("]",end ="")
	print("-------------> worked!")
	# down to here
	#plt.show()	
	#anim.save('/home/jeff/Desktop/GeneralTE-main/Petter_Examples/Petter_Gifs/{}.gif'.format(figname), writer='imagemagick')

def reward_fun(history):
	goals = np.array([
		[1.0,1.0,0.0,0.0],
		[1.0,4.0,0.0,0.0],
		[4.0,1.0,0.0,0.0],
		[4.0,4.0,0.0,0.0]]).transpose()
	num_iterations = history.shape[1]
	reward = 0
	for i in range(num_iterations):
		for j in range(4):
			base = np.max(np.abs(goals[:,j] - history[:,i]))
			if 1/base >= reward:
				reward = 1/base
		
	return reward

class tester:
	def __init__(self):
		self.run_number = 0

	def test_run(self, x):
		#print(x) # remove afterwards
		self.example = switch_ctrl(sys = dynsys(x = np.array([[2.5,0.5,0,0]]).transpose()), 
			params = 1.2*np.array([[1,0,1,0],[0,1,0,1]]))
		self.example.surveil(t_switch1 = x[0], t_switch2 = x[0]+x[1])
		return reward_fun(self.example.xhist)

	""" def optimizer(self):
		bounds = np.array([[0,100],
			[0,50]])

		init_samples = 5
		X_sample = np.random.uniform(bounds[:,0],bounds[:,1],size = (init_samples,2))

		cmax = 0
		best = np.zeros((1,2))
		Y_sample = np.zeros((init_samples,1))
		for i in range(init_samples):
			Y_sample[i,:] = self.test_run(x = np.round(X_sample[i,:]))
			if Y_sample[i,:] > cmax:
				cmax = Y_sample[i,:]
				best = np.round(X_sample[i,:])

		m52 = ConstantKernel(1.0) * Matern(length_scale=1.0, nu=2.5)
		gpr = GaussianProcessRegressor(kernel=m52, alpha=1e-6)

		n_iter = 80

		for i in range(n_iter):
			# Update Gaussian process with existing samples
			gpr.fit(X_sample, Y_sample)

			# Obtain next sampling point from the acquisition function (expected_improvement)
			X_next = propose_location(expected_improvement, X_sample, Y_sample, gpr, bounds)

			# Obtain next noisy sample from the objective function
			Y_next = self.test_run(x = np.round(X_next))

			if Y_next > cmax:
				cmax = Y_next
				best = np.round(X_next)

			# Add sample to previous samples
			X_sample = np.vstack((X_sample, X_next.reshape(1,-1)))
			Y_sample = np.vstack((Y_sample, Y_next))
			print('Finished with iteration %d/%d'%((i+1),n_iter))
			print('Best sample value: %f'%cmax)
			print('Best sample')
			print(best.reshape(-1,1))

		return best """
    	

#failure = tester()
#failure.test_run(x = worst_test)
#plot_run(failure.example,'placeholder_2')

# jeff added this part
a=30
b=50
t = datetime.now().strftime("%m%d%Y%H%M%S")
# down to here

failure = tester()
ex_switch = np.array([a,b]) # 1 tu = 0.1 sec
failure.test_run(x = ex_switch)
plot_run(failure.example,'placeholder')

# jeff added this part
	# building a data frame from csv file 
data=pd.read_csv("/home/jeff/Desktop/Test/lowLevelTesting/temp/v1gross.csv", delimiter = ';')
data.columns = [0, 1, 2, 3, 4] 
	# sorting data frame 
data=data.sort_values(by=[3,1,2], ascending=[True,True,True])
data.to_csv("/home/jeff/Desktop/Test/lowLevelTesting/logs/LoLev_v1_"+str(a)+"_"+str(b)+"_"+str(t)+".csv", index = False, header=False, sep = ';')
# down to here 