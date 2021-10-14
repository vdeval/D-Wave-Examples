###################################################################################################
# Demo program for stock Sales Strategy
###################################################################################################

# ------- Import Section -------
#import numpy as np
from dimod import ConstrainedQuadraticModel
from dimod import Integer
from dwave.system import LeapHybridCQMSampler

# ------- Program Configuration -------
max_days = 10
total_shares = 100
price_day_0 = 50
alpha = 1

max_time = 60

# ------- Model Configuration -------

# Initialization of CQM
cqm = ConstrainedQuadraticModel()

# Creation of the list of Integer variables
max_p = price_day_0 + alpha*total_shares    # max possible price
shares = [Integer(f's_{i}', upper_bound=total_shares) for i in range(max_days)]
price = [Integer(f'p_{i}', upper_bound=max_p) for i in range(max_days)]

# Objective function
revenue = [s*p for s, p in zip(shares, price)]
cqm.set_objective(-sum(revenue))

# Constraint 1: The total numeber of shares sold cannot exceed the initial number of shares
cqm.add_constraint(sum(shares) <= total_shares, label='Sell only shares you own')

# Constraint 2: Price at first day is fixed
cqm.add_constraint(price[0] == price_day_0, label='Initial share price')

# Constraint 3: The stock price increases in proportion to the number of shares sold the previous day
for i in range(1, max_days):
   pricing = cqm.add_constraint(price[i] - price[i-1] - alpha*shares[i-1] == 0, label=f'Sell at the price on day {i}')

# ------- Submit Model to Solver -------

# Initialization of Hybrid SOlver
sampler = LeapHybridCQMSampler()

# Submit the CQM to the selected solver
sampleset = sampler.sample_cqm(cqm, time_limit=max_time,label="D-Wave Example: Stock-Selling Strategy")

# Selection of feasible solutions
feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)  
if len(feasible_sampleset):      
   best = feasible_sampleset.first
   print("{} feasible solutions of {}.".format(len(feasible_sampleset), len(sampleset)))

   s = [val for key, val in best.sample.items() if "s_" in key]
   p = [val for key, val in best.sample.items() if "p_" in key]
   r = [p*s for p, s in zip(p, s)]

   print("Revenue of {} found for daily sales of: \n{}".format(sum(r), s))

  