#!/Users/ipasha/miniconda3/envs/theia/bin/python

#########
# Quick Script to generate the daily astronomical "times" from the command line for several observatories
#########
import sys 
from astropy.coordinates import SkyCoord, get_sun, get_moon
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

from datetime import datetime,timedelta
import astropy.units as u 

import zoneinfo
import numpy as np 
import json 


import importlib.resources

#with open('../sites/sites.json') as f:
#    sites = json.load(f)


def get_midnight(datetime_obj,days=1):
    """Returns the rounded time of the next midnight from now according to the date.

    Parameters
    ----------
    datetime_obj : datetime.datetime
        datetime obj
    """
    delt = timedelta(hours=datetime_obj.hour, minutes=datetime_obj.minute,
                        seconds=datetime_obj.second, microseconds=datetime_obj.microsecond)
    midnight = datetime_obj - delt + timedelta(days=days)

    return midnight



def astrotimes(observatory,tz_print='observatory',date='today'):
    date_utc = datetime.utcnow()
    if date == 'today':
        date_local = datetime.today()
    
        delt = timedelta(hours=date_local.hour, minutes=date_local.minute,
                            seconds=date_local.second, microseconds=date_local.microsecond)
        time_to_prev_midnight = delt.total_seconds()
        previous_midnight = date_local - delt 
        next_midnight = previous_midnight + timedelta(days=1)
        time_to_next_midnight = (next_midnight - date_local).total_seconds() 
        if time_to_prev_midnight < time_to_next_midnight:
            midnight_date_use = date_utc - timedelta(hours=date_utc.hour, minutes=date_utc.minute,
                            seconds=date_utc.second, microseconds=date_utc.microsecond)
        elif time_to_prev_midnight >= time_to_next_midnight:
            midnight_date_use = date_utc - timedelta(hours=date_utc.hour, minutes=date_utc.minute,
                            seconds=date_utc.second, microseconds=date_utc.microsecond) + timedelta(days=1)
        
        midnight_date_str = midnight_date_use.strftime('%Y-%m-%d')
    else:
        midnight_date_str = date


    
    
    
    if isinstance(observatory,str):
        try:
            obsloc = EarthLocation.of_site(observatory)
            utcoffset = datetime.now(zoneinfo.ZoneInfo(obsloc.info.meta['timezone'])).utcoffset().total_seconds()/60/60
        except:
            print('Falling back on local site list.')
            with importlib.resources.open_text("astrotimes", "sites.json") as file:
                sites = json.load(file)  
            try:
                site = sites[observatory]
            except KeyError:
                for key in sites.keys():
                    if observatory in sites[key]['aliases']:
                        site = sites[key]
                        break
                if not 'site' in locals():
                    raise AssertionError('Observatory not found in either primary list or aliases.')
            elevation = u.Quantity(site['elevation'],unit=site['elevation_unit'])
            lat = u.Quantity(site['latitude'],unit=site['latitude_unit'])
            lon = u.Quantity(site['longitude'],unit=site['longitude_unit'])
            tz = site['timezone']
            obsloc = EarthLocation.from_geodetic(lon, lat, elevation)
            utcoffset = datetime.now(zoneinfo.ZoneInfo(tz)).utcoffset().total_seconds()/60/60

                
    elif not isinstance(observatory,EarthLocation):
        raise AssertionError('If a non string is provided, it must be an astropy EarthLocation')
    midnight = Time(f'{midnight_date_str} 00:00:00') - utcoffset*u.hour

    delta_midnight = np.linspace(-12, 12, 800)*u.hour
    obs_times = midnight+delta_midnight
    frame = AltAz(obstime=obs_times,location=obsloc)
    
    sun = get_sun(obs_times).transform_to(frame)

    sunset = obs_times[np.where( sun.alt.to(u.deg) < -0*u.deg)[0][0]]
    sundown_12deg = obs_times[np.where( sun.alt.to(u.deg) < -12*u.deg)[0][0]]
    sundown_18deg = obs_times[np.where( sun.alt.to(u.deg) < -18*u.deg)[0][0]]
    sunrise_18deg = obs_times[np.where( sun.alt.to(u.deg) < -18*u.deg)[0][-1]]
    sunrise_12deg = obs_times[np.where( sun.alt.to(u.deg) < -12*u.deg)[0][-1]]
    sunrise = obs_times[np.where( sun.alt.to(u.deg) < 0*u.deg)[0][-1]]
    start_str = f'Local Sunset/Rise times at {observatory} for date {midnight_date_str}'
    
    
    if tz_print == 'observatory':
        prutcoffset = utcoffset 
        start_str = f'Local Sunset/Rise times at {observatory} for date {midnight_date_str}'
    else:
        prutcoffset = datetime.now(zoneinfo.ZoneInfo(tz_print)).utcoffset().total_seconds()/60/60
        start_str = f'Sunset/Rise times IN {tz_print} for {observatory} for date {midnight_date_str}'
        
    sunset = sunset+prutcoffset*u.hr
    sundown_12deg = sundown_12deg+prutcoffset*u.hr
    sundown_18deg = sundown_18deg+prutcoffset*u.hr
    sunrise_18deg = sunrise_18deg+prutcoffset*u.hr
    sunrise_12deg = sunrise_12deg+prutcoffset*u.hr
    sunrise = sunrise + +prutcoffset*u.hr
    
    print('\n')
    print(start_str)
    print('-'*len(start_str))
    print(f'Sunset:                  {sunset}')
    print(f'12 deg Twilight:         {sundown_12deg}')
    print(f'18 deg Twilight:         {sundown_18deg}')
    print('   ')
    print(f'18 deg Twilight:         {sunrise_18deg}')
    print(f'12 deg Twilight:         {sunrise_12deg}')
    print(f'Sunrise:                 {sunrise}')

    night_times = obs_times[sun.alt.to(u.deg) < -0*u.deg]
    frame2 = AltAz(obstime=night_times,location=obsloc)
    moon = get_moon(night_times).transform_to(frame2)
    moonrise = night_times[np.where( moon.alt.to(u.deg) > -0*u.deg)[0][0]]
    if moonrise == sunset:
        moonrise = 'UP @ start of night'
    #if moonrise < sunset:
    #    moonrise = sunset 
    moonset= night_times[np.where( moon.alt.to(u.deg) < -0*u.deg)[0][0]]
    if moonset == sunrise:
        moonset = 'UP @ end of night'

    #if moonset > sunrise:
    #    moonset = sunrise 

    print('  ')
    if isinstance(moonrise,str):
        print(f'Moonrise:               {moonrise}')
    else:
        print(f'Moonrise:                {moonrise+prutcoffset*u.hr}')
    if isinstance(moonset,str):
        print(f'Moonset:                 {moonset}')
    print(f'Moonset:                 {moonset+prutcoffset*u.hr}')



