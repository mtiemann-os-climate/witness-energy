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
from energy_models.core.stream_type.energy_type import EnergyType


class LowTemperatureHeat(EnergyType):
    name = 'Low heat temperature'
    short_name = 'low heat'
    default_techno_list = ['HeatPump']
    data_energy_dict = {'maturity': 5,
                        'Highest_Temperature': 100,
                        'Temperature_unit': 'c',
                        }


class MediumTemperatureHeat(EnergyType):

    name = 'Medium heat temperature'
    short_name = 'medium heat'
    default_techno_list = ['HeatPump']
    data_energy_dict = {'maturity': 5,
                        'Highest_Temperature': 400,
                        'Lowest_Temperature': 100,
                        'Temperature_unit': 'c',
                        }


class HighTemperatureHeat(EnergyType):

    name = 'High heat temperature'
    short_name = 'high heat'
    default_techno_list = ['HeatPump']
    data_energy_dict = {'maturity': 5,
                        'density': 100,
                        'Lowest_Temperature': 400,
                        'Temperature_unit': 'c',
                        }
