# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/    

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.animation as animation
import urllib
import xml.etree.ElementTree as ET
from matplotlib import pyplot as plt
from matplotlib import cm
import pandas as pd
import numpy as np
import tkinter as tk

dataUse = 'wind_speed_kt'
colorMap = cm.jet
colorMapStat = cm.RdYlGn_r
refreshinterval = 1000
figextent = [-126.24,-62.7,25.115,49.55]
img = 'ca.jpg'
imgextent = [-125,-113.5,32.53,40.52]
img = 'usa.jpg'
imgextent = [-126.24,-62.7,25.115,49.55]
size = 35
updatesteps = 75
statx = -122
staty = 34
statsize = 120
plot = True
led = True
ledVerbose = True
saveplot = False

normal = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=3&mostRecentForEachStation=true&stationString='
latlonrect = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&minLat='+str(figextent[2])+'&minLon='+str(figextent[0])+'&maxLat='+str(figextent[3])+'&maxLon='+str(figextent[1])+'&hoursBeforeNow=3&mostRecentForEachStation=true'

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
metars['led']['KSBP'] = 51
metars['led']['KSMX'] = 52
metars['led']['KVBG'] = 53
metars['led']['KIZA'] = 54
metars['led']['KOXR'] = 55
metars['led']['KSDB'] = 56
metars['led']['KDLO'] = 57
metars['led']['KVIS'] = 58
metars['led']['KMOD'] = 59
metars['led']['KCVH'] = 60
metars['led']['KE16'] = 61
metars['led']['KRHV'] = 62
metars['led']['KLVK'] = 63
metars['led']['KC83'] = 64
metars['led']['KHWD'] = 65
metars['led']['KPAO'] = 66
metars['led']['KSQL'] = 67
metars['led']['KHAF'] = 68
metars['led']['KNUQ'] = 69
metars['led']['KCCR'] = 70
metars['led']['KSCK'] = 71
metars['led']['KMMH'] = 72
metars['led']['KCRQ'] = 73
metars['led']['KNFG'] = 74
metars['led']['KL18'] = 75
metars['led']['KF70'] = 76
metars['led']['KOKB'] = 77
metars['led']['KRNM'] = 78
metars['led']['KNKX'] = 79
metars['led']['KMYF'] = 80
metars['led']['KSEE'] = 81
metars['led']['KSDM'] = 82
metars['led']['KNRS'] = 83
metars['led']['KCZZ'] = 84
metars['led']['KIPL'] = 85
metars['led']['KTRM'] = 86
metars['led']['KNXP'] = 87
metars['led']['KL35'] = 88
metars['led']['KTSP'] = 89

f = plt.figure(figsize=(10,10), tight_layout=True)

def animate(i):
    stat = 1 - (np.ceil(i/updatesteps) - i/updatesteps)
    try:
        if stat == 1:
            url = buildUrl(normal)
            processMetars(fetchMetars(latlonrect))
            if led: ledMetars(df, stat, i, 'true')
        if plot: plotMetars(df, dataUse, stat)
        if led: ledMetars(df, stat, i, 'false')
    except:
        pass

def buildUrl(url):
    for stationId in metars['led'].keys():
        url = url + stationId + ','
    return url

def fetchMetars(url):
    content = urllib.request.urlopen(url).read()
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

def plotMetars(df, name, stat):
    if plot:
        plt.cla()
        plt.clf()
        plt.imshow(plt.imread(img), extent=imgextent)
        plt.scatter(df['longitude'], df['latitude'], marker='+', c='black', s=size, linewidth=1)
        dfn = df[pd.notnull(df[dataUse])]
        plt.scatter(dfn['longitude'], dfn['latitude'], c=dfn['clr'], cmap=colorMap, s=size, linewidth=1)
        plt.scatter(statx, staty, c=stat, s=statsize, linewidth=1, cmap=colorMapStat, vmin=0, vmax=1)
        plt.xlim(figextent[0],figextent[1])
        plt.ylim(figextent[2],figextent[3])
        plt.grid('minor')
        plt.axes().set_aspect('auto')
    if saveplot:
        plt.savefig(name+'.pdf', dpi=400)
        
def ledMetars(df, stat, i, update):
    #strip.setPixelColor(0, Color(int(cm.RdYlGn_r(stat)[1] * 255),int(colorMapStat(stat)[0] * 255),int(colorMapStat(stat)[2] * 255)))
    #strip.show()
    print('UPDATE: ' + str(i) + ', LED: ' + '0' + ', SID: ' + 'status' + ', DATA: ' + 'status' + ', COLOR: ' + str([int(colorMapStat(stat)[1] * 255),int(colorMapStat(stat)[0] * 255),int(colorMapStat(stat)[2] * 255)]))
    if update == 'true':
        for id in df.index:
            if df['led'][id] > 0:
                #strip.setPixelColor(df['led'][id], Color(int(df['G'][id] * 255),int(df['R'][id] * 255),int(df['B'][id] * 255)))
                #strip.show()             
                if ledVerbose:
                    print('UPDATE: ' + str(i) + ', LED: ' + str(df['led'][id]) + ', SID: ' + str(df['station_id'][id]) + ', DATA: ' + str(df[dataUse][id]) + ', COLOR: ' + str(df['clr255'][id]))
                            
class metarApp(tk.Tk):    
    def __init__(self, *args, **kwargs):        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "METAR Application")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        frame = mapFrame(container, self)
        self.frames[mapFrame] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(mapFrame)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class mapFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = metarApp()
ani = animation.FuncAnimation(f, animate, interval=refreshinterval)
app.mainloop()
