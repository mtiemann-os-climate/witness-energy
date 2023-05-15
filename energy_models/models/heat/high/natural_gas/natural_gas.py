
from energy_models.core.stream_type.energy_models.heat import HighTemperatureHeat
from energy_models.core.techno_type.base_techno_models.heat_techno import HighHeatTechno
from energy_models.core.stream_type.energy_models.methane import Methane
from energy_models.core.stream_type.carbon_models.carbon_capture import CarbonCapture

import numpy as np


class NaturalGasHighHeat(HighHeatTechno):

    def compute_other_primary_energy_costs(self):
        """
        Compute primary costs to produce 1kWh of heat
        """
        self.cost_details[f'{Methane.name}_needs'] = self.get_theoretical_methane_needs()

        self.cost_details[f'{Methane.name}'] = \
            self.prices[f'{Methane.name}'] * \
            self.cost_details[f'{Methane.name}_needs'] / \
            self.cost_details['efficiency']

        # methane_needs

        # output needed in this method is in $/kwh of heat
        # to do so I need to know how much methane is used to produce 1kwh of heat (i need this information in kwh) : methane_needs is in kwh of methane/kwh of heat
        # kwh/kwh * price of methane ($/kwh) : kwh/kwh * $/kwh  ----> $/kwh  : price of methane is in self.prices[f'{Methane.name}']
        # and then we divide by efficiency


        return self.cost_details[f'{Methane.name}']

    def grad_price_vs_energy_price(self):
        '''
        Compute the gradient of global price vs energy prices
        Work also for total CO2_emissions vs energy CO2 emissions
        '''
        methane_needs = self.get_theoretical_methane_needs()
        efficiency = self.techno_infos_dict['efficiency']

        return {
                Methane.name: np.identity(len(self.years)) * methane_needs / efficiency
                }

    def compute_consumption_and_production(self):
        """
        Compute the consumption and the production of the technology for a given investment
        """

        self.compute_primary_energy_production()


        # Consumption

        self.consumption[f'{Methane.name} ({self.product_energy_unit})'] = self.cost_details[f'{Methane.name}_needs'] * \
            self.production[f'{HighTemperatureHeat.name} ({self.product_energy_unit})']

        # CO2 production
        self.production[f'{CarbonCapture.flue_gas_name} ({self.mass_unit})'] = Methane.data_energy_dict['CO2_per_use'] / \
                                                                               Methane.data_energy_dict['calorific_value'] * \
            self.consumption[f'{Methane.name} ({self.product_energy_unit})']

    def compute_CO2_emissions_from_input_resources(self):
        '''
        Need to take into account CO2 from Methane production
        '''

        self.carbon_emissions[Methane.name] = self.energy_CO2_emissions[Methane.name] * \
            self.cost_details[f'{Methane.name}_needs'] 

        return self.carbon_emissions[f'{Methane.name}']

    def get_theoretical_methane_needs(self):
        # we need as output kwh/kwh 
        methane_demand = self.techno_infos_dict['methane_demand']

        methane_needs = methane_demand
        return methane_needs



