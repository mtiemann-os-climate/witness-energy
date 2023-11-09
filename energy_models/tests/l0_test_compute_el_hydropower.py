'''
Copyright 2022 Airbus SAS
Modifications on 2023/11/07 Copyright 2023 Capgemini

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
import unittest
import pandas as pd
import numpy as np
from os.path import join, dirname

import scipy.interpolate as sc
import matplotlib.pyplot as plt

from climateeconomics.glossarycore import GlossaryCore
from energy_models.models.electricity.hydropower.hydropower_disc import HydropowerDiscipline
from energy_models.models.electricity.hydropower.hydropower import Hydropower
from climateeconomics.core.core_resources.resource_mix.resource_mix import ResourceMixModel
from sostrades_core.execution_engine.execution_engine import ExecutionEngine
from energy_models.core.stream_type.resources_data_disc import get_static_CO2_emissions
from energy_models.core.energy_mix.energy_mix import EnergyMix
from energy_models.core.stream_type.energy_models.electricity import Electricity


class HydropowerTestCase(unittest.TestCase):
    """
    Hydropower prices test class
    """

    def setUp(self):
        '''
        Initialize third data needed for testing
        '''
        years = np.arange(2020, 2051)
        self.resource_list = [
            'oil_resource', 'natural_gas_resource', 'uranium_resource', 'coal_resource']
        self.ratio_available_resource = pd.DataFrame(
            {GlossaryCore.Years: np.arange(2020, 2050 + 1)})
        for types in self.resource_list:
            self.ratio_available_resource[types] = np.linspace(
                1, 1, len(self.ratio_available_resource.index))
        self.invest_level = pd.DataFrame({GlossaryCore.Years: years,
                                          GlossaryCore.InvestValue: np.array([4435750000.0, 4522000000.0, 4608250000.0,
                                                              4694500000.0, 4780750000.0, 4867000000.0,
                                                              4969400000.0, 5071800000.0, 5174200000.0,
                                                              5276600000.0, 5379000000.0, 5364700000.0,
                                                              5350400000.0, 5336100000.0, 5321800000.0,
                                                              5307500000.0, 5293200000.0, 5278900000.0,
                                                              5264600000.0, 5250300000.0, 5236000000.0,
                                                              5221700000.0, 5207400000.0, 5193100000.0,
                                                              5178800000.0, 5164500000.0, 5150200000.0,
                                                              5135900000.0, 5121600000.0, 5107300000.0,
                                                              5093000000.0]) * 1.0e-9})

        co2_taxes_year = [2018, 2020, 2025, 2030, 2035, 2040, 2045, 2050]
        co2_taxes = [14.86, 17.22, 20.27,
                     29.01,  34.05,   39.08,  44.69,   50.29]
        func = sc.interp1d(co2_taxes_year, co2_taxes,
                           kind='linear', fill_value='extrapolate')
        self.co2_taxes = pd.DataFrame(
            {GlossaryCore.Years: years, GlossaryCore.CO2Tax: func(years)})

        self.margin = pd.DataFrame(
            {GlossaryCore.Years: np.arange(2020, 2051), GlossaryCore.MarginValue: np.ones(len(np.arange(2020, 2051))) * 110})

        transport_cost = 11,
        # It is noteworthy that the cost of transmission has generally been held (and can
        # continue to be held)    within the £10-12/MWhr range despite transmission distances
        # increasing by almost an order of magnitude from an average of 20km for the
        # leftmost bar to 170km for the 2020 scenarios / OWPB 2016

        self.transport = pd.DataFrame(
            {GlossaryCore.Years: years, 'transport': np.ones(len(years)) * transport_cost})

        self.resources_price = pd.DataFrame({GlossaryCore.Years: years})
        self.energy_prices = pd.DataFrame({GlossaryCore.Years: years})

        biblio_data_path = join(
            dirname(__file__), 'output_values_check', 'biblio_data.csv')
        self.biblio_data = pd.read_csv(biblio_data_path)
        self.biblio_data = self.biblio_data.loc[self.biblio_data['sos_name']
                                                == 'electricity.Hydropower']
        self.scaling_factor_techno_consumption = 1e3
        self.scaling_factor_techno_production = 1e3
        demand_ratio_dict = dict(
            zip(EnergyMix.energy_list, np.ones((len(years), len(years)))))
        demand_ratio_dict[GlossaryCore.Years] = years
        self.all_streams_demand_ratio = pd.DataFrame(demand_ratio_dict)
        self.is_stream_demand = True
        self.is_apply_resource_ratio = True

    def tearDown(self):
        pass

    def test_01_compute_hydropower_price(self):

        inputs_dict = {GlossaryCore.YearStart: 2020,
                       GlossaryCore.YearEnd: 2050,
                       'techno_infos_dict': HydropowerDiscipline.techno_infos_dict_default,
                       GlossaryCore.InvestLevelValue: self.invest_level,
                       GlossaryCore.InvestmentBeforeYearStartValue: HydropowerDiscipline.invest_before_year_start,
                       GlossaryCore.MarginValue:  self.margin,
                       GlossaryCore.TransportCostValue: self.transport,
                       GlossaryCore.ResourcesPriceValue: self.resources_price,
                       GlossaryCore.EnergyPricesValue: self.energy_prices,
                       GlossaryCore.CO2TaxesValue: self.co2_taxes,
                       GlossaryCore.TransportMarginValue: self.margin,
                       'initial_production': HydropowerDiscipline.initial_production,
                       'initial_age_distrib': HydropowerDiscipline.initial_age_distribution,
                       GlossaryCore.EnergyCO2EmissionsValue: pd.DataFrame(),
                       GlossaryCore.RessourcesCO2EmissionsValue: get_static_CO2_emissions(np.arange(2020, 2051)),
                       'scaling_factor_invest_level': 1e3,
                       'scaling_factor_techno_consumption': self.scaling_factor_techno_consumption,
                       'scaling_factor_techno_production': self.scaling_factor_techno_production,
                       ResourceMixModel.RATIO_USABLE_DEMAND: self.ratio_available_resource,
                       GlossaryCore.AllStreamsDemandRatioValue: self.all_streams_demand_ratio,
                       'is_stream_demand': self.is_stream_demand,
                       'is_apply_resource_ratio': self.is_apply_resource_ratio,
                       'smooth_type': 'smooth_max',
                       'data_fuel_dict': Electricity.data_energy_dict,
                       }

        hydropower_model = Hydropower(HydropowerDiscipline.techno_name)
        hydropower_model.configure_parameters(inputs_dict)
        hydropower_model.configure_parameters_update(inputs_dict)
        price_details = hydropower_model.compute_price()

        # Comparison in $/kWH
        plt.figure()
        plt.xlabel(GlossaryCore.Years)

        plt.plot(price_details[GlossaryCore.Years],
                 price_details[HydropowerDiscipline.techno_name], label='SoSTrades Total')

        plt.plot(price_details[GlossaryCore.Years], price_details['transport'],
                 label='SoSTrades Transport')

        plt.plot(price_details[GlossaryCore.Years], price_details[f'{HydropowerDiscipline.techno_name}_factory'],
                 label='SoSTrades Factory')
        plt.legend()
        plt.ylabel('Price ($/kWh)')
        # plt.show()

    def test_02_compute_hydropower_price_prod_consumption(self):

        inputs_dict = {GlossaryCore.YearStart: 2020,
                       GlossaryCore.YearEnd: 2050,
                       'techno_infos_dict': HydropowerDiscipline.techno_infos_dict_default,
                       GlossaryCore.InvestLevelValue: self.invest_level,
                       GlossaryCore.InvestmentBeforeYearStartValue: HydropowerDiscipline.invest_before_year_start,
                       GlossaryCore.MarginValue:  self.margin,
                       GlossaryCore.TransportCostValue: self.transport,
                       GlossaryCore.ResourcesPriceValue: self.resources_price,
                       GlossaryCore.EnergyPricesValue: self.energy_prices,
                       GlossaryCore.CO2TaxesValue: self.co2_taxes,
                       GlossaryCore.TransportMarginValue: self.margin,
                       'initial_production': HydropowerDiscipline.initial_production,
                       'initial_age_distrib': HydropowerDiscipline.initial_age_distribution,
                       GlossaryCore.EnergyCO2EmissionsValue: pd.DataFrame(),
                       GlossaryCore.RessourcesCO2EmissionsValue: get_static_CO2_emissions(np.arange(2020, 2051)),
                       'scaling_factor_invest_level': 1e3,
                       'scaling_factor_techno_consumption': self.scaling_factor_techno_consumption,
                       'scaling_factor_techno_production': self.scaling_factor_techno_production,
                       ResourceMixModel.RATIO_USABLE_DEMAND: self.ratio_available_resource,
                       GlossaryCore.AllStreamsDemandRatioValue: self.all_streams_demand_ratio,
                       'is_stream_demand': self.is_stream_demand,
                       'is_apply_resource_ratio': self.is_apply_resource_ratio,
                       'smooth_type': 'smooth_max',
                       'data_fuel_dict': Electricity.data_energy_dict,
                       }

        hydropower_model = Hydropower(HydropowerDiscipline.techno_name)
        hydropower_model.configure_parameters(inputs_dict)
        hydropower_model.configure_parameters_update(inputs_dict)
        price_details = hydropower_model.compute_price()
        hydropower_model.compute_consumption_and_production()
        hydropower_model.check_outputs_dict(self.biblio_data)
    
    def test_04_compute_hydropower_power(self):

        inputs_dict = {GlossaryCore.YearStart: 2020,
                       GlossaryCore.YearEnd: 2050,
                       'techno_infos_dict': HydropowerDiscipline.techno_infos_dict_default,
                       GlossaryCore.InvestLevelValue: self.invest_level,
                       GlossaryCore.InvestmentBeforeYearStartValue: HydropowerDiscipline.invest_before_year_start,
                       GlossaryCore.MarginValue:  self.margin,
                       GlossaryCore.TransportCostValue: self.transport,
                       GlossaryCore.ResourcesPriceValue: self.resources_price,
                       GlossaryCore.EnergyPricesValue: self.energy_prices,
                       GlossaryCore.CO2TaxesValue: self.co2_taxes,
                       GlossaryCore.TransportMarginValue: self.margin,
                       'initial_production': HydropowerDiscipline.initial_production,
                       'initial_age_distrib': HydropowerDiscipline.initial_age_distribution,
                       GlossaryCore.EnergyCO2EmissionsValue: pd.DataFrame(),
                       GlossaryCore.RessourcesCO2EmissionsValue: get_static_CO2_emissions(np.arange(2020, 2051)),
                       'scaling_factor_invest_level': 1e3,
                       'scaling_factor_techno_consumption': self.scaling_factor_techno_consumption,
                       'scaling_factor_techno_production': self.scaling_factor_techno_production,
                       ResourceMixModel.RATIO_USABLE_DEMAND: self.ratio_available_resource,
                       GlossaryCore.AllStreamsDemandRatioValue: self.all_streams_demand_ratio,
                       'is_stream_demand': self.is_stream_demand,
                       'is_apply_resource_ratio': self.is_apply_resource_ratio,
                       'smooth_type': 'smooth_max',
                       'data_fuel_dict': Electricity.data_energy_dict,
                       }

        hydropower_model = Hydropower(HydropowerDiscipline.techno_name)
        hydropower_model.configure_parameters(inputs_dict)
        hydropower_model.configure_parameters_update(inputs_dict)
        price_details = hydropower_model.compute_price()
        hydropower_model.compute_consumption_and_production()
        hydropower_model.compute_consumption_and_power_production()

        print(hydropower_model.power_production)

        print(hydropower_model.power_production * hydropower_model.techno_infos_dict['full_load_hours'] / 1000)

        print(hydropower_model.production[f'electricity ({hydropower_model.product_energy_unit})'])

        self.assertLessEqual(list(hydropower_model.production[f'electricity ({hydropower_model.product_energy_unit})'].values),
                            list(hydropower_model.power_production['total_installed_power'] * hydropower_model.techno_infos_dict['full_load_hours'] / 1000 * 1.001) )
        self.assertGreaterEqual(list(hydropower_model.production[f'electricity ({hydropower_model.product_energy_unit})'].values),
                            list(hydropower_model.power_production['total_installed_power'] * hydropower_model.techno_infos_dict['full_load_hours'] / 1000 * 0.999) )

    def test_03_hydropower_discipline(self):

        self.name = 'Test'
        self.model_name = HydropowerDiscipline.techno_name
        self.ee = ExecutionEngine(self.name)
        ns_dict = {'ns_public': self.name,
                   'ns_energy': self.name,
                   'ns_energy_study': self.name,
                   'ns_electricity': self.name,
                   'ns_resource': self.name
                   }
        self.ee.ns_manager.add_ns_def(ns_dict)

        mod_path = 'energy_models.models.electricity.hydropower.hydropower_disc.HydropowerDiscipline'
        builder = self.ee.factory.get_builder_from_module(
            self.model_name, mod_path)

        self.ee.factory.set_builders_to_coupling_builder(builder)

        self.ee.configure()
        self.ee.display_treeview_nodes()

        inputs_dict = {f'{self.name}.{GlossaryCore.YearEnd}': 2050,
                       f'{self.name}.{GlossaryCore.EnergyPricesValue}': self.energy_prices,
                       f'{self.name}.{GlossaryCore.EnergyCO2EmissionsValue}': pd.DataFrame(),
                       f'{self.name}.{self.model_name}.{GlossaryCore.InvestLevelValue}': self.invest_level,
                       f'{self.name}.{GlossaryCore.CO2TaxesValue}': self.co2_taxes,
                       f'{self.name}.{GlossaryCore.TransportMarginValue}': self.margin,
                       f'{self.name}.{GlossaryCore.TransportCostValue}': self.transport,
                       f'{self.name}.{GlossaryCore.ResourcesPriceValue}': self.resources_price,
                       f'{self.name}.{self.model_name}.{GlossaryCore.MarginValue}':  self.margin}

        self.ee.load_study_from_input_dict(inputs_dict)

        self.ee.execute()

        disc = self.ee.dm.get_disciplines_with_name(
            f'{self.name}.{self.model_name}')[0]
        filters = disc.get_chart_filter_list()
        graph_list = disc.get_post_processing_list(filters)
#         for graph in graph_list:
#             graph.to_plotly().show()
# if __name__ == "__main__":
#     unittest.main()
