# ⚙️ Guía de Instalación

Instrucciones detalladas para instalar y ejecutar el proyecto en diferentes plataformas.

---

## 📋 Requisitos Previos

Asegúrate de tener instalado:

- **Python** 3.8 o superior
  ```bash
  python --version
  ```

- **Git**
  ```bash
  git --version
  ```

- **pip** (gestor de paquetes de Python)
  ```bash
  pip --version
  ```

### Opcional (para Producción)
- **PostgreSQL** 12 o superior
- **Nginx** (como reverse proxy)

---

## 🖥️ Instalación por Sistema Operativo

### Windows

#### Paso 1: Descargar Python
1. Ir a [python.org](https://www.python.org/downloads/)
2. Descargar Python 3.8+
3. **Importante**: Marcar "Add Python to PATH"
4. Ejecutar instalador

#### Paso 2: Clonar Repositorio
```bash
git clone https://github.com/Luisa-0o/ProyectoFlask_POO1.git
cd New_Repo_Flask
```

#### Paso 3: Crear Entorno Virtual
```bash
python -m venv venv
venv\Scripts\activate
```

**Nota**: Después de activar, el prompt debe mostrar `(venv)`

#### Paso 4: Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### Paso 5: Configurar Variables de Entorno
```bash
copy .env.example .env
```

Editar `.env` con Notepad o VS Code:
```
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
FLASK_ENV=development
```

#### Paso 6: Inicializar Base de Datos
Primera vez:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

Siguientes veces:
```bash
flask db upgrade
```

#### Paso 7: Ejecutar
```bash
python app.py
```

Acceder a: `http://localhost:5000`

---

### Linux (Ubuntu/Debian)

#### Paso 1: Instalar Python y dependencias
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv git
```

#### Paso 2: Clonar Repositorio
```bash
git clone https://github.com/Luisa-0o/ProyectoFlask_POO1.git
cd New_Repo_Flask
```

#### Paso 3: Crear Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Paso 4: Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### Paso 5: Configurar Variables de Entorno
```bash
cp .env.example .env
nano .env  # O tu editor favorito
```

Contenido:
```
DATABASE_URL=sqlite:///db.sqlite3
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
FLASK_ENV=development
```

#### Paso 6: Inicializar Base de Datos
```bash
flask db upgrade
```

#### Paso 7: Ejecutar
```bash
python3 app.py
```

O para ejecutar en background:
```bash
nohup python3 app.py &
```

---

### macOS

#### Paso 1: Instalar Homebrew (si no lo tienes)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Paso 2: Instalar Python
```bash
brew install python3 git
```

#### Paso 3: Clonar Repositorio
```bash
git clone https://github.com/Luisa-0o/ProyectoFlask_POO1.git
cd New_Repo_Flask
```

#### Paso 4: Crear Entorno Virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Paso 5: Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### Paso 6: Configurar Variables de Entorno
```bash
cp .env.example .env
nano .env
```

#### Paso 7: Inicializar Base de Datos
```bash
flask db upgrade
```

#### Paso 8: Ejecutar
```bash
python3 app.py
```

---

## 🐘 Instalación con PostgreSQL (Producción)

### Linux

#### Paso 1: Instalar PostgreSQL
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### Paso 2: Crear Base de Datos
```bash
sudo -u postgres psql
```

En la consola psql:
```sql
CREATE DATABASE bookstore;
CREATE USER bookstore_user WITH PASSWORD 'contraseña_segura';
ALTER ROLE bookstore_user SET client_encoding TO 'utf8';
ALTER ROLE bookstore_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE bookstore_user SET default_transaction_deferrable TO on;
ALTER ROLE bookstore_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE bookstore TO bookstore_user;
\q
```

#### Paso 3: Configurar .env
```bash
nano .env
```

```
DATABASE_URL=postgresql://bookstore_user:contraseña_segura@localhost:5432/bookstore
SECRET_KEY=tu-clave-secreta-muy-segura-aqui
FLASK_ENV=production
```

#### Paso 4: Instalar driver PostgreSQL
```bash
pip install psycopg2-binary
```

(Ya está en requirements.txt)

#### Paso 5: Ejecutar migraciones
```bash
flask db upgrade
```

#### Paso 6: Ejecutar con Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 🌐 Despliegue en Heroku

### Requisitos
- Cuenta en [heroku.com](https://www.heroku.com)
- Heroku CLI instalado

### Pasos

#### 1. Crear aplicación Heroku
```bash
heroku login
heroku create nombre-app
```

#### 2. Agregar PostgreSQL
```bash
heroku addons:create heroku-postgresql:hobby-dev -a nombre-app
```

#### 3. Configurar variables de entorno
```bash
heroku config:set SECRET_KEY=tu-clave-secreta -a nombre-app
heroku config:set FLASK_ENV=production -a nombre-app
```

#### 4. Crear Procfile
Crear archivo `Procfile` en raíz:
```
web: gunicorn app:app
release: flask db upgrade
```

#### 5. Crear runtime.txt
Crear archivo `runtime.txt`:
```
python-3.11.9
```

#### 6. Push a Heroku
```bash
git push heroku main
```

#### 7. Ver logs
```bash
heroku logs --tail -a nombre-app
```

#### 8. Acceder
```
https://nombre-app.herokuapp.com
```

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"

**Causa**: Dependencias no instaladas

**Solución**:
```bash
pip install -r requirements.txt
```

---

### Error: "La variable DATABASE_URL no está definida"

**Causa**: Archivo `.env` no existe o no tiene DATABASE_URL

**Solución**:
```bash
copy .env.example .env
# Editar .env con la URL de tu base de datos
```

---

### Error: "sqlite3.OperationalError: no such table: users"

**Causa**: Base de datos no inicializada

**Solución**:
```bash
flask db upgrade
```

---

### Error: "Address already in use"

**Causa**: Puerto 5000 ya está en uso

**Solución** (Windows):
```bash
# Encontrar proceso en puerto 5000
netstat -ano | findstr :5000

# Matar proceso (reemplazar PID)
taskkill /PID <PID> /F

# O ejecutar en puerto diferente
python app.py --port 5001
```

**Solución** (Linux/macOS):
```bash
# Encontrar proceso
lsof -i :5000

# Matar proceso
kill -9 <PID>

# O ejecutar en puerto diferente
python3 app.py --port 5001
```

---

### Error: "FileNotFoundError: [Errno 2] No such file or directory: 'db.sqlite3'"

**Causa**: Base de datos no creada

**Solución**:
```bash
flask db upgrade
```

---

### Error al subir imágenes de portadas

**Causa**: Carpeta `static/uploads/` no existe

**Solución**:
```bash
mkdir static/uploads
```

---

### Contraseña de admin olvidada

**Causa**: Olvidó credenciales del admin

**Solución**: Usar script `make_admin.py`:
```bash
python make_admin.py
```

---

### Base de datos corrupta

**Causa**: Archivos de BD dañados

**Solución**:
```bash
# Respaldar data si es importante
cp db.sqlite3 db.sqlite3.backup

# Eliminar BD
rm db.sqlite3

# Reinicializar
flask db upgrade
```

---

## ✅ Verificar Instalación

Ejecuta estos comandos para verificar que todo está bien:

### 1. Versión de Python
```bash
python --version
# Debe ser 3.8+
```

### 2. Paquetes instalados
```bash
pip list
# Debe mostrar Flask, SQLAlchemy, etc.
```

### 3. Base de datos
```bash
flask db current
# Debe mostrar última migración
```

### 4. Conexión a BD
```bash
python -c "from models import db; print('BD OK')"
```

### 5. Ejecutar aplicación
```bash
python app.py
# Debe mostrar "Running on http://localhost:5000"
```

---

## 🚀 Primer Usuario (Admin)

El **primer usuario registrado** en la aplicación es automáticamente **administrador**.

### Pasos:
1. Ejecutar aplicación: `python app.py`
2. Ir a `http://localhost:5000/register`
3. Llenar formulario de registro
4. Hacer click "Registrarse"
5. Seleccionar 2 categorías favoritas
6. ¡Listo! Eres admin

### Si necesitas volver admin a otro usuario:

Opción 1: Usar script
```bash
python make_admin.py
```

Opción 2: Editar directamente en base de datos
```bash
# En Python shell
from models import db, User
user = User.query.filter_by(username='usuario').first()
user.role = 'admin'
db.session.commit()
```

---

## 📁 Estructura de Carpetas Después de Instalación

```
New_Repo_Flask/
├── venv/                      # Entorno virtual (creado)
├── migrations/                # Migraciones (creado si no existen)
├── static/
│   └── uploads/              # Portadas (crear si no existe)
├── app.py
├── models.py
├── forms.py
├── config.py
├── requirements.txt
├── .env                       # Archivo de config (creado)
├── db.sqlite3                 # BD (creado)
└── README.md
```

---

## 🔒 Seguridad en Instalación

### En Desarrollo

1. **SECRET_KEY** puede ser cualquier string
   ```
   SECRET_KEY=desarrollo-clave
   ```

2. **DATABASE_URL** puede ser SQLite
   ```
   DATABASE_URL=sqlite:///db.sqlite3
   ```

3. **FLASK_ENV**
   ```
   FLASK_ENV=development
   ```

### En Producción

1. **SECRET_KEY** debe ser aleatorio y seguro
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **DATABASE_URL** debe ser PostgreSQL con contraseña fuerte
   ```
   DATABASE_URL=postgresql://user:password@host:5432/db
   ```

3. **FLASK_ENV** debe ser production
   ```
   FLASK_ENV=production
   ```

4. **Usar HTTPS** (Heroku o Nginx/Certbot)

5. **Configurar CORS** si necesitas

---

## 📖 Próximos Pasos

Después de instalar:

1. ✅ Lee el [README.md](../README.md)
2. ✅ Lee [PAGINAS.md](PAGINAS.md) para entender las rutas
3. ✅ Lee [MODELOS.md](MODELOS.md) para entender la BD
4. ✅ Explora el código en `app.py`
5. ✅ Crea algunos libros desde el panel admin
6. ✅ Realiza una compra de prueba

---

**Documento actualizado**: Noviembre 2025

¿Necesitas ayuda? Abre un issue en el repositorio.
