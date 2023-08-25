import _collections_abc
from typing import Dict, List
from enum import Enum


class PropertyType(str, Enum):
    string = 'string'
    integer = 'integer'
    bool = 'boolean'


class property():
    def __init__(self, name: str, type: PropertyType, description: str, required: bool = True, enum: List = [],
                 default: str = None):
        self.name = name
        self.type = type
        self.description = description
        self.required = required  # making this property required or optional for gpt to fill
        self.enum = enum  # it doesn't strictly define options for gpt, only loosely
        self.default = default


class properties(Dict):
    def add(self, item: property):
        if isinstance(item, property):
            super().__setitem__(item.name,
                                {'type': item.type.value, 'description': item.description, 'required': item.required})
        else:
            raise ValueError('Must be type "property."')

        # add enumerators if passed
        if item.enum != None and len(item.enum) > 0:
            super().__getitem__(item.name)['enum'] = item.enum

        # default of property
        if item.default != None:
            super().__getitem__(item.name)['default'] = item.default


class function():
    def __init__(self, fn, trigger_fn, name: str, description: str):
        self.fn = fn  # function to be executed (with params)
        self.trigger_fn = trigger_fn  # insert trigger fn for ui flow here
        self.name = name
        self.description = description
        self.properties = properties()
        self.properties_wo_required = {}

    def to_json(self):
        # create "required" list for chatcompletion
        self.required = [k for k, v in self.properties.items() if v['required'] == True]

        # remove 'required' attribute from properties as it is a list of it's own
        for k, v in self.properties.items():
            self.properties_wo_required[k] = {m: v[m] for m in v.keys() - {'required'}}

        funct = {'name': self.name,
                 'description': self.description,
                 'parameters': {'type': 'object',
                                'properties': self.properties_wo_required},
                 'required': self.required
                }
        return funct
    
    # user for specific function call, like in OPENAI_FUNCTION_CALL_OPTIONS
    def to_json_without_params(self):
        funct = {'name': self.name,
                 'description': self.description,
                 'parameters': {'type': 'object',
                                'properties': {}},
                }
        return funct


class functions(_collections_abc.MutableMapping):
    def __init__(self):
        super().__init__()
        self._dict = dict()

    def __getitem__(self, key):
        return self._dict.__getitem__(key)

    def __setitem__(self, key, value):
        self._dict.__setitem__(key, value)
        self._changed = True

    def __delitem__(self, key):
        self._dict.__delitem__(key)
        self._changed = True

    def __iter__(self):
        return self._dict.__iter__()

    def __len__(self):
        return self._dict.__len__()

    # ChatGPT is expecting an List.
    def to_json_without_params(self):
        l = []
        for item in self._dict:
            l.append(self._dict[item].to_json_without_params())
        return l
