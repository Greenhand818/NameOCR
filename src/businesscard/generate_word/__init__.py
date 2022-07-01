from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy

__all__ = ['build_generate_content']

from .GenerateEmail import RandEmail
# from .GenerateAddr import GenerateAddr
# from .GenerateNet import GenerateNet
from .GenerateName import RandName
# from .GeneratePhone import GeneratePhone
# from .GenerateCompany import GenerateCompany


def build_generate_content(config, global_config=None):
    support_dict = [
        'RandEmail', 'GenerateAddr', 'GenerateNet', 'RandName', 'GeneratePhone', 'GenerateCompany', 'GeneratePost'
    ]

    config = copy.deepcopy(config)
    module_name = config.pop('name')
    if module_name == "None":
        return
    if global_config is not None:
        config.update(global_config)
    assert module_name in support_dict, Exception(
        'generate content on business cards only support {}'.format(support_dict))
    module_class = eval(module_name)(**config)
    return module_class
