"""Reproduce Corpus mode-ratio tables (FUN_000243e8 / 24ee4 / 25210 / 257b4) for the report."""
import math
def beam(N):
    b=[4.73,7.853,10.996]+[(i+1.5)*math.pi for i in range(3,N)]
    return [x*x/(b[0]*b[0]) for x in b[:N]]
def marimba(N):
    b=[4.73,9.413,15.45,20.71,24.58]+[(i*1.4142+2.1213)*math.pi for i in range(5,N)]
    return [x*x/(b[0]*b[0]) for x in b[:N]]
def string(N): return [i+1.0 for i in range(N)]
def grid2d(N,R,plate):
    mx=int(math.sqrt(R*N)); my=int(math.sqrt(N/R))
    if (mx+1)**2==R*N: mx+=1
    if (my+1)**2==N/R: my+=1
    e=[]
    for m in range(1,mx+2):
        for n in range(1,my+2):
            v=(m*m+(R*n)**2)
            e.append(((v/(R*R+1)) if plate else math.sqrt(v)/math.sqrt(R*R+1),m,n))
    e.sort(key=lambda t:t[0])  # stable, same as the bubble sort with strict <
    return e[:N]
if __name__=='__main__':
    f=lambda l:', '.join('%.4g'%x for x in l)
    print('beam16',f(beam(16)))
    print('marimba16',f(marimba(16)))
    for R in (1.0,1.5):
        print('membrane16 R=%g'%R, ', '.join('%.4g(%d,%d)'%t for t in grid2d(16,R,False)))
        print('plate16 R=%g'%R, ', '.join('%.4g(%d,%d)'%t for t in grid2d(16,R,True)))
    assert abs(beam(4)[1]-2.7565)<1e-3 and grid2d(4,1.5,False)[0][0]==1.0
