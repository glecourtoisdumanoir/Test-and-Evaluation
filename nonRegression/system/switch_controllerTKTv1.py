# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 14:20:35 2020

@author: prith
"""

import numpy as np
from DynSys import dynsys 
import matplotlib.pyplot as plt
import loggerTKTv1 as logger
from datetime import datetime


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
        self.goal_semantics = ['Middle','Top','Right','Bottom','Left']
        
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
            # jeff added this part
            logger.logger.info('PetterExample;movingTo{};B;{};a'.format(self.goal_semantics[i],self.counter))
            # down to here
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
                    # jeff added this part
                    logger.logger.info('PetterExample;movingTo{};E;{};a'.format(self.goal_semantics[i],self.counter))
                    # down to here
                    break
            if self.counter == self.t_switch1 or self.counter == self.t_switch2:
                break
            # jeff added this part
            logger.logger.info('PetterExample;movingTo{};E;{};a'.format(self.goal_semantics[i],self.counter))
            # down to here

    def surveil(self, t_switch1 = 53, t_switch2 = 65):
        # jeff added this part 
        logger.logger.info('0;1;2;3;4')    
        self.t_switch1 = t_switch1
        logger.logger.info('PetterExample;switch;B;{};a'.format(self.t_switch1))
        self.t_switch2 = t_switch2
        logger.logger.info('PetterExample;switch;B;{};a'.format(self.t_switch2))
        # down to here
        self.goal_seq = (1,3,1,3)
        self.simulate()
        self.goal_seq = (2,4,2,4)
        # jeff added this part
        logger.logger.info('PetterExample;switch;E;{};a'.format(self.counter))
        # down to here
        self.simulate()
        self.goal_seq = (1,3,1,3)
        # jeff added this part
        logger.logger.info('PetterExample;switch;E;{};a'.format(self.counter))
        # down to here
        self.simulate()   
        
#agent = dynsys(x = np.array([[2.5,0.0,0.0,0.0]]).transpose(),dt=0.01)
#example = switch_ctrl(sys = agent,
#                      params = np.array([[5,0,5,0],[0,5,0,5]]),
#                      t_switch = 1000,goal_seq = (2,1)) 
#example.simulate()
        
    