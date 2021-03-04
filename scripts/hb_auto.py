#automate in directory
import xlwt
import os
import sys
import hbond_out
import make_xl

def make_excel(d,suffix):
	bonds={}
	b,f=[],[]
	m=-9999
	for i in d:
	 	#b=d[i]
	 	f.append(i)
	 	for j in d[i]:
	 		if j not in b:
	 			b.append(j)
	 		bonds[j,i]=d[i][j]
	 		if m<len(d[i][j]):
	 			m=len(d[i][j])

	wb=xlwt.Workbook() 
	sheet = wb.add_sheet('Version1')
	r=0
	mul=-1
	for i in b:
		mul+=1
		c=0
		r=(m+3)*mul
		sheet.write(r,c,i)
		for j in f:
			r=(m+3)*mul+1
			sheet.write(r,c,j)
			if (i,j) not in bonds:
				c+=2
				r+=1
				continue
			lis=bonds[i,j]
			r+=1
			for k in lis:
				sheet.write(r,c,float(k[0]))
				if suffix=='_ah':
					sheet.write(r,c+1,float(k[1]))
				else:
					sheet.write(r,c+1,float(k[2]))
				r+=1
			c+=2
			
	print 'Making Excel files for '+suffix+' ...'		
	if suffix=='_ah':	
		wb.save('acceptors.xls')
	else:
		wb.save('donars.xls')




def make_output():
	dic={}
	for i in os.listdir(sys.argv[1]):
		if i[-5:]=='.fchk':
			print 'Procession the file '+i
			hbond_out.job(i)
			dic[i]=make_xl.xl(i.split('/')[-1].split('.')[0]+'.txt')
			print '\n'
	make_excel(dic,'_ah')
	make_excel(dic,'_dh')



if __name__ == "__main__":
	make_output()

