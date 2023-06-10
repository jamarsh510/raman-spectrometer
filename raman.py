#this is a helper file for functions involving raman spectra collection via an ocean optics spectrometer
import seabreeze
seabreeze.use('cseabreeze')
from seabreeze.spectrometers import Spectrometer
import serial
from powermeter import getPowerReading

ser = serial.Serial()

#change this value to match the COM port of your serial cable for usage in "level" triggering
ser.port = 'COM6'
ser.close()
spec = Spectrometer.from_first_available()

def getSingleSpectra():
    xData = spec.wavelengths()
    yData = spec.intensities()

    return(xData, yData)

def getSpectra(itime, username, usernum, xstep, ystep):
    t = itime
    n = username
    s = usernum
    powerlist = []

    spec.integration_time_micros(int(t))
    xData = spec.wavelengths()

    for x in range(0, int(s)):
        counter = 0

        ser.dsrdtr = True
        ser.open()
        rawYData = spec.intensities()
        ser.close()
        if x == 0:
            yData = rawYData
        else:
            for i in yData:
                yData[counter] = yData[counter] + rawYData[counter]
                counter += 1
        power = getPowerReading()
        powerlist.append(power)
    counter2 = 0
    for i in yData:
        i = i/float(s)
        yData[counter2] = i
        counter2 += 1

    if int(t) > 200000:
        storeSpectraData(xData, yData, n, xstep, ystep, powerlist)
    
    return (xData, yData)

def storeSpectraData(w, i, name, xstep, ystep, powerlist):
    wavelengths = w
    intensities = i
    title = f"{name}_{xstep}_{ystep}.txt"
    title2 = f"{name}_power_readings.txt"
    f = open(title, "a")

    f.write("Data stored in pairs of (Wavelength, Intensity): \n")
    for x in range(0, len(wavelengths)):
        string1 = str(wavelengths[x])
        string2 = str(intensities[x])
        f.write(string1 + ", " + string2 + "\n")

    f.write("\n")

    f2 = open(title2, "a")
    for x in powerlist:
        f2.write(f"{x}\n")
    
    return
