from bms import PhysicalBlock, np
from bms.blocks.continuous import Gain
from bms.signals.functions import Step


class Ground(PhysicalBlock):
    def __init__(self, node1, name='Ground'):
        occurence_matrix = np.array([[1, 0]])  # U1=0
        PhysicalBlock.__init__(self, [node1], [], occurence_matrix, [], name)

    def partial_dynamic_system(self, ieq, variable):
        """
        returns dynamical system blocks associated to output variable
        """
        if ieq == 0:
            # U1=0
            if variable == self.physical_nodes[0].variable:
                v = Step('Ground', 0)
                return[Gain(v, variable, 1)]
