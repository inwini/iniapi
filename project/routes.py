""" """
from flask import Blueprint, render_template, redirect, url_for, jsonify, request, session, send_file
from flask_login import current_user, login_required, logout_user
from .models import db, User, Build, Department, Build_Log
from xlsxwriter.workbook import Workbook
from werkzeug import secure_filename
from datetime import datetime
from io import BytesIO
import pandas as pd
import numpy as np
import time
import json
import os
import math

EXCELMIME="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

basedir = os.path.abspath(os.path.dirname(__file__))

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']

def equation_sum(a,b,c):
    api = a
    temp = c
    apio = b

    if api > 52.1:
        k0 = 192.4571
        k1 = 0.2438
    elif api <= 37:
        k0 = 103.872
        k1 = 0.2701
    else:
        k0 = 330.301
        k1 = 0

    delta = temp - 60
    rho = (141.5 * 999.012)/(131.5 + api)
    alpha = (k0/rho**2) + (k1/rho)
    ex = (alpha) * (delta) * (1 + 0.8*(alpha)*(delta)) * (-1)
    expo = math.exp(ex)
    apif = (141.5 * 999.012 * (expo))/(rho) - 131.5

    aa = float(apif)
    aaa = format(aa, '.2f')

    return aaa

def equation_error(a,b,c):

    api = float(a)
    temp = float(c)
    apio = float(b)

    if api > 52.1:
        k0 = 192.4571
        k1 = 0.2438
    elif api <= 37:
        k0 = 103.872
        k1 = 0.2701
    else:
        k0 = 330.301
        k1 = 0

    delta = temp - 60
    rho = (141.5 * 999.012)/(131.5 + api)
    alpha = (k0/rho**2) + (k1/rho)
    ex = (alpha) * (delta) * (1 + 0.8*(alpha)*(delta)) * (-1)
    expo = math.exp(ex)
    apif = (141.5 * 999.012 * (expo))/(rho) - 131.5

    aa = float(abs(apif-apio))
    aaa = format(aa, '.3f')

    return  aaa

