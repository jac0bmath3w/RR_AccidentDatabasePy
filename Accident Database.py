from collections import Counter
import csv
f = open("Illinois Compiled Database 2002-11.csv", "rb")
reader = csv.reader(f)
headers = reader.next()
rel_headers = ['GXID','MONTH','AMPM','VEHSPD','TYPVEH','VEHDIR','POSITION','TYPACC','VISIBLTY','WEATHER','TYPTRK','TRKCLAS','TRNSPD','TRNDIR','LOCWARN','WARNSIG','LIGHTS','MOTORIST','VIEW','CROSSING','PUBLIC','DRIVAGE','DRIVGEN']
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
with open('Files/WarnDev/SingleGatesAngle60.csv','wb') as fp:
    a = csv.writer(fp, delimiter = ',')
    a.writerow(["CROSSING","Line in File","PUBLIC","TYPEXING","WARNING DEVICE CODE","ANGLE"])
    i = 0
    for crossing, drivage, typveh, public, angle, acc_warn, inv_warn, inv_public in zip(column["GXID"],column["DRIVAGE"], column["TYPVEH"], column["PUBLIC"], column["XANGLE"], column["CROSSING"], column["WDCODE"], column["TYPEXING"]):
        if crossing in single_location and crossing in inv_column["CROSSING"]: #angle == "1" and warn == "8"):#(drivage != "" and int(drivage > 40)) and (typveh != "" and typveh in ["A","B","C","D","E","F","G","H","J"])):
            if ("01" in acc_warn and "101" not in acc_warn) and (angle == "3"): #and "101" not in acc_warn:
                write = [crossing,str(i),public,inv_public,acc_warn,angle]    
                a.writerow(write)
        i+=1
fp.close()
