# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in frappe_nextcloud/__init__.py
from frappe_nextcloud import __version__ as version

setup(
	name='frappe_nextcloud',
	version=version,
	description='Frappe & ERPNext Integrations: CardDav',
	author='Agile Shift',
	author_email='contacto@gruporeal.org',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
