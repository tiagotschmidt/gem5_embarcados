# -*- coding: utf-8 -*-

import m5
from m5.objects import *

from m5.objects import BaseCache
from m5.objects import DerivO3CPU
from m5.objects import DDR3_1600_8x8
from m5.objects import System
from m5.objects import SystemXBar
from m5.objects import SystemXBar


class ARM_A72_L1I_Cache(Cache):

    size = '48kB'
    assoc = 6
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def __init__(self, options=None):
        super(ARM_A72_L1I_Cache, self).__init__()
        pass

    def connectToICache(self, cpu):
        self.cpu_side = cpu.icache_port

    def connectBus(self, bus):
        self.mem_side = bus.slave
       
class ARM_A72_L1D_Cache(Cache):

    size = '32kB'
    assoc = 4
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def __init__(self, options=None):
        super(ARM_A72_L1D_Cache, self).__init__()
        pass

    def connectToDCache(self, cpu):
        self.cpu_side = cpu.dcache_port

    def connectBus(self, bus):
        self.mem_side = bus.slave       

class ARM_A72_L2_Cache(Cache):

    size = '512kB'
    assoc = 64
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def __init__(self, options=None):
        super(ARM_A72_L2_Cache, self).__init__()
        pass

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.master

    def connectMemSideBus(self, bus):
        self.mem_side = bus.slave

class ARM_A72_CPU(DerivO3CPU):
    fetchWidth = 3
    decodeWidth = 3
    renameWidth = 3
    dispatchWidth = 3
    issueWidth = 3
    wbWidth = 3
    commitWidth = 3
    squashWidth = 4

    cacheStorePorts = 1

    backComSize = 10
    forwardComSize = 10

class ARM72_System(System):

    def __init__(self, options=None):
        super(ARM72_System, self).__init__()

############################################################
## clk_domain - Mexer somente na frequencia
############################################################
        self.clk_domain = SrcClockDomain()
        self.clk_domain.voltage_domain = VoltageDomain()
        self.clk_domain.clock = '2.3GHz'

############################################################
## mem_mode e mem_ranges - Não mexer
############################################################
        self.mem_mode = 'timing'
        self.mem_ranges = [AddrRange('512MB')]

############################################################
## Cpu - definida em cpu.py
############################################################
        self.cpu = ARM_A72_CPU()
 
#//////////////////////////////////////////////////////////////
# CPU 0 = self.cpu

############################################################
## Caches - definidas em caches.py
############################################################
        self.cpu.icache  = ARM_A72_L1I_Cache()
        self.cpu.dcache  = ARM_A72_L1D_Cache()
        self.cpu.l2cache = ARM_A72_L2_Cache()

############################################################
## Define a interconexão entre as caches e memória principal
## Modifique aqui para alterar a hierarquia de memória.
############################################################
        self.l2bus  = SystemXBar()
        self.membus = SystemXBar()

        self.cpu.icache.connectToICache(self.cpu)
        self.cpu.icache.connectBus(self.l2bus)
        self.cpu.dcache.connectToDCache(self.cpu)
        self.cpu.dcache.connectBus(self.l2bus)

        self.cpu.l2cache.connectCPUSideBus(self.l2bus)
        self.cpu.l2cache.connectMemSideBus(self.membus)

############################################################
## Controlador de interrupções - conectado à memória principal
## Não mexer.
############################################################
        self.cpu.createInterruptController()

        self.system_port = self.membus.slave

#//////////////////////////////////////////////////////////////

############################################################
## Controlador de memória - conectado à memória principal
## Não mexer?
############################################################
        self.mem_ctrl = DDR3_1600_8x8()
        self.mem_ctrl.range = self.mem_ranges[0]
        self.mem_ctrl.port = self.membus.master
