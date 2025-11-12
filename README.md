# 📚 Sistema de Tienda Online de Libros

**Aplicación web para compra y venta de libros** desarrollada con Flask, SQLAlchemy y Bootstrap. Incluye autenticación de usuarios, carrito de compras, procesamiento de pagos y panel administrativo completo.

> **Repositorio**: [Luisa-0o/ProyectoFlask_POO1](https://github.com/Luisa-0o/ProyectoFlask_POO1)

---

## 🎯 Características Principales

✅ **Autenticación Segura**
- Registro e inicio de sesión de usuarios
- Validación de email único
- Contraseñas encriptadas con Werkzeug
- Cambio de contraseña

✅ **Catálogo Dinámico**
- Listado completo de libros
- Búsqueda por título y autor
- Filtrado por categorías
- Recomendaciones personalizadas basadas en categorías favoritas

✅ **Carrito de Compras**
- Agregar/remover productos
- Actualizar cantidades
- Cálculo automático de totales
- Validación de stock disponible

✅ **Sistema de Pedidos**
- Crear pedidos desde carrito
- Ver historial de compras
- Seguimiento de estado del pedido (created, paid, shipped, delivered, cancelled)
- Cancelación de pedidos con restauración de stock

✅ **Procesamiento de Pagos**
- Formulario de pago simulado
- Actualización de estado de pedido a "paid"
- Seguridad CSRF en todos los formularios

✅ **Generación de Facturas**
- Facturas detalladas con datos del cliente
- Información de productos y precios
- Opción de impresión
- Diseño profesional

✅ **Panel Administrativo**
- Gestión completa de libros (CRUD)
- Gestión de usuarios
- Visualización y actualización de pedidos de clientes
- Control de permisos y roles

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Descripción |
|------------|---------|-------------|
| **Python** | 3.8+ | Lenguaje principal |
| **Flask** | 3.1.2 | Framework web |
| **SQLAlchemy** | 2.0.44 | ORM para base de datos |
| **Flask-SQLAlchemy** | 3.1.1 | Integración SQLAlchemy-Flask |
| **Flask-Login** | 0.6.3 | Autenticación de usuarios |
| **Flask-Migrate** | 4.1.0 | Migraciones de BD (Alembic) |
| **Flask-WTF** | 1.2.2 | Manejo de formularios con validación |
| **WTForms** | 3.2.1 | Validación de formularios |
| **Bootstrap** | 5.x | Framework CSS |
| **Jinja2** | 3.1.6 | Motor de templates HTML |
| **PostgreSQL** | - | Base de datos (producción) |
| **SQLite** | - | Base de datos (desarrollo) |

---

## 📋 Requisitos Previos

- **Python** 3.8 o superior
- **Git**
- **pip** (gestor de paquetes de Python)
- **PostgreSQL** (opcional, para producción)

---

## ⚙️ Instalación

### 1️⃣ Clonar el Repositorio

```bash
git clone https://github.com/Luisa-0o/ProyectoFlask_POO1.git
cd New_Repo_Flask
```

### 2️⃣ Crear Entorno Virtual

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Configurar Variables de Entorno

Copiar archivo de ejemplo:
```bash
# Windows
copy .env.example .env

# Linux/macOS
cp .env.example .env
```

Editar `.env` con tus valores:
```bash
# Base de datos
DATABASE_URL=sqlite:///db.sqlite3

# Clave secreta para sesiones
SECRET_KEY=tu-clave-secreta-muy-segura-aqui

# Carpeta de subidas (opcional)
UPLOAD_FOLDER=static/uploads
FLASK_ENV=development
```

**Nota**: Para producción, usar PostgreSQL:
```
DATABASE_URL=postgresql://usuario:password@localhost:5432/bookstore
```

### 5️⃣ Inicializar Base de Datos

**Primera ejecución:**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

**Siguientes ejecuciones:**
```bash
flask db upgrade
```

### 6️⃣ Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

---

## 📁 Estructura del Proyecto

```
New_Repo_Flask/
├── app.py                          # Aplicación principal (rutas y lógica)
├── models.py                       # Modelos de base de datos
├── forms.py                        # Formularios WTForms
├── config.py                       # Configuración de la app
├── requirements.txt                # Dependencias de Python
├── db.sqlite3                      # Base de datos (desarrollo)
├── README.md                       # Este archivo
├── .env.example                    # Plantilla de variables de entorno
├── .gitignore                      # Archivos ignorados por Git
│
├── migrations/                     # Migraciones de base de datos
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                  # Historial de cambios
│
├── static/                         # Archivos estáticos
│   ├── style.css                  # Estilos CSS personalizados
│   └── uploads/                   # Portadas de libros (subidas)
│
├── templates/                      # Plantillas HTML
│   ├── base.html                  # Plantilla base (navbar, footer)
│   ├── login.html                 # Página de login
│   ├── register.html              # Página de registro
│   ├── profile.html               # Perfil del usuario
│   ├── catalogo.html              # Catálogo de libros
│   ├── select_favs.html           # Seleccionar categorías favoritas
│   ├── cart.html                  # Carrito de compras
│   ├── checkout.html              # Confirmación de compra
│   ├── payment.html               # Página de pago
│   ├── orders.html                # Historial de pedidos
│   ├── order_detail.html          # Detalle de un pedido
│   ├── invoice.html               # Factura (imprimible)
│   ├── change_password.html       # Cambiar contraseña
│   ├── admin.html                 # Panel admin principal
│   ├── admin_books.html           # Gestión de libros (admin)
│   ├── admin_users.html           # Gestión de usuarios (admin)
│   ├── admin_orders.html          # Gestión de pedidos (admin)
│   ├── create_book.html           # Crear libro (admin)
│   ├── edit_book.html             # Editar libro (admin)
│   ├── add_user.html              # Agregar usuario (admin)
│   └── edit_user.html             # Editar usuario (admin)
│
└── __pycache__/                   # Archivos compilados (auto-generado)
```

---

## 👥 Tipos de Usuario y Roles

### 👤 Usuario Normal
- Navegar por el catálogo de libros
- Buscar libros por título/autor
- Filtrar por categorías
- Seleccionar 2 categorías favoritas (recomendaciones personalizadas)
- Agregar/remover libros del carrito
- Realizar compras
- Ver historial de pedidos
- Descargar/imprimir facturas
- Cancelar pedidos (si es posible)
- Cambiar contraseña

### 🔐 Administrador
- Acceso completo al panel administrativo
- **Gestión de Libros**: Crear, editar, eliminar
- **Gestión de Usuarios**: Crear, editar, eliminar
- **Gestión de Pedidos**: Ver estado, actualizar estado (created → paid → shipped → delivered → cancelled)
- **Visualización de reportes** de pedidos de clientes

**Nota**: El primer usuario registrado en la aplicación es automáticamente administrador.

---

## 🗄️ Modelos de Base de Datos

### 📌 User (Usuarios)
```
- id: Identificador único
- username: Nombre de usuario (único)
- email: Correo electrónico (único)
- password_hash: Contraseña encriptada
- role: 'user' o 'admin' (por defecto: 'user')
- fav_category1: Primera categoría favorita (opcional)
- fav_category2: Segunda categoría favorita (opcional)
```

### 📖 Book (Libros)
```
- id: Identificador único
- title: Título del libro
- author: Autor del libro
- price: Precio unitario
- stock: Cantidad disponible
- description: Descripción del libro
- category: Categoría del libro
- cover_filename: Nombre del archivo de portada
```

### 🛒 Cart (Carrito)
```
- id: Identificador único
- user_id: Usuario propietario (relación 1:1)
- created_at: Fecha de creación
- items: Relación con CartItem
```

### 📦 CartItem (Items del Carrito)
```
- id: Identificador único
- cart_id: Carrito propietario
- book_id: Libro en el carrito
- quantity: Cantidad del producto
```

### 📋 Order (Pedidos)
```
- id: Identificador único
- user_id: Usuario que realizó la compra
- created_at: Fecha de creación
- status: Estado del pedido (created, paid, shipped, delivered, cancelled)
- total: Monto total del pedido
```

### 📄 OrderItem (Items del Pedido)
```
- id: Identificador único
- order_id: Pedido propietario
- book_id: Libro comprado
- quantity: Cantidad comprada
- price: Precio en el momento de la compra
```

---

## 🔄 Flujo Principal de la Aplicación

```
┌─────────────────────────────────────────────────┐
│         USUARIO NUEVO                           │
├─────────────────────────────────────────────────┤
│  1. Ingresa a /register                         │
│  2. Completa formulario de registro             │
│  3. Sistema crea cuenta (primer user = admin)   │
│  4. Auto-login y redirige a /select-favs       │
│  5. Selecciona 2 categorías favoritas          │
│  6. Redirige a /catalogo                       │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│         USUARIO COMPRA UN LIBRO                 │
├─────────────────────────────────────────────────┤
│  1. Navega /catalogo (ve recomendaciones)       │
│  2. Busca/filtra libros                         │
│  3. Hace click en libro                         │
│  4. Selecciona cantidad                         │
│  5. "Agregar al carrito" → /cart/add/<id>      │
│  6. Va a /cart (revisa carrito)                 │
│  7. Click "Checkout" → /checkout               │
│  8. Sistema crea Order + OrderItems             │
│  9. Reduce stock, vacía carrito                 │
│  10. Redirige a /payment                        │
│  11. Ingresa datos de tarjeta                   │
│  12. Procesa pago → Order status = "paid"       │
│  13. Redirige a /catalogo (éxito)               │
│  14. Puede ver pedido en /orders/<order_id>     │
│  15. Descargar factura en /invoice/<order_id>   │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│         ADMIN GESTIONA TIENDA                   │
├─────────────────────────────────────────────────┤
│  1. Accede a /admin                             │
│  2. /admin/books → CRUD de libros               │
│  3. /admin/users → Gestión de usuarios          │
│  4. /admin/orders → Seguimiento de pedidos      │
│  5. Puede actualizar estado de órdenes          │
└─────────────────────────────────────────────────┘
```

---

## 🔐 Seguridad Implementada

✅ **Contraseñas Encriptadas**
- Uso de `werkzeug.security.generate_password_hash` y `check_password_hash`
- Hash seguro para todas las contraseñas

✅ **Protección CSRF**
- Validación CSRF en todos los formularios con Flask-WTF
- Tokens CSRF en templates

✅ **Validación de Formularios**
- Validación en cliente (HTML5) y servidor (WTForms)
- Validadores personalizados para emails y usernames únicos

✅ **Rutas Protegidas**
- Decorador `@login_required` en rutas que requieren autenticación
- Decorador personalizado `@admin_required` para rutas solo admin

✅ **Control de Acceso**
- Verificación que el usuario es propietario del pedido/carrito
- Admin solo puede ver pedidos de usuarios normales

✅ **Validación de URLs**
- Función `is_safe_url()` previene open redirects

✅ **Manejo de Excepciones**
- Try-catch para operaciones de BD
- Logging de errores

---

## 📊 Rutas Principales

### Autenticación
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Perfil del usuario |
| `/register` | GET, POST | Registro de usuario |
| `/login` | GET, POST | Inicio de sesión |
| `/logout` | GET | Cerrar sesión |
| `/change-password` | GET, POST | Cambiar contraseña |

### Catálogo
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/catalogo` | GET | Ver catálogo de libros |
| `/select-favs` | GET, POST | Seleccionar categorías favoritas |

### Carrito y Compras
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/cart` | GET | Ver carrito |
| `/cart/add/<book_id>` | GET, POST | Agregar al carrito |
| `/cart/remove/<item_id>` | POST | Remover del carrito |
| `/checkout` | GET, POST | Crear pedido |
| `/payment` | GET, POST | Procesar pago |

### Pedidos e Invoices
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/orders` | GET | Ver historial de pedidos |
| `/orders/<order_id>` | GET | Ver detalle de pedido |
| `/orders/<order_id>/cancel` | POST | Cancelar pedido |
| `/invoice/<order_id>` | GET | Ver factura |

### Panel Administrativo
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/admin` | GET | Dashboard admin |
| `/admin/books` | GET | Listar libros |
| `/admin/books/create` | GET, POST | Crear libro |
| `/admin/books/edit/<id>` | GET, POST | Editar libro |
| `/admin/books/delete/<id>` | POST | Eliminar libro |
| `/admin/users` | GET | Listar usuarios |
| `/admin/users/add` | GET, POST | Agregar usuario |
| `/admin/users/edit/<id>` | GET, POST | Editar usuario |
| `/admin/users/delete/<id>` | POST | Eliminar usuario |
| `/admin/orders` | GET | Ver pedidos de clientes |
| `/admin/orders/<id>` | GET | Ver detalle de pedido |
| `/admin/orders/<id>/status` | POST | Actualizar estado de pedido |

---

## 🎨 Formularios Disponibles

### RegisterForm
- Username (3-80 caracteres, único)
- Email (válido, único)
- Contraseña (mín. 6 caracteres)
- Confirmar contraseña

### LoginForm
- Email
- Contraseña

### ChangePasswordForm
- Contraseña actual
- Nueva contraseña
- Confirmar nueva contraseña

### BookForm
- Título
- Autor
- Categoría
- Precio
- Stock
- Descripción
- Portada (imagen opcional)

---

## 🚀 Despliegue

### En Heroku

```bash
# Crear aplicación
heroku create nombre-app

# Configurar variables de entorno
heroku config:set SECRET_KEY=tu-clave
heroku config:set DATABASE_URL=postgresql://...

# Subir código
git push heroku main

# Ejecutar migraciones
heroku run flask db upgrade

# Ver logs
heroku logs --tail
```

### En Servidor Linux (DigitalOcean, AWS, etc.)

```bash
# Instalar Python y PostgreSQL
sudo apt-get install python3 python3-pip postgresql

# Clonar repositorio
git clone https://github.com/Luisa-0o/ProyectoFlask_POO1.git
cd New_Repo_Flask

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env con PostgreSQL
nano .env

# Inicializar BD
flask db upgrade

# Instalar Gunicorn
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Con Nginx como Reverse Proxy

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /home/usuario/New_Repo_Flask/static;
    }
}
```

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "La variable DATABASE_URL no está definida"
Asegúrate de que el archivo `.env` existe y contiene `DATABASE_URL`:
```bash
cat .env
```

### Error: "sqlite3.OperationalError: no such table: users"
Ejecutar migraciones:
```bash
flask db upgrade
```

### Puerto 5000 ya en uso
```bash
python app.py --port 5001
```

### Error al subir imágenes
Verificar que la carpeta `static/uploads/` existe:
```bash
mkdir -p static/uploads
```

---

## 📝 Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SECRET_KEY` | Clave secreta de Flask | `mi-clave-secreta-segura` |
| `DATABASE_URL` | URL de base de datos | `sqlite:///db.sqlite3` |
| `UPLOAD_FOLDER` | Carpeta de subidas | `static/uploads` |
| `FLASK_ENV` | Entorno (development/production) | `development` |

---

## 🤝 Contribuir

1. **Fork** el proyecto
2. **Crea una rama** con tu funcionalidad:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. **Commit** tus cambios:
   ```bash
   git commit -m "Agregar nueva funcionalidad"
   ```
4. **Push** a la rama:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. **Abre un Pull Request**

---

## 📧 Contacto

- **Autor**: Luisa Builes
- **GitHub**: [@Luisa-0o](https://github.com/Luisa-0o)
- **Repositorio**: [ProyectoFlask_POO1](https://github.com/Luisa-0o/ProyectoFlask_POO1)

---

## 📜 Licencia

Este proyecto está bajo licencia **MIT**. Ver archivo `LICENSE` para más detalles.

---

## 📅 Historial de Cambios

### [1.0.0] - Noviembre 2025

#### ✨ Características Principales
- ✅ Autenticación de usuarios (registro, login, logout)
- ✅ Catálogo dinámico con búsqueda y filtros
- ✅ Carrito de compras funcional
- ✅ Sistema de pedidos con múltiples estados
- ✅ Procesamiento de pagos (simulado)
- ✅ Generación de facturas imprimibles
- ✅ Panel administrativo completo
- ✅ Recomendaciones personalizadas

#### 🔧 Tecnologías
- Flask 3.1.2
- SQLAlchemy 2.0.44
- Bootstrap 5
- PostgreSQL + SQLite

---

**Última actualización**: Noviembre 11, 2025

**¿Preguntas?** Abre un issue en el repositorio.
