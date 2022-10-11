#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
from matplotlib.cm import get_cmap
from scipy import stats
from scipy.stats import t


# In[2]:


#pr_file = '/lhome/cra2022/climriskdata/EUR-11/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/historical/pr/pr_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1_day_19710101-20001231_LL.nc'
pr_file = '/lhome/cra2022/climriskdata/EUR-11/ICHEC-EC-EARTH_CLMcom-CCLM4-8-17_v1/historical/pr/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19710101-20001231_LL.nc'

ds_pr = xr.open_dataset(pr_file)

pr_file85 = '/lhome/cra2022/climriskdata/EUR-11/ICHEC-EC-EARTH_CLMcom-CCLM4-8-17_v1/rcp85/pr/pr_EUR-11_ICHEC-EC-EARTH_rcp85_r12i1p1_CLMcom-CCLM4-8-17_v1_day_20710101-21001231_LL.nc'

ds_pr85 = xr.open_dataset(pr_file85)

ds_pr85


# In[3]:


pr_mm85 = ds_pr85.pr * 86400
pr_mm85.attrs['units'] = 'mm/day'
prcp_7100_85 = pr_mm85.sel(lat=slice(30,45))


# In[4]:


del ds_pr85


# In[5]:


pr_mm = ds_pr.pr * 86400
pr_mm.attrs['units'] = 'mm/day'
prcp_7100 = pr_mm.sel(lat=slice(30,45))


# In[6]:


del ds_pr


# In[7]:


mon_water_cons = (133*365)/12
mon_water_cons


# In[8]:


mon_prcp_7100_85= prcp_7100_85.resample(time = 'M').sum()

mon_clim_rcp85 = mon_prcp_7100_85.groupby('time.month')

mon_mean_clim_rcp85 = mon_clim_rcp85.mean('time')


# In[9]:


season_prcp_7100_rcp85 = mon_prcp_7100_85.groupby('time.season')

season_mean_prcp_7100_rcp85 = season_prcp_7100_rcp85.sum('time')/30

season_var_prcp_7100_rcp85 = season_mean_prcp_7100_rcp85.var('season')


# In[10]:


clim_prcp_7100_85 = mon_prcp_7100_85.sum('time')/30


# In[11]:


del prcp_7100_85


# In[12]:


mon_prcp_7100= prcp_7100.resample(time = 'M').sum()


# In[13]:


clim_prcp_7100 = mon_prcp_7100.sum('time')/30

mon_clim = mon_prcp_7100.groupby('time.month')

mon_mean_clim = mon_clim.mean('time')


# In[14]:


season_prcp_7100 = mon_prcp_7100.groupby('time.season')

season_mean_prcp_7100 = season_prcp_7100.sum('time')/30

season_var_prcp_7100 = season_mean_prcp_7100.var('season')


# In[15]:


del prcp_7100


# In[16]:


rain_catcher_rcp85 = ((mon_mean_clim_rcp85/mon_water_cons) * 10)*100

rain_catcher = ((mon_mean_clim/mon_water_cons) * 10)*100


# In[17]:


#ROME, ITA
rain_cathcer_rome = rain_catcher.sel(lat='41.893333',lon='12.482778', method='nearest')
rain_cathcer_rcp85_rome = rain_catcher_rcp85.sel(lat='41.893333',lon='12.482778', method='nearest')

#MADRID, SPA
rain_cathcer_madrid = rain_catcher.sel(lat='40.416667',lon='-3.7025', method='nearest')
rain_cathcer_rcp85_madrid = rain_catcher_rcp85.sel(lat='40.416667',lon='-3.7025', method='nearest')

#CAIRO, EGY
rain_cathcer_cairo = rain_catcher.sel(lat='30.044444',lon='31.235833', method='nearest')
rain_cathcer_rcp85_cairo = rain_catcher_rcp85.sel(lat='30.044444',lon='31.235833', method='nearest')


# In[21]:


#ROME, ITA

barWidth = 0.8
fig = plt.subplots(figsize =(12, 8))

MM = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

plt.bar(rain_cathcer_rome.month, rain_cathcer_rome,width = barWidth, edgecolor ='grey', label ='(1971 - 2000)',color='blue')
#plt(rain_cathcer_rome.month, rain_cathcer_rcp85_rome, width = barWidth, edgecolor ='grey', label ='(2071 - 2100)_RCP8.5',
#        color='green', alpha = 0.8)

rain_cathcer_rcp85_rome.plot(color='black',label ='(2071 - 2100)_RCP8.5',marker='8')

plt.xlabel('Month', fontweight ='bold', fontsize = 15)
plt.ylabel('% of Water Consumption', fontweight ='bold', fontsize = 15)
plt.xticks(ticks = range(1,13), labels = MM)
plt.title('Raincatching Water Ratio in Rome, Italy',fontsize=20)
 
plt.legend()
plt.savefig("/lhome/cra2022/l.quirino.2_2022/Quirino_Leonardo/Project/Raincathcer_Rome.png", dpi = 300, bbox_inches="tight",pad_inches=0)


# In[22]:


plt.close()


# In[23]:


#MADRID, SPA

barWidth = 0.8
fig = plt.subplots(figsize =(12, 8))

MM = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

plt.bar(rain_cathcer_madrid.month, rain_cathcer_madrid,width = barWidth, edgecolor ='grey', label ='(1971 - 2000)',color='blue')

rain_cathcer_rcp85_madrid.plot(color='black',label ='(2071 - 2100)_RCP8.5',marker='8')

plt.xlabel('Month', fontweight ='bold', fontsize = 15)
plt.ylabel('% of Water Consumption', fontweight ='bold', fontsize = 15)
plt.xticks(ticks = range(1,13), labels = MM)
plt.title('Raincatching Water Ratio in Madrid, Spain',fontsize=20)
 
plt.legend()
plt.savefig("/lhome/cra2022/l.quirino.2_2022/Quirino_Leonardo/Project/Raincathcer_Madrid.png", dpi = 300, bbox_inches="tight",pad_inches=0)


# In[24]:


plt.close()


# In[25]:


#CAIRO, EGYPT

barWidth = 0.8
fig = plt.subplots(figsize =(12, 8))

MM = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul','Aug', 'Sep', 'Oct', 'Nov', 'Dec']

plt.bar(rain_cathcer_cairo.month, rain_cathcer_cairo,width = barWidth, edgecolor ='grey', label ='(1971 - 2000)',color='blue')

rain_cathcer_rcp85_cairo.plot(color='black',label ='(2071 - 2100)_RCP8.5',marker='8')

plt.xlabel('Month', fontweight ='bold', fontsize = 15)
plt.ylabel('% of Water Consumption', fontweight ='bold', fontsize = 15)
plt.xticks(ticks = range(1,13), labels = MM)
plt.title('Raincatching Water Ratio in Cairo, Egypt',fontsize=20)
 
plt.legend()
plt.savefig("/lhome/cra2022/l.quirino.2_2022/Quirino_Leonardo/Project/Raincathcer_Cairo.png", dpi = 300, bbox_inches="tight",pad_inches=0)

