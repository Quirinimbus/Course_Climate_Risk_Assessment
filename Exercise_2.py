#!/usr/bin/env python
# coding: utf-8

# **Note**: Work with reduced datasets for the exercise tasks, that is the datasets in the EUR-11N folder.
# 
# The solutions are available in the same folder, check them if you get stuck but try to find a solution on your own first.

# # Task 1

# To do this task, in your home directory select this file `/lhome/cra2022/YOURHOME/climriskdata/EUR-11N/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/historical/tas/reduced_tas_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1_day_19710101-19751231_LL.nc`. 
# 
# Find out the following:
# 
# a) Data variables (how many? what are their names?)
# 
# b) Coordinates and dimensions of the file. Are coordinates and dimensions the same?
# 
# c) Max/Min of the following: time, latitude, longitude
# 
# d) Unit of the variable
# 
# e) Extract the grid points located close to Bern. (Hint: Use `method='nearest'`)
# 
# f) Visualise the time-series for Bern using a quick plot.

# In[27]:


import cartopy.crs as ccrs # for geographic plotting
import cartopy.feature as cfeature
from IPython.display import Image
import xarray as xr
import xclim as xc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xclim as xc
import xarray as xr

# insert a new cell and enter your solution
#!pwd
input_file = '/lhome/cra2022/l.quirino.2_2022/climriskdata/EUR-11N/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/historical/tas/reduced_tas_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1_day_19710101-19751231_LL.nc'
#input_file

datos = xr.open_dataset(input_file)

datos

# a) time_bnds, tas

# b) dimensions: Eg, lat, lon, time
#    coordinates: labels of each point in the form of a Python-dictionary

# c) Time: 1 to 1826 steps ('1971-01-01T12:00:00.000000000', ..., '1975-12-31T12:00:00.000000000')
#    Lon: 5. to 11.
#    Lat: 44 to 48 N

# d) Long_name: Near-Surface Air Temperature
#    Units: K


# In[2]:


# e)

# quick time series plot for Bern
bern = datos.tas.sel(lat=46.9, lon=7.4, method='nearest')#.plot();

# f) 

bern.plot()


# # Task 2

# a)	Select the years 1971, 1972-1974 from the file you used in task 1.
# 
# b)	Select the `autumn (SON)` months for the years 1971-1975 (Hint: do it in two steps using a mask). 
# 
# c)	Calculate `mean climatology` for the data selected in b)
# 
# d) Calculate anomalies for autumn months in 1973 with respect to climatological mean (1971-1975) and visualize it with a quick plot
# 

# In[3]:


# a) 

temp71 = datos.tas.sel(time=slice('1971-01-01', '1971-12-31' ))

temp71

temp72_75 = datos.tas.sel(time=slice('1972-01-01', '1975-12-31' ))

temp72_75


# In[4]:


# b) 

time_mask_autumn = datos.time.dt.month.isin([9,10,11]) # isin selects timestamps that belong to months 9, 10 and 11

time_mask_autumn

temp71_75_SON = datos.tas[time_mask_autumn,:,:]

temp71_75_SON.plot()


# In[5]:


# c)

clima_SON = temp71_75_SON.mean("time")

clima_SON.plot()


# In[6]:


# d)

temp_SON73 = datos.tas.sel(time=slice('1973-09-01', '1973-11-30')).mean("time")

temp_SON73

anom = temp_SON73 - clima_SON

anom.plot(cmap='RdBu_r', vmin=-2.0, vmax=+2.0, extend='both')


# # Task 3

# Take a temperature file (e.g. tas.nc).
# 
# a) Convert the temperature from `degrees Kelvin` into `degrees Celsius` by subtracting -273.15 from the variable.
# 
# b) Correct the `unit` attribute of the modified file to degree Celsius.
# 
# c) Select the first time step of the modified file and verify the temperature using a quick plot. Are the automatic labelling in the colorbar in correct units, that is degree Celsius? Save only the first time step as a `.nc` file to the disk.
# 
# d) Convert temperature unit same as in a) for tas.nc but by using `xclim` 
# 
# e) Check the `unit` attribute in the file. Did `xclim` correct it automatically?

# In[7]:


# a) 

t2m_C = datos.tas - 273.15

# b)

t2m_C.attrs['units'] = '°C'

t2m_C

# c)

t2m_0 = t2m_C.isel(time=0)

t2m_0.plot()


# In[8]:


# d)
del t2m_C
t2m_C = xc.units.convert_units_to(datos.tas, '°C')

t2m_C.attrs["units"]


# # Task 4 

# Compare the maximum summer temperature of 1972 and 1973 for all the grid points.
# 
# *Hint:* Select the two years first in seperate variables (`Tmax_1972`, `Tmax_1973`) and calculate the difference.

# In[9]:


tmx_72 = datos.tas.sel(time=slice('1972')).max("time")
tmx_73 = datos.tas.sel(time=slice('1973')).max("time")

diff_tmx = tmx_72 - tmx_73

diff_tmx.plot()


# # Task 5

# 
# 
#  Calculate the 16th and 84th quantiles for the `precipitation rate`.
# 
# 
# *Use a PR file in EUR-11N*
# 
# 
# 

# In[10]:


pr_file = '/lhome/cra2022/climriskdata/EUR-11N/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/historical/pr/reduced_pr_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1_day_19710101-19751231_LL.nc'

