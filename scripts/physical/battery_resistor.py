# -*- coding: utf-8 -*-
"""
Battery and resistor circuit with physical modelling
                    _______
           ___1_____|  R   |______ 
      + __|__       |______|      |
         _ _                      |  
        - |_______________________| 
             2                 
"""


import bms
from bms.physical.electrical.electricalnode import ElectricalNode
from bms.physical.electrical.battery import Battery
from bms.physical.electrical.resistor import Resistor
from bms.physical.electrical.ground import Ground
from bms.signals.functions import Sinus

# U=Sinus('Generator',2,5)# Voltage of generator
r = 10  # Resistance in Ohm
r_int = 10
u_max = 12.5
u_min = 6
c = 3600*10
soc = 0.8

n1 = ElectricalNode('1')
n2 = ElectricalNode('2')
# n3=ElectricalNode('3')

bat = Battery(n1, n2, u_min, u_max, c, soc, r_int)
res = Resistor(n2, n1, r)
G = Ground(n1)

ps = bms.PhysicalSystem(5000, 50, [bat, res, G], [])
ds = ps.dynamic_system

# ds._ResolutionOrder3()
d = ds.Simulate()
ds.PlotVariables([[n1.variable, n2.variable], [bat.soc], [bat.variables[0]]])

# Validation: analytical solutions
