#  Copyright (c) 2022 github.com/shadowdog9500 .
#  License: MIT

import yaml
from src.cls.patchCls import patch


class ymlOperations:

    def loadYmlData(self, path):
        with open(path) as f:
            data = yaml.safe_load(f)

        patch_ojb_list = []
        for element in data:
            patch_ojb_list.append(patch(element))

        return patch_ojb_list

    def saveNewYml(self, data: list, path):
        if len(data) > 0:
            # Loop through the patch list to determine what patches are enabled
            final_list: list = []
            for element in data:
                if element.getEnabled():
                    final_list.append(element.getRawData())

            # Open the file to write the new config file
            with open("{}/tmp.yml".format(path), 'w') as nf:
                yaml.dump(final_list, nf, default_style=False)