def time_until(observatory):
    
    if isinstance(observatory,str):
        try:
            obsloc = EarthLocation.of_site(observatory)
            utcoffset = datetime.now(zoneinfo.ZoneInfo(obsloc.info.meta['timezone'])).utcoffset().total_seconds()/60/60
        except:
            print('Falling back on local site list.')
            with importlib.resources.open_text("astrotimes", "sites.json") as file:
                sites = json.load(file)  
            try:
                site = sites[observatory]
            except KeyError:
                for key in sites.keys():
                    if observatory in sites[key]['aliases']:
                        site = sites[key]
                        break
                if not 'site' in locals():
                    raise AssertionError('Observatory not found in either primary list or aliases.')
            elevation = u.Quantity(site['elevation'],unit=site['elevation_unit'])
            lat = u.Quantity(site['latitude'],unit=site['latitude_unit'])
            lon = u.Quantity(site['longitude'],unit=site['longitude_unit'])
            tz = site['timezone']
            obsloc = EarthLocation.from_geodetic(lon, lat, elevation)
            utcoffset = datetime.now(zoneinfo.ZoneInfo(tz)).utcoffset().total_seconds()/60/60
            print(utcoffset)

    elif not isinstance(observatory,EarthLocation):
        raise AssertionError('If a non string is provided, it must be an astropy EarthLocation')
    
    current_time_at_obsloc = datetime.utcnow() + timedelta(hours=utcoffset)
    next_midnight = Time(get_midnight(current_time_at_obsloc,days=1))  - utcoffset*u.hour
    print(next_midnight)
    night = Night(next_midnight,obsloc)

    
    print('\n')
    start_str = f'Time until next Astronomical time of Interest: {observatory} observatory.'
    print(start_str)
    print('-'*len(start_str))
    print(f'Time until next Sunset:                  {night.time_to_sunset}')
    print(f'Time until next 12 deg Twilight:         {night.time_to_sunset_12deg}')
    print(f'Time until next 18 deg Twilight:         {night.time_to_sunset_18deg}')
    print('   ')
    print(f'Time until next 18 deg Twilight:         {night.time_to_sunrise_18deg}')
    print(f'Time until next 12 deg Twilight:         {night.time_to_sunrise_12deg}')
    print(f'Time until next Sunrise:                 {night.time_to_sunrise}')

    # night_times = obs_times[sun.alt.to(u.deg) < -0*u.deg]
    # frame2 = AltAz(obstime=night_times,location=obsloc)
    # moon = get_moon(night_times).transform_to(frame2)
    # moonrise = (night_times[np.where( moon.alt.to(u.deg) > -0*u.deg)[0][0]] - Time.now()).to_datetime()
    # if moonrise <= sunset:
    #     moonrise = 'UP @ start of night'
    # #if moonrise < sunset:
    # #    moonrise = sunset 
    # moonset= (night_times[np.where( moon.alt.to(u.deg) < -0*u.deg)[0][0]] - Time.now()).to_datetime()
    # if moonset>=sunrise:
    #     moonset = 'UP @ end of night'

    # #if moonset > sunrise:
    # #    moonset = sunrise 

    # print(' ')
    # if isinstance(moonrise,str):
    #     print(f'Time until next Moonrise:                {moonrise}')
    # else:
    #     print(f'Time until next Moonrise:                 {moonrise}')
    # if isinstance(moonset,str):
    #     print(f'Time until next Moonset:                 {moonset}')
    # print(f'Time until next Moonset:                 {moonset}')




