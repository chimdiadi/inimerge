# -*- coding: utf-8 -*-
import sys
import os
import ConfigParser

from operator import itemgetter

class IniConfigMerge(object):

    _configs = None
    _default = None
    _last_order = 1

    def __init__(self):
        """
        IniConfigMerge takes in one or more .ini style configuration
        files and joins it into a single config for export as
        a file or dict
        """
        self._configs = []

    def __dict__(self):
        self.merge()
        c = {}
        for section in  self.default().sections():
            c.update({section:{}})
            for item in self.default().items(section):
                c[section].update(dict([item]))

        return c

    def load(self, filename):
        config = ConfigParser.RawConfigParser()
        config.read(filename)
        return config

    def default(self):     
        """
        Default config is order/index in _config 0
        Uses the default.ini or the first available config
        """
        for cfg in self._configs:
            if cfg['order'] == 0:
                return cfg['params']
        return self.first('params')


    def first(self, field=None):
        """
        get the first config file object
        @param field
        """
        return self.get(0, field)

    def last(self, field=None):
        """
        get the last config file object
        @param field
        """
        return self.get(-1, field)

    def get(self, index, field='params'):
        """
        # sort configs by file
        # set _merged as your go
        # on merge current overwrites pervious
        # output
        @param index
        @param field
        """

        try:
            if field is None:
                return self._configs[index]
            return self._configs[index][field]
        except Exception as e:
            print("No valid config found.")

    def get_all(self, field):
        """
        iterator gets list of configs by field
        """

        for cfg in self._configs:
            yield cfg[field]

    def merge(self):     
        """
        generates merged configuration
        """

        self._configs = sorted(self._configs, key=itemgetter('order')) 
        for i, cfg in enumerate(self._configs):
            if i is  0:
                continue

            for ss in self.get(i).sections():
                if not self.default().has_section(ss):
                    self.default().add_section(ss)
                print("Section: %s" % ss)
                [self.default().set(ss,_opt[0], _opt[1]) for _opt in self.get(i).items(ss)]
        return self.default()

    def append(self, filename):
        """
        append_ini - append ini configuration descriptor
        @param filename
        """
        self._configs.append(self.set_attr(filename, self.load(filename)))
        self.merge()


    def set_attr(self, filename, config_obj):
        """
        config_def - define the body of the config file
        @param self
        @param filename
        @param config_obj

        """
        body = dict()
        body['filename'] = filename
        body['params']   = config_obj
        body['order']    = self.get_order(filename)

        if body['order'] == 0:
            # 00_ or default trumps all other configs
            self._default = config_obj
        elif self._default is None:
            # Ensures that the first attr sets the default to something
            self._default = config_obj
        return body

    def get_order(self, filename):
        """
        get_order - order is defined by the filename
        expecting 00_default.ini as the topmost config file
        customer config files start at 100_
        the following formats are acceptable:
        - default.ini & 00_default.ini are considered the same
        - <int>_<name>.ini
        """
        fparts = os.path.basename(filename).split('_')
        if 'default.ini' in filename:
            return 0
        elif len(fparts) > 1:
            return int(fparts[0]) 
        self._last_order += 1 # increment by 1 
        return self._last_order


    def write(self, filename):
        """
        write
        @param  self
        @param  filename
        invoke ConfigParser.write
        """
        self.merge() 
        with open(filename, 'w') as fp:
            self.default().write(fp)


if __name__ == '__main__':
    c = IniConfigMerge() 
    c.append('/home/chimdi/Project/test/00_default.ini')
    c.append('/home/chimdi/Project/test/default.ini')
    c.append('/home/chimdi/Project/test/chimdi.ini')
    c.append('/home/chimdi/Project/test/100_story.ini')
    for v in c.get_all('order'):
        print("order %s" % v)

    c.write('/home/chimdi/Project/test/output.ini')
    print(c.__dict__())

