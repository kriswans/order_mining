"""
SNORST : Serial Number, Order Reporting & Search Tool
author: Kris Swanson kriswans@cisco.com
Version: 0.3
"""

print('\n\n'+64*'*'+'\n\n')
print("Welcome to the SOF1 SNORST!\n")
print("(S)erial (N)umber, (O)rder (R)eporting & (S)earch (T)ool")
print('\n\n'+64*'*'+'\n\n')

def SNORST():
    import re
    import time
    import datetime
    import sys
    import os

    file_list=os.listdir()
    if "Data" in file_list:
        os.chdir("Data")
        file_list=os.listdir()
        lfl=len(file_list)
        file_dict={}
    else:
        os.makedirs("Data")
        print("\n\nCreated 'Data' directory. Populate with tab delimited files to search and rerun program. Exiting...\n\n")
        sys.exit()
    a=1

    while a <= lfl:
        file_dict.update({a:file_list[a-1]})
        a+=1

    for c in file_dict:
        print ("Select ("+str(c)+") to search file: "+ str(file_dict[c]))

    try:
        f_sel=input("\nSelect file: ")
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
    except:
        print("\nNo file selected. Exiting... ")
        sys.exit()

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

    try:
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
                sel_list=set(sel_list)
                sel_list=list(sel_list)
                index_list=set(index_list)
                index_list=list(index_list)
                index_list.sort()
                print("\nColumns will be:\n")
                for items in index_list:
                    print (col_dict[int(items)])
            else:
                break
    except:
        print("\nNo columns selected. Exiting ...")
        sys.exit()

    search_val='None'

    while search_val != '':
        item=1
        search_val=input('\nPlease enter search string or <Enter> to exit: ')
        if search_val != '':
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('_%Y-%m-%d_@_%H.%M.%S')
            rec_filename='report_recurs_'+search_val+'__'+st+'.xls'
            out=open('report__'+search_val+'__'+st+'.xls','w')
            rec=open(rec_filename,'w')
            print("\n\nWriting output to file:"+' report__'+search_val+'__'+st+'.xls\n')
            print("\n\nWriting output to file:"+' report_recurs_'+search_val+'__'+st+'.xls\n\n')
            for nums in index_list:
                out.write(col_dict[int(nums)])
                out.write('\t')
                rec.write(col_dict[int(nums)])
                rec.write('\t')
            out.write('\n')
            rec.write('\n')

            while item < len_rl:
                out_list=[]
                rs=re.search(search_val,rl[item])
                if rs != None:
                    field_list=rl[item].split('\t')
                    for idx in index_list:
                        out.write(field_list[int(idx)-1])
                        out.write("\t")
                        out_list.append(field_list[int(idx)-1])
                        len_out_list=len(out_list)
                    out.write("\n")
                    rec_search=re.search(search_val,str(out_list))
                    if rec_search != None:
                        for thing in out_list:
                            rec.write(thing)
                            rec.write('\t')
                        rec.write("\n")
                    else:
                        pass

                else:
                    pass
                item+=1
            out.close()
            rec.close()

            crunch_file='crunch_'+rec_filename
            crunch=open(crunch_file,'w')
            print("\n\nWriting"+crunch_file+"\n\n")
            dup_file=open(rec_filename,'r')
            dup_list=dup_file.readlines()
            crunch.write(dup_list[0].rstrip('\n')+'\tCount/Occurences\n')
            del dup_list[0]
            dup_set=set(dup_list)
            for item in dup_set:
                crunch.write(item.rstrip('\n')+'\t'+str(dup_list.count(item)))
                crunch.write('\n')
            crunch.close()
            dup_file.close()



        else:
            print("\n\nExiting Program\n\n")
            time.sleep(2)
            sys.exit()

if __name__=="__main__":
    SNORST()
