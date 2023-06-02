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
import unittest
import pandas as pd
import numpy as np
from os.path import join, dirname

import scipy.interpolate as sc
import matplotlib.pyplot as plt

from energy_models.models.electricity.solar_thermal.solar_thermal_disc import SolarThermalDiscipline
from energy_models.models.electricity.solar_thermal.solar_thermal import SolarThermal

from sostrades_core.execution_engine.execution_engine import ExecutionEngine
from energy_models.core.stream_type.resources_data_disc import get_static_CO2_emissions
from climateeconomics.core.core_resources.resource_mix.resource_mix import ResourceMixModel
from energy_models.core.energy_mix.energy_mix import EnergyMix
from energy_models.core.stream_type.energy_models.electricity import Electricity


class SolarThermalPriceTestCase(unittest.TestCase):
    """
    Solar Thermal prices test class
    """

    def setUp(self):
        '''
        Initialize third data needed for testing
        '''
        years = np.arange(2020, 2051)
        self.resource_list = [
            'oil_resource', 'natural_gas_resource', 'uranium_resource', 'coal_resource']
        self.ratio_available_resource = pd.DataFrame(
            {'years': np.arange(2020, 2050 + 1)})
        for types in self.resource_list:
            self.ratio_available_resource[types] = np.linspace(
                1, 1, len(self.ratio_available_resource.index))

        self.invest_level_2 = pd.DataFrame(
            {'years': years, 'invest': np.ones(len(years)) * 15.0})

        co2_taxes_year = [2018, 2020, 2025, 2030, 2035, 2040, 2045, 2050]
        co2_taxes = [14.86, 17.22, 20.27,
                     29.01,  34.05,   39.08,  44.69,   50.29]
        func = sc.interp1d(co2_taxes_year, co2_taxes,
                           kind='linear', fill_value='extrapolate')

        self.co2_taxes = pd.DataFrame(
            {'years': years, 'CO2_tax': func(years)})
        self.margin = pd.DataFrame(
            {'years': years, 'margin': np.ones(len(years)) * 110.0})

        transport_cost = 11
        # It is noteworthy that the cost of transmission has generally been held (and can
        # continue to be held)    within the �10-12/MWhr range despite transmission distances
        # increasing by almost an order of magnitude from an average of 20km for the
        # leftmost bar to 170km for the 2020 scenarios / OWPB 2016

        self.transport = pd.DataFrame(
            {'years': years, 'transport': np.ones(len(years)) * transport_cost})
        self.resources_price = pd.DataFrame({'years': years})
        self.energy_prices = pd.DataFrame({'years': years})

        biblio_data_path = join(
            dirname(__file__), 'output_values_check', 'biblio_data.csv')
        self.biblio_data = pd.read_csv(biblio_data_path)
        self.biblio_data = self.biblio_data.loc[self.biblio_data['sos_name']
                                                == 'electricity.SolarThermal']
        self.scaling_factor_techno_consumption = 1e3
        self.scaling_factor_techno_production = 1e3
        demand_ratio_dict = dict(
            zip(EnergyMix.energy_list, np.ones((len(years), len(years)))))
        demand_ratio_dict['years'] = years
        self.all_streams_demand_ratio = pd.DataFrame(demand_ratio_dict)
        self.is_stream_demand = True
        self.is_apply_resource_ratio = True

        self.inputs_dict = {'year_start': 2020,
                            'year_end': 2050,
                            'techno_infos_dict': SolarThermalDiscipline.techno_infos_dict_default,
                            'invest_level': self.invest_level_2,
                            'invest_before_ystart': SolarThermalDiscipline.invest_before_year_start,
                            'CO2_taxes': self.co2_taxes,
                            'margin':  self.margin,
                            'transport_cost': self.transport,
                            'transport_margin': self.margin,
                            'resources_price': self.resources_price,
                            'energy_prices': self.energy_prices,
                            'initial_production': SolarThermalDiscipline.initial_production,
                            'initial_age_distrib': SolarThermalDiscipline.initial_age_distribution,
                            'resources_CO2_emissions': get_static_CO2_emissions(np.arange(2020, 2051)),
                            'energy_CO2_emissions': pd.DataFrame(),
                            'scaling_factor_invest_level': 1e3,
                            'scaling_factor_techno_consumption': self.scaling_factor_techno_consumption,
                            'scaling_factor_techno_production': self.scaling_factor_techno_production,
                            ResourceMixModel.RATIO_USABLE_DEMAND: self.ratio_available_resource,
                            'all_streams_demand_ratio': self.all_streams_demand_ratio,
                            'is_stream_demand': self.is_stream_demand,
                            'is_apply_resource_ratio': self.is_apply_resource_ratio,
                            'smooth_type': 'smooth_max',
                            'data_fuel_dict': Electricity.data_energy_dict,
                            }

    def tearDown(self):
        pass

    def test_01_compute_solar_thermal_price(self):

        solar_model = SolarThermal('SolarThermal')
        solar_model.configure_parameters(self.inputs_dict)
        solar_model.configure_parameters_update(self.inputs_dict)
        price_details = solar_model.compute_price()

    def test_02_compute_solar_thermal_price_prod_consumption(self):

        solar_model = SolarThermal('SolarThermal')
        solar_model.configure_parameters(self.inputs_dict)
        solar_model.configure_parameters_update(self.inputs_dict)
        price_details = solar_model.compute_price()
        solar_model.compute_consumption_and_production()

        solar_model.check_outputs_dict(self.biblio_data)