ds_pr = xr.open_dataset(pr_file)

ds_pr

pr_q16 = ds_pr.pr.quantile(q=0.16, dim='time')
pr_q84 = ds_pr.pr.quantile(q=0.84, dim='time')


# In[11]:


del datos


# # Advanced: Task 6

# Calculate the `number of freezing days` (i.e. days with maximum temperature below 0°C ) for all the grid points for the file used in Task 3. Watch out for the units! 
# 
# a) Use `masking concept` to calculate it. The masked file will contain a binary field which is set to `True` if the temperature is below 0°C and to `False` everywhere else.
# Then use `sum()` to add up the freezing days you have calculated over the whole period and have a quick look at the result with a quick plot. 
# 
# b) Use `xclim.indicators.icclim.ID()` to calculate. Check the results with both degree Celsius and degree Kelvin input file. Does `xclim` takes care of units automatically? 
# 
# 

# In[12]:


t_max = xr.open_dataset('/lhome/cra2022/l.quirino.2_2022/climriskdata/EUR-11N/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/historical/tasmax/reduced_tasmax_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1_day_19710101-19751231_LL.nc')

Tmax_C = xc.units.convert_units_to(t_max.tasmax, 'degC')

# a)

Tmax_C0 = Tmax_C < 0 
count = Tmax_C0.sum().values
print('Days with Tmax_C < 0 °C are {}'.format(count))

Tmax_C0.sum('time').plot()

# b) 

freeze_d_Tmax = xc.indices.tx_days_below(Tmax_C, '0 degC')
count2 = freeze_d_Tmax.sum().values

print('Days with freeze_d_Tmax < 0 °C are {}'.format(count2))


# In[13]:


#del Tmax, t_max


# # Advanced: Task 7

# Compare the values of `Consecutive summer days (CSU)` and `Tropical Nights Index (TNI)` for a future temperature scenario with current temperatures. What could that imply for our energy consumption? Use `Tmax`  for CSU and `Tmin` for TNI 
# 
# `Note`: Since the reduced dataset, EUR-11N folder contains only years 1971-1975, use EUR-11 folder containing 1971-2000 for current file. Slice out 5 years of data from the current file (1996-2000) and domain of Switzerland, that is latitiude: 44-48 deg N and longitude: 5, 11 deg E. 
# 
# `current-file:` /lhome/cra2022/YOURHOME/climriskdata/EUR-11/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/historical/tasmax/tasmax_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1_day_19710101-20001231_LL.nc
# 
# `future-file:` /lhome/cra2022/YOURHOME/climriskdata/EUR-11N/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/rcp85/tasmax/reduced_tasmax_EUR-11_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1_day_20710101-20751231_LL.nc

# In[16]:


current_file = '/lhome/cra2022/l.quirino.2_2022/climriskdata/EUR-11/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/historical/tasmin/tasmin_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1_day_19710101-20001231_LL.nc'

future_file = '/lhome/cra2022/l.quirino.2_2022/climriskdata/EUR-11N/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/rcp85/tasmin/reduced_tasmin_EUR-11_MPI-M-MPI-ESM-LR_rcp85_r1i1p1_MPI-CSC-REMO2009_v1_day_20710101-20751231_LL.nc'


# In[17]:


ds_tas_current = xr.open_dataset(current_file).sel(time=slice('1996', '2000'),
                                                  lat=slice(44,48), lon=slice(5,11))

ds_tas_future = xr.open_dataset(future_file)


# In[19]:


# convert tasmin to deg celsius

current_tas_degC = xc.units.convert_units_to(ds_tas_current.tasmin, 'degC')
future_tas_degC = xc.units.convert_units_to(ds_tas_future.tasmin, 'degC')


# In[32]:


current_CSU = xc.indicators.icclim.CSU(current_tas_degC,)

future_CSU = xc.indicators.icclim.CSU(future_tas_degC,)


# In[34]:


fig = plt.figure(figsize=(8,6))
ax = plt.axes(projection=ccrs.PlateCarree())
(future_CSU.isel(time=0) - current_CSU.isel(time=0)).plot(ax=ax, transform=ccrs.PlateCarree(),
                                                          cbar_kwargs=dict(label='Difference in CSU',
                                                                          shrink=0.6)
                                                         )


# In[21]:


current_TNI = xc.indicators.icclim.TR(current_tas_degC,)


# In[30]:


future_TNI = xc.indicators.icclim.TR(future_tas_degC,)


# In[28]:


fig = plt.figure(figsize=(8,6))
ax = plt.axes(projection=ccrs.PlateCarree())
current_TNI.isel(time=-1).plot(ax=ax, transform=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE, linestyle=':', color='grey')
ax.add_feature(cfeature.BORDERS, linestyle=':',  color='grey')
#ax.add_feature(cfeature.OCEAN, zorder=10)


# In[31]:


fig = plt.figure(figsize=(8,6))
ax = plt.axes(projection=ccrs.PlateCarree())
future_TNI.isel(time=-1).plot(ax=ax, transform=ccrs.PlateCarree())
ax.add_feature(cfeature.COASTLINE, linestyle=':', color='grey')
ax.add_feature(cfeature.BORDERS, linestyle=':',  color='grey')
#ax.add_feature(cfeature.OCEAN, zorder=10)

