# D-Wave-Examples
D-Wave example applications taken from D-Wave documentation
## Purpose
This repository contains a set of examples extracted from D-Wave documentation, each one encoding the solution of an optimization problem. Each problem is described in this README file, with the following structure:
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
1. In order to test the problem, it will be configured with:
    1. 5 items with weight [11, 12, 13, 14, 15].
    1. 5 bins of capacity [12, 15, 28, 37].
    1. Hybrid solver time limit set to 10 seconds.
    1. Correct solution is:
        1. 2 bins used
        1. Bin with capacity 28 containing [13, 15]
        1. Bin with capacity 37 containing [11, 12, 14]
## Stock Sales Strategy
### Problem description
You have some number of **shares** that you want to sell in daily blocks over a **defined interval of days**. Each sale of shares affects the **market price** of the stock. The goal is to find the **optimal number of shares to sell per day** to **maximize revenue from the total sales**.
### Problem formulation
We represent the problem as a **Constrained Quadratic Model**:
1. The  number of shares sold each day is associated to the integer variable **s_\<i\>**.
1. The daily price of shares is associated to the integer variable **p_\<i\>**.
1. The daily revenue is the number of shares sold multiplied by the price on each sales day. To maximize the total revenue, is to minimize the negative sum of all the daily revenues.
1. The total numeber of shares sold cannot exceed the initial number of shares.
1. Price at first day is fixed.
1. Price at day i, p_\<i\>, is given by p_\<i-1\> plus the price increment given by &alpha; * s_\<i-1\>
### Problem workflow
1. We represent the problem using a **Constrained Quadratic Model**.
1. We use the **LeapHybridCQMSampler** as solver.
### Notes
1. p_\<i\> and s_\<i\> are positive integer variables. In order to reduce the solution space the solver must search for, it is important to set upper bounds gpr these variables. For this problem it is possible to define these upper bounds:
    1.  On any day, you cannot sell more than the total number of shares you start with.
    1. The maximum share price is the sum of the initial price and the total price increase that would result from selling all your shares.