import json,sys,matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
X0,X1,Z0,Z1=[float(v) for v in sys.argv[1:5]];out=sys.argv[5]
D=json.load(open('pkregion.json'));P=json.load(open('/home/claude/od/city/parcels_game.json'));A=json.load(open('/home/claude/od/city/addr_game.json'))
M=json.load(open('/home/claude/od/massing_fit.json'));L=json.load(open('/home/claude/od/city/loc_fit.json'))
T=lambda x,z:(x*L[0][0]+z*L[1][0]+L[2][0],x*L[0][1]+z*L[1][1]+L[2][1])
fig,ax=plt.subplots(figsize=(12,12*(Z1-Z0)/(X1-X0)))
for n,c,car,p in D['r']:
    xs=[q[0] for q in p];zs=[q[1] for q in p];ax.plot(xs,zs,color='#bbbbbb',lw=max(1,car*2.2*72/((X1-X0)/12*1)),alpha=.5,solid_capstyle='butt')
for tag,h,p in D['b']:
    ax.fill([q[0] for q in p],[q[1] for q in p],color='#7aa6d6',alpha=.55);cx=sum(q[0] for q in p)/len(p);cz=sum(q[1] for q in p)/len(p)
    if X0<cx<X1 and Z0<cz<Z1:ax.text(cx,cz,f'{tag}\n{h}m',fontsize=6,ha='center',color='#003')
for m in M:
    x,z=m['c']
    if X0-30<x<X1+30 and Z0-30<abs(z)<Z1+30:
        r=m['r'][0];sg=1 if r[0][1]>0 else -1;r=[T(q[0],sg*q[1]) for q in r];ax.plot([q[0] for q in r],[q[1] for q in r],color='#1b5e20',lw=.8)
for p in P:
    r=[T(*q) for q in p['r']]
    if any(X0-20<x<X1+20 and Z0-20<z<Z1+20 for x,z in r):ax.plot([q[0] for q in r],[q[1] for q in r],color='#d0104c',lw=1.1)
for a in A:
    a=[a[0],*T(a[1],a[2])]
    if X0<a[1]<X1 and Z0<a[2]<Z1:ax.plot(a[1],a[2],'o',color='#e65100',ms=2.5);ax.text(a[1]+.6,a[2],a[0].replace(' Ave','').replace(' St',''),fontsize=6.5,color='#e65100')
ax.set_xlim(X0,X1);ax.set_ylim(Z1,Z0);ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_title('PK (blue fill, roads grey) vs City property lines (red), 3D massing (green), address points (orange). North up.',fontsize=9)
plt.tight_layout();plt.savefig(out,dpi=110)
