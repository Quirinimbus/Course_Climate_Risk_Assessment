#!/usr/bin/env python
# coding: utf-8

# `Aim:` *Notebook for the purpose of Climate Risk Assessment lecture:* `Xarray and Climate Indices`
# 
# `Author:` Yannick Barton
# 
# `Notes:` Remeber `del` command to free up memory when a python object is not used anymore !

# # Imports

# In[ ]:


from IPython.display import Image
import xarray as xr
import xclim as xc


# # Quantiles

# Quantiles are cut points dividing the range of observations into continuous intervals or groups with equal observations.
# 
# There is one fewer quantile than the number of groups created.
# 
# Common quantiles have special names, such as <b>quartiles</b> (four groups), <b>deciles</b> (ten groups), and <b>percentiles</b> (100 groups).

# For example, quantile 0.5 divides the observations into 2 subsets of equal size (50%). It is commonly referred to as the <b>median</b>. It is equivalent to the 50th percentile.
# 
# Quantile 0.9, or the 90th percentile, is the treshold above which the top 10% highest values are located.
# 
# On the other hand, quantile 0.1, or the 10th percentile, is the treshold below which the 10% lowest values can be found.

# In[ ]:


Image(url="https://upload.wikimedia.org/wikipedia/commons/5/5e/Iqr_with_quantile.png")


# Quantiles can be used as a measure of the spread of the data. A common measure for the spread is the <b>interquartile range</b> (IQR).
# 
# IQR is defined as the difference between the upper and lower quartiles (Q3 − Q1) and contains 50% of the data.
# 
# If IQR is large, then the spread of the data is large and we expect a large standard deviation.

# ## Example: comparing precipitation quantiles

# ### Read data

# In[ ]:


# let's read in precipitation data
input_file = '/scratch3/climriskdata/EUR-11N/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/historical/pr/reduced_pr_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1_day_19710101-19751231_LL.nc'

# let's load the data by using open_dataset function of xarray
ds_pr = xr.open_dataset(input_file) 


# In[ ]:


ds_pr # let's have a look at the data inside that file


# In[ ]:


ds_pr.pr.attrs # we need to check the precipitation units before we start


# Interesting, precipitation is given as a flux! Often precipitation data in reanalysis is expressed as a flux, that is in kg m-2 s-1.

# ### Pre-process data

# Let's convert the precipitation flux to daily precipitation rate (mm/day).
# 
# - 1 kg of rain over 1 m-2 is equivalent to 1 mm
# 
# Therefore, to convert to mm/day, one has to multiply the flux currently in seconds by 60 * 60 * 24 = 86400

# In[ ]:


pr_mm = ds_pr.pr * 86400 # we convert the precipitation data to mm/day and store the result in a new Data Array
pr_mm.attrs['units'] = 'mm/day' # it is better to modify the attributes as well


# In[ ]:


pr_mm.isel(time=10).plot() # let's plot the first time step of our variable


# ### Compute the local median (50th percentile)

# In[ ]:


pr_mm.quantile(q=.50)


# Oops! If you don't specify the dimension over which to compute the quantile, you we get a global value for the quantile over the entire domain.

# In[ ]:


# specify the dimension over which to compute any statistical quantity such as quantiles
pr_q50 = pr_mm.quantile(q=.5, dim='time')


# In[ ]:


# we expect a 2D array
pr_q50.shape


# In[ ]:


# compute the median with its function directly (don't forget to specifiy the dimension over which to compute)
pr_median = pr_mm.median(dim='time')


# In[ ]:


# let's plot both results to compare them
xr.concat([pr_q50, pr_median], dim='new').plot(col='new')


# In the figure above, the spatial distribution of the median (50th percentile) of daily rainfall (50% of the data is above/below this threshold) is identical for both methods.

# In[ ]:


# if you find it difficult to read absolute values on a continuous color scale, you can specify n discrete levels
xr.concat([pr_q50, pr_median], dim='new').plot(col='new', levels=7)


# In[ ]:


# you can specify your own array of discrete levels
xr.concat([pr_q50, pr_median], dim='new').plot(col='new', levels=[0,.1,.2,.5,1,2,5])


# ### Compute the IQR (75th - 25th percntile)

# In[ ]:


pr_q25 = pr_mm.quantile(q=.25, dim='time') # 25th percentile
pr_q75 = pr_mm.quantile(q=.75, dim='time') # 75th percentile


# In[ ]:


pr_iqr = pr_q75 - pr_q25# interquartile range (IQR)


# In[ ]:


pr_iqr.plot() # let's plot the IQR


# ### Compare the IQR with the standard deviation

# In[ ]:


