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
import json
import random


multi_formstart_files='''\
<html>
<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
<style>

ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: #333;
    font-family:verdana;
}

li {
    float: left;
}

li a {
    display: block;
    color: white;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
}

li a:hover:not(.active) {
    background-color: #111;
}

.active {
    background-color: lightgreen;
}
body {background-color: powderblue;}
h1 {
    color: black;
    text-align: left;
    font-family: verdana;
    font-size: 20px;
}


</style>
<body>
<ul>
  <li><a href="/">Home</a></li>
  <li><a href="mailto:kriswans@cisco.com">Contact</a></li>
  <li style="float:right"><a class="active" href="/logout">Logout</a></li>
</ul>
</br>
</br>
<h1></br>Source Files</h1></br></br>
<form id="form" action="" method="post">
    <div>
      <select multiple id="mymultiselect" size="25" name="mymultiselect[]">
'''

multi_formstart_columns='''\
<html>
<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
<style>

ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: #333;
    font-family:verdana;
}

li {
    float: left;
}

li a {
    display: block;
    color: white;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
}

li a:hover:not(.active) {
    background-color: #111;
}

.active {
    background-color: lightgreen;
}
body {background-color: powderblue;}
h1 {
    color: black;
    text-align: left;
    font-family: verdana;
    font-size: 20px;
}


</style>
<body>
<ul>
  <li><a href="/">Home</a></li>
  <li><a href="mailto:kriswans@cisco.com">Contact</a></li>
  <li style="float:right"><a class="active" href="/logout">Logout</a></li>
</ul>
</br>
</br>
<h1></br>Source Columns</h1></br></br>
<form id="form" action="" method="post">
    <div>
      <select multiple id="mymultiselect" size="25" name="mymultiselect[]">
'''

multi_formend='''\
      </select>
<input type="submit" value="submit">
</div>
</form>
</body>
'''

search_formstart='''\
<html>
<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
<style>

ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: #333;
    font-family:verdana;
}

li {
    float: left;
}

li a {
    display: block;
    color: white;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
}

li a:hover:not(.active) {
    background-color: #111;
}

.active {
    background-color: lightgreen;
}
body {background-color: powderblue;}
h1 {
    color: black;
    text-align: left;
    font-family: verdana;
    font-size: 20px;
}

p1 {

    color: green;
    text-align: left;
    font-family: verdana;
    font-size: 20px;
}
p2 {

    color: red;
    text-align: left;
    font-family: verdana;
    font-size: 20px;
}
p3 {

    color: black;
    text-align: left;
    font-family: verdana;
    font-size: 16px;
}
</style>
<body>
<ul>
  <li><a href="/">Home</a></li>
  <li><a href="mailto:kriswans@cisco.com">Contact</a></li>
  <li style="float:right"><a class="active" href="/logout">Logout</a></li>
</ul>
</br>
</br>
'''

search_formend='''\
  <p3>

<form method="POST">
    </br>
    Type in 'OR' SEARCH variables seperated by ',':
    </br>
    <input name="search">
    </br>
    </br>
    Type in 'AND' SEARCH variables seperated by ',':
    </br>
    <input name="search_AND">
    </br>
    </br>
    Type in EXCLUDE variables seperated by ',':
    </br>
    <input name="exclude">
    </br>
    </br>
    <input type="submit">
</form>
</p3>
</body>

'''

