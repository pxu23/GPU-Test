import datetime

## start of season
start_month = 4
start_day = 8

## end of season
end_month = 9
end_date = 11
year = 2022

## the days of each month that the High A Central Season runs from
April_days = [datetime.datetime(year,4,day) for day in range(start_day,31)]
May_days = [datetime.datetime(year,5,day) for day in range(1,32)]
June_days = [datetime.datetime(year,6,day) for day in range(1,31)]
July_days = [datetime.datetime(year,7,day) for day in range(1,32)]
August_days = [datetime.datetime(year,8,day) for day in range(1,32)]
September_days = [datetime.datetime(year,9,day) for day in range(1,end_date + 1)]

## all the dates in the High A Central baseball season
all_dates = April_days + May_days + June_days + July_days + August_days + September_days

## number of days in season
num_days = len(all_dates)
#%%
