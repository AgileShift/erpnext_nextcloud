from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in frappe_nextcloud/__init__.py
from erpnext_nextcloud import __version__ as version

setup(
	name='erpnext_nextcloud',
	version=version,
	description='Frappe & ERPNext Integrations with NextCloud Contacts',
	author='Agile Shift',
	author_email='contacto@gruporeal.org',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