#         pd.set_option('display.max_columns', None)
#         print(price_details)
#         print(production)
#         print(consumption)

    def test_04_compute_solar_pv_power(self):

        self.inputs_dict = {'year_start': 2020,
                            'year_end': 2050,
                            'techno_infos_dict': SolarThermalDiscipline.techno_infos_dict_default,
                            'invest_level': self.invest_level_2,
                            'invest_before_ystart': SolarThermalDiscipline.invest_before_year_start,
                            'CO2_taxes': self.co2_taxes,
                            'margin':  self.margin,
                            'transport_cost': self.transport,
                            'transport_margin': self.margin,
                            'resources_price': self.resources_price,
                            'energy_prices': self.energy_prices,
                            'initial_production': SolarThermalDiscipline.initial_production,
                            'initial_age_distrib': SolarThermalDiscipline.initial_age_distribution,
                            'resources_CO2_emissions': get_static_CO2_emissions(np.arange(2020, 2051)),
                            'energy_CO2_emissions': pd.DataFrame(),
                            'scaling_factor_invest_level': 1e3,
                            'scaling_factor_techno_consumption': self.scaling_factor_techno_consumption,
                            'scaling_factor_techno_production': self.scaling_factor_techno_production,
                            ResourceMixModel.RATIO_USABLE_DEMAND: self.ratio_available_resource,
                            'all_streams_demand_ratio': self.all_streams_demand_ratio,
                            'is_stream_demand': self.is_stream_demand,
                            'is_apply_resource_ratio': self.is_apply_resource_ratio,
                            'smooth_type': 'smooth_max',
                            'data_fuel_dict': Electricity.data_energy_dict,
                            }

        solar_model = SolarThermal('SolarThermal')
        solar_model.configure_parameters(self.inputs_dict)
        solar_model.configure_parameters_update(self.inputs_dict)
        price_details = solar_model.compute_price()
        solar_model.compute_consumption_and_production()
        solar_model.compute_consumption_and_power_production()

        print(solar_model.power_production)

        print(solar_model.power_production * solar_model.techno_infos_dict['full_load_hours'] / 1000)

        print(solar_model.production[f'electricity ({solar_model.product_energy_unit})'])

        self.assertLessEqual(list(solar_model.production[f'electricity ({solar_model.product_energy_unit})'].values),
                            list(solar_model.power_production['total_installed_power'] * solar_model.techno_infos_dict['full_load_hours'] / 1000 * 1.001) )
        self.assertGreaterEqual(list(solar_model.production[f'electricity ({solar_model.product_energy_unit})'].values),
                            list(solar_model.power_production['total_installed_power'] * solar_model.techno_infos_dict['full_load_hours'] / 1000 * 0.999) )

    def test_03_solar_Thermal_discipline(self):

        self.name = 'Test'
        self.model_name = 'Solar_Electricity'
        self.ee = ExecutionEngine(self.name)
        ns_dict = {'ns_public': self.name,
                   'ns_energy': self.name,
                   'ns_energy_study': self.name,
                   'ns_electricity': self.name,
                   'ns_resource': self.name}
        self.ee.ns_manager.add_ns_def(ns_dict)

        mod_path = 'energy_models.models.electricity.solar_thermal.solar_thermal_disc.SolarThermalDiscipline'
        builder = self.ee.factory.get_builder_from_module(
            self.model_name, mod_path)

        self.ee.factory.set_builders_to_coupling_builder(builder)
        self.ee.configure()

        inputs_dict = {f'{self.name}.year_end': 2050,
                       f'{self.name}.energy_prices': self.energy_prices,
                       f'{self.name}.energy_CO2_emissions': pd.DataFrame(),
                       f'{self.name}.{self.model_name}.invest_level': self.invest_level_2,
                       f'{self.name}.CO2_taxes': self.co2_taxes,
                       f'{self.name}.transport_margin': self.margin,
                       f'{self.name}.transport_cost': self.transport,
                       f'{self.name}.resources_price': self.resources_price,
                       f'{self.name}.{self.model_name}.margin':  self.margin}

        self.ee.load_study_from_input_dict(inputs_dict)

        self.ee.execute()

        disc = self.ee.dm.get_disciplines_with_name(
            f'{self.name}.{self.model_name}')[0]
        filters = disc.get_chart_filter_list()
        graph_list = disc.get_post_processing_list(filters)

        # for graph in graph_list:
        #     graph.to_plotly().show()

# if __name__ == "__main__":
#     unittest.main()
