"""Registry utilities for RoB domains.

This module centralizes domain discovery and metadata so callers can consume
questions and navigation/evaluation hooks without importing individual modules.
Currently it registers the refactored Domain 1 implementation as an example.
"""

from importlib import import_module
from typing import Dict

from .common import BaseDomain, DomainSpec

# Map domain key -> dotted path to a BaseDomain subclass
DOMAIN_CLASSES = {
    "domain_1_randomization": "rob2.domain_1_randomization:Domain1",
    "domain_2_assigment": "rob2.domain_2_assigment:Domain2Assignment",
    "domain_2_adhering": "rob2.domain_2_adhering:Domain2Adhering",
    "domain_3_missing_data": "rob2.domain_3_missing_data:Domain3MissingData",
    "domain_4_measurement": "rob2.domain_4_measurement:Domain4Measurement",
    "domain_5_reporting": "rob2.domain_5_reporting:Domain5Reporting",
}


def _load_domain(path: str) -> BaseDomain:
    module_path, class_name = path.split(":")
    module = import_module(module_path)
    domain_cls = getattr(module, class_name)
    return domain_cls()


def get_domain_specs() -> Dict[str, DomainSpec]:
    """Instantiate and return all registered domain specs."""
    specs: Dict[str, DomainSpec] = {}
    for key, path in DOMAIN_CLASSES.items():
        domain = _load_domain(path)
        if not isinstance(domain, BaseDomain):
            raise TypeError(f"{path} does not implement BaseDomain")
        specs[key] = domain.as_spec()
    return specs
