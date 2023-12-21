#!~/anaconda3/bin/python

in_date="Mon, 5 Sep 2022 05:43:36 -0400"

# 2022-09-05
x=in_date.split(" ",4)

print(x)

dd=x[1]
month=x[2]
yy=x[3]

if month=='Jan':
 	mm='01'
elif month=='Feb':
 	mm='02'
elif month=='Mar':
 	mm='03'
elif month=='Apr':
 	mm='04'
elif month=='May':
 	mm='05'
elif month=='June':
 	mm='06'
elif month=='Jul':
 	mm='07'
elif month=='Aug':
 	mm='08'
elif month=='Sep':
 	mm='09'
elif month=='Oct':
 	mm='10'
elif month=='Nov':
 	mm='11'
elif month=='Dec':
 	mm='12'

out_date=yy+"-"+mm+"-"+dd

print(out_date)
 
