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
import pickle

from sostrades_core.execution_engine.execution_engine import ExecutionEngine
from energy_models.core.stream_type.resources_data_disc import get_static_CO2_emissions, \
    get_static_prices
from sostrades_core.tests.core.abstract_jacobian_unit_test import AbstractJacobianUnittest

import warnings

warnings.filterwarnings("ignore")


class EthanolJacobianCase(AbstractJacobianUnittest):
    """
    Ethanol Fuel jacobian test class
    """

    # AbstractJacobianUnittest.DUMP_JACOBIAN = True

    def analytic_grad_entry(self):
        return [
            self.test_01_biomass_fermentation_discipline_analytic_grad,
            self.test_02_ethanol_discipline_jacobian,
        ]

    def setUp(self):
        '''
        Initialize third data needed for testing
        '''
        years = np.arange(2020, 2051)
        self.energy_name = 'ethanol'
        self.energy_prices = pd.DataFrame({'years': years, 'electricity': np.ones(len(years)) * 0.135 * 1000,
                                           'biomass_dry': 45.0,
                                           })

        self.energy_carbon_emissions = pd.DataFrame(
            {'years': years,
             'electricity': 0.0,
             'biomass_dry': - 0.64 / 4.86,
             })

        invest = np.array([5093000000.0, 5107300000.0, 5121600000.0, 5135900000.0,
                           5150200000.0, 5164500000.0, 5178800000.0,
                           5221700000.0, 5207400000.0, 5193100000.0,
                           5064600000.0, 4950300000.0, 4836000000.0,
                           4707500000.0, 4793200000.0, 4678900000.0,
                           4550400000.0, 4336100000.0, 4321800000.0,
                           4435750000.0, 4522000000.0, 4608250000.0,
                           4276600000.0, 4379000000.0, 4364700000.0,
                           4169400000.0, 4071800000.0, 4174200000.0,
                           3894500000.0, 3780750000.0, 3567000000.0,
                           ]) * 0.8e-9
        # We use the IEA Kero demand to fake the invest level through years

        self.invest_level = pd.DataFrame({'years': years,
                                          'invest': invest
                                          })
        co2_taxes_year = [2018, 2020, 2025, 2030, 2035, 2040, 2045, 2050]
        co2_taxes = [14.86, 17.22, 20.27, 29.01,
                     34.05, 39.08, 44.69, 50.29]
        func = sc.interp1d(co2_taxes_year, co2_taxes,
                           kind='linear', fill_value='extrapolate')

        self.co2_taxes = pd.DataFrame(
            {'years': years, 'CO2_tax': func(years)})
        self.margin = pd.DataFrame(
            {'years': years, 'margin': np.ones(len(years)) * 110.0})
        self.transport = pd.DataFrame(
            {'years': years, 'transport': np.ones(len(years)) * 200.0})

    def tearDown(self):
        pass

    def test_01_biomass_fermentation_discipline_analytic_grad(self):
        self.name = 'Test'
        self.model_name = 'BiomassFermentation'
        self.ee = ExecutionEngine(self.name)
        ns_dict = {'ns_public': self.name, 'ns_energy': f'{self.name}',
                   'ns_energy_study': f'{self.name}',
                   'ns_ethanol': f'{self.name}',
                   'ns_resource': f'{self.name}'
                   }
        self.ee.ns_manager.add_ns_def(ns_dict)

        mod_path = 'energy_models.models.ethanol.biomass_fermentation.biomass_fermentation_disc.BiomassFermentationDiscipline'
        builder = self.ee.factory.get_builder_from_module(
            self.model_name, mod_path)

        self.ee.factory.set_builders_to_coupling_builder(builder)

        self.ee.configure()
        self.ee.display_treeview_nodes()

        inputs_dict = {f'{self.name}.year_end': 2050,
                       f'{self.name}.energy_prices': self.energy_prices,
                       f'{self.name}.energy_CO2_emissions': self.energy_carbon_emissions,
                       f'{self.name}.{self.model_name}.invest_level': self.invest_level,
                       f'{self.name}.CO2_taxes': self.co2_taxes,
                       f'{self.name}.transport_margin': self.margin,
                       f'{self.name}.transport_cost': self.transport,
                       f'{self.name}.{self.model_name}.margin': self.margin,
                       f'{self.name}.resources_CO2_emissions': get_static_CO2_emissions(np.arange(2020, 2051)),
                       f'{self.name}.resources_price': get_static_prices(np.arange(2020, 2051))}

        self.ee.load_study_from_input_dict(inputs_dict)

        self.ee.execute()

        disc_techno = self.ee.root_process.proxy_disciplines[0].mdo_discipline_wrapp.mdo_discipline
        self.check_jacobian(location=dirname(__file__), filename=f'jacobian_{self.energy_name}_{self.model_name}.pkl',
                            discipline=disc_techno, step=1.0e-16, derr_approx='complex_step', threshold=1e-5,
                            local_data=disc_techno.local_data,
                            inputs=[f'{self.name}.{self.model_name}.invest_level',
                                    f'{self.name}.energy_prices',
                                    f'{self.name}.resources_price',
                                    f'{self.name}.resources_CO2_emissions',
                                    f'{self.name}.energy_CO2_emissions',
                                    f'{self.name}.CO2_taxes'],
                            outputs=[f'{self.name}.{self.model_name}.techno_prices',
                                     f'{self.name}.{self.model_name}.CO2_emissions',
                                     f'{self.name}.{self.model_name}.techno_consumption',
                                     f'{self.name}.{self.model_name}.techno_production'],
                            )


if '__main__' == __name__:
    # AbstractJacobianUnittest.DUMP_JACOBIAN = True
    cls = EthanolJacobianCase()
    cls.setUp()
    cls.test_01_biomass_fermentation_discipline_analytic_grad()
