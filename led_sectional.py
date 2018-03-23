from __future__ import division
import urllib3
import xml.etree.ElementTree as ET
from matplotlib import cm
from matplotlib import colors
import pandas as pd
import numpy as np
from time import sleep
from neopixel import *

dataUse = 'flight_category'
colorMap = cm.jet
colorMap = colors.LinearSegmentedColormap.from_list('', ['purple','blue','green','yellow','orange','red','deeppink'])
colorMapStat = cm.RdYlGn_r
colorMapStat = colors.LinearSegmentedColormap.from_list('', ['green','yellow','red'])
refreshinterval = 100
updatesteps = 600
led = True
ledVerbose = False

# LED strip configuration:
LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 100     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_RGB   # Strip type and colour ordering

normal = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=3&mostRecentForEachStation=true&stationString='
props = {}
props['columns'] = ['station_id','latitude','longitude','temp_c','dewpoint_c',
                    'wind_dir_degrees','wind_speed_kt','visibility_statute_mi',
                    'altim_in_hg','flight_category','elevation_m','wx_string',
                    'precip_in','sky_condition','observation_time']
props['station_id'] = {}
props['latitude'] = {}
props['latitude']['min'] = 24
props['latitude']['max'] = 50
props['longitude'] = {}
props['longitude']['min'] = -124
props['longitude']['max'] = -68
props['temp_c'] = {}
props['temp_c']['min'] = 0
props['temp_c']['max'] = 35
props['dewpoint_c'] = {}
props['dewpoint_c']['min'] = 0
props['dewpoint_c']['max'] = 35
props['wind_dir_degrees'] = {}
props['wind_dir_degrees']['min'] = 0
props['wind_dir_degrees']['max'] = 359
props['wind_speed_kt'] = {}
props['wind_speed_kt']['min'] = 0
props['wind_speed_kt']['max'] = 20
props['visibility_statute_mi'] = {}
props['visibility_statute_mi']['min'] = 0
props['visibility_statute_mi']['max'] = 10
props['altim_in_hg'] = {}
props['altim_in_hg']['min'] = 29
props['altim_in_hg']['max'] = 30.9
props['flight_category'] = {}
props['flight_category']['VFR'] = [0,255,0]
props['flight_category']['MVFR'] = [0,0,255]
props['flight_category']['IFR'] = [255,0,0]
props['flight_category']['LIFR'] = [255,127.5,255]
props['elevation_m'] = {}
props['elevation_m']['min'] = -20
props['elevation_m']['max'] = 4000
props['wx_string'] = {}
props['precip_in'] = {}
props['precip_in']['min'] = 0
props['precip_in']['max'] = 10
props['sky_condition'] = {}
props['observation_time'] = {}
props['temp_f'] = {}
props['temp_f']['min'] = -20
props['temp_f']['max'] = 120
props['elevation_ft'] = {}
props['elevation_ft']['min'] = -60
props['elevation_ft']['max'] = 12000
props['cloudbase_msl'] = {}
props['cloudbase_msl']['min'] = 0
props['cloudbase_msl']['max'] = 12000
props['cloudbase_agl'] = {}
props['cloudbase_agl']['min'] = 0
props['cloudbase_agl']['max'] = 12000

