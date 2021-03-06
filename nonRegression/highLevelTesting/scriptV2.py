import lsm.lsm as lsm
import ast
import shutil
import os
from shutil import rmtree

# create an event log, in this case hand-made, but can also be extracted with log file extractor:

fin = open("/home/jeff/Desktop/Test/highLevelTesting/temp/V2gross.log", "rt")
fout = open("/home/jeff/Desktop/Test/highLevelTesting/V2ready.log", "wt")
for line in fin:
        fout.write(line.replace("aaa", "{").replace("bbb", "},").replace("ccc", "[").replace("ddd", "]"))
fin.close()
fout.close()

with open("/home/jeff/Desktop/Test/highLevelTesting/V2ready.log") as f: 
    data = f.read() 

# reconstructing the data as a dictionary 
log = ast.literal_eval(data) 


# specify path of where results should be stored (.dot files and RESULT file):
lsm.setResultDir("results")   


# instantiate the Observer class providing a path name of specification file:
observer = lsm.Observer("spec")


# call the observer's monitor function on the log:
observer.monitor(log)


with open("/home/jeff/Desktop/Test/highLevelTesting/temp/V2gross.log") as g:
    header = g.readlines(0)
    t = header[1][2:16]
    a = header[2][6:8]
    b = header[3][6:8]
g.close()


with open("/home/jeff/Desktop/Test/highLevelTesting/results/RESULTS") as h: 
    if "specification was satisfied" in h.read(): 
        correctness = "OK"
    else :  
        correctness = "NOK"
h.close()

if os.path.isdir("/home/jeff/Desktop/Test/highLevelTesting/reports/v2_"+a+"_"+b+"_"+t+"_"+correctness) == False:
    shutil.copytree("/home/jeff/Desktop/Test/highLevelTesting/results", "/home/jeff/Desktop/Test/highLevelTesting/reports/HiLev_v2_"+a+"_"+b+"_"+t+"_"+correctness)

os.rename("/home/jeff/Desktop/Test/highLevelTesting/V2ready.log", "/home/jeff/Desktop/Test/highLevelTesting/logs/HiLev_v2_"+a+"_"+b+"_"+t+".log")
