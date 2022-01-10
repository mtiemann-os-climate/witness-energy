'''
Copyright 2022 Airbus SAS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from energy_models.core.techno_type.base_techno_models.solid_fuel_techno import SolidFuelTechno
from energy_models.core.stream_type.energy_models.electricity import Electricity
from energy_models.core.stream_type.carbon_models.carbon_capture import CarbonCapture
from energy_models.core.stream_type.energy_models.biomass_dry import BiomassDry

import numpy as np


class Pelletizing(SolidFuelTechno):

    def compute_other_primary_energy_costs(self):
        """
        Compute primary costs which depends on the technology 
        """

        # in kg of fuel by kg of pellets depends on moisture level
        self.cost_details['biomass_dry_needs'] = (1 + self.data_energy_dict['biomass_dry_moisture']) / \
            (1 + self.data_energy_dict['pellets_moisture'])

        # electricity needed for conditioning, storage + production of 1kg of pellets
        # plus electricity needed for chipping dry biomass
        self.cost_details['elec_needs'] = self.get_electricity_needs()
        # Cost of electricity for 1 kWh of pellet
        self.cost_details[Electricity.name] = list(
            self.prices[Electricity.name] * self.cost_details['elec_needs'])

        # Cost of biomass for 1 kWh of pellet
        self.cost_details[BiomassDry.name] = list(
            self.prices[BiomassDry.name] * self.cost_details['biomass_dry_needs'] /
            self.data_energy_dict['calorific_value'])

        return self.cost_details[Electricity.name] + self.cost_details[BiomassDry.name]

    def grad_price_vs_energy_price(self):
        '''
        Compute the gradient of global price vs energy prices 
        Work also for total CO2_emissions vs energy CO2 emissions
        '''
        elec_needs = self.get_electricity_needs()
        biomass_dry_needs = (1 + self.data_energy_dict['biomass_dry_moisture']) / \
            (1 + self.data_energy_dict['pellets_moisture']
             )
        return {Electricity.name: np.identity(len(self.years)) * elec_needs,
                BiomassDry.name: np.identity(len(self.years)) * biomass_dry_needs / self.data_energy_dict['calorific_value']}

    def compute_consumption_and_production(self):
        """
        Compute the consumption and the production of the technology for a given investment
        Maybe add efficiency in consumption computation ? 
        """

        self.compute_primary_energy_production()

        self.production[f'{CarbonCapture.flue_gas_name} ({self.mass_unit})'] = self.techno_infos_dict['CO2_from_production'] * \
            self.production[f'{SolidFuelTechno.energy_name} ({self.product_energy_unit})'] / \
            self.data_energy_dict['calorific_value']

        # Consumption
        self.consumption[f'{Electricity.name} ({self.product_energy_unit})'] = self.cost_details['elec_needs'] * \
            self.production[f'{SolidFuelTechno.energy_name} ({self.product_energy_unit})']

        self.consumption[f'{BiomassDry.name} ({self.product_energy_unit})'] = self.cost_details['biomass_dry_needs'] * \
            self.production[f'{SolidFuelTechno.energy_name} ({self.product_energy_unit})']

    def compute_CO2_emissions_from_input_ressources(self):
        ''' 
        Need to take into account negative CO2 from biomass_dry and CO2 from electricity (can be 0.0 or positive)
        '''

        self.carbon_emissions[f'{Electricity.name}'] = self.energy_CO2_emissions[f'{Electricity.name}'] * \
            self.cost_details['elec_needs']
        self.carbon_emissions[BiomassDry.name] = self.energy_CO2_emissions[BiomassDry.name] * \
            self.cost_details['biomass_dry_needs'] / \
            self.data_energy_dict['calorific_value']

        return self.carbon_emissions[f'{Electricity.name}'] + self.carbon_emissions[BiomassDry.name]
