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


# In[2]:


#pr_file = '/lhome/cra2022/climriskdata/EUR-11/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/historical/pr/pr_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1_day_19710101-20001231_LL.nc'
pr_file = '/lhome/cra2022/climriskdata/EUR-11/ICHEC-EC-EARTH_CLMcom-CCLM4-8-17_v1/historical/pr/pr_EUR-11_ICHEC-EC-EARTH_historical_r12i1p1_CLMcom-CCLM4-8-17_v1_day_19710101-20001231_LL.nc'

ds_pr = xr.open_dataset(pr_file)

ds_pr


# In[3]:


pr_mm = ds_pr.pr * 86400
pr_mm.attrs['units'] = 'mm/day'
prcp_7100 = pr_mm.sel(lat=slice(30,45))

prcp_7100


# In[4]:


del ds_pr


# In[5]:


mon_prcp_7100 = prcp_7100.resample(time = 'M').sum()


# In[6]:


mon_prcp_7100


# In[7]:


del prcp_7100


# In[8]:


clim_prcp_7100 = mon_prcp_7100.sum('time')/30
clim_prcp_7100

mon_clim = mon_prcp_7100.groupby('time.month')

mon_mean_clim = mon_clim.mean('time')

#clim_var_7100 = clim_var_7100**2


# In[9]:


season_prcp_7100 = mon_prcp_7100.groupby('time.season')


# In[10]:


season_prcp_7100


# In[11]:


season_mean_prcp_7100 = season_prcp_7100.sum('time')/30

season_var_prcp_7100 = season_mean_prcp_7100.var('season')


# In[12]:


season_DJF_prcp_7100 = season_mean_prcp_7100.sel(season='DJF')

season_JJA_prcp_7100 = season_mean_prcp_7100.sel(season='JJA')


# In[13]:


season_mean_prcp_7100

season_DJF_prcp_7100

#season_var_prcp_7100.plot()#.sel(season='JJA').plot()


# In[14]:


clim_var_7100 = mon_mean_clim.var('month')

clim_std_7100 = mon_mean_clim.std('month')


# In[15]:


clim_var_7100


# In[16]:


mon_mean_clim.sel(lat='40',lon='22', method='nearest').plot() #somewhere in greece given by Markella


# In[17]:


ds_pop = xr.open_dataset('/lhome/cra2022/climriskdata/EUR-11S/Estimated_population/Estimated_population_2020_LL.nc')
ds_pop_medi = ds_pop.sel(lat=slice(30,45))


# In[18]:


col_map = get_cmap("turbo_r").copy()
col_map.set_under("white")
precip_levels = np.arange(100,1200,200.)

fig = plt.figure(figsize=(30,10))
ax = plt.axes(projection=ccrs.PlateCarree())


#Include a ready-to-use colormap with cmap=<colormap_name>
a = clim_prcp_7100.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap=col_map, levels = precip_levels, add_colorbar=False)
d = ds_pop_medi.population.plot.contourf(ax=ax, transform=ccrs.PlateCarree(),levels=[0,500000], colors='none', hatches=['','+++'], add_colorbar=False)

# Hatch color has to be changed afterwards has edgecolor
d.collections[1].set_edgecolor('Black')

# Add a contour for clarity
ds_pop_medi.population.plot.contour(ax=ax, transform=ccrs.PlateCarree(), levels=[500000], colors = 'Black', linewidths=1, add_colorbar=False)

ax.add_feature(cfeature.COASTLINE, linestyle='-')
ax.add_feature(cfeature.BORDERS, linestyle=':');
ax.add_feature(cfeature.OCEAN, zorder=10)

cbar = fig.colorbar(a, ax=ax, fraction = 0.1, label=r'liters per year (mm)')
cbar.ax.tick_params(labelsize=15)
cbar.set_label("Liters per year (mm)", size=18)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='white', alpha=0.5, linestyle='--', zorder=11)
gl.top_labels = False # suppress gridline labels on the top
gl.right_labels = False # suppress gridline labels at the right edge

ax.set_title('')
#ax.set_title('Time:{}'.format(nice_time), loc='right');
ax.set_title('Average Precipitation (1971 - 2000) with populated areas (> 500k) in 2020', fontsize=24)
plt.savefig("/lhome/cra2022/l.quirino.2_2022/Quirino_Leonardo/Project/Precip7100_Pop_2020.png", dpi = 300, bbox_inches="tight",pad_inches=0)


# In[19]:


plt.close()


# In[20]:


col_map = get_cmap("Greens").copy()
col_map.set_under("white")
precip_levels = np.arange(25,500,75.)

fig = plt.figure(figsize=(30,10))
ax = plt.axes(projection=ccrs.PlateCarree())


#Include a ready-to-use colormap with cmap=<colormap_name>
a = season_JJA_prcp_7100.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap=col_map, levels = precip_levels, add_colorbar=False)
d = ds_pop_medi.population.plot.contourf(ax=ax, transform=ccrs.PlateCarree(),levels=[0,500000], colors='none', hatches=['','+++'], add_colorbar=False)

# Hatch color has to be changed afterwards has edgecolor
d.collections[1].set_edgecolor('Black')

