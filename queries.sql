 /* CREATE TABLE stores ( */ 
 /* 	id INTEGER, */
 /* 	name TEXT NOT NULL, */ 
 /* 	email TEXT NOT NULL UNIQUE, */ 
	/* password TEXT NOT NULL, */ 
 /* 	account_creation_date TEXT NOT NULL, */
	/* contact_number TEXT NOT NULL UNIQUE, */ 
	/* mobile_money_number TEXT NOT NULL UNIQUE, */ 
	/* categories_of_product TEXT NOT NULL, */ 
	/* head_branch_location TEXT NOT NULL, */
	/* branches_location TEXT NOT NULL, */ 
	/* about TEXT DEFAULT "Just Business", */ 
	/* profile_picture BLOB, */
 /* 	PRIMARY KEY(id) */ 
 /* ); */

/* CREATE TABLE customers ( */
	/* id INTEGER, */
	/* full_name TEXT NOT NULL, */
	/* email TEXT NOT NULL UNIQUE, */
	/* mobile_money_number TEXT NOT NULL UNIQUE, */
	/* password TEXT NOT NULL, */
	/* account_creation_date TEXT NOT NULL, */
	/* PRIMARY KEY(id) */
/* ); */

 CREATE TABLE products (
 	id INTEGER,
	store_id INTEGER NOT NULL,
 	name TEXT NOT NULL,
 	price REAL NOT NULL,
 	quantity INTEGER NOT NULL,
 	description TEXT NOT NULL,
 	creation_date TEXT NOT NULL,
	picture BLOB NOT NULL,
 	PRIMARY KEY(id),
	FOREIGN KEY(store_id) REFERENCES stores(id)
 );

 /* CREATE TABLE product_pictures ( */
 /* 	id INTEGER, */
 /* 	product_id INTEGER NOT NULL, */
 /* 	picture BLOB NOT NULL, */
 /* 	PRIMARY KEY(id), */
 /* 	FOREIGN KEY(product_id) REFERENCES products(id) */
 /* ); */

.schema
