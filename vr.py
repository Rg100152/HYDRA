from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
app.secret_key = 'hydra_secret_cyber_key'

# --- PRODUCT DATABASE ---
PRODUCTS = [
    {
        "id": 1,
        "name": "HYDRA VISION X",
        "category": "headset",
        "price": 799,
        "rating": "4.9",
        "badge": "BESTSELLER",
        "image": "https://yourimageshare.com/ib/6DMO0nt2dH.jpg",
        "desc": "Dual 4K Micro-OLED displays with 120Hz refresh rate and ultra-low latency."
    },
    {
        "id": 2,
        "name": "HYDRA ELITE PRO",
        "category": "headset",
        "price": 999,
        "rating": "5.0",
        "badge": "FLAGSHIP",
        "image": "https://yourimageshare.com/ib/SzE0smgrnW.jpg",
        "desc": "Wireless standalone headset featuring 8-hour battery and neural eye-tracking."
    },
    {
        "id": 3,
        "name": "HYDRA LITE VR",
        "category": "headset",
        "price": 499,
        "rating": "4.7",
        "badge": "NEW",
        "image": "https://yourimageshare.com/ib/Znd0NF7wzH.jpg",
        "desc": "Featherlight design optimized for extended casual gaming sessions."
    },
    {
        "id": 4,
        "name": "HYDRA AUDIO PODS",
        "category": "audio",
        "price": 199,
        "rating": "4.8",
        "badge": "HOT",
        "image": "https://yourimageshare.com/ib/kZpMQZPxzk.jpg",
        "desc": "True spatial audio subwoofers with zero-latency bone conduction."
    },
    {
        "id": 5,
        "name": "HYDRA HAPTIC SUIT",
        "category": "accessory",
        "price": 349,
        "rating": "4.9",
        "badge": "POPULAR",
        "image": "https://yourimageshare.com/ib/ee6zX3XrZn.jpg",
        "desc": "Full-body tactile feedback vest with 40 programmable vibration points."
    },
    {
        "id": 6,
        "name": "HYDRA NEXUS LINK",
        "category": "accessory",
        "price": 129,
        "rating": "4.6",
        "badge": "PRO GEAR",
        "image": "https://yourimageshare.com/ib/WH8Asyhj5k.jpg",
        "desc": "High-speed 10Gbps fiber optic PC streaming cable for seamless graphics."
    }
]

# Simulated In-Memory Cart Storage
cart_items = []

