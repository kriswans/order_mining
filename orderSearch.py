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


    len_file=(len(l))
    search_val=''

    while search_val != 'exit':
        search_val=str(input("Enter search input for Part#, Serial, PO# or SO# (or exit to end program): "))
        if search_val =='exit':
            sys.exit()
        elif search_val=='':
            sys.exit()
        else:
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('_%Y-%m-%d_@_%H.%M.%S')
            out=open('report__'+search_val+'__'+st+'.xls','w')
            out.write("Serial#/PAK# \t CiscoPart# \t CiscoSO# \t CiscoPO# \t \n")

            i=0
            while i < len_file:
                rs=re.search(search_val,l[i])
                if rs != None:
                 print(l[i])
                 out.write(l[i]+'\n')
                i+=1
            out.close()
    sys.exit()

if __name__=='__main__':
    orderSearch()
