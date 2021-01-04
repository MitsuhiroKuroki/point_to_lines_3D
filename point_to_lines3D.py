import Rhino
import rhinoscriptsyntax as rs
import scriptcontext
import System.Collections.Generic as SCG
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree
import clr
import ghpythonlib.components as gh
clr.AddReference("Grasshopper")
from math import *
#from numba.decorators import jit
linedata=[]
indv1=[];indv2=[];isuv=[]
drx=[];dry=[];drz=[]
el=[];s=[];pl=[]
i1=[];i2=[]
sle_out=[]
nodenum=len(pointdata)
elemnum=int(nodenum*(nodenum-1)/2+1)
#elemnum=int(400000)
for i in range(elemnum):
    indv1.Add(int(0))
    indv2.Add(int(0))
    isuv.Add(int(0))
    i1.Add(int(0))
    i2.Add(int(0))

for i in range(nodenum):
    el.Add(int(0))
    drx.Add(int(0))
    dry.Add(int(0))
    drz.Add(int(0))
    s.Add(int(0))
    pl.Add(int(0))

n=0
for i in range(nodenum):
    nj=0
    for j in range(1,nodenum):
        if j>i:
            #n+=1
            #nj+=1
            xij=pointdatax[j]-pointdatax[i]
            yij=pointdatay[j]-pointdatay[i]
            zij=pointdataz[j]-pointdataz[i]
            sle=sqrt(xij**2+yij**2+zij**2)
            #sle_out.Add(sle)
            
            if sle<=lmax:
                n+=1
                indv1[n]=i
                indv2[n]=j
                isuv[n]=int(1)
                nj+=1
                el[nj]=sle
                drx[nj]=xij/el[nj]
                dry[nj]=yij/el[nj]
                drz[nj]=zij/el[nj]
                if nj>0:
                    nn=n-nj
                    for k in range(nj):
                        #k+=1
                        s[k]=fabs(drx[k]-drx[nj])+fabs(dry[k]-dry[nj])+fabs(drz[k]-drz[nj])
                        pl[k]=el[k]-el[nj]
                        sle_out.Add(s[k])
                        if s[k]<0.0001:
                            if pl[k]>0:
                                isuv[nn+k]=0
                            else:
                                isuv[n]=0
                        if (case==1) and plane=="3d":#(drx[nj]*dry[nj]!=0 or dry[nj]*drz[nj]!=0 or drx[nj]*drz[nj]!=0) :
                            if drx[nj]*dry[nj]*drz[nj]!=0:
                                isuv[n]=0
                        if (case==1) and plane=="xy":
                            if drx[nj]*dry[nj]!=0:
                                isuv[n]=0
                        if (case==1) and plane=="yz":
                            if dry[nj]*drz[nj]!=0:
                                isuv[n]=0
                        if (case==1) and plane=="xz":
                            if drx[nj]*drz[nj]!=0:
                                isuv[n]=0

nel=0;l=0
for l in range(n):
    l+=1
    i1[l]=indv1[l]
    i2[l]=indv2[l]
    if isuv[l]==1:
        nel+=1
        indv1[nel]=i1[l]
        indv2[nel]=i2[l]
        k0=int(indv1[nel])
        k1=int(indv2[nel])
        linemake=gh.Line(pointdata[k0],pointdata[k1])
        linedata.Add(linemake)

a=indv1;b=indv2
