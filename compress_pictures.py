import cs50, base64, gzip

# Connect to the database
db = cs50.SQL("sqlite:///lib_stores.db")

# Query the database to retrieve all profile_picture BLOBs
rows = db.execute("SELECT id, picture FROM product_pictures")

# Iterate through the result set
for row in rows:
    # Get the id and profile_picture BLOB
    picture_id = row["id"]
    profile_picture_blob = row["picture"]
    
    # Compress the profile_picture BLOB using gzip
    compressed_blob = gzip.compress(profile_picture_blob)
    
    # Encode the compressed BLOB as Base64
    compressed_blob_base64 = base64.b64encode(compressed_blob)
    
    # Update the corresponding row in the database with the compressed BLOB
    db.execute("UPDATE product_pictures SET picture = ? WHERE id = ?", compressed_blob_base64, picture_id)

print("Profile pictures compressed and updated in the database.")
