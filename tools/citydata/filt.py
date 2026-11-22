import sys,csv,json,re
csv.field_size_limit(10**9)
LA0,LA1,LO0,LO1=43.625,43.648,-79.455,-79.418
r=csv.reader(sys.stdin);h=next(r);gi=h.index('geometry');out=[]
for row in r:
    g=row[gi];m=re.search(r'(-79\.\d+),\s*(43\.\d+)',g)
    if not m:continue
    lo,la=float(m.group(1)),float(m.group(2))
    if not(LA0<la<LA1 and LO0<lo<LO1):
        # polygons: check all coords quickly only if first not inside
        continue
    out.append(dict(zip(h,row)))
json.dump(out,open(sys.argv[1],'w'));print(len(out))
