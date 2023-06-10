#this is a helper file for commands used to control a PI stage to focus on and examine a sample using the raman microscope
import sys
from pipython import GCSDevice

__signature__ = 0xdd4ba763b303c0f7562b08fd884ca11e
sys.tracebacklimit = 0

pidevice = GCSDevice()

def connectToDevice(cpt, bdrt):
    pidevice.ConnectRS232(comport = cpt, baudrate = bdrt)

def moveToOrigin(positions, numSteps):
    while positions[0] != 20:
        moveStage('A', positions, (-1 * numSteps))
    while positions[1] != 25:
        moveStage('B', positions, (-1 * numSteps))
    while positions[2] != 20:
        moveStage('C', positions, (-1 * numSteps))
    
    return positions

def moveStage(axis, positions, numSteps):

    newPosition = 0

    pidevice.SVO(axis, 1)
    if axis == 'A':
        newPosition = positions[0] + numSteps
        axisMoved = 'A'
    if axis == 'B':
        newPosition = positions[1] + numSteps
        axisMoved = 'B'
    if axis == 'C':
        newPosition = positions[2] + numSteps
        axisMoved = 'C'

    if newPosition < 0:
        newPosition = 0

    if newPosition > 100:
        newPosition = 100
    

    pidevice.MOV(axis, newPosition)
    pidevice.SVO(axis, 0)

    if axisMoved == 'A':
        positions[0] = newPosition
    if axisMoved == 'B':
        positions[1] = newPosition
    if axisMoved == 'C':
        positions[2] = newPosition

    return positions