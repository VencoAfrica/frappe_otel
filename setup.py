from setuptools import find_packages, setup

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in frappe_otel/__init__.py
from frappe_otel import __version__ as version

setup(
    name="frappe_otel",
    version=version,
    description="Frappe Framework wrappers for Opentelemetry",
    author="Castlecraft Ecommerce Pvt. Ltd.",
    author_email="support@castlecraft.in",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
)