result_table_start='''\
<!DOCTYPE html>
<html>
<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
<head>
<style>
.navbar {
    overflow: hidden;
    background-color: #333;
    font-family: verdana;
}

.navbar a {
    float: left;
    font-size: 16px;
    color: white;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
}

.dropdown {
    float: left;
    overflow: hidden;
}

.dropdown .dropbtn {
    font-size: 16px;
    border: none;
    outline: none;
    color: white;
    padding: 14px 16px;
    background-color: inherit;
    font-family: inherit;
    margin: 0;
}

.navbar a:hover, .dropdown:hover .dropbtn {
    background-color:  #111;

}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: #f9f9f9;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
}

.dropdown-content a {
    float: none;
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
    text-align: left;
}

.dropdown-content a:hover {
    background-color: #333;
}

.dropdown:hover .dropdown-content {
    display: block;
}
.active {
    background-color: lightgreen;
}
body {background-color: powderblue;}
h1 {
    color: black;
    text-align: left;
    font-family: verdana;
    font-size: 20px;
}
h2 {
    color: black;
    text-align: left;
    font-family: verdana;
    font-size: 20px;
}

table {
    font-family: verdana;
    border-collapse: collapse;
    width: 100%;
}

td, th {

    font-family: verdana;
    border: 1px solid powderblue;
    text-align: left;
    padding: 3px;
}
td:hover {
    background-color: lightgreen;}

tr:nth-child(even) {
    background-color: white;
}
</style>
</head>
<body>

<div class="navbar">
  <a href="/">Home</a>
  <a href="maito:kriswans@cisco.com">Contact</a>
  <a href="/return-files/">Download Current Results</a>
  <div class="dropdown">
    <button class="dropbtn">Search Within Results
      <i class="fa fa-caret-down"></i>
    </button>
    <div class="dropdown-content">
      <a href="#"><form method="POST"><input name="search"> :OR Search</form></a>
      <a href="#"><form method="POST"><input name="search_AND"> :AND Search</form></a>
      <a href="#"><form method="POST"><input name="exclude"> :Exclude</form></a>
      <a href="#"><input type="button" value="Search"></a>
    </div>

  </div>

</div>
</br>
</br>
<table>
'''

result_table_end='''\
</table>

</body>
</html>
'''

def aquire_files():

    '''
    Clean up some older files, 15 minutes old seems ok.
    '''
    for i  in os.listdir('templates/'):
        if '.html' in i:
            try:
            	j=i.lstrip('resfile-').rstrip('.html')
            	j=int(float(j))
            	if int(time.time()) > j+900 :
            		os.remove('templates/'+i)
            except:
                pass

    for i  in os.listdir():
        if '.json' in i:
        	j=i.lstrip('rlj-').rstrip('.json')
        	j=int(float(j))
        	if int(time.time()) > j+900 :
        		os.remove(i)

    for i  in os.listdir():
        if '.xls' in i:
            j=i.split('-')
            j=j[2].rstrip('.xls')
            j=int(float(j))
            if int(time.time()) > j+900 :
                os.remove(i)

    file_template=str(time.time())+'.html'
    file_list=os.listdir()
    if "Data" in file_list:
        file_list=os.listdir("Data")
    else:
        os.makedirs("Data")
        print("\n\nCreated 'Data' directory. Populate with tab delimited files to search and rerun program. Exiting...\n\n")
        sys.exit()
    current_temp='templates/'+file_template
    with open (current_temp, 'w') as f:
        f.write(multi_formstart_files)
        f.write('\n')
        for i in file_list:
            i=str(i)
            f.write('           <option value="'+i+'">'+i+'</option>')
            f.write('\n')
        f.write('\n')
        f.write(multi_formend)
    return file_template

def get_columns(fileselect):
    column_template=str(time.time())+'.html'
    rows_total=[]

    for i in fileselect:
        i=str(i)
        i="Data/{i}".format(i=i)
        with open (i, 'r') as f:
            rows=f.readlines()
            rows_total=rows + rows_total

    columns=rows_total[0].split('\t')
    current_temp='templates/'+column_template
    with open (current_temp, 'w') as f:
        f.write(multi_formstart_columns)
        f.write('\n')
        for i in columns:
            i=str(i)
            f.write('           <option value="'+i+'">'+i+'</option>')
            f.write('\n')
        f.write('\n')
        f.write(multi_formend)
    return column_template, columns, rows_total

def get_search(colselect,fileselect):
    search_template=str(time.time())+'.html'
    current_temp='templates/'+search_template
    with open (current_temp, 'w') as f:
        f.write(search_formstart)
        f.write('\n')
        f.write('<h1>SNORST Search Menu</h1>')
        f.write('<p1>')
        f.write('</br>The files being searched will be:  </br></br>')
        for i in fileselect:
            i=str(i)
            f.write('**')
            f.write(i)
            f.write('**')
            f.write('</br>')
            f.write('\n')
        f.write('</p1>')
        f.write('<div> </div>')
        f.write('<p2>')
        f.write('</br>The columns being searched will be:  </br></br>')
        for i in colselect:
            i=str(i)
            f.write('**')
            f.write(i)
            f.write('**')
            f.write('</br>')
            f.write('\n')
        f.write('</p2>')
        f.write(search_formend)
    return search_template

