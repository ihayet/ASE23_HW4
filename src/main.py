from collections import OrderedDict
import re
import sys
import os
from strings import fmt, coerce
from utils import getThe, setThe, setSeed, get_ofile, rint
from test import settings_test, rand_test, sym_test, num_test, csv_test, data_test, stats_test, clone_test, around_test, half_test, cluster_test, optimize_test, copy_test, repcols_test, reprows_test, synonyms_test, prototypes_test, position_test, every_test

help = 'script.lua : an example script with help text and a test suite\n (c)2022, Tim Menzies <timm@ieee.org>, BSD-2\n USAGE:   script.lua  [OPTIONS] [-g ACTION] \n OPTIONS: \n -d  --dump  on crash, dump stack = false \n -f  --file  name of file = etc/data/repgrid1.csv \n -g  --go    start-up action      = data \n -h  --help  show help            = false \n -p  --p  distance coefficient = 2 \n -s  --seed  random number seed   = 937162211\n ACTIONS:\n'

env_b4 = {}
for env in os.environ:
    env_b4[env] = os.getenv(env)

def settings(s):
    t = OrderedDict()
    sSplit = s.split('\n')

    for st in sSplit:
        res = re.match(r'[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)', st)
        if res is not None:
            t[res.group(1)] = res.group(2)

    return t

def cli(options):
    for k in options:   
        skip = set()
        for i, arg in enumerate(sys.argv):
            if i not in skip:
                if arg == '-' + k[0:1] or arg == '--' + k:
                    tempV = options[k]
                    if tempV == 'false':
                        tempV = 'true'
                    elif tempV == 'true':
                        tempV = 'false'
                    else:
                        tempV = sys.argv[i+1]
                        skip.add(i)
                    
                    options[k] = coerce(tempV)
        else:
            options[k] = coerce(options[k])
    return options

egs = {}
def eg(key, str, fun):
    global help
    egs[key] = fun
    help = help + fmt(" -g %s\t%s\n", key, str)

def main(options, help, funs):
    # HW1
    eg("the","show settings", settings_test)
    # eg("rand","generate, reset, regenerate same", rand_test)
    eg("sym","check syms", sym_test)
    eg("num", "check nums", num_test)
    
    # HW2
    # eg("csv", "read from csv", csv_test)
    # eg("data", "read DATA csv", data_test)
    # eg("clone", "duplicate structure", clone_test)

    # HW3
    # eg("around", "sorting nearest neighbors", around_test)
    # eg("half", "1-level bi-clustering", half_test)
    # eg("cluster", "N-level bi-clustering", cluster_test)
    # eg("optimize", "semi-supervised optimization", optimize_test)
    
    # HW4
    eg('copy', 'check copy', copy_test)
    eg('repcols', 'checking repcols', repcols_test)
    eg('reprows', 'checking reprows', reprows_test)
    eg('synonyms', 'checking repcols cluster', synonyms_test)
    eg('prototypes', 'checking reprows cluster', prototypes_test)
    eg('position', 'where\'s wally', position_test)
    eg('every', 'the whole enchilada', every_test)
    

    o_file = get_ofile()
    err = 0
    options = cli(settings(help))
    saved = OrderedDict()
    for k in options:
        saved[k] = options[k]
    setThe(options)

    if options['help']:
        print(help)
    else:
        for fun_key in funs:
            if options['go'] == 'all' or fun_key == options['go']:
                setSeed(options['seed'])
                if funs[fun_key]() > 0:
                    err += funs[fun_key]()
                    print("❌ fail:", fun_key) 
                    o_file.write("❌ fail: " + str(fun_key) + "\n")
                    pass
                else:
                    print("✅ pass:", fun_key)
                    o_file.write("✅ pass: " + str(fun_key) + "\n")
                    pass
        
        o_file.close()

    return err

err = main(getThe(), help, egs)
exit(err)