# Add a contour for clarity
ds_pop_medi.population.plot.contour(ax=ax, transform=ccrs.PlateCarree(), levels=[500000], colors = 'Black', linewidths=1, add_colorbar=False)

ax.add_feature(cfeature.COASTLINE, linestyle='-')
ax.add_feature(cfeature.BORDERS, linestyle=':');
ax.add_feature(cfeature.OCEAN, zorder=10)

cbar = fig.colorbar(a, ax=ax, fraction = 0.1, label=r'liters per year (mm)')
cbar.ax.tick_params(labelsize=15)
cbar.set_label("Liters per year (mm)", size=18)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='white', alpha=0.5, linestyle='--', zorder=11)
gl.top_labels = False # suppress gridline labels on the top
gl.right_labels = False # suppress gridline labels at the right edge

ax.set_title('')
#ax.set_title('Time:{}'.format(nice_time), loc='right');
ax.set_title('Summer Precipitation (1971 - 2000) with populated areas (> 500k) in 2020', fontsize=24)
plt.savefig("/lhome/cra2022/l.quirino.2_2022/Quirino_Leonardo/Project/SummerPrecip7100_Pop_2020.png", dpi = 300, bbox_inches="tight",pad_inches=0)


# In[21]:


plt.close()


# In[22]:


col_map = get_cmap("Greens").copy()
col_map.set_under("white")
precip_levels = np.arange(25,500,75.)

fig = plt.figure(figsize=(30,10))
ax = plt.axes(projection=ccrs.PlateCarree())


#Include a ready-to-use colormap with cmap=<colormap_name>
a = season_DJF_prcp_7100.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap=col_map, levels = precip_levels, add_colorbar=False)
d = ds_pop_medi.population.plot.contourf(ax=ax, transform=ccrs.PlateCarree(),levels=[0,500000], colors='none', hatches=['','+++'], add_colorbar=False)

# Hatch color has to be changed afterwards has edgecolor
d.collections[1].set_edgecolor('Black')

# Add a contour for clarity
ds_pop_medi.population.plot.contour(ax=ax, transform=ccrs.PlateCarree(), levels=[500000], colors = 'Black', linewidths=1, add_colorbar=False)

ax.add_feature(cfeature.COASTLINE, linestyle='-')
ax.add_feature(cfeature.BORDERS, linestyle=':');
ax.add_feature(cfeature.OCEAN, zorder=10)

cbar = fig.colorbar(a, ax=ax, fraction = 0.1, label=r'liters per year (mm)')
cbar.ax.tick_params(labelsize=15)
cbar.set_label("Liters per year (mm)", size=18)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='white', alpha=0.5, linestyle='--', zorder=11)
gl.top_labels = False # suppress gridline labels on the top
gl.right_labels = False # suppress gridline labels at the right edge

ax.set_title('')
#ax.set_title('Time:{}'.format(nice_time), loc='right');
ax.set_title('Winter Precipitation (1971 - 2000) with populated areas (> 500k) in 2020', fontsize=24)
plt.savefig("/lhome/cra2022/l.quirino.2_2022/Quirino_Leonardo/Project/WinterPrecip7100_Pop_2020.png", dpi = 300, bbox_inches="tight",pad_inches=0)


# In[23]:


plt.close()


# In[24]:


col_map1 = get_cmap("cividis_r").copy()
col_map1.set_under("white")
var_levels = np.arange(100,15000,1000)

fig = plt.figure(figsize=(30,10))
ax = plt.axes(projection=ccrs.PlateCarree())

#Include a ready-to-use colormap with cmap=<colormap_name>
a1 = (season_var_prcp_7100).plot.contourf(ax=ax, transform=ccrs.PlateCarree(), levels=var_levels, cmap=col_map1, add_colorbar=False)
d = ds_pop_medi.population.plot.contourf(ax=ax, transform=ccrs.PlateCarree(),levels=[0,500000], colors='none', hatches=['','+++'], add_colorbar=False)

# Hatch color has to be changed afterwards has edgecolor
d.collections[1].set_edgecolor('Black')

# Add a contour for clarity
ds_pop_medi.population.plot.contour(ax=ax, transform=ccrs.PlateCarree(), levels=[500000], colors = 'Black', linewidths=1, add_colorbar=False)

ax.add_feature(cfeature.COASTLINE, linestyle='-')
ax.add_feature(cfeature.BORDERS, linestyle=':');
ax.add_feature(cfeature.OCEAN, zorder=10)

cbar1 = fig.colorbar(a1, ax=ax, fraction = 0.1, label=r'Montly Variance')
cbar1.ax.tick_params(labelsize=15)
cbar1.set_label("Monthly Variance", size=18)


gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='white', alpha=0.5, linestyle='--', zorder=11)

gl.top_labels = False # suppress gridline labels on the top
gl.right_labels = False # suppress gridline labels at the right edge

ax.set_title('')
#ax.set_title('Time:{}'.format(nice_time), loc='right');
ax.set_title('Seasonal Variance of Precipitation (1971 - 2000) with populated areas (> 500k) in 2020', fontsize=24)
plt.savefig("/lhome/cra2022/l.quirino.2_2022/Quirino_Leonardo/Project/SeasonalVarPrecip7100_Pop_2020.png", dpi = 300, bbox_inches="tight",pad_inches=0)

