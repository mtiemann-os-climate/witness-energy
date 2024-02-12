'''
Copyright 2024 Capgemini
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

from energy_models.sos_processes.energy.MDO.energy_mix_optim_process.process import ProcessBuilder as ProccesEnergyMixOptimFull


class ProcessBuilder(ProccesEnergyMixOptimFull):
    # ontology information
    _ontology_data = {
        'label': 'Energy Mix coarse Optim process',
        'description': '',
        'category': '',
        'version': '',
    }
    def __init__(self, ee):
        super().__init__(ee)
        self.sub_process_name = "energy_mix_optim_sub_process_coarse"