@main_bp.route('/export-search',  methods = [ 'GET'])
def excel():
    
    if request.method == 'GET':
        
        user_data = User.query.filter_by(id=current_user.id).first()
        
        build_data = Build.query.filter_by(user_id=user_data.id).first()
        
        if request.args.get("date_start") != None and request.args.get("time_start") != None and request.args.get("date_end") != None and request.args.get("time_end") != None and request.args.get("department") != None and request.args.get("department") != "0":
            
            if current_user.role_id == 2:
                
                build_data_select = Build.query.all()
                
                department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
                
                build_log_data = Build_Log.query.filter_by(build_id=request.args.get("build")).filter(Build_Log.created_at >= request.args.get("date_start")+" "+request.args.get("time_start")).filter(Build_Log.created_at <= request.args.get("date_end")+" "+request.args.get("time_end"))\
                    .filter_by(department_id=request.args.get("department")).all()

            else:
                
                build_data_select = Build.query.filter_by(id=build_data.id).all()
                
                department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
                
                build_log_data = Build_Log.query.filter_by(build_id=build_data.id).filter(Build_Log.created_at >= request.args.get("date_start")+" "+request.args.get("time_start")).filter(Build_Log.created_at <= request.args.get("date_end")+" "+request.args.get("time_end"))\
                    .filter_by(department_id=request.args.get("department")).all()   
            
            for x in build_log_data:
                for j in build_data_select:
                    if j.id == x.build_id:
                        x.build_name = j.build_name
                for j in department_data:
                    if j.id == x.department_id:
                        x.department_name = j.department_name
                x.created_at = str(x.created_at).split(".")[0]
                x.sum = equation_sum(x.variable_a,x.variable_b,x.variable_c)
                x.error = equation_error(x.variable_a,x.variable_b,x.variable_c)
        
        elif request.args.get("date_start") != None and request.args.get("time_start") != None and request.args.get("date_end") != None and request.args.get("time_end") != None:
            
            if current_user.role_id == 2:
                
                build_data_select = Build.query.all()
                
                department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
                
                build_log_data = Build_Log.query.filter_by(build_id=request.args.get("build")).filter(Build_Log.created_at >= request.args.get("date_start")+" "+request.args.get("time_start")).filter(Build_Log.created_at <= request.args.get("date_end")+" "+request.args.get("time_end")).all()
            
            else:
                
                build_data_select = Build.query.filter_by(id=build_data.id).all()
                
                department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
                
                build_log_data = Build_Log.query.filter_by(build_id=build_data.id).filter(Build_Log.created_at >= request.args.get("date_start")+" "+request.args.get("time_start")).filter(Build_Log.created_at <= request.args.get("date_end")+" "+request.args.get("time_end")).all()    
             
            for x in build_log_data:
                for j in build_data_select:
                    if j.id == x.build_id:
                        x.build_name = j.build_name
                for j in department_data:
                    if j.id == x.department_id:
                        x.department_name = j.department_name
                x.created_at = str(x.created_at).split(".")[0]
                x.sum = equation_sum(x.variable_a,x.variable_b,x.variable_c)
                x.error = equation_error(x.variable_a,x.variable_b,x.variable_c)
        
        else:
            build_log_data = []
            department_data = []
            if current_user.role_id == 2:
                build_data_select = Build.query.all()
            else:
                build_data_select = Build.query.filter_by(id=build_data.id).all()
        
        output = BytesIO()
        workbook = Workbook(output)
        
        sheet = workbook.add_worksheet('sheet_1')    
        
        header = workbook.add_format({
            'bg_color': '#F7F7F7',
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
        })
        text = workbook.add_format({
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
        })

        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            # 'fg_color': 'yellow'
            })

        set_col = 7
        set_row = 2
        
        sheet.merge_range('C2:J5', 'บริษัท ปตท. จำกัด (มหาชน) \r\n 555 ถนนวิภาวดีรังสิต แขวงจตุจักร เขตจตุจักร 10900 \r\n โทรศัพท์ : 0-2537-2000 โทรสาร : 0-2537-3498-9', merge_format)
        
        sheet.write(set_col, 1, ("#"), header)
        sheet.write(set_col, 2, ("Station"), header)
        sheet.write(set_col, 3, ("License Plate"), header)
        sheet.write(set_col, 4, ("Oil Type"), header)
        sheet.write(set_col, 5, ("API"), header)
        sheet.write(set_col, 6, ("API@Ori"), header)
        sheet.write(set_col, 7, ("Temp"), header)
        sheet.write(set_col, 8, ("API@60F"), header)
        sheet.write(set_col, 9, ("Error"), header)
        sheet.write(set_col, 10, ("Date"), header)
        count = 0
         
        for item in build_log_data:
            set_col += 1
            sheet.write(set_col, 1, (count), text)
            try:
                sheet.write(set_col, 2, (item.build_name), text)
                sheet.write(set_col, 3, (item.license_plate), text)
            except:
                sheet.write(set_col, 2, (""), text)
                sheet.write(set_col, 3, (""), text)
            try:
                sheet.write(set_col, 4, (item.department_name), text)
            except:
                sheet.write(set_col, 4, (""), text)

            try:
                sheet.write(set_col, 5, (item.variable_a), text)
                sheet.write(set_col, 6, (item.variable_b), text)
                sheet.write(set_col, 7, (item.variable_c), text)
                sheet.write(set_col, 8, (item.sum), text)
                sheet.write(set_col, 9, (item.error), text)
                sheet.write(set_col, 10, (str(item.created_at).split(".")[0]), text)
            except:
                sheet.write(set_col, 5, (""), text)
                sheet.write(set_col, 6, (""), text)
                sheet.write(set_col, 7, (""), text)
                sheet.write(set_col, 8, (""), text)
                sheet.write(set_col, 9, (""), text)
                sheet.write(set_col, 10, (""), text)

            count+=1
        
        workbook.close()
        output.seek(0)
        
        return send_file(output,
                            attachment_filename='data.xlsx',
                            as_attachment=True,
                            mimetype=EXCELMIME)


@main_bp.route('/uploader-image-profile', methods = [ 'POST'])
def upload_file():
   if request.method == 'POST':
        files = request.files['file']
        if files and allowed_file(files.filename):
            time_name = str(time.time()).split(".")
            filename = secure_filename(files.filename)
            
            filename = "profile_"+(datetime.now().strftime("%d-%m-%Y_%H-%M-%S_"))+"."+filename.split(".")[1]
            
            updir = os.path.join(basedir, 'static/upload/')
            files.save(os.path.join(updir, filename))
            user_data = User.query.filter_by(id=current_user.id).first()
            user_data.image = "upload/"+filename
            
            db.session.add(user_data)
            db.session.commit()
            file_size = os.path.getsize(os.path.join(updir, filename))
            
            return jsonify(name=filename, path="upload/"+filename, size=file_size)

