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

import unittest
import pandas as pd
import numpy as np
from os.path import join, dirname
import scipy.interpolate as sc

from climateeconomics.glossarycore import GlossaryCore
from sostrades_core.execution_engine.execution_engine import ExecutionEngine
from energy_models.core.stream_type.resources_data_disc import get_static_CO2_emissions,\
    get_static_prices
from sostrades_core.tests.core.abstract_jacobian_unit_test import AbstractJacobianUnittest

import warnings
warnings.filterwarnings("ignore")


class HydrotreatedOilFuelJacobianCase(AbstractJacobianUnittest):
    """
    Hydrotreated Vegetable Oil Fuel jacobian test class
    """
    #AbstractJacobianUnittest.DUMP_JACOBIAN = True

    def analytic_grad_entry(self):
        return [
            self.test_01_hefa_discipline_analytic_grad,
            self.test_02_hefa_green_discipline_analytic_grad,
        ]

    def setUp(self):
        '''
        Initialize third data needed for testing
        '''
        years = np.arange(2020, 2051)
        self.energy_name = 'hydrotreated_oil_fuel'
        # crude oil price : 1.3$/gallon
        self.energy_prices = pd.DataFrame({GlossaryCore.Years: years, 'electricity': np.ones(len(years)) * 0.135 * 1000,
                                           'hydrogen.gaseous_hydrogen': np.ones(len(years)) * 0.1266023955250543 * 1000,
                                           })

        self.energy_carbon_emissions = pd.DataFrame(
            {GlossaryCore.Years: years,
             'electricity': 0.0,
             'hydrogen.gaseous_hydrogen': 0.0,
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

        self.invest_level = pd.DataFrame({GlossaryCore.Years: years,
                                          GlossaryCore.InvestValue: invest
                                          })
        co2_taxes_year = [2018, 2020, 2025, 2030, 2035, 2040, 2045, 2050]
        co2_taxes = [14.86, 17.22, 20.27, 29.01,
                     34.05,   39.08,  44.69,   50.29]
        func = sc.interp1d(co2_taxes_year, co2_taxes,
                           kind='linear', fill_value='extrapolate')

        self.co2_taxes = pd.DataFrame(
            {GlossaryCore.Years: years, GlossaryCore.CO2Tax: func(years)})
        self.margin = pd.DataFrame(
            {GlossaryCore.Years: years, GlossaryCore.MarginValue: np.ones(len(years)) * 110.0})
        self.transport = pd.DataFrame(
            {GlossaryCore.Years: years, 'transport': np.ones(len(years)) * 200.0})

    def tearDown(self):
        pass

    def test_01_hefa_discipline_analytic_grad(self):

        self.name = 'Test'
        self.model_name = 'HefaDecarboxylation'
        self.ee = ExecutionEngine(self.name)
        ns_dict = {'ns_public': self.name, 'ns_energy': f'{self.name}',
                   'ns_energy_study': f'{self.name}',
                   'ns_hydrotreated_oil_fuel': f'{self.name}',
                   'ns_resource': f'{self.name}'
                   }
        self.ee.ns_manager.add_ns_def(ns_dict)

        mod_path = 'energy_models.models.hydrotreated_oil_fuel.hefa_decarboxylation.hefa_decarboxylation_disc.HefaDecarboxylationDiscipline'
        builder = self.ee.factory.get_builder_from_module(
            self.model_name, mod_path)

        self.ee.factory.set_builders_to_coupling_builder(builder)

        self.ee.configure()
        self.ee.display_treeview_nodes()

        inputs_dict = {f'{self.name}.{GlossaryCore.YearEnd}': 2050,
                       f'{self.name}.{GlossaryCore.EnergyPricesValue}': self.energy_prices,
                       f'{self.name}.{GlossaryCore.EnergyCO2EmissionsValue}': self.energy_carbon_emissions,
                       f'{self.name}.{self.model_name}.{GlossaryCore.InvestLevelValue}': self.invest_level,
                       f'{self.name}.{GlossaryCore.CO2TaxesValue}': self.co2_taxes,
                       f'{self.name}.{GlossaryCore.TransportMarginValue}': self.margin,
                       f'{self.name}.{GlossaryCore.TransportCostValue}': self.transport,
                       f'{self.name}.{self.model_name}.{GlossaryCore.MarginValue}':  self.margin,
                       f'{self.name}.{GlossaryCore.RessourcesCO2EmissionsValue}': get_static_CO2_emissions(np.arange(2020, 2051)),
                       f'{self.name}.{GlossaryCore.ResourcesPriceValue}': get_static_prices(np.arange(2020, 2051))}

        self.ee.load_study_from_input_dict(inputs_dict)

        self.ee.execute()

        disc_techno = self.ee.root_process.proxy_disciplines[0].mdo_discipline_wrapp.mdo_discipline

        self.check_jacobian(location=dirname(__file__), filename=f'jacobian_{self.energy_name}_{self.model_name}.pkl',
                            discipline=disc_techno, step=1.0e-16, derr_approx='complex_step', threshold=1e-5,local_data = disc_techno.local_data,
                            inputs=[f'{self.name}.{self.model_name}.{GlossaryCore.InvestLevelValue}',
                                    f'{self.name}.{GlossaryCore.EnergyPricesValue}',
                                    f'{self.name}.{GlossaryCore.ResourcesPriceValue}',
                                    f'{self.name}.{GlossaryCore.RessourcesCO2EmissionsValue}',
                                    f'{self.name}.{GlossaryCore.EnergyCO2EmissionsValue}',
                                    f'{self.name}.{GlossaryCore.CO2TaxesValue}'],
                            outputs=[f'{self.name}.{self.model_name}.{GlossaryCore.TechnoPricesValue}',
                                     f'{self.name}.{self.model_name}.{GlossaryCore.CO2EmissionsValue}',
                                     f'{self.name}.{self.model_name}.{GlossaryCore.TechnoConsumptionValue}',
                                     f'{self.name}.{self.model_name}.{GlossaryCore.TechnoProductionValue}'],
                            )

    def test_02_hefa_green_discipline_analytic_grad(self):

        self.name = 'Test'
        self.model_name = 'HefaDeoxygenation'
        self.ee = ExecutionEngine(self.name)
        ns_dict = {'ns_public': self.name, 'ns_energy': f'{self.name}',
                   'ns_energy_study': f'{self.name}',
                   'ns_hydrotreated_oil_fuel': f'{self.name}',
                   'ns_resource': f'{self.name}'
                   }
        self.ee.ns_manager.add_ns_def(ns_dict)

        mod_path = 'energy_models.models.hydrotreated_oil_fuel.hefa_deoxygenation.hefa_deoxygenation_disc.HefaDeoxygenationDiscipline'
        builder = self.ee.factory.get_builder_from_module(
            self.model_name, mod_path)

        self.ee.factory.set_builders_to_coupling_builder(builder)

        self.ee.configure()
        self.ee.display_treeview_nodes()

        inputs_dict = {f'{self.name}.{GlossaryCore.YearEnd}': 2050,
                       f'{self.name}.{GlossaryCore.EnergyPricesValue}': self.energy_prices,
                       f'{self.name}.{GlossaryCore.EnergyCO2EmissionsValue}': self.energy_carbon_emissions,
                       f'{self.name}.{self.model_name}.{GlossaryCore.InvestLevelValue}': self.invest_level,
                       f'{self.name}.{GlossaryCore.CO2TaxesValue}': self.co2_taxes,
                       f'{self.name}.{GlossaryCore.TransportMarginValue}': self.margin,
                       f'{self.name}.{GlossaryCore.TransportCostValue}': self.transport,
                       f'{self.name}.{self.model_name}.{GlossaryCore.MarginValue}':  self.margin,
                       f'{self.name}.{GlossaryCore.RessourcesCO2EmissionsValue}': get_static_CO2_emissions(np.arange(2020, 2051)),
                       f'{self.name}.{GlossaryCore.ResourcesPriceValue}': get_static_prices(np.arange(2020, 2051))}

        self.ee.load_study_from_input_dict(inputs_dict)

        self.ee.execute()

        disc_techno = self.ee.root_process.proxy_disciplines[0].mdo_discipline_wrapp.mdo_discipline

        self.check_jacobian(location=dirname(__file__), filename=f'jacobian_{self.energy_name}_{self.model_name}.pkl',
                            discipline=disc_techno, step=1.0e-16, derr_approx='complex_step', threshold=1e-5,local_data = disc_techno.local_data,
                            inputs=[f'{self.name}.{self.model_name}.{GlossaryCore.InvestLevelValue}',
                                    f'{self.name}.{GlossaryCore.EnergyPricesValue}',
                                    f'{self.name}.{GlossaryCore.EnergyCO2EmissionsValue}',
                                    f'{self.name}.{GlossaryCore.RessourcesCO2EmissionsValue}',
                                    f'{self.name}.{GlossaryCore.EnergyCO2EmissionsValue}',
                                    f'{self.name}.{GlossaryCore.CO2TaxesValue}'],
                            outputs=[f'{self.name}.{self.model_name}.{GlossaryCore.TechnoPricesValue}',
                                     f'{self.name}.{self.model_name}.{GlossaryCore.CO2EmissionsValue}',
                                     f'{self.name}.{self.model_name}.{GlossaryCore.TechnoConsumptionValue}',
                                     f'{self.name}.{self.model_name}.{GlossaryCore.TechnoProductionValue}'],
                            )
