'''
Copyright 2022 Airbus SAS
Modifications on 2023/11/07-2023/11/09 Copyright 2023 Capgemini

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
import numpy as np
import pandas as pd
import scipy.interpolate as sc

from climateeconomics.glossarycore import GlossaryCore
from energy_models.core.stream_type.energy_models.solid_fuel import SolidFuel
from energy_models.core.energy_mix_study_manager import EnergyMixStudyManager
from energy_models.core.energy_process_builder import INVEST_DISCIPLINE_DEFAULT, INVEST_DISCIPLINE_OPTIONS
DEFAULT_TECHNOLOGIES_LIST = ['CoalExtraction', 'Pelletizing']
TECHNOLOGIES_LIST = ['CoalExtraction', 'Pelletizing']
TECHNOLOGIES_LIST_DEV = ['CoalExtraction', 'Pelletizing']


class Study(EnergyMixStudyManager):
    def __init__(self, year_start=2020, year_end=2050, time_step=1, technologies_list=TECHNOLOGIES_LIST,
                 bspline=True, main_study=True, execution_engine=None, invest_discipline=INVEST_DISCIPLINE_DEFAULT):
        super().__init__(__file__, technologies_list=technologies_list,
                         main_study=main_study, execution_engine=execution_engine, invest_discipline=invest_discipline)
        self.year_start = year_start
        self.year_end = year_end
        self.years = np.arange(self.year_start, self.year_end + 1)
        self.energy_name = None
        self.bspline = bspline

    def get_investments(self):
        invest_solid_fuel_mix_dict = {}

        l_ctrl = np.arange(0, 8)

        if 'CoalExtraction' in self.technologies_list:
            #             invest_solid_fuel_mix_dict['CoalExtraction'] = [
            #                 99.9, 50.0] + [0.02] * (len(l_ctrl) - 2)
            invest_solid_fuel_mix_dict['CoalExtraction'] = np.array(
                [99, 50, 20, 50, 20, 50, 20, 50])

        if 'Pelletizing' in self.technologies_list:
            #             invest_solid_fuel_mix_dict['Pelletizing'] = [
            #                 1, 50.0] + [99.9] * (len(l_ctrl) - 2)
            invest_solid_fuel_mix_dict['Pelletizing'] = np.array(
                [1, 50, 80, 80, 80, 80, 80, 80])

        if self.bspline:
            invest_solid_fuel_mix_dict[GlossaryCore.Years] = self.years

            for techno in self.technologies_list:
                invest_solid_fuel_mix_dict[techno], _ = self.invest_bspline(
                    invest_solid_fuel_mix_dict[techno], len(self.years))

        solid_fuel_mix_invest_df = pd.DataFrame(invest_solid_fuel_mix_dict)

        return solid_fuel_mix_invest_df

    def get_investments_old(self):
        invest_solid_fuel_mix_dict = {}

        l_ctrl = np.arange(0, 8)

        if 'CoalExtraction' in self.technologies_list:
            invest_solid_fuel_mix_dict['CoalExtraction'] = [
                99.9, 50.0] + [0.02] * (len(l_ctrl) - 2)
        if 'Pelletizing' in self.technologies_list:
            invest_solid_fuel_mix_dict['Pelletizing'] = [
                1, 50.0] + [99.9] * (len(l_ctrl) - 2)

        if self.bspline:
            invest_solid_fuel_mix_dict[GlossaryCore.Years] = self.years

            for techno in self.technologies_list:
                invest_solid_fuel_mix_dict[techno], _ = self.invest_bspline(
                    invest_solid_fuel_mix_dict[techno], len(self.years))

        solid_fuel_mix_invest_df = pd.DataFrame(invest_solid_fuel_mix_dict)

        return solid_fuel_mix_invest_df

    def setup_usecase(self):
        energy_mix_name = 'EnergyMix'
        self.energy_name = SolidFuel.name
        solid_fuel_name = f'{energy_mix_name}.{SolidFuel.name}'
        years = np.arange(self.year_start, self.year_end + 1)
        # reference_data_name = 'Reference_aircraft_data'
        self.energy_prices = pd.DataFrame({GlossaryCore.Years: self.years,
                                           'electricity': 16.0,
                                           'crude oil': 44.0,
                                           'biomass_dry': 68.12 / 3.36})

        # 2020 - 2025 www.globenewswire.com growth rate of 14,47%
        # self.invest_level = pd.DataFrame(
        #    {GlossaryCore.Years: years, GlossaryCore.InvestValue:  13.0e9})
        # the value for invest_level is just set as an order of magnitude
        self.invest_level = pd.DataFrame(
            {GlossaryCore.Years: years, GlossaryCore.InvestValue:  10.0})
        co2_taxes_year = [2018, 2020, 2025, 2030, 2035, 2040, 2045, 2050]
        co2_taxes = [14.86, 17.22, 20.27,
                     29.01,  34.05,   39.08,  44.69,   50.29]
        func = sc.interp1d(co2_taxes_year, co2_taxes,
                           kind='linear', fill_value='extrapolate')

        self.co2_taxes = pd.DataFrame(
            {GlossaryCore.Years: years, GlossaryCore.CO2Tax: func(years)})
        self.margin = pd.DataFrame(
            {GlossaryCore.Years: years, GlossaryCore.MarginValue: 110.0})
        # From future of hydrogen
        self.transport = pd.DataFrame(
            {GlossaryCore.Years: years, 'transport': 7.6})

        self.resources_price = pd.DataFrame(columns=[GlossaryCore.Years, 'CO2'])
        self.resources_price[GlossaryCore.Years] = years
        self.resources_price['CO2'] = np.linspace(50.0, 100.0, len(years))

        self.energy_carbon_emissions = pd.DataFrame(
            {GlossaryCore.Years: years, 'solid_fuel': 0.64 / 4.86, 'biomass_dry': - 0.425 * 44.01 / 12.0, 'electricity': 0.0, 'methane': 0.123 / 15.4, 'syngas': 0.0, 'hydrogen.gaseous_hydrogen': 0.0, 'crude oil': 0.02533})

        investment_mix = self.get_investments()
        values_dict = {f'{self.study_name}.{GlossaryCore.YearStart}': self.year_start,
                       f'{self.study_name}.{GlossaryCore.YearEnd}': self.year_end,
                       f'{self.study_name}.{solid_fuel_name}.{GlossaryCore.techno_list}': self.technologies_list,
                       f'{self.study_name}.{solid_fuel_name}.CoalExtraction.{GlossaryCore.MarginValue}': self.margin,
                       f'{self.study_name}.{solid_fuel_name}.Pelletizing.{GlossaryCore.MarginValue}': self.margin,
                       f'{self.study_name}.{solid_fuel_name}.{GlossaryCore.TransportCostValue}': self.transport,
                       f'{self.study_name}.{solid_fuel_name}.{GlossaryCore.TransportMarginValue}': self.margin,

                       f'{self.study_name}.{solid_fuel_name}.invest_techno_mix': investment_mix,
                       }

        if self.main_study:
            values_dict.update(
                {f'{self.study_name}.{solid_fuel_name}.{GlossaryCore.InvestLevelValue}': self.invest_level,
                 f'{self.study_name}.{energy_mix_name}.{GlossaryCore.EnergyCO2EmissionsValue}': self.energy_carbon_emissions,
                 f'{self.study_name}.{GlossaryCore.CO2TaxesValue}': self.co2_taxes,
                 f'{self.study_name}.{energy_mix_name}.{GlossaryCore.EnergyPricesValue}': self.energy_prices,
                 })
            if self.invest_discipline == INVEST_DISCIPLINE_OPTIONS[1]:
                investment_mix_sum = investment_mix.drop(
                    columns=[GlossaryCore.Years]).sum(axis=1)
                for techno in self.technologies_list:
                    invest_level_techno = pd.DataFrame({GlossaryCore.Years: self.invest_level[GlossaryCore.Years].values,
                                                        GlossaryCore.InvestValue: self.invest_level[GlossaryCore.InvestValue].values * investment_mix[techno].values / investment_mix_sum})
                    values_dict[f'{self.study_name}.{solid_fuel_name}.{techno}.{GlossaryCore.InvestLevelValue}'] = invest_level_techno
            else:
                values_dict[f'{self.study_name}.{solid_fuel_name}.{GlossaryCore.InvestLevelValue}'] = self.invest_level
        else:
            self.update_dv_arrays()
        return [values_dict]


if '__main__' == __name__:
    uc_cls = Study(main_study=True,
                   technologies_list=DEFAULT_TECHNOLOGIES_LIST)
    uc_cls.load_data()
    uc_cls.run()
#     ppf = PostProcessingFactory()
#     for disc in uc_cls.execution_engine.root_process.sos_disciplines:
#         filters = ppf.get_post_processing_filters_by_discipline(
#             disc)
#         graph_list = ppf.get_post_processing_by_discipline(
#             disc, filters, as_json=False)
#
#         for graph in graph_list:
#             graph.to_plotly()
