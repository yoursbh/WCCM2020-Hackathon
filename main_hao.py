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
    ONGOING TASK: question 3.2

    TODO LIST:
      - 3.1: done !
      - 3.2: Uy
      - 4 : ?
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
TIME_STEP = 0.005  # unit: s
STEPS = int((1.245 - 0) / TIME_STEP)

#!------------------------------------------------------------------------------
#!                                     CLASSES
#!------------------------------------------------------------------------------

#!------------------------------------------------------------------------------
#!                                    FUNCTIONS
#!------------------------------------------------------------------------------




#!------------------------------------------------------------------------------
#!                                     TESTING
#!------------------------------------------------------------------------------
def micro():
    inputdata = read_file("input.data")
    outputdata = read_file("result.data")
    pop_all = Population(inputdata[:, :2], inputdata[:, 2], inputdata[:, 3:5],
                         inputdata[:, 5])
    bound_square = Boundary([[-1, -1], [-1, 1], [1, -1], [1, 1]])
    for _ in range(STEPS):
        pop_all.X = update_position(pop_all.X, pop_all.V, TIME_STEP)
        pop_all.X = check_boundary(pop_all.X, bound_square)
        pop_all.distance = get_distance(pop_all.X, )
        pop_all.contact = get_contact(pop_all.distance, pop_all.R_sum)
        pop_all.state = get_contamination(pop_all.contact, pop_all.state)
        pop_all.time = _ * TIME_STEP
        pop_all.update_statistic()
        pop_all.save_to_history()
        #! Uncomment the following 2 lines if you want to check the result, but  
        #! this will REDUCE PERFORMANCE !
        # print("Time {:.3f}: Sick = {}, Health = {}".format(
        #    pop_all.time, pop_all.total_sick, pop_all.total_health))

    # show contamination history and save it to disk
    pop_all.plot_history(show=False, save=True)

def main():
    pass


if __name__ == "__main__":
    TIK = time.time()
    print("----- Welcome to team DEFRUA -----")
    print("Microscopic simulation processing ...")
    micro()
    TOK = time.time()
    print("Microscopic simulation finised in: {}s".format(TOK - TIK))
