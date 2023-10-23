import pandas as pd
import numpy as np
from energy_models.core.techno_type.disciplines.heat_techno_disc import HighHeatTechnoDiscipline
from energy_models.core.stream_type.energy_models.heat import hightemperatureheat
from energy_models.models.heat.high.electric_boiler_high_heat.electric_boiler_high_heat import ElectricBoilerHighHeat
from sostrades_core.execution_engine.sos_wrapp import SoSWrapp
from sostrades_core.tools.post_processing.charts.chart_filter import ChartFilter
from sostrades_core.tools.post_processing.charts.two_axes_instanciated_chart import InstanciatedSeries, \
    TwoAxesInstanciatedChart
class ElectricBoilerHighHeatDiscipline(HighHeatTechnoDiscipline):

    # ontology information
    _ontology_data = {
        'label': 'Electric Boiler Model',
        'type': 'Research',
        'source': 'SoSTrades Project',
        'validated': '',
        'validated_by': 'SoSTrades Project',
        'last_modification_date': '',
        'category': '',
        'definition': '',
        'icon': 'fas fa-gas-pump fa-fw',
        'version': '',
    }
    # -- add specific techno inputs to this
    techno_name = 'ElectricBoilerHighHeat'
    energy_name = hightemperatureheat.name

    # Heat Producer [Online]
    #https://www.google.com/search?q=electric+boiler+maximum+heat+temperature+in+degree+celcius&rlz=1C1UEAD_enIN1000IN1000&sxsrf=APwXEdf5IN3xbJw5uB3tC7-M-5nvtg8TKg%3A1683626939090&ei=uxtaZNOCBYWeseMP6ZuEwAM&ved=0ahUKEwiTzI2N_-f-AhUFT2wGHekNATgQ4dUDCA8&uact=5&oq=electric+boiler+maximum+heat+temperature+in+degree+celcius&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCCEQoAEyBQghEKABMgUIIRCgATIFCCEQoAE6CwgAEIoFEIYDELADOggIIRAWEB4QHToHCCEQoAEQCjoECCEQFUoECEEYAVDPB1izUGDqoQVoAXAAeACAAZ0BiAGUBJIBAzAuNJgBAKABAcgBA8ABAQ&sclient=gws-wiz-serp
    #https://www.google.com/search?q=electric+boiler+lifetime&rlz=1C1UEAD_enIN1000IN1000&oq=electric+boiler+lifetime&aqs=chrome..69i57j0i22i30l4j0i390i650l4.14155j0j7&sourceid=chrome&ie=UTF-8
    lifetime = 45          # years

    construction_delay = 2  # years

    techno_infos_dict_default = {

        'Capex_init': 42.86,          #https://capgemini-my.sharepoint.com/personal/valentin_joncquieres_capgemini_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fvalentin%5Fjoncquieres%5Fcapgemini%5Fcom%2FDocuments%2FFichiers%20de%20conversation%20Microsoft%20Teams%2FPriyankaChintada%5Ffinal%5Fthesis%2Epdf&parent=%2Fpersonal%2Fvalentin%5Fjoncquieres%5Fcapgemini%5Fcom%2FDocuments%2FFichiers%20de%20conversation%20Microsoft%20Teams&ga=1
                                      # table 5.2.
        'Capex_init_unit': '$/kW',    # $ per kW of electricity
        'Opex_percentage': 1.6,       #https://www.google.com/search?q=+OPEX+%25+of+an+electric+boiler&rlz=1C1UEAD_enIN1000IN1000&sxsrf=APwXEddXq4YjX58191BnDyTZd08c2VWtJw%3A1683713517747&ei=7W1bZJqaLaicseMP_pSKkAQ&ved=0ahUKEwjaxIPRwer-AhUoTmwGHX6KAkIQ4dUDCA8&uact=5&oq=+OPEX+%25+of+an+electric+boiler&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCAAQogQyBQgAEKIEMgUIABCiBDIFCAAQogQ6BQghEKABSgQIQRgAUABYxSdggjFoAHAAeACAAZYBiAGuA5IBAzIuMpgBAKABAcABAQ&sclient=gws-wiz-serp
        'lifetime': lifetime,
        'lifetime_unit': 'years',
        'construction_delay': construction_delay,
        'construction_delay_unit': 'years',
        'efficiency': 0.99,           # consumptions and productions already have efficiency included
                                      # https://www.google.com/search?q=electric+boiler+efficiency&rlz=1C1UEAD_enIN1000IN1000&sxsrf=APwXEddgb3MP-p7vfw3Bi3_aNLESRLQX8g%3A1685475202926&ei=gk92ZJKcOL-VseMPs4WWuA0&ved=0ahUKEwiS5f215J3_AhW_SmwGHbOCBdcQ4dUDCA8&uact=5&oq=electric+boiler+efficiency&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCAAQgAQyBQgAEIAEMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjoKCAAQRxDWBBCwAzoECCMQJzoHCCMQ6gIQJzoVCAAQAxCPARDqAhC0AhCMAxDlAhgBOhUILhADEI8BEOoCELQCEIwDEOUCGAE6BwgAEIoFEEM6CAgAEIoFEJECOgsIABCABBCxAxCDAToNCAAQigUQsQMQgwEQQzoKCAAQigUQsQMQQzoICAAQgAQQsQM6CggAEIAEEBQQhwJKBAhBGABQ-QRYx1pgxWVoAnABeAOAAcMBiAG0K5IBBTI3LjI2mAEAoAEBsAEUwAEByAEI2gEGCAEQARgL&sclient=gws-wiz-serp
        'elec_demand': 1,             #https://billswiz.com/electric-boiler-electricity-use
        'elec_demand_unit': 'KWh',
        'learning_rate': 0.56,
        'full_load_hours': 8760.0,
        'WACC': 0.062,
        'techno_evo_eff': 'no',
    }

    # production in 2019: 1.51 EJ = 419 TWh
    # https://www.worldbioenergy.org/uploads/211214%20WBA%20GBS%202021.pdf
    # page 14
    # in TWh
    initial_production = 139.67

    distrib = [40.0, 40.0, 20.0, 20.0, 20.0, 12.0, 12.0, 12.0, 12.0, 12.0,
               8.0, 8.0, 8.0, 8.0, 8.0, 5.0, 5.0, 5.0, 5.0, 5.0,
               3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
               2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0,
               1.0, 1.0, 1.0, 1.0,
               ]

    initial_age_distribution = pd.DataFrame({'age': np.arange(1, lifetime),
                                             'distrib': 100 / sum(distrib) * np.array(distrib)})

    # Renewable Association [online]
    invest_before_year_start = pd.DataFrame(
        {'past years': np.arange(-construction_delay, 0), 'invest': 0})

    flux_input_dict = {'land_rate': 22000, 'land_rate_unit': '$/Gha', }
    DESC_IN = {'techno_infos_dict': {'type': 'dict', 'default': techno_infos_dict_default, 'unit': 'defined in dict'},
               'initial_age_distrib': {'type': 'dataframe', 'unit': '%', 'default': initial_age_distribution,
                                       'dataframe_descriptor': {'years': ('int', [1900, 2100], False),
                                                                'age': ('float', None, True),
                                                                'distrib': ('float', None, True),
                                                                }
                                       },
               'initial_production': {'type': 'float', 'unit': 'TWh', 'default': initial_production},
               'invest_before_ystart': {'type': 'dataframe', 'unit': 'G$', 'default': invest_before_year_start,
                                        'dataframe_descriptor': {'past years': ('int',  [-20, -1], False),
                                                                 'invest': ('float',  None, True)},
                                        'dataframe_edition_locked': False},
               'flux_input_dict': {'type': 'dict', 'default': flux_input_dict, 'unit': 'defined in dict'},
               }
    DESC_IN.update(HighHeatTechnoDiscipline.DESC_IN)
    # -- add specific techno outputs to this
    DESC_OUT = HighHeatTechnoDiscipline.DESC_OUT

    def init_execution(self):
        inputs_dict = self.get_sosdisc_inputs()
        self.techno_model = ElectricBoilerHighHeat(self.techno_name)
        self.techno_model.configure_parameters(inputs_dict)
        self.techno_model.configure_input(inputs_dict)

    def setup_sos_disciplines(self):
        super().setup_sos_disciplines()
        # dynamic_inputs = self.get_inst_desc_in()
        # #self.get_data_in()
        # #print(self.get_sosdisc_inputs())
        # # heat_flux_input_parameters_default = {'land_rate': 1000.0,
        # #                               'land_rate_unit': '$/Gha',
        # #                              }
        # dynamic_inputs['flux_input_dict'] = {
        #     'type': 'dict', 'unit': '$/Gha', 'dataframe_descriptor': {'land_rate': ('float', [1.e-8, 1e30], True),
        #                               'land_rate_unit': '$/Gha'}
        #                              }
        #
        #         #'default': heat_flux_input_parameters_default,
        #    #'visibility': HighHeatTechnoDiscipline.SHARED_VISIBILITY, 'namespace': 'ns_heat_high'}
        #
        #

        dynamic_outputs = {}
        # heat_flux_distribution = pd.DataFrame({'years': np.arange(1, self.lifetime),
        #                                          'heat_flux': 0 / sum(self.distrib) * np.array(self.distrib)})
        dynamic_outputs['heat_flux'] = {'type': 'dataframe', 'unit': 'TWh/Gha',
                                        'dataframe_descriptor': {'years': ('int', [1900, 2100], True),
                                                                 'heat_flux': ('float', [1.e-8, 1e30], True),
                                                                 },
                                        }
                                                         # 'visibility': HighHeatTechnoDiscipline.SHARED_VISIBILITY,
                                                         # 'namespace': 'ns_heat_high'}

        #print(dynamic_outputs)
        #self.add_inputs(dynamic_inputs)
        self.add_outputs(dynamic_outputs)
    def run(self):
        '''
        Run for all energy disciplines
        '''

        inputs_dict = self.get_sosdisc_inputs()
        self.techno_model.configure_parameters_update(inputs_dict)
        super().run()
        self.techno_model.compute_heat_flux()

        outputs_dict = {'heat_flux': self.techno_model.heat_flux_distribution}
        #-- store outputs
        self.store_sos_outputs_values(outputs_dict)

    @staticmethod
    def get_charts(title, x_data, y_data, x_label, y_label, series_name, stacked_bar):
        """
        Line graph object for x and y data
        title = string for graph name
        x_data = dataframe
        y_data = dataframe
        x_label = string for x-axis name
        y_label = string for y-axis name
        series_name = string for series name
        stacked_bar = for bar chart stacking
        """

        chart_name = title
        if stacked_bar:
            new_chart = TwoAxesInstanciatedChart(x_label, y_label,
                                                 chart_name=chart_name, stacked_bar=True)
        else:
            new_chart = TwoAxesInstanciatedChart(x_label, y_label,
                                                 chart_name=chart_name)
        serie = InstanciatedSeries(
            x_data.tolist(),
            y_data.tolist(), series_name, 'lines')
        new_chart.series.append(serie)

        return new_chart

    def get_chart_filter_list(self):
        chart_filters = HighHeatTechnoDiscipline.get_chart_filter_list(self)

        self.instanciated_charts = HighHeatTechnoDiscipline.get_post_processing_list(self, chart_filters)

        chart_list = ['heat_flux']
        chart_filters.append(ChartFilter(
            'Charts', chart_list, chart_list, 'charts'))
        #print(chart_filters)
        return chart_filters


    def get_post_processing_list(self, filters=None):
        """
        Basic post processing method for the model
        """
        #m = self.get_post_processing_list()
        instanciated_charts = self.instanciated_charts #HighHeatTechnoDiscipline.get_post_processing_list(self, filters) #self, filters
        charts = []
        # for pie charts Title
        unit_str = '$/MWh'
        var_str = 'Split up of Opex contributions'
        # Overload default value with chart filter
        if filters is not None:
            for chart_filter in filters:
                if chart_filter.filter_key == 'charts':
                    charts = chart_filter.selected_values

        heat_flux = self.get_sosdisc_outputs('heat_flux')
        #print(charts)



        if 'heat_flux' in charts:
            x_data = heat_flux['years'].values
            y_data = heat_flux['heat_flux'].values
            x_label = 'years'
            y_label = 'heat_flux'
            series_name =  y_label
            title = f'Detailed heat_flux over the years'
            new_chart = self.get_charts(title, x_data, y_data, x_label, y_label, series_name, True)
            # for element in self.techno_list:
            #     y_data = dict_input[f"{element}.{Glossary.TechnologyProduction['var_name']}"][
            #         Glossary.PowerCapacity].values
            #     serie = self.create_new_series(x_data, y_data, element, 'bar')
            #     new_chart.series.append(serie)

            instanciated_charts.append(new_chart)

        return instanciated_charts
