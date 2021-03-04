#!/usr/bin/python
import xlwt
import module
import sys
#import xlrd
#from xlutils.copy import copy as xl_copy

#metals=['Co','Rh','Ni','Pd','Pt','Ir','I']

def func(path,keyword,ref,d,n):
        filename=path
        file =open(filename,'r')
        for line in file:
                if 'Type' in line and keyword in line.strip().split():
                        d[(n,'bn')]=line.strip().split()[4:]
                        d[(n,'comment')]=path
                        ref=1
                if ref==1:
                        if 'Rho' in line.strip().split():
                                d[(n,'rho')]=line.strip().split()[2]
                        if 'DelSqRho' in line:
                                d[n,'DelSqRho']=line.strip().split()[2]
                        if 'Bond Ellipticity' in line:
                                d[n,'Bond Ellipticity']=line.strip().split()[3]
                        if 'HessRho_EigVals ' in line:
                                d[n,'HessianEigenValue0'] = line.strip().split()[2]
                                d[n,'HessianEigenValue1'] = line.strip().split()[3]
                                d[n,'HessianEigenValue2'] = line.strip().split()[4]
                        if 'V' in line.strip().split():
                                d[n,'V']=line.strip().split()[2]
                        if 'G' in line.strip().split():
                                d[n,'G']=line.strip().split()[2]
                        if 'K' in line.strip().split():
                                d[n,'K']=line.strip().split()[2]
                        if 'L' in line.strip().split():
                                d[n,'L']=line.strip().split()[2]
                                ref=0
                                n+=1
        file.close()

def check(string,p_id,d,index):
        # st = [O19, C18]
        a,b=string
        for i in p_id:
                if p_id[i]==string:
                        p_id[i]=d[(index-1,'K')]
                        return True
                elif p_id[i]==[b,a]:
                        p_id[i]=d[(index-1,'K')]
                        return True
        return False

def get_ids(path,suffix='_ah'):
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
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', DensityCriticalPointAcceptor \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        s,e=line.index('('),line.index(')')
                        n1=line.strip().split()[line.strip().split().index('(')-1]
                        l=line[s+1:e].split(',')
                        st=[n1+l[0].strip(),'H'+l[1].strip()]

                        if i2==0:
                                length=len(line)
                        lm[str(i2+1)+'.']=st
                        #lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
                        i2+=1
        return lm 

def addBCP(path,p_id):
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
                        lines[i-1]=' '.join(lines[i-1].strip().split())+', DensityCriticalPointAcceptor \n'
                if ref==2 or ref==3:
                        ref+=1
                if ref==4:
                        if i2==0:
                                if length<len(line):
                                        length=len(line)
                        try:
                                float(p_id[str(i2+1)+'.'])
                                lm[str(i2+1)+'.']=str(float(p_id[str(i2+1)+'.'])*627.51*-1/(0.529**3))
                        except TypeError:
                                lm[str(i2+1)+'.']='0.0'
                        #lines[i]=lines[i].strip()+' '+lmodes[i2]+'\n'
                        i2+=1
        j=0
        length+=1
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


def job(path, filename):
        ref=0
        d={}
        n=0

        #filename = path.split('.')[0]#filename+'.sum'#raw_input("Enter .sum path : ")
        func(path,'BCP',ref,d,n)
        #module.search_deep(path,func,['.sum'])


        #rb=xlrd.open_workbook('Data.xls', formatting_info=True)
        workbook = xlwt.Workbook()
        #workbook = xl_copy(rb)
        name='sheet1'
        sheet = workbook.add_sheet(name)

        sheet.write(0,0,'Bond')
        sheet.write(0,1,'Rho')
        sheet.write(0,2,'DelSqRho')
        sheet.write(0,3,'Bond Ellipticity')
        sheet.write(0,4,'V')
        sheet.write(0,5,'G')
        sheet.write(0,6,'K')
        sheet.write(0,7,'L')
        sheet.write(0,8,'HessianEigenValue0')
        sheet.write(0,9,'HessianEigenValue1')
        sheet.write(0,10,'HessianEigenValue2')
        sheet.write(0,11,'Comments')
        index=1
        max_d=-99999
        for i in d:
                a,b=i
                if a>max_d:
                        max_d=a
        print ('Points found from sum file',max_d)
        i_ref=1
        txt_path=filename+'.txt'#raw_input("Enter .txt path : ")
        p_id=get_ids(txt_path,suffix='_ah')
        #print p_id
        li=[]
        for i in range (max_d+1):
                if check(d[(index-1,'bn')],p_id,d,index):
                        #print index
                        li.append(index)
                index+=1

        for index in li:
                d[(index-1,'bn')]='-'.join(d[(index-1,'bn')])
                sheet.write(i_ref,0,d[(index-1,'bn')])
                sheet.write(i_ref,1,d[(index-1,'rho')])
                sheet.write(i_ref,2,d[(index-1,'DelSqRho')])
                sheet.write(i_ref,3,d[(index-1,'Bond Ellipticity')])
                sheet.write(i_ref,4,d[(index-1,'V')])
                sheet.write(i_ref,5,d[(index-1,'G')])
                sheet.write(i_ref,6,d[(index-1,'K')])
                sheet.write(i_ref,7,d[(index-1,'L')])
                sheet.write(i_ref,8,d[(index-1,'HessianEigenValue0')])
                sheet.write(i_ref,9,d[(index-1,'HessianEigenValue1')])
                sheet.write(i_ref,10,d[(index-1,'HessianEigenValue2')])
                sheet.write(i_ref,11,d[(index-1,'comment')])
                i_ref+=1

        print ('Making Excel file for aimall calculation...')
        workbook.save(filename+'_BCP.xls')
        return addBCP(txt_path,p_id)

if __name__=='__main__':
        job(sys.argv[1].split('.')[0])