# --- HTML TEMPLATE (Embedded Directly in Python) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HYDRA - Virtual Reality Store</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #07080c;
            --surface: #0e111a;
            --primary: #ff3b00;
            --cyan: #00f0ff;
            --glass: rgba(18, 22, 34, 0.75);
            --border: rgba(255, 255, 255, 0.1);
            --text: #f0f2f8;
            --text-dim: #9098b0;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }

        body {
            background-color: var(--bg-dark);
            color: var(--text);
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 15%, rgba(255, 59, 0, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 90% 70%, rgba(0, 240, 255, 0.1) 0%, transparent 45%);
            background-attachment: fixed;
        }

        h1, h2, h3, .logo, .btn-neon { font-family: 'Orbitron', sans-serif; }

        /* NAVBAR */
        nav {
            display: flex; justify-content: space-between; align-items: center;
            padding: 20px 8%; position: fixed; top: 0; width: 100%; z-index: 1000;
            background: rgba(7, 8, 12, 0.9); backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border);
        }

        .logo { font-size: 22px; font-weight: 900; letter-spacing: 2px; color: #fff; cursor: pointer; }
        .logo span { color: var(--primary); text-shadow: 0 0 15px var(--primary); }

        .nav-links { display: flex; gap: 30px; list-style: none; }
        .nav-links a { color: var(--text-dim); text-decoration: none; font-size: 13px; font-weight: 600; transition: 0.3s; }
        .nav-links a:hover { color: var(--cyan); text-shadow: 0 0 10px var(--cyan); }

        .nav-actions { display: flex; gap: 15px; align-items: center; }
        
        .cart-btn {
            background: var(--surface); border: 1px solid var(--border); padding: 10px 18px;
            border-radius: 30px; color: #fff; cursor: pointer; display: flex; align-items: center; gap: 8px;
            font-weight: 600; transition: 0.3s;
        }
        .cart-btn:hover { border-color: var(--primary); box-shadow: 0 0 15px rgba(255,59,0,0.4); }
        .cart-badge { background: var(--primary); color: #fff; padding: 2px 8px; border-radius: 50px; font-size: 11px; }

        /* HERO SECTION */
        .hero {
            display: flex; align-items: center; justify-content: space-between;
            padding: 160px 8% 80px; min-height: 100vh; position: relative;
        }
        .hero-content { width: 52%; }
        .hero-content h1 { font-size: 3.5rem; line-height: 1.1; margin-bottom: 20px; font-weight: 900; }
        .hero-content h1 span { color: var(--primary); text-shadow: 0 0 30px rgba(255,59,0,0.5); }
        .hero-content p { color: var(--text-dim); font-size: 1rem; margin-bottom: 30px; line-height: 1.6; }

        .btn-neon {
            background: var(--primary); color: #fff; border: none; padding: 14px 32px;
            border-radius: 30px; font-weight: 700; cursor: pointer; letter-spacing: 1px;
            box-shadow: 0 0 20px rgba(255,59,0,0.5); transition: 0.3s; text-decoration: none; display: inline-block;
        }
        .btn-neon:hover { background: #ff5722; box-shadow: 0 0 30px rgba(255,59,0,0.8); transform: translateY(-3px); }

        .hero-img { width: 42%; position: relative; }
        .hero-img img { width: 100%; border-radius: 20px; border: 1px solid var(--border); box-shadow: 0 20px 50px rgba(0,0,0,0.8); }

        /* PRODUCTS SECTION */
        .products { padding: 80px 8%; }
        .section-header { text-align: center; margin-bottom: 50px; }
        .section-header h2 { font-size: 2.5rem; margin-bottom: 10px; }
        .section-header h2 span { color: var(--cyan); }

        .filter-tabs { display: flex; justify-content: center; gap: 15px; margin-bottom: 40px; }
        .tab-btn {
            background: var(--surface); border: 1px solid var(--border); color: var(--text-dim);
            padding: 8px 20px; border-radius: 20px; cursor: pointer; font-weight: 600; transition: 0.3s;
        }
        .tab-btn.active, .tab-btn:hover { background: var(--cyan); color: #000; border-color: var(--cyan); box-shadow: 0 0 15px rgba(0,240,255,0.4); }

        .product-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; }

        .product-card {
            background: var(--glass); border: 1px solid var(--border); border-radius: 20px;
            padding: 20px; backdrop-filter: blur(10px); transition: 0.4s; display: flex; flex-direction: column; justify-content: space-between;
        }
        .product-card:hover { transform: translateY(-8px); border-color: var(--primary); box-shadow: 0 15px 35px rgba(255,59,0,0.2); }

        .card-img { width: 100%; height: 220px; border-radius: 14px; overflow: hidden; margin-bottom: 15px; position: relative; }
        .card-img img { width: 100%; height: 100%; object-fit: cover; transition: 0.5s; }
        .product-card:hover .card-img img { transform: scale(1.08); }
        
        .badge { position: absolute; top: 12px; left: 12px; background: rgba(0,0,0,0.7); backdrop-filter: blur(5px); color: var(--cyan); border: 1px solid var(--cyan); padding: 4px 10px; border-radius: 20px; font-size: 10px; font-weight: 700; }

        .card-info h3 { font-size: 1.2rem; margin-bottom: 8px; }
        .card-info p { color: var(--text-dim); font-size: 0.85rem; margin-bottom: 15px; }
        
        .card-footer { display: flex; justify-content: space-between; align-items: center; margin-top: auto; }
        .price { font-size: 1.3rem; font-weight: 700; color: #fff; font-family: 'Orbitron', sans-serif; }
        
        .btn-add {
            background: transparent; border: 1px solid var(--cyan); color: var(--cyan);
            padding: 8px 18px; border-radius: 20px; cursor: pointer; font-weight: 600; transition: 0.3s;
        }
        .btn-add:hover { background: var(--cyan); color: #000; box-shadow: 0 0 15px var(--cyan); }

        /* CART DRAWER */
        .cart-drawer {
            position: fixed; top: 0; right: -400px; width: 380px; height: 100%;
            background: #0b0e14; border-left: 1px solid var(--border); z-index: 2000;
            box-shadow: -10px 0 30px rgba(0,0,0,0.8); transition: 0.4s ease; display: flex; flex-direction: column; padding: 25px;
        }
        .cart-drawer.open { right: 0; }
        .cart-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 15px; margin-bottom: 20px; }
        .close-cart { background: none; border: none; color: #fff; font-size: 20px; cursor: pointer; }
        
        .cart-items { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; }
        .cart-item { display: flex; gap: 12px; background: var(--surface); padding: 10px; border-radius: 12px; border: 1px solid var(--border); align-items: center; }
        .cart-item img { width: 50px; height: 50px; border-radius: 8px; object-fit: cover; }
        .cart-item-details { flex: 1; }
        .cart-item-details h4 { font-size: 13px; }
        .cart-item-details p { font-size: 12px; color: var(--text-dim); }

        .cart-footer-panel { border-top: 1px solid var(--border); padding-top: 20px; margin-top: auto; }
        .total-row { display: flex; justify-content: space-between; font-size: 1.1rem; font-weight: 700; margin-bottom: 15px; }

        /* TOAST */
        #toast {
            position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(100px);
            background: var(--cyan); color: #000; padding: 12px 25px; border-radius: 30px;
            font-weight: 700; z-index: 3000; box-shadow: 0 0 20px var(--cyan); transition: 0.4s; opacity: 0;
        }
        #toast.show { transform: translateX(-50%) translateY(0); opacity: 1; }
    </style>
</head>
<body>

    <!-- NAVBAR -->
    <nav>
        <div class="logo">HYDRA<span>.VR</span></div>
        <ul class="nav-links">
            <li><a href="#home">HOME</a></li>
            <li><a href="#products">PRODUCTS</a></li>
            <li><a href="#">TECHNOLOGY</a></li>
            <li><a href="#">CONTACT</a></li>
        </ul>
        <div class="nav-actions">
            <button class="cart-btn" onclick="toggleCart()">
                🛒 Cart <span class="cart-badge" id="cartCount">0</span>
            </button>
        </div>
    </nav>

    <!-- HERO SECTION -->
    <section class="hero" id="home">
        <div class="hero-content">
            <h1>Dive Into The Future of <span>Virtual Reality</span></h1>
            <p>Experience uncompromised clarity with our next-generation 4K OLED headsets, zero latency haptics, and boundless immersive worlds.</p>
            <a href="#products" class="btn-neon">Explore Collection →</a>
        </div>
        <div class="hero-img">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFzrk-_1ess7wXjjAUMRqzWMpTcr4ffCWGueV6XyhHjA&s=10" alt="VR Hero">
        </div>
    </section>

    <!-- PRODUCTS SECTION -->
    <section class="products" id="products">
        <div class="section-header">
            <h2>Elite Hardware <span>Collection</span></h2>
            <p style="color: var(--text-dim);">Engineered for maximum immersion and cinematic fidelity.</p>
        </div>

        <div class="filter-tabs">
            <button class="tab-btn active" onclick="filterProducts('all')">All Gear</button>
            <button class="tab-btn" onclick="filterProducts('headset')">Headsets</button>
            <button class="tab-btn" onclick="filterProducts('audio')">Spatial Audio</button>
            <button class="tab-btn" onclick="filterProducts('accessory')">Accessories</button>
        </div>

        <div class="product-grid" id="productGrid">
            {% for p in products %}
            <div class="product-card" data-category="{{ p.category }}">
                <div class="card-img">
                    <span class="badge">{{ p.badge }}</span>
                    <img src="{{ p.image }}" alt="{{ p.name }}">
                </div>
                <div class="card-info">
                    <h3>{{ p.name }}</h3>
                    <p>{{ p.desc }}</p>
                </div>
                <div class="card-footer">
                    <span class="price">${{ p.price }}</span>
                    <button class="btn-add" onclick="addToCart({{ p.id }})">Add to Cart</button>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>

    <!-- SLIDE-OUT CART DRAWER -->
    <div class="cart-drawer" id="cartDrawer">
        <div class="cart-header">
            <h3>Your Cyber Cart</h3>
            <button class="close-cart" onclick="toggleCart()">✕</button>
        </div>
        <div class="cart-items" id="cartItemsContainer">
            <p style="color: var(--text-dim); text-align: center; margin-top: 50px;">Your cart is empty</p>
        </div>
        <div class="cart-footer-panel">
            <div class="total-row">
                <span>Grand Total:</span>
                <span id="cartGrandTotal" style="color: var(--cyan);">$0</span>
            </div>
            <button class="btn-neon" style="width: 100%; text-align: center;" onclick="checkoutOrder()">Checkout Now</button>
        </div>
    </div>

    <!-- TOAST NOTIFICATION -->
    <div id="toast">Notification message</div>

    <!-- JAVASCRIPT -->
    <script>
        function toggleCart() {
            document.getElementById('cartDrawer').classList.toggle('open');
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.innerText = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 3000);
        }

        function filterProducts(category) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            fetch(`/api/products?category=${category}`)
                .then(res => res.json())
                .then(data => {
                    if(data.success) {
                        let grid = document.getElementById('productGrid');
                        grid.innerHTML = '';
                        data.products.forEach(p => {
                            grid.innerHTML += `
                            <div class="product-card" data-category="${p.category}">
                                <div class="card-img">
                                    <span class="badge">${p.badge}</span>
                                    <img src="${p.image}" alt="${p.name}">
                                </div>
                                <div class="card-info">
                                    <h3>${p.name}</h3>
                                    <p>${p.desc}</p>
                                </div>
                                <div class="card-footer">
                                    <span class="price">$${p.price}</span>
                                    <button class="btn-add" onclick="addToCart(${p.id})">Add to Cart</button>
                                </div>
                            </div>`;
                        });
                    }
                });
        }

        function addToCart(productId) {
            fetch('/api/cart/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ product_id: productId })
            })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    showToast(data.message);
                    document.getElementById('cartCount').innerText = data.total_items;
                    document.getElementById('cartGrandTotal').innerText = '$' + data.grand_total;
                    
                    let container = document.getElementById('cartItemsContainer');
                    container.innerHTML = '';
                    data.cart.forEach(item => {
                        container.innerHTML += `
                        <div class="cart-item">
                            <img src="${item.image}" alt="${item.name}">
                            <div class="cart-item-details">
                                <h4>${item.name}</h4>
                                <p>$${item.price} x ${item.qty}</p>
                            </div>
                        </div>`;
                    });
                }
            });
        }

        function checkoutOrder() {
            fetch('/api/cart/checkout', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                if(data.success) {
                    showToast(data.message);
                    document.getElementById('cartCount').innerText = '0';
                    document.getElementById('cartGrandTotal').innerText = '$0';
                    document.getElementById('cartItemsContainer').innerHTML = '<p style="color: var(--text-dim); text-align: center; margin-top: 50px;">Your cart is empty</p>';
                    toggleCart();
                } else {
                    showToast(data.message);
                }
            });
        }
    </script>
