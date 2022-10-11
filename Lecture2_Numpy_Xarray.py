#!/usr/bin/env python
# coding: utf-8

# `Aim:` *Notebook for the purpose of Climate Risk Assessment lecture:* `Xarray, Numpy and Error Handling`
# 
# `Author:` Mubashshir Ali with additions by Martin Aregger

# ## What is Numpy and why do we need it?

# `Numpy` is considered the "fundamental package for scientific computing in Python". It is a Python library that provides a multidimensional array object, various derived objects (such as masked arrays and matrices), and an assortment of routines for fast operations on arrays, including mathematical, logical, shape manipulation, sorting, selecting, I/O, discrete Fourier transforms, basic linear algebra, basic statistical operations, random simulation and much more.

# Everything we do today is also possible without Numpy, it would just be more time consuming and significantly more difficult! Additonally, the code in numpy has been optimized by the community and it is very efficient.

# In[2]:


import numpy as np


# ## The Numpy Array

# In the last lecture we looked at different basic datatypes. You may have noticed that we did not have a "multidimensional" datatype. Only Lists, Tuples, Sets and Dictionaries. If we want to store multidimensional data with the base python we have to put lists into lists:

# In[3]:


a = [0,1,2,3,4] # This is a 1-dimensional array
b = [7,8,0,1,3] 

c = [a,b]
c


# This works well if you are doing simple calculations in a low dimensional space. However, if you want to go into higher dimensions and do complex matrix computations it becomes impractical quickly. That is where Numpy has its strengths:

# In[ ]:


import IPython.display as display # This is a convenient packagae which allows us to show websites within a jupyter notebook
display.Image(url= "https://fgnt.github.io/python_crashkurs_doc/_images/numpy_array_t.png")


# ## Creating Numpy arrays

# Below we reproduce four numpy arrays, three of which having the same dimensions as in the above picture and one with four dimensions (we could go on and on with dimensions). 
# <br>
# Note that we use four different methods to generate such arrays: all ones, all zeros, random numbers between 0 and 1 and random integers.

# ### 1. Initialize an array of arbitrary dimension.

# In[4]:


np.ones(shape=(4,)) # a 1-dimensional array filled with ones


# In[5]:


np.zeros(shape=(2,3))#two rows, three columns


# In[6]:


np.random.random((4,3,2))


# In[7]:


np.random.randint(2, 10, size=(2,4,3,2))   # random integers from 2 to 10


# harder to visualize? think that the $4^{th}$ dimension is time. So we have two 3D blocks like the in the figure above at two different time steps.

# ### 2. Use lists.

# In[9]:


a = [1,2,3,4,5,6]


# In[10]:


## to create a numpy array of the above list a just call np.array(a)
b = np.array(a)
## or directly give the list into numpy array function
c = np.array([1,2,3,4,5,6])
c


# ### 3. Subsequent numbers with a given step

# In[11]:


start=0
end=10
step=2.5

np.arange(start,end,step)


# ### 4. Subsequent n numbers

# Another useful way to create an array is when we want a given amount of number between a given range
# 
# Example: if we need 50 numbers between 0-10

# In[12]:


start=0
end=10
n = 50

np.linspace(start,end,n)


# ## Array attributes

# In[14]:


arr=np.random.random((4,3,2))


# In[15]:


arr.ndim    # number of dimensions


# In[16]:


arr.shape  # number of elements in each dimension


# In[17]:


arr.size  # overall size, i.e. total number of elements (just the product of the amount of elements in each dimension)


# In[18]:


arr.dtype # types of array elements.


# If elements are of different type (e.g. you have got intengers and strings), you need to be careful when performing operations

# In[19]:


c = np.array([1.,2,3,4.,5, 'c'])
c.dtype


# In[20]:


c[0]


# The first element is *not* read as number

# ## Slicing and indexing:

# Pretty much has we have seen before. However, here we may deal with multiple dimensions.

# In[21]:


arr=np.random.random((4)) # 1D array
arr


# In[22]:


arr[:2]  # in 1D is just like before


# In[23]:


arr=np.random.random((4, 2)) # 2D array
arr


# Just specify what elements to pick along each dimension. In 2D, just read it as: array[rows, columns]
# <br>
# If you want to take all elements of the first two rows:

# In[24]:


arr[0:2, :] # remember, index starts at 0 and slicing will give you all elements within the slice, not the last index


# which is equivalent to:

# In[ ]:


arr[0:2,]


# or even:

# In[ ]:


arr[0:2]


# However, omitting rows is not allowed:

# In[26]:


arr[,0:2]


# Higer-dimensional arrays follow the same principle:

