###################################################################################################
# Demo program for Bin Packing
###################################################################################################

# ------- Import Section -------
import numpy as np
from dimod import ConstrainedQuadraticModel
from dimod import Binary
from dwave.system import LeapHybridCQMSampler

# ------- Program Configuration -------
#num_items = 20
#num_bins = 5
#item_weight_range = [10, 20]
#weights = list(np.random.randint(*item_weight_range, num_items))
#bin_capacity = 100

weights = [11, 12, 13, 14, 15]
num_items = len(weights)
bin_capacity = [12, 15, 28, 37]
num_bins = len(bin_capacity)

max_time = 10

print("Problem: pack a total weight of {} into bins of capacity {}.".format(sum(weights), sum(bin_capacity)))
for i, value in enumerate(weights):
    print("---Item {} : {}".format(i, value))
for i, value in enumerate(bin_capacity):
    print("---Bin {} : {}".format(i, value))

# ------- Model Configuration -------

# Initialization of CQM
cqm = ConstrainedQuadraticModel()

# Creation of the list of bin_used variables
bin_used = [Binary(f'bin_used_{j}') for j in range(num_bins)]

# Objective function
cqm.set_objective(sum(bin_used))

# Creation of the list of variables item_<i>_in_bin_<j> 
item_in_bin = [[Binary(f'item_{i}_in_bin_{j}') for j in range(num_bins)] for i in range(num_items)]

# Constraint 1: Each item can go into only one bin
for i in range(num_items):
#    one_bin_per_item = cqm.add_constraint(sum(item_in_bin[i]) == 1, label=f'item_placing_{i}')
    one_bin_per_item = cqm.add_constraint(sum(item_in_bin[i][j] for j in range(num_bins)) == 1, label=f'item_placing_{i}')

# Constraint 2: Each bin has limited capacity
for j in range(num_bins):
    bin_up_to_capacity = cqm.add_constraint(
        sum(weights[i] * item_in_bin[i][j] for i in range(num_items)) - bin_used[j] * bin_capacity[j] <= 0,
        label=f'capacity_bin_{j}')

# ------- Submit Model to Solver -------

# Initialization of Hybrid SOlver
sampler = LeapHybridCQMSampler()

# Submit the CQM to the selected solver
sampleset = sampler.sample_cqm(cqm, time_limit=max_time,label="D-Wave Example: Bin Packing")

# Selection of feasible solutions
feasible_sampleset = sampleset.filter(lambda row: row.is_feasible)  
if len(feasible_sampleset):      
   best = feasible_sampleset.first
   print("{} feasible solutions of {}.".format(len(feasible_sampleset), len(sampleset)))
else:
   print("No feasible solution found")

# Helper function (for subsequent steps)
def get_indices(name):
    return [int(digs) for digs in name.split('_') if digs.isdigit()]

# Analysis of best solution
selected_bins = [key for key, val in best.sample.items() if 'bin_used' in key and val]   
print("{} bins are used.".format(len(selected_bins)))
for bin in selected_bins:                        
    in_bin = [key for key, val in best.sample.items() if
       "_in_bin" in key and
       get_indices(key)[1] == get_indices(bin)[0]
       and val]
    b = get_indices(in_bin[0])[1]
    w = [weights[get_indices(item)[0]] for item in in_bin]
    print("Bin {} has weights {} for a total of {}.".format(b, w, sum(w)))

