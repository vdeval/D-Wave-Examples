# D-Wave-Examples
D-Wave example applications taken from D-Wave documentation
## Purpose
This repository contains a set of examples extracted from D-Wave documentation, each one encoding the solution of an optimization problem. Each problem is described in this README file:
1. Problem Description
1. Mathematical formulation of objective function and constraints
1. D-Wave workflow: which model, which solver, any pre processing, any post processing
1. Specific notes, if any.
## Bin Packing
### Problem description
A set of **items**, each one with a specific **weight**, has to be packed in a collection on **bins**, each one with a specific **capacity**. The minimum set of bins has to be used.
### Problem formulation
We represent the problem as a **Constrained Quadratic Model**:
1. Each bin **b<sub>j</sub>** is associated to a binery variable **bin_used_\<j\>** indicating that bin b<sub>j</sub> is in use.
1. To minimize the number of used bins is to minimize the **sum of bin_used_\<j\> variables with value 1**.
1. Each item can go into only one bin:
    1. We use the binary variable **x<sub>i,j</sub>** to indicate that item **i** is in bin **j**
    1. The constraints can be expressed stating that, for each item i, the **sum of x<sub>i,j</sub> over j shall be 1**.
1. Each bin has limited capacity:
    1. The **sum of x<sub>i,j</sub> over i shall be less or equal to the bin j capacity**.
### Problem workflow
1. We represent the problem using a **Constrained Quadratic Model**.
1. We use the **LeapHybridCQMSampler** as solver.
### Notes
1. The problem will be configured with:
    1. 20 items with weight randomly selected from 10 to 20.
    1. 5 bins of capacity 100.
    1. Hybrid solver time limit set to 10 seconds.