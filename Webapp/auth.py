from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Category, Product, Userbook, Confirmbooking
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import text
auth = Blueprint('auth', __name__)

#User Login
@auth.route('/', methods=['GET', 'POST'])
def Login():
    # data = request.form
    # print(data)
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                flash("Logged In", category='success')
                login_user(user, remember=True)
                if user.admin=='True':
                    return redirect(url_for('auth.adminmain'))
                else:
                    return redirect(url_for('auth.usermain'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("User don\'t exist", category='error')

    return render_template("login.html", user=current_user)

#Admin Login
@auth.route('/admin', methods=['GET', 'POST'])
def admin():
    # data = request.form
    # print(data)
    if request.method == "POST":
        email = request.form.get('ademail')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                if user.admin == "True":
                    flash("Logged In", category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('auth.adminmain'))
                else:
                    flash("NOT A ADMIN", category='error')
                    return render_template("admin.html", user=current_user)
            else:
                flash("Incorrect password", category='error')
        else:
            flash("User don\'t exist", category='error')

    return render_template("admin.html", user=current_user)


#logout 

@auth.route('/logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('auth.Login'))


#user signup

@auth.route('/signup', methods=['get', 'post'])
def Signup():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", category='error')
        elif len(email) < 4:
            flash("Email length error", category='error')
        elif len(password) < 5:
            flash("Password is too short", category='error')
        else:
            new_user = User(email=email, name=name,
                            password=password, admin="False")
            db.session.add(new_user)
            db.session.commit()
            flash("Account successfully created", category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('auth.usermain'))

    return render_template("signup.html", user=current_user)

#Admin homepage
@auth.route('/main', methods=['get', 'post'])
@login_required
def adminmain():
    
    if request.method == "GET":

        cat = Category.query.all()
        var = 'true'
        pro = Product.query.all()
        
    return render_template("adminend.html", cat=cat, pro=pro, var=var, user=current_user)


#Create Category

@auth.route('/createcategory', methods=["get", "post"])
@login_required
def create():
    # var = "false"
    # if request.method == "POST":
    #     name = request.form.get('vname')
    #     if name!='':
            
    #         new_category = Category(name=name)
    #         db.session.add(new_category)
    #         db.session.commit()
    #         flash("Category added", category='success')
            
    #         return redirect(url_for('auth.adminmain'))
    #     else:
    #         flash("Invalid Format", category='error')
    return render_template("createCategory.html", user=current_user)


# Edit Category

@auth.route('/editcategory/<int:ev>', methods=["get", "post"])
@login_required
def editcategory(ev):
    edit_mode=ev
    # # print(type(dv),dv)
    # if request.method == "POST":
    #     # print(type(dv),dv)
    #     editt = Category.query.filter_by(id=str(ev)).first()

    #     name = request.form.get('vname')
    #     if name!='':
    #         editt.name = name
        
    #         db.session.commit()
    #         return redirect(url_for('auth.adminmain'))
    #     else:
    #         flash('Invaid Format', category="error")
    return render_template("createCategory.html",edit_mode=edit_mode, user=current_user)


# delete Category

@auth.route('/deletecategory/<int:dv>', methods=["get", "post"])
@login_required
def deletecat(dv):
    
    dell = Category.query.filter_by(id=str(dv)).first()
    desh = Product.query.filter_by(category_id=str(dv)).all()
    
    for items in desh:
        db.session.delete(items)
    
    db.session.delete(dell)
    db.session.commit()

    return redirect(url_for('auth.adminmain'))
   

#Create Product

@auth.route('/createproduct/<pk>', methods=["get", "post"])
@login_required
def product(pk):
    var = "false"
    edit_mode=pk
    # if request.method == "POST":
    #     name = request.form.get('sname')
    #     expiry = request.form.get('expiry')
    #     quantity = request.form.get('quantity')
    #     price = request.form.get('price')
        
    #     if name!='' and quantity!='' or price!='' :
    #         new_product = Product(name=name, expirydate=expiry,
    #                         quantity=quantity, price=price, category_id=int(pk))
    #         db.session.add(new_product)
    #         db.session.commit()
    #         flash("Product added", category='success')
    #         return redirect(url_for('auth.adminmain'))
    #     else:
    #          flash("Invalid Input", category='error')
#     return render_template("createVenue.html", user= current_user)
    return render_template("createproduct.html",edit_mode=edit_mode, user=current_user)


# Edit Product

@auth.route('/editproduct/<int:es>', methods=["get", "post"])
@login_required
def editproduct(es):
    edit_mode=es
    # if request.method == "POST":

    #     editt = Product.query.filter_by(id=str(es)).first()

    #     name = request.form.get('sname')
    #     expiry = request.form.get('expiry')
    #     quantity = request.form.get('quantity')
    #     price = request.form.get('price')

    #     editt.name = name
    #     editt.expirydate = expiry
    #     editt.quantity = quantity
    #     editt.price = price

    #     db.session.commit()
    #     return redirect(url_for('auth.adminmain'))

    return render_template("editproduct.html", edit_mode=edit_mode,user=current_user)


#delete Product

@auth.route('/deleteproduct/<int:ds>', methods=["get", "post"])
@login_required
def deleteproduct(ds):

    # if request.method=="POST":

    dell = Product.query.filter_by(id=str(ds)).first()
    print(dell)
    db.session.delete(dell)
    db.session.commit()

    return redirect(url_for('auth.adminmain'))


# user main page

@auth.route('/usermain', methods=['get', 'post'])
@login_required
def usermain():

    # if request.method=="GET":

    cat = Category.query.all()
    var = 'true'
    pro = Product.query.all()

    return render_template("userend.html", cat=cat, pro=pro, var=var, user=current_user)



# booking tickets


@auth.route('/bookticket/<sid>/<vid>', methods=['get', 'post'])
@login_required
def booking(sid, vid):

    bookpro = Product.query.filter_by(id=sid).first()
    bookcat = Category.query.filter_by(id=vid).first()
    
    if request.method == "POST":
        try:
            cap = int(bookpro.quantity)
            a = int(request.form.get('ticketsno'))
            price = int(bookpro.price)
            if cap == 0:
                flash("Housefull", category='error')
            elif a <= cap:
                
                flash('Added to Cart', category='success')
            
                total = a*price
                
                Productadded = Userbook(sname=bookpro.name, vname=bookcat.name,
                                    notickets=a, total=total, email=current_user.email,product_id=sid)
            
                db.session.add(Productadded)
                db.session.commit()
                return redirect(url_for('auth.usermain'))
            else:
                flash("Quantity exceeds available stock", category='error')
        except Exception as e:
            flash("Invalid Input", category='error')
    return render_template("book.html", bookpro=bookpro, bookcat=bookcat, user=current_user)


# user cart
@auth.route('/cart', methods=['get', 'post'])
@login_required
def cart():

    counter = 0
    a=0

    bookings = Userbook.query.filter_by(email=current_user.email).all()
    
    cbook = Confirmbooking.query.filter_by(email=current_user.email).all()
    for i in bookings:
        
        counter = counter+i.total
        a=a+i.total

    if request.method == 'POST':
       
        for i in bookings:
        
            bookpro=Product.query.filter_by(id=i.product_id).first()
            ordervalue=i.notickets
            bookpro.quantity=bookpro.quantity-ordervalue
           
        print(cbook)
        for j in cbook:

            j.overalltotal = j.overalltotal+counter
            a = j.overalltotal
            
        for i in bookings:
          
            confirm = Confirmbooking(
                pname=i.sname, cname=i.vname, quantity=i.notickets, total=i.total, overalltotal=a, email=i.email)
            db.session.add(confirm)
           

        Userbook.query.delete()
        db.session.commit()

        flash("Product Purchased", category='success')
        return redirect(url_for('auth.usermain'))
    return render_template("cart.html", bookings=bookings, counter=counter, user=current_user)



# user bookings

@auth.route('/bookings', methods=['get', 'post'])
@login_required
def userbookings():
    a = ''
    bookings = Confirmbooking.query.filter_by(email=current_user.email).all()
    for i in bookings:
        a = i.overalltotal
        break

    return render_template("userbookings.html", bookings=bookings, overall=a, user=current_user)



# searching...

@auth.route('/search', methods=['get', 'post'])
@login_required
def searching():
    s = []
    v = []
    p,ed = [],[]
    pro = Product.query.all()
    cat = Category.query.all()
    print(cat)
    for i in pro:
        s.append(i.name.lower())
        p.append(str(i.price))
        ed.append((i.expirydate))
    
    for j in cat:
        v.append(j.name.lower())
       
    if request.method == 'POST':
       
        query = request.form.get('querys')
        if query!='':
       
            if query.lower() in v:
            
                cat = Category.query.filter(text("LOWER(name) = LOWER(:query)")).params(query=query).first()
                return render_template("searchpage.html", query=query, cat=cat, pro=pro, user=current_user)

            elif query.lower() in s:
            
                sh = Product.query.filter(text("LOWER(name) = LOWER(:query)")).params(query=query).first()
                cat = Category.query.filter_by(id=sh.category_id).first()
                return render_template("searchpage.html", query=query, cat=cat, pro=pro, user=current_user)

            elif query in p:
            
                sh = Product.query.filter_by(price=int(query)).first()
                cat = Category.query.filter_by(id=sh.category_id).first()
                return render_template("searchpage.html", query=query, cat=cat, pro=pro, user=current_user)

            elif query in ed:
            
                sh = Product.query.filter_by(expirydate=str(query)).first()
                cat = Category.query.filter_by(id=sh.category_id).first()
                return render_template("searchpage.html", query=query, cat=cat, pro=pro, user=current_user)

            
            else:
                return "NO SUCH Category OR Product AVAILABLE"
        else:
            flash("Please Enter Something",category="success")
    return redirect(url_for('auth.usermain'))

