from flask import Blueprint, render_template,url_for,redirect
from flask_login import login_user,logout_user,login_required,current_user
from models import User,Venue,Show
views = Blueprint('views',__name__)

@views.route('/')
def home():
    return(render_template("home.html"))

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/summary')
def summary():
    return render_template("summary.html")

@views.route('/admin')
def adlogin():
    return render_template("adminlogin.html")

@views.route('/user/dashboard')
def usrhome():
    return render_template("userhome.html")

@views.route('/admin/dashboard')
def adhome():
    if(current_user.is_authenticated):
        id=current_user.get_id()
        ven=Venue.query.filter_by(admin_id=id).all()
        if ven:
            show=Show.query.filter_by().all()
            return render_template("adminhome.html",venue=ven,show=show)
        return render_template("adminhome.html",venue=ven)
    return redirect(url_for('auth.adlogin'))
