#the purpose of this file is for single point raman spectra collection and storage
#if the trigger mode is switched, unplug the spectrometer and replug it in after each scan
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from raman import getSingleSpectra, getSpectra, spec
from powermeter import getPowerReading

#input variables
useritime = 300000
usernum = 1
username = "myspectra"

_VARS = {'window': False,
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
        [sg.Submit()],
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
        [sg.Text('Current Power Reading: '), sg.Text(size = (50, 1), key = 'power-output')]      
]

layout = [
        [sg.Column(user_input, element_justification='c',)],
        [sg.Column(status, element_justification='c')],
        [sg.Column(graph, element_justification='c')]
]

_VARS['window'] = sg.Window('Raman Spectrometer GUI', layout, finalize=True)

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def drawChart(windowVar):
    _VARS['pltFig'] = plt.figure()
    dataXY = getSingleSpectra()
    plt.plot(dataXY[0], dataXY[1], '.k')
    plt.xlabel('Wavelengths')
    plt.ylabel('Intensities')
    _VARS['fig_agg'] = draw_figure(windowVar['figCanvas'].TKCanvas, _VARS['pltFig'])
    power_inst = getPowerReading()
    _VARS['window']['power-output'].update(power_inst)

def quickUpdate(windowVar, useritime):
    _VARS['fig_agg'].get_tk_widget().forget()
    spec.integration_time_micros(int(useritime))
    power_inst = getPowerReading()
    dataXY = getSingleSpectra()
    plt.cla()
    plt.clf()
    plt.plot(dataXY[0], dataXY[1], '.k')
    _VARS['fig_agg'] = draw_figure(windowVar['figCanvas'].TKCanvas, _VARS['pltFig'])
    return power_inst

def updateChart(windowVar, useritime, username, usernum, xstep = 1, ystep = 1):
    _VARS['fig_agg'].get_tk_widget().forget()
    power_inst = getPowerReading()
    dataXY = getSpectra(useritime, username, usernum, xstep, ystep)
    plt.cla()
    plt.clf()
    plt.plot(dataXY[0], dataXY[1], '.k')
    _VARS['fig_agg'] = draw_figure(windowVar['figCanvas'].TKCanvas, _VARS['pltFig'])
    return power_inst

drawChart(_VARS['window'])

while True:
    event, values = _VARS['window'].read(timeout=200)
    _VARS['window']['int-time-output'].update(useritime)
    _VARS['window']['int-num-output'].update(usernum)
    _VARS['window']['file-output'].update(username)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Collect Single Spectra':
        power = quickUpdate(_VARS['window'], useritime)
        _VARS['window']['power-output'].update(power)

    if event == 'Collect Spectra':
        power = updateChart(_VARS['window'], useritime, username, usernum)
        _VARS['window']['power-output'].update(power)

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
        _VARS['window']['int-time-output'].update(useritime)
        _VARS['window']['int-num-output'].update(usernum)
        _VARS['window']['file-output'].update(username)

_VARS['window'].close()