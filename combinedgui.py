#this is a gui used to take area scans of a sample using a raman microscope
from ramangui import drawChart, quickUpdate, updateChart
from movement import moveStage, moveToOrigin
from controllergui import updatePositions, startStageControl
import PySimpleGUI as sg
from powermeter import getPowerReading

useritime = 300000
usernum = 1
username = "myspectra"
stepsizes = [1, 1, 1]
scansizes = [0, 0]

_VARS2 = {'window': False,
         'fig_agg': False,
         'pltFig': False}

AppFont = 'Any 16'
sg.theme('LightBlue1')

user_input = [
        [sg.Text('Set Integration Time:')],
        [sg.Input(key = 'int-time')],
        [sg.Text('Set Number of Integrations: ')],
        [sg.Input(key = 'int-amount')],
        [sg.Text('Set Output File Name (no spaces, include root path if you want it saved outside the source folder): ')],
        [sg.Input(key = 'file-name')],
        [sg.Text('Enter X-Axis Movement Distance (um): ')],
        [sg.Input(key = 'step-size-x')],
        [sg.Text('Enter Y-Axis Movement Distance (um): ')],
        [sg.Input(key = 'step-size-y')],
        [sg.Text('Enter Z-Axis Movement Distance (um): ')],
        [sg.Input(key = 'step-size-z')],
        [sg.Text('Enter X-Axis Scan Size (columns): ')],
        [sg.Input(key = 'scan-size-x')],
        [sg.Text('Enter Y-Axis Scan Size (rows): ')],
        [sg.Input(key = 'scan-size-y')],
        [sg.Submit()],
        [sg.Text('Enter COM Port: ')],
        [sg.Input(key = 'cpt-input')],
        [sg.Text('Enter Baud Rate: ')],
        [sg.Input(key = 'bdrt-input')],
        [sg.Submit('Connect')]  
]

graph = [
        [sg.Button('Collect Single Spectra')],
        [sg.Button('Collect Spectra')],
        [sg.Canvas(key='figCanvas')]
]

status = [
        [sg.Text('Current Integration Time: '), sg.Text(size = (50, 1), key = 'int-time-output')],
        [sg.Text('Current Number of Integrations: '), sg.Text(size = (50, 1), key = 'int-num-output')],
        [sg.Text('Current File Name: '), sg.Text(size = (50, 1), key = 'file-output')],
        [sg.Text('Current Power Reading: '), sg.Text(size = (50, 1), key = 'power-output')],
        [sg.Text('Current COM Port: '), sg.Text(size = (50, 1), key = 'cpt-output')],
        [sg.Text('Current Baud Rate: '), sg.Text(size = (50, 1), key = 'bdrt-output')],
        [sg.Text('Current X-Axis Step Size (um): '), sg.Text(size = (50, 1), key = 'step-output-x')],
        [sg.Text('Current Y-Axis Step Size (um): '), sg.Text(size = (50, 1), key = 'step-output-y')],
        [sg.Text('Current Z-Axis Step Size (um): '), sg.Text(size = (50, 1), key = 'step-output-z')],
        [sg.Text('Current X-Axis Scan Size (columns): '), sg.Text(size = (50, 1), key = 'scan-output-x')],
        [sg.Text('Current Y-Axis Scan Size (rows): '), sg.Text(size = (50, 1), key = 'scan-output-y')],
        [sg.Text('Current X Position: '), sg.Text(size = (50, 1), key = 'x-output')],  
        [sg.Text('Current Y Position: '), sg.Text(size = (50, 1), key = 'y-output')],
        [sg.Text('Current Z Position: '), sg.Text(size = (50, 1), key = 'z-output')]      
]

stage_control = [
    [sg.Button('Start Scan')],
    [sg.Button('Focus Up'), sg.Button('Focus Down')]
]

recenter = [
    [sg.Button('Recenter')]
]

