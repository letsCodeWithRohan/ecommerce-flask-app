from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

app.secret_key = "Harshal"

app.config["UPLOAD_FOLDER"] = 'static/img/products/'

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "ecommerce"

mysql = MySQL(app)

@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id,name,brand,price,category,image,description FROM products ORDER BY created_at LIMIT 8 OFFSET 0;")
    topdata = cursor.fetchall()
    cursor.execute("SELECT id,name,brand,price,category,image,description FROM products ORDER BY created_at LIMIT 8 OFFSET 8;")
    bottomdata = cursor.fetchall()
    cursor.close()
    return render_template("index.html",topdata=topdata,bottomdata=bottomdata)

@app.route("/shop")
def shop():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id,name,brand,price,category,image,description FROM products ORDER BY created_at DESC")
    data = cursor.fetchall()
    cursor.close()
    return render_template("shop.html",data=data)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/cart")
def cart():
    if "email" in session :
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT c.id,c.user_id,c.product_id,p.name,p.price,c.quantity,c.price,p.image,c.size FROM cart c JOIN products p ON c.product_id = p.id WHERE c.user_id = %s",(session["id"],))
        data = cursor.fetchall()
        cursor.execute("SELECT SUM(price),(50 * COUNT(price)),(SUM(price) + (50 * COUNT(price))) FROM cart WHERE user_id = %s",(session["id"],))
        shipping = cursor.fetchone()
        cursor.close()
        return render_template("cart.html",data=data,shipdata=shipping)
    else:
        flash("Please Login first")
        return redirect(url_for("login"))

@app.route("/sproduct/<int:id>/",methods=["GET","POST"])
def sproduct(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id,name,brand,price,category,image,description FROM products WHERE id = %s",(id,))
        data = cursor.fetchone()
        cursor.execute("SELECT id,name,brand,price,category,image,description FROM products WHERE id != %s ORDER BY created_at DESC",(id,))
        more = cursor.fetchall()
        cursor.close()
        product = dict()
        product["id"] = data[0]
        product["name"] = data[1]
        product["brand"] = data[2]
        product["price"] = data[3]
        product["category"] = data[4]
        product["image"] = data[5]
        product["description"] = data[6]
        return render_template("sproduct.html",data=product,more=more)
    else:
        if "email" in session :
            data = request.form
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO cart(user_id, product_id, quantity, price,size) VALUES (%s,%s,%s,%s,%s)",(session["id"],data["id"],data["quantity"],(float(data["price"]) * int(data["quantity"])),data["size"]))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("cart"))
        else:
            flash("Login to buy product")
            return redirect(url_for("login"))

@app.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "GET" :
        return render_template("login.html")
    else :
        data = request.form
        cursor = mysql.connection.cursor()
        cursor.execute("select email,password,id from accounts WHERE email = %s",(data["email"],))
        record = cursor.fetchone()
        cursor.close()
        if record :
            if data["email"] == record[0] and data["password"] == record[1] :
                session["id"] = record[2]
                session["email"] = data["email"]
                session["password"] = data["password"]
                return redirect(url_for("index"))
            elif data["email"] == record[0] and data["password"] != record[1]:
                flash("Password Wrong")
                return redirect(url_for("login"))
            else:
                flash("Unknown error")
                return redirect(url_for("login"))
        elif data["email"]=="admin@gmail.com" and data["password"]=="admin@123":
                session["admin"] = data["email"]
                return redirect(url_for("admin_home"))
        else:
            flash("Account not found")
            return redirect(url_for("login"))
        
@app.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "GET" :
        return render_template("register.html")
    else:
        data = request.form
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO accounts (email, password, fullname, phone, address, city, state, postal_code, country) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(data["email"],data["password"],data["name"],data["phone"],data["address"],data["city"],data["state"],data["zip"],data["country"]))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("login"))

@app.route("/admin_home",methods=["GET","POST"])
def admin_home():
    if "admin" not in session:
        flash("Login as admin")
        return redirect(url_for("login"))
    else:
        if request.method == "GET":
            return render_template("admin_home.html")
        else:
            data = request.form
            photo = request.files["photo"]
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"],photo.filename))
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO products(name, brand, price, category, image, description) VALUES (%s,%s,%s,%s,%s,%s)",(data["name"],data["brand"],data["price"],data["category"],photo.filename,data["desc"]))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("admin_items"))
    
@app.route("/admin_items")
def admin_items():
    if "admin" not in session:
        flash("Login as admin")
        return redirect(url_for("login"))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id,name,brand,price,category,image,description FROM products ORDER BY created_at DESC")
        response = cursor.fetchall()
        cursor.close()
        return render_template("admin_items.html",data=response)

@app.route("/admin_orders")
def admin_orders():
    if "admin" not in session:
        flash("Login as admin")
        return redirect(url_for("login"))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT order_id,product_name,total_amount,quantity,user_name,address,status,(SELECT image FROM products WHERE id = product_id),size FROM orders ORDER BY order_date DESC")
        data = cursor.fetchall()
        cursor.close()
        return render_template("admin_orders.html",data=data)

@app.route("/logout")
def logout():
    session.pop("id",None)
    session.pop("email",None)
    session.pop("password",None)
    return redirect(url_for("index"))

@app.route("/logout_admin")
def logout_admin():
    session.pop("admin",None)
    return redirect(url_for("login"))

@app.route("/remove/<int:id>")
def remove(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM cart WHERE id = %s",(id,))
    mysql.connection.commit()
    return redirect(url_for("cart"))

@app.route("/placeOrder")
def placeorder():
    cursor = mysql.connection.cursor()
    userdetailsquery = "SELECT (SELECT name FROM products WHERE id = cart.product_id),cart.quantity,cart.price,a.id AS user_id,a.fullname,a.address,a.city,a.state,a.postal_code,a.country,cart.id,cart.size,cart.product_id FROM cart JOIN accounts a ON cart.user_id = a.id WHERE a.id = %s;"
    cursor.execute(userdetailsquery,(session["id"],))
    data = cursor.fetchall()
    for userdata in data :
        insertquery = "INSERT INTO orders (user_id, total_amount, quantity, address, city, state, zip_code, country, product_name,user_name,size,product_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        query = '''pname = i[0],quantity = i[1],price = i[2],uid = i[3],fullname = i[4],address = i[5],city = i[6],state = i[7],postal_code = i[8],country = i[9],uname = i[10],cartid'''
        cursor.execute(insertquery,(userdata[3],(userdata[2] + 50),userdata[1],userdata[5],userdata[6],userdata[7],userdata[8],userdata[9],userdata[0],userdata[4],userdata[11],userdata[12]))
        cursor.execute("DELETE FROM cart WHERE id = %s ",(userdata[10],))
        mysql.connection.commit()
    cursor.close()
    return redirect(url_for("track_order"))

@app.route("/track_order")
def track_order():
    if "email" not in session:
        flash("Login to buy product")
        return redirect(url_for("login"))
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT (SELECT image FROM products WHERE id = product_id),(SELECT name FROM products WHERE id = product_id),size,quantity,total_amount,order_date,status FROM orders WHERE user_id = %s",(session["id"],))
        data = cursor.fetchall()
        return render_template("track_order.html",data=data)

@app.route("/order_update/<int:id>",methods=["GET","POST"])
def order_update(id):
    if request.method == "POST":
        data = request.form["status"]
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE orders SET status = %s WHERE order_id = %s",(data,id))
        mysql.connection.commit()
        return redirect(url_for("admin_orders"))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')