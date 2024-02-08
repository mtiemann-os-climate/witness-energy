'''
Copyright 2024 Capgemini
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
from energy_models.core.energy_study_manager import DEFAULT_COARSE_TECHNO_DICT
from energy_models.sos_processes.energy.MDO.energy_mix_optim_process.usecase import Study as subStudy
from energy_models.glossaryenergy import GlossaryEnergy


class Study(subStudy):
    def __init__(
            self,
            file_path=__file__,
            year_start=GlossaryEnergy.YeartStartDefault,
            year_end=2050,
            main_study=True,
            bspline=True,
            execution_engine=None,
    ):
        super().__init__(
            file_path=file_path,
            main_study=main_study,
            execution_engine=execution_engine,
            bspline=bspline,
            year_start=year_start,
            year_end=year_end,
            techno_dict=DEFAULT_COARSE_TECHNO_DICT
        )


if "__main__" == __name__:
    uc_cls = Study()
    uc_cls.load_data()
    uc_cls.run()