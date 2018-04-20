#!/usr/bin/env python3

import os, sys
import numpy as np
import matplotlib.pyplot as plt

from scenes import Square, Circular
from agent import Agent2D as Agent

agent = Agent()
scene = Square()


dt   = 0.1  # in s
Tmax = 10000 # maximal simulation time (in ticks)
t    = 0


Xs = []
Ys = []

def prepare_plot():
    fig = plt.figure()
    ax0 = plt.subplot2grid((1,1), (0,0))
    ax0.set_xlim([-1, 1])
    ax0.set_ylim([-1, 1])
    return fig, ax0

do_live_plot = True
if do_live_plot:
    plt.ion()
    fig, ax0 = prepare_plot()

while t < Tmax:
    agent.iter(dt, scene)

    Xs.append(agent.X[0])
    Ys.append(agent.X[1])

    if do_live_plot:
        if t == 0:
            agent_pos_plot, = ax0.plot(Xs, Ys)
        else:
            agent_pos_plot.set_data(Xs, Ys)
            # ax0.draw_artist(ax0.patch)
            # ax0.draw_artist(agent_pos_plot)

            ax0.set_title('{}'.format(t * dt))
            fig.canvas.update()
            fig.canvas.flush_events()

    t += 1
    print(t)

if do_live_plot:
    plt.ioff()
else:
    fig, ax0 = prepare_plot()
    ax0.plot(Xs, Ys)

plt.show()


