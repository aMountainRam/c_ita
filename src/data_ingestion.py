import os
import datetime
import pandas as pd

# set begin data
begin_date = datetime.date(2020,2,24)
today = datetime.date.today()
# with a delta of: 
delta_days = today - begin_date

def data_ingestion( main_path ):
    # get some folder paths
    path_to_data = main_path + '/COVID-19/dati-province'
    # check the data file list
    list_data_files = os.listdir(path_to_data)
    
    # Data ingestion
    root_file_name = ''
    ext = '.csv'
    n_files = 0
    # count files and exclude a file which is an extra
    # plus this routine saves in list_data_files the absolute paths
    for file in list_data_files:
        if( file != 'dpc-covid19-ita-province.csv' and file != 'dpc-covid19-ita-province-latest.csv' ):
            file_path = path_to_data + '/' + file
            n_files += 1
        if(file == 'dpc-covid19-ita-province.csv'):
            root_file_name = file[:-4] + '-'    # here it removes extension
                                                # and returns the root of the names

    this_day = begin_date
    data_array = []  # creates the data dictionary
    data_array_ticks = []  # and this array serves the plot ticks
    for day in range(0,n_files):  # files are scanned by date since date is present in the filename
        day_two_digits = '{:02d}'.format(this_day.day)          # Converts day to a fixed two digit string
        month_two_digits = '{:02d}'.format(this_day.month)    # and similarly for months
        date_string = str(begin_date.year) + month_two_digits + day_two_digits   # name_file is added to this string
        this_path = path_to_data + '/' + root_file_name + date_string + ext      # and path location
        data_array_ticks.append( day_two_digits + '/' + month_two_digits )
        data_array.append( pd.read_csv(this_path,encoding='latin-1',header=0) )  # everything is appendend in an array of DFs
        this_day = this_day + datetime.timedelta(days=1)
    # each day can be reached through the day count 
    # with 0 being the 24 of Feb 2020
    # USE converter to move from one to the other
    province = {}
    filtered_provs = data_array[18].filter(['sigla_provincia','denominazione_provincia'])
    #print(filtered_provs)
    for index, row in filtered_provs.iterrows():
        if ( len(str(row['sigla_provincia'])) == 2 ):
            province.update( { row['sigla_provincia'] : row['denominazione_provincia'] } )   
    
    #print(province)    
        #cleaned_provs = [ p for p in provs if str(p) != 'nan' ]
        #provs = cleaned_provs    
    
    return n_files, province, data_array, data_array_ticks

def data_ingestion_france( main_path ):
    path_to_data = main_path + '/FRANCE-COVID-19'
    file_contagion = path_to_data + '/' + 'france_coronavirus_time_series-confirmed.csv'
    file_dead = path_to_data + '/' + 'france_coronavirus_time_series-deaths.csv'
    data_france_contagion = pd.read_csv(file_contagion,encoding='utf-8',delimiter=';',na_values='NaN')
    data_france_dead = pd.read_csv(file_dead,encoding='utf-8',delimiter=';',na_values='NaN')
    return data_france_contagion, data_france_dead

def num_to_date( num ):
    date = begin_date + datetime.timedelta(days=1)
    day_date = date.day
    month_date = date.month
    year_date = date.year
    return datetime.date(year_date,month_date,day_date)

def date_to_num( date ):
    delay = date - begin_date
    return int(delay.days)
