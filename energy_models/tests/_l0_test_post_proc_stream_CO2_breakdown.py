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
from time import sleep
from shutil import rmtree
from pathlib import Path
from sostrades_core.execution_engine.execution_engine import ExecutionEngine
#from energy_models.sos_processes.energy.MDA.energy_process_v0_mda.usecase import Study
from climateeconomics.sos_processes.iam.witness.witness.usecase_witness_wo_damage_gdp_input import Study as Study
import cProfile
import pstats
from io import StringIO
from os.path import join, dirname
from sostrades_core.tools.post_processing.post_processing_factory import PostProcessingFactory


class PostProcessEnergy(unittest.TestCase):
    def setUp(self):
        """
        setup of test
        """
        self.study_name = 'post-processing'
        self.repo = 'climateeconomics.sos_processes.iam.witness'
        self.proc_name = 'witness'

        self.ee = ExecutionEngine(self.study_name)
        builder = self.ee.factory.get_builder_from_process(repo=self.repo,
                                                           mod_id=self.proc_name)

        self.ee.factory.set_builders_to_coupling_builder(builder)
        self.ee.configure()

        self.usecase = Study()
        self.usecase.study_name = self.study_name
        values_dict = self.usecase.setup_usecase()
        for values_dict_i in values_dict:
            self.ee.load_study_from_input_dict(values_dict_i)
        self.ee.load_study_from_input_dict({f'{self.study_name}.sub_mda_class': 'MDAGaussSeidel',
                                            f'{self.study_name}.max_mda_iter': 2})

        energylist = ['methane', 'hydrogen.gaseous_hydrogen', 'biogas', 'syngas', 'fuel.liquid_fuel', \
                      'fuel.hydrotreated_oil_fuel', 'solid_fuel', 'biomass_dry', \
                      'electricity', 'fuel.biodiesel', 'fuel.ethanol', 'hydrogen.liquid_hydrogen']
        self.namespace_list =[]
        for energ in energylist:
            self.namespace_list.append(f'{self.study_name}.EnergyMix.{energ}')

    def test_post_processing_plots(self): # FIXME: rename and fix docstrings
        """
        Test to check the generation of plots to compare WITNESS to IPCC SSP baseline scenarios 1-5
        """
        self.ee.execute()

        ppf = PostProcessingFactory()

        for itm in self.namespace_list:
            filters = ppf.get_post_processing_filters_by_namespace(self.ee, itm)
            graph_list = ppf.get_post_processing_by_namespace(self.ee, itm, filters,
                                                              as_json=False)

            # FIXME: too many plots. Plot only the tables without index-based (use title?)
            # for graph in graph_list:
            #     graph.to_plotly().show()

            # graph_list[-5].to_plotly().show() # FIXME: biomass_dry plots not showing ?


if '__main__' == __name__:
    cls = PostProcessEnergy()
    cls.setUp()
    cls.test_post_processing_plots()