</body>
</html>
"""

# --- FLASK ROUTES ---
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, products=PRODUCTS)

@app.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category', 'all')
    if category != 'all':
        filtered = [p for p in PRODUCTS if p['category'] == category]
        return jsonify({"success": True, "products": filtered})
    return jsonify({"success": True, "products": PRODUCTS})

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    product_id = data.get('product_id')
    
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        existing = next((item for item in cart_items if item['id'] == product_id), None)
        if existing:
            existing['qty'] += 1
        else:
            cart_items.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "image": product["image"],
                "qty": 1
            })
        
        total_items = sum(item['qty'] for item in cart_items)
        grand_total = sum(item['price'] * item['qty'] for item in cart_items)
        
        return jsonify({
            "success": True, 
            "message": f"Added {product['name']} to Cart!",
            "cart": cart_items,
            "total_items": total_items,
            "grand_total": grand_total
        })
    return jsonify({"success": False, "message": "Product not found"}), 404

@app.route('/api/cart/checkout', methods=['POST'])
def checkout():
    global cart_items
    if not cart_items:
        return jsonify({"success": False, "message": "Cart is empty!"}), 400
    
    total = sum(item['price'] * item['qty'] for item in cart_items)
    cart_items = []
    return jsonify({
        "success": True, 
        "message": f"Order Placed Successfully! Total Paid: ${total}",
        "cart": [],
        "total_items": 0,
        "grand_total": 0
    })

if __name__ == '__main__':
    print("🚀 Starting HYDRA VR Store Server at http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