@main_bp.route('/uploader-image-build', methods = [ 'POST'])
def upload_file_build():
   if request.method == 'POST':
        files = request.files['file']
        if files and allowed_file(files.filename):
            time_name = str(time.time()).split(".")
            filename = secure_filename(files.filename)
            filename = "build_"+(datetime.now().strftime("%d-%m-%Y_%H-%M-%S_"))+"."+filename.split(".")[1]
            updir = os.path.join(basedir, 'static/upload/')
            files.save(os.path.join(updir, filename))
            build_data = Build.query.filter_by(user_id=current_user.id).first()
            build_data.build_image = "upload/"+filename
            db.session.add(build_data)
            db.session.commit()
            file_size = os.path.getsize(os.path.join(updir, filename))
            return jsonify(name=filename, path="upload/"+filename, size=file_size)
	
@main_bp.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
   if request.method == 'POST':
        files = request.files['file']
        if files and allowed_file(files.filename):
            time_name = str(time.time()).split(".")
            filename = secure_filename(files.filename)
            filename = (datetime.now().strftime("%d-%m-%Y_%H-%M-%S_"))+"."+filename.split(".")[1]
            updir = os.path.join(basedir, 'static/upload/')
            files.save(os.path.join(updir, filename))
            file_size = os.path.getsize(os.path.join(updir, filename))
            return jsonify(name=filename, path="upload/"+filename, size=file_size)

@main_bp.route('/', methods=['GET'])
@main_bp.route('/add-data', methods=['GET','POST'])
@login_required
def add_data():
    if request.method=="GET":
        build_data = Build.query.filter_by(user_id=current_user.id).first()
        department_data = Department.query.join(Build, Build.id==Department.build_id).add_columns(Build.id, Build.build_name).filter_by(id=build_data.id).all()
        return render_template(
            'add_data.html',
            title='Manage Build',
            template='dashboard-template',
            current_user=current_user,
            build_data=build_data,
            department_data=department_data,
            add_data='active',
            body="You are now logged in!"
        )
    elif request.method=="POST":
        results = []
        build_data = Build.query.filter_by(user_id=current_user.id).first()
        
        table_send_form = request.form.getlist('table_send_form[]')
        license_plate = request.form.getlist('license_plate[]')
        department = request.form.getlist('department[]')
        column_a = request.form.getlist('column_a[]')
        column_b = request.form.getlist('column_b[]')
        column_c = request.form.getlist('column_c[]')
        
        for x in range(0,len(license_plate)):
            build = Build_Log(
                build_id=build_data.id,
                license_plate=license_plate[x],
                department_id=department[x],
                variable_a=column_a[x],
                variable_b=column_b[x],
                variable_c=column_c[x]
            )
            db.session.add(build)
            db.session.commit()
            
            results.append({'table': table_send_form[x], 'sum':equation_sum(float(column_a[x]), float(column_b[x]) , float(column_c[x])), 'error': equation_error(float(column_a[x]), float(column_b[x]) , float(column_c[x]))})
        return json.dumps({ 'status': True,'data':results })
    elif request.method=="PUT":
        pass

