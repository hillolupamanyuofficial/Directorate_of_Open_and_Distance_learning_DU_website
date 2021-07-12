from flask import (Flask,jsonify,Blueprint,request,
flash,render_template,redirect,url_for,send_file)
from api.daos.notification_daos import Datadaos
from werkzeug.utils import secure_filename
from api import config
import os
import uuid
import datetime

def create_blueprint(cluster):
    data = Blueprint("data",__name__)
    daos = Datadaos(cluster)

    @data.route("/",methods=['GET'])
    def index():
        general = daos.get_notifications_by_category('general')
        exam = daos.get_notifications_by_category('exam')
        admission = daos.get_notifications_by_category('admission')

        return render_template('index.html',general=general,exam=exam,adm=admission)

    @data.route("/<pdf>",methods=['GET'])
    def get_pdf(pdf):
        file = os.path.join(os.environ.get("UPLOAD_BASE_DIR"),pdf)
        if os.path.isfile(file):
            return send_file(file)
        return redirect(url_for('data.file_access_error'))

    @data.route("/error",methods=['GET'])
    def file_access_error():
        return "<h2>File Not Found</h2>"

    @data.route("/upload",methods=['POST'])
    def add_files():
        if request.method == 'POST':
            title = request.form.get('title')
            pdf = request.files['pdf']
            category = request.form.get('category')

            separator = "_"
            temp_array = str(pdf.filename).split(" ")
            pdf.filename = separator.join(temp_array)

            filename = secure_filename(pdf.filename)
            # UPLOAD DESTINATION
            upload_filename = filename
            filename = os.path.join(os.environ.get("UPLOAD_BASE_DIR"),filename)
            pdf.save(filename)

            data = {
                "title" : title,
                "doc_link" : upload_filename,
            }
            response = daos.post_new_notification(data,category)
            if response:
                flash('Notification added successfully','success')
                return redirect(url_for('admin.notification_page'))
            flash('Notification cannot be added','error')
            return redirect(url_for('admin.notification_page'))

    @data.route("/d/<title>",methods=['GET'])
    def delete_ntf(title):
        try:
            response = daos.get_notifications_by_title(title)
            if response:
                filename = os.path.join(os.environ.get("UPLOAD_BASE_DIR"),response)
                os.remove(filename)

        except Exception as e:
            with open('error.log','a') as fptr:
                fptr.write(f"Error: {e}\n")

        finally:
            # Delete Database Data for the corresponding entry    
            response = daos.delete_notification(title)
            if response:
                flash('Notification deleted successfully','success')
                return redirect(url_for('admin.notification_page'))
            flash('Notification cannot be deleted','error')
            return redirect(url_for('admin.notification_page'))

    @data.route("/about",methods=['GET'])
    def about():
        return render_template('AboutUs.html')

    @data.route("/contact",methods=['GET'])
    def contact():
        return render_template('ContactUs.html')

    @data.route("/adm",methods=['GET'])
    def adm():
        return render_template('administration.html')

    @data.route("/programmes",methods=['GET'])
    def programmes():
        return render_template('programmes.html')

    @data.route("/recognition",methods=['GET'])
    def recognition():
        return render_template('recognition.html')

    @data.route("/syllabus",methods=['GET'])
    def syllabus():
        return render_template('syllabus.html')
    
    @data.route("/eslm",methods=['GET'])
    def eslm():
        return render_template('eslm.html')
    
    @data.route("/assignment",methods=['GET'])
    def assignment():
        return render_template('assignment.html')

    return data