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

ds_pr = xr.open_dataset(pr_file).sel(lat=slice(30,45))

ds_pr

#ds_tas_current = xr.open_dataset(current_file).sel(time=slice('1996', '2000'), 
#                                                   lat=slice(44,48), lon=slice(5,11))


# In[3]:


#pr_mm = ds_pr.pr * 86400
#pr_mm.attrs['units'] = 'mm/day'
#prcp_7100 = pr_mm.sel(lat=slice(30,45))

#prcp_7100

pr_mm = xc.units.convert_units_to(ds_pr.pr, 'mm/day')


# In[4]:


#pr_mm
consec_wet = xc.indicators.icclim.CWD(pr_mm) #.icclim.ID(prcp_7100)
consec_dry = xc.indicators.icclim.CDD(pr_mm) #.icclim.ID(prcp_7100)


# In[5]:


#ROME, ITA
consec_dry_rome = consec_dry.sel(lat='41.893333',lon='12.482778', method='nearest')
#consec_dry_rcp85_rome = consec_dry_rcp85.sel(lat='41.893333',lon='12.482778', method='nearest')

#MADRID, SPA
consec_dry_madrid = consec_dry.sel(lat='40.416667',lon='-3.7025', method='nearest')
#consec_dry_rcp85_madrid = consec_dry_rcp85.sel(lat='40.416667',lon='-3.7025', method='nearest')

#CAIRO, EGY
consec_dry_cairo = consec_dry.sel(lat='30.044444',lon='31.235833', method='nearest')
#consec_dry_rcp85_cairo = consec_dry_rcp85.sel(lat='30.044444',lon='31.235833', method='nearest')


# In[6]:


mu_rome = consec_dry_rome.mean('time') # mean of distribution
sigma_rome = consec_dry_rome.std('time') # standard deviation of distribution
#consec_dry_rome.var('CDD')#.number_of_days_with_lwe_thickness_of_precipitation_amount_below_threshold


# In[7]:


mean_cdd = consec_dry.sum('time')/30

mean_cdd.plot()


# In[8]:


ds_pop_medi = xr.open_dataset('/lhome/cra2022/climriskdata/EUR-11S/Estimated_population/Estimated_population_2020_LL.nc').sel(lat=slice(30,45))
#ds_pop_medi = ds_pop.sel(lat=slice(30,45))


# In[9]:


col_map = get_cmap("inferno_r").copy()
#col_map.set_under("white")
precip_levels = np.arange(25,200,25)

fig = plt.figure(figsize=(30,10))
ax = plt.axes(projection=ccrs.PlateCarree())


#Include a ready-to-use colormap with cmap=<colormap_name>
a = mean_cdd.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), cmap=col_map, levels = precip_levels, add_colorbar=False)
d = ds_pop_medi.population.plot.contourf(ax=ax, transform=ccrs.PlateCarree(),levels=[0,500000], colors='none', hatches=['','+++'], add_colorbar=False)

# Hatch color has to be changed afterwards has edgecolor
d.collections[1].set_edgecolor('Gray')

# Add a contour for clarity
ds_pop_medi.population.plot.contour(ax=ax, transform=ccrs.PlateCarree(), levels=[500000], colors = 'Black', linewidths=1, add_colorbar=False)

ax.add_feature(cfeature.COASTLINE, linestyle='-')
ax.add_feature(cfeature.BORDERS, linestyle=':');
ax.add_feature(cfeature.OCEAN, zorder=10)

cbar = fig.colorbar(a, ax=ax, fraction = 0.1, label=r'Consecutive Dry Days')
cbar.ax.tick_params(labelsize=15)
cbar.set_label("Consecutive Dry Days", size=18)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='white', alpha=0.5, linestyle='--', zorder=11)
gl.top_labels = False # suppress gridline labels on the top
gl.right_labels = False # suppress gridline labels at the right edge

ax.set_title('')
#ax.set_title('Time:{}'.format(nice_time), loc='right');
ax.set_title('Average Consecutive Dry Days (1971 - 2000) with populated areas (> 500k) in 2020', fontsize=24)
plt.savefig("/lhome/cra2022/l.quirino.2_2022/Quirino_Leonardo/Project/CDD7100_Pop_2020.png", dpi = 300, bbox_inches="tight",pad_inches=0)

