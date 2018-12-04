from bms import PhysicalBlock, Variable, np
from bms.blocks.continuous import ODE, WeightedSum, Product
from bms.blocks.nonlinear import Saturation


class Battery(PhysicalBlock):
    """
    Caution: still a bug, soc=0 doesn't imply i=0
    : param u_max: Voltage when soc=1
    : param u_min: Voltage when soc=0
    : param c: capacity of battery in W.s

    """
    def __init__(self, node1, node2, u_min, u_max, c, initial_soc, r, name='Battery'):
        # 1st eq: U2=signal, U1=0
        occurrence_matrix = np.array([[1, 1, 1, 0], [0, 1, 0, 1]])
        # occurrence_matrix=np.array([[1,1,1,0]]) # 1st eq: U2=signal, U1=0
        PhysicalBlock.__init__(self, [node1, node2], [0, 1], occurrence_matrix, [], name)
        self.u_max = u_max
        self.u_min = u_min
        self.c = c
        self.r = r
        self.initial_soc = initial_soc
        self.soc = Variable('Battery SoC', [initial_soc])
        self.u = Variable('Battery voltage')

    def partial_dynamic_system(self, ieq, variable):
        """
        returns dynamical system blocks associated to output variable
        """
        if ieq == 0:
            # Soc determination
            # soc=1-UI/CP
            v1 = Variable('UI', hidden=True)  # UI
            v2 = Variable('UI/CP', hidden=True)  # UI/CP
            v3 = Variable('soc0-UI/CP', hidden=True)  # soc0-UI/CP
            b1 = Product(self.u, self.variables[0], v1)
            b2 = ODE(v1, v2, [1], [1, self.c])
            b3 = WeightedSum([v2], v3, [-1], self.initial_soc)
            b4 = Saturation(v3, self.soc, 0, 1)
            b5 = WeightedSum([self.soc], self.u, [self.u_max-self.u_min], self.u_min)
            blocks = [b1, b2, b3, b4, b5]
        # U2-U1=U+Ri1
        # U=soc(Umax-Umin)+Umin
        if variable == self.physical_nodes[0].variable:
            print('Bat0#1')
            # U1 is output
            # U1=-U-Ri1+U2
            blocks.append(
                WeightedSum(
                    [self.u, self.variables[0], self.physical_nodes[1].variable],
                    variable, [-1, -self.r, 1]
                )
            )
        elif variable == self.physical_nodes[1].variable:
            print('Bat0#2')
            # U2 is output
            # U2=U1+Ri1+U
            blocks.append(
                WeightedSum(
                    [self.physical_nodes[0].variable, self.variables[0], self.u],
                    variable, [1, self.r, 1]
                )
            )

        elif variable == self.variables[0]:
            print('Bat0#3')
            # i1 is output
            # i1=(-U1+U2-U)/R
            blocks.append(
                WeightedSum(
                    [self.physical_nodes[0].variable, self.physical_nodes[1].variable, self.u],
                    variable,
                    [-1/self.r, 1/self.r, -1/self.r]
                )
            )

        return blocks
