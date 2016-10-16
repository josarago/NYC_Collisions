import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sb
import datetime as dt


#import mpld3
#mpld3.enable_notebook()

filepath ='/Users/jonathansaragosti/Documents/Open Data/NYPD_Motor_Vehicle_Collisions.csv'

Names = ['DATE', 'TIME', 'BOROUGH', 'ZIP_CODE', 'LATITUDE', 'LONGITUDE', 'LOCATION',
         'ON_STREET_NAME', 'CROSS_STREET_NAME', 'OFF_STREET_NAME', 'NUMBER_OF_PERSONS_INJURED',
         'NUMBER_OF_PERSONS_KILLED', 'NUMBER_OF_PEDESTRIANS_INJURED', 'NUMBER_OF_PEDESTRIANS_KILLED',
         'NUMBER_OF_CYCLIST_INJURED', 'NUMBER_OF_CYCLIST_KILLED', 'NUMBER_OF_MOTORIST_INJURED',
         'NUMBER_OF_MOTORIST_KILLED', 'CONTRIBUTING_FACTOR_VEHICLE_1', 'CONTRIBUTING_FACTOR_VEHICLE_2',
         'CONTRIBUTING_FACTOR_VEHICLE_3', 'CONTRIBUTING_FACTOR_VEHICLE_4', 'CONTRIBUTING_FACTOR_VEHICLE_5',
         'UNIQUE_KEY','VEHICLE_TYPE_CODE_1', 'VEHICLE_TYPE_CODE_2', 'VEHICLE_TYPE_CODE_3', 'VEHICLE_TYPE_CODE_4',
         'VEHICLE_TYPE_CODE_5']


DATASET = pd.read_csv(filepath, skipinitialspace=True)


dead = DATASET.NUMBER_OF_PERSONS_KILLED.nonzero()
Dead = dead[0]
print(str(Dead.size) + ' collisions resulting in killed persons')



plt.scatter(DATASET.LONGITUDE,DATASET.LATITUDE, marker='.')
plt.scatter(DATASET.LONGITUDE[Dead],DATASET.LATITUDE[Dead],c='red',marker='o')
#plt.xlim(-74.1,-73.9)
#plt.ylim(40.6,40.8)
plt.show()



print('total number of collisions: ' + str(DATASET.DATE.count()))


print(str(np.sum(DATASET.NUMBER_OF_PERSONS_KILLED))+' people killed over 3 years')
print('among which: '+ str(np.sum(DATASET.NUMBER_OF_MOTORIST_KILLED))+ ' were in a motorized vehicle')
print('             '+ str(np.sum(DATASET.NUMBER_OF_PEDESTRIANS_KILLED))+ ' were pedestrians')
print('             '+ str(np.sum(DATASET.NUMBER_OF_CYCLIST_KILLED))+ ' were cyclists')


## time array for plot
timearray = np.zeros(DATASET.TIME.count())
count = -1
for thistime in DATASET.TIME:
    count = count + 1
    thattime = thistime.split(":")
    # print(thattime)
    # #print(float(thattime[0])+float(thattime[1])/60)
    timearray[count] = float(thattime[0]) + float(thattime[1]) / 60

print('timearray done')


# to make sure the kernel-density estimate behaves on the edges of the data set,
# we artificially make the data periodical:
dt = np.ones(np.size(timearray))*24
Timearray = np.concatenate([timearray, timearray-dt])
Timearray = np.concatenate([Timearray, timearray+dt])


# hour of the day histogram plot
sb.distplot(Timearray, bins=120)
plt.show()

plt.xlim(0, 24)
plt.xticks(np.arange(25))
print("done")

## let's get a datetime
catDate = DATASET.DATE + ' ' + DATASET.TIME
print(catDate)

YA = [dt.datetime.strptime(x, '%m/%d/%Y %H:%M') for x in catDate]
print('done')

DATASET.fldt = YA[0]