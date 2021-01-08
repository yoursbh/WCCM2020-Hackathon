''' WCCM-Junio Hackathon
    Group: DEFRUA
    Contact: hao.bai@insa-rouen.fr
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
# external imports
import time
import numpy as np
from pathlib import Path
# internal imports
from publics_hao import *


#!------------------------------------------------------------------------------
#!                                 GLOBAL VARIABLES
#!------------------------------------------------------------------------------
TIME_STEP = 0.005 # unit: s
STEPS = int((1.245 - 0)/TIME_STEP)



#!------------------------------------------------------------------------------
#!                                     CLASSES
#!------------------------------------------------------------------------------


#!------------------------------------------------------------------------------
#!                                    FUNCTIONS
#!------------------------------------------------------------------------------

  

#!------------------------------------------------------------------------------
#!                                     TESTING
#!------------------------------------------------------------------------------
def main():
  TIK = time.time()


  inputdata = read_file("input.data")
  outputdata = read_file("result.data")
  pop_all = Population(inputdata[:,:2], inputdata[:,2], inputdata[:,3:5], inputdata[:,5])
  test = inputdata[:,5]
  print("INIT:", len(test), len(test[test==1]))
  pop_all.show_statistic()
  
  for t in range(STEPS)[:10]:
    pop_all.X = update_position(pop_all.X, pop_all.V, TIME_STEP)

    pop_all.distance = get_distance(pop_all.X,)
    pop_all.contact = get_contact(pop_all.distance, pop_all.R_sum)
    #print(pop_all.contact)
    pop_all.state = get_contamination(pop_all.contact, pop_all.state)
    pop_all.time = pop_all.time + TIME_STEP
    pop_all.show_statistic()
  
  TOK = time.time()
  print("Finished: {}s".format(TOK-TIK))
  

if __name__ == "__main__":
  main()
