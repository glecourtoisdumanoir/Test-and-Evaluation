# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:20:35 2020

@author: prith
"""

import numpy as np
from DynSys import dynsys 
import matplotlib.pyplot as plt

class switch_ctrl:
    def __init__(self,sys = dynsys(),
                 params=np.zeros((dynsys().gmat.shape[1],
                                  dynsys().gmat.shape[0]))):
        """
        goal_seq determines the order in which goals are visited,
        goal_seq = (1,2,3,4) implies that the system is to visit the north,
        east,south,west quadrants in that order.  Each time, the system
        is to visit the central, purple region first before moving to the
        next, desired goal location.  The purple region is denoted by the
        0th column in bmat.  If Ax<b for an appropriate column, then the system
        occupies the appropriate region
        """
        self.system = sys
        self.params = params
        self.A = np.array([
                [1,0,0,0],
                [0,1,0,0],
                [-1,0,0,0],
                [0,-1,0,0]])
        self.bmat = np.array([
                [3,3,5,3,1],
                [3,5,3,1,3],
                [-2,-2,-4,-2,0],
                [-2,-4,-2,0,-2],])
        self.goals = np.array([
                [2.5,2.5,0,0],
                [2.5,4.5,0,0],
                [4.5,2.5,0,0],
                [2.5,0.5,0,0],
                [0.5,2.5,0,0]]).transpose()
        self.counter = 0
        copy = self.system.x
        self.xhist = copy
        self.goal_semantics = ['middle','top','right','bottom','left']
        
    def move_to(self,gindex):
        error = self.goals[:,gindex].reshape(-1,1)-self.system.x
        u = np.dot(self.params,error).reshape(-1,1)
        self.system.update(u)
        
    def simulate(self):
        for i in self.goal_seq:
            mid_check = np.less_equal(
                    np.dot(self.A,self.system.x),self.bmat[:,0].reshape(-1,1))
            if not all(mid_check):
                while not all(mid_check):
                    self.move_to(0)
                    self.counter+=1
                    mid_check = np.less_equal(
                            np.dot(self.A,self.system.x),
                            self.bmat[:,0].reshape(-1,1))
                    copy = self.xhist
                    self.xhist = np.concatenate((copy,self.system.x),axis=1)
            #print('Finished moving to the {} at time step: {}, equivalent to: {} microsec'.format(self.goal_semantics[0],self.counter,int((time.clock()-t0)*1000000)))
            #log.info('Finished moving to the {} at time step: {}'.format(self.goal_semantics[0],self.counter))
            check = np.less_equal(
                    np.dot(self.A,self.system.x),self.bmat[:,i].reshape(-1,1))
            while not all(check):
                self.move_to(i)
                self.counter+=1
                check = np.less_equal(
                        np.dot(self.A,self.system.x),self.bmat[:,i].reshape(-1,1))
                copy = self.xhist
                self.xhist = np.concatenate((copy,self.system.x),axis=1)
                if self.counter == self.t_switch1 or self.counter == self.t_switch2:
                    #print('Switched at {}, equivalent to: {} microsec'.format(self.counter,int((time.clock()-t0)*1000000)))
                    #log.info('Switched at {}'.format(self.counter))
                    break
            if self.counter == self.t_switch1 or self.counter == self.t_switch2:
                break
            #print('Finished moving to the {} at time step: {}, equivalent to: {} microsec'.format(self.goal_semantics[i],self.counter,int((time.clock()-t0)*1000000)))
            #log.info('Finished moving to the {} at time step: {}'.format(self.goal_semantics[i],self.counter))
            
    def surveil(self, t_switch1 = 53, t_switch2 = 65):
        # # create logger with 'spam_application'
        # logger = logging.getLogger('PetterExample')
        # logger.setLevel(logging.DEBUG)
        # # create file handler 
        # fh = logging.FileHandler('/home/jeff/Desktop/PetterExample.log', "w")
        # # create formatter and add it to the handlers
        # formatter = logging.Formatter('%(asctime)s - %(message)s')
        # fh.setFormatter(formatter)
        # # add the handlers to the logger
        # logger.addHandler(fh)

        # Run the sim with current arguments.
        # t0 = time.clock()
        # logger.info('logging B')
        # logger.info('t_switch1 B')
        self.t_switch1 = t_switch1
        # logger.info('t_switch1 E')
        # logger.info('t_switch2 B')
        self.t_switch2 = t_switch2
        # logger.info('t_switch2 E')
        # logger.info('goal_seq 1313 B')
        self.goal_seq = (1,3,1,3)
        # logger.info('goal_seq 1313 E')
        # logger.info('simulate B')
        self.simulate()
        # logger.info('simulate E')
        # logger.info('goal_seq 2424 B')
        self.goal_seq = (2,4,2,4)
        # logger.info('goal_seq 2424 E')
        # logger.info('simulate B')
        self.simulate()
        # logger.info('simulate E')
        # logger.info('goal_seq 1313 B')
        self.goal_seq = (1,3,1,3)
        # logger.info('goal_seq 1313 E')
        # logger.info('simulate B')
        self.simulate()
        # logger.info('simulate E')
        # logger.info('logging E')
        
#agent = dynsys(x = np.array([[2.5,0.0,0.0,0.0]]).transpose(),dt=0.01)
#example = switch_ctrl(sys = agent,
#                      params = np.array([[5,0,5,0],[0,5,0,5]]),
#                      t_switch = 1000,goal_seq = (2,1)) 
#example.simulate()
        
    