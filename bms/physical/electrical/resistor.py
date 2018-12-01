from bms import PhysicalBlock, np
from bms.blocks.continuous import Gain, WeightedSum


class Resistor(PhysicalBlock):
    def __init__(self, node1, node2, r, name='Resistor'):
        # 1st eq: (U1-U2)=R(i1-i2) 2nd: i1=-i2
        occurrence_matrix = np.array([[1, 1, 1, 0], [0, 1, 0, 1]])
        PhysicalBlock.__init__(self, [node1, node2], [
                               0, 1], occurrence_matrix, [], name)
        self.r = r

    def partial_dynamic_system(self, ieq, variable):
        """
        returns dynamical system blocks associated to output variable
        """
#        print(ieq,variable.name)
        if ieq == 0:
            # U1-U2=R(i1)
            if variable == self.physical_nodes[0].variable:
                # U1 is output
                # U1=R(i1)+U2
                return [
                    WeightedSum(
                        [self.physical_nodes[1].variable, self.variables[0]],
                        variable,
                        [1, self.r]
                    )
                ]
            elif variable == self.physical_nodes[1].variable:
                # U2 is output
                # U2=-R(i1)+U2
                return [
                    WeightedSum(
                        [self.physical_nodes[0].variable, self.variables[0]],
                        variable,
                        [1, -self.r]
                    )
                ]
            elif variable == self.variables[0]:
                # i1 is output
                # i1=(U1-U2)/R
                return [
                    WeightedSum(
                        [self.physical_nodes[0].variable, self.physical_nodes[1].variable],
                        variable,
                        [1/self.r, -1/self.r]
                    )
                ]
        elif ieq == 1:
            # i1=-i2
            if variable == self.variables[0]:
                # i1 as output
                return [Gain(self.variables[1], self.variables[0], -1)]
            elif variable == self.variables[1]:
                # i2 as output
                return [Gain(self.variables[0], self.variables[1], -1)]
