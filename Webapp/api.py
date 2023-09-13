from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import render_template
from flask_login import login_required
from .models import Category,Product
from flask_restful import Api,Resource,abort
from flask_login import login_user, login_required, logout_user, current_user

from . import db
from flask import jsonify

apis = Blueprint('api',__name__)
api=Api(apis)
class CategoryApi(Resource):
    def get(self):
        pass
    def post(self,ev=None):
        if ev is not None:  # Check if ev is provided, which means it's an edit request
            try:
                ev = int(ev)  # Ensure ev is converted to an integer

                # Find the category to edit
                category_to_edit = Category.query.filter_by(id=ev).first()

                if category_to_edit:
                    name = request.form.get('vname')
                    if name != '':
                        category_to_edit.name = name
                        db.session.commit()
                        flash("Category Edited Succcsessfully",category="success")
                        return redirect(url_for('auth.adminmain'))
                    else:
                        flash("Invalid Format", category='error')
                        return redirect(url_for('auth.editcategory',ev=ev))
                else:
                    flash("Category not found", category='error')
                    return redirect(url_for('auth.editcategory',ev=ev))

            except ValueError:
                flash("Category not found", category='error')
                return redirect(url_for('auth.editcategory',ev=ev))
        else:
            # ... Your existing POST method code for creating a category ...
            name1 = request.form.get('vname')
            print(name1)
            if name1 != '':
                # Add your database operations here
                # Assuming you have already imported necessary modules for SQLAlchemy

                new_category = Category(name=name1)
                db.session.add(new_category)
                db.session.commit()

                flash("Category added", category='success')
                return redirect(url_for('auth.adminmain'))
            
            else:
                flash("Invalid Format", category='error')
                return redirect(url_for('auth.create'))

class Productapi(Resource):
    # def get(self):
    #     pass
    
    def post(self,pk):
        name = request.form.get('sname')
        expiry = request.form.get('expiry')
        expiry2 = request.form.get('radio')
        print(expiry,type(expiry))
        if expiry=='':
            expiry=expiry2
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        print(name)
        if name!='' and quantity!='' or price!='' :
            new_product = Product(name=name, expirydate=expiry,
                            quantity=quantity, price=price, category_id=int(pk))
            db.session.add(new_product)
            db.session.commit()
            flash("Product added", category='success')
            return redirect(url_for('auth.adminmain'))
        else:
            flash("Invalid Input", category='error')
            return redirect(url_for('auth.product',pk=pk))
    
class EditProductapi(Resource):
    # def get(self):
    #     pass
    
    def post(self,es):
        editt = Product.query.filter_by(id=str(es)).first()
        
        name = request.form.get('sname')
        expiry = request.form.get('expiry')
        expiry2 = request.form.get('radio')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        print(expiry,type(expiry))
        if expiry=='':
            expiry=expiry2
        if name!='' and quantity!='' or price!='' :
            editt.name = name
            editt.expirydate = expiry
            editt.quantity = quantity
            editt.price = price

            db.session.commit()
            flash("Product edited succesfully", category='success')
            return redirect(url_for('auth.adminmain'))
        else:
            flash("Invalid Input", category='error')
            return redirect(url_for('auth.editproduct',es=es))
    

api.add_resource(CategoryApi, '/categoryapi', '/editcategoryapi/<int:ev>')
api.add_resource(Productapi, '/createproductapi/<int:pk>')
api.add_resource(EditProductapi, '/editproductapi/<int:es>')

# views.add_resource(Category, "/categoryapi/")
# class Signup(Resource):
#     def get(self):
#         return render_template('signup.html',user=current_user)

#     def post(self):
#         # email = request.form.get('email')
#         # name = request.form.get('name')
#         # password = request.form.get('password')
#         # args = signup_parser.parse_args()
#         # email = args.get("email")
#         # name = args.get("name") 
#         # password = args.get("password")
#         user = User.query.filter_by(email = email).first()
#         if user:
#             flash("Email already exists", category='error')
#         elif len(email) < 4:
#             flash("Email length error", category= 'error')
#         elif len(password) < 5:
#             flash("Password is too short", category='error')
#         else:
#             new_user = User(email = email, name = name, password = password,admin="False")
#             db.session.add(new_user)
#             db.session.commit()
#             flash("Account successfully created", category='success')
#             login_user(new_user, remember=True)
#             return jsonify({"message":"article created"})


     




# api=Api(app)
# class Signup(Resource):
#     # @marshal_with
#     def get(self):
#         return {"name":"harsh"}
    
#     # def post(self):
#     #     return {"name":"harshpost"}
    
# api.add_resource(Signup,'/hl')

# import requests
# BASE = "http://127.0.0.1:5000/"
# response = requests.get(BASE + 'hi')
# print(response.json())




# @views.route('/', methods = ['get','post'])
# @login_required
# def home():
    

#     return render_template("addVenue.html", user= current_user)
'''
# @views.route('/delete-note', methods = ["POST"])
# def delete_note():
#     note = json.loads(request.data)
#     noteID = note['noteID']
#     note = Notes.query.get(noteID)
#     if note:
#         if (note.user_id == current_user.id):
#             db.session.delete(note)
#             db.session.commit()
            
#     return jsonify({})
# @views.route('/home', methods = ['get','post'])
# @login_required
# def home():
#     # if (request.method == "POST"):
#     #     note = request.form.get('note')

#     #     if (len(note) < 1):
#     #         flash("Note length is too short", category='error')
#     #     else:
#     #         new_note = Notes(data = note, user_id = current_user.id)
#     #         db.session.add(new_note)
#     #         db.session.commit()
#     #         flash("Note added!", category='success')

#     return render_template("addVenue.html", user= current_user)   

# @views.route('/createvenue', methods = ['get','post'])
# @login_required
# def create():
#     if request.method=="POST":
#         name=request.form.get('name')
#         place=request.form.get('place')
#         location=request.form.get('location')
#         capacity=request.form.get('capacity')
#         new_venue=Venue(name=name, place=place, location=location, capacity=capacity)
#         db.session.add(new_venue)
#         db.session.commit()
#         flash("venue added", category='success')
        
#     return render_template("createVenue.html", user= current_user)
# @views.route('/create', methods=['get','post'])
# def home1():
#     if request.method=="GET":
#        return redirect('/createvenue')







# @views.route('/create', methods=["get","post"])
# def home():
#     var="true"
#     return render_template("createVenue.html",var=var, user = current_user)    
# @views.route('/main', methods=["get","post"])
# def home1():
   
#     return redirect(url_for('views.home'))
    '''