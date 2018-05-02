from flask import Flask, request, render_template, redirect, session,send_file,flash
from SNORST_classes import aquire_files as af
from SNORST_classes import get_columns as gc
from SNORST_classes import get_search as gs
from SNORST_classes import get_result as gr
from SNORST_classes import get_download as gd
import time
import os




def snorst_fe():
    app = Flask(__name__)

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'



    @app.route('/',methods=['GET'])
    def files():
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            file_template=af()
            session['file_template']=file_template
            return render_template(file_template)

    @app.route('/', methods=['POST'])
    def files_multi_post():
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            try:
                fileselect = request.form.getlist('mymultiselect[]')
                column_template, columns, rows_total=gc(fileselect)
                session['column_template']=column_template
                session['fileselect']=fileselect
                return redirect('columns')
            except:
                session.pop('results','file_template')
                session.pop('search_template','fileselect')
                session.pop('column_template','colselect')
                return redirect('/')

    @app.route('/login', methods=['POST'])
    def do_admin_login():
        if request.form['password'] == 'SOF1TEAM' and request.form['username'] == 'sof1team':
            session['logged_in'] = True
        else:
            flash('wrong password!')
        return redirect('/')

    @app.route("/logout")
    def logout():
        session['logged_in'] = False
        return redirect('/')

    @app.route('/columns', methods=['GET'])
    def columns():
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            try:
                column_template=session['column_template']
                return render_template (column_template)
            except:
                session.pop('results','file_template')
                session.pop('search_template','fileselect')
                session.pop('column_template','colselect')
                return redirect('/')


    @app.route('/columns', methods=['POST'])
    def columns_multi_post():
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            colselect = request.form.getlist('mymultiselect[]')
            session['colselect']=colselect
            fileselect=session['fileselect']
            search_template=gs(colselect,fileselect)
            session['search_template']=search_template
            return redirect ('search')

    @app.route('/search', methods=['GET'])
    def search():
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            try:
                search_template=session['search_template']
                return render_template (search_template)
            except:
                session.pop('results','file_template')
                session.pop('search_template','fileselect')
                session.pop('column_template','colselect')
                return redirect('/')

    @app.route('/search', methods=['POST'])
    def search_post():
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            try:
                search=request.form['search']
                search_AND=request.form['search_AND']
                exclude=request.form.get('exclude')
                exclude=exclude.split(',')
                search=search.split(',')
                search_AND=search_AND.split(',')
                colselect=session['colselect']
                fileselect=session['fileselect']
                search_template=session['search_template']
                column_template=session['column_template']
                file_template=session['file_template']
                os.remove('templates/'+search_template)
                os.remove('templates/'+column_template)
                os.remove('templates/'+file_template)
                result_template, result_list_json, template_columns=gr(colselect,fileselect,search,search_AND,exclude)
                session['results']=[result_template,result_list_json,template_columns]
                return redirect('result')

            except KeyError:
                session.pop('results','file_template')
                session.pop('search_template','fileselect')
                session.pop('column_template','colselect')
                return redirect('/')


    @app.route('/result', methods=['GET'])
    def result():
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            try:
                result_template,result_list_json,template_columns=session['results']
                dl_template_columns=template_columns
                dl_result_list_json=result_list_json
                session.pop('results','file_template')
                session.pop('search_template','fileselect')
                session.pop('column_template','colselect')
                session['dl_results']=dl_template_columns,dl_result_list_json
                return render_template (result_template)
            except KeyError:
                session.pop('results','file_template')
                session.pop('search_template','fileselect')
                session.pop('column_template','colselect')
                return redirect('/')




    @app.route('/return-files/',methods=['GET'])
    def downloadfile():
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            dl_template_columns,dl_result_list_json=session['dl_results']
            file_download=gd(dl_result_list_json,dl_template_columns)
            return send_file(file_download, as_attachment=True)


    app.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':
    snorst_fe()
