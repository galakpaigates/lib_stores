from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import re, os, base64
from datetime import datetime

from .utils import *
from . import lib_stores_db

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

all_routes = Blueprint("all_routes", __name__)


# display all stores
@all_routes.route("/stores/")
@login_required
def display_all_stores():
    all_existing_stores = lib_stores_db.execute("SELECT * FROM stores ORDER BY RANDOM();")
    
    # convert each BLOB profile picture to a base64 string that can be used as src in an `img` tag
    for store in all_existing_stores:
        store['profile_picture'] = base64.b64encode(store['profile_picture']).decode('utf-8')
    
    return render_template("stores.html", all_existing_stores=all_existing_stores)


@all_routes.route("/stores/<store_name_id>")
@login_required
def dynamic_store(store_name_id):
    
    store_name, store_id = store_name_id.split("+")
    
    # check for IndexError or any other error in the split to show that there is no `id` and claim the the route is invalid
    try:
        store_full_information = lib_stores_db.execute("SELECT * FROM stores WHERE id = ?;", store_id)[0]
    except Exception:
        flash(message=("Invalid Store!", "Error: The requested store does not exists in LIB Stores!"), category="danger")
        return redirect(url_for("all_routes.display_all_stores"))
    
    # check if the name passed with the url is the same as the name in the database for the user with the `id`
    if len(store_full_information) <= 0 or store_full_information['name'] != store_name.replace("-", " "):
        flash(message=("Invalid Store!", "Error: The requested store does not exists in LIB Stores!"), category="danger")
        return redirect(url_for("all_routes.display_all_stores"))
    
    # convert the store's profile picture from BLOB to base64 string
    store_full_information['profile_picture'] = base64.b64encode(store_full_information['profile_picture']).decode('utf-8')
    
    store_products = lib_stores_db.execute("SELECT * FROM products WHERE store_id = ?", store_id)
        
    product_id_and_photos = {}
    
    for product_info in store_products:
        # format the price as USD ($29.93)
        product_info['price'] = usd(product_info['price'])
        
        product_id_and_photos[product_info['id']] = lib_stores_db.execute(
            """
                SELECT picture FROM product_pictures
                WHERE product_id = ?
            """,
            product_info['id']
        )
        
    """
        loop through the `store_products` and use the id to uniquely 
        identify elements in the `product_id_and_info` dictionary that would have
        a key that will be an id of a product and the value of the `product_id_and_info`
        is an array that was returned by the SQL query which would be a list
    """
    
    for product_info in store_products:
        for info_and_id in product_id_and_photos[product_info['id']]:
            # conver each picture BLOB that returned from the SQL query to a base 64 image
            info_and_id['picture'] = base64.b64encode(info_and_id['picture']).decode("utf-8")
    
    return render_template("stores.html", store_full_information=store_full_information, store_products=store_products, product_id_and_photos=product_id_and_photos)


@all_routes.route("/sign-up/", methods=['GET', 'POST'])
def sign_up():
    return render_template("signup.html", ACCOUNT_TYPES=ACCOUNT_TYPES)


