# D-Wave-Examples
D-Wave example applications taken from D-Wave documentation
## Purpose
This repository contains a set of examples extracted from D-Wave documentation, each one encoding the solution of an optimization problem. Each problem is described in this README file:
1. Problem Description
1. Mathematical formulation of objective and constraints
1. D-Wave workflow: which model, which solver, any pre processing, any post processing
1. Specific notes, if any.
## Bin Packing
A set of **items**, each one with a specific **weight**, has to be packed in a collection on **bins**, each one with a specific **capacity**. The minimum set of bins has to be used.
### Problem description
We represent the problem as a **Constrained QUadratic Model**:
1. Each bin **b<sub>j</sub>** is associated to a binery variable **bin_used_\<j\>** indicating that bin b<sub>j</sub> is in use.
1. To minimize the number of used bins is to minimize the sum of bin_used_\<j\> variables with value 1

### Problem formulation
### Problem workflow