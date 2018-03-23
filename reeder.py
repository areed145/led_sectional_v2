import urllib
import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
from matplotlib import cm
import pandas as pd
import numpy as np
import tkinter as tk

#import time
#from neopixel import *
#import sys
#import os


# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

#strip.begin()

normal = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=3&mostRecentForEachStation=true&stationString='
#latlonrect = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&minLat=32&minLon=-124&maxLat=42&maxLon=-114&hoursBeforeNow=3&mostRecentForEachStation=true'
dataUse = 'cloudbase_msl'
colorMap = cm.jet
size = 3
plot = True
led = False
verbose = False
saveplot = False

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
props['temp_c']['max'] = 40
props['dewpoint_c'] = {}
props['dewpoint_c']['min'] = -5
props['dewpoint_c']['max'] = 40
props['wind_dir_degrees'] = {}
props['wind_dir_degrees']['min'] = 0
props['wind_dir_degrees']['max'] = 359
props['wind_speed_kt'] = {}
props['wind_speed_kt']['min'] = 0
props['wind_speed_kt']['max'] = 30
props['visibility_statute_mi'] = {}
props['visibility_statute_mi']['min'] = 0
props['visibility_statute_mi']['max'] = 10
props['altim_in_hg'] = {}
props['altim_in_hg']['min'] = 29
props['altim_in_hg']['max'] = 31
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
metars['led']['KSBA'] = 5
metars['led']['KNTD'] = 8
metars['led']['KCMA'] = 9
metars['led']['KNTD'] = 10
metars['led']['KVNY'] = 13
metars['led']['KWHP'] = 14
metars['led']['KBUR'] = 15
metars['led']['KBFL'] = 16
metars['led']['KNID'] = 17
metars['led']['KDAG'] = 18
metars['led']['KWJF'] = 19
metars['led']['KPMD'] = 20
metars['led']['KEDW'] = 22
metars['led']['KMHV'] = 24
metars['led']['KLAX'] = 26
metars['led']['KHHR'] = 27
metars['led']['KLGB'] = 28
metars['led']['KSLI'] = 29
metars['led']['KSNA'] = 30
metars['led']['KONT'] = 33
metars['led']['KRAL'] = 34
metars['led']['KRIV'] = 35
metars['led']['KSBD'] = 36
metars['led']['KL35'] = 37
metars['led']['KPSP'] = 38
metars['led']['KNFG'] = 43
metars['led']['KCRQ'] = 44
metars['led']['KMYF'] = 46
metars['led']['KSAN'] = 47
metars['led']['KNZY'] = 48
metars['led']['KAVX'] = 49

metars['led']['KPTV'] = 0
metars['led']['KSAC'] = 0
metars['led']['KSFO'] = 0
metars['led']['KOAK'] = 0
metars['led']['KHAN'] = 0
metars['led']['KNLC'] = 0
metars['led']['KNLC'] = 0
metars['led']['KSBA'] = 0
metars['led']['KFAT'] = 0
metars['led']['KNID'] = 0
metars['led']['KBIH'] = 0
metars['led']['KMCE'] = 0
metars['led']['KSJC'] = 0
metars['led']['KSNS'] = 0
metars['led']['KPRB'] = 0
metars['led']['KMER'] = 0
metars['led']['KWVI'] = 0
metars['led']['KMRY'] = 0
metars['led']['KMAE'] = 0
metars['led']['KSBP'] = 0
metars['led']['KSMX'] = 0
metars['led']['KVBG'] = 0
metars['led']['KIZA'] = 0
metars['led']['KOXR'] = 0
metars['led']['KSDB'] = 0
metars['led']['KDLO'] = 0
metars['led']['KVIS'] = 0
metars['led']['KMOD'] = 0
metars['led']['KCVH'] = 0
metars['led']['KE16'] = 0
metars['led']['KRHV'] = 0
metars['led']['KLVK'] = 0
metars['led']['KC83'] = 0
metars['led']['KHWD'] = 0
metars['led']['KPAO'] = 0
metars['led']['KSQL'] = 0
metars['led']['KHAF'] = 0
metars['led']['KNUQ'] = 0
metars['led']['KCCR'] = 0
metars['led']['KSCK'] = 0
metars['led']['KMMH'] = 0
metars['led']['KCRQ'] = 0
metars['led']['KNFG'] = 0
metars['led']['KL18'] = 0
metars['led']['KF70'] = 0
metars['led']['KOKB'] = 0
metars['led']['KRNM'] = 0
metars['led']['KNKX'] = 0
metars['led']['KMYF'] = 0
metars['led']['KSEE'] = 0
metars['led']['KSDM'] = 0
metars['led']['KNRS'] = 0
metars['led']['KCZZ'] = 0
metars['led']['KIPL'] = 0
metars['led']['KTRM'] = 0
metars['led']['KNXP'] = 0
metars['led']['KL35'] = 0
metars['led']['K'] = 0
    
