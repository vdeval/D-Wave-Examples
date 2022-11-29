###################################################################################################
# Demo program for Job Scheduling Problem
###################################################################################################

# ------- Import Section -------
import numpy as np
from dimod import ConstrainedQuadraticModel
from dimod import Binary
from dwave.system import LeapHybridCQMSampler

# ------- Problem Configuration -------


# ------- Solver Configuration -------
max_time = 10