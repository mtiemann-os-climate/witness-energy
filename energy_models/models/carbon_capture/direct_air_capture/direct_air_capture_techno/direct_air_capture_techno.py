'''
Copyright 2022 Airbus SAS
Modifications on 2023/11/09-2023/11/15 Copyright 2023 Capgemini

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

from energy_models.core.stream_type.carbon_models.carbon_capture import CarbonCapture
from energy_models.core.stream_type.energy_models.fossil import Fossil
from energy_models.core.stream_type.energy_models.renewable import Renewable
from energy_models.core.techno_type.base_techno_models.carbon_capture_techno import CCTechno
from energy_models.glossaryenergy import GlossaryEnergy


class DirectAirCaptureTechno(CCTechno):


    def compute_other_energies_needs(self):
        self.cost_details[f'{GlossaryEnergy.renewable}_needs'] = self.get_electricity_needs()
        self.cost_details[f'{Fossil.name}_needs'] = self.get_heat_needs()

    def compute_production(self):

        self.production_detailed[f'{CarbonCapture.flue_gas_name} ({self.mass_unit})'] = self.cost_details[
                                                                                            f'{Fossil.name}_needs'] * \
                                                                                        self.production_detailed[
                                                                                            f'{CCTechno.energy_name} ({self.product_energy_unit})'] * \
                                                                                        Fossil.data_energy_dict[
                                                                                            GlossaryEnergy.CO2PerUse] / \
                                                                                        Fossil.data_energy_dict[
                                                                                            'calorific_value']