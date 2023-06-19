from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.email_model import Email

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/validate_email', methods=['POST'])
def validation():
    if not Email.is_valid(request.form):  #if input does not pass validation, return to index page
        return redirect('/')                #if we get a false return, we have errors
    Email.save(request.form)                    #bc input passes validation, save the data and redirect to success page
    return redirect('/success')

@app.route('/success')
def success():
    email = Email.get_all()
    return render_template('success.html', email=email)

@app.route('/delete/<int:email_id>')
def delete(email_id):
    data = {
        "id": email_id
    }
    Email.delete(data)
    return redirect('/success')