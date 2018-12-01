from bms import PhysicalBlock, np
from bms.blocks.continuous import WeightedSum


class Generator(PhysicalBlock):
    """
    :param voltage_signal: BMS signal to be input function of voltage (Step,Sinus...)
    """

    def __init__(self, node1, node2, voltage_signal, name='GeneratorGround'):
        occurence_matrix = np.array([[1, 0, 1, 0]])  # 1st eq: U2=signal, U1=0
        PhysicalBlock.__init__(self, [node1, node2], [
                               0, 1], occurence_matrix, [], name)
        self.voltage_signal = voltage_signal

    def partial_dynamic_system(self, ieq, variable):
        """
        returns dynamical system blocks associated to output variable
        """
        if ieq == 0:
            # U2-U1=signal
            if variable == self.physical_nodes[0].variable:
                # U1 is output
                # U1=U2-signal
                return [WeightedSum([self.physical_nodes[1].variable, self.voltage_signal], variable, [1, -1])]
            elif variable == self.physical_nodes[1].variable:
                # U2 is output
                # U2=U1+signal
                return [WeightedSum([self.physical_nodes[0].variable, self.voltage_signal], variable, [1, 1])]
