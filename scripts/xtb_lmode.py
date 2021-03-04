#xtb_lmode
import os
import sys
import atom_data

def sub_s(lis):
	sub_s,ref='',0
	for i in lis:
		if ref%5==0:
			sub_s+='\n    '+i+'    '
		else:
			sub_s+=i+'    '
		ref+=1
	return sub_s

def get_ids(path,suffix):
        f=open(path,'r')
        lines=f.readlines()
        f.close()
        ref=0
        st=''
        for line in lines:
                if ref==5:
                        break
                if 'File format' in line:
                        ref=1
                if len(line.strip().split())==0 and ref>0:
                        ref+=1
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        #if suffix=='_dh':
                        s,e=line.index('('),line.index(')')
                        n1=line.strip().split()[line.strip().split().index('(')-1]
                        l=line[s+1:e].split(',')
                        k = line.strip().split()[2]
                        try:
                            int(k)
                        except ValueError:
                            k = line[44:51].strip()
                        a, h, d = [l[0].strip(),l[1].strip(),k]
                        #print a, h, d
                        l=line.strip().split()
                        if suffix=='_dh':
                                
                                st+=h+' '+d+' 0 0 : '+l[-3]+'\n'
                        else:
                                st+=h+' '+a+' 0 0 : '+l[-3]+'\n'
                                 
                        
        return st

def make_dat(filename, path):
        filename=filename[:-4]+'.xyz'
        #print (path)#filename[:-4]+'_hessian'
        h=open(path,'r')
        hess0=h.readlines()[1:]
        h.close()
        hess=[]
        for line in hess0:
                hess+=line.strip().split()
        amass,za,xyz=[],[],[]
        f=open(filename,'r')
        lines=f.readlines()
        f.close()
        data=atom_data.data(sys.argv[0])
        sym=atom_data.symbol_dict(sys.argv[0])
        #print sym
        for line in lines[2:]:
                if len(line.strip().split())==0:
                        continue

                s,x,y,z=line.strip().split()
                amass.append(data[sym[s]]['atomicMass'][:-3])
                za.append(str(sym[s]))
                x = str(1.88973*float(x))
                y = str(1.88973*float(y))
                z = str(1.88973*float(z))
                xyz+=[x,y,z]

        g=open(filename[:-4]+'.dat','w')
        s=''
        s+='Eventually the world will end in singularity !! \n'
        s+='NATM\n   '+lines[0].strip().split()[0]+'\nAMASS'+sub_s(amass)
        s+='\nZA'+sub_s(za)
        s+='\nXYZ'+sub_s(xyz)
        s+='\nNOAPT'
        s+='\nFFX'+sub_s(hess)
        g.write(s)
        g.close()

def get_inp():
    tp = open(os.path.join(os.path.split(sys.argv[0])[0], 'main_input'))
    lines = tp.readlines()
    tp.close()

    dic={}
    for line in lines:
        if '#' in line or len(line.strip().split())==0:
            continue
        a,b=line.strip().split()
        dic[a]=b 
    return dic


def make_alm(filename, suffix, path):
        make_dat(filename, path)
        #path=sys.argv[1]
        filename=filename.split('/')[-1].split('.')[0]
        s1="""
 $contrl
   qcprog="ALMODE"
   iprint=0
   isymm = 1
   ifsave=.false.
 $end

$qcdata
 """
        s2='fchk="'+filename+'.dat"'
        s3="""$end

$LocMod $End
"""
        f=open(filename+suffix+'.alm','w')
        f.write(filename+'\n')
        f.write(s1)
        f.write(' '+s2+'\n')
        f.write(s3)
        f.write(get_ids(filename + '.txt',suffix))
        f.close()

        inp_d = get_inp()

        os.system(inp_d['lmode_path']+ " -b "+'< '+filename+suffix+'.alm' +' >'+' '+filename+suffix+'.out')
	

if __name__ == '__main__':
	make_alm(sys.argv[1], '')
	