@main_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if request.method=="GET":
        user_data = User.query.filter_by(id=current_user.id).first()
        build_data = Build.query.filter_by(user_id=user_data.id).first()
        if request.args.get("date_start") != None and request.args.get("time_start") != None and request.args.get("date_end") != None and request.args.get("time_end") != None and request.args.get("department") != None and request.args.get("department") != "0":
            print(request.args.get("department"))
            if current_user.role_id == 2:
                build_data_select = Build.query.all()
                department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
                build_log_data = Build_Log.query.filter_by(build_id=request.args.get("build")).filter(Build_Log.created_at >= request.args.get("date_start")+" "+request.args.get("time_start")).filter(Build_Log.created_at <= request.args.get("date_end")+" "+request.args.get("time_end"))\
                    .filter_by(department_id=request.args.get("department")).all()
            else:
                build_data_select = Build.query.filter_by(id=build_data.id).all()
                department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
                build_log_data = Build_Log.query.filter_by(build_id=build_data.id).filter(Build_Log.created_at >= request.args.get("date_start")+" "+request.args.get("time_start")).filter(Build_Log.created_at <= request.args.get("date_end")+" "+request.args.get("time_end"))\
                    .filter_by(department_id=request.args.get("department")).all()    
            for x in build_log_data:
                for j in build_data_select:
                    if j.id == x.build_id:
                        x.build_name = j.build_name
                for j in department_data:
                    if j.id == x.department_id:
                        x.department_name = j.department_name
                x.created_at = str(x.created_at).split(".")[0]
                x.sum = equation_sum(x.variable_a,x.variable_b,x.variable_c)
                x.error = equation_error(x.variable_a,x.variable_b,x.variable_c)
        elif request.args.get("date_start") != None and request.args.get("time_start") != None and request.args.get("date_end") != None and request.args.get("time_end") != None:
            if current_user.role_id == 2:
                build_data_select = Build.query.all()
                department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
                build_log_data = Build_Log.query.filter_by(build_id=request.args.get("build")).filter(Build_Log.created_at >= request.args.get("date_start")+" "+request.args.get("time_start")).filter(Build_Log.created_at <= request.args.get("date_end")+" "+request.args.get("time_end")).all()
            else:
                build_data_select = Build.query.filter_by(id=build_data.id).all()
                department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
                build_log_data = Build_Log.query.filter_by(build_id=build_data.id).filter(Build_Log.created_at >= request.args.get("date_start")+" "+request.args.get("time_start")).filter(Build_Log.created_at <= request.args.get("date_end")+" "+request.args.get("time_end")).all()    
            for x in build_log_data:
                for j in build_data_select:
                    if j.id == x.build_id:
                        x.build_name = j.build_name
                for j in department_data:
                    if j.id == x.department_id:
                        x.department_name = j.department_name
                x.created_at = str(x.created_at).split(".")[0]
                x.sum = equation_sum(x.variable_a,x.variable_b,x.variable_c)
                x.error = equation_error(x.variable_a,x.variable_b,x.variable_c)
        else:
            build_log_data = []
            department_data = []
            if current_user.role_id == 2:
                build_data_select = Build.query.all()
            else:
                build_data_select = Build.query.filter_by(id=build_data.id).all()
                
        return render_template(
            'dashboard.html',
            title='Dashborad',
            template='dashboard-template',
            current_user=current_user,
            build_data=build_data_select,
            build_log_data=build_log_data,
            body="You are now logged in!"
        )

@main_bp.route('/get-department', methods=['GET'])
@login_required
def get_search():
    if request.method=="GET":
        data = []
        department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
        for x in department_data:
            data.append({"id":x.id,"department_name":x.department_name})
        return jsonify(status=True,data=data)

