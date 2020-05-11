import os, sys, argparse, datetime, itertools

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import text
from matplotlib import font_manager
from matplotlib import axes

from src import my_fit as mf
from src import io_module as iom
from src import data_ingestion as di
from src.national import National

####
# Parsing input
####
description='This program allows a direct evaluation' \
    + ' of some basic stats on COVID-19 data' \
    + ' provided by Protezione Civile region-by-region' \
    + ' and province-by-province since 24 Feb 2020.' \
    + ' By simply pass the name of a province (even in abbreviated form)' \
    + ' like \033[1;35mBG\033[0m or \033[1;33mBergamo\033[0m' \
    + ' you\'ll obtain plots for (\033[1;39m1\033[0m) data, (\033[1;39m2\033[0m) logistic distribution' \
    + ' when available and (\033[1;39m3\033[0m) exponential growth of the contagion.' \
    + ' Logistic CDF \t=>\t f(x)=(1+exp(-x))^(-1)'
    
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-p', dest='provinces', type=str, nargs='+',
                help='list here the provinces')
parser.add_argument('-n',action='store_true',default=False,
                    dest='national_switch', help='switch to "nation" mode')
parser.add_argument('-v', action='store_true', default=False, 
                    dest='verbose_switch', help='print fit output')

args = parser.parse_args()
input_provs = args.provinces
verbose = args.verbose_switch
national = args.national_switch

    
if(verbose):
    print('\n')
    iom.log_message(iom.WARN,'In VERBOSE mode!')
if ( input_provs ):
    flag_passed = True
else:
    flag_passed = False
    
####
## Splash
####
main_path = os.path.dirname( os.path.abspath( __file__ ) )
std = iom.Standard_to_terminal( main_path )
if(national):
    a = National( main_path )
    a.ingestion()
#exit()
####
## Data Ingestion
####
n_files, provs, data_array, data_array_ticks = di.data_ingestion( main_path )

####
## Prompt user if needed
####
if( flag_passed ):
    pass
else:
    print('Input "Provincia" name or abbreviation')
    print('(e.g., BS or Bergamo,...) comma separated. ')
    input_string = input('Letter case or blank spaces don\'t count: ')
    input_provs = input_string.split(',')
    to_be_removed = []
    for j in range(0,len(input_provs)):
        print(j)
        input_provs[j] = input_provs[j].strip(' ').upper()
        if(len(input_provs[j])!=2 or not ( input_provs[j] in provs ) ):
            to_be_removed.append(input_provs[j])
            
    for s in to_be_removed:
        input_provs.remove(s)
    print(input_provs)

####
## Plotting
####
marker = itertools.cycle(('+', 'o', '*','v','s','d'))
color = itertools.cycle(('red','blue','green','brown','cyan','magenta')) 
casi = {}
max_y = 1.0
got_at_least_one = False
for prov in input_provs:
    prov_casi = np.arange(0,n_files)
    for i in range(0,n_files):
        filtered = data_array[i].filter(['sigla_provincia','totale_casi'])
        prov_casi[i] = filtered[filtered.sigla_provincia == prov]['totale_casi'] 
    casi.update( { prov : prov_casi } )
    
    ###
    # FIT-TIME !!!
    ###
    x = np.arange(0,n_files)
    plot_fit_logistic = True
    # Logistic
    try:
        dlo, zl = mf.do_the_logistic_fit(x,casi[prov],print_flag=verbose)
        plot_fit_logistic = True
        if (zl < 0.8):
            raise Exception('R2 is very bad!')
        if( dlo[0] > max_y ):
            max_y = dlo[0]
            got_at_least_one = True
    except Exception:
        plot_fit_logistic = False
    # Exponential
    try:
        deo, ze = mf.do_the_exp_fit(x,casi[prov],print_flag=verbose)
    except:
        pass

    the_color = next(color)
    x_two = np.arange(0,int(3/2*len(x)))
    x_ticks = np.arange(0,int(3/2*len(x)),5)
    #print(x_ticks)
    x_data_ticks = []
    for i in x_ticks:
        date = datetime.date(2020,2,24)+datetime.timedelta(days=int(i))
        if( date.day < 10 ):
            string_date = '0' + str(date.day)
        else:
            string_date = str(date.day)
        if( date.month < 10 ):
            string_date += '/0' + str(date.month)
        else:
            string_date += '/' + str(date.month)
        x_data_ticks.append(string_date)
    if(plot_fit_logistic):
        plt.plot(x_two,mf.logistic_condensed(x_two,dlo),color=the_color,linestyle='dotted',linewidth=1)
        plt.hlines(dlo[0],xmin=x_two[0],xmax=x_two[len(x_two)-1],linestyle='dashed',linewidth=0.8,color='grey')

    plt.plot(x,casi[prov],marker=next(marker),markersize=7,color=the_color,linestyle='None',label=prov)
    plt.plot(x,mf.exp_condensed(x,deo),color=the_color,linestyle='dashed',label='fit exp')
    xl = font_manager.FontProperties(size='xx-small')
    plt.xticks(ticks=x_ticks,labels=x_data_ticks,fontproperties=xl)
    plt.legend(loc='upper left')

# compute y axis

if (got_at_least_one):
    padding = 3.5/100.0*max_y
    plt.ylim( ( 0.0-padding, max_y+padding ) )
    plt.xlim( ( 0,int(3/2 * di.date_to_num(datetime.date.today() )) ) )
plt.show()
