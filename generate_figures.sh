#!/bin/sh

# this script runs several simulations
./demo.py --hide-final-plot --Tmax 50000 square output/square_50000.svg
./demo.py --hide-final-plot --Tmax 50000 circular output/circular_50000.svg
./demo.py --hide-final-plot --Tmax 50000 triangular output/triangular_50000.svg

# get some consecutive images for TMaze
# set the seed to get real consecutive images
./demo.py --hide-final-plot --seed 1337 --Tmax 1000 tmaze output/tmaze_1000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 20000 tmaze output/tmaze_20000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 100000 tmaze output/tmaze_100000.svg
