"""
SNORST : Serial Number, Order Reporting & Search Tool
author: Kris Swanson kriswans@cisco.com
Version: 0.5
"""

import re
import time
import datetime
import sys
import os

print('\n\n'+64*'*'+'\n\n')
print("Welcome to the SOF1 SNORST!\n")
print("(S)erial (N)umber, (O)rder (R)eporting & (S)earch (T)ool")
print('\n\n'+64*'*'+'\n\n')

def SNORST():


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

    print('\n\n...Reading column headers...\n\n')

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
    search_input='None'
    val_list=[]
    excl_list=[]
    print("\n\n"+64*'#')
    print("\n###Build Search INCLUDE List!!!!!!!Build Search INCLUDE List####\n\n")
    print(64*'#'+'\n\n')
    print("\nNOTE: Enter Individual search INCLUDE values that will be wildcarded and chained with 'OR' operator\n\n")
    print("\nNOTE: After INCLUDE List completion, just hit <Enter to continue with building the exclude list\n\n")
    while search_input != '':
        search_input=input("\n\nEnter individual search INCLUDE values, then hit <Enter> to continue: ")
        val_list.append(search_input)
        print("\nYour INCLUDED search variables will be:\n")
        for val in val_list:
            print(val)

    print("\n\n"+64*'#')
    print("\n###Build Search EXCLUDE List!!!!!!!Build Search EXCLUDE List####\n\n")
    print(64*'#'+'\n\n')
    print("\nNOTE: Enter Individual search EXCLUDE values that will be wildcarded and chained with 'OR' operator\n\n")
    print("\nNOTE: After EXCLUDE List completion, just hit <Enter to continue generating search output files.\n\n")
    search_input='None'
    while search_input != '':
        search_input=input("\n\nEnter individual search EXCLUDE values, then hit <Enter> to continue: ")
        excl_list.append(search_input)
        print("\nYour EXCLUDED search variables will be:\n")
        for val in excl_list:
            print(val)


    excl_list.pop()
    val_list.pop()

    if len(excl_list) == 0:
        excl_list=['!NO_EXCL_VALUE!']
    if len(val_list) == 0:
        val_list=['!NO_INCL_VALUE!']

    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('_%Y-%m-%d_@_%H.%M.%S')
    filename='inc_'+str(val_list)+'exc_'+str(excl_list)+st+'.xls'
    rec_filename='rec_'+'inc_'+str(val_list)+'exc_'+str(excl_list)+st+'.xls'
    out=open(filename,'w')
    rec=open(rec_filename,'w')
    print("\n\nWriting output to file: "+filename+'.xls based on search hits on ALL fields in the file input.\n')
    print("\n\nWriting output to file: "+rec_filename+'.xls based on the search hits on the selected output columns.\n\n')

    for nums in index_list:
        out.write(col_dict[int(nums)])
        out.write('\t')
        rec.write(col_dict[int(nums)])
        rec.write('\t')
    out.write('\n')
    rec.write('\n')

    hit_list=[]
    stop_list=[]
    item=1


    while item < len_rl:
        out_list=[]
        hit_list=[]
        stop_list=[]
        for val in val_list:
            inc=re.search(val,rl[item])
            hit_list.append(inc)
        hit_list=list(set(hit_list))

        for ex in excl_list:
            exc=re.search(ex,rl[item])
            stop_list.append(exc)
        stop_list=list(set(stop_list))



        if hit_list != [None] and stop_list == [None]:
            field_list=rl[item].split('\t')
            for idx in index_list:
                out.write(field_list[int(idx)-1])
                out.write("\t")
                out_list.append(field_list[int(idx)-1])
                len_out_list=len(out_list)
            out.write("\n")

        for val in val_list:
            inc=re.search(val,str(out_list))
            if inc != None:
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
    print(crunch_file+' eliminates and counts duplicate lines in '+rec_filename)
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



if __name__=="__main__":
    SNORST()
    while True:
        choice=input("\n\n\nWould you like to run the tool again? : [Y] or[N]: ")
        if choice == 'Y':
            os.chdir('..')
            SNORST()
        elif choice == 'N':
            print('\n\nGoodbye\n\n')
            sys.exit()
        else:
            print("\n\nPlease enter 'Y or 'N'\n\n")
            continue
