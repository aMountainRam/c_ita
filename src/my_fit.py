import numpy as np
from scipy.stats import logistic
from scipy.optimize import curve_fit
from scipy.optimize import OptimizeWarning
from sklearn.metrics import r2_score
from src import io_module as iom

def exp_line(x,growth=1.0,amplitude=1.0):
    return amplitude * np.exp( growth * x )

def logistic_line(x,amplitude=1.0,loc=0.0,scale=1.0):
    return amplitude * logistic.cdf(x,loc=loc,scale=scale)

def logistic_condensed(x,dlo):
    return logistic_line(x,dlo[0],dlo[1],dlo[2])
    
def exp_condensed(x,deo):
    return exp_line(x,deo[0],deo[1])

def do_the_logistic_fit(x,y_data,print_flag=False,maxfev=800):
    # fit with logistic curve
    try:
        popt_logistic, pcov_logistic = curve_fit(logistic_line, x, y_data,maxfev=maxfev)
        y_true_logistic = logistic_condensed(x,popt_logistic)
        z_logistic = r2_score(y_true_logistic,y_data)
        if (print_flag):
            string2 = '* logistic *'
            string1 = '*' * len(string2)
            print('\n' + string1 + '\n' + string2  + '\n' + string1 + '\n')
            print('amp = {0}, loc = {1}, scale = {2}, R2 = {3}\n'.format( popt_logistic[0],
                    popt_logistic[1],popt_logistic[2],z_logistic) )    
        return popt_logistic, z_logistic
    except OptimizeWarning as oe:
        iom.log_message(iom.ERROR, str(oe))
        raise Exception

def do_the_exp_fit(x,y_data,print_flag=False):
    # fit with exponential
    popt_exp, pcov_exp = curve_fit(exp_line, x, y_data)
    # R2 test of logistic
    # R2 test of exp
    y_true_exp = exp_condensed(x,popt_exp)
    z_exp = r2_score(y_true_exp,y_data)
    iom.log_message(iom.INFO,'Fit done')
    if (print_flag):
        string2 = '* exponential *'
        string1 = '*' * len(string2)
        print('\n' + string1 + '\n' + string2  + '\n' + string1 + '\n')
        print('growth = {0}, amp = {1}, R2 = {2}\n'.format( popt_exp[0], popt_exp[1],z_exp) )    
    return popt_exp, z_exp

