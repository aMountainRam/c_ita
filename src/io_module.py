import sys
import os
from datetime import datetime
    
# We define generic message tags
WARN = "|\033[1;33mWARN\033[0m|"
ERROR = "|\033[1;31mERR \033[0m|"
INFO = "|\033[1;34mINFO\033[0m|"

def make_it_fancy(string,color,deco):
    pass

# and a function to write standardized logs
def log_message (type=WARN,message="default warning message"):
    SEP = '  '
    now = datetime.now()
    now_formatted = now.strftime('%Y-%m-%d %H:%M:%S')
    output_string = \
        '{1}{0}{2}{0}-{0}{3}\n'.format(SEP,type,now_formatted,message)
    if ( type == ERROR ):
        sys.stderr.write(output_string)  # Errors written on 2>
    else:
        sys.stdout.write(output_string)  # Anything else written on 1>

class Standard_to_terminal:
            
    # Splash message
    splash_lines = [ 'Data analysis in Python', \
            '> version 1.0-SNAPSHOT', \
            'for COVID-19 in Italy by province', \
            'and data repo at https://github.com/pcm-dpc/COVID-19' ]

    splash_lines_fancy = []
    
    for a_line in splash_lines:
        splash_lines_fancy.append(a_line)
        
    splash_lines_fancy[3] = \
        'and data repo at ' + \
        '\033[1;97mhttps://\033[1;35mgithub.com/pcm-dpc/COVID-19\033[0m'
    
    def __init__(self,main_path):
        self.main_path = os.path.dirname(main_path)
        self.src_path = os.path.dirname(main_path + '/src')
        self.print_splash()
        
    def print_splash(self):
        list_OS = ['darwin','linux','freebsd']
        
        # for better ASCII art use
        # not used ATM
        if (sys.platform in list_OS):
            # we can use the `stty size` method
            # which returns `rows` and `columns` separated by a space
            rows, columns = \
                os.popen('stty size', 'r').read().split(sep=' ',maxsplit=1)
            rows = int(rows)
            columns = int(columns)
        
        # Actual splash
        print('\n')  # carriage return
        
        # compute the width of the box without fancy things
        max = 0
        actual_lengths = [] # while storing lengths
        for line in self.splash_lines:
            actual_lengths.append(len(line))
            if ( len(line) > max ):
                max = len(line)
        # and now print the fancy version of the splash
        # with escape characters which include
        # \033[1;97m `white bold` and \033[1;35m `magenta bold`
        print('*','-' * (max+2), '*')
        for n in range(0,len(self.splash_lines_fancy)):
            print('| ',self.splash_lines_fancy[n],' ' * (max-actual_lengths[n]), '|')
        print('*','-' * (max+2), '*')
        print('\n')
        
        # activate to run a template warning message
        #log_message()