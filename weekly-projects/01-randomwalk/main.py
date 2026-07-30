import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Problem encountered: few extreme Cauchy values stretch the x axis extremely wide
# Solution: truncate to +- some limit

NUM_TRIALS = 50000
process = "cauchy"

def trial(step_size=1000, start_pos=(0,0)):
    path = [start_pos] # Stores tuples of (x,y) coordinates

    for i in range(1,step_size+1):
        old_pos = path[i-1]

        if (process=="standard"):
            increment=random.randint(-100,100)
        elif (process=="cauchy"):
            increment=np.random.standard_cauchy(1)[0]
        new_pos = (old_pos[0]+1,old_pos[1]+increment)
        path.append(new_pos)

    return path


def randomwalk():
    trials = []
    for i in range(NUM_TRIALS):
        run = trial()
        trials.append(
            {
                "ID": i,
                "Path": run,
                "Endpoint": run[-1][1]
            }
        )


    df = pd.DataFrame(trials)

    df.to_csv("output.csv")


def create_histogram():

    limit = 10000

    try:
        df = pd.read_csv("output.csv")
    except:
        print("Error: output csv not found")
        return

    end_pos_list = df["Endpoint"].to_list()

    if (process=="cauchy"):
        end_pos_list = [i for i in end_pos_list if i >(-1*limit) and i<limit]

        
    plt.hist(end_pos_list,bins=100)
    #plt.yscale("log")

    plt.show()

#randomwalk()
create_histogram()






    
