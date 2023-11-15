'''
Copyright 2022 Airbus SAS
Modifications on 2023/10/23-2023/11/03 Copyright 2023 Capgemini

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
from climateeconomics.glossarycore import GlossaryCore
from energy_models.core.stream_type.carbon_models.carbon_capture import CarbonCapture
from energy_models.core.techno_type.techno_disc import TechnoDiscipline
from energy_models.glossaryenergy import GlossaryEnergy
from sostrades_core.tools.post_processing.charts.chart_filter import ChartFilter
from sostrades_core.tools.post_processing.charts.two_axes_instanciated_chart \
    import InstanciatedSeries, TwoAxesInstanciatedChart

import numpy as np


class CCTechnoDiscipline(TechnoDiscipline):

    # ontology information
    _ontology_data = {
        'label': 'Carbon Capture Techology Model',
        'type': 'Research',
        'source': 'SoSTrades Project',
        'validated': '',
        'validated_by': 'SoSTrades Project',
        'last_modification_date': '',
        'category': '',
        'definition': '',
        'icon': 'fas fa-air-freshener fa-fw',
        'version': '',
    }
    DESC_IN = {GlossaryCore.TransportCostValue: {'type': 'dataframe', 'unit': '$/t', 'visibility': TechnoDiscipline.SHARED_VISIBILITY,
                                  'namespace': 'ns_carbon_capture',
                                  'dataframe_descriptor': {GlossaryCore.Years: ('int',  [1900, 2100], False),
                                                           'transport': ('float',  None, True)},
                                  'dataframe_edition_locked': False},
               GlossaryCore.TransportMarginValue: {'type': 'dataframe', 'unit': '%', 'visibility': TechnoDiscipline.SHARED_VISIBILITY,
                                    'namespace': 'ns_carbon_capture',
                                    'dataframe_descriptor': {GlossaryCore.Years: ('int',  [1900, 2100], False),
                                                             GlossaryCore.MarginValue: ('float',  None, True)},
                                    'dataframe_edition_locked': False},
               'fg_ratio_effect': {'type': 'bool', 'visibility': TechnoDiscipline.SHARED_VISIBILITY,
                                   'namespace': 'ns_carbon_capture', 'default': True},
               'data_fuel_dict': {'type': 'dict', 'visibility': TechnoDiscipline.SHARED_VISIBILITY,
                                  'namespace': 'ns_carbon_capture', 'default': CarbonCapture.data_energy_dict,
                                  'unit': 'defined in dict'},

               }
    DESC_IN.update(TechnoDiscipline.DESC_IN)

    _maturity = 'Research'

    energy_name = CarbonCapture.name

    def set_partial_derivatives_flue_gas(self, energy_name='electricity'):

        inputs_dict = self.get_sosdisc_inputs()
        scaling_factor_invest_level = inputs_dict['scaling_factor_invest_level']
        scaling_factor_techno_consumption = self.get_sosdisc_inputs(
            'scaling_factor_techno_consumption')
        scaling_factor_techno_production = self.get_sosdisc_inputs(
            'scaling_factor_techno_production')
        dcapex_dfluegas = self.techno_model.compute_dcapex_dfg_ratio(
            inputs_dict[GlossaryCore.FlueGasMean][GlossaryCore.FlueGasMean].values,
            inputs_dict[GlossaryCore.InvestLevelValue].loc[inputs_dict[GlossaryCore.InvestLevelValue][GlossaryCore.Years] <=
                                            inputs_dict[GlossaryCore.YearEnd]][GlossaryCore.InvestValue].values,
            inputs_dict['techno_infos_dict'], inputs_dict['fg_ratio_effect'])

        crf = self.techno_model.compute_crf(inputs_dict['techno_infos_dict'])
        dfactory_dfluegas = dcapex_dfluegas * \
            (crf + inputs_dict['techno_infos_dict']['Opex_percentage'])

        delec_dflue_gas = self.techno_model.compute_delec_dfg_ratio(
            inputs_dict[GlossaryCore.FlueGasMean][GlossaryCore.FlueGasMean].values, inputs_dict['fg_ratio_effect'], energy_name)

        margin = inputs_dict[GlossaryCore.MarginValue].loc[inputs_dict[GlossaryCore.MarginValue][GlossaryCore.Years]
                                           <= inputs_dict[GlossaryCore.YearEnd]][GlossaryCore.MarginValue].values

        dprice_dfluegas = (dfactory_dfluegas + delec_dflue_gas) * np.split(margin, len(margin)) / \
            100.0

        self.set_partial_derivative_for_other_types(
            (GlossaryCore.TechnoPricesValue, f'{self.techno_name}'), (GlossaryCore.FlueGasMean, GlossaryCore.FlueGasMean), dprice_dfluegas)

        self.set_partial_derivative_for_other_types(
            (GlossaryCore.TechnoPricesValue, f'{self.techno_name}_wotaxes'), (GlossaryCore.FlueGasMean, GlossaryCore.FlueGasMean), dprice_dfluegas)

        capex = self.get_sosdisc_outputs(GlossaryCore.TechnoDetailedPricesValue)[
            f'Capex_{self.techno_name}'].values

        dprod_dfluegas = self.techno_model.compute_dprod_dfluegas(
            capex, inputs_dict[GlossaryCore.InvestLevelValue][GlossaryCore.InvestValue].values,
            inputs_dict[GlossaryCore.InvestmentBeforeYearStartValue][GlossaryCore.InvestValue].values,
            inputs_dict['techno_infos_dict'], dcapex_dfluegas)

        self.set_partial_derivative_for_other_types(
            (GlossaryCore.TechnoProductionValue, f'{self.energy_name} ({self.techno_model.product_energy_unit})'), (
                GlossaryCore.FlueGasMean, GlossaryCore.FlueGasMean),
            dprod_dfluegas * self.techno_model.applied_ratio['applied_ratio'].values[:, np.newaxis] * scaling_factor_invest_level / scaling_factor_techno_production)

        production, consumption = self.get_sosdisc_outputs(
            [GlossaryCore.TechnoProductionValue, GlossaryCore.TechnoConsumptionValue])
        for column in consumption:
            dprod_column_dfluegas = dprod_dfluegas.copy()
            if column != GlossaryCore.Years:
                var_cons = (consumption[column] /
                            production[f'{self.energy_name} ({self.techno_model.product_energy_unit})']).fillna(
                    0)
                for line in range(len(consumption[column].values)):
                    dprod_column_dfluegas[line, :] = dprod_dfluegas[line,
                                                                    :] * var_cons[line]
                self.set_partial_derivative_for_other_types(
                    (GlossaryCore.TechnoConsumptionValue, column), (GlossaryCore.FlueGasMean, GlossaryCore.FlueGasMean),
                    dprod_column_dfluegas * self.techno_model.applied_ratio['applied_ratio'].values[:, np.newaxis] * scaling_factor_invest_level / scaling_factor_techno_production)
                self.set_partial_derivative_for_other_types(
                    (GlossaryCore.TechnoConsumptionWithoutRatioValue,
                     column), (GlossaryCore.FlueGasMean, GlossaryCore.FlueGasMean),
                    dprod_column_dfluegas * scaling_factor_invest_level / scaling_factor_techno_production)

        dnon_use_capital_dflue_gas_mean, dtechnocapital_dflue_gas_mean = self.techno_model.compute_dnon_usecapital_dfluegas(
            dcapex_dfluegas, dprod_dfluegas)

        self.set_partial_derivative_for_other_types(
            ('non_use_capital', self.techno_model.name), (GlossaryCore.FlueGasMean, GlossaryCore.FlueGasMean), dnon_use_capital_dflue_gas_mean)
        self.set_partial_derivative_for_other_types(
            (GlossaryEnergy.TechnoCapitalValue, GlossaryEnergy.Capital),
            (GlossaryCore.FlueGasMean, GlossaryCore.FlueGasMean), dtechnocapital_dflue_gas_mean)

    def get_chart_filter_list(self):

        chart_filters = super().get_chart_filter_list()
        chart_filters[0].remove(
            [
                'CO2 emissions',
                'Non-Use Capital',
                'Power production',
                'Factory Mean Age'
            ]
        )
        return chart_filters

    def get_post_processing_list(self, filters=None):

        # For the outputs, making a graph for block fuel vs range and blocktime vs
        # range

        instanciated_charts = []
        charts = []
        price_unit_list = ['$/tCO2']
        # Overload default value with chart filter
        if filters is not None:
            for chart_filter in filters:
                if chart_filter.filter_key == 'charts':
                    charts = chart_filter.selected_values
                if chart_filter.filter_key == 'price_unit':
                    price_unit_list = chart_filter.selected_values

        if 'Detailed prices' in charts and '$/tCO2' in price_unit_list:
            new_chart = self.get_chart_detailed_price_in_dollar_tCO2()
            if new_chart is not None:
                instanciated_charts.append(new_chart)

        if GlossaryCore.UtilisationRatioValue in charts:
            new_chart = self.get_utilisation_ratio_chart()
            instanciated_charts.append(new_chart)

        if 'Consumption and production' in charts:
            new_chart = self.get_chart_investments()
            if new_chart is not None:
                instanciated_charts.append(new_chart)

            new_charts = self.get_charts_consumption_and_production()
            for new_chart in new_charts:
                if new_chart is not None:
                    instanciated_charts.append(new_chart)

            new_charts = self.get_charts_consumption_and_production_energy()
            for new_chart in new_charts:
                if new_chart is not None:
                    instanciated_charts.append(new_chart)

        if 'Applied Ratio' in charts:
            new_chart = self.get_chart_applied_ratio()
            if new_chart is not None:
                instanciated_charts.append(new_chart)

        if 'Initial Production' in charts:
            if 'initial_production' in self.get_data_in():
                new_chart = self.get_chart_initial_production()
                if new_chart is not None:
                    instanciated_charts.append(new_chart)

        return instanciated_charts

    def get_chart_detailed_price_in_dollar_tCO2(self):

        techno_detailed_prices = self.get_sosdisc_outputs(
            GlossaryCore.TechnoDetailedPricesValue)

        chart_name = f'Detailed prices of {self.techno_name} technology over the years'
        year_start = min(techno_detailed_prices[GlossaryCore.Years].values.tolist())
        year_end = max(techno_detailed_prices[GlossaryCore.Years].values.tolist())
        minimum = 0
        maximum = max(
            (techno_detailed_prices[self.techno_name].values).tolist()) * 1.2

        new_chart = TwoAxesInstanciatedChart(GlossaryCore.Years, 'Prices [$/tCO2]', [year_start, year_end], [minimum, maximum],
                                             chart_name=chart_name)

        if 'percentage_resource' in self.get_data_in():
            percentage_resource = self.get_sosdisc_inputs(
                'percentage_resource')
            new_chart.annotation_upper_left = {
                'Percentage of total price at starting year': f'{percentage_resource[self.energy_name][0]} %'}
            tot_price = (techno_detailed_prices[self.techno_name].values) / \
                (percentage_resource[self.energy_name] / 100.)
            serie = InstanciatedSeries(
                techno_detailed_prices[GlossaryCore.Years].values.tolist(),
                tot_price.tolist(), 'Total price without percentage', 'lines')
            new_chart.series.append(serie)
        # Add total price
        serie = InstanciatedSeries(
            techno_detailed_prices[GlossaryCore.Years].values.tolist(),
            (techno_detailed_prices[self.techno_name].values).tolist(), 'Total price with margin', 'lines')

        new_chart.series.append(serie)

        # Factory price
        serie = InstanciatedSeries(
            techno_detailed_prices[GlossaryCore.Years].values.tolist(),
            (techno_detailed_prices[f'{self.techno_name}_factory'].values).tolist(), 'Factory', 'lines')

        new_chart.series.append(serie)

        if 'energy_costs' in techno_detailed_prices:
            # energy_costs
            serie = InstanciatedSeries(
                techno_detailed_prices[GlossaryCore.Years].values.tolist(),
                (techno_detailed_prices['energy_costs'].values).tolist(), 'Energy costs', 'lines')

            new_chart.series.append(serie)

        # Transport price
        serie = InstanciatedSeries(
            techno_detailed_prices[GlossaryCore.Years].values.tolist(),
            (techno_detailed_prices['transport'].values).tolist(), 'Transport', 'lines')

        new_chart.series.append(serie)
        # CO2 taxes
        serie = InstanciatedSeries(
            techno_detailed_prices[GlossaryCore.Years].values.tolist(),
            (techno_detailed_prices['CO2_taxes_factory'].values).tolist(), 'CO2 taxes due to production', 'lines')
        new_chart.series.append(serie)

        return new_chart

    def get_chart_investments(self):
        # Chart for input investments
        input_investments = self.get_sosdisc_inputs(GlossaryCore.InvestLevelValue)

        chart_name = f'Input investments over the years'

        new_chart = TwoAxesInstanciatedChart(GlossaryCore.Years, 'Investments [G$]',
                                             chart_name=chart_name, stacked_bar=True)
        invest = input_investments[GlossaryCore.InvestValue].values
        serie = InstanciatedSeries(
            input_investments[GlossaryCore.Years].values.tolist(),
            invest.tolist(), '', 'bar')

        new_chart.series.append(serie)

        return new_chart

    def get_charts_consumption_and_production(self):
        instanciated_charts = []
        # Charts for consumption and prod
        techno_consumption = self.get_sosdisc_outputs(
            GlossaryCore.TechnoDetailedConsumptionValue)
        techno_production = self.get_sosdisc_outputs(
            GlossaryCore.TechnoDetailedProductionValue)
        chart_name = f'{self.techno_name} resources production & consumption <br>with input investments'

        new_chart = TwoAxesInstanciatedChart(GlossaryCore.Years, 'Mass [Mt]',
                                             chart_name=chart_name, stacked_bar=True)

        for reactant in techno_consumption.columns:
            if reactant != GlossaryCore.Years and reactant.endswith('(Mt)'):
                energy_twh = -techno_consumption[reactant].values
                legend_title = f'{reactant} consumption'.replace(
                    "(Mt)", "")
                serie = InstanciatedSeries(
                    techno_consumption[GlossaryCore.Years].values.tolist(),
                    energy_twh.tolist(), legend_title, 'bar')

                new_chart.series.append(serie)

        for products in techno_production.columns:
            if products != GlossaryCore.Years and products.endswith('(Mt)'):
                energy_twh = techno_production[products].values
                legend_title = f'{products} product'.replace(
                    "(Mt)", "")
                serie = InstanciatedSeries(
                    techno_production[GlossaryCore.Years].values.tolist(),
                    energy_twh.tolist(), legend_title, 'bar')

                new_chart.series.append(serie)
        instanciated_charts.append(new_chart)

        return instanciated_charts

    def get_charts_consumption_and_production_energy(self):
        instanciated_charts = []
        # Charts for consumption and prod
        techno_consumption = self.get_sosdisc_outputs(
            GlossaryCore.TechnoDetailedConsumptionValue)
        techno_production = self.get_sosdisc_outputs(
            GlossaryCore.TechnoDetailedProductionValue)
        chart_name = f'{self.techno_name} energy production & consumption<br>with input investments'

        new_chart = TwoAxesInstanciatedChart(GlossaryCore.Years, 'Energy [TWh]',
                                             chart_name=chart_name, stacked_bar=True)

        for reactant in techno_consumption.columns:
            if reactant != GlossaryCore.Years and reactant.endswith('(TWh)'):
                energy_twh = -techno_consumption[reactant].values
                legend_title = f'{reactant} consumption'.replace(
                    "(TWh)", "")
                serie = InstanciatedSeries(
                    techno_consumption[GlossaryCore.Years].values.tolist(),
                    energy_twh.tolist(), legend_title, 'bar')

                new_chart.series.append(serie)

        for products in techno_production.columns:
            if products != GlossaryCore.Years and products.endswith('(TWh)'):
                energy_twh = techno_production[products].values
                legend_title = f'{products}'.replace(
                    "(TWh)", "")
                serie = InstanciatedSeries(
                    techno_production[GlossaryCore.Years].values.tolist(),
                    energy_twh.tolist(), legend_title, 'bar')

                new_chart.series.append(serie)
        instanciated_charts.append(new_chart)

        return instanciated_charts

    def get_chart_initial_production(self):

        year_start = self.get_sosdisc_inputs(
            GlossaryCore.YearStart)
        initial_production = self.get_sosdisc_inputs(
            'initial_production')
        initial_age_distrib = self.get_sosdisc_inputs(
            'initial_age_distrib')
        initial_prod = initial_age_distrib.copy(deep=True)
        initial_prod['CO2 (Mt)'] = initial_prod['distrib'] / \
            100.0 * initial_production
        initial_prod[GlossaryCore.Years] = year_start - initial_prod['age']
        initial_prod.sort_values(GlossaryCore.Years, inplace=True)
        initial_prod['cum CO2 (Mt)'] = initial_prod['CO2 (Mt)'].cumsum()

        study_production = self.get_sosdisc_outputs(
            GlossaryCore.TechnoDetailedProductionValue)
        chart_name = f'World CO2 capture via {self.techno_name}<br>with 2020 factories distribution'

        new_chart = TwoAxesInstanciatedChart(GlossaryCore.Years, f'{self.energy_name} (Mt)',
                                             chart_name=chart_name)

        serie = InstanciatedSeries(
            initial_prod[GlossaryCore.Years].values.tolist(),
            initial_prod[f'cum CO2 (Mt)'].values.tolist(), 'Initial carbon capture by 2020 factories', 'lines')
        study_prod = study_production[f'{self.energy_name} (Mt)'].values
        new_chart.series.append(serie)
        years_study = study_production[GlossaryCore.Years].values.tolist()
        years_study.insert(0, year_start - 1)
        study_prod_l = study_prod.tolist()
        study_prod_l.insert(
            0, initial_prod[f'cum CO2 (Mt)'].values.tolist()[-1])
        serie = InstanciatedSeries(
            years_study,
            study_prod_l, 'Predicted carbon capture', 'lines')
        new_chart.series.append(serie)

        return new_chart
