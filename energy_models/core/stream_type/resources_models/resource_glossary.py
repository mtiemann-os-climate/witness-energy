'''
Copyright 2022 Airbus SAS
Modifications on 26/03/2024 Copyright 2024 Capgemini


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
from energy_models.core.stream_type.energy_models.heat import mediumtemperatureheat
from energy_models.glossaryenergy import GlossaryEnergy


class ResourceGlossary:
    '''
    Just a glossary to harmonize the resources names and data
    CO2 emissions [kgCO2/kg]
    Prices [$/t]
    '''

    UNITS = {'production': 'Mt', 'consumption': 'Mt', 'price': '$/t', GlossaryEnergy.CO2EmissionsValue: 'kgCO2/kg'}


    UraniumResource = 'uranium_resource'
    Uranium = {'name': UraniumResource,
               GlossaryEnergy.CO2EmissionsValue: 0.474 / 277.78,
               'price': 1390000.0, }
    WaterResource = 'water_resource'
    Water = {'name': WaterResource,
             GlossaryEnergy.CO2EmissionsValue: 0.0,
             'price': 1.78}

    SeaWaterResource = 'sea_water_resource'
    SeaWater = {'name': SeaWaterResource,
                GlossaryEnergy.CO2EmissionsValue: 0.0,
                'price': 1.4313}
    CO2Resource = 'CO2_resource'
    CO2 = {'name': CO2Resource,
           GlossaryEnergy.CO2EmissionsValue: -1.0,
           'price': 200.0}
    BiomassDryResource = 'biomass_dry_resource'
    BiomassDry = {'name': BiomassDryResource,
                  GlossaryEnergy.CO2EmissionsValue: - 0.425 * 44.01 / 12.0,
                  'price': 68.12}
    WetBiomassResource = 'wet_biomass_resource'
    WetBiomass = {'name': WetBiomassResource,
                  GlossaryEnergy.CO2EmissionsValue: - 0.9615,
                  'price': 56.0}
    # - 0.425 * 44.01 / 12.0 (old CO2_emissions value)
    # Calibration to have zero CO2 emissions in biogas.anaerobic_digestion when biogas use

    NaturalOilResource = 'natural_oil_resource'
    NaturalOil = {'name': NaturalOilResource,
                  GlossaryEnergy.CO2EmissionsValue: -2.95,
                  'price': 1100.0}
    MethanolResource = 'methanol_resource'
    Methanol = {'name': MethanolResource,
                GlossaryEnergy.CO2EmissionsValue: 0.54,
                'price': 400.0}
    SodiumHydroxideResource = 'sodium_hydroxide_resource'
    SodiumHydroxide = {'name': SodiumHydroxideResource,
                       GlossaryEnergy.CO2EmissionsValue: 0.6329,
                       'price': 425.0}
    WoodResource = 'wood_resource'
    Wood = {'name': WoodResource,
            GlossaryEnergy.CO2EmissionsValue: 1.78,
            'price': 120.0, }
    CarbonResource = 'carbon_resource'
    Carbon = {'name': CarbonResource,
              GlossaryEnergy.CO2EmissionsValue: 44.01 / 12.0,
              'price': 25000.0}
    ManagedWoodResource = 'managed_wood_resource'
    ManagedWood = {'name': ManagedWoodResource,
                   GlossaryEnergy.CO2EmissionsValue: 0.0,
                   'price': 37.5}
    OxygenResource = 'oxygen_resource'
    Oxygen = {'name': OxygenResource,
              GlossaryEnergy.CO2EmissionsValue: 0.0,
              'price': 10.0}
    DioxygenResource = 'dioxygen_resource'
    Dioxygen = {'name': DioxygenResource,
                GlossaryEnergy.CO2EmissionsValue: 0.0,
                'price': 10.0}
    CrudeOilResource = 'crude_oil_resource'
    CrudeOil = {'name': CrudeOilResource,
                GlossaryEnergy.CO2EmissionsValue: 0.02533,
                'price': 44.0}
    SolidFuelResource = 'solid_fuel_resource'
    SolidFuel = {'name': SolidFuelResource,
                 GlossaryEnergy.CO2EmissionsValue: 0.64 / 4.86,
                 'price': 250.0}
    CalciumResource = 'calcium_resource'
    Calcium = {'name': CalciumResource,
               GlossaryEnergy.CO2EmissionsValue: 0.0,
               'price': 85.0}
    CalciumOxydeResource = 'calcium_oxyde_resource'
    CalciumOxyde = {'name': CalciumOxydeResource,
                    GlossaryEnergy.CO2EmissionsValue: 0.0,
                    'price': 150.0}
    PotassiumResource = 'potassium_resource'
    Potassium = {'name': PotassiumResource,
                 GlossaryEnergy.CO2EmissionsValue: 0.0,
                 'price': 500.0}
    PotassiumHydroxideResource = 'potassium_hydroxide_resource'
    PotassiumHydroxide = {'name': PotassiumHydroxideResource,
                          GlossaryEnergy.CO2EmissionsValue: 0.0,
                          'price': 500.0}
    AmineResource = 'amine_resource'
    Amine = {'name': AmineResource,
             GlossaryEnergy.CO2EmissionsValue: 0.0,
             'price': 1300.0}
    EthanolAmineResource = 'ethanol_amine_resource'
    EthanolAmine = {'name': EthanolAmineResource,
                    GlossaryEnergy.CO2EmissionsValue: 0.0,
                    'price': 1700.0}
    MonoEthanolAmineResource = 'mono_ethanol_amine_resource'
    MonoEthanolAmine = {'name': MonoEthanolAmineResource,
                        GlossaryEnergy.CO2EmissionsValue: 0.0,
                        'price': 1700.0}
    GlycerolResource = 'glycerol_resource'
    Glycerol = {'name': GlycerolResource,
                GlossaryEnergy.CO2EmissionsValue: 0.0,
                'price': 0.0}
    NaturalGasResource = 'natural_gas_resource'
    NaturalGas = {'name': NaturalGasResource,
                  GlossaryEnergy.CO2EmissionsValue: 0.0,
                  'price': 0.0}
    CoalResource = 'coal_resource'
    Coal = {'name': CoalResource,
            GlossaryEnergy.CO2EmissionsValue: 0.0,
            'price': 0.0}
    OilResource = 'oil_resource'
    Oil = {'name': OilResource,
           GlossaryEnergy.CO2EmissionsValue: 0.02533,
           'price': 44.0}

    CopperResource = 'copper_resource'
    Copper = {'name': CopperResource,
              GlossaryEnergy.CO2EmissionsValue: 0.0,
              'price': 10057.0}

    PlatinumResource = 'platinum_resource'
    Platinum = {'name': PlatinumResource,
                GlossaryEnergy.CO2EmissionsValue: 0.0,
                'price': 32825887.76}

    GlossaryDict = {
        'Uranium': Uranium, 'Water': Water, 'SeaWater': SeaWater, 'CO2': CO2, 'BiomassDry': BiomassDry,
        'WetBiomass': WetBiomass, 'NaturalOil': NaturalOil, 'Methanol': Methanol,
        'SodiumHydroxide': SodiumHydroxide, 'Wood': Wood, 'Carbon': Carbon, 'ManagedWood': ManagedWood,
        'Oxygen': Oxygen, 'Dioxygen': Dioxygen, 'CrudeOil': CrudeOil, 'SolidFuel': SolidFuel,
        'Calcium': Calcium, 'CalciumOxyde': CalciumOxyde, 'Potassium': Potassium,
        'PotassiumHydroxide': PotassiumHydroxide, 'Amine': Amine, 'EthanolAmine': EthanolAmine,
        'MonoEthanolAmine': MonoEthanolAmine, 'Glycerol': Glycerol, 'NaturalGas': NaturalGas,
        'Coal': Coal, 'Oil': Oil, 'Copper': Copper, 'Platinum': Platinum,
    }

    TechnoResourceUsedDict = {
        GlossaryEnergy.Transesterification: [MethanolResource, NaturalOilResource, SodiumHydroxideResource, WaterResource],
        GlossaryEnergy.AnaerobicDigestion: [WetBiomassResource],
        f'{GlossaryEnergy.direct_air_capture}.AmineScrubbing': [AmineResource],
        f'{GlossaryEnergy.direct_air_capture}.CalciumPotassiumScrubbing': [CalciumResource, PotassiumResource],
        GlossaryEnergy.CoalGen: [WaterResource],
        GlossaryEnergy.Nuclear: [UraniumResource, WaterResource],
        GlossaryEnergy.OilGen: [WaterResource],
        GlossaryEnergy.BiomassFermentation: [WaterResource],
        GlossaryEnergy.ElectrolysisAWE: [WaterResource],
        GlossaryEnergy.ElectrolysisPEM: [WaterResource, PlatinumResource],
        GlossaryEnergy.ElectrolysisSOEC: [WaterResource],
        GlossaryEnergy.Refinery: [OilResource],
        GlossaryEnergy.FossilGas: [NaturalGasResource],
        GlossaryEnergy.Methanation: [CO2Resource],
        GlossaryEnergy.CO2Hydrogenation: [WaterResource],
        GlossaryEnergy.CoalExtraction: [CoalResource],
        GlossaryEnergy.AutothermalReforming: [CO2Resource, OxygenResource],
        GlossaryEnergy.CoElectrolysis : [CO2Resource, WaterResource],
        GlossaryEnergy.Pyrolysis: [WoodResource],
        GlossaryEnergy.WaterGasShift: [WaterResource],
        GlossaryEnergy.ReversedWaterGasShift: [CO2Resource],
        GlossaryEnergy.SMR: [WaterResource],
        GlossaryEnergy.HefaDecarboxylation: [NaturalOilResource],
        GlossaryEnergy.HefaDeoxygenation: [NaturalOilResource],
        GlossaryEnergy.BiomassGasification: [WaterResource],
        GlossaryEnergy.CropEnergy: [CO2Resource]
    }

    # dictionnary of energies used by each techno
    TechnoEnergiesUsedDict = {
        GlossaryEnergy.Transesterification: [GlossaryEnergy.electricity],
        GlossaryEnergy.AnaerobicDigestion: [GlossaryEnergy.electricity],
        GlossaryEnergy.ManagedWood: [GlossaryEnergy.electricity],
        GlossaryEnergy.UnmanagedWood: [GlossaryEnergy.electricity],
        f'{GlossaryEnergy.direct_air_capture}.AmineScrubbing': [GlossaryEnergy.electricity, GlossaryEnergy.methane],
        f'{GlossaryEnergy.direct_air_capture}.CalciumPotassiumScrubbing': [GlossaryEnergy.electricity, GlossaryEnergy.methane],
        f'{GlossaryEnergy.direct_air_capture}.DirectAirCaptureTechno': [GlossaryEnergy.renewable, GlossaryEnergy.fossil],
        f'{GlossaryEnergy.flue_gas_capture}.CalciumLooping': [GlossaryEnergy.electricity],
        f'{GlossaryEnergy.flue_gas_capture}.ChilledAmmoniaProcess': [GlossaryEnergy.electricity],
        f'{GlossaryEnergy.flue_gas_capture}.CO2Membranes': [GlossaryEnergy.electricity],
        f'{GlossaryEnergy.flue_gas_capture}.FlueGasTechno': [GlossaryEnergy.renewable],
        f'{GlossaryEnergy.flue_gas_capture}.MonoEthanolAmine': [GlossaryEnergy.electricity],
        f'{GlossaryEnergy.flue_gas_capture}.PiperazineProcess': [GlossaryEnergy.electricity],
        f'{GlossaryEnergy.flue_gas_capture}.PressureSwingAdsorption': [GlossaryEnergy.electricity],
        GlossaryEnergy.BiomassFired: [GlossaryEnergy.biomass_dry],
        GlossaryEnergy.CoalGen: [GlossaryEnergy.solid_fuel],
        GlossaryEnergy.GasTurbine: [GlossaryEnergy.methane],
        GlossaryEnergy.CombinedCycleGasTurbine: [GlossaryEnergy.methane],
        GlossaryEnergy.BiogasFired: [GlossaryEnergy.biogas],
        GlossaryEnergy.OilGen: [f"{GlossaryEnergy.fuel}.{GlossaryEnergy.liquid_fuel}"],
        GlossaryEnergy.BiomassFermentation: [GlossaryEnergy.biomass_dry, GlossaryEnergy.electricity],
        GlossaryEnergy.ElectrolysisAWE: [GlossaryEnergy.electricity],
        GlossaryEnergy.ElectrolysisPEM: [GlossaryEnergy.electricity],
        GlossaryEnergy.ElectrolysisSOEC: [GlossaryEnergy.electricity],
        GlossaryEnergy.PlasmaCracking: [GlossaryEnergy.electricity, GlossaryEnergy.methane],
        GlossaryEnergy.WaterGasShift: [GlossaryEnergy.electricity, GlossaryEnergy.syngas],
        GlossaryEnergy.CHPHighHeat: [GlossaryEnergy.methane],
        GlossaryEnergy.ElectricBoilerHighHeat: [GlossaryEnergy.electricity],
        GlossaryEnergy.GeothermalHighHeat: [GlossaryEnergy.electricity],
        GlossaryEnergy.HeatPumpHighHeat: [GlossaryEnergy.electricity],
        GlossaryEnergy.NaturalGasBoilerHighHeat: [GlossaryEnergy.methane],
        GlossaryEnergy.CHPLowHeat: [GlossaryEnergy.methane],
        GlossaryEnergy.ElectricBoilerLowHeat: [GlossaryEnergy.electricity],
        GlossaryEnergy.GeothermalLowHeat: [GlossaryEnergy.electricity],
        GlossaryEnergy.HeatPumpLowHeat: [GlossaryEnergy.electricity],
        GlossaryEnergy.NaturalGasBoilerLowHeat: [GlossaryEnergy.methane],
        GlossaryEnergy.CHPMediumHeat: [GlossaryEnergy.methane],
        GlossaryEnergy.ElectricBoilerMediumHeat: [GlossaryEnergy.electricity],
        GlossaryEnergy.GeothermalMediumHeat: [GlossaryEnergy.electricity],
        GlossaryEnergy.HeatPumpMediumHeat: [GlossaryEnergy.electricity],
        GlossaryEnergy.NaturalGasBoilerMediumHeat: [GlossaryEnergy.methane],
        GlossaryEnergy.HefaDecarboxylation: [f"{GlossaryEnergy.hydrogen}.{GlossaryEnergy.gaseous_hydrogen}", GlossaryEnergy.electricity],
        GlossaryEnergy.HefaDeoxygenation: [f"{GlossaryEnergy.hydrogen}.{GlossaryEnergy.gaseous_hydrogen}", GlossaryEnergy.electricity],
        GlossaryEnergy.FischerTropsch: [GlossaryEnergy.electricity],
        GlossaryEnergy.Refinery: [f"{GlossaryEnergy.hydrogen}.{GlossaryEnergy.gaseous_hydrogen}", GlossaryEnergy.electricity],
        GlossaryEnergy.HydrogenLiquefaction: [f"{GlossaryEnergy.hydrogen}.{GlossaryEnergy.gaseous_hydrogen}", GlossaryEnergy.electricity],
        GlossaryEnergy.FossilGas: [GlossaryEnergy.electricity],
        GlossaryEnergy.Methanation: [f"{GlossaryEnergy.hydrogen}.{GlossaryEnergy.gaseous_hydrogen}"],
        GlossaryEnergy.UpgradingBiogas: [GlossaryEnergy.electricity, GlossaryEnergy.biogas],
        GlossaryEnergy.CO2Hydrogenation: [f"{GlossaryEnergy.hydrogen}.{GlossaryEnergy.gaseous_hydrogen}", GlossaryEnergy.electricity, GlossaryEnergy.carbon_capture],
        GlossaryEnergy.CoalExtraction: [GlossaryEnergy.electricity],
        GlossaryEnergy.Pelletizing: [GlossaryEnergy.electricity, GlossaryEnergy.biomass_dry],
        GlossaryEnergy.AutothermalReforming: [GlossaryEnergy.methane],
        GlossaryEnergy.BiomassGasification: [GlossaryEnergy.electricity, GlossaryEnergy.biomass_dry],
        GlossaryEnergy.CoElectrolysis: [GlossaryEnergy.electricity],
        GlossaryEnergy.CoalGasification: [GlossaryEnergy.solid_fuel],
        GlossaryEnergy.ReversedWaterGasShift: [GlossaryEnergy.electricity, GlossaryEnergy.syngas],
        GlossaryEnergy.SMR: [GlossaryEnergy.electricity, GlossaryEnergy.methane],
        GlossaryEnergy.AnimalManure: [GlossaryEnergy.electricity],
        GlossaryEnergy.WetCropResidues: [GlossaryEnergy.electricity],
        GlossaryEnergy.Geothermal: [GlossaryEnergy.mediumtemperatureheat_energyname]
    }

    ResourcesList = [UraniumResource,
                     WaterResource,
                     SeaWaterResource,
                     CO2Resource,
                     BiomassDryResource,
                     WetBiomassResource,
                     NaturalOilResource,
                     MethanolResource,
                     SodiumHydroxideResource,
                     WoodResource,
                     CarbonResource,
                     ManagedWoodResource,
                     OxygenResource,
                     DioxygenResource,
                     CrudeOilResource,
                     SolidFuelResource,
                     CalciumResource,
                     CalciumOxydeResource,
                     PotassiumResource,
                     PotassiumHydroxideResource,
                     AmineResource,
                     EthanolAmineResource,
                     MonoEthanolAmineResource,
                     GlycerolResource,
                     NaturalGasResource,
                     CoalResource,
                     OilResource,
                     CopperResource,
                     PlatinumResource, ]