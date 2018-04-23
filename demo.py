#!/usr/bin/env python3

import os, sys, math, argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

from scenes import Square, Circular, TMaze, Triangular
from agent import Agent2D as Agent


#
# Simulation & Visualzation Setup
#
live_plot = False
live_plot_ticks = 1000
test_scene_boundaries = True

# duration of the simulation
Tmax = 100000

# lists to keep track of the agent position
Xs = []
Ys = []

#
# Particles and particle behavior
#

# The particles are simply a list of coordinates, i.e. their center regions.
# We initialize N particles mostly to avoid re-allocation of memory during the
# simulation
N = 1000
c = 0
particles = np.zeros((N, 2))

# minimal and maximal distance of particle interactions, particle plasticity
mindist = 0.2
maxdist = 2.0 * mindist

# memory trace and impact of inter-particle Push/Pull dynamics
mem = 0.8
alpha = 0.02

#
# Additional variables
#

# integration time step (in s). this is only required to retrieve good values
# from the samplers that are used within the Agent class, as this class is also
# used in other simulations where it is necessary to specify real units. Here,
# the value is chosen arbitrarily
dt   = 0.1



#
# The parser will read arguments that are passed to this demo script
#
parser = argparse.ArgumentParser(prog='demo.py', description="closes packing of particles with minimal distance")
parser.add_argument('--live-plot', default=live_plot, action='store_true')
parser.add_argument('--TMax', type=int, default=Tmax, help='Maximal duration of the simulation')
parser.add_argument('--seed', type=int, default=-1, help='Seed for the random number generator')
parser.add_argument('--mindist', type=float, default=mindist, help='Minimal distance for Push-Pull interactions')
parser.add_argument('--maxdist', type=float, default=maxdist, help='Maximal distance for Push-Pull interactions')
parser.add_argument('--mem', type=float, default=mem, help="Memory trace plasticity in (0,1)")
parser.add_argument('--alpha', type=float, default=alpha, help="Push/Pull interaction strength")
parser.add_argument('scene', help="The maze to simulate. One of: Square, Circular, TMaze, Triangular")
parser.add_argument('filename', help="Filename of final figure")
args = parser.parse_args()


# read out the variables from the parser
live_plot = args.live_plot
Tmax = args.TMax
mindist = args.mindist
maxdist = args.maxdist
mem = args.mem
alpha = args.alpha

# setup the agent and scene
agent = Agent()
s = args.scene.lower()
if s == 'square':
    scene = Square()
elif s == 'circular':
    scene = Circular()
elif s == 'tmaze':
    scene = TMaze()
elif s == 'triangular':
    scene = Triangular()
else:
    print("Unknown scene '{}'".format(args.scene))
    sys.exit()

# seutp random number generator
if not (args.seed == -1):
    np.random.seed(args.seed)


# helper function to prepare plotting and avoiding duplicate code
def prepare_plot():
    fig = plt.figure()
    ax0 = plt.subplot2grid((1,1), (0,0))
    ax0.axis('equal')
    ax0.autoscale(True)

    # get a patch for the scene to render nicely
    scenepatch = scene.getScenePatch(linestyle='solid', edgecolor='black', facecolor='none', lw=2)
    ax0.add_patch(scenepatch)

    return fig, ax0

# setup plotting if necessary
if live_plot:
    plt.ion()
    fig, ax0 = prepare_plot()

# tick setup
t = 0
max_ticks = math.ceil(Tmax / dt)



# simulation main loop
while t < max_ticks:

    # iterate the agent. this will move the agent within the scene
    agent.iter(dt, scene)
    # append the new location of the agent to the list of X and Y coordinates
    Xs.append(agent.X[0])
    Ys.append(agent.X[1])

    # if there's no particle yet, initialize the first one. Otherwise, we would
    # like to update the particles
    if c == 0:
        particles[c, :] = agent.X[0:2]
        c += 1
    else:
        # compute the difference between particles and input
        d = np.sqrt(np.sum((particles[0:c, :] - agent.X[0:2])**2.0, axis=1))

        # select all the particles that are within the minimal distance
        r = []
        for i in range(d.size):
            if d[i] <= mindist:
                r.append(i)

        # if we have not found anything suitable, we simply create a novel
        # particle
        if len(r) == 0:
            particles[c, :] = agent.X[0:2]
            r = [c]
            c += 1

        # now we need to compute the interactions between particles. first,
        # we'll find the index of the winner, i.e. closest particle
        w = r[0]
        for i in range(1, len(r)):
            if d[r[i]] < d[w]:
                w = r[i]

        # now compute the particle interactions, but do not move the winner
        # (it's the winner for a reason)
        Pull = np.zeros((len(r), 2))
        Push = np.zeros((len(r), 2))

        for i in range(len(r)):

            # accidentally selected the winner? don't change anything
            if w == r[i]:
                continue

            # everyone else has local interactions with the winner, and with all
            # other particles
            for j in range(len(r)):
                if i == j:
                    continue

                v = particles[r[j], :] - particles[r[i], :]
                dist = np.sqrt(np.sum(v**2))
                v /= np.linalg.norm(v)

                if dist <= mindist:
                    Push[i, :] += dist * v
                elif dist <= maxdist:
                    Pull[i, :] += dist * v

        # update according to push/pull forces
        for i in range(len(r)):
            if r[i] == w:
                continue

            Pnew = particles[r[i], :] + alpha * Pull[i, :] - 5.0 * alpha * Push[i, :]
            Pold = particles[r[i], :]

            # test if we can move the particle to this location
            tmp = mem * Pold + (1.0 - mem) * Pnew
            if test_scene_boundaries:
                if scene.isValidMove(np.array([Pold[0], Pold[1], 0.0]), np.array([tmp[0], tmp[1], 0.0])):
                    particles[r[i], :] = tmp
            else:
                particles[r[i], :] = tmp


    # in case live-plotting is enabled, setup or plot
    if live_plot:
        if t == 0:
            # agent_pos_plot, = ax0.plot(Xs, Ys)
            particle_plot, = ax0.plot(particles[0:c, 0], particles[0:c, 1], 'o', color='red')
        elif t % live_plot_ticks == 0 or t == max_ticks:
            # agent_pos_plot.set_data(Xs, Ys)
            particle_plot.set_data(particles[0:c, 0], particles[0:c, 1])
            ax0.set_title('{}'.format(t * dt))
            ax0.set_xlim([-1.2, 1.2])
            ax0.set_ylim([-1.2, 1.2])
            ax0.relim()
            ax0.autoscale_view()
            fig.canvas.update()
            fig.canvas.flush_events()

    t += 1
    if t % 100 == 0:
        print(t / 10)


# turn off interactive mode of matplotlib or prepare the plot for visualization
if live_plot:
    plt.ioff()
else:
    fig, ax0 = prepare_plot()
    particle_plot, = ax0.plot(particles[0:c, 0], particles[0:c, 1], 'o', color='#4b9dda')
    ax0.set_xlim([-1.2, 1.2])
    ax0.set_ylim([-1.2, 1.2])
    plt.axis('off')

plt.savefig(args.filename, bbox_inches='tight')
plt.show()



