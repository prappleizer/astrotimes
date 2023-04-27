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







def astrotimes(observatory,tz_print='observatory'):

    date_local =datetime.today()
    date = datetime.today() + timedelta(days=1)
    date_str1 = date_local.strftime('%Y-%m-%d')
    date_str2 = date.strftime('%Y-%m-%d')
    
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
    midnight = Time(f'{date_str2} 00:00:00') - utcoffset*u.hour

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
    start_str = f'Local Sunset/Rise times at {observatory} for date {date_str1}'
    
    
    if tz_print == 'observatory':
        prutcoffset = utcoffset 
        start_str = f'Local Sunset/Rise times at {observatory} for date {date_str1}'
    else:
        prutcoffset = datetime.now(zoneinfo.ZoneInfo(tz_print)).utcoffset().total_seconds()/60/60
        start_str = f'Sunset/Rise times IN {tz_print} for {observatory} for date {date_str1}'
        
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

    date_local =datetime.today()
    date = datetime.today() + timedelta(days=1)
    date_str1 = date_local.strftime('%Y-%m-%d')
    date_str2 = date.strftime('%Y-%m-%d')
    
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
    midnight = Time(f'{date_str2} 00:00:00') - utcoffset*u.hour
    delta_midnight = np.linspace(-12, 12, 800)*u.hour
    obs_times = midnight+delta_midnight
    frame = AltAz(obstime=obs_times,location=obsloc)
    
    sun = get_sun(obs_times).transform_to(frame)

    sunset = (obs_times[np.where( sun.alt.to(u.deg) < -0*u.deg)[0][0]] - Time.now()).to_datetime()
    sundown_12deg = (obs_times[np.where( sun.alt.to(u.deg) < -12*u.deg)[0][0]] - Time.now()).to_datetime()
    sundown_18deg = (obs_times[np.where( sun.alt.to(u.deg) < -18*u.deg)[0][0]] - Time.now()).to_datetime()
    sunrise_18deg = (obs_times[np.where( sun.alt.to(u.deg) < -18*u.deg)[0][-1]] - Time.now()).to_datetime()
    sunrise_12deg = (obs_times[np.where( sun.alt.to(u.deg) < -12*u.deg)[0][-1]] - Time.now()).to_datetime()
    sunrise = (obs_times[np.where( sun.alt.to(u.deg) < 0*u.deg)[0][-1]] - Time.now()).to_datetime() 
    print('\n')
    start_str = f'Time until next Astronomical time of Interest: {observatory} observatory.'
    print(start_str)
    print('-'*len(start_str))
    print(f'Time until next Sunset:                  {sunset}')
    print(f'Time until next 12 deg Twilight:         {sundown_12deg}')
    print(f'Time until next 18 deg Twilight:         {sundown_18deg}')
    print('   ')
    print(f'Time until next 18 deg Twilight:         {sunrise_18deg}')
    print(f'Time until next 12 deg Twilight:         {sunrise_12deg}')
    print(f'Time until next Sunrise:                 {sunrise}')

    night_times = obs_times[sun.alt.to(u.deg) < -0*u.deg]
    frame2 = AltAz(obstime=night_times,location=obsloc)
    moon = get_moon(night_times).transform_to(frame2)
    moonrise = (night_times[np.where( moon.alt.to(u.deg) > -0*u.deg)[0][0]] - Time.now()).to_datetime()
    if moonrise <= sunset:
        moonrise = 'UP @ start of night'
    #if moonrise < sunset:
    #    moonrise = sunset 
    moonset= (night_times[np.where( moon.alt.to(u.deg) < -0*u.deg)[0][0]] - Time.now()).to_datetime()
    if moonset>=sunrise:
        moonset = 'UP @ end of night'

    #if moonset > sunrise:
    #    moonset = sunrise 

    print(' ')
    if isinstance(moonrise,str):
        print(f'Time until next Moonrise:                {moonrise}')
    else:
        print(f'Time until next Moonrise:                 {moonrise}')
    if isinstance(moonset,str):
        print(f'Time until next Moonset:                 {moonset}')
    print(f'Time until next Moonset:                 {moonset}')


