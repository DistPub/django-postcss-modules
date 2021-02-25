import pathlib
import posixpath

import re

import os
from py_mini_racer import py_mini_racer
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured


def get_options():
    default = {
        'polyfill': 'postcss-modules-v8-polyfill.js',
        'transpiler': 'npm/postcss-modules-standalone@1.0.1/index.bundle.min.js',
        'setup': 'postcss-modules-setup.js',
        'extensions': ['.cssm'],
        'mimetypes': {
            '.cssm': 'text/css'
        },
        'max_time': 3
    }

    if hasattr(settings, 'POSTCSS_MODULES'):
        default.update(settings.POSTCSS_MODULES)

    def validate_config(name):
        path = get_absolute_path(default[name])
        if not path:
            raise ImproperlyConfigured(f'POSTCSS_MODULES.{name}')

    validate_config('polyfill')
    validate_config('transpiler')
    validate_config('setup')

    mimetype_keys = list(default['mimetypes'].keys())
    for item in default['extensions']:
        if item not in mimetype_keys:
            raise ImproperlyConfigured(f'POSTCSS_MODULES.mimetypes missing extension: {item}')

    return default


def get_absolute_path(path):
    normalized_path = posixpath.normpath(path).lstrip('/')
    if not settings.DEBUG:
        file = os.path.join(settings.STATIC_ROOT, normalized_path)
        if os.path.isfile(file):
            return file
    return finders.find(normalized_path)


def get_file_content(path):
    file = open(path)
    code = file.read()
    file.close()
    return code


def get_transpiler(options):
    ctx = py_mini_racer.MiniRacer()
    ctx.eval(get_file_content(get_absolute_path(options['polyfill'])))
    ctx.eval(get_file_content(get_absolute_path(options['transpiler'])))
    ctx.eval(get_file_content(get_absolute_path(options['setup'])))
    return ctx


def get_composes(dir_path, source):
    composes = set(re.findall('.+from\s+[\'\"](.+)[\'\"];', source))
    return [str(pathlib.Path(dir_path, depend).resolve()) for depend in composes]
