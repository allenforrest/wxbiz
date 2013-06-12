"""EIPC Device classes for running in background threads or processes."""


#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

from eipc.kernel.device import device
from eipc.devices import basedevice, monitoredqueue, monitoredqueuedevice

from eipc.devices.basedevice import *
from eipc.devices.monitoredqueue import *
from eipc.devices.monitoredqueuedevice import *

__all__ = ['device']
for submod in (basedevice, monitoredqueue, monitoredqueuedevice):
    __all__.extend(submod.__all__)