layout = [
        [sg.Column(user_input, element_justification='c'), sg.Column(status, element_justification='c'), sg.Column(graph, element_justification='c')],
        [sg.Column(stage_control, element_justification='c'), sg.Column(recenter, element_justification='c')]
]

def rasterMovement():
    for y in range(0, scansizes[1]):
        for x in range(0, scansizes[0]):
            updateChart(_VARS2['window'], 200000, username, usernum, x, y)
            updateChart(_VARS2['window'], useritime, username, usernum, x, y)
            moveStage('A', positions, stepsizes[0])
        if y != scansizes[1]:
            for x in range(0, scansizes[0]):
                moveStage('A', positions, (-1 * stepsizes[0]))
        if y != scansizes[1]:
            moveStage('B', positions, stepsizes[1])

_VARS2['window'] = sg.Window('Raman Spectrometer GUI', layout, finalize=True)

drawChart(_VARS2['window'])

while True:
    event, values = _VARS2['window'].read(timeout=200)
    _VARS2['window']['int-time-output'].update(useritime)
    _VARS2['window']['int-num-output'].update(usernum)
    _VARS2['window']['file-output'].update(username)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Collect Single Spectra':
        quickUpdate(_VARS2['window'], useritime)
        power_inst = getPowerReading()
        _VARS2['window']['power-output'].update(power_inst)

    if event == 'Collect Spectra':
        updateChart(_VARS2['window'], useritime, username, usernum)
        power_inst = getPowerReading()
        _VARS2['window']['power-output'].update(power_inst)

    if event == 'Submit':
        if values['int-time']:
            useritime = values['int-time']
        else:
            useritime = useritime
        if values['int-amount']:
            usernum = values['int-amount']
        else:
            usernum = usernum
        if values['file-name']:
            username = values['file-name']
        else:
            username = username
        if values['step-size-x']:
            stepsizes[0] = int(values['step-size-x'])
        else:
            stepsizes[0] = 0
        if values['step-size-y']:
            stepsizes[1] = int(values['step-size-y'])
        else:
            stepsizes[1] = 0
        if values['step-size-z']:
            stepsizes[2] = int(values['step-size-z'])
        else:
            stepsizes[2] = 0
        if values['scan-size-x']:
            scansizes[0] = int(values['scan-size-x'])
        else:
            scansizes[0] = 0
        if values['scan-size-y']:
            scansizes[1] = int(values['scan-size-y'])
        else:
            scansizes[1] = 0
        _VARS2['window']['step-output-x'].update(stepsizes[0])
        _VARS2['window']['step-output-y'].update(stepsizes[1])
        _VARS2['window']['step-output-z'].update(stepsizes[2])
        _VARS2['window']['scan-output-x'].update(scansizes[0])
        _VARS2['window']['scan-output-y'].update(scansizes[1])
        _VARS2['window']['int-time-output'].update(useritime)
        _VARS2['window']['int-num-output'].update(usernum)
        _VARS2['window']['file-output'].update(username)

    if event == 'Recenter':
        moveToOrigin(positions, 1)
        updatePositions(_VARS2['window'], positions)
    
    if event == 'Connect':
        positions = [56.0, 26.3, 49.6]
        if values['cpt-input']:
            cpt = values['cpt-input']
        else:
            cpt = cpt
        if values['bdrt-input']:
            bdrt = values['bdrt-input']
        cpt = values['cpt-input']
        bdrt = values['bdrt-input']
        startStageControl(_VARS2['window'], cpt, bdrt, positions)

    if event == 'Start Scan':
        rasterMovement()
        updatePositions(_VARS2['window'], positions)
        moveToOrigin(positions, 1)
    
    if event == 'Focus Up':
        moveStage('C', positions, (-1 * stepsizes[2]))
        _VARS2['z-output'].update(positions[2])

    if event == 'Focus Down':
        moveStage('C', positions, stepsizes[2])
        _VARS2['z-output'].update(positions[2])

_VARS2['window'].close()