# In[25]:


arr=np.random.random((4, 2, 5)) # 2D array
arr


# In[27]:


arr[-1, :, 2:4] # last "block" (-1), all rows (:) in the third and fourth columns (2:4)


# ## Copying array

# **Very important.** Whenever in python you have a variable *a* and you do something like:
a=b #It makes apointer meaning it goes back to element a
# what you might think you are doing is that you create a variable called *b* with the same value of the varaible *a*. However, what you are actually doing is creating a variable *b* which is identitical to *a*. So if you change *b* you also change *a*. Not being aware of this can easily mess up your code.

# In[29]:


a=np.array([1,2,3])
b=a
a


# In[30]:


b[2] = 50


# In[31]:


a


# Unless the above is in fact intended, what you might instead do is assigning to *b* a *copy* of *a*:

# In[32]:


a=np.array([1,2,3])
b=a.copy()   # assing a copy


# In[33]:


b[2] = 50


# In[34]:


a


# ## Reshape arrays

# You can easily reshape arrays (i.e. from 2D to 1D), as along as you preserve the size, i.e. the total number of elements.

# In[35]:


arr=np.random.random((4, 2)) # 2D array
arr


# In[36]:


arr.reshape(8)


# In[37]:


arr.reshape(2,2,2)


# ## Operations with arrays

# In[38]:


a=np.array([[1,2,3],
            [4,5,6]])
a


# In[39]:


a.max() # overall max - same with min


# In[40]:


a.max(axis=0) # column-wise max - same with min


# In[41]:


a.max(axis=1) # row-wise max - same with min


# In[42]:


a.sum() # overall sum


# In[43]:


a.sum(axis=0) # column-wise sum


# In[44]:


a.sum(axis=1) # row-wise sum


# In[45]:


a.mean()  # overall sum - and you can also get it row-wise or column-wise as above


# Between two arrays:

# In[53]:


b=np.array([[1,2,3],
            [4,5,6]])*2
b


# In[54]:


np.add(a,b) # add two arrays element wise


# In[55]:


np.subtract(a,b) # subtract two arrays element wise


# In[56]:


print(a)
print(b)
np.multiply(a,b) # multiply two arrays element wise


# The three above also work between two vectors of different dimensions, as long as one dimension is the same:

# In[57]:


print(a[0])
print(b)
np.multiply(a[0],b)


# In[58]:


np.add(a[0],b)


# In[59]:


np.subtract(b,a[0])


# .. and what about the cross-product? Use a .dot(). Here the order matters, obviously.

# In[61]:


b.dot(a[0])  # b(2,3) X a[0](3,1) vector product


# ## Find element in array and array concatenation:

# A nice function is where()

# In[62]:


a=np.array([[1,2,3],
            [4,5,6]])
a


# In[67]:


np.where(a == 6)
#print(a)


# it gives back the positions at which the array meets the specified condition

# In[64]:


a[1,2]# remember counting starts at 0


# In[68]:


np.where(a != 6)


# Sometimes it is needed to concatenate arrays.

# In[69]:


a


# In[70]:


b


# In[71]:


np.concatenate([b,a], axis=0) # concatenate vertically - equivalent to np.vstack


# In[72]:


np.concatenate([b,a], axis=1) # concatenate horizontally - equivalent to np.hstack


# # Xarray

# The numpy arrays are very useful for any calculations you might want to do with data in a gridded format. However, especially with climate model data you usually have not only the data but also attributes on top of it such as coordinates. It gets even more complicated if you have more than one variable for each coordinate. You could just put the addtional attributes into a new dimension of your numpy array but there is a more convenient way.  We will use a python library called `xarray` which is specifically designed to make our life easier to handle multi-dimensional data.

# Lets import the libary as an alias

# In[73]:


import xarray as xr # xr is, like np for numpy, considered a "standard" alias
# library to work with climate model data format


# In[74]:


from IPython.display import Image
Image(url='http://xarray.pydata.org/en/stable/_images/dataset-diagram.png')


# This is how a multi-dimensional dataset looks like.

# ## Xarray Dataset

# Climate data is usually stored in the `NetCDF` format. We can use `Xarray` to easily open such a NetCDF file.

# In[77]:


# file to be plotted
# Adapt it as per your need

file1 = '/scratch3/climriskdata/EUR-11N/ICHEC-EC-EARTH_SMHI-RCA4_v1/rcp85/tas/reduced_tas_EUR-11_ICHEC-EC-EARTH_rcp85_r12i1p1_SMHI-RCA4_v1_day_20710101-20751231_LL.nc'


# In[78]:


# lets load the data by using open_dataset function of xarray