pr_std = pr_mm.std(dim='time') # compute the standard deviation; don't forget to specify the dimension


# In[ ]:


xr.concat([pr_iqr, pr_std], dim='new').plot(col='new')


# From the figure above, we observe that the spatial patterns between the IQR and STD are similar. Differences may be related to the skewed distribution of rainfall values.

# # Masking

# Using masking concept allows to transform the data to binary values that are True/False based upon one or multiple conditions. The idea behind masking is to 'mask', hide or ignore data values that do not meet a desired condition.
# 
# Examples:
# 
# - Select only days of a specific season or time period
# 
# - Find days with minimum temperature below 0°C
# 
# - Find days with precipitation sums above the extreme 99th wet percentile
# 
# - ...
# 
# Masking can by applied similarly to time-series as well as multi-dimensional data

# In[ ]:


Image(url="https://climatedataguide.ucar.edu/sites/default/files/styles/node_lightbox_display/public/key_figures_346?itok=7NgR6qEW") 


# Binary files such as masks contain TRUE/FALSE values, but if plotted, as in the example here above, it shows 1 for TRUE and 0 for FALSE !

# ## Example: find the number of extreme rainfall days (> 50 mm)

# In[ ]:


# We re-use the precipitation file that we have previously converted to mm/day
pr_mm


# In[ ]:


temp_mask = pr_mm > 50 # gives true and false values (which is our mask)


# In[ ]:


temp_mask[0,:5,:5] # we can check that we indeed have true/false binary values


# In[ ]:


# we could use the mask to extract data values that are True, however it is not needed for this example
count = temp_mask.sum().values # we simply add up all True values
print('Total number of days, all grid-points confounded, with daily rainfall above 50 mm are {}'.format(count))


# In[ ]:


# but we are interested in the local 'per-grid-point' count of days, so we need to specify to sum over the time dim
temp_mask.sum(dim='time').plot() # Sum up True values and plot the result


# Note that the label on the color bar is wrong since xarray just uses the label from original precipitation file.
# 
# You can pass the following argument to change the label to your taste: cbar_kwargs={"label": "number of days"}

# In[ ]:


# quick customization
temp_mask.sum(dim='time').plot(levels=[0,1,2,5,10,20,50,100,200], cbar_kwargs={"label": "number of days"})


# # A more advanced example: seasonal heavy rainfall thresholds

# Let's apply what we have learned so far about quantiles and masks through a more complex example to determine seasonal heavy (90th percentile) rainfall days. We will use the same precipitation file as above, already converted in mm/day.

# In[ ]:


pr_mm


# ## Select periods of interest

# ### a) using a mask

# In[ ]:


# create a time mask; returns True or False values
time_mask_winter = pr_mm.time.dt.month.isin([12,1,2]) # isin selects timestamps that belong to months 12, 1 and 2
time_mask_spring = pr_mm.time.dt.month.isin([3,4,5]) # isin selects timestamps that belong to months 3, 4 and 5
time_mask_summer = pr_mm.time.dt.month.isin([6,7,8]) # isin selects timestamps that belong to months 6, 7 and 8
time_mask_autumn = pr_mm.time.dt.month.isin([9,10,11]) # isin selects timestamps that belong to months 9, 10 and 11


# In[ ]:


# let's check the masks by plotting them
time_mask_winter.plot()
time_mask_summer.plot()


# In[ ]:


# we apply the mask on the first dimension, since we mask time
pr_DJF_masked = pr_mm[time_mask_winter,:,:]
pr_MAM_masked = pr_mm[time_mask_spring,:,:]
pr_JJA_masked = pr_mm[time_mask_summer,:,:]
pr_SON_masked = pr_mm[time_mask_autumn,:,:]


# In[ ]:


print(pr_mm.shape) # 1826 time steps
print(pr_DJF_masked.shape) # 451 time steps (only autumn)


# ### b) using the built-in groupby function

# In[ ]:


pr_grouped_data = pr_mm.groupby('time.season') # many time-grouping possibilies: 'time.month', 'time.day', ...


# In[ ]:


pr_grouped_data


# ## Determine heavy rainfall thresholds (90th percentile)

# In[ ]:


# compute the 90th percentile for the masked data
pr_DJF_q90_masked = pr_DJF_masked.quantile(.9, dim='time')
pr_MAM_q90_masked = pr_MAM_masked.quantile(.9, dim='time')
pr_JJA_q90_masked = pr_JJA_masked.quantile(.9, dim='time')
pr_SON_q90_masked = pr_SON_masked.quantile(.9, dim='time')


# In[ ]:


pr_DJF_q90_masked


# In[ ]:


