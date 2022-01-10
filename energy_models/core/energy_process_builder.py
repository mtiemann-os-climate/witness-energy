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
import re
from sos_trades_core.sos_processes.base_process_builder import BaseProcessBuilder


class EnergyProcessBuilder(BaseProcessBuilder):
    def __init__(self, ee):
        BaseProcessBuilder.__init__(self, ee)
        self.techno_list = None
        self.one_invest_discipline = False

    def setup_process(self, techno_list, one_invest_discipline=False):
        self.techno_list = techno_list
        self.one_invest_discipline = one_invest_discipline

    def get_stream_disc_path(self, stream, substream_name):
        list_name = re.findall('[A-Z][^A-Z]*', substream_name)
        mod_name = "_".join(l.lower() for l in list_name)
        disc_name = f'{mod_name}_disc'
        energy_path = f'energy_models.core.stream_type.{stream}.{disc_name}.{substream_name}Discipline'
        return energy_path

    def get_techno_disc_path(self, energy_name, techno_name, sub_dir=None):
        list_name = re.findall('[A-Z][^A-Z]*', techno_name)
        test = [len(l) for l in list_name]
        #-- in case only one letter is capital, support all are capital and don't add _
        if 1 in test:
            mod_name = "".join(l.lower() for l in list_name)
        else:
            mod_name = "_".join(l.lower() for l in list_name)
        #--case of CO2... to be generalized
        if '2' in mod_name:
            mod_name = "2_".join(mod_name.split('2'))
        #-- try to find rule for electrolysis case
        #-- get correct disc name in case of dot in name
        dot_plit = mod_name.split('.')
        dot_name = "_".join(dot_plit)
        disc_name = f'{dot_name}_disc'
        #-- fix techno name in case of dot in name
        dot_tech_split = techno_name.split('.')
        mod_techno_name = "".join(dot_tech_split)

        if sub_dir is not None:
            techno_path = f'energy_models.models.{energy_name}.{sub_dir}.{mod_name}.{disc_name}.{mod_techno_name}Discipline'
        else:
            techno_path = f'energy_models.models.{energy_name}.{mod_name}.{disc_name}.{mod_techno_name}Discipline'
        return techno_path