class Night():
    def __init__(self,midnight,obsloc):
        self.midnight=midnight
        self.obsloc=obsloc 
        self.calc_quantities() 
    
    def calc_quantities(self):
        # First, Sunsets. We are only ever going to need the next upcoming midnight or the next one after that. 
        self.time_to_sunset = self.sunset_wrapper(self.midnight,0.0)
        self.time_to_sunset_12deg = self.sunset_wrapper(self.midnight,-12.0)
        self.time_to_sunset_18deg = self.sunset_wrapper(self.midnight,-18.0)
        self.time_to_sunrise = self.sunrise_wrapper(self.midnight,0.0)
        self.time_to_sunrise_18deg = self.sunrise_wrapper(self.midnight,-18.0)
        self.time_to_sunrise_12deg = self.sunrise_wrapper(self.midnight,-12.0)
        

    def sunset_wrapper(self,midnight,angle,which='sunsets'):
        time_until = self.calc_values(midnight,angle,which=which)
        print(time_until)
        if time_until< timedelta(hours=0):
            next_midnight = midnight + 24*u.hour
            time_until = self.calc_values(next_midnight,angle,which=which)
        return time_until

    def sunrise_wrapper(self,midnight,angle,which='sunrises'):
        time_until = self.calc_values(midnight,angle,which=which)
        if time_until> timedelta(hours=24,minutes=5): 
            prev_midnight = midnight - 24*u.hour 
            time_until = self.calc_values(prev_midnight,angle,which=which)
        return time_until 

    def calc_values(self,midnight,angle,which):
        if which == 'sunsets':
            ind = 0 
        elif which == 'sunrises':
            ind = -1
        # delta_midnight_init = np.linspace(-12, 12, 24)*u.hour
        # obs_times = midnight+delta_midnight_init
        # frame1 = AltAz(obstime=obs_times,location=self.obsloc)
        # sun = get_sun(obs_times).transform_to(frame1)
        # coarse_time = obs_times[np.where( sun.alt.to(u.deg) < angle*u.deg)[0][ind]] 
        # delta_times_2 = np.linspace(-1,1,120)*u.minute
        # obs_times_2 = coarse_time + delta_times_2 
        # frame2 = AltAz(obstime=obs_times_2,location=self.obsloc)
        # sun2 = get_sun(obs_times_2).transform_to(frame2)
        # time = obs_times_2[np.where( sun2.alt.to(u.deg) < angle*u.deg)[0][ind]] 
        # time_until = (time - Time.now()).to_datetime() 
        delta_midnight = np.linspace(-12,12,800)*u.hour
        obs_times = midnight+delta_midnight
        frame = AltAz(obstime=obs_times,location=self.obsloc)
        sun = get_sun(obs_times).transform_to(frame)
        time = obs_times[np.where( sun.alt.to(u.deg) < angle*u.deg)[0][ind]] 
        print(time)
        time_until = (time - Time.now()).to_datetime() 
        return time_until


