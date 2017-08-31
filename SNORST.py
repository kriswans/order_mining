"""
SNORST : Serial Number, Order Reporting & Search tool
author: Kris Swanson kriswans@cisco.com
"""

print('\n\n'+48*'*'+'\n\n')
print("Welcome to the SOF1 SNORST!")
print('\n\n'+48*'*'+'\n\n')

def SNORST():
    import re
    import time
    import datetime
    import sys
    import os

    os.chdir("Data")
    file_list=os.listdir()
    lfl=len(file_list)
    file_dict={}
    a=1

    while a <= lfl:
        file_dict.update({a:file_list[a-1]})
        a+=1

    for c in file_dict:
        print ("Select ("+str(c)+") to search file: "+ str(file_dict[c]))

    f_sel=input("Select file: ")
    f_sel_list=[]
    f_sel_list.append(file_dict[int(f_sel)])
    for n in f_sel_list:
        print (n)
    while f_sel != '':
        f_sel=input("Select file or hit <Enter> to continue: ")
        if f_sel != '':
            f_sel_list.append(file_dict[int(f_sel)])
            f_sel_list=set(f_sel_list)
            f_sel_list=list(f_sel_list)
            for n in f_sel_list:
                print (n)
        else:
            break

    print(f_sel_list)
    row_in_list=[]
    rl=[]
    for item in f_sel_list:
        f=open(item,'r')
        row_in_list=f.readlines()
        rl=row_in_list+rl

    len_rl=len(rl)

    cols=rl[0].split('\t')
    lc=(len(cols))



    a=1
    col_dict={}
    while a <= lc:
        col_dict.update({a:cols[a-1]})
        a+=1

    for c in col_dict:
        print ("Select ("+str(c)+") to include columns: "+ str(col_dict[c]))

    sel=input("Select columns: ")
    sel_list=[]
    index_list=[]
    sel_list.append(col_dict[int(sel)])
    index_list.append(sel)

    for items in sel_list:
        print (items)

    while sel != '':
        sel=input("\nSelect columns or hit <Enter> to continue to search: ")

        if sel != '':
            index_list.append(sel)
            sel_list.append(col_dict[int(sel)])
            print("\nColumns will be:\n")
            for items in sel_list:
                print (items)
        else:
            break
    len_sel_list=len(sel_list)
    item=1
    search_val=input('\nPlease enter search string: ')
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('_%Y-%m-%d_@_%H.%M.%S')
    out=open('report__'+search_val+'__'+st+'.xls','w')
    for names in sel_list:
        out.write(names)
        out.write('\t')
    out.write('\n')

    while item < len_rl:
        rs=re.search(search_val,rl[item])
        if rs != None:
            field_list=rl[item].split('\t')
            for idx in index_list:
                out.write(field_list[int(idx)-1])
                out.write("\t")
            out.write("\n")
        else:
            pass
        item+=1
    out.close()

if __name__=="__main__":
    SNORST()
