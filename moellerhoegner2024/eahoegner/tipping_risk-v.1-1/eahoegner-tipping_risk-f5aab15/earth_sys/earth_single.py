# Add modules directory to path
import sys

sys.path.append('')

# global imports
import numpy as np
# private imports from sys.path
from core.coupling import linear_coupling
from core.tipping_element import cusp
from core.tipping_network import tipping_network
from earth_sys.functions_earth_system_no_enso import global_functions

"""
Here the Earth system network is defined after Kriegler et al., 2009
"""


class earth_system():
    def __init__(self, gis_time, thc_time, wais_time, nino_time, amaz_time, limits_gis, limits_thc, limits_wais, limits_nino, limits_amaz,
                  pf_wais_to_gis, pf_thc_to_gis, pf_gis_to_thc, pf_nino_to_thc, pf_wais_to_thc, pf_gis_to_wais, pf_thc_to_wais, pf_nino_to_wais,
                   pf_thc_to_nino, pf_amaz_to_nino, pf_nino_to_amaz, pf_thc_to_amaz):
        #timescales
        self._gis_time = gis_time
        self._thc_time = thc_time
        self._wais_time = wais_time
        self._nino_time = nino_time
        self._amaz_time = amaz_time

        #tipping limits
        self._limits_gis = limits_gis
        self._limits_thc = limits_thc
        self._limits_wais = limits_wais
        self._limits_nino = limits_nino
        self._limits_amaz = limits_amaz

        #probability fractions
        self._pf_wais_to_gis = pf_wais_to_gis
        self._pf_thc_to_gis = pf_thc_to_gis
        self._pf_gis_to_thc = pf_gis_to_thc
        self._pf_nino_to_thc = pf_nino_to_thc
        self._pf_wais_to_thc = pf_wais_to_thc
        self._pf_gis_to_wais = pf_gis_to_wais
        self._pf_thc_to_wais = pf_thc_to_wais
        self._pf_thc_to_amaz = pf_thc_to_amaz

    """
    you must provide this method with a global mean temperature, a coupling strength and
    an integer (-1, 0, +1) for the network type that you want to invoke, i.e. kk0, kk1 and kk2 must be -1, 0 or +1
    """
    def earth_network(self, effective_GMT, strength, kk0, kk1, kk2):
        gis = cusp(a=-1 / self._gis_time, b=1 / self._gis_time, c=(1 / self._gis_time) * global_functions.CUSPc(0., self._limits_gis, effective_GMT))
        thc = cusp(a=-1 / self._thc_time, b=1 / self._thc_time, c=(1 / self._thc_time) * global_functions.CUSPc(0., self._limits_thc, effective_GMT))
        wais = cusp(a=-1 / self._wais_time, b=1 / self._wais_time, c=(1 / self._wais_time) * global_functions.CUSPc(0., self._limits_wais, effective_GMT))
        amaz = cusp(a=-1 / self._amaz_time, b=1 / self._amaz_time, c=(1 / self._amaz_time) * global_functions.CUSPc(0., self._limits_amaz, effective_GMT))

        # set up network
        net = tipping_network()
        net.add_element(gis)
        net.add_element(thc)
        net.add_element(wais)
        net.add_element(amaz)


        ######################################Set edges to active state#####################################
        """
        net.add_coupling(1, 0, linear_coupling(strength=-(1 / self._gis_time) * strength * self._pf_thc_to_gis, x_0=-1))
        net.add_coupling(2, 0, linear_coupling(strength=(1 / self._gis_time) * strength * self._pf_wais_to_gis, x_0=-1))

        net.add_coupling(0, 1, linear_coupling(strength=(1 / self._thc_time) * strength * self._pf_gis_to_thc, x_0=-1))
        net.add_coupling(2, 1, linear_coupling(strength=(1 / self._thc_time) * strength * self._pf_wais_to_thc * kk0, x_0=-1))

        net.add_coupling(0, 2, linear_coupling(strength=(1 / self._wais_time) * strength * self._pf_gis_to_wais, x_0=-1))
        net.add_coupling(1, 2, linear_coupling(strength=(1 / self._wais_time) * strength * self._pf_thc_to_wais, x_0=-1))

        net.add_coupling(1, 3, linear_coupling(strength=(1 / self._amaz_time) * strength * self._pf_thc_to_amaz * kk2, x_0=-1))
        """
        return net
