from flask import Blueprint, render_template, request,flash, redirect,url_for
from models import User,Venue,Show,Tag,Booking
from __init__ import db
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,logout_user,login_required,current_user
from datetime import date as date1
from datetime import datetime
auth = Blueprint('auth',__name__)

@auth.route('/userlogin', methods=['GET', 'POST'])
def ulogin():
    if (request.method=='POST'):
        em=request.form['email']
        pw=request.form['password1']
        u = User.query.filter_by(email=em).first()
        if u and check_password_hash(u.password,pw):
            flash("Logged in successfully",category="success")
            login_user(u,remember=True)
            return redirect(url_for('views.usrhome'))
        else:
            flash("invalid Email and password",category="error")
    return render_template('userlogin.html') 


@auth.route('/admin' , methods=['GET', 'POST'])
def adlogin():
    if (request.method=='POST'):
        name=request.form['name']
        pw=request.form['password1']
        admin = User.query.filter_by(name=name).first()
        if admin and check_password_hash(admin.password,pw):
            if(admin.isadmin):
                login_user(admin,remember=True)
                flash("Logged in successfully",category="success")
                return redirect(url_for('views.adhome'))
            else:
                flash("This page is for admin please login through user portal",category="error")
        else:
            flash("invalid username and password",category="error")
    return render_template('adminlogin.html') 

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/usersignup', methods=['GET', 'POST'])
def usersignup():
    if request.method == 'POST':
        em=request.form['email']
        pw=request.form['password']
        pw1=request.form['confirm_password']
        user=request.form['username']
        a=User.query.filter_by(email=em).first()
        if a:
            flash("email already exist",category="error")
        else:
            if len(em) < 4:
                flash('Email too short', category='error')
            elif len(pw) < 7:
                flash('Password too short', category='error')
            elif len(user) < 2:
                flash('Username too short', category='error')
            elif pw != pw1:
                flash('Passwords don\'t match', category='error')
            else:
                new_usr=User(email=em,password=generate_password_hash(pw,method='sha256'),name=user)
                db.session.add(new_usr)
                db.session.commit()
                flash('Account created!', category='success')
    
    return render_template('usersignup.html') 

@auth.route('/adminsignup',methods=['GET', 'POST'])
def adminsignup():
    if request.method == 'POST':
        em=request.form['email']
        pw=request.form['password']
        pw1=request.form['confirm_password']
        user=request.form['username']
        a=User.query.filter_by(email=em).first()
        if a:
            flash("email already exist",category="error")
        else:
            if len(em) < 4:
                flash('Email too short', category='error')
            elif len(pw) < 7:
                flash('Password too short', category='error')
            elif len(user) < 2:
                flash('Username too short', category='error')
            elif pw != pw1:
                flash('Passwords don\'t match', category='error')
            else:
                new_ad=User(email=em,password=generate_password_hash(pw,method='sha256'),name=user,isadmin=True)
                db.session.add(new_ad)
                db.session.commit()
                flash('Account created!', category='success')
    return render_template('adminsignup.html')


@auth.route('/addven',methods=['GET', 'POST'])
@login_required
def addven():
    if request.method == 'POST':
        n=request.form['name']
        add=request.form['addr']
        city=request.form['city']
        a=Venue.query.filter_by(name=n).first()
        if a:
            flash("Venue already exist",category="error")
        else:
            if len(n) < 4 or add=="" or city=="":
                flash('Invalid details provided', category='error')
            else:
                id=current_user.get_id()
                new_ven=Venue(admin_id=id,name=n,address=add,city=city)
                db.session.add(new_ven)
                db.session.commit()
                flash('Venue created!', category='success')
                ven=Venue.query.filter_by(admin_id=id).all()
                sh=Show.query.filter_by().all()
                return render_template('adminhome.html',venue=ven,show=sh)
    return render_template('addvenue.html')

@auth.route('/delete_venue/<int:venue_id>', methods=['GET', 'POST'])
@login_required
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)
    show=Show.query.filter_by(venue_id=venue.id).all()
    for s in show:
        tg=Tag.query.filter_by(show_id=s.id).all()
        for t in tg:
            db.session.delete(t)
        bg=Booking.query.filter_by(show_id=s.id).all()
        for b in bg:
            db.session.delete(b)
        db.session.delete(s)
    db.session.delete(venue)
    db.session.commit()
    flash('Venue deleted successfully', 'success')
    return redirect(url_for('views.adhome'))
        
@auth.route('/addshow/<int:venue_id>', methods=['GET', 'POST'])
@login_required
def addshow(venue_id):
    venue = Venue.query.get(venue_id)
    if request.method == 'POST':
        n = request.form['name']
        date = request.form['date']
        time = request.form['time']
        desc = request.form['description']
        tag=desc.split(",")
        rat=request.form['rating']
        price = request.form['price']
        cap=request.form['numb']
        if date =="":
            date =date1.today()
        if rat=="" or time =="" or price=="" or cap=="":
             flash('Invalid details provided', category='error')
             return render_template('addshow.html', venue=venue)
        new_show = Show(name=n, date=date, time=time, desc=desc, price=price, venue_id=venue_id,capacity=cap,rating=rat)
        db.session.add(new_show)
        show=Show.query.filter_by(desc=desc).all()
        for s in show:
            for t in tag:
                sh=Tag.query.filter_by(show_id=s.id,tag=t).first()
                if(sh==None):
                    new_tag=Tag(show_id=s.id,tag=t)
                    db.session.add(new_tag)
                continue
        db.session.commit()
        flash('Show added successfully', 'success')
        return redirect(url_for('views.adhome'))
    return render_template('addshow.html', venue=venue)  

