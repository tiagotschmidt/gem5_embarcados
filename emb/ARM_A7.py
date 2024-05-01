# -*- coding: utf-8 -*-

import m5
from m5.objects import *

from m5.objects import BaseCache
from m5.objects import MinorCPU
from m5.objects import DDR3_1600_8x8
from m5.objects import System
from m5.objects import SystemXBar
from m5.objects import SystemXBar


class ARM_A7_L1_Cache(Cache):

    size = '32kB'
    assoc = 4
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    def __init__(self, options=None):
        super(ARM_A7_L1_Cache, self).__init__()
        pass

    def connectToICache(self, cpu):
        self.cpu_side = cpu.icache_port

    def connectToDCache(self, cpu):
        self.cpu_side = cpu.dcache_port

    def connectBus(self, bus):
        self.mem_side = bus.slave

class ARM_A7_L2_Cache(Cache):

    size = '1MB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    def __init__(self, options=None):
        super(ARM_A7_L2_Cache, self).__init__()
        pass

    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.master

    def connectMemSideBus(self, bus):
        self.mem_side = bus.slave

class ARM_A7_CPU(MinorCPU):
    decodeInputWidth  = 2
    executeInputWidth = 2

class A7_System(System):

    def __init__(self, options=None):
        super(A7_System, self).__init__()

############################################################
## clk_domain - Mexer somente na frequencia
############################################################
        self.clk_domain = SrcClockDomain()
        self.clk_domain.voltage_domain = VoltageDomain()
        self.clk_domain.clock = '2GHz'

############################################################
## mem_mode e mem_ranges - Não mexer
############################################################
        self.mem_mode = 'timing'
        self.mem_ranges = [AddrRange('512MB')]

############################################################
## Cpu - definida em cpu.py
############################################################
        self.cpu = ARM_A7_CPU()

############################################################
## Caches - definidas em caches.py
############################################################
        self.cpu.icache  = ARM_A7_L1_Cache()
        self.cpu.dcache  = ARM_A7_L1_Cache()
        self.cpu.l2cache = ARM_A7_L2_Cache()

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
        #self.cpu.interrupts[0].pio = self.membus.master
        #self.cpu.interrupts[0].int_master = self.membus.slave
        #self.cpu.interrupts[0].int_slave = self.membus.master

        self.system_port = self.membus.slave

############################################################
## Controlador de memória - conectado à memória principal
## Não mexer?
############################################################
        self.mem_ctrl = DDR3_1600_8x8()
        self.mem_ctrl.range = self.mem_ranges[0]
        self.mem_ctrl.port = self.membus.master
