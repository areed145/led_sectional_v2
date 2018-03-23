# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/    

from __future__ import division
import urllib3
import xml.etree.ElementTree as ET
from matplotlib import cm
import pandas as pd
import numpy as np
from time import sleep
from neopixel import *

dataUse = 'flight_category'
colorMap = cm.jet
colorMapStat = cm.RdYlGn_r
refreshinterval = 100
updatesteps = 60
led = True
ledVerbose = False

# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

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
props['temp_c']['min'] = -5
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
metars['led']['KNTD'] = 2
metars['led']['KCMA'] = 3
metars['led']['KNTD'] = 4
metars['led']['KVNY'] = 5
metars['led']['KWHP'] = 6
metars['led']['KBUR'] = 7
metars['led']['KBFL'] = 8
metars['led']['KNID'] = 9
metars['led']['KDAG'] = 10
metars['led']['KWJF'] = 11
metars['led']['KPMD'] = 12
metars['led']['KEDW'] = 13
metars['led']['KMHV'] = 14
metars['led']['KLAX'] = 15
metars['led']['KHHR'] = 16
metars['led']['KLGB'] = 17
metars['led']['KSLI'] = 18
metars['led']['KSNA'] = 19
metars['led']['KONT'] = 20
metars['led']['KRAL'] = 21
metars['led']['KRIV'] = 22
metars['led']['KSBD'] = 23
metars['led']['KL35'] = 24
metars['led']['KPSP'] = 25
metars['led']['KNFG'] = 26
metars['led']['KCRQ'] = 27
metars['led']['KMYF'] = 28
metars['led']['KSAN'] = 29
metars['led']['KNZY'] = 30
metars['led']['KAVX'] = 31

metars['led']['KPTV'] = 32
metars['led']['KSAC'] = 33
metars['led']['KSFO'] = 34
metars['led']['KOAK'] = 35
metars['led']['KHAN'] = 36
metars['led']['KNLC'] = 37
metars['led']['KNLC'] = 38
metars['led']['KSBA'] = 39
metars['led']['KFAT'] = 40
metars['led']['KNID'] = 41
metars['led']['KBIH'] = 42
metars['led']['KMCE'] = 43
metars['led']['KSJC'] = 44
metars['led']['KSNS'] = 45
metars['led']['KPRB'] = 46
metars['led']['KMER'] = 47
metars['led']['KWVI'] = 48
metars['led']['KMRY'] = 49
metars['led']['KMAE'] = 50
##metars['led']['KSBP'] = 51
##metars['led']['KSMX'] = 52
##metars['led']['KVBG'] = 53
##metars['led']['KIZA'] = 54
##metars['led']['KOXR'] = 55
##metars['led']['KSDB'] = 56
##metars['led']['KDLO'] = 57
##metars['led']['KVIS'] = 58
##metars['led']['KMOD'] = 59
##metars['led']['KCVH'] = 60
##metars['led']['KE16'] = 61
##metars['led']['KRHV'] = 62
##metars['led']['KLVK'] = 63
##metars['led']['KC83'] = 64
##metars['led']['KHWD'] = 65
##metars['led']['KPAO'] = 66
##metars['led']['KSQL'] = 67
##metars['led']['KHAF'] = 68
##metars['led']['KNUQ'] = 69
##metars['led']['KCCR'] = 70
##metars['led']['KSCK'] = 71
##metars['led']['KMMH'] = 72
##metars['led']['KCRQ'] = 73
##metars['led']['KNFG'] = 74
##metars['led']['KL18'] = 75
##metars['led']['KF70'] = 76
##metars['led']['KOKB'] = 77
##metars['led']['KRNM'] = 78
##metars['led']['KNKX'] = 79
##metars['led']['KMYF'] = 80
##metars['led']['KSEE'] = 81
##metars['led']['KSDM'] = 82
##metars['led']['KNRS'] = 83
##metars['led']['KCZZ'] = 84
##metars['led']['KIPL'] = 85
##metars['led']['KTRM'] = 86
##metars['led']['KNXP'] = 87
##metars['led']['KL35'] = 88
##metars['led']['KTSP'] = 89

def animate(strip, i, stat):
    try:
        if stat == 1:
            url = buildUrl(normal)
            content = fetchMetars(url)
            processMetars(content)
            if led: ledMetars(strip, df, stat, i, 'true')
        if led: ledMetars(strip, df, stat, i, 'false')
    except:
        pass

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
        
def ledMetars(strip, f, stat, i, update):
    strip.setPixelColor(0, Color(int(cm.RdYlGn_r(stat)[1] * 255),int(colorMapStat(stat)[0] * 255),int(colorMapStat(stat)[2] * 255)))
    strip.show()
    print('UPDATE: ' + str(i) + ', LED: ' + '0' + ', SID: ' + 'status' + ', DATA: ' + 'status' + ', COLOR: ' + str([int(colorMapStat(stat)[1] * 255),int(colorMapStat(stat)[0] * 255),int(colorMapStat(stat)[2] * 255)]))
    if update == 'true':
        for id in df.index:
            if df['led'][id] > 0:
                if df['R'][id] > -1:
                    strip.setPixelColor(int(df['led'][id]), Color(int(df['G'][id] * 255),int(df['R'][id] * 255),int(df['B'][id] * 255)))             
                    strip.show()
                    if ledVerbose:
                        print('UPDATE: ' + str(i) + ', LED: ' + str(df['led'][id]) + ', SID: ' + str(df['station_id'][id]) + ', DATA: ' + str(df[dataUse][id]) + ', COLOR: ' + str(df['clr255'][id]))  

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

i = 0
stat = 1
while 1 > 0:
    animate(strip, i, stat)
    i = i + 1
    stat = 1 - (float(np.ceil(i/updatesteps)) - float((i/updatesteps)))
    sleep(refreshinterval/1000)
    