@all_routes.route("/sign-up/store/", methods=['GET', 'POST'])
def sign_up_as_store():
    
    if request.method == "POST":
        form_data = request.form
        
        # get data from individual input fields
        store_name = form_data.get("store_name")
        email = form_data.get("email")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")
        contact_number = form_data.get("contact_number")
        mobile_money_number = form_data.get("mobile_money_number")
        head_branch_location = form_data.get("head_branch_location")
        branches_location = form_data.get("branches_location")
        product_categories = form_data.get("product_categories")
        about_store = form_data.get("about_store")
        profile_picture = request.files.get("profile_picture_input")
        
        # validate store's sign up information
        
        # store name too short
        if len(store_name.strip()) < 2:
            return refill_input_fields(sign_up_type="store", store_name_error="Store Name must be atleast 2 character long")
        
        # store name too long
        elif len(store_name.strip()) > 120:
            return refill_input_fields(sign_up_type="store", store_name_error="Store Name must be atmost 120 character long")
        
        # ensure store name does not have special characters
        elif find_punctuation_in_str(store_name.strip()):
            return refill_input_fields(sign_up_type="store", store_name_error="Store Name must not contain any special character")
        
        # email not valid
        elif re.match(email_regex, email) is None:
            return refill_input_fields(sign_up_type="store", email_error="Invalid email address!")
        
        # check if the email already exists
        elif len(lib_stores_db.execute("SELECT email FROM stores WHERE email = ?", email)) > 0:
                return refill_input_fields(sign_up_type="store", email_error="Email address already exists!")

        # contact number not valid
        elif not validate_contact_number(contact_number):            
            return refill_input_fields(sign_up_type="store", contact_number_error="Invalid contact number! e.g. 0775326934 or +231555943559 or 0888061282")
        
        # check if the contact_number already exists
        elif len(lib_stores_db.execute("SELECT contact_number FROM stores WHERE contact_number = ?", clean_phone_number(contact_number))) > 0:
            return refill_input_fields(sign_up_type="store", contact_number_error="This contact number already exists!")
        
        # mobile money number not valid
        elif not validate_mobile_money_number(mobile_money_number):
            return refill_input_fields(sign_up_type="store", mobile_money_number_error="Invalid mobile money number! e.g. 0888061282 or +231555943559")
        
        # check if the mobile_money_number does not already exists
        elif len(lib_stores_db.execute("SELECT mobile_money_number FROM stores WHERE mobile_money_number = ?", clean_phone_number(mobile_money_number))) > 0:
            return refill_input_fields(sign_up_type="store", mobile_money_number_error="This mobile money number address already exists!")
        
        # ensure password len(password) >= 12 and lower upper punc and digit in password
        elif not validate_password(password):
            return refill_input_fields(sign_up_type="store", password_error="Password must be atleast 12 characters long and must have atleast one special symbol, uppercase, lowercase and number")

        # ensure the confirmation password is the same as the first password
        elif confirm_password != password:
            return refill_input_fields(sign_up_type="store", confirm_password_error="Passwords don't match!")
        
        # check if the actually provided a category of product atleast a single word
        # check the boolean value in the tuple that was returned
        elif not validate_product_categories_and_branches_location(product_categories)[1]:
            return refill_input_fields(sign_up_type="store", product_categories_error="Invalid product category! Please follow the specifications above!")

        # ensure the user actually gave a head branch
        elif head_branch_location is None or len(head_branch_location) < 2:
            return refill_input_fields(sign_up_type="store", head_branch_location_error="Please provide a descriptive Head Branch location!")

        # check if the actually provided a location atleast a single word
        # check the boolean value in the tuple that was returned
        elif not validate_product_categories_and_branches_location(branches_location)[1]:
            return refill_input_fields(sign_up_type="store", branches_location_error="Invalid branches location! Please follow the specifications above!")
        
        # validate profile picture
        elif len(profile_picture.filename) < 5:
            return refill_input_fields(sign_up_type="store", file_upload_error="Profile Picture / Logo is required!")

        elif not isinstance(profile_picture, FileStorage) or profile_picture is None or profile_picture.filename is None:
            return refill_input_fields(sign_up_type="store", file_upload_error="Please provide a valid image!")

        # save the file to a temporary location to open it and read its information, then store in the database as BLOB
        filename = secure_filename(profile_picture.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        profile_picture.save(filepath)
        
        # final image validation to check the dimensions and format of the uploaded file
        if validate_image(filepath) == False:
            return refill_input_fields(sign_up_type="store", file_upload_error="Please provide a valid image!")

        with open(filepath, 'rb') as uploaded_picture:
            picture_data = uploaded_picture.read()
             
                
        # update product_categories and branches_location per the changes in teh validation function
        branches_location = validate_product_categories_and_branches_location(branches_location)[0]
        product_categories = validate_product_categories_and_branches_location(product_categories)[0]
                
        # make sure about store has a value that can be stored in the database and not None
        if about_store is None or len(about_store.strip()) <= 0:
            about_store = ""
        
        # add the new store to database's stores table
        lib_stores_db.execute(
            """
                INSERT INTO stores (
                    name, 
                    email,
                    password,
                    account_creation_date,
                    contact_number,
                    mobile_money_number,
                    categories_of_product,
                    head_branch_location,
                    branches_location,
                    about,
                    profile_picture
                ) VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                );
            """,
            store_name,
            email,
            generate_password_hash(password=password, method='pbkdf2:sha512:600000'),
            datetime.now().strftime("%d-%m-%Y %H:%M"),
            clean_phone_number(contact_number),
            clean_phone_number(mobile_money_number),
            product_categories,
            head_branch_location,
            branches_location,
            about_store,
            picture_data
        )
        
        # remove image that was temporarily saved to upload to database
        clear_tmp_profile_dir()
        
        flash(message=("Store Registered!", "Success: You now have your Store on LIB Stores!",), category="success")
        return redirect(url_for("index"))
        
    
    return render_template("signup.html", as_store=True)


@all_routes.route("/sign-up/customer/", methods=['GET', 'POST'])
def sign_up_as_customer():
    
    if request.method == "POST":
        form_data = request.form
        
        # validate customer's sign up information
        full_name = form_data.get("full_name").strip()
        email = form_data.get("email")
        mobile_money_number = form_data.get("mobile_money_number")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")

        # ensure name is atleast 5 characters long and has atleast one space assuming it seperates first and last name
        if len(full_name) < 5 or ' ' not in full_name:
            return refill_input_fields(sign_up_type="customer", full_name_error="Please input a proper full name! e.g: John Carter or James Benedict Tarnue")
        
        # validate email using regex
        elif re.match(email_regex, email) is None:
            return refill_input_fields(sign_up_type="customer", email_error="Invalid email address!")
        
        # ensure it's a valid Lonestar number
        elif not validate_mobile_money_number(mobile_money_number):
            return refill_input_fields(sign_up_type="customer", mobile_money_number_error="Invalid mobile money number! Please enter a valid Lonestar Cell MTN number!  e.g. 0888061282 or +231555943559")

        # ensure password is atleast 12 characters long and has punc, upper, lower and int
        elif not validate_password(password):
            return refill_input_fields(sign_up_type="customer", password_error="Password must be atleast 12 character long and must have atleast one punctuation, uppercase, lowercase and number!")

        # ensure confirmation password is the same as the first password
        elif confirm_password != password:
            return refill_input_fields(sign_up_type="customer", confirm_password_error="Passwords don't match!")
        
        # add this customer to the customers table in lib_stores_db
        lib_stores_db.execute(
            """
                INSERT INTO customers (
                    name, 
                    email,
                    password,
                    mobile_money_number,
                    account_creation_date
                ) VALUES (
                    ?, ?, ?, ?, ?
                );
            """,
            full_name,
            email,
            generate_password_hash(password=password, method='pbkdf2:sha512:600000'),
            clean_phone_number(mobile_money_number),
            datetime.now().strftime("%d-%m-%Y %H:%M")
        )
        
        flash(message=("Account Registered!", "Success: You now have your LIB Stores Account as a Customer!",), category="success")
        return redirect(url_for("index"))
    
    return render_template("signup.html", as_customer=True)


@all_routes.route("/login/", methods=['POST', 'GET'])
def login():
    return render_template("login.html", ACCOUNT_TYPES=ACCOUNT_TYPES)


@all_routes.route("/login/store", methods=['POST', 'GET'])
def login_as_store():
    
    # make sure the current user's information is cleared
    session.clear()
    
    if request.method == "POST":
        form_data = request.form
        
        # get the values in the form
        email = form_data.get("email")
        password = form_data.get("password")

        # check for proper email pattern using regular expression
        if re.match(email_regex, email) is None:
            return refill_input_fields(sign_up_type="login_store", email_error="Invalid email address!")
        
        # check if the password meets the requirements
        elif not validate_password(password):
            return refill_input_fields(sign_up_type="login_store", password_error="Invalid password! Password does not meet the requirements!")
        
        # get the store in the database that have a matching email
        existing_store = lib_stores_db.execute("SELECT * FROM stores WHERE email = ?;", email)
        
        # check if there is a user with that email
        if len(existing_store) <= 0:
            return refill_input_fields(sign_up_type="login_store", email_error="Email does not exists!")
        
        # get the first user that will be returned as a list of dicts, even though it must be one
        existing_store = existing_store[0]
        
        # check if the password matches the password in the database
        if not check_password_hash(existing_store['password'], password):
            return refill_input_fields(sign_up_type="login_store", password_error="Incorrect password!")
        
        # store information in session to indicate the user is logged in
        session['current_user_info'] = {
            'id': existing_store['id'],
            'account_type': 'store'
        }
        
        flash(message=("Successfully Logged In!", "Success: You have Logged In to your Store as Manager!",), category="success")
        return redirect(url_for("index"))
    
    return render_template("login.html", as_store=True)


@all_routes.route("/login/customer", methods=['POST', 'GET'])
def login_as_customer():
    
    # make sure the current user's information is cleared
    session.clear()
    
    if request.method == "POST":
        form_data = request.form

        # get the values in the form
        email = form_data.get("email")
        password = form_data.get("password")
        
        # check for proper email pattern using regular expression
        if re.match(email_regex, email) is None:
            return refill_input_fields(sign_up_type="login_customer", email_error="Invalid email address!")
        
        # check if the password meets the requirements
        elif not validate_password(password):
            return refill_input_fields(sign_up_type="login_customer", password_error="Invalid password! Password does not meet the requirements!")
        
        # get the store in the database that have a matching email
        existing_customer = lib_stores_db.execute("SELECT * FROM customers WHERE email = ?;", email)
        
        # check if there is a user with that email
        if len(existing_customer) <= 0:
            return refill_input_fields(sign_up_type="login_customer", email_error="Email does not exists!")
        
        # get the first user that will be returned as a list of dicts, even though it must be one
        existing_customer = existing_customer[0]
        
        # check if the password matches the password in the database
        if not check_password_hash(existing_customer['password'], password):
            return refill_input_fields(sign_up_type="login_customer", password_error="Incorrect password!")
        
        # store information in session to indicate the user is logged in
        session['current_user_info'] = {
            'id': existing_customer['id'],
            'account_type': 'customer'
        }
        
        flash(message=("Successfully Logged In!", "Success: You have Logged In to LIB Stores as a Customer!",), category="success")
        return redirect(url_for("index"))
        
        
    return render_template("login.html", as_customer=True)


@all_routes.route("/logout")
@login_required
def logout():
    
    # clear all the saved information from the session to indicate the user has logged out
    session.clear()
    
    # then send the user to the login page
    return redirect(url_for("all_routes.login"))


@all_routes.route("/add-product", methods=['POST', 'GET'])
@login_required
def add_product():
    
    if request.method == "POST":
        
        form_data = request.form
        product_picture_list = request.files.getlist("product_pictures_input[]")
        
        # get input fields values from the form
        product_name = form_data.get("product_name")
        product_price = form_data.get("product_price")
        product_quantity = form_data.get("product_quantity")
        product_description = form_data.get("product_description")
        
        if len(product_name.strip()) <= 3 or ' ' not in product_name.strip():
            return refill_input_fields(sign_up_type="add_product", product_name_error="Please provide a descriptive product name! e.g. 'Face cap' instead of just 'Cap' or 'Cowboy Hat' instead of just 'Hat'")
        
        elif not validate_product_price(product_price):
            return refill_input_fields(sign_up_type="add_product", product_price_error="Product price must be a positive real number! e.g. 12.5 or 19.0")
        
        # make sure quantity is an integer without numbers after the decimal place
        elif not validate_product_quantity(product_quantity):
            return refill_input_fields(sign_up_type="add_product", product_quantity_error="Product quantity must be a positive interger without decimal! e.g. 10 or 7 or 123")

        # ensure description is atleast 50 character with punctuations and spaces being counted and there are atleast 7 spaces in the description
        elif not validate_product_description(product_description):
            return refill_input_fields(sign_up_type="add_product", product_description_error="Product description must be atleast 60 characters long inorder to convince your customer to buy your product! (punctuations and spaces don't count)")

        picture_data_list = []

        for product_picture in product_picture_list:

            # validate profile picture
            if len(product_picture.filename) < 5:
                return refill_input_fields(sign_up_type="add_product", file_upload_error="Please provide picture(s) for your product!")

            elif not isinstance(product_picture, FileStorage) or product_picture is None or product_picture.filename is None:
                return refill_input_fields(sign_up_type="add_product", file_upload_error="Please provide a valid image!")

            # save the file to a temporary location to open it and read its information, then store in the database as BLOB
            filename = secure_filename(product_picture.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            product_picture.save(filepath)
            
            # final image validation to check the dimensions and format of the uploaded file
            if validate_image(filepath) == False:
                return refill_input_fields(sign_up_type="add_product", file_upload_error="Please provide a valid image!")

            # open the file and save the data in a temporary array
            with open(filepath, 'rb') as uploaded_picture:
                picture_data_list.append(uploaded_picture.read())

                
        # ensure the information are in the format you want to store in the database
        product_name = product_name.title()
        product_price = float(product_price)
        product_quantity = int(product_quantity)
        product_description = product_description.strip()
            
        lib_stores_db.execute("BEGIN TRANSACTION;")
        
        # add the product information to the products table in the database
        lib_stores_db.execute(
            """
                INSERT INTO products (
                    store_id,
                    name,
                    price,
                    quantity,
                    description,
                    creation_date
                ) VALUES (
                    ?, ?, ?, ?, ?, ?
                );
            """,
            session['current_user_info']['id'],
            product_name,
            product_price,
            product_quantity,
            product_description,
            datetime.now().strftime("%d-%m-%Y %M:%H")
        )
        
        # get the id of the product we added above
        just_added_product_id = lib_stores_db.execute(
            """
                SELECT id FROM products
                ORDER BY id DESC
                LIMIT 1;
            """
        )[0]['id']
        
        # add each picture to the product pictures database with a corresponding product_id
        for picture_data in picture_data_list:
        
            lib_stores_db.execute(
                """
                    INSERT INTO product_pictures (
                        product_id,
                        picture
                    ) VALUES (
                        ?, ?
                    )
                """,
                just_added_product_id,
                picture_data
            )

        lib_stores_db.execute("COMMIT;")
        
        # delete all the temporarily saved pictures
        clear_tmp_profile_dir()

        picture_data_list = []
        flash(message=("Product Added!", "Success: You have added a Product to your Store!"), category="success")
        return redirect(url_for("index"))

    return render_template("add_product.html")


@all_routes.route("/products/<product_id_and_store_id>")
@login_required
def product_page(product_id_and_store_id):

    particular_product = lib_stores_db.execute(
        """
            SELECT * FROM products 
            WHERE id = ? 
            AND 
            store_id = ?;
        """,
        product_id_and_store_id.rsplit("+")[0],
        product_id_and_store_id.rsplit("+")[1]
    )[0]
    
    # get the name of the store that owns the product to use as the anchor the the stores pages
    store_name = lib_stores_db.execute(
        """
            SELECT name FROM stores 
            WHERE id = ?;
        """,
        product_id_and_store_id.rsplit("+")[1]
    )[0]['name']
    
    particular_product_photos = lib_stores_db.execute(
        """
            SELECT picture FROM product_pictures
            WHERE product_id = ?
        """,
        particular_product['id']
    )
    
    for each_picture in particular_product_photos:
        each_picture['picture'] = base64.b64encode(each_picture['picture']).decode('utf-8')
        
    particular_product['price'] = usd(particular_product['price'])
    
    return render_template("product_page.html", particular_product=particular_product, store_name=store_name, particular_product_photos=particular_product_photos, product_id_and_store_id=product_id_and_store_id)


@all_routes.route("/buy", methods=['POST', 'GET'])
@login_required
def buy():
    product_quantity = request.form.get("product_quantity")
    product_id_and_store_id = request.form.get("product_id_and_store_id")
    
    # make sure the store id and product id were not tampered with by inspecting the html
    if product_id_and_store_id is None or "+" not in product_id_and_store_id:
        flash(message=("Error purchasing product!", "Sensitive Information may have been tampered with!"))
        return redirect(request.headers.get("Referer"))
    
    # seperate the store id and the product id
    product_id, store_id = product_id_and_store_id.rsplit("+")
    
    # ensure they were changed by inspecting the html
    if product_id.isdigit() == False and store_id.isdigit() == False:
        flash(message=("Error purchasing product!", "Sensitive Information may have been tampered with!"), category="danger")
        return redirect(request.headers.get("Referer"))

    # validate quantity
    if not validate_product_quantity(product_quantity):
        flash(message=("Invalid Quantity!", "Product quantity must be a positive interger without decimal! e.g. 10 or 7 or 123"), category="danger")
        return redirect(request.headers.get("Referer"))
    
    # reduce the quantity of that particular product in the database by the amount bought
    current_product_info = lib_stores_db.execute(
        """
            SELECT quantity, name, price FROM products
            WHERE store_id = ?
            AND
            id = ?;
        """,
        store_id,
        product_id
    )
    
    # ensure there is a product with that store_id and product_id
    if len(current_product_info) <= 0:
        flash(message=("Error purchasing product!", "Product not found!"), category="danger")
        return redirect(request.headers.get("Referer"))
    
    current_product_quantity = int(current_product_info[0]['quantity'])
    
    # update the product quantity
    current_product_quantity -= int(product_quantity)
    
    # ensure there is enough available product to purchase
    if current_product_quantity < 0:
        flash(message=("Not enough product", f"The quantity of product available for sale is less than what you've ordered! ({current_product_quantity + int(product_quantity)} is currently available for sale!)"), category="danger")
        return redirect(request.headers.get("Referer"))
    
    lib_stores_db.execute(
        """
            UPDATE products
            SET quantity = ?
            WHERE store_id = ?
            AND
            id = ?;
        """,
        current_product_quantity,
        store_id,
        product_id
    )
    
    # send an email to the store informing them about the purchase request
    
    # get the email address to send the purchase request to
    store_email = lib_stores_db.execute(
        """
            SELECT email FROM stores
            WHERE id = ?
        """,
        store_id
    )[0]['email']
    
    # get the name of the buyer from the session    
    if session["current_user_info"]["account_type"] == "customer":
        buyer_name = lib_stores_db.execute(
            """
                SELECT name FROM customers
                WHERE id = ?;
            """,
            session["current_user_info"]['id']
        )[0]['name']
        
    else:
        buyer_name = lib_stores_db.execute(
            """
                SELECT name FROM stores
                WHERE id = ?;
            """,
            session["current_user_info"]["id"]
        )[0]['name']
        
    # get the price and name of the product to be purchased
    price = float(current_product_info[0]['price'])
    product_name = current_product_info[0]['name']
    
    # send email to the store as a purchase request
    send_email(store_email=store_email, buyer_name=buyer_name, product_name=product_name, quantity=int(product_quantity), price=price)
    
    flash(message=("Product Purchased!", "Success: You have purchased the product!"), category="success")
    return redirect(url_for("index"))


@all_routes.route("/test_error")
def test_error():
    # Simulate a server error
    1 / 0  # This will raise a ZeroDivisionError

