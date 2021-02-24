#!/usr/bin/env bash
python3 setup.py sdist bdist_wheel
rm -rf build
rm -rf django_postcss_modules.egg-info