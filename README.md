# astrotimes

Quick CLI tool for quickly (in terminal) printing today's sunset, 12 degree, and 18 degree twilight times, along with moonrise and moonset (if during the night), for a given observatory, presented in any time zone.

Also: Script which will, for some observatory, tell you how many hours and minutes are left until the next (sunset, twilight, etc). 

## Dependencies
Only a few: 

External:
- `numpy`
- `astropy`

Internal (you should have these)
- `datetime`
- `zoneinfo`
- `json`


## Installation 
Clone the repo via 

```
git clone https://github.com/prappleizer/astrotimes.git
```
And then install in an environment of choice: 

```
pip install .
```

## Usage

Once installed, you can call the two scripts from the command line:

```
astrotimes -o keck
```
where `keck` is the observatory of interest. The following also works:

```
astrotimes --observatory keck
```

A list of supported observatories is [here](https://github.com/astropy/astropy-data/blob/gh-pages/coordinates/sites.json); names are case insensitive for that.

It is also relatively easy to add a new observatory --- simply open the local `sites.json` file in the repo and copy the format of the other observatories to add your own. When using the tool, it will fall back on the local list if the web-search doesn't work (or if you are offline).

This will print times in the local time of the observatory. If you want to see the times in a different timezone (i.e., where you are now), run, e.g., 

```
astrotimes -o palomar -t US/Eastern
```
in which `-t` is short for `--tz_print`. All officially recognized timezones should work. 

By default, the code determines which night to compute based on the midnight which is closest to your current time when the code is run. Most of the time, this should be what you want, but you can also supply arbitrary dates via the `-d` or `--date` argument, e.g., 

```
astrotimes -o keck -d 2023-04-26
```
or
```
astrotimes -o keck --date 2023-04-26
```

The code printout shows which evening->morning is being shown, so you can adjust accordingly to get yesterday, tomorrow, etc.

## Time Until

The other way the tool works is to tell you how many hours and minutes until the next sunset, sunrise, etc. You can do this with the same format (but without the need to specify a current timezone):

```
astrotimes_until -o keck
```

This will give you a readout similar to the above, but with how long remains until the next set of sunsets, twilights, etc. 

In both cases, the moon is handled as follows: Only the range of -12 hours to the calculated sunrise is queried; if the moon is already up at the start of night, or is still up at the end of night, the moonrise/moonset times will simply display the sunset or sunrise time. 


