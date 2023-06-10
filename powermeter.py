#this is a helper file for the usage of a Thorlabs PM100 power meter to read laser power
import pyvisa
from ThorlabsPM100 import ThorlabsPM100

rm = pyvisa.ResourceManager()
inst = rm.open_resource('USB0::0x1313::0x8078::P0035649::INSTR', timeout=1)
power_meter = ThorlabsPM100(inst=inst)

def getPowerReading():
    y = power_meter.read
    return y