# -*- coding: utf-8 -*-
"""
Created on Monday Nov 29 17:21:18 2021

"""

from sos_trades_core.execution_engine.execution_engine import ExecutionEngine
from energy_models.sos_processes.energy.MDA.energy_process_v0.usecase import Study as MDA_Energy
import pickle

if '__main__' == __name__:
    # Run MDA Energy
    name = 'Data_Generator'
    ee = ExecutionEngine(name)
    model_name = 'EnergyMix'

    repo = 'energy_models.sos_processes.energy.MDA'
    builder = ee.factory.get_builder_from_process(
        repo, 'energy_process_v0')

    ee.factory.set_builders_to_coupling_builder(builder)
    ee.configure()
    usecase = MDA_Energy(execution_engine=ee)
    usecase.study_name = name
    values_dict = usecase.setup_usecase()

    ee.display_treeview_nodes()
    full_values_dict = {}
    for dict_v in values_dict:
        full_values_dict.update(dict_v)

    full_values_dict[f'{name}.epsilon0'] = 1.0
    full_values_dict[f'{name}.tolerance'] = 1.0e-8
    full_values_dict[f'{name}.sub_mda_class'] = 'MDAGaussSeidel'
    full_values_dict[f'{name}.max_mda_iter'] = 200

    ee.load_study_from_input_dict(full_values_dict)

    ee.execute()

    Energy_Mix_disc = ee.dm.get_disciplines_with_name(
        f'{name}.{model_name}')[0]
    energy_list = Energy_Mix_disc.get_sosdisc_inputs(
        'energy_list')

    # Collect input and output data from each energy and each techno
    mda_energy_data_streams_input_dict, mda_energy_data_streams_output_dict = {}, {}
    mda_energy_data_technologies_input_dict, mda_energy_data_technologies_output_dict = {}, {}

    ############
    # Energies #
    ############
    for energy in energy_list:
        # Loop on energies
        energy_disc = ee.dm.get_disciplines_with_name(
            f'{name}.{model_name}.{energy}')[0]
        # Inputs
        mda_energy_data_streams_input_dict[energy] = {}
        # Check if the input is a coupling
        full_inputs = energy_disc.get_input_data_names()
        # For the coupled inputs and outputs, test inputs/outputs on all
        # namespaces
        coupled_inputs = []
        namespaces = [f'{name}.', f'{name}.{model_name}.',
                      f'{name}.{model_name}.{energy}.']
        for namespace in namespaces:
            coupled_inputs += [input[len(namespace):] for input in full_inputs if ee.dm.get_data(
                input, 'coupling')]
        # Loop on inputs and fill the dict with value and boolean is_coupling
        for key in energy_disc.get_sosdisc_inputs().keys():
            is_coupling = False
            if key in coupled_inputs:
                is_coupling = True
            mda_energy_data_streams_input_dict[energy][key] = {
                'value': energy_disc.get_sosdisc_inputs(key), 'is_coupling': is_coupling}
        # Output
        mda_energy_data_streams_output_dict[energy] = {}
        full_outputs = energy_disc.get_output_data_names()
        # For the coupled inputs and outputs, test inputs/outputs on all
        # namespaces
        coupled_outputs = []
        namespaces = [f'{name}.', f'{name}.{model_name}.',
                      f'{name}.{model_name}.{energy}.']
        for namespace in namespaces:
            coupled_outputs += [output[len(namespace):] for output in full_outputs if ee.dm.get_data(
                output, 'coupling')]
        for key in energy_disc.get_sosdisc_outputs().keys():
            is_coupling = False
            if key in coupled_outputs:
                is_coupling = True
            mda_energy_data_streams_output_dict[energy][key] = {
                'value': energy_disc.get_sosdisc_outputs(key), 'is_coupling': is_coupling}
        ################
        # Technologies #
        ################
        technologies_list = energy_disc.get_sosdisc_inputs('technologies_list')
        for techno in technologies_list:
            # Loop on technologies
            techno_disc = ee.dm.get_disciplines_with_name(
                f'{name}.{model_name}.{energy}.{techno}')[0]
            # Inputs
            mda_energy_data_technologies_input_dict[techno] = {}
            full_inputs = techno_disc.get_input_data_names()
            # For the coupled inputs and outputs, test inputs/outputs on all
            # namespaces
            coupled_inputs = []
            namespaces = [f'{name}.', f'{name}.{model_name}.', f'{name}.{model_name}.{energy}.',
                          f'{name}.{model_name}.{energy}.{techno}.']
            for namespace in namespaces:
                coupled_inputs += [input[len(namespace):] for input in full_inputs if ee.dm.get_data(
                    input, 'coupling')]
            for key in techno_disc.get_sosdisc_inputs().keys():
                is_coupling = False
                if key in coupled_inputs:
                    is_coupling = True
                mda_energy_data_technologies_input_dict[techno][key] = {
                    'value': techno_disc.get_sosdisc_inputs(key), 'is_coupling': is_coupling}
            # Output
            mda_energy_data_technologies_output_dict[techno] = {}
            full_outputs = techno_disc.get_output_data_names()
            # For the coupled inputs and outputs, test inputs/outputs on all
            # namespaces
            coupled_outputs = []
            namespaces = [f'{name}.', f'{name}.{model_name}.', f'{name}.{model_name}.{energy}.',
                          f'{name}.{model_name}.{energy}.{techno}.']
            for namespace in namespaces:
                coupled_outputs += [output[len(namespace):] for output in full_outputs if ee.dm.get_data(
                    output, 'coupling')]
            for key in techno_disc.get_sosdisc_outputs().keys():
                is_coupling = False
                if key in coupled_outputs:
                    is_coupling = True
                mda_energy_data_technologies_output_dict[techno][key] = {
                    'value': techno_disc.get_sosdisc_outputs(key), 'is_coupling': is_coupling}

    ccs_list = Energy_Mix_disc.get_sosdisc_inputs(
        'ccs_list')
    ###############
    # CCS Streams #
    ###############
    for stream in ccs_list:
        stream_disc = ee.dm.get_disciplines_with_name(
            f'{name}.CCUS.{stream}')[0]
        # Inputs
        mda_energy_data_streams_input_dict[stream] = {}
        full_inputs = stream_disc.get_input_data_names()
        # For the coupled inputs and outputs, test inputs/outputs on all
        # namespaces
        coupled_inputs = []
        namespaces = [f'{name}.', f'{name}.CCUS.', f'{name}.CCUS.{stream}.', ]
        for namespace in namespaces:
            coupled_inputs += [input[len(namespace):] for input in full_inputs if ee.dm.get_data(
                input, 'coupling')]
        for key in stream_disc.get_sosdisc_inputs().keys():
            is_coupling = False
            if key in coupled_inputs:
                is_coupling = True
            mda_energy_data_streams_input_dict[stream][key] = {
                'value': stream_disc.get_sosdisc_inputs(key), 'is_coupling': is_coupling}
        # Output
        mda_energy_data_streams_output_dict[stream] = {}
        full_outputs = stream_disc.get_output_data_names()
        # For the coupled inputs and outputs, test inputs/outputs on all
        # namespaces
        coupled_outputs = []
        namespaces = [f'{name}.', f'{name}.CCUS.', f'{name}.CCUS.{stream}.']
        for namespace in namespaces:
            coupled_outputs += [output[len(namespace):] for output in full_outputs if ee.dm.get_data(
                output, 'coupling')]
        for key in stream_disc.get_sosdisc_outputs().keys():
            is_coupling = False
            if key in coupled_outputs:
                is_coupling = True
            mda_energy_data_streams_output_dict[stream][key] = {
                'value': stream_disc.get_sosdisc_outputs(key), 'is_coupling': is_coupling}
        ################
        # Technologies #
        ################
        technologies_list = stream_disc.get_sosdisc_inputs('technologies_list')
        for techno in technologies_list:
            # Loop on technologies
            techno_disc = ee.dm.get_disciplines_with_name(
                f'{name}.CCUS.{stream}.{techno}')[0]
            # Inputs
            mda_energy_data_technologies_input_dict[techno] = {}
            full_inputs = techno_disc.get_input_data_names()
            # For the coupled inputs and outputs, test inputs/outputs on all
            # namespaces
            coupled_inputs = []
            namespaces = [f'{name}.', f'{name}.CCUS.', f'{name}.CCUS.{stream}.',
                          f'{name}.CCUS.{stream}.{techno}.']
            for namespace in namespaces:
                coupled_inputs += [input[len(namespace):] for input in full_inputs if ee.dm.get_data(
                    input, 'coupling')]
            for key in techno_disc.get_sosdisc_inputs().keys():
                is_coupling = False
                if key in coupled_inputs:
                    is_coupling = True
                mda_energy_data_technologies_input_dict[techno][key] = {
                    'value': techno_disc.get_sosdisc_inputs(key), 'is_coupling': is_coupling}
            # Output
            mda_energy_data_technologies_output_dict[techno] = {}
            full_outputs = techno_disc.get_output_data_names()
            # For the coupled inputs and outputs, test inputs/outputs on all
            # namespaces
            coupled_outputs = []
            namespaces = [f'{name}.', f'{name}.CCUS.', f'{name}.CCUS.{stream}.',
                          f'{name}.CCUS.{stream}.{techno}.']
            for namespace in namespaces:
                coupled_outputs += [output[len(namespace):] for output in full_outputs if ee.dm.get_data(
                    output, 'coupling')]
            for key in techno_disc.get_sosdisc_outputs().keys():
                is_coupling = False
                if key in coupled_outputs:
                    is_coupling = True
                mda_energy_data_technologies_output_dict[techno][key] = {
                    'value': techno_disc.get_sosdisc_outputs(key), 'is_coupling': is_coupling}

    output = open('mda_energy_data_streams_input_dict.pkl', 'wb')
    pickle.dump(mda_energy_data_streams_input_dict, output)
    output.close()

    output = open('mda_energy_data_streams_output_dict.pkl', 'wb')
    pickle.dump(mda_energy_data_streams_output_dict, output)
    output.close()

    output = open('mda_energy_data_technologies_input_dict.pkl', 'wb')
    pickle.dump(mda_energy_data_technologies_input_dict, output)
    output.close()

    output = open('mda_energy_data_technologies_output_dict.pkl', 'wb')
    pickle.dump(mda_energy_data_technologies_output_dict, output)
    output.close()
