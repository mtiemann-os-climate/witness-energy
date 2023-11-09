'''
Copyright 2022 Airbus SAS
Modifications on 2023/06/14-2023/11/09 Copyright 2023 Capgemini

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

from climateeconomics.glossarycore import GlossaryCore
from energy_models.core.techno_type.disciplines.hydrotreated_oil_fuel_techno_disc import \
    HydrotreatedOilFuelTechnoDiscipline
from energy_models.models.hydrotreated_oil_fuel.hefa_decarboxylation.hefa_decarboxylation import \
    HefaDecarboxylation
from energy_models.core.stream_type.energy_models.hydrotreated_oil_fuel import HydrotreatedOilFuel


class HefaDecarboxylationDiscipline(HydrotreatedOilFuelTechnoDiscipline):

    # ontology information
    _ontology_data = {
        'label': 'HEFA decarboxylation',
        'type': 'Research',
        'source': 'SoSTrades Project',
        'validated': '',
        'validated_by': 'SoSTrades Project',
        'last_modification_date': '',
        'category': '',
        'definition': '',
        'icon': 'fa-solid fa-gas-pump fa-fw',
        'version': '',
    }
    # -- add specific techno inputs to this
    techno_name = 'HefaDecarboxylation'
    energy_name = HydrotreatedOilFuel.name
    # Source:
    # https://biotechnologyforbiofuels.biomedcentral.com/articles/10.1186/s13068-017-0945-3/tables/2
    lifetime = 30   # years
    construction_delay = 3  # years

    # conversion factors
    dollar_per_gallon_to_dollar_per_m3 = 264.17
    gallon_to_mc = 0.00378541

    techno_infos_dict_default = {

        'Opex_percentage': 0.0715,
        # https://dspace.mit.edu/bitstream/handle/1721.1/65508/746766700-MIT.pdf?sequence=2&isAllowed=y
        # (page 67)

        'lifetime': lifetime,  # for now constant in time but should increase with time
        'lifetime_unit': GlossaryCore.Years,
        'construction_delay': construction_delay,
        'construction_delay_unit': GlossaryCore.Years,

        'Invest_init': 347.5,
        'Invest_init_unit': 'M$',
        'Capex_init': 347.5 * 1e6 * dollar_per_gallon_to_dollar_per_m3 / 780
        / (48.64 * 1e6),
        # https://biotechnologyforbiofuels.biomedcentral.com/articles/10.1186/s13068-017-0945-3
        # Mean value computed for production volume (mean value)
        'Capex_init_unit': '$/kg',

        'efficiency': 0.753,     # https://core.ac.uk/download/pdf/37440495.pdf

        'CO2_from_production': 0.03 * 44,
        # https://theicct.org/sites/default/files/publications/Alt-aviation-fuel-sustainability-mar2021.pdf
        # to review
        'CO2_from_production_unit': 'kg/kg',

        'maturity': 5,
        'learning_rate': 0.1,

        'full_load_hours': 7920.0,

        'WACC': 0.0878,
        'techno_evo_eff': 'no',
    }

    # Source: IEA 2022, Data and Statistics,
    # https://www.iea.org/data-and-statistics/charts/global-biofuel-production-in-2019-and-forecast-to-2025,
    # License: CC BY 4.0.
    # 9 bl of HVO/HEFA in 2020
    # https://www.ieabioenergy.com/wp-content/uploads/2021/06/IEA-Bioenergy-Task-39-Progress-in-the-commercialisation-of-biojet-fuels-May-2021-1.pdf
    # most current commercial HEFA production removes oxygen through the
    # addition of hydrogen : hypothesis only 10% of decarboxylation
    initial_production = 9e6 * \
        HydrotreatedOilFuel.data_energy_dict['density'] * \
        HydrotreatedOilFuel.data_energy_dict['calorific_value'] * 0.1 / 1e9
    # https://www.ieabioenergy.com/wp-content/uploads/2021/06/IEA-Bioenergy-Task-39-Progress-in-the-commercialisation-of-biojet-fuels-May-2021-1.pdf
    # (page 23)
    # Existing: Neste(2014), Total(2015), Eni(2015).
    # Source
    # https://www.etipbioenergy.eu/value-chains/products-end-use/products/hvo-hefa
    initial_age_distribution = pd.DataFrame({'age': np.arange(1, lifetime),
                                             'distrib': [100 * 3 / 6, 0, 0, 0, 100 * 2 / 6, 100 * 1 / 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                         0, 0, 0, 0, 0, 0, 0, 0, 0, 0]})

    invest_before_year_start = pd.DataFrame(
        {'past years': np.arange(-construction_delay, 0), GlossaryCore.InvestValue: [347.5 / 1000 * i for i in [0.0, 0.0, 3.0]]})  # in G$

    DESC_IN = {'techno_infos_dict': {'type': 'dict',
                                     'default': techno_infos_dict_default, 'unit': 'defined in dict'},
               'initial_production': {'type': 'float', 'unit': 'TWh', 'default': initial_production},
               'initial_age_distrib': {'type': 'dataframe', 'unit': '%', 'default': initial_age_distribution,
                                       'dataframe_descriptor': {GlossaryCore.Years: ('float', None, True),
                                                                'age': ('float', None, True),
                                                                'distrib': ('float', None, True)}
                                       },
               GlossaryCore.InvestmentBeforeYearStartValue: {'type': 'dataframe', 'unit': 'G$', 'default': invest_before_year_start,
                                        'dataframe_descriptor': {'past years': ('int',  [-20, -1], False),
                                                                 GlossaryCore.InvestValue: ('float',  None, True)},
                                        'dataframe_edition_locked': False}}
    DESC_IN.update(HydrotreatedOilFuelTechnoDiscipline.DESC_IN)
    # -- add specific techno outputs to this
    DESC_OUT = HydrotreatedOilFuelTechnoDiscipline.DESC_OUT

    def init_execution(self):
        inputs_dict = self.get_sosdisc_inputs()
        self.techno_model = HefaDecarboxylation(self.techno_name)
        self.techno_model.configure_parameters(inputs_dict)
