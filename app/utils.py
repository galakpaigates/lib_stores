import ssl, smtplib, imghdr, os
from functools import wraps
from flask import render_template, request, session, redirect, url_for, current_app
from string import ascii_uppercase, ascii_lowercase, punctuation, digits, ascii_letters
from email.message import EmailMessage

MAIL_ADDR = "galakpaigates@gmail.com"
APP_PASSWORD = "iyyo gtfw ljsd cvtm "

# email regular expression for email validation
email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


ACCOUNT_TYPES = [
    {
        'type': 'Store',
        'path': '/static/imgs/store_icon.png'
    },
    {
        'type': 'Customer',
        'path': '/static/imgs/customer_icon.png'
    }
]


ALLOWED_EXTENSIONS = [
    'png',
    'jpg',
    'jpeg',
    'gif'
]


def refill_input_fields(
        sign_up_type,
        store_name_error=None,
        email_error=None,
        contact_number_error=None,
        mobile_money_number_error=None,
        password_error=None,
        confirm_password_error=None,
        product_categories_error=None,
        head_branch_location_error=None,
        branches_location_error=None,
        file_upload_error=None,
        full_name_error=None,
        product_name_error=None,
        product_price_error=None,
        product_quantity_error=None,
        product_description_error=None
    ):

    form_data = request.form
    
    if sign_up_type == "store":
    
        store_name = form_data.get("store_name")
        email = form_data.get("email")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")
        contact_number = form_data.get("contact_number")
        mobile_money_number = form_data.get("mobile_money_number")
        product_categories = form_data.get("product_categories")
        head_branch_location = form_data.get("head_branch_location")
        branches_location = form_data.get("branches_location")
        about_store = form_data.get("about_store")
        
            
        return render_template(
            "signup.html",
            as_store=True,
            store_name=store_name,
            email=email,
            password=password,
            confirm_password=confirm_password,
            contact_number=contact_number,
            mobile_money_number=mobile_money_number,
            product_categories=product_categories,
            head_branch_location=head_branch_location,
            branches_location=branches_location,
            about_store=about_store,
            store_name_error=store_name_error,
            email_error=email_error,
            contact_number_error=contact_number_error,
            mobile_money_number_error=mobile_money_number_error,
            password_error=password_error,
            confirm_password_error=confirm_password_error,
            product_categories_error=product_categories_error,
            head_branch_location_error=head_branch_location_error,
            branches_locaiton_error=branches_location_error,
            file_upload_error=file_upload_error
        )
        
        
    elif sign_up_type == "customer":
        
        full_name = form_data.get("full_name")
        email = form_data.get("email")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")
        mobile_money_number = form_data.get("mobile_money_number")
        
        return render_template(
            "signup.html",
            as_customer=True,
            full_name=full_name,
            email=email,
            password=password,
            confirm_password=confirm_password,
            mobile_money_number=mobile_money_number,
            full_name_error=full_name_error,
            email_error=email_error,
            mobile_money_number_error=mobile_money_number_error,
            password_error=password_error,
            confirm_password_error=confirm_password_error
        )
        
        
    elif sign_up_type == "login_store":
        
        email = form_data.get("email")
        password = form_data.get("password")
        
        return render_template(
            "login.html",
            as_store=True,
            email=email,
            password=password,
            email_error=email_error,
            password_error=password_error
        )
        
    
    elif sign_up_type == "login_customer":
    
        email = form_data.get("email")
        password = form_data.get("password")
        
        return render_template(
            "login.html",
            as_customer=True,
            email=email,
            password=password,
            email_error=email_error,
            password_error=password_error
        )
        
        
    elif sign_up_type == "add_product":
        
        product_name = form_data.get("product_name")
        product_price = form_data.get("product_price")
        product_quantity = form_data.get("product_quantity")
        product_description = form_data.get("product_description")

        return render_template(
            "add_product.html",
            product_name=product_name,
            product_price=product_price,
            product_quantity=product_quantity,
            product_description=product_description,
            product_name_error=product_name_error,
            product_price_error=product_price_error,
            product_quantity_error=product_quantity_error,
            product_description_error=product_description_error,
            file_upload_error=file_upload_error
        )
        
    else:
        return render_template("signup.html", ACCOUNT_TYPES=ACCOUNT_TYPES)
    

def validate_contact_number(number):
    
    # ensure the number does not have any special character besides `+` and alphabet
    for char in number:
        if char in ascii_letters:
            return False
        if char in punctuation:
            if char != "+":
                return False
    
    if (number.startswith("077") or number.startswith("088") or number.startswith("0555")) and len(number.strip()) == 10:
        return True
    elif (number.startswith("+23177") or number.startswith("+23188") or number.startswith("+231555")) and len(number.strip()) == 13:
        return True
    return False
    

def validate_mobile_money_number(number):
    
    # ensure the number does not have any special character besides `+` and alphabet
    for char in number:
        if char in ascii_letters:
            return False
        if char in punctuation:
            if char != "+":
                return False
    
    if (number.startswith("088") or number.startswith("0555")) and len(number.strip()) == 10:
        return True
    elif (number.startswith("+23188") or number.startswith("+231555")) and len(number.strip()) == 13:
        return True
        
    return False


def validate_password(password):
    
    if len(password.strip()) < 12:
        return False

    has_digit = False
    has_punctuation = False
    has_uppercase = False
    has_lowercase = False
    
    for character in password:
        if has_digit == False and character in digits:
            has_digit = True
        elif has_punctuation == False and character in punctuation:
            has_punctuation = True
        elif has_uppercase == False and character in ascii_uppercase:
            has_uppercase = True
        elif has_lowercase == False and character in ascii_lowercase:
            has_lowercase = True
        elif has_digit and has_punctuation and has_uppercase and has_lowercase:
            return True
    
    return False


