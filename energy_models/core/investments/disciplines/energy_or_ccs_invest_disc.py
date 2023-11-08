'''
mode: python; py-indent-offset: 4; tab-width: 8; coding: utf-8
Copyright (c) 2020 Airbus SAS.
All rights reserved.
'''
import numpy as np

from climateeconomics.glossarycore import GlossaryCore
from energy_models.core.investments.energy_or_ccsinvest import EnergyOrCCSInvest
from sostrades_core.execution_engine.sos_wrapp import SoSWrapp
from sostrades_core.tools.post_processing.charts.chart_filter import ChartFilter
from sostrades_core.tools.post_processing.charts.two_axes_instanciated_chart import InstanciatedSeries, \
    TwoAxesInstanciatedChart


class InvestCCSorEnergyDiscipline(SoSWrapp):

    # ontology information
    _ontology_data = {
        'label': 'Energy Investment CCS Model',
        'type': 'Research',
        'source': 'SoSTrades Project',
        'validated': '',
        'validated_by': 'SoSTrades Project',
        'last_modification_date': '',
        'category': '',
        'definition': '',
        'icon': '',
        'version': '',
    }
    DESC_IN = {
        GlossaryCore.EnergyInvestmentsValue: {'type': 'dataframe', 'unit': '100G$',
                              'dataframe_descriptor': {GlossaryCore.Years: ('int',  [1900, 2100], False),
                                                       GlossaryCore.EnergyInvestmentsValue: ('float',  None, True)},
                              'dataframe_edition_locked': False,
                              'visibility': 'Shared', 'namespace': 'ns_witness'},
        'ccs_percentage': {'type': 'dataframe',
                           'dataframe_descriptor': {GlossaryCore.Years: ('int',  [1900, 2100], False),
                                                    'ccs_percentage': ('float',  [0., 100.], True)},
                           'dataframe_edition_locked': False,
                           'visibility': 'Shared', 'namespace': 'ns_ccs'}
    }

    DESC_OUT = {
        GlossaryCore.EnergyInvestmentsValue: {'type': 'dataframe', 'unit': '100G$',
                              'visibility': 'Shared', 'namespace': 'ns_energy_mix'},
        'ccs_investment': {'type': 'dataframe', 'unit': 'G$',
                           'visibility': 'Shared', 'namespace': 'ns_ccs'}
    }
    _maturity = 'Research'
    rescaling_factor = 1e2

    def init_execution(self):
        self.energy_model = EnergyOrCCSInvest()

    def run(self):

        input_dict = self.get_sosdisc_inputs()

        self.energy_model.configure(input_dict)

        self.energy_model.compute()

        ccs_invest = self.energy_model.get_ccs_investment(
            self.rescaling_factor)
        energy_conversion_investment = self.energy_model.get_energy_conversion_investment()

        output_dict = {'ccs_investment': ccs_invest,
                       GlossaryCore.EnergyInvestmentsValue: energy_conversion_investment}

        self.store_sos_outputs_values(output_dict)

    def compute_sos_jacobian(self):

        inputs_dict = self.get_sosdisc_inputs()
        len_grad = len(inputs_dict['ccs_percentage']['ccs_percentage'].values)
        self.set_partial_derivative_for_other_types(
            ('ccs_investment', GlossaryCore.EnergyInvestmentsValue), (GlossaryCore.EnergyInvestmentsValue,
                                                      GlossaryCore.EnergyInvestmentsValue),
            np.identity(len_grad) * inputs_dict['ccs_percentage']['ccs_percentage'].values / 100.0 * self.rescaling_factor)

        self.set_partial_derivative_for_other_types(
            (GlossaryCore.EnergyInvestmentsValue,
             GlossaryCore.EnergyInvestmentsValue), (GlossaryCore.EnergyInvestmentsValue, GlossaryCore.EnergyInvestmentsValue),
            np.identity(len_grad) * (1.0 - inputs_dict['ccs_percentage']['ccs_percentage'].values / 100.0))

        self.set_partial_derivative_for_other_types(
            ('ccs_investment', GlossaryCore.EnergyInvestmentsValue), ('ccs_percentage', 'ccs_percentage'),
            np.identity(len_grad) * inputs_dict[GlossaryCore.EnergyInvestmentsValue][GlossaryCore.EnergyInvestmentsValue].values / 100.0 * self.rescaling_factor)

        self.set_partial_derivative_for_other_types(
            (GlossaryCore.EnergyInvestmentsValue,
             GlossaryCore.EnergyInvestmentsValue), ('ccs_percentage', 'ccs_percentage'),
            -np.identity(len_grad) * inputs_dict[GlossaryCore.EnergyInvestmentsValue][GlossaryCore.EnergyInvestmentsValue].values / 100.0)

    def get_chart_filter_list(self):

        chart_filters = []
        chart_list = ['Global Invest Distribution']
        chart_filters.append(ChartFilter(
            'Charts Investments', chart_list, chart_list, 'charts_invest'))

        return chart_filters

    def get_post_processing_list(self, filters=None):

        # For the outputs, making a graph for block fuel vs range and blocktime vs
        # range

        instanciated_charts = []
        charts = []
        # Overload default value with chart filter
        if filters is not None:
            for chart_filter in filters:
                if chart_filter.filter_key == 'charts_invest':
                    charts = chart_filter.selected_values

        if 'Global Invest Distribution' in charts:

            ccs_percentage = self.get_sosdisc_inputs(
                'ccs_percentage')['ccs_percentage'].values / 100.0
            total_energy_investment = self.get_sosdisc_inputs(
                GlossaryCore.EnergyInvestmentsValue)

            chart_name = 'Distribution of Investments into CCS and Energy Conversion'

            new_chart = TwoAxesInstanciatedChart(GlossaryCore.Years, 'Invest [G$]',
                                                 chart_name=chart_name, stacked_bar=True)

            total_invest = total_energy_investment[GlossaryCore.EnergyInvestmentsValue].values * \
                self.rescaling_factor
            e_invest = total_invest * (1.0 - ccs_percentage)
            serie = InstanciatedSeries(
                total_energy_investment[GlossaryCore.Years].values.tolist(),
                e_invest.tolist(), 'Energy conversion', 'bar')

            new_chart.series.append(serie)
            ccs_investment = total_invest * ccs_percentage
            serie = InstanciatedSeries(
                total_energy_investment[GlossaryCore.Years].values.tolist(),
                ccs_investment.tolist(), 'CCS', 'bar')
            new_chart.series.append(serie)

            serie = InstanciatedSeries(
                total_energy_investment[GlossaryCore.Years].values.tolist(),
                total_invest.tolist(), 'Total', 'lines')
            new_chart.series.append(serie)
            instanciated_charts.append(new_chart)
        return instanciated_charts
