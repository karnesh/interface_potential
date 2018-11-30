# Interface Potential
 
## Purpose
This python script generates volume histogram by binning the spring positions from umbrella sampling simulation of LAMMPS. The cumulative integration of histogram provides the free energy.

## Dependencies
* Numpy
* Scipy
* Pandas
* os

## Input
This script takes instantenous values of height (*H*) of the simulation box and force exerted by fluid particles on the wall in direction normal to the wall. The molecular dynamic simulations are carried out using LAMMPS. We collect data after every 20 steps. 

## Method
The height (*H*) of simulation box is binned and average force is calculated for the bin. The average force is then corrected for saturation pressure to compute properties at liquid-vapor coexistence conditions. Cumulative integration of corrected force provides us with free energy.