ds1 = xr.open_dataset(file1)
ds1


# ------------------------------------------------------------------------------------
# Here, you can see one of the reasons why `NetCDF` format is used. It presevers the metadata like standard name, units etc.
# 
# What are the dimensions of the tas variable? 
# 
# `Note:` If your data file has only one variable then one can also use `xr.open_datarray()` to open the file 

# ## DataArray/Data variables

# Data Array is the actual data which the dataset holds. It can be a N-D numpy array. A dataset can hold multiple data variables. 
# 
# We see that this dataset has variables called `time_bnds` and `tas`

# Every `DataArray` contains:
#     
# * `dimensions`: Eg, lat, lon, time
# * `coordinates`: labels of each point in the form of a Python-dictionary
# * `attributes`: Metadata

# ## Difference between dimensions and coordinates

# Coordinates are labels to your dimensions. This will be more clear when we look at selecting data examples

# ## DataArray properties

# In[84]:


ds1.tas.name


# In[80]:


ds1.tas.data


# In[81]:


ds1.tas.dims


# In[82]:


ds1.tas.coords


# In[83]:


ds1.tas.attrs


# ## Different Ways of Selecting Data
# 
# Basic positional based indexing same as in numpy works, but one has to know the specific position to extract the data

# In[85]:


ds1.tas[0,1,1] # gives the time=0, lat=1, lon=1 position respectively


# In[87]:


# index style selecting; isel -> index selection
ds1.tas.isel(time=0)


# ---------------------------------------------------------------------------------------
# Another easy way to select the data by specifying the date as a string using `sel` method. This is label based selection which is possible thanks to `coordinates` in our data. It works on the principle of python dictionaries.

# In[88]:


ds1.tas.sel(time='2071-05-15 12:00') # sel -> selection function


# In[90]:


# assigning a variable name to our data for easy access
data_to_plot = ds1.tas.sel(time='2071-05-15 12:00')


# In[91]:


# ploting it, just one line
data_to_plot.plot()


# Here, **we see how xarray makes our life so much easier for quick analysis.** We didn't have to specify a map or axis. It does everything intelligently in the background for us. This saves a lot of time for analysis.

# This is just one of the many powerful features which xarray offers.
# 
# **You can also do everything above in just one line using Python's powerful Object-oriented language features** 

# In[92]:


# selecting and plotting the data in one line
ds1.tas.isel(time=0).plot(); # add semicolon to suppress text output, depends on individual taste


# In[97]:


# selecting lat, lon values
# quick time series plot for Bern
ds1.tas.sel(lat=46.9, lon=7.4, method='nearest').plot();


# ### Multiple plots

# In[98]:


## first we select data to plot
## we can select multiple time-steps using slice function
temp = ds1.tas.sel(time=slice('2071-05-15', '2071-05-18' ))
temp # print preview of our data


# __Since, we have 4 time steps, we can plot it in a _2x2_ fashion__

# In[99]:


temp.plot(col='time',col_wrap=2); # colwrap puts it in 2x2 instead 4x1


# ## Calling-basic numpy functions

# In[101]:


ds1.tas.min()


# In[102]:


ds1.tas.max()


# In[103]:


# applying along a specific dimension
ds1.tas.min(dim='time')


# In[104]:


ds1.tas.min(dim='time').plot()


# **These numpy functions are also now directly supported in the latest xarray version**

# In[105]:


np.min(ds1.tas)


# ## Modyfying values inplace

# In[108]:


# changing into deg Celsius
ds1.tas.values = ds1.tas.values - 273.15


# Be careful when modifying data like that because the metadata says temperature is in Kelvin. So let's correct the meta data

# In[109]:


ds1.tas.attrs


# In[111]:


ds1.tas.attrs['units'] = 'degC'


# In[112]:


ds1.tas.attrs


# In[113]:


# check again
ds1.tas


# In[123]:


# To avoid confusion save it as a separate variable when you modify things inplace

tas_in_degC = ds1.tas - 273.15


# In[124]:


# now the new variable is just an xarray dataarray
type(tas_in_degC)


# In[125]:


type(ds1)


# ## Saving file to disk

# Once you have your `data_to_plot` file, it is better to save the file to disk especially if the calculations to produce the file took a while.
# 

# In[126]:


data_to_plot


# In[121]:


# use this command to find your current directory
get_ipython().system('pwd')


# In[129]:


out_file = '/lhome/cra2022/l.quirino.2_2022/Quirino_Leonardo/data_to_plot.nc' # change it to your directory
data_to_plot.to_netcdf(out_file)


# # Common Error Handling

# ## Name error

