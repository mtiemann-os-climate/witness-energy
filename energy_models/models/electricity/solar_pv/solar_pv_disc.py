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

import pandas as pd
import numpy as np

from energy_models.models.electricity.solar_pv.solar_pv import SolarPv
from energy_models.core.techno_type.disciplines.electricity_techno_disc import ElectricityTechnoDiscipline


class SolarPvDiscipline(ElectricityTechnoDiscipline):
    """**EnergyModelsDiscipline** is the :class:`~gems.core.discipline.MDODiscipline`
    implementing the computation of Energy Models outputs."""

    # ontology information
    _ontology_data = {
        'label': 'Solar Photovoltaic Energy Model',
        'type': 'Research',
        'source': 'SoSTrades Project',
        'validated': '',
        'validated_by': 'SoSTrades Project',
        'last_modification_date': '',
        'category': '',
        'definition': '',
        'icon': 'fas fa-solar-panel fa-fw',
        'version': '',
    }
    techno_name = 'SolarPv'
    lifetime = 25  # IRENA, EOLES model
    construction_delay = 1
    # Source for Opex percentage, Capex init, capacity factor:
    # IEA 2022, World Energy Outlook 2019,
    # https://www.iea.org/reports/world-energy-outlook-2019, License: CC BY
    # 4.0.
    techno_infos_dict_default = {'maturity': 0,
                                 'product': 'electricity',
                                 'Opex_percentage': 0.021,  # Mean of IEA 2019, EOLES data and others
                                 'CO2_from_production': 0.0,
                                 'CO2_from_production_unit': 'kg/kg',
                                 'fuel_demand': 0.0,
                                 'fuel_demand_unit': 'kWh/kWh',
                                 'elec_demand': 0.0,
                                 'elec_demand_unit': 'kWh/kWh',
                                 'heat_demand': 0.0,
                                 'heat_demand_unit': 'kWh/kgCO2',
                                 'WACC': 0.075,  # Weighted averaged cost of capital. Source IRENA
                                 'learning_rate':  0.18,  # IEA 2011
                                 'lifetime': lifetime,  # should be modified
                                 'lifetime_unit': 'years',
                                 'Capex_init': 1077,  # IEA 2019 Mean of regional value
                                 'Capex_init_unit': '$/kW',
                                 'efficiency': 1.0,  # No need of efficiency here
                                 'full_load_hours': 8760,  # 1577, #Source Audi ?
                                 'water_demand': 0.0,
                                 'water_demand_unit': '',
                                 # IEA Average annual capacity factors by
                                 # technology, 2018 10-21%, IRENA 2019: 18%
                                 'capacity_factor': 0.2,
                                 'density_per_ha': 315059,
                                 'density_per_ha_unit': 'kWh/ha',
                                 'transport_cost_unit': '$/kg',  # check if pertient
                                 'techno_evo_eff': 'no',
                                 'energy_efficiency': 1.0,
                                 'construction_delay': construction_delay, }

    techno_info_dict = techno_infos_dict_default
    initial_production = 700  # in TWh at year_start source IEA 2019
    # Invest before year start in $ source IEA 2019
    invest_before_year_start = pd.DataFrame(
        {'past years': np.arange(-construction_delay, 0), 'invest': [108.0]})

    initial_age_distribution = pd.DataFrame({'age': np.arange(1, lifetime),
                                             'distrib': [20.4, 18.8, 15.2, 10.1, 8.0, 7.6, 5.9, 6, 3.4, 1.5, 1.3, 0.25, 0.19, 0.18,
                                                         0.17, 0.16, 0.15, 0.14, 0.13, 0.12, 0.10, 0.1, 0.1, 0.01]
                                             })

    DESC_IN = {'techno_infos_dict': {'type': 'dict',
                                     'default': techno_infos_dict_default, 'unit': 'defined in dict'},
               'initial_production': {'type': 'float', 'unit': 'TWh', 'default': initial_production},
               'initial_age_distrib': {'type': 'dataframe', 'unit': '%', 'default': initial_age_distribution,
                                       'dataframe_descriptor': {'age': ('int',  [0, 100], False),
                                                                'distrib': ('float',  None, True)},
                                       'dataframe_edition_locked': False},
               'invest_before_ystart': {'type': 'dataframe', 'unit': 'G$', 'default': invest_before_year_start,
                                        'dataframe_descriptor': {'past years': ('int',  [-20, -1], False),
                                                                 'invest': ('float',  None, True)},
                                        'dataframe_edition_locked': False}}
    # -- add specific techno outputs to this
    DESC_IN.update(ElectricityTechnoDiscipline.DESC_IN)

    DESC_OUT = ElectricityTechnoDiscipline.DESC_OUT

    _maturity = 'Research'

    def init_execution(self):
        inputs_dict = self.get_sosdisc_inputs()
        self.techno_model = SolarPv(self.techno_name)
        self.techno_model.configure_parameters(inputs_dict)
