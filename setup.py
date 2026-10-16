from setuptools import setup, find_packages
setup(
    name="octopus-settlement-engine",
    version="2.0.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'octopus=regulators_companion_wrapper:inspect_compliance_manifests',
        ],
    },
)
