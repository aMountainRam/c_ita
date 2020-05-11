import os
import datetime
import pandas as pd
class National:
    main_path = ''
    data_path = ''
    data = []
    begin_date = datetime.date(2020,2,24)
    def __init__( self, main_path ):
        self.main_path = main_path
        self.data_path = main_path + '/' + 'COVID-19/dati-andamento-nazionale'
        
    def ingestion(self):
        # check the data file list
        list_data_files = os.listdir( self.data_path )
        
        # Data ingestion
        root_file_name = ''
        ext = '.csv'
        n_files = 0
        # count files and exclude a file which is an extra
        # plus this routine saves in list_data_files the absolute paths
        for file in list_data_files:
            if( file != 'dpc-covid19-ita-andamento-nazionale.csv' 
               and file != 'dpc-covid19-ita-andamento-nazionale-latest.csv' ):
                file_path = self.data_path + '/' + file
                n_files += 1
            if(file == 'dpc-covid19-ita-andamento-nazionale.csv'):
                root_file_name = file[:-4] + '-'    # here it removes extension
                                                    # and returns the root of the names

        this_day = self.begin_date
        data_array = []  # creates the data dictionary
        data_array_ticks = []  # and this array serves the plot ticks
        for day in range(0,n_files):  # files are scanned by date since date is present in the filename
            day_two_digits = '{:02d}'.format(this_day.day)          # Converts day to a fixed two digit string
            month_two_digits = '{:02d}'.format(this_day.month)    # and similarly for months
            date_string = str(self.begin_date.year) + month_two_digits + day_two_digits   # name_file is added to this string
            this_path = self.data_path + '/' + root_file_name + date_string + ext      # and path location
            data_array_ticks.append( day_two_digits + '/' + month_two_digits )
            data_array.append( pd.read_csv(this_path,encoding='latin-1',header=0) )  # everything is appendend in an array of DFs
            this_day = this_day + datetime.timedelta(days=1) 
        
        print(data_array[0].keys())
        #self.data = data_array        
        
        
    def ingestion( self ):
        pass
    def show_national_data():
        pass