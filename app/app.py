from __init__ import create_app, lib_stores_db
import os, base64
from flask import redirect, url_for, flash, render_template, request
from utils import login_required, usd

app = create_app()

# display homepage
@app.route("/")
@login_required
def index():
    
    full_product_information = lib_stores_db.execute(
        """
            SELECT * FROM products
            ORDER BY RANDOM();
        """
    )
    
    product_id_and_photos = {}
    
    for product_info in full_product_information:
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
        loop through the `full_product_information` and use the id to uniquely 
        identify elements in the `product_id_and_info` dictionary that would have
        a key that will be an id of a product and the value of the `product_id_and_info`
        is an array that was returned by the SQL query which would be a list
    """
    
    for product_info in full_product_information:
        for info_and_id in product_id_and_photos[product_info['id']]:
            # conver each picture BLOB that returned from the SQL query to a base 64 image
            info_and_id['picture'] = base64.b64encode(info_and_id['picture']).decode("utf-8")
        
    
    return render_template("index.html", full_product_information=full_product_information, product_id_and_photos=product_id_and_photos)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))