@auth.route('/updateven/<int:venue_id>', methods=['GET', 'POST'])
@login_required
def updatevenue(venue_id):
    if request.method == 'POST':
            venue = Venue.query.get(venue_id)
            n = request.form['name']
            ad=request.form['addr']
            venue.name = n
            venue.city=ad
            db.session.commit()
            flash('Venue updated successfully!', 'success')
            return redirect(url_for('views.adhome'))
    return render_template('update_ven.html')


@auth.route('/updateshow/<int:show_id>', methods=['GET', 'POST'])
@login_required
def update_show(show_id):
    sh = Show.query.get(show_id)
    if request.method == 'POST':
            tg=Tag.query.filter_by(show_id=show_id).all()
            for t in tg:
                db.session.delete(t)
            bg=Booking.query.filter_by(show_id=show_id).all()
            for b in bg:
                db.session.delete(b)
            n = request.form['name']
            price = request.form['price']
            cap=request.form['numb']
            sh.name = n
            sh.price=price
            sh.capacity=cap
            db.session.commit()
            flash('Venue updated successfully!', 'success')
            return redirect(url_for('views.adhome'))
    return render_template('update_show.html',show=sh)

@auth.route('/delete_show/<int:show_id>', methods=['GET', 'POST'])
@login_required
def delete_show(show_id):
    sh = Show.query.get(show_id)
    tg=Tag.query.filter_by(show_id=show_id).all()
    for t in tg:
        db.session.delete(t)
    bg=Booking.query.filter_by(show_id=show_id).all()
    for b in bg:
        db.session.delete(b)
    db.session.delete(sh)
    db.session.commit()
    flash('Show deleted successfully', 'success')
    return redirect(url_for('views.adhome'))

@auth.route('/user/dashboard',methods=['GET','POST'])
def userhome():
    if request.method=='POST':
        cit=request.form['city']
        d=request.form['date']
        t=request.form['Tags']
        mn=request.form['movie']
        if cit=="" :
            if mn=="":
                flash('City must be entered','error')
            else:
                f=Venue.query.filter_by(name=mn).all()
                if f==[]:
                    flash("Venue not found enter a city to search for movies",'error')
                else:
                    return render_template('userhome.html',venue=f)
        else:
            if d=="":
                d=date1.today()
            sh=Show.query.filter_by(date=d).all()
            v=[]
            id1=0
            l=[]
            for s in sh:
                
                d = datetime.strptime(s.date, "%Y-%m-%d")
                d1=datetime.strptime(str(date1.today()), "%Y-%m-%d")
                print(d,d1)
                l.append(datetime.strptime(s.time,'%H:%M').time()>datetime.now().time() or d1<d)
                if(id1 !=s.venue_id):
                    f=Venue.query.filter_by(id=s.venue_id,city=cit).first()
                    if f == None:
                        continue
                    if f not in v:
                        v.append(f)
                    id1=s.venue_id
            
            if( mn==""):
                if(t==""):
                    return render_template('userhome.html',venue=v,show=sh,valid=l)
                else:
                    t1=Tag.query.filter_by(tag=t).all()
                    if t1==[]:
                        flash("Not a valid tag","error")
                        return render_template("userhome.html")
                    return render_template('userhome.html',venue=v,show=sh,tags=t1,valid=l)
            else:
                sha=Show.query.filter_by(date=d,name=mn).all()
                
                v1=[]
                id=0
                for s in sha:
                    if(id !=s.venue_id):
                        f=Venue.query.filter_by(id=s.venue_id,city=cit).first()
                        if f ==None:
                            continue
                        v1.append(f)
                        id1=s.venue_id
                if(t==""):
                    return render_template('userhome.html',venue=v1,show=sha,valid=l)
                else:
                    t1=Tag.query.filter_by(tag=t).all()
                    if t1==[]:
                        flash("Not a valid tag","error")
                        return render_template("userhome.html")
                    
                    return render_template('userhome.html',venue=v1,show=sha,tags=t1,valid=l)


    return render_template('userhome.html')
@auth.route('/booking/<int:show_id>', methods=['GET', 'POST'])
def book(show_id):
    total = None
    house=0
    if request.method == 'POST':
        num = request.form['number']
        sh=Show.query.filter_by(id=show_id).first()
        p=sh.capacity
        if(num == ''):
            flash("Enter an whole number","error")
            return render_template("booking.html",show_id=show_id)
        sh.capacity-=int(num)
        price = sh.price
        total = int(price)*int(num)
        house=0
        if int(num)<=0:
            flash("Enter an whole number","error")
            return render_template("booking.html",show_id=show_id)
        if(int(num)>p):
            house=1
        if 'confirm' in request.form:
            house=0
            if(int(num)>p):
                house=1
            else:
                if int(num)>0:
                    book=Booking(user_id=current_user.id,show_id=show_id,tick=num)
                    db.session.add(book)
                    db.session.commit()          
                    return render_template('booking_confirmation.html', show_id=show_id, num=num, total=total,usr=current_user.id)
                else:
                    flash("Enter number of tickets to book!","error")
    return render_template('booking.html', show_id=show_id,total=total,house=house)

@auth.route("/usrbook",methods=["POST","GET"])
@login_required
def usrbook():
    b=Booking.query.filter_by(user_id=current_user.id).all()
    s=Show.query.filter_by().all()
    return render_template("usr_booking.html",book=b,show=s)


@auth.route("/venue/<string:venue_id>",methods=["POST","GET"])

def vdetail(venue_id):
    v=Venue.query.filter_by(id=venue_id).first()
    s=Show.query.filter_by(venue_id=venue_id).all()
    return render_template("venue.html",venue=v,show=s)