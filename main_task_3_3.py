''' WCCM-Junio Hackathon
Group: DEFRUA
Members:
    Hao Bai, hao.bai@insa-rouen.fr
    Christoph Eckert, eckert@irz.uni-hannover.de
    Koliesnikova Daria, koliesnikova.daria@gmail.com
    Mahshid Sharifi, mahshid.sharifi@outlook.com
    Cong Uy, cong-uy.nguyen@utc.fr
    Kumar Paras, paras.kumar@fau.de
---------------------------------------------------------
ONGOING TASK: question 3.1

TODO LIST:
  - ...
  - ...
  - ...
  '''


import math
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


maxMaskUse = 50
nPoints    = 0



def main():
  # Welcome
  print("Welcome to the solution of Challenge number 1")
  
  # Input data
  deltaT    = 0.1
  totalTime = 1.2
  ntimestep = 10 #int(totalTime/deltaT)
  pointList = np.loadtxt("input.data")
  nPoints   = len(pointList)
  
  # Define constants
  t = np.linspace(-1,1,9)#constant

  t = np.pi*t

  # Define the domain
  X = np.cos(t+np.pi/4) + (1/20.)*np.cos(5*t+np.pi/4)
  Y = np.sin(t+np.pi/4) - (1/20.)*np.sin(5*t+np.pi/4)

  # Plot the domain
  plt.plot(X,Y)
  plt.savefig('country.png')
  plt.close() 

  xbar = np.array([-0.05,-0.5,0.5,0.55,0.9,-0.6])
  ybar = np.array([0.5,-0.4,-0.2,-0.7,0.5,0.25])

  posX = pointList[:,0]
  posY = pointList[:,1]

  A = np.zeros(len(posX))
  B = np.zeros(len(posX))
  F = np.zeros(len(posX))

  # The initial ccondition
  for i in range(len(posX)):
    for j in range(len(xbar)):
      A[i] = A[i] + np.exp(((-posX[i]+xbar[j])**2)/0.01)*np.exp(((-posY[i]+ybar[j])**2)/0.01)

  for i in range(len(posX)):
    B[i] = A[i] - np.min(A)

  for i in range(len(posX)):  
    F[i] = B[i]/np.max(B)

  np.savetxt("value_inital_condition.dat",np.array([A,B,F]).T)
 

# Execute main program+++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
  main()