def get_result(colselect,fileselect,search,search_AND,exclude):

    rows_total=[]
    for i in fileselect:
        i=str(i)
        i="Data/{i}".format(i=i)
        with open (i, 'r') as f:
            rows=f.readlines()
            rows_total=rows + rows_total

    columns=rows_total[0].split('\t')
    colselect_indices=[columns.index(i) for i in columns if i in colselect]
    rts_list=[]
    for i in rows_total:
        rt_list_temp=[]
        rts=i.split('\t')
        for j in colselect_indices:
            rt_list_temp.append(rts[j])
        rts_list.append(rt_list_temp)



    result_list=[]

    search_list=[]
    if search != ['']:
        for i in search:
            for j in rts_list:
                j=json.dumps(j)
                '''need to pass a string for i in order to search'''
                if bool(re.search(i,j)) == True:
                    result_list.append(j)
                else:
                     pass

    if search_AND != []:
        AND_search_list=[]
        if result_list !=[]:
            for i in result_list:
                temp_list=[]
                for j in search_AND:
                    if bool(re.search(j,i)) == True:
                            temp_list.append(i)
                    if len(temp_list) == len(search_AND):
                        AND_search_list.append(i)
                    else:
                        pass
            result_list=AND_search_list

        if result_list == []:
            for i in rts_list:
                temp_list=[]
                i=json.dumps(i)
                for j in search_AND:
                    if bool(re.search(j,i)) == True:
                        temp_list.append(i)
                if len(temp_list) == len(search_AND):
                    AND_search_list.append(i)
                else:
                    pass
            result_list=AND_search_list




    filtered_list=[]
    if exclude != ['']:
        for i in result_list:
            hit_list=[]
            i=json.dumps(i)
            for j in exclude:
                if bool(re.search(j,i)) == True:
                    i=json.loads(i)
                    hit_list.append(i)
                else:
                    pass
            if hit_list == []:
                i=json.loads(i)
                filtered_list.append(i)
        result_list=filtered_list

    result_list_pre=result_list
    result_list=list(set(result_list))

    temp_list=[]
    for i in result_list:
        c=str(result_list_pre.count(i))
        i=json.loads(i)
        i.append(c)
        temp_list.append(i)

    result_list=temp_list

    template_columns=[]
    for i in colselect_indices:
        column=columns[i]
        template_columns.append(column)
    template_columns.append('Count')

    result_list_json='rlj-'+str(time.time())+'.json'

    with open (result_list_json,'w') as rlj:
        json.dump(result_list,rlj)

    result_file='resfile-'+str(time.time())+'.html'
    with open ('templates/'+result_file, 'w') as rf:
        rf.write(result_table_start)
        rf.write('<tr>')
        for i in template_columns:
            rf.write('<th>')
            rf.write(i)
            rf.write('</th>')
        rf.write('</tr>')
        for i in result_list:
            rf.write('<tr>')
            for j in i:
                rf.write('<td>')
                rf.write(j)
                rf.write('</td>')
            rf.write('</tr>')
        rf.write(result_table_end)

    result_template=result_file
    return result_template, result_list_json, template_columns

def get_download(dl_result_list_json,dl_template_columns):

    with open(dl_result_list_json,'r') as rlj:
        dl_result_list=json.load(rlj)

    rn=str(abs(hash(random._sha512())))+'-'
    file_download='dl-'+rn+str(time.time())+'.xls'
    with open (file_download, 'w') as fd:
        for i in dl_template_columns:
            fd.write(i)
            fd.write('\t')
        fd.write('\n')
        for i in dl_result_list:
            for j in i:
                fd.write(j)
                fd.write('\t')
            fd.write('\n')
    return file_download
