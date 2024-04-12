"""
Copyright 2023 Capgemini

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from climateeconomics.glossarycore import GlossaryCore as GlossaryWitnessCore


class GlossaryEnergy(GlossaryWitnessCore):
    """Glossary for witness energy, inheriting from glossary of Witness Core"""

    CCSListName = "ccs_list"
    EnergyListName = "energy_list"

    CO2Taxes = GlossaryWitnessCore.CO2Taxes
    CO2Taxes["namespace"] = "ns_energy_study"

    NB_POLES_UTILIZATION_RATIO = (
        10  # number of poles for bspline design variables utilization ratio
    )
    NB_POLES_COARSE: int = 7  # number of poles in witness coarse
    NB_POLES_FULL: int = 8  # number of poles in witness full
    NB_POLE_ENERGY_MIX_PROCESS = 12
    YearEndDefaultValueGradientTest = 2030
    LifetimeDefaultValueGradientTest = 7
    YearEndDefault = 2050
    YearEndDefaultCore = GlossaryWitnessCore.YearEndDefault
    YearEndVar = {
        "type": "int",
        "default": YearEndDefault,
        "unit": "year",
        "visibility": "Shared",
        "namespace": "ns_public",
        "range": [2000, 2300],
    }

    biogas = "biogas"
    biodiesel = "biodiesel"
    biomass_dry = "biomass_dry"
    ethanol = "ethanol"
    electricity = "electricity"
    fossil = "fossil"
    fuel = "fuel"
    gasoline = "gasoline"
    heating_oil = "heating_oil"
    hydrogen = "hydrogen"
    kerosene = "kerosene"
    liquid_fuel = "liquid_fuel"
    liquid_hydrogen = "liquid_hydrogen"
    gaseous_hydrogen = "gaseous_hydrogen"
    liquefied_petroleum_gas = "liquefied_petroleum_gas"
    hydrotreated_oil_fuel = "hydrotreated_oil_fuel"
    methane = "methane"
    renewable = "renewable"
    solid_fuel = "solid_fuel"
    syngas = "syngas"
    ultra_low_sulfur_diesel = "ultra_low_sulfur_diesel"
    wet_biomass = "wet_biomass"
    carbon_capture = "carbon_capture"
    carbon_storage = "carbon_storage"
    direct_air_capture = "direct_air_capture"
    flue_gas_capture = "flue_gas_capture"
    heat = "heat"
    lowtemperatureheat = "lowtemperatureheat"
    mediumtemperatureheat = "mediumtemperatureheat"
    hightemperatureheat = "hightemperatureheat"

    AllEnergies = [biogas,
                   biodiesel,
                   biomass_dry,
                   ethanol,
                   electricity,
                   fossil,
                   fuel,
                   gasoline,
                   heating_oil,
                   hydrogen,
                   kerosene,
                   liquid_fuel,
                   liquid_hydrogen,
                   gaseous_hydrogen,
                   liquefied_petroleum_gas,
                   hydrotreated_oil_fuel,
                   methane,
                   renewable,
                   solid_fuel,
                   syngas,
                   ultra_low_sulfur_diesel,
                   wet_biomass,
                   carbon_capture,
                   carbon_storage,
                   direct_air_capture,
                   flue_gas_capture,
                   heat,
                   lowtemperatureheat,
                   mediumtemperatureheat,
                   hightemperatureheat, ]

    LifetimeName = "lifetime"
    Transesterification = "Transesterification"
    AnaerobicDigestion = "AnaerobicDigestion"

    AllStreamsDemandRatioValue = "all_streams_demand_ratio"
    FlueGasMean = "flue_gas_mean"
    MarginValue = "margin"
    CO2EmissionsValue = "CO2_emissions"
    TechnoProductionValue = "techno_production"
    TechnoPricesValue = "techno_prices"
    TechnoDetailedConsumptionValue = "techno_detailed_consumption"
    TechnoDetailedProductionValue = "techno_detailed_production"
    TechnoDetailedPricesValue = "techno_detailed_prices"
    TechnoConsumptionValue = "techno_consumption"
    TechnoProductionWithoutRatioValue = "techno_production_woratio"
    RessourcesCO2EmissionsValue = "resources_CO2_emissions"
    TransportCostValue = "transport_cost"
    TransportMarginValue = "transport_margin"
    TransportDemandValue = "transport_demand"
    ForestInvestmentValue = "forest_investment"
    CarbonCapturedValue = "carbon_captured_type"
    InstalledPower = "power_production"  # todo : rename string to 'Installed Power [MW]' (check unit)

    # energy techno discipline names
    FossilSimpleTechno = "FossilSimpleTechno"
    RenewableSimpleTechno = "RenewableSimpleTechno"
    CarbonCaptureAndStorageTechno = "CarbonCaptureAndStorageTechno"
    CarbonStorageTechno = "CarbonStorageTechno"
    DirectAirCapture = "direct_air_capture.DirectAirCaptureTechno"
    FlueGasCapture = f"{flue_gas_capture}.FlueGasTechno"

    ResourcesUsedForProductionValue = "Resources used for production"
    ResourcesUsedForProduction = {
        "var_name": ResourcesUsedForProductionValue,
        "type": "list",
        "subtype_descriptor": {"list": "string"},
    }

    EnergiesUsedForProductionValue = "Energies used for production"
    EnergiesUsedForProduction = {
        "var_name": EnergiesUsedForProductionValue,
        "type": "list",
        "subtype_descriptor": {"list": "string"},
    }

    CostOfResourceUsageValue = "cost_of_resources_usage"
    CostOfResourceUsageDf = {
        "var_name": CostOfResourceUsageValue,
        "type": "dataframe",
        "unit": "?",
        "description": "Cost of usage for each resource",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "int",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
        },
    }
    N2OPerUse = "N2O_per_use"
    CH4PerUse = "CH4_per_use"
    CO2PerUse = "CO2_per_use"
    CO2PerUseDf = {
        "varname": CO2PerUse,
        "type": "dataframe",
        "unit": "kg/kWh",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: ("float", None, True),
            CO2PerUse: ("float", None, True),
        },
    }
    CH4PerUseDf = {
        "varname": CH4PerUse,
        "type": "dataframe",
        "unit": "kg/kWh",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: ("float", None, True),
            CH4PerUse: ("float", None, True),
        },
    }
    N2OPerUseDf = {
        "varname": N2OPerUse,
        "type": "dataframe",
        "unit": "kg/kWh",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: ("float", None, True),
            N2OPerUse: ("float", None, True),
        },
    }

    CostOfEnergiesUsageValue = "cost_of_energies_usage"
    CostOfEnergiesUsageDf = {
        "var_name": CostOfEnergiesUsageValue,
        "type": "dataframe",
        "unit": "?",
        "description": "Cost of usage for each energy",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "int",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
        },
    }

    SpecificCostsForProductionValue = "Specific costs for production"
    SpecificCostsForProduction = {
        "var_name": SpecificCostsForProductionValue,
        "type": "dataframe",
        "description": "Costs that are specific to the techno",
        "dynamic_dataframe_columns": True,
    }

    CCSTechnoInvest = {
        "type": "dataframe",
        "unit": "G$",
        "visibility": "Shared",
        "namespace": "ns_ccs",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "int",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
            "invest": ("float", [0.0, 1e30], True),
        },
    }

    EnergyTechnoInvest = {
        "type": "dataframe",
        "unit": "G$",
        "visibility": "Shared",
        "namespace": "ns_energy",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "int",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
            "invest": ("float", [0.0, 1e30], True),
        },
    }
    TechnoCapitalDf = {
        "var_name": GlossaryWitnessCore.TechnoCapitalValue,
        "type": "dataframe",
        "unit": "G$",
        "description": "Capital in G$ of the technology",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "int",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
            GlossaryWitnessCore.Capital: ("float", [0.0, 1e30], False),
        },
    }

    UtilisationRatioDf = {
        "var_name": GlossaryWitnessCore.UtilisationRatioValue,
        "type": "dataframe",
        "namespace": "ns_witness",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "int",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
            GlossaryWitnessCore.UtilisationRatioValue: ("float", [0, 100], False),
        },
    }

    EnergyTypeCapitalDfValue = "energy_type_capital"
    EnergyTypeCapitalDf = {
        "var_name": EnergyTypeCapitalDfValue,
        "type": "dataframe",
        "unit": "G$",
        # 'namespace': 'ns_energy',
        # 'visibility': 'Shared',
        "description": "Capital in G$ of the energy type",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "int",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
            GlossaryWitnessCore.Capital: ("float", [0.0, 1e30], False),
        },
    }

    TechnoInvestPercentageName = "techno_invest_percentage"
    TechnoInvestPercentage = {
        "var_name": TechnoInvestPercentageName,
        "type": "dataframe",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "int",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
        },
        "unit": "%",
        "description": "Percentage of investments in each energy technology based on total energy investments",
    }

    EnergyInvestPercentageGDPName = "percentage_of_gdp_energy_invest"
    EnergyInvestPercentageGDP = {
        "var_name": EnergyInvestPercentageGDPName,
        "type": "dataframe",
        "unit": "%",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "int",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
            EnergyInvestPercentageGDPName: ("float", [0, 100], True),
        },
        "description": "percentage of total energy investment in each of the energy technologies",
    }

    ManagedWoodInvestmentName = "managed_wood_investment"
    ManagedWoodInvestment = {
        "var_name": ManagedWoodInvestmentName,
        "type": "dataframe",
        "unit": "G$",
        "visibility": "Shared",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "float",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
            GlossaryWitnessCore.InvestmentsValue: ("float", [0.0, 1e30], False),
        },
        "namespace": "ns_forest",
        "dataframe_edition_locked": False,
    }

    DeforestationInvestmentName = "deforestation_investment"
    DeforestationInvestment = {
        "var_name": DeforestationInvestmentName,
        "type": "dataframe",
        "unit": "G$",
        "visibility": "Shared",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: ("float", None, False),
            GlossaryWitnessCore.InvestmentsValue: ("float", [0.0, 1e30], False),
        },
        "namespace": "ns_forest",
        "dataframe_edition_locked": False,
    }

    CropInvestmentName = "crop_investment"
    CropInvestment = {
        "var_name": CropInvestmentName,
        "type": "dataframe",
        "unit": "G$",
        "visibility": "Shared",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "float",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
            GlossaryWitnessCore.InvestmentsValue: ("float", [0.0, 1e30], False),
        },
        "namespace": "ns_crop",
        "dataframe_edition_locked": False,
    }

    TechnoListName = "technologies_list"
    TechnoList = {
        "var_name": TechnoListName,
        "type": "list",
        "subtype_descriptor": {"list": "string"},
        "structuring": True,
        "visibility": "Shared",
    }

    InvestLevel = {"type": "dataframe", "unit": "G$", "visibility": "Shared"}

    EnergyList = {
        "var_name": EnergyListName,
        "type": "list",
        "subtype_descriptor": {"list": "string"},
        "visibility": "Shared",
        "namespace": "ns_energy_study",
        "editable": False,
        "structuring": True,
    }

    CCSList = {
        "var_name": CCSListName,
        "type": "list",
        "subtype_descriptor": {"list": "string"},
        "visibility": "Shared",
        "namespace": "ns_energy_study",
        "editable": False,
        "structuring": True,
    }

    ForestInvestment = {
        "var_name": ForestInvestmentValue,
        "type": "dataframe",
        "unit": "G$",
        "visibility": "Shared",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "float",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
            ForestInvestmentValue: ("float", [0.0, 1e30], False),
        },
        "namespace": "ns_invest",
        "dataframe_edition_locked": False,
    }

    CarbonCaptured = {
        "var_name": CarbonCapturedValue,
        "type": "dataframe",
        "unit": "G$",
        "visibility": "Shared",
        "dataframe_descriptor": {
            GlossaryWitnessCore.Years: (
                "float",
                [1900, GlossaryWitnessCore.YearEndDefault],
                False,
            ),
            CarbonCapturedValue: ("float", [0.0, 1e30], False),
        },
        "namespace": "ns_invest",
        "dataframe_edition_locked": False,
    }

    # techno names
    GeothermalLowHeat = "GeothermalLowHeat"
    CropEnergy = "CropEnergy"
    ManagedWood = "ManagedWood"
    UnmanagedWood = "UnmanagedWood"
    BiomassBuryingFossilization = "BiomassBuryingFossilization"
    CarbonStorageTechno = "CarbonStorageTechno"
    DeepOceanInjection = "DeepOceanInjection"
    DeepSalineFormation = "DeepSalineFormation"
    DepletedOilGas = "DepletedOilGas"
    EnhancedOilRecovery = "EnhancedOilRecovery"
    GeologicMineralization = "GeologicMineralization"
    PureCarbonSolidStorage = "PureCarbonSolidStorage"
    Reforestation = "Reforestation"
    BiomassFired = "BiomassFired"
    CoalGen = "CoalGen"
    BiogasFired = "BiogasFired"
    CombinedCycleGasTurbine = "CombinedCycleGasTurbine"
    GasTurbine = "GasTurbine"
    Geothermal = "Geothermal"
    Hydropower = "Hydropower"
    Nuclear = "Nuclear"
    OilGen = "OilGen"
    RenewableElectricitySimpleTechno = "RenewableElectricitySimpleTechno"
    SolarPv = "SolarPv"
    SolarThermal = "SolarThermal"
    WindOffshore = "WindOffshore"
    WindOnshore = "WindOnshore"
    BiomassFermentation = "BiomassFermentation"
    FossilSimpleTechno = "FossilSimpleTechno"
    ElectrolysisAWE = "Electrolysis.AWE"
    ElectrolysisPEM = "Electrolysis.PEM"
    ElectrolysisSOEC = "Electrolysis.SOEC"
    PlasmaCracking = "PlasmaCracking"
    WaterGasShift = "WaterGasShift"
    CHPHighHeat = "CHPHighHeat"
    ElectricBoilerHighHeat = "ElectricBoilerHighHeat"
    GeothermalHighHeat = "GeothermalHighHeat"
    HeatPumpHighHeat = "HeatPumpHighHeat"
    NaturalGasBoilerHighHeat = "NaturalGasBoilerHighHeat"
    CHPLowHeat = "CHPLowHeat"
    ElectricBoilerLowHeat = "ElectricBoilerLowHeat"
    GeothermalLowHeat = "GeothermalLowHeat"
    HeatPumpLowHeat = "HeatPumpLowHeat"
    NaturalGasBoilerLowHeat = "NaturalGasBoilerLowHeat"
    CHPMediumHeat = "CHPMediumHeat"
    ElectricBoilerMediumHeat = "ElectricBoilerMediumHeat"
    GeothermalMediumHeat = "GeothermalMediumHeat"
    HeatPumpMediumHeat = "HeatPumpMediumHeat"
    NaturalGasBoilerMediumHeat = "NaturalGasBoilerMediumHeat"
    HefaDecarboxylation = "HefaDecarboxylation"
    HefaDeoxygenation = "HefaDeoxygenation"
    FischerTropsch = "FischerTropsch"
    Refinery = "Refinery"
    HydrogenLiquefaction = "HydrogenLiquefaction"
    FossilGas = "FossilGas"
    Methanation = "Methanation"
    UpgradingBiogas = "UpgradingBiogas"
    CO2Hydrogenation = "CO2Hydrogenation"
    RenewableSimpleTechno = "RenewableSimpleTechno"
    CoalExtraction = "CoalExtraction"
    Pelletizing = "Pelletizing"
    AutothermalReforming = "AutothermalReforming"
    BiomassGasification = "BiomassGasification"
    CoElectrolysis = "CoElectrolysis"
    CoalGasification = "CoalGasification"
    Pyrolysis = "Pyrolysis"
    ReversedWaterGasShift = "ReversedWaterGasShift"
    SMR = "SMR"
    AnimalManure = "AnimalManure"
    WetCropResidues = "WetCropResidues"