@main_bp.route('/search', methods=['GET'])
@login_required
def search():
    if request.method=="GET":
        user_data = User.query.filter_by(id=current_user.id).first()
        build_data = Build.query.filter_by(user_id=user_data.id).first()
        if request.args.get("date_start") != None and request.args.get("time_start") != None and request.args.get("date_end") != None and request.args.get("time_end") != None and request.args.get("department") != None and request.args.get("department") != "0":
            print(request.args.get("department"))
            if current_user.role_id == 2:
                build_data_select = Build.query.all()
                department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
                build_log_data = Build_Log.query.filter_by(build_id=request.args.get("build")).filter(Build_Log.created_at >= request.args.get("date_start")+" "+request.args.get("time_start")).filter(Build_Log.created_at <= request.args.get("date_end")+" "+request.args.get("time_end"))\
                    .filter_by(department_id=request.args.get("department")).all()
            else:
                build_data_select = Build.query.filter_by(id=build_data.id).all()
                department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
                build_log_data = Build_Log.query.filter_by(build_id=build_data.id).filter(Build_Log.created_at >= request.args.get("date_start")+" "+request.args.get("time_start")).filter(Build_Log.created_at <= request.args.get("date_end")+" "+request.args.get("time_end"))\
                    .filter_by(department_id=request.args.get("department")).all()    
            for x in build_log_data:
                for j in build_data_select:
                    if j.id == x.build_id:
                        x.build_name = j.build_name
                for j in department_data:
                    if j.id == x.department_id:
                        x.department_name = j.department_name
                x.created_at = str(x.created_at).split(".")[0]
                x.sum = equation_sum(x.variable_a,x.variable_b,x.variable_c)
                x.error = equation_error(x.variable_a,x.variable_b,x.variable_c)
        elif request.args.get("date_start") != None and request.args.get("time_start") != None and request.args.get("date_end") != None and request.args.get("time_end") != None:
            if current_user.role_id == 2:
                build_data_select = Build.query.all()
                department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
                build_log_data = Build_Log.query.filter_by(build_id=request.args.get("build")).filter(Build_Log.created_at >= request.args.get("date_start")+" "+request.args.get("time_start")).filter(Build_Log.created_at <= request.args.get("date_end")+" "+request.args.get("time_end")).all()
            else:
                build_data_select = Build.query.filter_by(id=build_data.id).all()
                department_data = Department.query.filter_by(build_id=request.args.get("build")).all()
                build_log_data = Build_Log.query.filter_by(build_id=build_data.id).filter(Build_Log.created_at >= request.args.get("date_start")+" "+request.args.get("time_start")).filter(Build_Log.created_at <= request.args.get("date_end")+" "+request.args.get("time_end")).all()    
            for x in build_log_data:
                for j in build_data_select:
                    if j.id == x.build_id:
                        x.build_name = j.build_name
                for j in department_data:
                    if j.id == x.department_id:
                        x.department_name = j.department_name
                x.created_at = str(x.created_at).split(".")[0]
                x.sum = equation_sum(x.variable_a,x.variable_b,x.variable_c)
                x.error = equation_error(x.variable_a,x.variable_b,x.variable_c)
        else:
            build_log_data = []
            department_data = []
            if current_user.role_id == 2:
                build_data_select = Build.query.all()
            else:
                build_data_select = Build.query.filter_by(id=build_data.id).all()
        return render_template(
            'search.html',
            title='Search',
            template='dashboard-template',
            current_user=current_user,
            build_data=build_data_select,
            build_log_data=build_log_data,
            body="You are now logged in!"
        )

@main_bp.route('/manage-user', methods=['GET','POST','PUT','DELETE'])
@login_required
def manage_user():
    if request.method=="GET":
        if request.args.get("user_id") != None:
            user_data = User.query.filter_by(id=request.args.get("user_id")).first()
            build_data = Build.query.filter_by(user_id=user_data.id).first()
            return jsonify(email=user_data.email,image=user_data.image,build_name=build_data.build_name,build_image=build_data.build_image)
        else:
            user_data = Build.query.join(User, User.id==Build.user_id).add_columns(User.id, User.role_id, User.username , User.email, User.created_at).all()
            
            return render_template(
                'manage_user.html',
                title='Manage User',
                template='dashboard-template',
                current_user=current_user,
                user_data=user_data,
                manage_user='active',
                body="You are now logged in!"
            )
    elif request.method=="POST":
        user = User(
                username=request.form['username'],
                image=request.form['image'],
                email=request.form['email'],
                role_id=1,
                status=1
            )
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        find_user = User.query.filter_by(username=request.form['username']).first()
        build = Build(
                user_id=find_user.id,
                build_name=request.form['build'],
                build_image=request.form['image_build']
            )
        db.session.add(build)
        db.session.commit()
        return json.dumps({ 'status': True })
    elif request.method=="PUT":
        user_data = User.query.filter_by(id=request.form["user_id"]).first()
        build_data = Build.query.filter_by(user_id=user_data.id).first()
        user_data.email = request.form["email"]
        build_data.build_name = request.form["build"]
        try:
            user_data.image = request.form["image"]
        except :
            pass
        try:
            build_data.image_build = request.form["image_build"]
        except :
            pass
        db.session.add(user_data)
        db.session.add(build_data)
        db.session.commit()
        return jsonify(status=True)
    elif request.method=="DELETE":
        if request.form["user_id"]:
            user_data = User.query.filter_by(id=request.form["user_id"]).first()
            build_data = Build.query.filter_by(user_id=user_data.id).first()
            build_log_data = Build_Log.query.filter_by(build_id=build_data.id).all()
            for x in build_log_data:
                db.session.delete(x)
            db.session.delete(user_data)
            db.session.delete(build_data)
            db.session.commit()
            return jsonify(status=True)
        else:
            return jsonify(status=False)
        

