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

from energy_models.core.energy_process_builder import EnergyProcessBuilder
from energy_models.core.stream_type.energy_models.syngas import Syngas
from energy_models.sos_processes.energy.techno_mix.liquid_fuel_mix.usecase import TECHNOLOGIES_LIST_FOR_OPT


class ProcessBuilder(EnergyProcessBuilder):

    def __init__(self, ee):
        EnergyProcessBuilder.__init__(self, ee)
        self.techno_list = TECHNOLOGIES_LIST_FOR_OPT

    def get_builders(self):

        ns_study = self.ee.study_name
        energy_mix = 'EnergyMix'
        model_name = 'liquid_fuel'
        ns_dict = {'ns_liquid_fuel': f'{ns_study}.{energy_mix}.{model_name}',
                   'ns_energy': f'{ns_study}.{energy_mix}',
                   'ns_energy_study': f'{ns_study}',
                   'ns_public': f'{ns_study}',
                   'ns_syngas': f'{ns_study}.{energy_mix}.{Syngas.name}',
                   'ns_resource': f'{ns_study}.{energy_mix}'}
        mods_dict = {}
        mods_dict[f'{energy_mix}.{model_name}'] = self.get_stream_disc_path(
            'energy_disciplines', 'LiquidFuel')
        for techno_name in self.techno_list:
            mods_dict[f'{energy_mix}.{model_name}.{techno_name}'] = self.get_techno_disc_path(
                model_name, techno_name)

        builder_list = self.create_builder_list(mods_dict, ns_dict=ns_dict)
        if not self.one_invest_discipline:
            mods_dict_invest = {f'{energy_mix}.{model_name}': 'energy_models.core.investments.disciplines.techno_invest_disc.InvestTechnoDiscipline',
                                }

            builder_list_invest = self.create_builder_list(
                mods_dict_invest, ns_dict=ns_dict)
            builder_list.extend(builder_list_invest)

        return builder_list
