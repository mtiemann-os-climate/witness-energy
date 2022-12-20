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
import unittest
import pandas as pd
import numpy as np
import scipy.interpolate as sc

from energy_models.core.stream_type.energy_models.gaseous_hydrogen import GaseousHydrogen
from sostrades_core.execution_engine.execution_engine import ExecutionEngine
from climateeconomics.core.core_resources.resource_mix.resource_mix import ResourceMixModel


class HydrogenPriceTestCase(unittest.TestCase):
    """
    Hydrogen prices test class
    """

    def setUp(self):
        '''
        Initialize third data needed for testing
        '''
        years = np.arange(2020, 2051)
        self.resource_list = [
            'oil_resource', 'natural_gas_resource', 'uranium_resource', 'coal_resource']
        self.ratio_available_resource = pd.DataFrame(
            {'years': np.arange(2020, 2050 + 1)})
        for types in self.resource_list:
            self.ratio_available_resource[types] = np.linspace(
                1, 1, len(self.ratio_available_resource.index))
        self.electrolysis_techno_prices = pd.DataFrame({'Electrolysis.PEM': np.array([0.09, 0.08974117039450046, 0.08948672733558984,
                                                                                      0.089236536471781, 0.08899046935409588, 0.08874840310033885,
                                                                                      0.08875044941298937, 0.08875249600769718, 0.08875454288453355,
                                                                                      0.08875659004356974, 0.0887586374848771, 0.08893789675406477,
                                                                                      0.08911934200930778, 0.08930302260662477, 0.08948898953954933,
                                                                                      0.08967729551117891, 0.08986799501019029, 0.09006114439108429,
                                                                                      0.09025680195894345, 0.09045502805900876, 0.09065588517140537,
                                                                                      0.0908594380113745, 0.09106575363539733, 0.09127490155362818,
                                                                                      0.09148695384909017, 0.0917019853041231, 0.0919200735346165,
                                                                                      0.09214129913260598, 0.09236574581786147, 0.09259350059915213,
                                                                                      0.0928246539459331]) * 1000.0,
                                                        'Electrolysis.PEM_wotaxes': np.array([0.09, 0.08974117039450046, 0.08948672733558984,
                                                                                              0.089236536471781, 0.08899046935409588, 0.08874840310033885,
                                                                                              0.08875044941298937, 0.08875249600769718, 0.08875454288453355,
                                                                                              0.08875659004356974, 0.0887586374848771, 0.08893789675406477,
                                                                                              0.08911934200930778, 0.08930302260662477, 0.08948898953954933,
                                                                                              0.08967729551117891, 0.08986799501019029, 0.09006114439108429,
                                                                                              0.09025680195894345, 0.09045502805900876, 0.09065588517140537,
                                                                                              0.0908594380113745, 0.09106575363539733, 0.09127490155362818,
                                                                                              0.09148695384909017, 0.0917019853041231, 0.0919200735346165,
                                                                                              0.09214129913260598, 0.09236574581786147, 0.09259350059915213,
                                                                                              0.0928246539459331]) * 1000.0})

        self.smr_techno_prices = pd.DataFrame({'WaterGasShift': np.array([0.06363, 0.0612408613576689, 0.059181808246196024, 0.05738028027202377,
                                                                          0.0557845721244601, 0.05435665353332419, 0.05225877624361548,
                                                                          0.05045797192512811, 0.04888746457113824, 0.04750006564084081,
                                                                          0.04626130284326101, 0.044848110567750024, 0.043596892851567724,
                                                                          0.04247763196812953, 0.04146768302263715, 0.04054957955940597,
                                                                          0.03970959176775726, 0.03893674917609171, 0.038222160192931814,
                                                                          0.03755852715493717, 0.03693979356326306, 0.03636088278590117,
                                                                          0.03581750135963429, 0.03530598876014997, 0.03482320115289285,
                                                                          0.03436642036567466, 0.03393328183670935, 0.033521717015978045,
                                                                          0.03312990690071806, 0.032756244237772174, 0.03239930253734476]) * 1000.0,
                                               'WaterGasShift_wotaxes': np.array([0.06363, 0.0612408613576689, 0.059181808246196024, 0.05738028027202377,
                                                                                  0.0557845721244601, 0.05435665353332419, 0.05225877624361548,
                                                                                  0.05045797192512811, 0.04888746457113824, 0.04750006564084081,
                                                                                  0.04626130284326101, 0.044848110567750024, 0.043596892851567724,
                                                                                  0.04247763196812953, 0.04146768302263715, 0.04054957955940597,
                                                                                  0.03970959176775726, 0.03893674917609171, 0.038222160192931814,
                                                                                  0.03755852715493717, 0.03693979356326306, 0.03636088278590117,
                                                                                  0.03581750135963429, 0.03530598876014997, 0.03482320115289285,
                                                                                  0.03436642036567466, 0.03393328183670935, 0.033521717015978045,
                                                                                  0.03312990690071806, 0.032756244237772174, 0.03239930253734476]) * 1000.0
                                               })

        self.plasmacracking_techno_prices = pd.DataFrame({'PlasmaCracking':
                                                          np.array([0.06363, 0.0612408613576689, 0.059181808246196024, 0.05738028027202377,
                                                                    0.0557845721244601, 0.05435665353332419, 0.05225877624361548,
                                                                    0.05045797192512811, 0.04888746457113824, 0.04750006564084081,
                                                                    0.04626130284326101, 0.044848110567750024, 0.043596892851567724,
                                                                    0.04247763196812953, 0.04146768302263715, 0.04054957955940597,
                                                                    0.03970959176775726, 0.03893674917609171, 0.038222160192931814,
                                                                    0.03755852715493717, 0.03693979356326306, 0.03636088278590117,
                                                                    0.03581750135963429, 0.03530598876014997, 0.03482320115289285,
                                                                    0.03436642036567466, 0.03393328183670935, 0.033521717015978045,
                                                                    0.03312990690071806, 0.032756244237772174, 0.03239930253734476]) * 1000.0,
                                                          'PlasmaCracking_wotaxes':
                                                          np.array([0.06363, 0.0612408613576689, 0.059181808246196024, 0.05738028027202377,
                                                                    0.0557845721244601, 0.05435665353332419, 0.05225877624361548,
                                                                    0.05045797192512811, 0.04888746457113824, 0.04750006564084081,
                                                                    0.04626130284326101, 0.044848110567750024, 0.043596892851567724,
                                                                    0.04247763196812953, 0.04146768302263715, 0.04054957955940597,
                                                                    0.03970959176775726, 0.03893674917609171, 0.038222160192931814,
                                                                    0.03755852715493717, 0.03693979356326306, 0.03636088278590117,
                                                                    0.03581750135963429, 0.03530598876014997, 0.03482320115289285,
                                                                    0.03436642036567466, 0.03393328183670935, 0.033521717015978045,
                                                                    0.03312990690071806, 0.032756244237772174, 0.03239930253734476]) * 1000.0,
                                                          })

        self.smr_consumption = pd.DataFrame({'years': years,
                                             'electricity (TWh)': [2896311508.0963955, 2982753151.7982965,
                                                                   3066756571.3836217, 3148856944.5695057,
                                                                   3229439770.4969134, 3308790913.4863434,
                                                                   3407857732.7514524, 3504165477.2542033,
                                                                   3598314488.6977625, 3690732832.930875,
                                                                   3781735255.124399, 3792625789.342879,
                                                                   3800920905.868535, 3807068942.0443764,
                                                                   3811413493.827316, 3814223407.5059695,
                                                                   3815715837.2417374, 3816060929.328741,
                                                                   3815400603.911421, 3813852554.2526307,
                                                                   3811515405.3375063, 3808294832.9902496,
                                                                   3804439457.7222347, 3800010580.6161594,
                                                                   3795061245.507408, 3789637637.548874,
                                                                   3783783266.135714, 3777530659.2496386,
                                                                   3770911299.619129, 3763953154.457168,
                                                                   3756681168.944179],
                                             'methane (TWh)': [13033401786.43378, 13422389183.092335,
                                                               13800404571.226297, 14169856250.562777,
                                                               14532478967.236109, 14889559110.688545,
                                                               15335359797.381535, 15768744647.643913,
                                                               16192415199.13993, 16608297748.188936,
                                                               17017808648.059795, 17066816052.042955,
                                                               17104144076.408407, 17131810239.199694,
                                                               17151360722.22292, 17164005333.776861,
                                                               17170721267.587818, 17172274181.979334,
                                                               17169302717.601393, 17162336494.136839,
                                                               17151819324.018778, 17137326748.456123,
                                                               17119977559.750055, 17100047612.772717,
                                                               17077775604.783337, 17053369368.969933,
                                                               17027024697.610714, 16998887966.623373,
                                                               16969100848.286081, 16937789195.057255, 16905065260.248804],
                                             'water (Mt)': [4115502095.6261625, 4238330998.8052826, 4357695317.310647, 4474355509.749778,
                                                            4588859349.564196, 4701613034.501204, 4842381629.713719, 4979229728.828101,
                                                            5113010384.953646, 5244331856.522723, 5373641379.409873, 5389116239.856808,
                                                            5400903152.055088, 5409639179.134679, 5415812552.377599, 5419805287.82774,
                                                            5421925949.810389, 5422416307.012394, 5421478020.287647, 5419278325.400867,
                                                            5415957363.124849, 5411381103.904389, 5405902824.047203, 5399609629.078232,
                                                            5392576891.420324, 5384870237.679245, 5376551492.353654, 5367666875.947291,
                                                            5358261123.715561, 5348373975.556368, 5338040877.222709]})

        self.smr_production = pd.DataFrame({'years': years,
                                            'hydrogen.gaseous_hydrogen (TWh)': [14481557540.481977, 14913765758.991482, 15333782856.918108, 15744284722.847528,
                                                                                16147198852.484566, 16543954567.431717, 17039288663.757261, 17520827386.271015,
                                                                                17991572443.48881, 18453664164.654373, 18908676275.621994, 18963128946.714394,
                                                                                19004604529.342674, 19035344710.22188, 19057067469.136578, 19071117037.529846,
                                                                                19078579186.208687, 19080304646.643703, 19077003019.557102, 19069262771.263153,
                                                                                19057577026.68753, 19041474164.95125, 19022197288.61117, 19000052903.080795,
                                                                                18975306227.53704, 18948188187.74437, 18918916330.67857, 18887653296.24819,
                                                                                18854556498.095646, 18819765772.28584, 18783405844.720894],
                                            'CO2 (Mt)': [1452504570.1264207, 1495855184.2351818, 1537983025.288483, 1579156485.7150376,
                                                         1619568893.9128664, 1659363611.267926, 1709045769.878356, 1757344248.3527086,
                                                         1804560118.9565356, 1850908057.355724, 1896545908.72605, 1902007527.9887712,
                                                         1906167541.3815176, 1909250790.7549877, 1911429589.9974828, 1912838765.926417,
                                                         1913587221.6797903, 1913760285.8795788, 1913429131.691313, 1912652782.463031,
                                                         1911480698.7728636, 1909865576.9050202, 1907932100.4192588, 1905711011.9005964,
                                                         1903228912.9121237, 1900508965.3773632, 1897572989.323316, 1894437297.5816505,
                                                         1891117678.7879717, 1887628158.5415828, 1883981246.8879216]})

        self.plasmacracking_production = pd.DataFrame({'years': years,
                                                       'hydrogen.gaseous_hydrogen (TWh)': [1097111725247.1581, 1074283458370.2065,
                                                                                           1059357209295.9789, 1012387616382.4406,
                                                                                           933807168833.0933, 886484117080.1772,
                                                                                           850185159537.7354, 806257639980.3197, 814880240798.5356,
                                                                                           854855722377.0725, 765371262339.0336, 739965268826.7208,
                                                                                           748224975467.2812, 738715777729.1125, 761354173153.3649,
                                                                                           787494966087.825, 791285113944.1445, 781257873794.123,
                                                                                           737144478326.2227, 740828726010.5015, 787890596779.661,
                                                                                           835192505463.6168, 848467209437.1797, 862665698763.6089,
                                                                                           876077004764.9058, 888687180526.2354, 900482498681.7069,
                                                                                           911449443619.2367, 921574704085.7356, 930618161335.769,
                                                                                           938563362570.5361],
                                                       'C (Mt)':   [84232562661.74246, 82479884811.41814,
                                                                    81333897414.22173, 77727729430.37773,
                                                                    71694585931.9824, 68061280562.627815,
                                                                    65274368213.23983, 61901760429.96109,
                                                                    62563774832.88249, 65632958380.4732,
                                                                    58762641334.405495, 56812054269.05661,
                                                                    57446206872.80522, 56716122528.69455,
                                                                    58454222684.998184, 60461225188.21498,
                                                                    60752220042.66592, 59982362137.74675,
                                                                    56595483424.79247, 56878347618.82657,
                                                                    60491600387.27092, 64123282462.6254,
                                                                    65142469760.08803, 66232582202.02834,
                                                                    67262257345.52893, 68230424393.19446,
                                                                    69136029403.86201, 69978034694.11652,
                                                                    70755418270.54187, 71449744620.32236,
                                                                    72059750552.6871]})

        self.plasmacracking_consumption = pd.DataFrame({'years': years,
                                                        'electricity (TWh)': [231813581540.16727,
                                                                              226990096216.54742, 223836263131.7011,
                                                                              213911850415.83292, 197308240622.72845,
                                                                              187309144027.72778, 179639376983.5443,
                                                                              170357737381.62845, 172179644788.01544,
                                                                              180626240832.21136, 161718674085.59528,
                                                                              156350529517.32108, 158095759410.28214,
                                                                              156086519025.25027, 160869885571.11072,
                                                                              166393289154.34372, 167194126233.1219,
                                                                              165075426379.08817, 155754512235.17267,
                                                                              156532973198.9194, 166476883710.42328,
                                                                              176471512893.0104, 179276383719.91168,
                                                                              182276445233.6813, 185110179306.29034,
                                                                              187774639032.51038, 190266923896.57892,
                                                                              192584178125.13058, 194723589124.71442,
                                                                              196634421145.1847, 198313197802.02316],
                                                        'methane (TWh)':  [1715281276020.9375, 1679590381614.333,
                                                                           1656253910980.5151, 1582819217491.3284,
                                                                           1459962477160.3691, 1385975167820.7847,
                                                                           1329223498160.5203, 1260544939664.6624,
                                                                           1274025960233.2437, 1336525697929.6362,
                                                                           1196621059900.621, 1156900014206.2437,
                                                                           1169813667228.0337, 1154946495129.78,
                                                                           1190340534676.327, 1231210403832.7415,
                                                                           1237136117232.4697, 1221459010805.025,
                                                                           1152489844286.683, 1158249987874.2866,
                                                                           1231828953340.7898, 1305783206511.6445,
                                                                           1326537566023.6108, 1348736219386.759,
                                                                           1369704149581.6802, 1389419551279.5964,
                                                                           1407860962405.9175, 1425007251952.9182,
                                                                           1440837608418.3074, 1454976617722.9282,
                                                                           1467398556709.2646]})

        self.electrolysis_consumption = pd.DataFrame({'years': years,
                                                      'electricity (TWh)': [2896311508.0963955, 2982753151.7982965,
                                                                            3066756571.3836217, 3148856944.5695057,
                                                                            3229439770.4969134, 3308790913.4863434,
                                                                            3407857732.7514524, 3504165477.2542033,
                                                                            3598314488.6977625, 3690732832.930875,
                                                                            3781735255.124399, 3792625789.342879,
                                                                            3800920905.868535, 3807068942.0443764,
                                                                            3811413493.827316, 3814223407.5059695,
                                                                            3815715837.2417374, 3816060929.328741,
                                                                            3815400603.911421, 3813852554.2526307,
                                                                            3811515405.3375063, 3808294832.9902496,
                                                                            3804439457.7222347, 3800010580.6161594,
                                                                            3795061245.507408, 3789637637.548874,
                                                                            3783783266.135714, 3777530659.2496386,
                                                                            3770911299.619129, 3763953154.457168,
                                                                            3756681168.944179],
                                                      'water (Mt)': [4115502095.6261625, 4238330998.8052826, 4357695317.310647, 4474355509.749778,
                                                                     4588859349.564196, 4701613034.501204, 4842381629.713719, 4979229728.828101,
                                                                     5113010384.953646, 5244331856.522723, 5373641379.409873, 5389116239.856808,
                                                                     5400903152.055088, 5409639179.134679, 5415812552.377599, 5419805287.82774,
                                                                     5421925949.810389, 5422416307.012394, 5421478020.287647, 5419278325.400867,
                                                                     5415957363.124849, 5411381103.904389, 5405902824.047203, 5399609629.078232,
                                                                     5392576891.420324, 5384870237.679245, 5376551492.353654, 5367666875.947291,
                                                                     5358261123.715561, 5348373975.556368, 5338040877.222709]})

        self.electrolysis_production = pd.DataFrame({'years': years,
                                                     'hydrogen.gaseous_hydrogen (TWh)': [14481557540.481977, 14913765758.991482, 15333782856.918108, 15744284722.847528,
                                                                                         16147198852.484566, 16543954567.431717, 17039288663.757261, 17520827386.271015,
                                                                                         17991572443.48881, 18453664164.654373, 18908676275.621994, 18963128946.714394,
                                                                                         19004604529.342674, 19035344710.22188, 19057067469.136578, 19071117037.529846,
                                                                                         19078579186.208687, 19080304646.643703, 19077003019.557102, 19069262771.263153,
                                                                                         19057577026.68753, 19041474164.95125, 19022197288.61117, 19000052903.080795,
                                                                                         18975306227.53704, 18948188187.74437, 18918916330.67857, 18887653296.24819,
                                                                                         18854556498.095646, 18819765772.28584, 18783405844.720894],
                                                     'O2 (Mt)': [1452504570.1264207, 1495855184.2351818, 1537983025.288483, 1579156485.7150376,
                                                                 1619568893.9128664, 1659363611.267926, 1709045769.878356, 1757344248.3527086,
                                                                 1804560118.9565356, 1850908057.355724, 1896545908.72605, 1902007527.9887712,
                                                                 1906167541.3815176, 1909250790.7549877, 1911429589.9974828, 1912838765.926417,
                                                                 1913587221.6797903, 1913760285.8795788, 1913429131.691313, 1912652782.463031,
                                                                 1911480698.7728636, 1909865576.9050202, 1907932100.4192588, 1905711011.9005964,
                                                                 1903228912.9121237, 1900508965.3773632, 1897572989.323316, 1894437297.5816505,
                                                                 1891117678.7879717, 1887628158.5415828, 1883981246.8879216]})

        self.electrolysis_carbon_emissions = pd.DataFrame(
            {'years': years, 'Electrolysis.PEM': 0.0})

        self.plasma_cracking_carbon_emissions = pd.DataFrame(
            {'years': years, 'PlasmaCracking': 0.013})
        self.smr_carbon_emissions = pd.DataFrame(
            {'years': years, 'WaterGasShift': 0.1721})
        co2_taxes_year = [2018, 2020, 2025, 2030, 2035, 2040, 2045, 2050]
        co2_taxes = [0.01486, 0.01722, 0.02027,
                     0.02901,  0.03405,   0.03908,  0.04469,   0.05029]
        func = sc.interp1d(co2_taxes_year, co2_taxes,
                           kind='linear', fill_value='extrapolate')

        self.co2_taxes = pd.DataFrame(
            {'years': years, 'CO2_tax': func(years)})

        self.land_use_required_WaterGasShift = pd.DataFrame(
            {'years': years, 'WaterGasShift (Gha)': 0.0})
        self.land_use_required_Electrolysis = pd.DataFrame(
            {'years': years, 'Electrolysis.PEM (Gha)': 0.0})
        self.land_use_required_PlasmaCracking = pd.DataFrame(
            {'years': years, 'PlasmaCracking (Gha)': 0.0})
        self.scaling_factor_techno_consumption = 1e3
        self.scaling_factor_techno_production = 1e3

    def tearDown(self):
        pass

    def test_01_compute_hydrogen_price_with_same_production(self):
        year_start = 2020
        year_end = 2050

        inputs_dict = {'year_start': year_start,
                       'year_end': year_end,
                       'CO2_taxes': self.co2_taxes,
                       'data_fuel_dict': GaseousHydrogen.data_energy_dict,
                       'technologies_list': ['WaterGasShift', 'Electrolysis.PEM'],
                       'WaterGasShift.techno_consumption': self.smr_consumption,
                       'WaterGasShift.techno_consumption_woratio': self.smr_consumption,
                       'WaterGasShift.techno_production': self.smr_production,
                       'WaterGasShift.techno_prices': self.smr_techno_prices,
                       'WaterGasShift.CO2_emissions': self.smr_carbon_emissions,
                       'WaterGasShift.land_use_required': self.land_use_required_WaterGasShift,
                       'Electrolysis.PEM.techno_consumption': self.electrolysis_consumption,
                       'Electrolysis.PEM.techno_consumption_woratio': self.electrolysis_consumption,
                       'Electrolysis.PEM.techno_production': self.electrolysis_production,
                       'Electrolysis.PEM.techno_prices': self.electrolysis_techno_prices,
                       'Electrolysis.PEM.CO2_emissions': self.electrolysis_carbon_emissions,
                       'Electrolysis.PEM.land_use_required': self.land_use_required_Electrolysis,
                       'PlasmaCracking.techno_consumption': self.plasmacracking_consumption,
                       'PlasmaCracking.techno_consumption_woratio': self.plasmacracking_consumption,
                       'PlasmaCracking.techno_production': self.plasmacracking_production,
                       'PlasmaCracking.techno_prices': self.plasmacracking_techno_prices,
                       'PlasmaCracking.CO2_emissions': self.plasma_cracking_carbon_emissions,
                       'PlasmaCracking.land_use_required': self.land_use_required_PlasmaCracking,
                       'scaling_factor_techno_consumption': self.scaling_factor_techno_consumption,
                       'scaling_factor_techno_production': self.scaling_factor_techno_production,
                       ResourceMixModel.RATIO_USABLE_DEMAND: self.ratio_available_resource}

        h2_model = GaseousHydrogen('hydrogen.gaseous_hydrogen')
        h2_model.configure(inputs_dict)
        prices, production, consumption, consumption_woratio, techno_mix_weights = h2_model.compute()

        # Same production then same weights : 50%
        # self.assertListEqual(
        #     list(techno_mix_weights['SMR'].values), list(techno_mix_weights['electrolysis'].values))
        # self.assertListEqual(list(techno_mix_weights['SMR'].values), list(np.ones(
        #     year_end - year_start + 1) * 50.0))

        # Check that the final price is inbetween the two techno prices
        for smr_price, price, electrolysis_price in zip(self.smr_techno_prices['WaterGasShift'], prices['hydrogen.gaseous_hydrogen'], self.electrolysis_techno_prices['Electrolysis.PEM']):
            if smr_price < electrolysis_price:
                self.assertTrue(smr_price <= price <= electrolysis_price)
            else:
                self.assertTrue(electrolysis_price <= price <= smr_price)

        # for column in consumption:
        #     if column != 'years':
        #         self.assertListEqual(
        # list(consumption[column].values), list(2.0 *
        # self.smr_consumption[column].values))

        # for column in production:
        #     if column != 'years' and not column.startswith('H2'):
        #         self.assertEqual(
        # list(production[column].values), list(2.0 *
        # self.smr_production[column].values))

    def test_02_hydrogen_discipline(self):

        self.name = 'Test'
        self.model_name = 'hydrogen.gaseous_hydrogen'
        self.ee = ExecutionEngine(self.name)
        ns_dict = {'ns_public': f'{self.name}',
                   'ns_hydrogen': f'{self.name}',
                   'ns_energy_study': f'{self.name}',
                   'ns_resource': self.name}
        self.ee.ns_manager.add_ns_def(ns_dict)

        mod_path = 'energy_models.core.stream_type.energy_disciplines.gaseous_hydrogen_disc.GaseousHydrogenDiscipline'
        builder = self.ee.factory.get_builder_from_module(
            self.model_name, mod_path)

        self.ee.factory.set_builders_to_coupling_builder(builder)

        self.ee.configure()
        self.ee.display_treeview_nodes()

        inputs_dict = {f'{self.name}.year_start': 2020,
                       f'{self.name}.year_end': 2050,
                       f'{self.name}.CO2_taxes': self.co2_taxes,
                       f'{self.name}.technologies_list': ['WaterGasShift', 'Electrolysis.PEM', 'PlasmaCracking'],
                       f'{self.name}.{self.model_name}.WaterGasShift.techno_consumption': self.smr_consumption,
                       f'{self.name}.{self.model_name}.WaterGasShift.techno_consumption_woratio': self.smr_consumption,
                       f'{self.name}.{self.model_name}.WaterGasShift.techno_production': self.smr_production,
                       f'{self.name}.{self.model_name}.WaterGasShift.techno_prices': self.smr_techno_prices,
                       f'{self.name}.{self.model_name}.WaterGasShift.CO2_emissions': self.smr_carbon_emissions,
                       f'{self.name}.{self.model_name}.WaterGasShift.land_use_required': self.land_use_required_WaterGasShift,
                       f'{self.name}.{self.model_name}.Electrolysis.PEM.techno_consumption': self.electrolysis_consumption,
                       f'{self.name}.{self.model_name}.Electrolysis.PEM.techno_consumption_woratio': self.electrolysis_consumption,
                       f'{self.name}.{self.model_name}.Electrolysis.PEM.techno_production': self.electrolysis_production,
                       f'{self.name}.{self.model_name}.Electrolysis.PEM.techno_prices': self.electrolysis_techno_prices,
                       f'{self.name}.{self.model_name}.Electrolysis.PEM.CO2_emissions': self.electrolysis_carbon_emissions,
                       f'{self.name}.{self.model_name}.Electrolysis.PEM.land_use_required': self.land_use_required_Electrolysis,
                       f'{self.name}.{self.model_name}.PlasmaCracking.techno_consumption': self.plasmacracking_consumption,
                       f'{self.name}.{self.model_name}.PlasmaCracking.techno_consumption_woratio': self.plasmacracking_consumption,
                       f'{self.name}.{self.model_name}.PlasmaCracking.techno_production': self.plasmacracking_production,
                       f'{self.name}.{self.model_name}.PlasmaCracking.techno_prices': self.plasmacracking_techno_prices,
                       f'{self.name}.{self.model_name}.PlasmaCracking.CO2_emissions': self.plasma_cracking_carbon_emissions,
                       f'{self.name}.{self.model_name}.PlasmaCracking.land_use_required': self.land_use_required_PlasmaCracking}

        self.ee.load_study_from_input_dict(inputs_dict)

        self.ee.execute()

        disc = self.ee.dm.get_disciplines_with_name(
            f'{self.name}.{self.model_name}')[0]
        filters = disc.get_chart_filter_list()
        graph_list = disc.get_post_processing_list(filters)
#         for graph in graph_list:
#             graph.to_plotly().show()
