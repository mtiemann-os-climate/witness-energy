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

from os.path import dirname
from sostrades_core.execution_engine.execution_engine import ExecutionEngine

from energy_models.sos_processes.energy.MDA.energy_process_v0_mda.usecase import Study
from sostrades_core.tests.core.abstract_jacobian_unit_test import AbstractJacobianUnittest
from climateeconomics.sos_processes.iam.witness.witness_coarse.usecase_witness_coarse_new import \
    DEFAULT_COARSE_TECHNO_DICT
from energy_models.core.energy_process_builder import INVEST_DISCIPLINE_OPTIONS


class EnergyMixCoarseJacobianTestCase(AbstractJacobianUnittest):
    """
    Energy mix jacobian test class
    """

    #AbstractJacobianUnittest.DUMP_JACOBIAN = True

    def analytic_grad_entry(self):
        return []

    def setUp(self):
        '''
        Initialize third data needed for testing
        '''
        self.name = 'TestAntoine'
        self.ee = ExecutionEngine(self.name)
        self.model_name = 'EnergyMix'

        repo = 'energy_models.sos_processes.energy.MDA'
        builder = self.ee.factory.get_builder_from_process(
            repo, 'energy_process_v0_mda',
            techno_dict=DEFAULT_COARSE_TECHNO_DICT, invest_discipline=INVEST_DISCIPLINE_OPTIONS[2])

        self.ee.factory.set_builders_to_coupling_builder(builder)
        self.ee.configure()
        usecase = Study(execution_engine=self.ee,
                        invest_discipline=INVEST_DISCIPLINE_OPTIONS[2], techno_dict=DEFAULT_COARSE_TECHNO_DICT)
        usecase.study_name = self.name
        values_dict = usecase.setup_usecase()

        self.ee.display_treeview_nodes()
        self.full_values_dict = {}
        for dict_v in values_dict:
            self.full_values_dict.update(dict_v)
        self.full_values_dict[f'{self.name}.epsilon0'] = 1.0
        self.full_values_dict[f'{self.name}.tolerance'] = 1.0e-8
        self.full_values_dict[f'{self.name}.max_mda_iter'] = 50
        self.ee.load_study_from_input_dict(self.full_values_dict)

        self.ee.execute()

        self.disc = self.ee.dm.get_disciplines_with_name(
            f'{self.name}.EnergyMix')[0].mdo_discipline_wrapp.mdo_discipline
        self.energy_list = ['renewable', 'fossil']

    def test_01_energy_mix_discipline_co2_emissions_gt(self):
        inputs_names = []

        inputs_names.extend([
            f'{self.name}.{self.model_name}.{energy}.energy_prices' for energy in self.energy_list if
            energy not in ['carbon_capture', 'carbon_storage']])
        inputs_names.extend([
            f'{self.name}.{self.model_name}.{energy}.energy_production' for energy in self.energy_list if
            energy not in ['carbon_capture', 'carbon_storage']])
        inputs_names.extend(
            [f'{self.name}.{self.model_name}.{energy}.energy_consumption' for energy in self.energy_list if
             energy not in ['carbon_capture', 'carbon_storage']])
        inputs_names.extend(
            [f'{self.name}.CCUS.{energy}.energy_consumption' for energy in ['carbon_capture', 'carbon_storage']])

        inputs_names.extend(
            [f'{self.name}.CCUS.{energy}.energy_production' for energy in ['carbon_capture', 'carbon_storage']])
        inputs_names.extend([
            f'{self.name}.CCUS.{energy}.energy_prices' for energy in ['carbon_capture', 'carbon_storage']])
        inputs_names.extend(
            [f'{self.name}.{self.model_name}.{energy}.CO2_emissions' for energy in self.energy_list if
             energy not in ['carbon_capture', 'carbon_storage']])

        # AbstractJacobianUnittest.DUMP_JACOBIAN = True
        self.check_jacobian(location=dirname(__file__), filename=f'jacobian_coarse_energymix_co2_emissions.pkl',
                            discipline=self.disc, step=1.0e-16, derr_approx='complex_step', threshold=1e-5,
                            local_data=self.disc.local_data,
                            inputs=inputs_names,
                            outputs=[f'{self.name}.{self.model_name}.co2_emissions_needed_by_energy_mix',
                                     f'{self.name}.{self.model_name}.carbon_capture_from_energy_mix',
                                     f'{self.name}.{self.model_name}.energy_mean_price',
                                     f'{self.name}.{self.model_name}.energy_production',
                                     f'{self.name}.{self.model_name}.land_demand_df',
                                     f'{self.name}.{self.model_name}.energy_prices_after_tax'
                                     ])

    def test_02_energy_mix_co2_tax(self):
        inputs_names = [
            f'{self.name}.CO2_taxes']

        energy_mix_output = [f'{self.name}.{self.model_name}.energy_mean_price',
                             f'{self.name}.{self.model_name}.energy_prices_after_tax']
        # AbstractJacobianUnittest.DUMP_JACOBIAN = True
        self.check_jacobian(location=dirname(__file__), filename=f'jacobian_coarse_energy_mix_co2_tax.pkl',
                            discipline=self.disc, step=1.0e-12, derr_approx='complex_step', threshold=1e-5,
                            local_data=self.disc.local_data,
                            inputs=inputs_names, outputs=energy_mix_output)

