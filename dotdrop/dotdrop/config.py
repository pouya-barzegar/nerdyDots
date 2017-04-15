"""
author: deadc0de6 (https://github.com/deadc0de6)
Copyright (c) 2017, deadc0de6
config file manager
"""

import yaml
import os
from dotfile import Dotfile
from logger import Logger


class Cfg:
    key_all = 'ALL'
    key_config = 'config'
    key_profiles = 'profiles'
    key_dotfiles = 'dotfiles'
    key_dotfiles_src = 'src'
    key_dotfiles_dst = 'dst'

    def __init__(self, cfgpath, dotpath):
        if not os.path.exists(cfgpath):
            raise ValueError('config file does not exist')
        self.cfgpath = cfgpath
        self.log = Logger()
        relconf = dotpath
        if not relconf.startswith(os.sep):
            relconf = os.path.join(os.path.dirname(cfgpath), dotpath)
        self.configs = {'dotpath': relconf}
        self.dotfiles = {}
        self.profiles = {}
        self.prodots = {}
        if not self._load_file():
            raise ValueError('config is not valid')

    def _load_file(self):
        with open(self.cfgpath, 'r') as f:
            self.content = yaml.load(f)
        if not self._is_valid():
            return False
        return self._parse()

    def _is_valid(self):
        if self.key_profiles not in self.content:
            self.log.err('missing \"%s\" in config' % (self.key_profiles))
            return False
        if self.key_config not in self.content:
            self.log.err('missing \"%s\" in config' % (self.key_config))
            return False
        if self.key_dotfiles not in self.content:
            self.log.err('missing \"%s\" in config' % (self.key_dotfiles))
            return False
        return True

    def _parse(self):
        """ parse config file """
        self.profiles = self.content[self.key_profiles]
        if self.profiles is None:
            self.profiles = {}
        self.configs = self.content[self.key_config]
        # contains all defined dotfiles
        if self.content[self.key_dotfiles] is not None:
            for k, v in self.content[self.key_dotfiles].items():
                src = v[self.key_dotfiles_src]
                dst = v[self.key_dotfiles_dst]
                self.dotfiles[k] = Dotfile(k, dst, src)
        # contains a list of dotfiles defined for each profile
        for k, v in self.profiles.items():
            self.prodots[k] = []
            if v is None:
                continue
            if len(v) == 1 and v == [self.key_all]:
                self.prodots[k] = self.dotfiles.values()
            else:
                self.prodots[k].extend([self.dotfiles[dot] for dot in v])
        # make sure we have a correct dotpath
        if not self.configs['dotpath'].startswith(os.sep):
            relconf = os.path.join(os.path.dirname(
                self.cfgpath), self.configs['dotpath'])
            self.configs['dotpath'] = relconf
        return True

    def new(self, dotfile, profile):
        """ import new dotfile """
        dots = self.content[self.key_dotfiles]
        if dots is None:
            self.content[self.key_dotfiles] = {}
            dots = self.content[self.key_dotfiles]
        if self.content[self.key_dotfiles] and dotfile.key in dots:
            self.log.err('\"%s\" entry already exists in dotfiles' %
                         (dotfile.key))
            return False
        home = os.path.expanduser('~')
        dotfile.dst = dotfile.dst.replace(home, '~')
        dots[dotfile.key] = {
            self.key_dotfiles_dst: dotfile.dst,
            self.key_dotfiles_src: dotfile.src
        }
        profiles = self.profiles
        if profile in profiles and profiles[profile] != [self.key_all]:
            if self.content[self.key_profiles][profile] is None:
                self.content[self.key_profiles][profile] = []
            self.content[self.key_profiles][profile].append(dotfile.key)
        elif profile not in profiles:
            if self.content[self.key_profiles] is None:
                self.content[self.key_profiles] = {}
            self.content[self.key_profiles][profile] = [dotfile.key]
        self.profiles = self.content[self.key_profiles]

    def get_dotfiles(self, profile):
        """ returns a list of dotfiles for a specific profile """
        if profile not in self.prodots:
            return []
        tmp = sorted(self.prodots[profile], key=lambda x: x.key, reverse=True)
        return tmp

    def get_profiles(self):
        """ returns all defined profiles """
        return self.profiles.keys()

    def get_configs(self):
        """ returns all defined configs """
        return self.configs.copy()

    def dump(self):
        """ dump config file """
        return yaml.dump(self.content, default_flow_style=False, indent=2)

    def save(self):
        """ save config file to path """
        with open(self.cfgpath, 'w') as f:
            ret = yaml.dump(self.content, f,
                            default_flow_style=False, indent=2)
        return ret
