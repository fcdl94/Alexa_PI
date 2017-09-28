from __future__ import unicode_literals

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import logging
import re
import time

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from collections import OrderedDict
from contextlib import closing

import requests

try:
    import io as StringIO
except ImportError:
    try:
        import cStringIO as StringIO
    except ImportError:
        import StringIO as StringIO

try:
    import xml.etree.cElementTree as elementtree
except ImportError:
    import xml.etree.ElementTree as elementtree

logger = logging.getLogger(__name__)


class PlaylistError(Exception):
    pass


class Cache(object):
    # TODO: merge this to util library (copied from mopidy-spotify)

    def __init__(self, ctl=0, ttl=3600):
        self.cache = {}
        self.ctl = ctl
        self.ttl = ttl
        self._call_count = 0

    def __call__(self, func):
        def _memoized(*args):
            now = time.time()
            try:
                value, last_update = self.cache[args]
                age = now - last_update
                if self._call_count > self.ctl or age > self.ttl:
                    self._call_count = 0
                    raise AttributeError
                if self.ctl:
                    self._call_count += 1
                return value

            except (KeyError, AttributeError):
                value = func(*args)
                if value:
                    self.cache[args] = (value, now)
                return value

            except TypeError:
                return func(*args)

        def clear():
            self.cache.clear()

        _memoized.clear = clear
        return _memoized


def parse_m3u(data):
    # Copied from mopidy.audio.playlists
    # Mopidy version expects a header but it's not always present
    for line in data.readlines():
        if not line.startswith('#') and line.strip():
            yield line.strip()


def parse_pls(data):
    # Copied from mopidy.audio.playlists
    try:
        cp = configparser.RawConfigParser()
        cp.readfp(data)
    except configparser.Error:
        return

    for section in cp.sections():
        if section.lower() != 'playlist':
            continue
        for i in xrange(cp.getint(section, 'numberofentries')):
            try:
                # TODO: Remove this horrible hack to avoid adverts
                if cp.has_option(section, 'length%d' % (i + 1)):
                    if cp.get(section, 'length%d' % (i + 1)) == '-1':
                        yield cp.get(section, 'file%d' % (i + 1))
                else:
                    yield cp.get(section, 'file%d' % (i + 1))
            except configparser.NoOptionError:
                return


def fix_asf_uri(uri):
    return re.sub(r'http://(.+\?mswmext=\.asf)', r'mms://\1', uri, re.I)


def parse_old_asx(data):
    try:
        cp = configparser.RawConfigParser()
        cp.readfp(data)
    except configparser.Error:
        return
    for section in cp.sections():
        if section.lower() != 'reference':
            continue
        for option in cp.options(section):
            if option.lower().startswith('ref'):
                uri = cp.get(section, option).lower()
                yield fix_asf_uri(uri)


def parse_new_asx(data):
    # Copied from mopidy.audio.playlists
    try:
        for _, element in elementtree.iterparse(data):
            element.tag = element.tag.lower()  # normalize
            for ref in element.findall('entry/ref[@href]'):
                yield fix_asf_uri(ref.get('href', '').strip())

            for entry in element.findall('entry[@href]'):
                yield fix_asf_uri(entry.get('href', '').strip())
    except elementtree.ParseError:
        return


def parse_asx(data):
    if 'asx' in data.getvalue()[0:50].lower():
        return parse_new_asx(data)
    else:
        return parse_old_asx(data)


# This is all broken: mopidy/mopidy#225
# from gi.repository import TotemPlParser
# def totem_plparser(uri):
#     results = [