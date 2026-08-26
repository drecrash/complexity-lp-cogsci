import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools
import numpy as np
from graphgenerator import GraphGenerator
import sys
from collections import deque
from scipy.optimize import fsolve
import os
import json

generator = GraphGenerator()

ER_P = 0.005
ER_N = 1000
BA_M = 10

IMMUNIZATION_RATE = 0

INFECTION_RATE = 0.01
RECOVERY_RATE = 0.01

LOG_FILE = "./log.json"

def draw_graph(G,title=None, color_map=False):
    layout_ = nx.spring_layout(G, k=0.5, iterations=50)

    node_colors = []
    if color_map:
        for node in G.nodes():
            if G.nodes[node]["infected"]:
                node_colors.append("red")
            elif G.nodes[node]["recovered"]:
                node_colors.append("orange")
            else:
                node_colors.append("green")

    nx.draw(G, layout_, node_color=node_colors, node_size=10)

    if title:
        plt.title(title)

    plt.show()

def si_model(G, immunization=False):

    nodes = list(G.nodes())

    patient_zero = nodes[0]

    visited = set()
    queue = deque()

    queue.append(patient_zero)

    while queue:
        victim = queue.popleft()
        
        G.nodes[victim]["infected"] = True

        for node in G.neighbors(victim):
            if node not in visited:
                visited.add(node)

                if immunization and G.nodes[node]["immune"]:
                    continue
                queue.append(node)

    return G

def dice_roll(p):
    rng_= random.uniform(0,1)
    return rng_ <= p
def immunize(G, p_imm):


    for node in G.nodes():

        if (dice_roll(p_imm)):
            G.nodes[node]["immune"] = True
        else:
            G.nodes[node]["immune"] = False

    return G


def get_susceptible(G):
    susceptible = []

    for n in G.nodes():
        if (not G.nodes[n]["infected"]) and (not G.nodes[n]["recovered"]) and (not G.nodes[n]["immune"]):
            susceptible.append(n)

    return susceptible


def log_sir(G):


    susceptible = len(get_susceptible(G))
    infected = len([n for n in G.nodes() if G.nodes[n]["infected"]])
    recovered = len([n for n in G.nodes() if G.nodes[n]["recovered"]])

    new_log = {
        "s": susceptible,
        "i": infected,
        "r": recovered
    }
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([new_log], f)

    else:
        with open(LOG_FILE, "r") as f:
            log = json.load(f)

        log.append(new_log)

        with open(LOG_FILE, "w") as f:
            json.dump(log, f, indent=2)




def sir_model(G, infection_rate, recovery_rate):

    for node in G.nodes():
        G.nodes[node]["immune"] = False
        G.nodes[node]["infected"] = False 
        G.nodes[node]["recovered"] = False

    G = immunize(G, IMMUNIZATION_RATE)


    nodes = list(G.nodes())

    patient_zero = nodes[0]

    G.nodes[patient_zero]["infected"] = True

    currently_infected = [n for n in G.nodes() if G.nodes[n]["infected"]]
    while len(currently_infected) > 0:
        new_infected = set()
        new_recovered = set()

        currently_infected = [n for n in G.nodes() if G.nodes[n]["infected"]]

        susceptible = get_susceptible(G)
        for n in currently_infected:
            for neighbor in G.neighbors(n):
                if neighbor in susceptible:
                    if dice_roll(infection_rate):
                        new_infected.add(neighbor)

            if dice_roll(recovery_rate):
                new_recovered.add(n)


        for n in new_infected:
            G.nodes[n]["infected"] = True
        for n in new_recovered:
            G.nodes[n]["infected"] = False
            G.nodes[n]["recovered"] = True

        log_sir(G)


    return G


def get_infected_fraction(G):
    total_nodes = len(list(G.nodes()))
    infected_count = len([node for node in G.nodes() if G.nodes[node]["infected"]])

    return infected_count/total_nodes

def get_er_critical_immunization(p_conn, N, p_imm):
    def crit_imm_eq(q):
        return q - (1 - np.exp(-(N-1)*p_conn*(1-p_imm)*q))


    return fsolve(crit_imm_eq, 0.5)

def get_reproductive_number(G, infection_rate, recovery_rate):
    lambda_ = -np.log(1-infection_rate)
    sigma_ = -np.log(1-recovery_rate)
    spreading_rate = lambda_/sigma_

    avg_deg = sum([d for n, d in G.degree()])/len(G.nodes())

    r = spreading_rate*avg_deg

    return r


def plot_log(title=""):
    with open(LOG_FILE, "r") as f:
        log = json.load(f)

    timestamps = range(len(log))

    infected_rates = [t["i"] for t in log]
    rec_rates = [t["r"] for t in log]
    sus_rates = [t["s"] for t in log]

    plt.plot(timestamps, infected_rates,label="Infected")
    plt.plot(timestamps, rec_rates,label="Recovered")
    plt.plot(timestamps, sus_rates,label="Susceptible")
    plt.title(title)

    plt.xlabel("Time")
    plt.ylabel("Rates")

    plt.legend()
    plt.show()

def er_experiments():

    G = generator.create_er_graph(p=ER_P, attr = {"infected": False})
    # immunize(G,IMMUNIZATION_RATE)
    # G = si_model(G, immunization=True)
    # print(get_infected_fraction(G))
    # print(get_er_critical_immunization(ER_P, ER_N, IMMUNIZATION_RATE))
    # draw_graph(G,color_map=["infected"])

    G = sir_model(G, INFECTION_RATE, RECOVERY_RATE)
    print(get_infected_fraction(G))
    print(get_reproductive_number(G, INFECTION_RATE, RECOVERY_RATE))
    draw_graph(G,color_map=True)

def ba_experiments():
    G = generator.create_ba_graph(BA_M)
    G = sir_model(G, INFECTION_RATE, RECOVERY_RATE)
    print(get_infected_fraction(G))
    print(get_reproductive_number(G, INFECTION_RATE, RECOVERY_RATE))
    draw_graph(G,color_map=True)

er_experiments()
plot_log()