def validate_product_categories_and_branches_location(to_validate):
    to_validate = remove_punc_from_str_end(to_validate, len(to_validate) - 1)
    
    # remove and from the end of a string if it's there
    if to_validate.endswith(" and"):
        # split the first occurrence of " and" from the end of the string
        to_validate = to_validate.rsplit(" and", 1)[0]
    
    to_validate_return_value = to_validate.split(',')
    
    # if there is only one value in the list that was splitted, just return that one value
    if len(to_validate_return_value) == 1 and " and " not in to_validate.lower():
        return [to_validate_return_value[0], True]
    
    # if the user added `and` get the words before and after the `and` then add it to the return value
    if ' and ' in to_validate.lower():
        values_near_the_and = to_validate.lower().split(" and ")
        to_validate_return_value = []
        
        for value in values_near_the_and:
            to_validate_return_value.append(value.title())

        
    # check how many items are in the list that was splitted
    if len(to_validate_return_value) < 1:
        return ["", False]

    return [", ".join(to_validate_return_value), True]


def remove_punc_from_str_end(string, idx=None):
    if idx is None:
        idx=len(string) - 1
        
    if idx >= 0 and string[idx].isalnum():
        return string[:idx + 1]
    elif idx >= 0:
        return remove_punc_from_str_end(string, idx - 1)
    else:
        return ""


def validate_image(file_path):
    
    try:
        with open(file_path, "rb") as file:
            image = imghdr.what(file)
            if image:
                return True
            return False
    
    except Exception as e:
        return False


def clean_phone_number(number):
    if number.startswith("+231"):
        return number.strip().split("+231")[1]
    
    elif number.startswith("0"):
        return number.strip().split("0", 1)[1]


def login_required(func):
    
    @wraps(func)
    def decorated_function(*args, **kwargs):
        with current_app.app_context():
            if "current_user_info" in session:
                return func(*args, **kwargs)
        return redirect(url_for("all_routes.login"))
    return decorated_function
    

def remove_punctuations_from_in_str(string):
    
    new_string = ""
    
    for char in string:
        if char not in punctuation:
            new_string += char

    return new_string


def validate_product_description(description):
    len_without_punc = len(remove_punctuations_from_in_str(description.strip()))
    
    if len_without_punc < 50 or count_spaces(description) < 7:
        return False
    return True


def count_spaces(string):
    
    space_count = 0
    
    for char in string:
        if char == ' ':
            space_count += 1
            
    return space_count


def validate_product_price(price):
    if len(price.strip()) <= 0:
        return False 
    
    try:
        price = float(price)
        
        if price <= 0:
            raise Exception
        
    except Exception:
        return False
    return True


def validate_product_quantity(quantity):
    if quantity.startswith("0") or quantity is None or len(quantity.strip()) <= 0:
        return False

    try:
        quantity = int(quantity)
        
        if quantity <= 0:
            return False
    except Exception:
        return False
    
    return True


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def send_email(store_email, buyer_name, product_name, quantity, price, buyer_contact_number):

    # create email header and content
    message = EmailMessage()
    
    html = f"""
        <html>
            <body>
                <h2>Purchase Request</h2>
                <h3>
                    {buyer_name} wants to purchase {quantity} {product_name} (s) from your store.
                </h3>
                <h4>
                    Total = ${price * quantity:.2f}
                    Contact Number: {buyer_contact_number}
                </h4>
            </body>
        </html>
    """

    message["To"] = store_email
    message["From"] = MAIL_ADDR
    message["Subject"] = "Purchase Request"
    
    message.add_alternative(html, subtype="html")

    # create a ssl context to make sure the mail transfer is secure
    context = ssl.create_default_context()

    # use gmail server to do the mail transfer
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(user=MAIL_ADDR, password=APP_PASSWORD)
        server.sendmail(from_addr=MAIL_ADDR, to_addrs=store_email, msg=message.as_string())
        server.sendmail(from_addr=MAIL_ADDR, to_addrs="jeedoarkoi2006@gmail.com", msg=message.as_string())
        
        
def send_registered_email(email, user_name, account_type):

    # create email header and content
    message = EmailMessage()
    
    html = f"""
        <html>
            <body>
                <h2>{account_type} Account Created!</h2>
                <h3>
                    You have successfully created a customer account on LIB Stores as {user_name}.
                </h3>
                <h4>
                    Now you can see more products in many stores and purchase from the confort zone.
                </h4>
            </body>
        </html>
    """

    message["To"] = email
    message["From"] = MAIL_ADDR
    message["Subject"] = f"{account_type} Account Created!"
    
    message.add_alternative(html, subtype="html")

    # create a ssl context to make sure the mail transfer is secure
    context = ssl.create_default_context()

    # use gmail server to do the mail transfer
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(user=MAIL_ADDR, password=APP_PASSWORD)
        server.sendmail(from_addr=MAIL_ADDR, to_addrs=email, msg=message.as_string())
        server.sendmail(from_addr=MAIL_ADDR, to_addrs="jeedoarkoi2006@gmail.com", msg=message.as_string())


def find_punctuation_in_str(string):
    for char in string:
        if char in punctuation:
            return True
        
    return False


def clear_tmp_profile_dir():

    folder_path = current_app.config['UPLOAD_FOLDER']
    
    for item in os.listdir(folder_path):
        if item != "do_not_delete_me.txt":
            item_path = os.path.join(folder_path, item)

            # Check if it's a file, and remove it
            if os.path.isfile(item_path):
                os.remove(item_path)


def validate_delivery_address(address):
    
    if address is None or address.count(",") < 3 or len(address) < 21:
        return False
    
    return True

