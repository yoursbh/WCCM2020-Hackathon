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

import csv
import math
import random
import pandas as pd
import numpy as np

# Define constants
lowerBounX = -1
lowerBounY = -1
upperBounX = +1
upperBounY = +1
lenBounX   = 2
lenBounY   = 2
maxMaskUse = 50
nPoints    = 0


# Main program++++++++++++++++++++++++++++++++++++++++++++
def main():
  # Welcome
  print("Welcome to the solution of Challenge number 1")
  
  # Input data
  deltaT    = 0.005
  totalTime = 1.2
  ntimestep = int(totalTime/deltaT)
  pointList = np.loadtxt("input.data")
  nPoints   = len(pointList)
  
  # Initialize variables
  count        = 0
  numIllPoint  = 0
  numFinePoint = 0
  illPointList      = []
  finePointList     = []
  tempFinePointList = []

  # Preparation: classify ill and fine points
  for id in range(nPoints):
      # Collect all ill points
      if (pointList[id][5] == 1):
        illPointList.append(pointList[id][:])
      else:
        finePointList.append(pointList[id][:])

  print(len(illPointList))

  # Initialize a loop over time <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  for time in range(ntimestep):
    # Marker of a new time step
    print("+++++++++++++++++++++++++++++++++++++++++++++++")

    # Fist step: update position for only ill points
    numIllPoint = len(illPointList)
    print("Time step " + str(time) + ": " + "n.o. ill cases = " + str(numIllPoint))
    for id1 in range(numIllPoint):
      update_point_position(illPointList, id1, deltaT)

    # Second step: update position for healthy points
    numFinePoint = len(finePointList)
    print("Time step " + str(time) + ": " + "n.o. fine cases = " + str(numFinePoint))
    for id2 in range(numFinePoint):
      update_point_position(finePointList, id2, deltaT)

    # Third step: check near-contact between fine and ill points
    for id1 in range(numIllPoint):
      for id2 in range(numFinePoint):
        # Update health condition
        if (finePointList[id2][5] == 0):
          contaminate_point(illPointList, id1, finePointList, id2)

    # Fourth step: update ill and fine lists
    tempFinePointList = finePointList
    finePointList = []
    for id2 in range(numFinePoint):
      if (tempFinePointList[id2][5] == 1):
        illPointList.append(tempFinePointList[id2][:])
      else:
        finePointList.append(tempFinePointList[id2][:])

    # # Export data++++++++++++++++++++++++++++++++++++++++++++++++
    # # Write ill points
    # fileName = "./Task01/IllPoint_TimeStep_" + str(time)
    # with open(fileName,"w+") as my_csv:
    #   csvWriter = csv.writer(my_csv,delimiter = ' ')
    #   csvWriter.writerows(illPointList)

    # # Write fine points
    # fileName = "./Task01/FinePoint_TimeStep_" + str(time)
    # with open(fileName,"w+") as my_csv:
    #   csvWriter = csv.writer(my_csv,delimiter = ' ')
    #   csvWriter.writerows(finePointList)
	  # # Export data++++++++++++++++++++++++++++++++++++++++++++++++
  # End a loop over time <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


  # Print total number of infected cases <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
  print("***********************************************")
  numIllPoint = len(illPointList)
  numFinePoint = len(finePointList)
  print("Final number of ill: " + str(numIllPoint))
  print("Final number of fine: " + str(numFinePoint))
  # End print number of infected cases <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# Check contaminate by near contact with ill points
def contaminate_point(illPointList, id1, finePointList, id2):
  if (check_near_contact(illPointList, id1, finePointList, id2)):
    finePointList[id2][5] = 1


# Check clashing between two points 
def check_near_contact(illPointList, id1, finePointList, id2):
  # Radius of each point
  firstPointRadius = illPointList[id1][4]
  secondPointRadius = finePointList[id2][4]

  # Distance between the given two points 
  distance = compute_distance(illPointList, id1, finePointList, id2)

  # Sum of radius
  sumRadius = firstPointRadius + secondPointRadius;

  # Check clashing
  if (distance < sumRadius):
    return True
  else:
    return False


# Compute distance between two points 
def compute_distance(illPointList, id1, finePointList, id2):
  # Position X and Y of points
  firstPosX = illPointList[id1][0]
  firstPosY = illPointList[id1][1]
  secondPosX = finePointList[id2][0]
  secondPosY = finePointList[id2][1]

  # Distance
  distance = math.sqrt((firstPosX-secondPosX)**2+
                       (firstPosY-secondPosY)**2)

  return distance
  

# Check clashing of a point with boundary 
def check_clashing_boundary(tempX, tempY):
  # Default not clashing
  clashingX = 0
  clashingY = 0

  # Position X and Y of point
  posX = tempX
  posY = tempY

  # Check clashing with which boundary
  if (posX < lowerBounX):
    clashingX = 1

  if (posX > upperBounX):
    clashingX = 2

  if (posY < lowerBounY):
    clashingY = 1

  if (posY > upperBounY):
    clashingY = 2

  # Return type of clashing
  return (clashingX, clashingY)


# Update position of a point 
def update_point_position(anyPointList, id, deltaT):
  # point data
  posX = anyPointList[id][0]
  posY = anyPointList[id][1]
  velX = anyPointList[id][2]
  velY = anyPointList[id][3]

  # Temporary position
  tempX = posX + velX * deltaT
  tempY = posY + velY * deltaT

  # Check clashing with boundary
  (clashingX, clashingY) = check_clashing_boundary(tempX, tempY)
  if (clashingX !=0) and (clashingY == 0):
    posX = posX - 2 * pow(lowerBounX,clashingX)
    posY = tempY
  elif (clashingX ==0) and (clashingY != 0):
    posX = tempX
    posY = posY - 2 * pow(lowerBounY,clashingY)
  elif (clashingX !=0) and (clashingY != 0):
    posX = posX - 2 * pow(lowerBounX,clashingX)
    posY = posY - 2 * pow(lowerBounY,clashingY)
  else:
    posX = tempX
    posY = tempY

  # Update poin position
  anyPointList[id][0] = posX
  anyPointList[id][1] = posY

# Execute main program+++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
  main()
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++