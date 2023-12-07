


#import sqlite and Flask, NOTE THAT THIS CODE ONLY RUNS FROM TERMINAL INPUTS

import sqlite3
from flask import Flask, render_template, request, redirect, url_for


#initialize Flask app
app = Flask(__name__, template_folder='templates')


#function to create the products database
def init_db():
    with sqlite3.connect('products.db') as con:
        
        
        #create 'products' table
        con.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT,
                        description TEXT,
                        price REAL,
                        code TEXT)''')
        con.commit()


#call function to init the database
init_db()


#route to home page first
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')  #rendering template


#tunnel enter product
@app.route('/enter_product', methods=['GET', 'POST'])
def enter_product():
    if request.method == 'POST':
        
        
        #post request retrieve
        category = request.form['category']
        description = request.form['description']
        price = request.form['price']
        code = request.form['code']
        
        
        #init into SQlite3 database
        with sqlite3.connect('products.db') as con:
            cur = con.cursor()
            
            
            #insert into product table
            cur.execute('''INSERT INTO products (category, description, price, code) VALUES (?, ?, ?, ?)''', (category, description, price, code))
            
            
            #commit to database
            con.commit()  
            
            
            #insert data ---> redirect
        return redirect('/')  
    
    
    #render form
    return render_template('enter_product.html')  



#tunnel to product details
@app.route('/retrieve_product', methods=['GET', 'POST'])
def retrieve_product():
    if request.method == 'POST':
        category = request.form.get('category')
        with sqlite3.connect('products.db') as con:
            cur = con.cursor()
            if category:
                
                
                #retrieve based on user imputed category
                cur.execute('''SELECT * FROM products WHERE category = ?''', (category,))
            else:
                
                
                #all products if none are specified
                cur.execute('''SELECT * FROM products''')
                #fetch products retrieved from the database
            products = cur.fetchall()  
            # Render the product details page
        return render_template('product_details.html', products=products)  
    #render form for product details
    return render_template('retrieve_product.html')  


#run app
if __name__ == '__main__':
    #debug mode
    app.run(debug=True)  