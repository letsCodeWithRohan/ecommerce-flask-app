<h1>ecommerce application in flask</h1>

<h3>Created By Chaudhari Rohan</h3>

<h4>Steps to download and run this project</h4>

<ol start="1">
<li>Download and Extract This Repository</li>
<li>Open command prompt in that folder</li>
<li><p>Install virtualenv if you don't have it</p>  
    
```bash
pip install virtualenv
```

</li>
<li><p>create virtual environment for this project by using</p>

```bash
python -m venv .venv
```
<p align="center">OR</p>

```bash
virtualenv .venv
```
</li>
<li>
<p>Activate virtual environment</p>

```bash
.venv\Scripts\activate
```
</li>
<li>
<p>Install required dependencies</p>
    
```bash
pip install flask flask_mysqldb
```
</li>
<li>
<p>Setup Database</p>
<ul>
<li>Open XAMPP CONTROL PANEL.</li>
<li>Start <mark>Apache</mark> and <mark>MySQL</mark></li>
<li>Open <kbd>Admin</kbd> of MySQL</li>
<li>Create New Database as your wish Ex : "to_do_list"</li>
<li>Click on it then open <kbd>SQL</kbd> Tab </li>
<li>
<p>Paster The below Query to create table</p>

<p><kbd>accounts</kbd> table</p> 

```SQL
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    fullname VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(50),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
<p><kbd>products</kbd> table</p> 

```SQL
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100),
    image VARCHAR(255),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
<p><kbd>cart</kbd> table</p> 

```SQL
CREATE TABLE cart (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    size VARCHAR(10) DEFAULT 'M',
    FOREIGN KEY (user_id) REFERENCES accounts(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```
<p><kbd>orders</kbd> table</p> 


```SQL
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending','Delivered','Out for delivery') DEFAULT 'Pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    address VARCHAR(255),
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    country VARCHAR(50),
    product_name VARCHAR(255),
    user_name VARCHAR(100) NOT NULL,
    size VARCHAR(10) NOT NULL DEFAULT 'M',
    product_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES accounts(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

<p>insert query for <kbd>products</kbd> table</p> 

```SQL

INSERT INTO `products` (`id`, `name`, `brand`, `price`, `category`, `image`, `description`, `created_at`) VALUES
(2, 'Polo T-shirt', 'POLO', 250.00, 'T-Shirt', 'n4.jpg', 'T-shirt with nice design', '2024-08-13 14:34:36'),
(3, 'Abstract Print Shirt', 'Zara', 300.00, 'Shirt', 'f1.jpg', 'Abstract Print Shirt of brand zara', '2024-08-15 05:12:33'),
(4, 'Printed Streachy Shirt', 'Zara', 350.00, 'Shirt', 'f2.jpg', 'Printed Streachy Shirt of brand zara', '2024-08-15 05:24:20'),
(5, 'Floral Print Shirt', 'POLO', 350.00, 'Shirt', 'f3.jpg', 'Shirt with lot of flowers design atracts girls', '2024-08-15 05:26:24'),
(6, 'White Flowers Shirt', 'Zara', 200.00, 'Shirt', 'f4.jpg', 'Shirt specially for Chhapri', '2024-08-15 05:27:32'),
(7, 'Blue and pinks shirt', 'Zara', 240.00, 'Shirt', 'f5.jpg', 'Pink and blue shirt with awesome design', '2024-08-15 17:01:12'),
(8, 'FINE CORDUROY SHIRT', 'POLO', 290.00, 'Shirt', 'f6.jpg', 'FINE CORDUROY SHIRT with epic design', '2024-08-15 17:02:07'),
(9, 'Wide linen-blend trousers', 'H&M', 150.00, 'Bottom', 'f7.jpg', 'Wide linen-blend trousers', '2024-08-15 17:03:00'),
(10, 'Women summer top', 'H&M', 200.00, 'Top', 'f8.jpg', 'summer edition for womens', '2024-08-15 17:04:01'),
(11, 'Regular fit shirt', 'Zara', 130.00, 'Shirt', 'n1.jpg', 'Shirt with plain sky blue color', '2024-08-15 17:05:44'),
(12, 'Regular Fit Cotton shirt', 'H&M', 220.00, 'Shirt', 'n2.jpg', 'Regular Fit Cotton shirt', '2024-08-15 17:06:56'),
(13, 'Regular Fit Cotton shirt', 'Zara', 180.00, 'Shirt', 'n3.jpg', 'Regular Fit Cotton shirt', '2024-08-15 17:07:31'),
(14, 'JEANS SHIRT', 'H&M', 180.00, 'Shirt', 'n5.jpg', 'JEANS SHIRT', '2024-08-15 17:08:18'),
(15, 'Regular Fit Linen-blend overshirt', 'POLO', 200.00, 'Shirt', 'n7.jpg', 'Regular Fit Linen-blend overshirt', '2024-08-15 17:08:50'),
(16, 'Regular Fit Resort Shirt', 'H&M', 189.00, 'Shirt', 'n8.jpg', 'Regular Fit Resort Shirt', '2024-08-15 17:09:20'),
(17, 'Gray Formal Pant', 'H&M', 200.00, 'Pant', 'n6.jpg', 'Grey Formal Pant', '2024-08-15 17:10:12');
```

</li>
<li>Run The Query by clicking <kbd>Go</kbd></li>
</ul>
</li>
<li>
<p>Run the Project</p>

```bash
python app.py
```
</li>

</ol># ecommerce-flask-app
