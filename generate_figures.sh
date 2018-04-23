#!/bin/sh

# set the seed to get real consecutive images

# this script runs several simulations
./demo.py --hide-final-plot --seed 1337 --Tmax 1000 square output/square_01000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 5000 square output/square_05000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 10000 square output/square_10000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 20000 square output/square_20000.svg

./demo.py --hide-final-plot --seed 1337 --Tmax 1000 circular output/circular_01000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 5000 circular output/circular_05000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 10000 circular output/circular_10000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 20000 circular output/circular_20000.svg

./demo.py --hide-final-plot --seed 1337 --Tmax 1000 triangular output/triangular_01000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 5000 triangular output/triangular_05000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 10000 triangular output/triangular_10000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 20000 triangular output/triangular_20000.svg

# get some consecutive images for TMaze
#./demo.py --hide-final-plot --seed 1337 --Tmax 1000 tmaze output/tmaze_1000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 5000 tmaze output/tmaze_5000.svg
./demo.py --hide-final-plot --seed 1337 --Tmax 10000 tmaze output/tmaze_10000.svg
#./demo.py --hide-final-plot --seed 1337 --Tmax 20000 tmaze output/tmaze_20000.svg
