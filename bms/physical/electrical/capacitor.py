from bms import PhysicalBlock, Variable, np
from bms.blocks.continuous import Sum, Gain, ODE


class Capacitor(PhysicalBlock):
    def __init__(self, node1, node2, c, name='Capacitor'):
        # 1st eq: (U1-U2)=R(i1-i2) 2nd: i1=-i2
        occurrence_matrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1]])
        PhysicalBlock.__init__(self, [node1, node2], [
                               0, 1], occurrence_matrix, [], name)
        self.c = c

    def partial_dynamic_system(self, ieq, variable):
        """
        returns dynamical system blocks associated to output variable
        """

        if ieq == 0:

            if variable == self.physical_nodes[0].variable:
                print('1')
                # U1 is output
                # U1=i1/pC+U2
                uc = Variable(hidden=True)
                block1 = ODE(self.variables[0], uc, [1], [0, self.c])
                sub1 = Sum([self.physical_nodes[1].variable, uc], variable)
                return [block1, sub1]
            elif variable == self.physical_nodes[1].variable:
                print('2')
                # U2 is output
                # U2=U1-i1/pC
                uc = Variable(hidden=True)
                block1 = ODE(self.variables[0], uc, [-1], [0, self.c])
                sum1 = Sum([self.physical_nodes[0].variable, uc], variable)
                return [block1, sum1]
#            elif variable==self.variables[0]:
#                print('3')
#                # i1 is output
#                # i1=pC(U1-U2)
#                ic=Variable(hidden=True)
#                subs1=Subtraction(self.physical_nodes[0].variable,self.physical_nodes[1].variable,ic)
#                block1=ODE(ic,variable,[0,self.C],[1])
#                return [block1,subs1]
        elif ieq == 1:
            # i1=-i2
            if variable == self.variables[0]:
                # i1 as output
                #                print('Bat1#0')
                return [Gain(self.variables[1], self.variables[0], -1)]
            elif variable == self.variables[1]:
                # i2 as output
                #                print('Bat1#1')
                return [Gain(self.variables[0], self.variables[1], -1)]