# compute the 90th percentile for the grouped data and where rainfall values are at least 1 mm
pr_q90_grouped = pr_grouped_data.quantile(.9, dim='time')


# In[ ]:


pr_q90_grouped # notice that the 90th percentile is computed for each of the 4 seasons separately


# In[ ]:


pr_q90_grouped.sel(season='DJF') # you can select the result for a season with .sel(season='DJF')


# ## Comparison masking vs grouping

# In[ ]:


xr.concat([pr_DJF_q90_masked, pr_JJA_q90_masked, pr_MAM_q90_masked, pr_SON_q90_masked], dim='new').plot(col='new')


# In[ ]:


pr_q90_grouped.plot(col='season')


# ## Saving to NETCDF file

# If you are happy with your results, you can store them to disk as a NETCDF file.
# 
# Sometimes it may be usefull to store intermediate steps to speed up computational time, especially when you are working with large amount of data.

# In[ ]:


# 2D data array containing winter q90 values
pr_DJF_q90_masked


# In[ ]:


# Just like for datasets, you can write data arrays
pr_DJF_q90_masked.to_netcdf("saved_on_disk.nc")


# In[ ]:


# Let's read in the saved data array
ds_disk = xr.open_dataset("saved_on_disk.nc")


# In[ ]:


ds_disk # let's have a look at the data inside that file


# Notice how xarray has automatically converted the data array to a dataset !
# 
# Your data array is now stored as a variable (pr).

# ## Conclusions

# In[ ]:


# a) using masking (has to be computed for each season seperatly)
pr_DJF_q90_masked = pr_mm[ pr_mm.time.dt.month.isin([12,1,2]) ,:,:].quantile(.9, dim='time')
pr_MAM_q90_masked = pr_mm[ pr_mm.time.dt.month.isin([3,4,5]) ,:,:].quantile(.9, dim='time')
pr_JJA_q90_masked = pr_mm[ pr_mm.time.dt.month.isin([6,7,8]) ,:,:].quantile(.9, dim='time')
pr_SON_q90_masked = pr_mm[ pr_mm.time.dt.month.isin([9,10,11]) ,:,:].quantile(.9, dim='time')

# b) using grouping (one line of code)
pr_q90_grouped = pr_mm.groupby('time.season').quantile(.9, dim='time')


# ### Note 1

# The code above computes the all-day 90th percentile.
# 
# You might be interested in the 'wet' percentile, that is considering the non-zero rainfall days of the distibution only!
# 
# Usually, a non-zero rainfall day, or commonly referred to as 'wet day' is defined as a day with at least 1 mm of precipitation.
# 
# Xarray's 'where' function allows you to subset a data array meeting given condition, returning an array with identical dimensions, where values that do not meet the condition are set to missing (nan).
# 
# But careful, 'where' does not do the same thing as masking! The function 'where' returns the actual values that are True whereas a mask only contains True/False values.

# In[ ]:


# compute the 'wet' 90th percentile for the masked data where rainfall values are at least 1 mm
pr_q90_masked = pr_DJF_masked.where(pr_DJF_masked >= 1).quantile(.9, dim='time')


# ### Note 2

# Note that depedening on the research question, it would make more sense to choose a year round threshold instead of a seasonal one. This would be the case if you are interested in the impact relevance of extreme events and want to know when the most extreme events occur throughout the year (and would probably have less events in winter than in summer).

# # XCLIM

# XCLIM is a <b>library of functions to compute climate indices</b> from observations or model simulations. It is built using xarray. Its objective is to make it as simple as possible for users to compute indices from large climate datasets and for scientists to write new indices with very little boilerplate.
# 
# XCLIM currently provides <b>over 50 indices</b> related to mean, minimum and maximum daily temperature, daily precipitation, streamflow and sea ice concentration as well as ICCLIM climate indices part of the European Climate assessment project.
# 
# For general information: https://pypi.org/project/xclim/
# 
# A list of ICCLIM climate indices (recommended tu be used): https://xclim.readthedocs.io/en/stable/indicators_api.html#icclim-indices
# 
# Examples:
# 
# - Maximum number of consecutive dry days
# - Maximum number of consecutive frost days (Tn < 0℃)
# - Extreme intra-period temperature range
# - Frost days index
# - Growing degree-days over threshold temperature value
# - Heating degree days
# - Number of ice/freezing days
# - Accumulated total (liquid and/or solid) precipitation
# - Wet days
# - Number of wet days with daily precipitation over a given percentile
# - Highest 1-day precipitation amount for a period (frequency)
# - Highest precipitation amount cumulated over a n-day moving window
# - Average daily precipitation intensity
# - Number of summer days
# - Tropical nights
# - Warm spell duration index
# - ...
# 

