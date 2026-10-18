# usage: q.py code <entry> | callers <entry> | callees <entry> | name <entry>
import sys, pickle, json
off,callers,callees,names=pickle.load(open(__file__.rsplit('/',1)[0]+'/idx.pkl','rb'))
C='/var/tmp/sound-analysis/corpus/decomp/chunks/'
def norm(a): return hex(int(a,16))
cmd=sys.argv[1]
for a in sys.argv[2:]:
    a=norm(a)
    if cmd=='code':
        f,p=off[a]; fh=open(C+f,'rb'); fh.seek(p); r=json.loads(fh.readline())
        print('//',a,r['name'],r['state'],r.get('error') or '','sig:',r['signature']); print(r['code'])
    elif cmd=='callers':
        for s,c,k in callers.get(a,[]): print(a,'<-',c,names.get(c),s,k)
    elif cmd=='callees':
        for s,t,n,k in callees.get(a,[]): print(a,'->',t,n,s,k)
    elif cmd=='name': print(a,names.get(a))
