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
from climateeconomics.glossarycore import GlossaryCore
from energy_models.core.stream_type.carbon_models.carbon_dioxyde import CO2
from energy_models.core.techno_type.base_techno_models.biomass_dry_techno import BiomassDryTechno
from energy_models.core.stream_type.energy_models.electricity import Electricity

import pandas as pd
import numpy as np
from copy import deepcopy


class UnmanagedWood(BiomassDryTechno):

    def compute_other_primary_energy_costs(self):
        """
        Compute primary costs to produce 1kg of wood
        """

        self.cost_details['elec_needs'] = self.get_electricity_needs()
        self.cost_details[f'{Electricity.name}'] = list(
            self.prices[f'{Electricity.name}'] * self.cost_details['elec_needs'])

        return self.cost_details[f'{Electricity.name}']

    def grad_price_vs_energy_price(self):
        '''
        Compute the gradient of global price vs energy prices 
        Work also for total CO2_emissions vs energy CO2 emissions
        '''
        elec_needs = self.get_electricity_needs()

        return {Electricity.name: np.identity(len(self.years)) * elec_needs}

    def grad_production_invest(self, capex, production, production_mix):

        dcapex_dinvest = self.compute_dcapex_dinvest(
            self.invest_level.loc[self.invest_level[GlossaryCore.Years]
                                  <= self.year_end][GlossaryCore.InvestValue].values, self.techno_infos_dict, self.initial_production)

        dprod_dinvest = self.compute_dprod_dinvest(
            capex, self.invest_level[GlossaryCore.InvestValue].values,
            self.invest_before_ystart[GlossaryCore.InvestValue].values,
            self.techno_infos_dict, dcapex_dinvest)

        years = self.years
        name_tot = f'{self.energy_name}_tot (TWh)'

        residue_year_start_production = production_mix[name_tot][0] * self.techno_infos_dict['residue_density_percentage'] * \
            (1 - self.techno_infos_dict['residue_percentage_for_energy'])
        wood_year_start_production = production_mix[name_tot][0] * self.techno_infos_dict['non_residue_density_percentage'] * \
            (1 - self.techno_infos_dict['wood_percentage_for_energy'])

        # compute production dedicated to energy from residue
        residues = production_mix[name_tot] *\
            self.techno_infos_dict['residue_density_percentage'] - \
            residue_year_start_production
        d_residue = [
            self.techno_infos_dict['residue_density_percentage']] * len(residues)
        for i in range(0, len(residues)):
            if residues[i] < 0:
                d_residue[i] = 0
        # compute production dedicated to energy from wood
        woods = production_mix[name_tot] *\
            self.techno_infos_dict['non_residue_density_percentage'] - \
            wood_year_start_production
        d_woods = [
            self.techno_infos_dict['non_residue_density_percentage']] * len(woods)
        for i in range(0, len(residues)):
            if woods[i] < 0:
                d_woods[i] = 0
        d_production_tot = np.add(d_residue, d_woods)

        dconso_dinvest = {}
        for column in production:
            dprod_column_dinvest = dprod_dinvest.copy()
            if column == f'{self.energy_name} ({self.product_energy_unit})':
                var_prod = d_production_tot
                for line in range(len(years)):
                    if self.is_invest_before_year(years[line] - self.techno_infos_dict['construction_delay']) \
                            and var_prod[line] == 0.0 and dprod_dinvest[line, :].sum() != 0.0 and line != len(years) - 1:

                        var_prod[line] = var_prod[line + 1]
                    dprod_column_dinvest[line,
                                         :] = dprod_dinvest[line, :] * var_prod[line]
                dconso_dinvest[column] = dprod_column_dinvest

        return dconso_dinvest

    def compute_consumption_and_production(self):
        """
        Compute the consumption and the production of the technology for a given investment
        Maybe add efficiency in consumption computation ? 
        """
        name_residue = f'{self.energy_name}_residue (TWh)'
        name_wood = f'{self.energy_name}_wood (TWh)'
        name_non_energy = f'{self.energy_name}_non_energy (TWh)'
        name_tot = f'{self.energy_name}_tot (TWh)'

        self.compute_primary_energy_production()

        self.production_mix = pd.DataFrame({GlossaryCore.Years: self.years})
        unmanaged_production = deepcopy(
            self.production[f'{BiomassDryTechno.energy_name} ({self.product_energy_unit})'])

        # compute production for non energy at year start with percentages
        residue_year_start_production = unmanaged_production[0] * self.techno_infos_dict['residue_density_percentage'] * \
            (1 - self.techno_infos_dict['residue_percentage_for_energy'])
        wood_year_start_production = unmanaged_production[0] * self.techno_infos_dict['non_residue_density_percentage'] * \
            (1 - self.techno_infos_dict['wood_percentage_for_energy'])

        # compute production dedicated to energy from residue
        self.production_mix[name_residue] = unmanaged_production *\
            self.techno_infos_dict['residue_density_percentage'] - \
            residue_year_start_production
        # unmanaged wood production must not be negative because we don't want
        # to force invest in this techno
        self.production_mix.loc[
            self.production_mix[name_residue] < 0, name_residue] = 0

        # compute production dedicated to energy from wood
        self.production_mix[name_wood] = unmanaged_production *\
            self.techno_infos_dict['non_residue_density_percentage'] - \
            wood_year_start_production
        # unmanaged wood production must not be negative because we don't want
        # to force invest in this techno
        self.production_mix.loc[
            self.production_mix[name_wood] < 0, name_wood] = 0

        # compute production dedicated to non energy
        self.production_mix[name_non_energy] = unmanaged_production - \
            self.production_mix[name_residue] - \
            self.production_mix[name_wood]

        self.production_mix[name_tot] = unmanaged_production

        # compute output production dedicated to energy
        self.production[f'{BiomassDryTechno.energy_name} ({self.product_energy_unit})'] = self.production_mix[name_residue] +\
            self.production_mix[name_wood]

        self.consumption[f'{Electricity.name} ({self.product_energy_unit})'] = self.cost_details['elec_needs'] * \
            self.production[f'{BiomassDryTechno.energy_name} ({self.product_energy_unit})']  # in kWH

        self.production[f'{CO2.name} ({self.mass_unit})'] = self.techno_infos_dict['CO2_from_production'] / \
            self.data_energy_dict['high_calorific_value'] * \
            self.production[f'{BiomassDryTechno.energy_name} ({self.product_energy_unit})']

    def compute_CO2_emissions_from_input_resources(self):
        '''
        Need to take into account  CO2 from electricity/fuel production
        '''

        self.carbon_emissions[f'{Electricity.name}'] = self.energy_CO2_emissions[f'{Electricity.name}'] * \
            self.cost_details['elec_needs']

        return self.carbon_emissions[f'{Electricity.name}']

    def compute_price(self):
        prices = BiomassDryTechno.compute_price(self)
        unmanaged_price = deepcopy(self.cost_details[self.name])

        residue_percent = self.techno_infos_dict['residue_density_percentage']
        wood_percent = self.techno_infos_dict['non_residue_density_percentage']

        wood_residue_percent = self.techno_infos_dict['wood_residue_price_percent_dif']

        # Price_tot = Price_residue * %res + Price_wood * %wood
        # Price_residue = %res_wood * Price_wood
        self.price_mix = pd.DataFrame({GlossaryCore.Years: self.years})
        self.price_mix[f'{BiomassDryTechno.energy_name}_wood'] = unmanaged_price / \
            (wood_residue_percent * residue_percent + wood_percent)
        self.price_mix[f'{BiomassDryTechno.energy_name}_residue'] = wood_residue_percent * \
            self.price_mix[f'{BiomassDryTechno.energy_name}_wood']

        return prices

    def get_mean_age_over_years(self):

        mean_age_df = pd.DataFrame({GlossaryCore.Years: self.years})

        self.age_distrib_prod_df['age_x_prod'] = self.age_distrib_prod_df['age'] * \
            self.age_distrib_prod_df[f'distrib_prod ({self.product_energy_unit})']

        production = self.production_woratio[f'{self.energy_name} ({self.product_energy_unit})']

        # compute production for non energy at year start with percentages
        residue_year_start_production = production[0] * self.techno_infos_dict['residue_density_percentage'] * \
            (1 - self.techno_infos_dict['residue_percentage_for_energy'])
        wood_year_start_production = production[0] * self.techno_infos_dict['non_residue_density_percentage'] * \
            (1 - self.techno_infos_dict['wood_percentage_for_energy'])

        mean_age_df['mean age'] = self.age_distrib_prod_df.groupby(
            [GlossaryCore.Years], as_index=False).agg({'age_x_prod': 'sum'})['age_x_prod'] / \
            (production + residue_year_start_production + wood_year_start_production)
        mean_age_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        mean_age_df.fillna(0.0, inplace=True)

        return mean_age_df
