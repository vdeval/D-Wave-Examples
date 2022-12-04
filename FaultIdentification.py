###################################################################################################
# Demo program for Fault Identification
###################################################################################################

# ------- Import Section -------
from dwave.system import DWaveSampler, EmbeddingComposite
from dimod import Binary
from dimod.binary.binary_quadratic_model import BinaryQuadraticModel
from dimod.typing import Variable
from dimod.vartypes import Vartype
from dimod.generators import and_gate, or_gate


# ------- Definition of NOT gate (not available in dimod.generators) -------
def not_gate(in0: Variable, out: Variable, *, strength: float = 1.0) -> BinaryQuadraticModel:
    """Generate a binary quadratic model with ground states corresponding to a NOT gate.
    Args:
        in0: Variable label for the input.
        out: Variable label for the output.
        strength: Energy of the lowest-energy infeasible state.
    Returns:
        A binary quadratic model with ground states corresponding to an NOT gate.
    """
    bqm = BinaryQuadraticModel(Vartype.BINARY)

    # add the variables (in order)
    bqm.add_variable(in0, bias=-1)
    bqm.add_variable(out, bias=-1)

    # add the quadratic biases
    bqm.add_quadratic(in0, out, 2)

    # the bqm currently has a strength of 1, so just need to scale
    if strength <= 0:
        raise ValueError("strength must be positive")
    bqm.scale(strength)

    return bqm

# ------- Program Configuration -------
# o1 = (AND (NOT(AND i1 i2)) (NOT (OR i3 i4)))


# ------- Model Preparation -------
bqm = BinaryQuadraticModel(Vartype.BINARY)
bqm += and_gate("i1", "i2", "x1")
bqm += or_gate("i3", "i4", "x2")
bqm += not_gate("x1", "x3")
bqm += not_gate("x2", "x4")
bqm += and_gate("x3", "x4","o1")

bqm.fix_variable("o1", 1)

# ------- Sampling -------
sampler = DWaveSampler()
embedding_sampler = EmbeddingComposite(sampler)
sampleset = embedding_sampler.sample(bqm, num_reads=100, label='Fault Identification')

# ------- Printing -------
print("Best solution found: \n",sampleset.first.sample)
#TODO: print more than one solution, ordered by energy