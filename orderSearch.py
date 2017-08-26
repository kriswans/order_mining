"""
version 0.2
author kriswans@cisco.com
This tool performs a regex search of all fields and selectively outputs rows based on search criteria
It will output to console and a tiemstamped tab delimited file.

The input is fixed to tab delimited files with columns Serial#/PAK#, CiscoPart#, CiscoSO#, CiscoPO#

The input is seperated into 3 different FYs of Data named FY15.txt, FY16.txt, and FY17.txt .
"""
import re
import time
import datetime
import sys

print("Welcome to the SOF1 order search tool!\n\n")
print("Data is current as of 18SEP17.\n\n")

def orderSearch():
    try:
        start=int(input("Input starting 'Shipped' FY: 1=FY15, 2=FY16, 3=FY17: "))
        if start==1:

            f1=open('FY15.txt','r')
            lf1=f1.readlines()
            f1.close()

            f2=open('FY16.txt','r')
            lf2=f2.readlines()
            f2.close()

            f3=open('FY17.txt','r')
            lf3=f3.readlines()
            f3.close()

            l=set(lf1+lf2+lf3)
            l=(list(l))

        elif start==2:

            f2=open('FY16.txt','r')
            lf2=f2.readlines()
            f2.close()

            f3=open('FY17.txt','r')
            lf3=f3.readlines()
            f3.close()

            l=set(lf2+lf3)
            l=(list(l))

        elif start ==3:

            f3=open('FY17.txt','r')
            lf3=f3.readlines()
            f3.close()

            l=set(lf3)
            l=(list(l))
        else:
            sys.exit()
    except:
        print('\n\nNeed to enter 1,2, or 3. Exiting...')
        sys.exit()


    columns=[]
    limit_out='0'
    choices={'1': 'Serial#','2':'Part#','3':'SO#','4':'PO#'}

    print("\nLimit output columns?\n\nType: '1' for SN, '2' for Part#, '3' for SO#, '4' for PO#, 'a' for all, or <return> to continue.\n" )

    while limit_out is '0' or limit_out is '1' or limit_out is '2' or limit_out is '3' or limit_out is '4':

        limit_out=str(input(":"))
        columns.append(limit_out)
        sc=set(columns)
        columns=list(sc)
        try:
            for val in columns:
                print(choices[val])
        except:
            if limit_out is 'a':
                pass
            elif limit_out is '':
                columns.remove('')
            else:
                columns.reverse()
                columns.pop()
                pass


    if 'a' in columns:
        columns=['1','2','3','4']

    c=set(columns)
    columns=list(c)
    columns.sort()

    print("Output columns will be:\n")
    for val in columns:
        print(choices[val])

    len_file=(len(l))
    search_val=''

    while search_val != 'exit':
        search_val=str(input("\nEnter search input for Part#, Serial, PO# or SO# (or 'exit' or return to end program): "))
        if search_val =='exit':
            sys.exit()
        elif search_val=='':
            sys.exit()
        else:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('_%Y-%m-%d_@_%H.%M.%S')
            out=open('report__'+search_val+'__'+st+'.xls','w')
            for fields in columns:
                out.write(choices[fields]+'\t')
            out.write('\n')

            i=0
            lc=len(columns)
            while i < len_file:
                rs=re.search(search_val,l[i])
                if rs != None:
                    m=l[i].split('\t')
                    for z in columns:
                        z=int(z)
                        z=z-1
                        print(m[z])
                        out.write(m[z]+'\t')
                    out.write('\n')
                i+=1
            out.close()
    sys.exit()

if __name__=='__main__':
    orderSearch()
