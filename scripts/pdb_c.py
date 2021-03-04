import numpy as np
import scipy.spatial as spatial
import time
import math
from math import log10, floor
import os
import sys

def get_donars(arr_h,refe1,arr):
    point_tree = spatial.cKDTree(arr)
    li_a={}
    for i in range (len(arr_h)):
        li1=(point_tree.query_ball_point(arr_h[i], 1.5))
        if len(li1)==0:
            pass
        else:
            li_a[i]=refe1[li1[0]]
    return li_a

def angle(a,b,c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)

        return np.degrees(angle)

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)

def distance(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)

def chain(r,st):
    l=len(r)
    l_=st[l:]
    if len(l_)==0 or l_.isdigit() or l_ == 'A':
        chain='backbone'
    else:
        chain='side_chain' 
    return chain

def data_extraction(path1,path2):
    d={}
    file_ref=1
    d['file_xyz']=path2.split('/')[-1]
    if path1:
        d['file_pdb']=path1.split('/')[-1]
    else:
        d['file_pdb']='-'
        file_ref=0
    if path1=='':
        path1=path2
    file1,file2=open(path1,'r'),open(path2,'r')
    list1,list2=file1.readlines(),file2.readlines()
    file1.close()
    file2.close()
    l=0
    n_heavy_pdb,n_light_pdb=0,0
    ref_l1=1
    for line in list1[2:]:
        if path1==path2:
            if len(line.strip().split())<4:
                break
            id=ref_l1
            d[id]=['','',line.split()[0],'','']
            ref_l1+=1
            #print id,d[id]
        else:
            if "TER" in line.split()[0]:
                break
                l+=1
                id=line.strip().split()[1]
                d[int(id)]=['-','-','-','-','-']
                continue
            if "MASTER" in line.split()[0]: #break with TER
                break
            if 'ATOM' in line.split()[0]: #use HETATM only when required
                #print line
                id,at,rt,_,_0,x,y,z=line.strip().split()[1:9]
                s=line.strip().split()[-1]
                d[int(id)]=[at,rt,s,chain(s,at),_0]
                if rt=='HOH':
                    d[int(id)][3]='Water'
                #print id
                l+=1
                if s=='H':
                    n_light_pdb+=1
                else:
                    n_heavy_pdb+=1
    l=ref_l1   

    refe_h,refe_d,ref_all={},{},1
    refe1,r1,r2={},0,0
    arr,arr_h,arr_a=[],[],[]
    ref=1
    refe_a,ra={},0
    coord={}
    for line in list2[2:]:
        if len(line.strip().split())<4:
            break
        s,x,y,z=line.strip().split()
        if s!='H':
            #print 'hd'
            ref_ad=ref 
            while ref_ad<l:
                if d[ref_ad][2]==s:
                    break
                ref_ad+=1
            if s in ['O','N','F','C','S','I']:
                #print d[ref_ad][2],s,ref_ad
                refe_a[ra]=ref_ad 
                refe_d[ref_ad]=ref_all
                ra+=1
                #print ref_ad,ref_all
                arr_a.append([float(x),float(y),float(z)])
            refe1[r1]=ref_ad 
            r1+=1
            arr.append([float(x),float(y),float(z)])
            ref=ref_ad+1
        elif s=='H':
            refe_h[r2]=ref_all
            r2+=1
            arr_h.append([float(x),float(y),float(z)])  
        coord[ref_all]=[float(x),float(y),float(z)]
        ref_all+=1
    donars=get_donars(arr_h,refe1,arr)

    return d,donars,arr_a,arr_h,refe_a,refe_h,n_heavy_pdb,n_light_pdb,r1,r2,refe_d,coord,file_ref

#return [index from array donars,[index for hydrogens,...]]
def result(arr1,arr2,mi,ma):
    points = arr2
    if len(arr2)==0:
        raise Exception("There are no hydrogen atoms !!")
    point_tree = spatial.cKDTree(points)
    li1,li2=[],[]
    res=[]
    for i in range (len(arr1)):
        #print i
        li1=(point_tree.query_ball_point(arr1[i], ma))
        li2=(point_tree.query_ball_point(arr1[i], mi))
        res.append([i,list(set(li1)-set(li2))])
    return res

