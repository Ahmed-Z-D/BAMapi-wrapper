from types import MappingProxyType

import BAMapi as bam

def test_get_instruments():
    instruments = bam.INSTRUMENTS

    assert isinstance(instruments, MappingProxyType)
    assert all(isinstance(name, str) for name in instruments.keys())
    assert all(isinstance(acronym, str) for acronym in instruments.values())