@main_bp.route('/manage-build', methods=['GET','PUT','DELETE'])
@login_required
def manage_build():
    if request.method=="GET":
        build_data = Build.query.filter_by(user_id=current_user.id).first()
        return render_template(
            'manage_build.html',
            title='Manage Build',
            template='dashboard-template',
            current_user=current_user,
            build_data=build_data,
            manage_build='active',
            body="You are now logged in!"
        )
    elif request.method=="PUT":
        user_data = User.query.filter_by(id=current_user.id).first()
        build_data = Build.query.filter_by(user_id=user_data.id).first()
        build_data.build_name = request.form["build_name"]
        db.session.add(build_data)
        db.session.commit()
        return json.dumps({ 'status': True })
    else:
        return json.dumps({ 'status': False })

@main_bp.route('/manage-department', methods=['GET','POST','PUT','DELETE'])
@login_required
def manage_department():
    if request.method=="GET":
        if request.args.get("department_id") != None:
            department_data = Department.query.filter_by(id=request.args.get("department_id")).join(Build, Build.id==Department.build_id).add_columns(Build.id, Build.build_name).first()
            return jsonify(department_id=department_data[0].id,deparment_name=department_data[0].department_name,build_name=department_data.build_name,deparment_created=department_data[0].created_at)
        else:
            build_data = Build.query.filter_by(user_id=current_user.id).first()
            department_data = Department.query.filter_by(build_id=build_data.id).join(Build, Build.id==Department.build_id).add_columns(Build.id, Build.build_name).all()
            return render_template(
                'manage_department.html',
                title='Manage Department',
                template='dashboard-template',
                current_user=current_user,
                department_data=department_data,
                manage_department='active',
                body="You are now logged in!"
            )
    elif request.method=="POST":
        user_data = User.query.filter_by(id=current_user.id).first()
        build_data = Build.query.filter_by(user_id=user_data.id).first()
        department = Department(
                department_name=request.form['departmaent'],
                build_id=build_data.id
            )
        db.session.add(department)
        db.session.commit()
        return json.dumps({ 'status': True })
    elif request.method=="PUT":
        if request.form["department_id"]:
            department_data = Department.query.filter_by(id=request.form["department_id"]).first()
            department_data.department_name = request.form["department_name"]
            db.session.add(department_data)
            db.session.commit()
            return jsonify(status=True)
        else:
            return jsonify(status=False)
    elif request.method=="DELETE":
        if request.form["department_id"]:
            department_data = Department.query.filter_by(id=request.form["department_id"]).first()
            build_log_data = Build_Log.query.filter_by(department_id=department_data.id).all()
            for x in build_log_data:
                db.session.delete(x)
            db.session.delete(department_data)
            db.session.commit()
            return jsonify(status=True)
        else:
            return jsonify(status=False)
    
@main_bp.route('/profile', methods=['GET','PUT'])
@login_required
def profile():
    if request.method=="GET":
        return render_template(
            'profile.html',
            title='Manage User',
            template='dashboard-template',
            current_user=current_user,
            body="You are now logged in!"
        )
    elif request.method=="PUT":
        user_data = User.query.filter_by(id=current_user.id).first()
        user_data.email = request.form["email"]
        db.session.add(user_data)
        db.session.commit()
        return json.dumps({ 'status': True })
    else:
        return json.dumps({ 'status': False })

@main_bp.route('/update-password', methods=['GET','PUT'])
@login_required
def update_password():
    if request.method=="GET":
        return render_template(
            'update_password.html',
            title='Manage Build',
            template='dashboard-template',
            current_user=current_user,
            body="You are now logged in!"
        )
    if request.method=="PUT":
        user_data = User.query.filter_by(id=current_user.id).first()
        if user_data.check_password(password=request.form["current_passowrd"]) == True:
            user_data.set_password(request.form["new_password"])
            db.session.add(user_data)
            db.session.commit()
            return json.dumps({ 'status': True,"msg":"เปลี่ยนรหัสผ่านสำเร็จ" })
        else:
            return json.dumps({ 'status': False,"msg":"เปลี่ยนรหัสผ่านไม่สำเร็จ" })

@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
