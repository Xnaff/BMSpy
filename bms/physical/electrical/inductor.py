from bms import PhysicalBlock, Variable, np
from bms.blocks.continuous import Gain, Subtraction, ODE


class Inductor(PhysicalBlock):
    def __init__(self, node1, node2, L, name='Inductor'):
        # 1st eq: (U1-U2)=Ldi1/dt 2nd: i1=-i2
        occurence_matrix = np.array([[1, 1, 1, 0], [0, 1, 0, 1]])
        PhysicalBlock.__init__(self, [node1, node2], [
                               0, 1], occurence_matrix, [], name)
        self.L = L

    def partial_dynamic_system(self, ieq, variable):
        """
        returns dynamical system blocks associated to output variable
        """

        if ieq == 0:

            #            if variable==self.physical_nodes[0].variable:
            # print('1')
            #                # U1 is output
            #                # U1=i1/pC+U2
            #                Uc=Variable(hidden=True)
            #                block1=ODE(self.variables[0],Uc,[1],[0,self.C])
            #                sub1=Sum([self.physical_nodes[1].variable,Uc],variable)
            #                return [block1,sub1]
            #            elif variable==self.physical_nodes[1].variable:
            #                print('2')
            #                # U2 is output
            #                # U2=U1-i1/pC
            #                Uc=Variable(hidden=True)
            #                block1=ODE(self.variables[0],Uc,[-1],[0,self.C])
            #                sum1=Sum([self.physical_nodes[0].variable,Uc],variable)
            #                return [block1,sum1]
            if variable == self.variables[0]:  # i1=(u1-u2)/Lp
                print('3')
                # i1 is output
                # i1=pC(U1-U2)
                uc = Variable(hidden=True)
                subs1 = Subtraction(
                    self.physical_nodes[0].variable, self.physical_nodes[1].variable, uc)
                block1 = ODE(uc, variable, [1], [0, self.L])
                return [block1, subs1]
        elif ieq == 1:
            # i1=-i2
            if variable == self.variables[0]:
                # i1 as output
                return [Gain(self.variables[1], self.variables[0], -1)]
            elif variable == self.variables[1]:
                # i2 as output
                return [Gain(self.variables[0], self.variables[1], -1)]
