import sys
import os
import numpy as np 
import flask
import pickle
import time

HER_GRID = 50
VER_GRID = 50
HER_LEN = 1050
VER_LEN = 750
a_col = 6
a_row = 4
hopDis = 2
COL = HER_LEN//HER_GRID
ROW = VER_LEN//VER_GRID
PRELOCATION = 10

arg1 = sys.argv[1]
loaded_model = pickle.load(open("model.pkl","rb"))
if not arg1:
    exit

class GridPoint():
    def __init__(self, pStr):
        pStrList = pStr.split(" ")
        self.point = [int(x) for x in pStrList]
        self.x = self.point[0]
        self.y = self.point[1]
        
def encodeGPList(gpList, nRows):
    xx = np.zeros((1, PRELOCATION, ROW+COL), dtype=np.bool)
    x = np.zeros((nRows, COL+ROW))
    #print(len(gpList))
    if(len(gpList)==nRows):
        for i, p in enumerate(gpList):
            x[i, p.x] = 1
            yy = COL+p.y
            if(yy>=COL+ROW):
                yy=COL+ROW-1
            x[i, yy] = 1
    elif len(gpList)<nRows:
        start = nRows - len(gpList)
        counter = 0;
        for i in range(start, nRows):
            p = gpList[counter]
            counter+=1
            x[i, p.x] = 1
            yy = COL+p.y
            if(yy>=COL+ROW):
                yy=COL+ROW-1
            x[i, yy] = 1
    xx[0] = x        
    return xx

def decodeToGP(oneHot):
    gpList = []
    for row in oneHot[0]:
        count = 0
        cur = []
        first = True
        #print(row)
        for cell in row:
            
            
            if cell ==1:
                if not first:
                    count-=COL
                first = False
                cur.append(count)
            count+=1
        gpList.append(cur)
    return gpList


def decodeConstraint (self, x, calc_argmax=True):
    if calc_argmax:
        x = x.argmax(axis=-1)
        
    return [x for x in x]

def ValuePredictor(to_predict):
     
     
     result = loaded_model.predict_classes(to_predict, verbose=0)
     return result[0]

def preProcessInput(strIn):
    gpList = []
    for p in strIn.strip().split(")("):
        gp = GridPoint(p.replace("(","").replace(")","").replace(","," "))
        gpList.append(gp)
    return gpList
       



start_time = time.time()
print(ValuePredictor(encodeGPList(preProcessInput(arg1),PRELOCATION)))
print("--- %s seconds ---" % (time.time() - start_time))       

#guess = decodeConstraint(ValuePredictor(encodeGPList(preProcessInput(arg1),PRELOCATION)), calc_argmax=False)
#print(guess)

sys.stdout.flush()
exit