# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser, NoSectionError


class configer(object):

    def __int__(self):
        super(configer, self).__int__()
        self.__dict__.update(self._get_config())

    def find(self, field):
        return self.__dict__.get(field, None)

    def set(self, field, value):
        self.__dict__[field] = value
        section = self._locate_option(field)
        if section is None:
            return  # section 不存在时不做任何处理
        configfile = ConfigParser()
        configfile.read('config.cfg')
        configfile.set(section, field, value)
        with open('config.cfg', 'w') as fp:
            configfile.write(fp)

    def create(self, section, field, value):
        self.__dict__.update({field: value})
        configfile = ConfigParser()
        configfile.read('config.cfg')
        try:
            configfile.set(section, field, value)
        except NoSectionError:
            configfile.add_section(section)
            configfile.set(section, field, value)
        with open('config.cfg', 'w') as fp:
            configfile.write(fp)

    def _get_config(self):
        configfile = ConfigParser()
        configfile.read('config.cfg')
        options = {}
        for section in configfile.sections():
            for option in configfile.items(section):
                options[option[0]] = option[1]
        return options

    def _locate_option(self, option):
        configfile = ConfigParser()
        configfile.read('config.cfg')
        for section in configfile.sections():
            if configfile.has_option(section, option):
                return section
        return None