#returns [donar id,[(hydrogen id,acceptor id),....]]
def output(data):
    d,donars,arr_a,arr_h,refe_a,refe_h,n_heavy_pdb,n_light_pdb,n_heavy,n_light,refe_d,coord,file_ref=data 
    res=result(arr_a,arr_h,1.4,4.0)
    #res=result(arr_a,arr_h,1.6,2.4)
    lis=[]
    h_count=0
    for i in res:
        a=i[0]
        a_id=refe_a[a]
        li=[]
        for j in i[1]:
            h_id=refe_h[j]
            d_id=donars[j]
            #if d[d_id][2] in ['O','N','F','C','I'] and d[a_id][2] in ['O','N','F','S','I']:
            #    h_count+=1
            li.append((h_id,d_id))
        lis.append([a_id,li]) 
    return [lis,[n_heavy_pdb,n_light_pdb,n_heavy,n_light,h_count,refe_d,coord,file_ref]]

def write_o(path1,out,d):
    file=open(path1.split('/')[-1].split('.')[0]+'.txt','w')
    tp = open(os.path.join(os.path.split(sys.argv[0])[0], 'init.txt'))
    file.write(''.join(tp.readlines()))
    n_heavy_pdb,n_light_pdb,n_heavy,n_light,h_count,refe_d,coord,file_ref=out[1]
    file.write("Filename : "+d['file_xyz']+'\n')
    file.write("Total number of heavy atoms : "+str(n_heavy)+'\n')
    file.write("Total number of light atoms : "+str(n_light)+'\n\n')
    file.write("Filename : "+d['file_pdb']+'\n')
    file.write("Total number of heavy atoms : "+str(n_heavy_pdb)+'\n')
    file.write("Total number of light atoms : "+str(n_light_pdb)+'\n\n')
    file.write("Number of hydrogen bonds possible : "+str(h_count)+'\n\n')
    tp.close
    
    h_c=0
    for item in out[0]:
        a,b=item 
        for i in b:
            j,k=i 
            hid=str(j)
            dist=str(round_sig(distance(coord[int(hid)],coord[refe_d[a]]),5))
            if d[a][2] in ['C'] or d[k][2] not in ['O','N','F','C','I'] or d[k][2]=='-' or d[a][2]=='-':
                continue
            if d[a][2] in ['O','N','F','S'] and d[k][2] in ['O','N','F','C','S'] and float(dist)>3.0:
                continue
            if d[a][2] in ['S'] and float(dist) < 3.3:
                continue
            if distance(coord[refe_d[a]],coord[refe_d[k]]) < 1.7:
                continue
            ang = angle(coord[refe_d[k]],coord[int(hid)],coord[refe_d[a]])
            if ang > 180:
                ang = 360.0 - ang
            if ang < 90.0 :
                continue  
            h_c+=1

    file.write("Number of hydrogen bonds possible : "+str(h_c)+'\n\n')
    #file.write("Number of hydrogen bonds possible : "+str(h_count)+'\n\n')
    if file_ref:
        file.write('File format : \nDonarResidueId donarResidueType donarChain donarSymbol donarAtomId, HydrogenAtomId, acceptorAtomId acceptorResidueId acceptorResidueType, acceptorChain acceptorSymbol (acceptorAtomId, hydrogenAtomId) D-H...A hydrogenBondLength \n\n')
    else:
        file.write('File format : \nDonarSymbol donarAtomId, HydrogenAtomId, acceptorAtomId , acceptorSymbol (acceptorAtomId, hydrogenAtomId) D-H...A hydrogenBondLength \n\n')
    st=''
    count=0
    st_d,b_d={},{}
    lm={}
    for item in out[0]:
        a,b=item 
        if file_ref:
            li1=[str(refe_d[a]),'[',str(d[a][4]),']',d[a][1],d[a][3],d[a][2]]
            li1_test="{:>6} {}{:>6}{} {:>6} {:>13} {:>2}".format(*li1)
        else:
            li1=[str(refe_d[a]),str(d[a][4]),d[a][1],d[a][3],d[a][2]]
            li1_test="{:>6}{}{}{} {:>2}".format(*li1)
        for i in b:
            j,k=i 
            hid=str(j)
            dist=str(round_sig(distance(coord[int(hid)],coord[refe_d[a]]),5))
            #print d[a][2],d[k][2],dist,distance(coord[refe_d[a]],coord[refe_d[k]])
            if d[a][2] in ['C'] or d[k][2] not in ['O','N','F','C','I'] or d[k][2]=='-' or d[a][2]=='-':
                continue
            if d[a][2] in ['O','N','F','S'] and d[k][2] in ['O','N','F','C','S'] and float(dist)>3.0:
                continue
            if d[a][2] in ['S'] and float(dist) < 3.3:
                continue
            if distance(coord[refe_d[a]],coord[refe_d[k]]) < 1.7:
                continue
            count+=1
            c=d[k][3]+'-'+d[a][3]
            #print refe_d
            if file_ref:
                li2=['[',str(d[k][4]),']',d[k][1],d[k][3],d[k][2],str(refe_d[k])]
                li2_test="{}{:>6}{} {:>6} {:>13} {:>2} {:>6}".format(*li2)
                est=[str(refe_d[a]),hid]
                lis_test=str(count)+'.',li2_test,hid,li1_test,str(refe_d[a]),hid,d[k][2]+'-H...'+d[a][2],dist+'\n'
                st_test="{:>6}  {:>30} ,{:>6} ,{:>24} ({:>6} ,{:>6}) {:>8}  {:>6}".format(*lis_test)
            else:
                li2=[str(d[k][4]),d[k][1],d[k][3],d[k][2],str(refe_d[k])]
                li2_test="{}{}{} {:>2} {:>6}".format(*li2)
                est=[str(refe_d[a]),hid]
                lis_test=str(count)+'.',li2_test,hid,li1_test,str(refe_d[a]),hid,d[k][2]+'-H...'+d[a][2],dist+'\n'
                st_test="{:>6}  {:>8} ,{:>6} ,{:>6} ({:>6} ,{:>6}) {:>8}  {:>6}".format(*lis_test)
            st0=st_test
            db=d[k][2]+'-H...'+d[a][2]
            if c not in st_d and c!='-':
                st_d[c]=[st0]
            elif c!='-':
                st_d[c].append(st0)
            if db not in b_d:
                b_d[db]=[st0]
            else:
                b_d[db].append(st0)
            file.write(st0)
            lm[str(count)+'.']=[d[k][2]+'-H...'+d[a][2],str(refe_d[a])+'-'+hid,dist]
            #st+=str(count)+'.'+' '*(5-(len(str(count))))+d[k][2]+'-H...'+d[a][2]+'   '+d[k][3]+'...'+d[a][3]+'\n'
    
    file.write('\n')
    file.write("Additional : \n\n")
    for string in st_d:
        if '--' in string:
            continue
        file.write(string+' N = '+str(len(st_d[string]))+'\n'+''.join(st_d[string])+'\n\n')
    for string in b_d:
        if '.-' in string:
            continue
        file.write(string+'    N = '+str(len(b_d[string]))+'\n'+''.join(b_d[string])+'\n\n')
    #file.write(st+'\n\n')
    file.write("...Termination of the program ....")
    file.close()
    return lm

def make_xyz(path):
    f=open(path,'r')
    lines=f.readlines()
    f.close()
    lis=''
    ref=0
    for line in lines:
        if '#p ' in line:
            ref+=1
        if len(line.strip().split())==0:
            ref+=1
        if ref==6:
            break
        if ref==3 or ref==4:
            ref+=1
        if ref==5:
            lis+=line
    g=open(path[:-4]+'.xyz','w')
    g.write(lis)
    g.close()
    return 1

'''
files=os.listdir('.')
path1,path2='',''
for i in files:
    if i[-4:]=='.com':
        make_xyz(i)
files=os.listdir('.')
for i in files:
    if i[-4:]=='.xyz':
        path2=i
'''
def job(path1):
    #path2=path2 or raw_input('Enter xyz path : ')
    data=data_extraction('',path1)
    out=output(data)
    return write_o(path1,out,data[0])






