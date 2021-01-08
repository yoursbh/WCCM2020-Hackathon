#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Definition of class
    Matrix version
'''

import numpy as np
from matplotlib import pyplot as plt
from copy import deepcopy
from scipy.spatial import distance


#!------------------------------------------------------------------------------
#!                                     CLASSES
#!------------------------------------------------------------------------------
class Population(object):
    ''' :class:`Population` defines a group of population inside a country
    '''

    def __init__(self, position, radius, velocity, health_state):
        '''
        Creates a new :class:`Population` for populations.

        Parameters
        ----------
          position: 2D array
          radius: 1D array
          velocity: 2D array
          health_state: 1D array
        
        Returns
        -------
        A population object.
        '''
        self.X = np.array(position)
        self.R = np.reshape(radius, (-1,1))
        self.V = np.array(velocity)
        self.state = np.reshape(health_state, (-1,1))
        # Other attributes
        self.time = 0 # counter of propagation step (time step)
        self.mask = np.array([]) # reserved for the following questions
        self.contact = np.array([])
        self.distance = np.array([])
        self.hist_time, self.hist_sick, self.hist_health = [], [], []


    def __repr__(self):
        line1 = "A {} including {} persons of {} dimensions:\n{}".format(
            type(self).__name__, self.shape[0], self.shape[1], self.X)
        return line1

    def __len__(self):
        return self.NP

    @property
    def NP(self):
        return self.shape[0]

    @property
    def shape(self):
        return self.X.shape

    @property
    def R(self):
      return self._R
    
    @R.setter
    def R(self, array):
      self._R = array
      # sum up the radius between every two person
      _ = np.tile(self._R, self.NP)
      self.R_sum = _ + _.transpose() # an NP*NP array
      np.fill_diagonal(self.R_sum, 1) # ensure everyone keeps its health state

    @property
    def X_last(self):
        return self._X_last

    @X_last.setter
    def X_last(self, array):
        self._X_last = deepcopy(array)

    # ----------------------------- Public methods -----------------------------
    def update_statistic(self):
        self.total_sick = self.state[self.state >= 1].size
        self.total_health = self.NP - self.total_sick
    
    def save_to_history(self):
        self.hist_time.append(self.time)
        self.hist_sick.append(self.total_sick)
        self.hist_health.append(self.total_health)

    def plot_history(self, show=True, save=True):
        fig, axis = plt.subplots()
        axis.plot(self.hist_time, self.hist_sick, ".", label="Sick")
        axis.plot(self.hist_time, self.hist_health, ".", label="Health")
        axis.legend()
        axis.set(xlabel="Time (s)", ylabel="Number of people")
        if show == True:
            plt.show()
        if save == True:
            plt.savefig("DEFRUA_micro_history.png")


class Boundary(object):
    ''' :class:`Boundary` defines boundary of country and the method to travel
        across boundary

        Parameters
        ----------
          geo_limit: N*2 array
          douane_policy: str
    '''

    def __init__(self, geo_limit, douane_policy='periodic'):
      self.geo_limit = np.array(geo_limit)
      self.douane_policy = douane_policy
      self.x_min = np.min(self.geo_limit[:,0], )
      self.x_max = np.max(self.geo_limit[:,0], )
      self.y_min = np.min(self.geo_limit[:,1], )
      self.y_max = np.max(self.geo_limit[:,1], )
      self.x_distance = abs(self.x_max - self.x_min)
      self.y_distance = abs(self.y_max - self.y_min)



#!------------------------------------------------------------------------------
#!                                    FUNCTIONS
#!------------------------------------------------------------------------------
def read_file(filename, skiprows=2, *args, **kwargs):
    return np.loadtxt(filename, skiprows=skiprows, *args, **kwargs)

def update_position(position, velocity, timestep):
    return position + velocity * timestep

def get_distance(position,):
    return distance.cdist(position, position, 'euclidean')

def get_contact(distance, redius_sum):
    return distance <= redius_sum

def get_contamination(contact, health_state):
    return np.matmul(contact, health_state)

def check_boundary(pos, bound):
    ''' Hao: may be still improved in future'''
    # x
    flag = pos[:,0] >= bound.x_max
    pos[flag,0] = pos[flag,0] - bound.x_distance
    flag = pos[:,0] <= bound.x_min
    pos[flag,0] = pos[flag,0] + bound.x_distance
    # y
    flag = pos[:,1] >= bound.y_max
    pos[flag,1] = pos[flag,1] - bound.y_distance
    flag = pos[:,1] <= bound.y_min
    pos[flag,1] = pos[flag,1] + bound.y_distance
    return pos



#!------------------------------------------------------------------------------
#!                                     TESTING
#!------------------------------------------------------------------------------
def main():
    b = Boundary([[-1, -1], [-1, 1], [1, -1], [1, 1]])
    print(b.x_min, b.x_max, b.y_min, b.y_max)


#  --- Test population

if __name__ == '__main__':
    main()
