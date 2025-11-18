from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devkey')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:22994433@localhost/saep_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100))
    category = db.Column(db.String(50))
    specs = db.Column(db.JSON)  # JSON
    quantity = db.Column(db.Integer, default=0, nullable=False)
    min_quantity = db.Column(db.Integer, default=1, nullable=False)
    price = db.Column(db.Numeric(12,2))
    warranty_months = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Movement(db.Model):
    __tablename__ = 'movements'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    responsible = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product', backref=db.backref('movements', lazy=True))

# Autenticação.
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    low_stock = Product.query.filter(Product.quantity < Product.min_quantity).all()
    return render_template('dashboard.html', username=session.get('username'), low_stock=low_stock)

# CRUD Produtos
@app.route('/products')
def products():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    q = request.args.get('q','')
    if q:
        products = Product.query.filter(Product.name.ilike(f'%{q}%')).order_by(Product.name.asc()).all()
    else:
        products = Product.query.order_by(Product.name.asc()).all()
    return render_template('products.html', products=products, q=q)

@app.route('/product/new', methods=['GET','POST'])
def product_new():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        code = request.form['code'].strip()
        name = request.form['name'].strip()
        description = request.form.get('description','').strip()
        try:
            quantity = int(request.form.get('quantity',0))
            min_quantity = int(request.form.get('min_quantity',1))
        except ValueError:
            flash('Quantidade inválida.', 'danger')
            return redirect(url_for('product_new'))
        if not code or not name:
            flash('Código e nome são obrigatórios.', 'danger')
            return redirect(url_for('product_new'))
        if Product.query.filter_by(code=code).first():
            flash('Código já existe.', 'danger')
            return redirect(url_for('product_new'))
        p = Product(code=code, name=name, description=description, quantity=quantity, min_quantity=min_quantity)
        db.session.add(p)
        db.session.commit()
        flash('Produto criado.', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', product=None)

@app.route('/product/<int:id>/edit', methods=['GET','POST'])
def product_edit(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    p = Product.query.get_or_404(id)
    if request.method == 'POST':
        p.code = request.form['code'].strip()
        p.name = request.form['name'].strip()
        p.description = request.form.get('description','').strip()
        try:
            p.quantity = int(request.form.get('quantity',0))
            p.min_quantity = int(request.form.get('min_quantity',1))
        except ValueError:
            flash('Quantidade inválida.', 'danger')
            return redirect(url_for('product_edit', id=id))
        db.session.commit()
        flash('Produto atualizado.', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', product=p)

@app.route('/product/<int:id>/delete', methods=['POST'])
def product_delete(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    p = Product.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Produto excluído.', 'success')
    return redirect(url_for('products'))

# Movimentações (entrada / saída)
@app.route('/movements', methods=['GET','POST'])
def movements():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        type_op = request.form['type']
        amount = int(request.form['amount'])
        responsible = request.form['responsible'] or session.get('username','unknown')
        p = Product.query.get_or_404(product_id)
        if type_op == 'out' and amount > p.quantity:
            flash('Quantidade insuficiente para saída.', 'danger')
            return redirect(url_for('movements'))
        if type_op == 'in':
            p.quantity += amount
        else:
            p.quantity -= amount
        m = Movement(product_id=product_id, type=type_op, amount=amount, responsible=responsible)
        db.session.add(m)
        db.session.commit()
        flash('Movimentação registrada.', 'success')
        return redirect(url_for('movements'))
    products = Product.query.order_by(Product.name.asc()).all()
    movements = Movement.query.order_by(Movement.timestamp.desc()).limit(50).all()
    return render_template('movements.html', products=products, movements=movements)

if __name__ == '__main__':
    app.run(debug=True)
