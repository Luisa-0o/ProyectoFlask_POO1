from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, User, Book
from forms import RegisterForm, LoginForm, ChangePasswordForm, BookForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os
from functools import wraps

# --- Configuración inicial ---
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Crear tablas si no existen
with app.app_context():
    db.create_all()

# --- Manejo de Login ---
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # versión actualizada para SQLAlchemy 2.x

# --- Decorador para admin ---
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Primero inicia sesión.', 'warning')
            return redirect(url_for('login'))
        if not getattr(current_user, 'is_admin', False):
            flash('Acceso denegado. Solo administradores.', 'danger')
            return redirect(url_for('index'))
        return fn(*args, **kwargs)
    return wrapper

# --- Rutas principales ---
@app.route('/')
def index():
    return render_template('profile.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
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
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
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
            f = form.cover.data
            filename = secure_filename(f.filename)
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            f.save(os.path.join(upload_folder, filename))

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
            f = form.cover.data
            filename = secure_filename(f.filename)
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            f.save(os.path.join(upload_folder, filename))
            book.cover_filename = filename

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
            except:
                pass
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

# --- Prueba de conexión a la BD ---
@app.route('/test-db')
def test_db():
    try:
        db.session.execute("SELECT 1")
        return "✅ Conexión exitosa a la base de datos"
    except Exception as e:
        return f"❌ Error al conectar: {str(e)}"

# --- Ejecutar aplicación ---
if __name__ == '__main__':
    app.run(debug=True)
