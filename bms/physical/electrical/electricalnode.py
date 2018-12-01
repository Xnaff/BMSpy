from bms import PhysicalNode
from bms.blocks.continuous import WeightedSum


class ElectricalNode(PhysicalNode):
    def __init__(self, name=''):
        PhysicalNode.__init__(self, False, True, name, 'Voltage', 'Intensity')

    @staticmethod
    def conservative_law(flux_variables, output_variable):
        return [WeightedSum(flux_variables, output_variable, [-1]*len(flux_variables))]
