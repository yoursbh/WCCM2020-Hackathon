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
      - 3.2: done !
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
INPUT_DATA = read_file("input.data")
REF_DATA = read_file("result.data")



#!------------------------------------------------------------------------------
#!                                    FUNCTIONS
#!------------------------------------------------------------------------------
def question3_1():
    pop_all = Population(INPUT_DATA[:, :2], INPUT_DATA[:, 2],
                         INPUT_DATA[:, 3:5], INPUT_DATA[:, 5])
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
        #   pop_all.time, pop_all.total_sick, pop_all.total_health))

    # plot contamination history and save it to disk
    pop_all.plot_history(
        title="Microscopic simulation WITHOUT mask",
        show=False,
        save=True,
        filename="DEFRUA_without_mask.png")
    # save data to disk for comparaison
    pop_all.save_to_json("without_mask.json")
    return pop_all


def question3_2():
    number_of_mask = 1000
    mask = np.zeros([INPUT_DATA.shape[0], 1])
    mask[:number_of_mask] = 50
    pop = Population(INPUT_DATA[:, :2], INPUT_DATA[:, 2],
                     INPUT_DATA[:, 3:5], INPUT_DATA[:, 5],
                     mask=mask)
    bound_square = Boundary([[-1, -1], [-1, 1], [1, -1], [1, 1]])

    for _ in range(STEPS):
        pop.X = update_position(pop.X, pop.V, TIME_STEP)
        pop.X = check_boundary(pop.X, bound_square)
        pop.distance = get_distance(pop.X, )
        
        pop.contact = get_contact(pop.distance, pop.R_sum)
        pop.contact, pop.mask = check_mask(pop.contact, pop.mask)
        
        pop.state = get_contamination(pop.contact, pop.state)
        pop.time = _ * TIME_STEP
        pop.update_statistic()
        pop.save_to_history()
        #! Uncomment the following 2 lines if you want to check the result, but
        #! this will REDUCE PERFORMANCE !
        # print("Time {:.3f}: Sick = {}, Health = {}".format(
        #    pop.time, pop.total_sick, pop.total_health))

    # show contamination history and save it to disk
    pop.plot_history(
        title="Microscopic simulation WITH mask",
        show=False,
        save=True,
        filename="DEFRUA_with_mask.png")
    # save data to disk for comparaison
    pop.save_to_json("with_mask_{}.json".format(number_of_mask))
    return pop



#!------------------------------------------------------------------------------
#!                                     TESTING
#!------------------------------------------------------------------------------
if __name__ == "__main__":
    print("----- Welcome to team DEFRUA -----")

    ## Question 3.1
    print("Microscopic simulation processing without masks ...")
    TIK = time.time()
    question3_1()
    TOK = time.time()
    print("Microscopic simulation finised in: {}s".format(TOK - TIK))

    ## Question 3.2
    print("\nMicroscopic simulation processing with masks ...")
    TIK = time.time()
    question3_2()
    TOK = time.time()
    print("Microscopic simulation finised in: {}s".format(TOK - TIK))
    
    ## Compare the effect of mask
    datafile_list = ("with_mask_0.json", "with_mask_500.json",
                     "with_mask_1000.json", "with_mask_1500.json")
    plot_with_without_mask(
        datafile_list,
        show=False,
        save=True,
        filename="DEFRUA_with_without_mask.png")