# ## Example: Number of very hot days (> 30 °C) using XCLIM

# For this example, we are going to use historical daily maximum temperatures.

# ### Read data

# In[ ]:


# let's read in precipitation data
input_file = '/scratch3/climriskdata/EUR-11N/MPI-M-MPI-ESM-LR_MPI-CSC-REMO2009_v1/historical/tasmax/reduced_tasmax_EUR-11_MPI-M-MPI-ESM-LR_historical_r1i1p1_MPI-CSC-REMO2009_v1_day_19710101-19751231_LL.nc'

# let's load the data by using open_dataset function of xarray
ds_tasmax = xr.open_dataset(input_file) 


# In[ ]:


ds_tasmax # let's have a look at the data inside that file


# In[ ]:


ds_tasmax.tasmax.attrs # let's check the temperature units


# ### Convert from Kelvin to Celsius

# #### a) manually

# In[ ]:


# let's convert to Celsius
tasmax_degC = ds_tasmax.tasmax - 273.15 # store the result as a new Data Array
tasmax_degC.attrs['units'] = 'degC' # we also modify the attributes manually


# In[ ]:


tasmax_degC.attrs


# #### a) using xclim's built-in function

# In[ ]:


tasmax_degC_xclim = xc.units.convert_units_to(ds_tasmax.tasmax, 'degC')


# In[ ]:


tasmax_degC_xclim.attrs


# So xclim automatically corrects the unit in the metadata as well!
# 
# [More examples in the documentation of xclim](https://xclim.readthedocs.io/en/stable/notebooks/units.html)

# In[ ]:


# let's quickly plot a random time step of our temperature variable to compare manual and xclim unit conversion
xr.concat([tasmax_degC.isel(time=160), tasmax_degC_xclim.isel(time=160)], dim='new').plot(col='new')


# ### Compute number of days > 30°C

# #### a) manually using masking

# In[ ]:


# recall tu usage of masking introduced above
temp_mask = tasmax_degC > 30 # create mask for temperatures above 30°C
number_hot_days_m1 = temp_mask.sum(dim='time') # sum up the True values


# In[ ]:


number_hot_days_m1.plot() # plot result


# #### b) using xclim's built-in function

# ICCLIM's xc.icclim.SU(tasmax) computes the number of summer days (default thresh: '25.0 degC').
# We use xc.indices.tx_days_above(tasmax, thresh), which let's us choose the threshold.
# Notice the string format for the threshold.

# In[ ]:


get_ipython().run_cell_magic('html', '', '<iframe src="https://xclim.readthedocs.io/en/stable/indices.html#xclim.indices.tx_days_above" width="950" height="500"></iframe>')


# In[ ]:


number_hot_days_m2 = xc.indices.tx_days_above(tasmax_degC_xclim, '30.0 degC') # change the default treshold from: '25.0 degC'


# In[ ]:


number_hot_days_m2 # let's see the result


# Note that xclim returns the number of hot days for each year by default. Hence time is now 5. This is the case for most xclim climate indices.

# In[ ]:


number_hot_days_m2 = number_hot_days_m2.sum(dim='time') # we sum the result over the 5 years


# In[ ]:


# we expect a 2D array
number_hot_days_m2.shape


# In[ ]:


# let's plot results to see whether xclim gives sames results as above with using masking
xr.concat([number_hot_days_m1, number_hot_days_m2], dim='new').plot(col='new')


# In[ ]:


# quick customization
xr.concat([number_hot_days_m1, number_hot_days_m2], dim='new').plot(col='new',
                                                                    levels=[0,1,2,5,10,20,50,100,200,500],
                                                                    cbar_kwargs={"label": "number of days"})


# ### Important note

# Note that xclim checks the units from your data's attributes. As long as you keep the units correct in the original file, xclim will automatically handle unit conversion. Let's test it together.

# In[ ]:


tasmax_degK = ds_tasmax.tasmax # let's take the original temperature file in Kelvin


# In[ ]:


tasmax_degK.attrs


# In[ ]:


number_hot_days_K = xc.indices.tx_days_above(tasmax_degK, '30.0 degC').sum(dim='time')


# In[ ]:


# Comparison between the 3 possible methods
xr.concat([number_hot_days_m1, number_hot_days_m2, number_hot_days_K], dim='new').plot(col='new',
                                                                    levels=[0,1,2,5,10,20,50,100,200,500],
                                                                    cbar_kwargs={"label": "number of days"})


# <br>
# <br>
# <br>
# <br>
# <h1><center>Thank you for your attention !</h1></center>
# <h1><center>Questions?</h1></center>