metars = {}
metars['led'] = {}
metars['led']['KSBA'] = 1
metars['led']['KCMA'] = 2
metars['led']['KNTD'] = 3
metars['led']['KVNY'] = 4
metars['led']['KBUR'] = 5
metars['led']['KBFL'] = 6
metars['led']['KNID'] = 7
metars['led']['KDAG'] = 8
metars['led']['KWJF'] = 9
metars['led']['KPMD'] = 10
metars['led']['KEDW'] = 11
metars['led']['KMHV'] = 12
metars['led']['KLAX'] = 13
metars['led']['KHHR'] = 14
metars['led']['KLGB'] = 15
metars['led']['KSLI'] = 16
metars['led']['KSNA'] = 17
metars['led']['KONT'] = 18
metars['led']['KRAL'] = 19
metars['led']['KRIV'] = 20
metars['led']['KSBD'] = 21
metars['led']['KL35'] = 22
metars['led']['KPSP'] = 23
metars['led']['KNFG'] = 24
metars['led']['KCRQ'] = 25
metars['led']['KMYF'] = 26
metars['led']['KSAN'] = 27
metars['led']['KNZY'] = 28
metars['led']['KAVX'] = 29
metars['led']['KPTV'] = 30
metars['led']['KSAC'] = 31
metars['led']['KSFO'] = 32
metars['led']['KOAK'] = 33
metars['led']['KHJO'] = 34
metars['led']['KNLC'] = 35
metars['led']['KSBP'] = 36
metars['led']['KSMX'] = 37
metars['led']['KFAT'] = 38
metars['led']['KVBG'] = 39
metars['led']['KBIH'] = 40
metars['led']['KMCE'] = 41
metars['led']['KSJC'] = 42
metars['led']['KSNS'] = 43
metars['led']['KPRB'] = 44
metars['led']['KMER'] = 45
metars['led']['KWVI'] = 46
metars['led']['KMRY'] = 47
metars['led']['KMAE'] = 48
metars['led']['KIZA'] = 49
metars['led']['KOXR'] = 50
metars['led']['KSDB'] = 51
metars['led']['KDLO'] = 52
metars['led']['KVIS'] = 53
metars['led']['KMOD'] = 54
metars['led']['KCVH'] = 55
metars['led']['KE16'] = 56
metars['led']['KRHV'] = 57
metars['led']['KLVK'] = 58
metars['led']['KC83'] = 59
metars['led']['KHWD'] = 60
metars['led']['KPAO'] = 61
metars['led']['KSQL'] = 62
metars['led']['KHAF'] = 63
metars['led']['KNUQ'] = 64
metars['led']['KCCR'] = 65
metars['led']['KSCK'] = 66
metars['led']['KMMH'] = 67
metars['led']['KL18'] = 68
metars['led']['KF70'] = 69
metars['led']['KOKB'] = 70
metars['led']['KRNM'] = 71
metars['led']['KNKX'] = 72
metars['led']['KSEE'] = 73
metars['led']['KSDM'] = 74
metars['led']['KNRS'] = 75
metars['led']['KCZZ'] = 76
metars['led']['KIPL'] = 77
metars['led']['KTRM'] = 78
metars['led']['KNXP'] = 79
metars['led']['KTSP'] = 80
metars['led']['KDFW'] = 81
metars['led']['KMIA'] = 82
metars['led']['KMDW'] = 83
metars['led']['KDEN'] = 84
metars['led']['KDAL'] = 85
metars['led']['KSEA'] = 86
metars['led']['KSAF'] = 87
metars['led']['KLAS'] = 88
metars['led']['KAUS'] = 89
metars['led']['KIAH'] = 90
metars['led']['KSAT'] = 91
metars['led']['KMSY'] = 92
metars['led']['KJFK'] = 93
metars['led']['KMKE'] = 94
metars['led']['KJAC'] = 95
metars['led']['KPHX'] = 96
metars['led']['KSLC'] = 97
metars['led']['KBNA'] = 98
metars['led']['KDEN'] = 99

def animate(strip, i, stat):
    try:
        if stat == 1:
            url = buildUrl(normal)
            content = fetchMetars(url)
            processMetars(content)
        if led: ledMetars(strip, df, stat, i)
    except:
        pass

def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos  * 3, 0)
    elif pos < 170:
       pos -= 85
       return Color(255 - pos * 3, 0, pos * 3)
    else:
       pos -= 170
       return Color(0, pos * 3, 255 - pos * 3)

def rainbowCycle(strip):
    for j in range(256 * 2):
       for i in range(strip.numPixels()):
           strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
       strip.show()
       sleep(1/1000)

def buildUrl(url):
    for stationId in metars['led'].keys():
        url = url + stationId + ','
    return url

def fetchMetars(url):
    http = urllib3.PoolManager()
    content = http.request('GET', url).data
    return content

