from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from models import db, User
from forms import RegisterForm, LoginForm, ChangePasswordForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('profile.html')

@app.route('/register', methods=['GET','POST'])
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

@app.route('/login', methods=['GET','POST'])
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

@app.route('/change-password', methods=['GET','POST'])
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

# solo visible para admin
@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('No tienes permiso para acceder a esta página.', 'danger')
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('admin.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
