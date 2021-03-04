#automate in directory
import xlwt
import os
import sys
import hbond_out
import make_xl_ab

def make_excel(d,suffix):

	wb=xlwt.Workbook() 
	sheet = wb.add_sheet('Version1')
	col=0
	for bond in d:
		row=0
		lis=d[bond]
		sheet.write(row,col,bond)
		row+=1
		for a,b,c in lis:
			sheet.write(row,col,float(a))
			if suffix=='_ah':
				sheet.write(row,col+1,float(b))
			else:
				sheet.write(row,col+1,float(c))
			row+=1
		col+=2
			
	print 'Making Excel files for '+suffix+' ...'		
	if suffix=='_ah':	
		wb.save('allBonds_accep_xtb.xls')
	else:
		wb.save('allBonds_donars_xtb.xls')




def make_output():
	dic={}
	for i in os.listdir(sys.argv[1]):

		if i[-4:]=='.xyz':
			print 'Procession the file '+i
			#hbond_out.job(i)

			kd=make_xl_ab.xl(i.split('/')[-1].split('.')[0]+'.txt')
			for j in kd:
				if j not in dic:
					dic[j]=kd[j]
				else:
					dic[j]+=kd[j]
			print '\n'
	make_excel(dic,'_ah')
	make_excel(dic,'_dh')



if __name__ == "__main__":
	make_output()

