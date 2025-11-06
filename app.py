from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, User, Book, Cart, CartItem, Order, OrderItem
from forms import RegisterForm, LoginForm, ChangePasswordForm, BookForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from urllib.parse import urlparse, urljoin
from sqlalchemy.exc import SQLAlchemyError
import os
import logging
from functools import wraps
 
# --- Configuración inicial ---
load_dotenv()
logging.basicConfig(level=logging.INFO)
 
app = Flask(__name__)
app.config.from_object(Config)
 
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
 
# Crear tablas si no existen
with app.app_context():
    db.create_all()
 
# --- Función de seguridad para evitar redirecciones abiertas ---
def is_safe_url(target):
    """Verifica que la URL sea interna a la aplicación."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (
        test_url.scheme in ('http', 'https') and
        ref_url.netloc == test_url.netloc
    )
 
# --- Manejo de Login ---
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # versión actualizada SQLAlchemy 2.x
 
# --- Decorador para admin ---
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Primero inicia sesión.', 'warning')
            return redirect(url_for('login'))
        if not getattr(current_user, 'is_admin', False) and getattr(current_user, 'role', 'user') != 'admin':
            flash('Acceso denegado. Solo administradores.', 'danger')
            return redirect(url_for('index'))
        return fn(*args, **kwargs)
    return wrapper
 
# --- Rutas principales ---
@app.route('/')
def index():
    return render_template('profile.html', user=current_user)
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
   
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        if User.query.count() == 0:
            user.role = 'admin'  # Primer usuario será admin (opcional)
        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
   
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Has ingresado correctamente.', 'success')
           
            # 🚫 Eliminamos redirección basada en datos del usuario
            # En lugar de usar request.args.get('next'), siempre mandamos a una ruta segura
            return redirect(url_for('index'))
       
        flash('Correo o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)
 
 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('login'))
 
@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Contraseña actual incorrecta.', 'danger')
            return render_template('change_password.html', form=form)
       
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Contraseña actualizada correctamente.', 'success')
        return redirect(url_for('index'))
    return render_template('change_password.html', form=form)
 
# --- Panel de administrador ---
@app.route('/admin')
@login_required
@admin_required
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)
 
# --- CRUD de libros (ADMIN) ---
@app.route('/admin/books')
@login_required
@admin_required
def admin_books():
    books = Book.query.order_by(Book.id.desc()).all()
    return render_template('admin_books.html', books=books)
 
@app.route('/admin/books/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_book():
    form = BookForm()
    if form.validate_on_submit():
        filename = None
        if form.cover.data:
            try:
                f = form.cover.data
                filename = secure_filename(f.filename)
                upload_folder = os.path.join('static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                f.save(os.path.join(upload_folder, filename))
            except (OSError) as e:
                app.logger.error(f"Error al guardar la imagen: {e}")
                flash("Error al guardar la imagen.", "danger")
 
        book = Book(
            title=form.title.data,
            author=form.author.data,
            price=form.price.data,
            stock=form.stock.data,
            description=form.description.data,
            cover_filename=filename
        )
        db.session.add(book)
        db.session.commit()
        flash('Libro creado correctamente.', 'success')
        return redirect(url_for('admin_books'))
    return render_template('edit_book.html', form=form, action='Crear')
 
@app.route('/admin/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        if form.cover.data:
            try:
                f = form.cover.data
                filename = secure_filename(f.filename)
                upload_folder = os.path.join('static', 'uploads')
                os.makedirs(upload_folder, exist_ok=True)
                f.save(os.path.join(upload_folder, filename))
                book.cover_filename = filename
            except (OSError) as e:
                app.logger.error(f"Error al actualizar la imagen: {e}")
                flash("Error al actualizar la imagen.", "danger")
 
        book.title = form.title.data
        book.author = form.author.data
        book.price = form.price.data
        book.stock = form.stock.data
        book.description = form.description.data
        db.session.commit()
        flash('Libro actualizado.', 'success')
        return redirect(url_for('admin_books'))
    return render_template('edit_book.html', form=form, action='Editar', book=book)
 
@app.route('/admin/books/delete/<int:book_id>', methods=['POST'])
@login_required
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.cover_filename:
        path = os.path.join('static', 'uploads', book.cover_filename)
        if os.path.exists(path):
            try:
                os.remove(path)
            except (OSError) as e:
                app.logger.warning(f"No se pudo eliminar la portada: {e}")
    db.session.delete(book)
    db.session.commit()
    flash('Libro eliminado.', 'success')
    return redirect(url_for('admin_books'))
 
# --- CRUD de usuarios (ADMIN) ---
@app.route('/admin/users', methods=['GET'])
@login_required
@admin_required
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)
 
@app.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'user')
 
        new_user = User(username=username, email=email, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('✅ Usuario agregado correctamente.', 'success')
        return redirect(url_for('admin_users'))
    return render_template('add_user.html')
 
@app.route('/admin/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        db.session.commit()
        flash('✅ Usuario actualizado correctamente.', 'success')
        return redirect(url_for('admin_users'))
    return render_template('edit_user.html', user=user)
 
@app.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if current_user.id == user.id:
        flash("❌ No puedes eliminarte a ti mismo.", "danger")
        return redirect(url_for('admin_users'))
 
    db.session.delete(user)
    db.session.commit()
    flash('🗑️ Usuario eliminado correctamente.', 'success')
    return redirect(url_for('admin_users'))
 
# --- Catálogo de usuario ---
@app.route('/catalogo')
@login_required
def catalogo():
    query = request.args.get('q', '')
    if query:
        books = Book.query.filter(
            (Book.title.ilike(f'%{query}%')) |
            (Book.author.ilike(f'%{query}%'))
        ).order_by(Book.id.desc()).all()
    else:
        books = Book.query.order_by(Book.id.desc()).all()
    return render_template('catalogo.html', books=books, query=query)
 
# --------------------------
# RUTAS DE CARRITO Y PEDIDOS
# --------------------------

@app.route('/cart')  # ver carrito
@login_required
def view_cart():
    # crear carrito si no existe
    cart = current_user.cart
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    items = cart.items  # lista de CartItem
    total = sum(item.line_total() for item in items)
    return render_template('cart.html', cart=cart, items=items, total=total)


@app.route('/cart/add/<int:book_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(book_id):
    book = Book.query.get_or_404(book_id)
    qty = int(request.form.get('quantity', 1)) if request.method == 'POST' else int(request.args.get('quantity', 1))

    if qty <= 0:
        flash('Cantidad inválida.', 'warning')
        return redirect(url_for('catalogo'))

    if book.stock < qty:
        flash('No hay suficiente stock disponible.', 'danger')
        return redirect(url_for('catalogo'))

    # obtener o crear carrito
    cart = current_user.cart
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()

    # buscar item existente
    item = CartItem.query.filter_by(cart_id=cart.id, book_id=book.id).first()
    if item:
        # asegurarse que no exceda stock
        if book.stock < item.quantity + qty:
            flash('No hay suficiente stock para aumentar la cantidad.', 'danger')
            return redirect(url_for('catalogo'))
        item.quantity += qty
    else:
        item = CartItem(cart_id=cart.id, book_id=book.id, quantity=qty)
        db.session.add(item)

    db.session.commit()
    flash(f'✅ Añadido {qty} x "{book.title}" al carrito.', 'success')
    return redirect(url_for('catalogo'))


@app.route('/cart/remove/<int:item_id>', methods=['POST', 'GET'])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    # seguridad: solo el dueño del carrito puede eliminar
    if not current_user.cart or item.cart_id != current_user.cart.id:
        flash('Acción no autorizada.', 'danger')
        return redirect(url_for('view_cart'))

    db.session.delete(item)
    db.session.commit()
    flash('Artículo eliminado del carrito.', 'info')
    return redirect(url_for('view_cart'))


@app.route('/checkout', methods=['POST', 'GET'])
@login_required
def checkout():
    cart = current_user.cart
    if not cart or len(cart.items) == 0:
        flash('El carrito está vacío.', 'warning')
        return redirect(url_for('catalogo'))

    # validación de stock antes de crear pedido
    for item in cart.items:
        if item.book.stock < item.quantity:
            flash(f'No hay suficiente stock para "{item.book.title}".', 'danger')
            return redirect(url_for('view_cart'))

    # crear pedido dentro de una transacción
    try:
        order = Order(user_id=current_user.id, status='created', total=0.0)
        db.session.add(order)
        db.session.flush()  # para obtener order.id

        order_total = 0.0
        for item in list(cart.items):  # list() para evitar issues al modificar
            # decrementar stock
            item.book.stock -= item.quantity
            line_price = item.book.price or 0.0
            oi = OrderItem(order_id=order.id, book_id=item.book_id, quantity=item.quantity, price=line_price)
            db.session.add(oi)
            order_total += line_price * item.quantity
            # eliminar item del carrito
            db.session.delete(item)

        order.total = order_total
        db.session.commit()
        flash('✅ Pedido creado correctamente.', 'success')
        return redirect(url_for('view_order', order_id=order.id))
    except SQLAlchemyError as e:
        db.session.rollback()
        app.logger.exception("Error al crear el pedido")
        flash('Ocurrió un error creando el pedido.', 'danger')
        return redirect(url_for('view_cart'))


@app.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)


@app.route('/orders/<int:order_id>')
@login_required
def view_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        flash('Acceso denegado.', 'danger')
        return redirect(url_for('orders'))
    return render_template('order_detail.html', order=order)
 
# --- Prueba de conexión a la BD ---
@app.route('/test-db')
def test_db():
    try:
        db.session.execute("SELECT 1")
        return "✅ Conexión exitosa a la base de datos"
    except SQLAlchemyError as e:
        app.logger.error(f"Error de base de datos: {e}")
        return "❌ Error al conectar a la base de datos"
    except SystemExit as e:
        app.logger.critical("SystemExit detectado, relanzando.")
        raise e
    except BaseException as e:
        app.logger.exception("Error inesperado crítico.")
        raise e
 
# --- Ejecutar aplicación ---
if __name__ == '__main__':
    app.run(debug=True)
