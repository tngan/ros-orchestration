#!/usr/bin/env python
# This is a script constructing the interface of suite

__version__ = '1.0.0'

# some common properties are defined here
__yml_root__ = 'stream'
__yml_state_name__ = 'state'

class Suite:

    @staticmethod
    def parseFromYml(cfg):
        return { instance[__yml_state_name__]: instance for instance in cfg[__yml_root__] }

    @staticmethod
    def getInitialState(cfg):
        return cfg[__yml_root__][0][__yml_state_name__]

    @staticmethod
    def getEndState(cfg):
        return cfg[__yml_root__][-1][__yml_state_name__]