def buildUrl(url):
    for stationId in metars['led'].keys():
        url = url + stationId + ','
    content = urllib.request.urlopen(url).read()
    return content

def getMetars(content):
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

def buildDf(metars):        
    df = pd.DataFrame.from_dict(metars, orient='columns')
    df['temp_f'] = (1.8 * df['temp_c']) + 32
    df['elevation_ft'] = df['elevation_m'] * 3.28084
    df['cloudbase_msl'] = (df['temp_c'] - df['dewpoint_c']) * (1800 / 4.4)
    df['cloudbase_agl'] = df['cloudbase_msl'] - df['elevation_ft']
    return df
    
def findColor(df):
    if dataUse == 'flight_category':
        for cat in props['flight_category'].keys():
            df.ix[df['flight_category'] == cat, 'R'] = props['flight_category'][cat][0] / 255
            df.ix[df['flight_category'] == cat, 'G'] = props['flight_category'][cat][1] / 255
            df.ix[df['flight_category'] == cat, 'B'] = props['flight_category'][cat][2] / 255
    else:
        df['R'] = (df[dataUse] - props[dataUse]['min'])/(props[dataUse]['max'] - props[dataUse]['min'])
        df['G'] = (df[dataUse] - props[dataUse]['min'])/(props[dataUse]['max'] - props[dataUse]['min'])
        df['B'] = (df[dataUse] - props[dataUse]['min'])/(props[dataUse]['max'] - props[dataUse]['min'])
        df['R'] = df['R'].apply(lambda x: colorMap(x)[0])
        df['G'] = df['G'].apply(lambda x: colorMap(x)[1])
        df['B'] = df['B'].apply(lambda x: colorMap(x)[2])
        
def plotMetars(df, name):
    plt.cla
    plt.clf    
    plt.scatter(df['longitude'], df['latitude'], marker='.', c='black', s=1)
    for i in df.index:
        if np.isfinite(df['R'][i]):
            try:
                clr = tuple([df['R'][i], df['G'][i], df['B'][i]])
                clr255 = tuple([int(df['R'][i] * 255), int(df['G'][i] * 255), int(df['B'][i] * 255)])
            except:
                pass
            if plot:
                plt.scatter(df['longitude'][i], df['latitude'][i], c=[clr], s=size)
            if led:
                if df['led'][i] > 0:
                    strip.setPixelColor(df['led'][i], Color(int(df['G'][i] * 255),int(df['R'][i] * 255),int(df['B'][i] * 255)))
                    strip.show()
            if verbose:
                print('LED: ' + str(df['led'][i]) + ', SID: ' + str(df['station_id'][i]) + ', DATA: ' + str(df[dataUse][i]) + ', COLOR: ' + str(clr255))
    if saveplot:
        plt.savefig(name+'.pdf', dpi=400)

url = buildUrl(normal)  
getMetars(url)
df = buildDf(metars)
findColor(df)
plotMetars(df, dataUse)