def processMetars(content):
    global df
    metars['FEW'] = {}
    metars['BKN'] = {}
    metars['OVC'] = {}
    for col in props['columns']:
        if col != 'sky_condition':
            metars[col] = {}
            for metar in ET.fromstring(content).iter('METAR'):
                stationId = metar.find('station_id').text
                try:
                    metars[col][stationId] = float(metar.find(col).text)
                except:
                    try:
                        metars[col][stationId] = metar.find(col).text
                    except:
                        pass
    for metar in ET.fromstring(content).iter('METAR'):
        stationId = metar.find('station_id').text
        for sky_condition in metar.iter('sky_condition'):
            cover = sky_condition.items()[0][1]
            try:
                metars[cover][stationId] = sky_condition.items()[1][1]
            except:
                pass
    df = pd.DataFrame.from_dict(metars, orient='columns')
    df['temp_f'] = (1.8 * df['temp_c']) + 32
    df['elevation_ft'] = df['elevation_m'] * 3.28084
    df['cloudbase_msl'] = (df['temp_c'] - df['dewpoint_c']) * (1800 / 4.4)
    df['cloudbase_agl'] = df['cloudbase_msl'] - df['elevation_ft']
    if dataUse == 'flight_category':
        for cat in props['flight_category'].keys():
            df.ix[df['flight_category'] == cat, 'R'] = props['flight_category'][cat][0] / 255
            df.ix[df['flight_category'] == cat, 'G'] = props['flight_category'][cat][1] / 255
            df.ix[df['flight_category'] == cat, 'B'] = props['flight_category'][cat][2] / 255
        df['clr'] = df.apply(lambda row: [row['R'], row['G'], row['B']], axis=1)
        df['clr255'] = df.apply(lambda row: [row['R'] * 255, row['G'] * 255, row['B'] * 255], axis=1)
    else:
        df['R'] = (df[dataUse] - props[dataUse]['min'])/(props[dataUse]['max'] - props[dataUse]['min'])
        df['G'] = (df[dataUse] - props[dataUse]['min'])/(props[dataUse]['max'] - props[dataUse]['min'])
        df['B'] = (df[dataUse] - props[dataUse]['min'])/(props[dataUse]['max'] - props[dataUse]['min'])
        df['clr'] = (df[dataUse] - props[dataUse]['min'])/(props[dataUse]['max'] - props[dataUse]['min'])
        df['clr255'] = (df[dataUse] - props[dataUse]['min'])/(props[dataUse]['max'] - props[dataUse]['min'])
        df['R'] = df['R'].apply(lambda x: colorMap(x)[0])
        df['G'] = df['G'].apply(lambda x: colorMap(x)[1])
        df['B'] = df['B'].apply(lambda x: colorMap(x)[2])
        df['clr'] = df['clr'].apply(lambda x: [colorMap(x)[0], colorMap(x)[1], colorMap(x)[2]])
        df['clr255'] = df['clr255'].apply(lambda x: tuple([int(colorMap(x)[0] * 255), int(colorMap(x)[1] * 255), int(colorMap(x)[2] * 255)]))
    #df.ix[~(df['R'] > -1), 'R'] = 0
    #df.ix[~(df['G'] > -1), 'G'] = 0
    #df.ix[~(df['B'] > -1), 'B'] = 0
    #df.ix[~(df['R'] > -1), 'clr'] = [0.0, 0.0, 0.0]
    #df.ix[~(df['R'] > -1), 'clr255'] = [0.0, 0.0, 0.0]
    df = df.set_index('led')
    df.sort_index(inplace=True)

def ledMetars(strip, df, stat, i):
    strip.setPixelColorRGB(0, int(cm.RdYlGn_r(stat)[0] * 255), int(colorMapStat(stat)[1] * 255), int(colorMapStat(stat)[2] * 255))
    print('UPDATE: ' + str(i) + ', LED: ' + '0' + ', SID: ' + str(stat) + ', DATA: ' + 'status' + ', COLOR: ' + str([int(colorMapStat(stat)[1] * 255),int(colorMapStat(stat)[0] * 255),int(colorMapStat(stat)[2] * 255)]))
    if stat == float(1):
        for led in df.index:
            r = df['R'][led]
            g = df['G'][led]
            b = df['B'][led]
            station = df['station_id'][led]
            data = df[dataUse][led]
            try:
                strip.setPixelColorRGB(int(led), int(r * 255), int(g * 255), int(b * 255))
            except:
                strip.setPixelColorRGB(int(led), 0, 0, 0)
            print('UPDATE: ' + str(i) + ', LED: ' + str(led) + ', SID: ' + str(station) + ', DATA: ' + str(data) + ', COLOR: ['+str(r * 255)+','+str(g * 255)+','+str(b * 255)+']')
    strip.show()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

rainbowCycle(strip)
i = 0
stat = float(1)
while 1 > 0:
    try:
        animate(strip, i, stat)
    except:
        pass
    i = i + 1
    stat = 1 - (float(np.ceil(i/updatesteps)) - float((i/updatesteps)))
    sleep(refreshinterval/1000)
    if i >= 6000:
         i = 0
