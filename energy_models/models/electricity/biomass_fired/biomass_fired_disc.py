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
'''
mode: python; py-indent-offset: 4; tab-width: 8; coding: utf-8
'''
import pandas as pd
import numpy as np

from energy_models.core.techno_type.disciplines.electricity_techno_disc import ElectricityTechnoDiscipline
from energy_models.models.electricity.biomass_fired.biomass_fired import BiomassFired


class BiomassFiredDiscipline(ElectricityTechnoDiscipline):

    # ontology information
    _ontology_data = {
        'label': 'Biomass Fired Model',
        'type': 'Research',
        'source': 'SoSTrades Project',
        'validated': '',
        'validated_by': 'SoSTrades Project',
        'last_modification_date': '',
        'category': '',
        'definition': '',
        'icon': 'fas fa-burn fa-fw',
        'version': '',
    }

    techno_name = 'BiomassFired'
    lifetime = 25   # Value for CHP units
    construction_delay = 2  # years

    # IEA Data Tables
    # https://www.iea.org/data-and-statistics/data-tables?country=WORLD&energy=Renewables%20%26%20waste&year=2019
    # Gross. elec. prod.: 75742 GWh
    # Electricity plants consumption: 650891 TJ net -> 650891 / 3.6 GWh
    biomass_needs = (650891 / 3.6) / 75742  # ratio without dimension

    # IRENA Power Generation Cost 2019 Report
    # https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2020/Jun/IRENA_Power_Generation_Costs_2019.pdf
    # pages 110 to 119

    # Whole Building Design Guide
    # https://www.wbdg.org/resources/biomass-electricity-generation

    techno_infos_dict_default = {'maturity': 5,
                                 'Opex_percentage': 0.04,   # IRENA (mean of 2% - 6%)
                                 'WACC': 0.075,
                                 'learning_rate': 0,
                                 'lifetime': lifetime,
                                 'lifetime_unit': 'years',
                                 'Capex_init': 3000,    # IRENA (value from Figure 7.1, page 111)
                                 'Capex_init_unit': '$/kW',
                                 'capacity_factor': 0.80,   # IRENA (value from Figure 7.1, page 111)
                                 'biomass_needs': biomass_needs,
                                 'efficiency': 1,
                                 'techno_evo_eff': 'no',  # yes or no
                                 'construction_delay': construction_delay,
                                 'full_load_hours': 8760}

    # From IRENA Data
    # https://public.tableau.com/views/IRENARETimeSeries/Charts?:embed=y&:showVizHome=no&publish=yes&:toolbar=no
    # setup = region: all, techno: bioenergy, sub-techno: biomass, flow: installed_capacity
    # (15.414-9.598)/5 = 1.1632 MW per year increase
    invest_before_year_start = pd.DataFrame(
        {'past years': np.arange(-construction_delay, 0), 'invest': [1.1632*3000/1000, 1.1632*3000/1000]})
    # In G$

    # Initial prod in TWh (2019)
    # IEA Data Tables
    # https://www.iea.org/data-and-statistics/data-tables?country=WORLD&energy=Renewables%20%26%20waste&year=2019
    initial_production = 75.742

    # From IRENA Data
    # https://public.tableau.com/views/IRENARETimeSeries/Charts?:embed=y&:showVizHome=no&publish=yes&:toolbar=no
    # setup = region: all, techno: bioenergy, sub-techno: biomass, flow: installed_capacity
    # (15.414-9.598)/5 = 1.1632 MW per year increase
    # 1.1632 / 15.414 ~= 7.5% added production each year (linear approximation)
    initial_age_distribution = pd.DataFrame({'age': np.arange(1, lifetime),
                                             'distrib': [100-12*7.5, 7.5, 7.5, 7.5, 7.5,
                                                         7.5, 7.5, 7.5, 7.5, 7.5,
                                                         7.5, 7.5, 7.5, 0.0, 0.0,
                                                         0.0, 0.0, 0.0, 0.0, 0.0,
                                                         0.0, 0.0, 0.0, 0.0]})

    DESC_IN = {'techno_infos_dict': {'type': 'dict',
                                     'default': techno_infos_dict_default},
               'initial_production': {'type': 'float', 'unit': 'TWh', 'default': initial_production},
               'initial_age_distrib': {'type': 'dataframe', 'unit': '%', 'default': initial_age_distribution,
                                       'dataframe_descriptor': {'age': ('int',  [0, 100], False),
                                                                'distrib': ('float',  None, True)},
                                       'dataframe_edition_locked': False},
               'invest_before_ystart': {'type': 'dataframe', 'unit': 'G$', 'default': invest_before_year_start,
                                        'dataframe_descriptor': {'past years': ('int',  [-20, -1], False),
                                                                 'invest': ('float',  None, True)},
                                        'dataframe_edition_locked': False},
               }
    # -- add specific techno inputs to this
    DESC_IN.update(ElectricityTechnoDiscipline.DESC_IN)

    def init_execution(self):
        inputs_dict = self.get_sosdisc_inputs()
        self.techno_model = BiomassFired(self.techno_name)
        self.techno_model.configure_parameters(inputs_dict)
