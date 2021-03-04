import sys
import module
import scipy.spatial as spatial
import os
import hb_connections as hb
import math

def xyz(filename,end):
	if end==xyz:
		return
	print 'Making xyz ...'
	print 'Exit status :',module.make_xyz(filename+'.'+end)

# reading from pdb
def read_data(path):
	#xyz(path[:-4],path[-4:])
	os.system('babel '+path+' '+'.'.join(path.split('.')[:-1])+'.xyz')
	f=open(path[:-4]+'.xyz','r')
	lines=f.readlines()
	f.close()

	d={}
	ir=1
	nitro=[]
	nitro_d={}
	for i in lines[2:]:
		l=i.strip().split()
		if len(l)==1:
			break
		if len(l)==0:
			continue
		a,x,y,z=l
		x,y,z=list(map(float,[x,y,z]))
		if a=='N':
			nitro.append([x,y,z])
			nitro_d[len(nitro)-1]=ir  
		d[ir]=[a,x,y,z]
		ir+=1


	return d,nitro,nitro_d

def pre_data(path,ma,mi):
        d,nitro,nitro_d=read_data(path)
        #print nitro
        arr=[d[i][1:] for i in d]

        point_tree = spatial.cKDTree(arr)
        result=[]
        for j in range(len(nitro)):
                #print j
                li1=(point_tree.query_ball_point(nitro[j], ma))
                li2=(point_tree.query_ball_point(nitro[j], mi))
                #print li2
                re=list(map(lambda x: x+1,list(set(li1)-set(li2))))
                #print nitro_d[j],re
                re1=[]
                for i in re:
                	if d[i][0] in ['N','O']:
                		re1.append(i)
                result.append([nitro_d[j],re1])

        return result,d 

def distance(a,b):
    return math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2)

def connection_analysis(path,ma=3.0,mi=2.0):
	all_res={}
	res,d=pre_data(path,ma,mi)
	for a,li in res:
		for b in li:
			con=hb.connections('.'.join(path.split('.')[:-1])+'.xyz')
			lis = con.bfs(a-1,b-1)
			if len(lis)==4:
				dih=con.dihedral(lis)
				li=[a,b]
				li.sort()
				#print li
				all_res[tuple(li)]=[dih,distance(d[a][1:],d[b][1:]),d[a][0]+'-'+d[b][0],lis]

	return all_res

def write_o(path):
	f=open('results.txt','a')
	dic=connection_analysis(path)
	for i in dic:
		f.write(str(dic[i][1])+' '+str(dic[i][0])+' '+dic[i][2]+' '+path+'\n')
	f.close()



if __name__=='__main__':
	write_o(sys.argv[1])




