import os
import sys
def lmode(path):
		file = open(path,'r', encoding="ascii", errors="surrogateescape")
		filename=path.split('/')[-1].split('.')[0]
		if len(filename)<4:
				return
		global d
		filename=path
		d=[]
		ref_l=0
		ref_o,lm=0,{}
		p_ref1,p_ref2=0,0
		for line in file:
				try:
						p_ref1+=1
						if 'Program LOCALMODES' not in line and p_ref1>5 and p_ref2==0:
								return d
						elif 'Program LOCALMODES' in line:
								p_ref2=1
						if 'Local mode properties:' in line:
								ref_l=1
						if '------------------' in line and ref_l>0:
								ref_l+=1
						elif ref_l==3:
								if 'Unphysical' in line:
									d.append('(?)')
									continue
								bond,q_n,ka,wa=line.strip().split()[5:8]+[line.strip().split()[9]]
								if '?' in line:
										d.append(wa+'?')
								else:
										d.append(wa)
						if ref_l==4:
								ref_l=0
				except TypeError:
					print ('Error in line',line)
					pass
		return d

def addFreq(path,suffix):
	lmodes=lmode(path.split('/')[-1].split('.')[0]+suffix+'.out')
	f=open(path,'r')
	lines=f.readlines()
	f.close()
	i=-1
	i2=0
	ref=0
	lm={}
	length=0
	for line in lines:
		i+=1
		if ref==5:
			break
		if 'File format' in line:
			ref+=1
		if len(line.strip().split())==0 and ref>0:
			ref+=1
		if ref==2:
			if suffix=='_dh':
				lines[i-1]=' '.join(lines[i-1].strip().split())+', Donar_H_Frequency \n'
			else:
				lines[i-1]=' '.join(lines[i-1].strip().split())+', Acceptor_H_Frequency \n'
		if ref==2 or ref==3:
			ref+=1
		if ref==4:
			if i2==0:
				length=len(line)
			lm[str(i2+1)+'.']=lmodes[i2]
			#lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
			i2+=1
	j=0
	
	for line in lines:
		if len(line.strip().split())==0:
			j+=1
			continue
		if line.strip().split()[0] in lm:
			string=lm[line.strip().split()[0]]
			lines[j]=lines[j][:-1]+' '*(length-len(lines[j])+2)+string+'\n' 
		j+=1
	g=open(path,'w')
	g.write(''.join(lines))
	g.close()
	return lm

'''
for i in os.listdir('.'):
	if i[-4:]=='.txt':
		addKa(i)
print 'Done!!'
'''

#addKa(sys.argv[1])


















