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

from energy_models.core.stream_type.energy_disc import EnergyDiscipline
from energy_models.core.stream_type.energy_models.heat import hightemperatureheat
from sostrades_core.execution_engine.sos_wrapp import SoSWrapp
import numpy as np
import pandas as pd
class HighHeatDiscipline(EnergyDiscipline):
    # ontology information
    _ontology_data = {
        'label': ' High Heat Energy Model',
        'type': 'Research',
        'source': 'SoSTrades Project',
        'validated': '',
        'validated_by': 'SoSTrades Project',
        'last_modification_date': '',
        'category': '',
        'definition': '',
        'icon': 'fas fa-bong fa-fw',
        'version': '',
    }
    # -- add specific techno inputs to this

    DESC_IN = {'technologies_list': {'type': 'list', 'subtype_descriptor': {'list': 'string'},
                                     'possible_values': hightemperatureheat.default_techno_list,
                                     'default': hightemperatureheat.default_techno_list,
                                     'visibility': EnergyDiscipline.SHARED_VISIBILITY, 'namespace': 'ns_heat_high',
                                     'structuring': True, 'unit': '-'
                                     },
               'data_fuel_dict': {'type': 'dict', 'visibility': EnergyDiscipline.SHARED_VISIBILITY,
                                  'unit': 'defined in dict',
                                  'namespace': 'ns_heat_high', 'default': hightemperatureheat.data_energy_dict},

               # 'flux_input_dict': {'type': 'dict', 'visibility': EnergyDiscipline.SHARED_VISIBILITY,
               #                    'unit': 'defined in dict',
               #                    'namespace': 'ns_heat_high', 'default': hightemperatureheat.data_energy_dict},
               }
    DESC_IN.update(EnergyDiscipline.DESC_IN)
    energy_name = hightemperatureheat.name

    DESC_OUT = EnergyDiscipline.DESC_OUT  # -- add specific techno outputs to this

    def init_execution(self):
        inputs_dict = self.get_sosdisc_inputs()
        self.energy_model = hightemperatureheat(self.energy_name)
        self.energy_model.configure_parameters(inputs_dict)


    # def setup_sos_disciplines(self):
    #     '''
    #     Overload SoSDiscipline setup_sos_disciplines
    #     '''
    #
    #     dynamic_inputs = {}
    #     if 'technologies_list' in self.get_data_in():
    #         self.techno_list = self.get_sosdisc_inputs('technologies_list')
    #         if self.techno_list is not None:
    #             for techno in self.techno_list:
    #                 #print(techno)
    #                 dynamic_inputs[f'{techno}.heat_flux'] = {'type': 'dataframe',
    #                                                              'unit': '$/MWh',
    #                                                              'visibility': SoSWrapp.SHARED_VISIBILITY,
    #                                                              'namespace': 'ns_heat_high'
    #                                                              }
    #     self.add_inputs(dynamic_inputs)
    #
    # def run(self):
    #     '''
    #     Overload SoSDiscipline run
    #     '''
    #
    #     # init dataframes
    #     year_start, year_end = self.get_sosdisc_inputs(
    #         ['year_start', 'year_end'])
    #     years = np.arange(year_start, year_end + 1)
    #     techno_heat_fluxes = pd.DataFrame({'years': years})
    #
    #     for techno in self.techno_list:
    #         techno_heat_flux = self.get_sosdisc_inputs(f'{techno}.heat_flux')
    #         techno_heat_flux = techno_heat_flux.copy()
    #
    #         techno_heat_flux.rename(columns={'heat_flux': f'{techno}.heat_flux'}, inplace=True)
    #
    #         techno_heat_fluxes = pd.concat(
    #             [techno_heat_fluxes, techno_heat_flux.drop('years', axis=1)], axis=1)
    #     outputs_dict = {'energy_heat_flux_detailed': techno_heat_flux
    #                     }
    #     self.store_sos_outputs_values(outputs_dict)





