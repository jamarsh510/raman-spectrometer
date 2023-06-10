#this gui uses movement commands and user input to move the stage on a raman microscope using a PI stage controller
import sys
import PySimpleGUI as sg
from movement import moveStage, connectToDevice, moveToOrigin

__signature__ = 0xdd4ba763b303c0f7562b08fd884ca11e

sg.theme('DarkAmber')
cpt = 0
bdrt = 0
stepsize = 1
sys.tracebacklimit = 0

user_input = [
    [sg.Text('Enter COM Port: ')],
    [sg.Input(key = 'cpt-input')],
    [sg.Text('Enter Baud Rate: ')],
    [sg.Input(key = 'bdrt-input')],
    [sg.Submit('Connect')],
    [sg.Text('Enter Movement Distance (um): ')],
    [sg.Input(key = 'step-size')],
    [sg.Submit()]
]

status = [
    [sg.Text('Current COM Port: '), sg.Text(size = (50, 1), key = 'cpt-output')],
    [sg.Text('Current Baud Rate: '), sg.Text(size = (50, 1), key = 'bdrt-output')],
    [sg.Text('Current Step Size (um): '), sg.Text(size = (50, 1), key = 'step-output')],
    [sg.Text('Current X Position: '), sg.Text(size = (50, 1), key = 'x-output')],  
    [sg.Text('Current Y Position: '), sg.Text(size = (50, 1), key = 'y-output')],
    [sg.Text('Current Z Position: '), sg.Text(size = (50, 1), key = 'z-output')]
]

stage_control = [
    [sg.Button('Left'), sg.Button('Up'), sg.Button('Down'), sg.Button('Right')],
    [sg.Button('Focus Up'), sg.Button('Focus Down')]
]

recenter = [
    [sg.Button('Recenter')]
]

layout = [
    [sg.Column(user_input, element_justification='c')],
    [sg.Column(status, element_justification='c')],
    [sg.Column(stage_control, element_justification='c')],
    [sg.Column(recenter, element_justification='c')]
]

def startStageControl(windowVar, cpt, bdrt, pstns):
    windowVar['cpt-output'].update(cpt)
    windowVar['bdrt-output'].update(bdrt)
    connectToDevice(cpt, bdrt)
    updatePositions(windowVar, pstns)

def updatePositions(windowVar, positions):
    windowVar['x-output'].update(positions[0])
    windowVar['y-output'].update(positions[1])
    windowVar['z-output'].update(positions[2])


window = sg.Window('Controller', layout, resizable=True)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == 'Recenter':
        moveToOrigin(positions, 1)
        updatePositions(window, positions)
    
    if event == 'Connect':
        positions = [35.5, 40.7, 39.8]
        if values['cpt-input']:
            cpt = values['cpt-input']
        else:
            cpt = cpt
        if values['bdrt-input']:
            bdrt = values['bdrt-input']
        else:
            bdrt = bdrt
        startStageControl(window, cpt, bdrt, positions)
        

    if event == 'Submit':
        if values['step-size']:
            stepsize = float(values['step-size'])
        else:
            stepsize = 0
        window['step-output'].update(stepsize)
    
    if event == 'Left':
        moveStage('A', positions, (-1 * stepsize))
        window['x-output'].update(positions[0])
    
    if event == 'Right':
        moveStage('A', positions, stepsize)
        window['x-output'].update(positions[0])
    
    if event == 'Up':
        moveStage('B', positions, stepsize)
        window['y-output'].update(positions[1])
    
    if event == 'Down':
        moveStage('B', positions, (-1 * stepsize))
        window['y-output'].update(positions[1])
    
    if event == 'Focus Up':
        moveStage('C', positions, (-1 * stepsize))
        window['z-output'].update(positions[2])

    if event == 'Focus Down':
        moveStage('C', positions, stepsize)
        window['z-output'].update(positions[2])