from collections import Counter
import csv
f = open("Illinois Compiled Database 2002-11.csv", "rb")
reader = csv.reader(f)
headers = reader.next()
rel_headers = ['GXID','MONTH','AMPM','VEHSPD','TYPVEH','VEHDIR','POSITION','RRCAR','TYPACC','VISIBLTY','WEATHER','TYPTRK','TRKCLAS','TRNSPD','TRNDIR','LOCWARN','WARNSIG','LIGHTS','MOTORIST','VIEW','CROSSING','PUBLIC','DRIVAGE','DRIVGEN']
index = []
column = {}
for i, h in enumerate(rel_headers):
    index.append(headers.index(h))
    column[h] = []

for row in reader:
    for j in range(len(index)):
        column[headers[index[j]]].append(str(row[index[j]]))
    
inv_column = {}    
inv_file = open("All.csv", "rb")
inv_reader = csv.reader(inv_file)
inv_headers = inv_reader.next()
for h in inv_headers:
    inv_column[h] = []

for row in inv_reader:
    for i, h in enumerate(inv_headers):
        inv_column[h].append(str(row[i]))

#Getting all the single accident locations

single_location = [k for k, v in Counter(column["GXID"]).iteritems() if v == 1]

column["XANGLE"] = []
column["WDCODE"] = []
column["TYPEXING"] = []
for xing in column["GXID"]:
    if xing in inv_column["CROSSING"]:
        i = inv_column["CROSSING"].index(xing)
        column["XANGLE"].append(str(inv_column["XANGLE"][i]))
        column["WDCODE"].append(str(inv_column["WDCODE"][i]))
        column["TYPEXING"].append(str(inv_column["TYPEXING"][i]))
    else:
        column["XANGLE"].append("None")
        column["WDCODE"].append("None")
        column["TYPEXING"].append("None")
    
                                    
##for i, h in enumerate(headers):
##    if (i in index):
##        column[h] = []

#
with open('Files/MicroMacro/MicroMacroBucksAngle3060.csv','wb') as fp:
    a = csv.writer(fp, delimiter = ',')
    a.writerow(["CROSSING","Line in File","PUBLIC","TYPEXING","TYPACC","RRCAR", "POSITION"])
    i = 0
    for crossing, drivage, typveh, typacc, rrcar, position, public, angle, warn, inv_public in zip(column["GXID"],column["DRIVAGE"], column["TYPVEH"], column["TYPACC"], column["RRCAR"], column["POSITION"], column["PUBLIC"], column["XANGLE"], column["WDCODE"], column["TYPEXING"]):
        if (crossing in inv_column['CROSSING'] and crossing in single_location):
            if (angle == "2" and warn == "3"): #angle == "1" and warn == "8"):#(drivage != "" and int(drivage > 40)) and (typveh != "" and typveh in ["A","B","C","D","E","F","G","H","J"])):
                if ((typacc == "1" and position == "3") or (typacc == "2" and int(rrcar) <= 3)):
                    write = [crossing,str(i),public,inv_public, typacc, rrcar, position]    
                    a.writerow(write)
        i+=1
fp.close()
