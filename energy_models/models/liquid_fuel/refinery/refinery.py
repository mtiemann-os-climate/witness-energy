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
from energy_models.core.stream_type.carbon_models.carbon_capture import CarbonCapture
from energy_models.core.techno_type.base_techno_models.liquid_fuel_techno import LiquidFuelTechno
from energy_models.core.stream_type.energy_models.electricity import Electricity
from energy_models.core.stream_type.resources_models.oil import CrudeOil
from sos_trades_core.tools.base_functions.exp_min import compute_func_with_exp_min
import pandas as pd
import numpy as np


class Refinery(LiquidFuelTechno):

    def configure_energy_data(self, inputs_dict):
        '''
        Configure energy data by reading the data_energy_dict in the right Energy class
        Overloaded for each energy type
        '''
        self.data_energy_dict = inputs_dict['data_fuel_dict']
        self.other_energy_dict = inputs_dict['other_fuel_dict']

    def compute_other_primary_energy_costs(self):
        """
        Compute primary costs which depends on the technology 
        """

        self.cost_details['elec_needs'] = self.get_electricity_needs()

        self.cost_details[Electricity.name] = list(
            self.prices[Electricity.name] * self.cost_details['elec_needs'] / self.cost_details['efficiency'])

        self.cost_details['crude_oil_needs'] = self.get_fuel_needs()
        self.cost_details[CrudeOil.name] = list(
            self.resources_prices[CrudeOil.name] * self.cost_details['crude_oil_needs'] / self.cost_details['efficiency'])

        return self.cost_details[Electricity.name] + self.cost_details[CrudeOil.name]

    def grad_price_vs_energy_price(self):
        '''
        Compute the gradient of global price vs energy prices 
        Work also for total CO2_emissions vs energy CO2 emissions
        '''
        elec_needs = self.get_electricity_needs()

        return {Electricity.name: np.identity(len(self.years)) * elec_needs}

    def compute_consumption_and_production(self):
        """
        Compute the consumption and the production of the technology for a given investment
        Maybe add efficiency in consumption computation ?

        liquid_fuel is the total production
        the break down is made with self.production['kerosene'] ... ect 
        """

        self.compute_primary_energy_production()

        for energy in self.other_energy_dict:
            # if it s a dict, so it is a data_energy_dict
            self.production[f'{energy} ({self.product_energy_unit})'] = self.production[
                f'{self.energy_name} ({self.product_energy_unit})'] * self.techno_infos_dict['product_break_down'][energy] / 11.66 * self.other_energy_dict[energy]['calorific_value']

        self.production[f'{CarbonCapture.flue_gas_name} ({self.mass_unit})'] = self.techno_infos_dict['CO2_from_production'] / \
            self.data_energy_dict['calorific_value'] * \
            self.production[f'{LiquidFuelTechno.energy_name} ({self.product_energy_unit})']

        # Consumption
        self.consumption[f'{Electricity.name} ({self.product_energy_unit})'] = self.cost_details['elec_needs'] * \
            self.production[f'{LiquidFuelTechno.energy_name} ({self.product_energy_unit})']  # in kWH

        self.consumption[f'{CrudeOil.name} ({self.product_energy_unit})'] = self.cost_details['crude_oil_needs'] * \
            self.production[f'{LiquidFuelTechno.energy_name} ({self.product_energy_unit})']  # in kWH

        # oil consumption:
        self.consumption[f'oil_resource'] = self.cost_details['crude_oil_needs'] * \
            self.production[f'{LiquidFuelTechno.energy_name} ({self.product_energy_unit})'] / \
            CrudeOil.data_energy_dict['calorific_value']  # in Mt

    def compute_price(self):
        """
        Compute the detail price of the technology
        """

        self.cost_details['invest'] = self.invest_level.loc[self.invest_level['years']
                                                            <= self.cost_details['years'].max()]['invest'].values
        # Maximize with smooth exponential
        self.cost_details['invest'] = compute_func_with_exp_min(
            self.cost_details['invest'].values, 1.0e-12)

        self.cost_details[f'Capex_{self.name}'] = self.compute_capex(
            self.cost_details['invest'].values, self.techno_infos_dict)

        crf = self.compute_crf(self.techno_infos_dict)

        # Compute efficiency evolving in time or not
        if self.techno_infos_dict['techno_evo_eff'] == 'yes':
            self.cost_details['efficiency'] = self.configure_efficiency()
        else:
            self.cost_details['efficiency'] = self.techno_infos_dict['efficiency']

        self.prices = self.prices.loc[self.prices['years']
                                      <= self.cost_details['years'].max()]
        self.cost_details['energy_costs'] = self.compute_other_primary_energy_costs(
        )

        # Factory cost including CAPEX OPEX
        self.cost_details[f'{self.name}_factory'] = self.cost_details[f'Capex_{self.name}'] * \
            (crf + self.techno_infos_dict['Opex_percentage'])

        # Compute transport and CO2 taxes
        self.cost_details['transport'] = self.compute_transport()

        self.cost_details['CO2_taxes_factory'] = self.compute_co2_tax()

        # Add transport and CO2 taxes
        self.cost_details[self.name] = self.cost_details[f'{self.name}_factory'] + self.cost_details['transport'] + \
            self.cost_details['CO2_taxes_factory'] + \
            self.cost_details['energy_costs']

        # Add margin in %
        self.cost_details[self.name] *= self.margin.loc[self.margin['years']
                                                        <= self.cost_details['years'].max()]['margin'].values / 100.0

        if 'CO2_taxes_factory' in self.cost_details:
            self.cost_details[f'{self.name}_wotaxes'] = self.cost_details[self.name] - \
                self.cost_details['CO2_taxes_factory'] * \
                self.margin.loc[self.margin['years']
                                <= self.cost_details['years'].max()]['margin'].values / 100.0

        else:
            self.cost_details[f'{self.name}_wotaxes'] = self.cost_details[self.name]

        return self.cost_details

    def compute_CO2_emissions_from_input_resources(self):
        '''
        Need to take into account  CO2 from electricity/fuel production
        '''

        self.carbon_emissions[f'{Electricity.name}'] = self.energy_CO2_emissions[f'{Electricity.name}'] * \
            self.cost_details['elec_needs']

        self.carbon_emissions[CrudeOil.name] = self.resources_CO2_emissions[f'{CrudeOil.name}'] * \
            self.cost_details['crude_oil_needs']

        return self.carbon_emissions[f'{Electricity.name}'] + self.carbon_emissions[CrudeOil.name]

    def compute_prod_from_invest(self, construction_delay):
        '''
        Compute the energy production of a techno from investment in TWh
        Add a delay for factory construction
        '''

        # Reverse the array of invest before year start with [::-1]
        prod_before_ystart = pd.DataFrame({'years': np.arange(self.year_start - construction_delay, self.year_start),
                                           'invest': self.invest_before_ystart['invest'].values[::1],
                                           f'Capex_{self.name}': self.cost_details.loc[self.cost_details['years'] == self.year_start, f'Capex_{self.name}'].values[0]})

        production_from_invest = pd.concat(
            [self.cost_details[['years', 'invest', f'Capex_{self.name}']], prod_before_ystart], ignore_index=True)
        production_from_invest.sort_values(by=['years'], inplace=True)
        # invest from G$ to M$
        production_from_invest['prod_from_invest'] = production_from_invest['invest'] / \
            (production_from_invest[f'Capex_{self.name}'] +
             self.cost_details[CrudeOil.name])
        production_from_invest['years'] += construction_delay
        production_from_invest = production_from_invest[production_from_invest['years']
                                                        <= self.year_end]

        return production_from_invest

    def compute_dprod_dinvest(self, capex_list, invest_list, invest_before_year_start, techno_dict, dcapex_list_dinvest_list):
        '''
        Compute the partial derivative of prod vs invest  and the partial derivative of prod vs capex
        To compute after the total derivative of prod vs invest = dpprod_dpinvest + dpprod_dpcapex*dcapexdinvest
        with dcapexdinvest already computed for detailed prices
        '''
        nb_years = len(capex_list)

        if 'complex128' in [capex_list.dtype, invest_list.dtype, invest_before_year_start.dtype, dcapex_list_dinvest_list.dtype]:
            arr_type = 'complex128'
        else:
            arr_type = 'float64'
        dprod_list_dinvest_list = np.zeros(
            (nb_years, nb_years), dtype=arr_type)
        dprod_list_dcapex_list = np.zeros(
            (nb_years, nb_years), dtype=arr_type)

        crude_oil_price = self.resources_prices[CrudeOil.name] * \
            self.get_fuel_needs() / self.configure_efficiency()
        # We fill this jacobian column by column because it is the same element
        # in the entire column
        for i in range(nb_years):

            dpprod_dpinvest = 1.0 / \
                (capex_list[i] + crude_oil_price[i])
            len_non_zeros = min(max(0, nb_years -
                                    techno_dict['construction_delay'] - i),
                                techno_dict['lifetime'])
            first_len_zeros = min(
                i + techno_dict['construction_delay'], nb_years)
            last_len_zeros = max(0, nb_years -
                                 len_non_zeros - first_len_zeros)
            # For prod in each column there is lifetime times the same value which is dpprod_dpinvest
            # This value is delayed in time (means delayed in lines for
            # jacobian by construction _delay)
            # Each column is then composed of [0,0,0... (dp/dx,dp/dx)*lifetime,
            # 0,0,0]

            dprod_list_dinvest_list[:, i] = np.hstack((np.zeros(first_len_zeros),
                                                       np.ones(
                len_non_zeros) * dpprod_dpinvest,
                np.zeros(last_len_zeros)))
            # Same for capex
            dpprod_dpcapex = - \
                invest_list[i] / (capex_list[i] +
                                  crude_oil_price[i])**2

            dprod_list_dcapex_list[:, i] = np.hstack((np.zeros(first_len_zeros),
                                                      np.ones(
                len_non_zeros) * dpprod_dpcapex,
                np.zeros(last_len_zeros)))
        # but the capex[0] is used for invest before
        # year_start then we need to add it to the first column
        dpprod_dpcapex0_list = [- invest / (capex_list[0] +
                                            crude_oil_price[0]) ** 2
                                for invest in invest_before_year_start]

        for index, dpprod_dpcapex0 in enumerate(dpprod_dpcapex0_list):
            len_non_zeros = min(
                techno_dict['lifetime'], nb_years - index)
            dprod_list_dcapex_list[:, 0] += np.hstack((np.zeros(index),
                                                       np.ones(
                len_non_zeros) * dpprod_dpcapex0,
                np.zeros(nb_years - index - len_non_zeros)))

        if 'complex128' in [dprod_list_dinvest_list.dtype, dcapex_list_dinvest_list.dtype, dprod_list_dcapex_list.dtype]:
            arr_type = 'complex128'
        else:
            arr_type = 'float64'

        #dprod_dfluegas = dpprod_dpfluegas + dprod_dcapex * dcapexdfluegas
        dprod_dinvest = np.zeros(
            (nb_years, nb_years), dtype=arr_type)

        for line in range(nb_years):
            for column in range(nb_years):

                dprod_dinvest[line, column] = dprod_list_dinvest_list[line, column] + \
                    np.matmul(
                        dprod_list_dcapex_list[line, :], dcapex_list_dinvest_list[:, column])

        return dprod_dinvest