# In[131]:


#ds


# ## Key Error

# In[132]:


#ds1.sel(time='2000-01-01') , this error usually mean this value dosen't existe


# ## Value error

# In[133]:


int(4.5)


# In[135]:


#int("cat")  Value errores usually come when you are not wokring properly with a data


# In[137]:


#xr.open_dataarray(file1) wrong open function


# ## Type Error
# 
# Common cause can be calling an object which is not a function.

# In[139]:


#ds1.tas() #calling a function that is not a funciton


# ## Index Error

# In[140]:


#ds1.tas[0,2,22345] #calling a index that does not exist


# ## Dealing with Errors
# 
# * Carefully read the stack trace!
# * Asking Google for help
# * Looking up on stackoverflow for FAQs
# 

# # Closing and deleting dataset

# In[141]:


ds1.close()


# It will only delete ds1 variable, it won't delete the original data stored on disk. Note: Xarray never modifies original data on the disk in all the operations we looked above. 

# In[142]:


ds1


# In[143]:


del ds1 


# In[144]:


ds1


# # Exercises

# You are given the output of a climate model in the form of a csv file. The the data is supposed to contain 3 days of daily precipitation data for a 10*10 pixel area over Bern. First we read the data:

# In[ ]:


# This is an example of how you can read a csv file
import csv
input_list = []
with open("cra2022_shared/ex2_data.csv", newline="") as file:
    reader = csv.reader(file, delimiter = ',')
    for row in reader:
        input_list.append(row)
        
input_list = [element[0] for element in input_list] # The csv reader gives us a list of strings which we convert to floats here


# Now we have the model data in the form of a one-dimensional list which is rather inconvenient. It would be easier to interpret if we had it in the form of a 3d-array. Can you create an appropriate array from the list? (Hint: the data is ordered with the values of each row appended and then the values of each day appended)

# In[ ]:


# your code here


# Now that we have a nice 3d-array lets look at the data. First let's check what datatype the values have:

# In[ ]:


# your code here


# If we want to do any calculations this datatype will not work. Can you convert it into a more useful one? (Hint: we'd like to have a "float64" datatype)

# In[ ]:


# your code here


# Ok, now that we have numeric values let's see what the maximum measured precipitation was:

# In[ ]:


# your code here


# Now this value looks a bit weird for precipitation. The unit is actually $kg*m^{-2}*s^{-1}$ averaged for the whole day. Let's convert the data into a more easily interpretable unit. Can you calculate the number of daily $mm*m^{-2}$ which fell for each pixel?

# In[ ]:


# your code here


# Now let's find the maximum value again. Can you figure out on which day the highest precipitation sum was measured? (Hint: look at the "where" function in numpy.)

# In[ ]:


# your code here


# While the daily maxima are interesting, we are actually even more interested in the 3 day precipitation mean for that pixel. Can you calculate it?

# In[ ]:


# your code here


# Now finally, can you figure out the total precipitation (in $m^3$) which fell in this pixel and all it's adjacent pixels over the 3 days? Let's assume that each pixel has an area of 1 $km^2$.
# 
# (Hint: Since the pixel is at the edge (as we can see in the previous exercise) of our $10*10$ grid we should select a $2*3$ area for all 3 days.)

# In[ ]:


# your code here


# Now playing around with this small model output was fun but we'd like to look at a bit more data. You can find the full model output in this NetCDF file: '/scratch3/climriskdata/EUR-11S/ICHEC-EC-EARTH_CLMcom-CCLM4-8-17_v1/rcp85/pr/pr_EUR-11_ICHEC-EC-EARTH_rcp85_r12i1p1_CLMcom-CCLM4-8-17_v1_day_20210101-20211231_LL.nc'. Let's open it:

# In[ ]:


# your code here


# Can you figure out what the dataset contains? Which timeframe do we have? When was it created? What's the title of the dataset?

# In[ ]:


# your code here


# Again the units are in $kg*m^{-2}*s^{-1}$. Can you convert the dataset to total daily $mm*m^{-2}$ and also adapt its metadata?

# In[ ]:


# your code here


# Now can you find on what day the Bern had the maximum precipitation accumulation? (Bern is located at 46.9480° N, 7.4474° E) (Hint: You may need to google for the correct function.)

# In[ ]:


# your code here


# Now let's see how the precipitation looked over switzerland on that day. Can you plot it?

# In[ ]:


# your code here


# Can you also add the previous and the following day to your plot? Can you arrange them vertically, each plot above another?

# In[ ]:


# your code here


# To finish up: can you properly close the dataset and delete all the xarray objects?

# In[ ]:


# your code here

