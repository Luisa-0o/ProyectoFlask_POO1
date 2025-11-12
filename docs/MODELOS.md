# 🗄️ Modelos de Base de Datos

Documentación detallada de todos los modelos y relaciones de base de datos de la aplicación.

---

## 📌 User (Usuarios)

**Tabla**: `users`  
**Descripción**: Almacena información de usuarios registrados

### Campos

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---|---|
| `id` | Integer | PRIMARY KEY, AUTOINCREMENT | Identificador único del usuario |
| `username` | String(80) | UNIQUE, NOT NULL | Nombre de usuario (único para cada cuenta) |
| `email` | String(120) | UNIQUE, NOT NULL | Correo electrónico (único y validado) |
| `password_hash` | Text | NOT NULL | Contraseña encriptada con werkzeug |
| `role` | String(20) | DEFAULT 'user' | Rol del usuario ('user' o 'admin') |
| `fav_category1` | String(50) | NULLABLE | Primera categoría favorita para recomendaciones |
| `fav_category2` | String(50) | NULLABLE | Segunda categoría favorita para recomendaciones |

### Índices
- `username` (UNIQUE)
- `email` (UNIQUE)

### Métodos Python

#### `set_password(password: str) -> None`
```python
def set_password(self, password):
    """Encripta y guarda la contraseña en password_hash"""
    self.password_hash = generate_password_hash(password)
```
- Usa `werkzeug.security.generate_password_hash`
- Se llama al registrarse o cambiar contraseña

#### `check_password(password: str) -> bool`
```python
def check_password(self, password):
    """Verifica si la contraseña es correcta"""
    return check_password_hash(self.password_hash, password)
```
- Compara contraseña con hash
- Se usa en login y cambio de contraseña

#### `is_admin` (Propiedad)
```python
@property
def is_admin(self):
    """Retorna True si el usuario es administrador"""
    return self.role == 'admin'
```
- Acceso: `user.is_admin`
- Retorna: `True` si `role == 'admin'`, `False` en caso contrario

### Relaciones

#### `orders` (Relación 1:N)
```
User ──── Order
(1)        (N)
```
- Un usuario puede tener múltiples pedidos
- Acceso: `user.orders`
- Ordenados por: `Order.id DESC`

#### `cart` (Relación 1:1)
```
User ──── Cart
(1)        (1)
```
- Un usuario tiene exactamente un carrito
- Acceso: `user.cart`
- Creado automáticamente al agregar primer item

### Restricciones de Negocio

1. **Primer usuario es admin**
   ```python
   if User.query.count() == 0:
       user.role = 'admin'
   ```

2. **Username único**
   - Validación en formulario RegisterForm
   - Error: "El nombre de usuario ya existe."

3. **Email único y válido**
   - Validación con `email-validator`
   - Error: "El email ya está en uso."

4. **Contraseña mínimo 6 caracteres**
   - Validación en formulario
   - Se recomienda mayor seguridad

### Ciclo de Vida

```
[Registro] → Crear User
    ↓
[Validar datos]
    ↓
[Encriptar contraseña]
    ↓
[¿Primer usuario?] → [Marcar como admin]
    ↓
[Guardar en BD]
    ↓
[Auto-login] → [Redirige a /select-favs]
```

---

## 📖 Book (Libros)

**Tabla**: `books`  
**Descripción**: Catálogo de libros disponibles para compra

### Campos

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---|---|
| `id` | Integer | PRIMARY KEY, AUTOINCREMENT | Identificador único |
| `title` | String(120) | NOT NULL | Título del libro |
| `author` | String(120) | NOT NULL | Nombre del autor |
| `price` | Float | NOT NULL | Precio de venta |
| `stock` | Integer | NOT NULL | Cantidad disponible |
| `description` | Text | NULLABLE | Descripción/sinopsis del libro |
| `category` | String(50) | NULLABLE | Categoría (para filtros y recomendaciones) |
| `cover_filename` | String(255) | NULLABLE | Nombre del archivo de portada en `static/uploads/` |

### Validaciones

- **price**: Debe ser ≥ 0
- **stock**: Debe ser ≥ 0 (entero)
- **title**: Máximo 120 caracteres
- **author**: Máximo 120 caracteres

### Métodos Python

#### `image_url() -> str`
```python
def image_url(self):
    """Retorna la URL de la imagen o una por defecto"""
    if self.cover_filename:
        return url_for('static', filename=f'uploads/{self.cover_filename}')
    return url_for('static', filename='no_cover.png')
```
- Retorna: URL de portada o imagen por defecto
- Uso: En templates para mostrar portada

### Relaciones

#### `cartitems` (Relación 1:N)
```
Book ──── CartItem
(1)        (N)
```
- Un libro puede estar en múltiples carritos
- Acceso: `book.cartitems`

#### `orderitems` (Relación 1:N)
```
Book ──── OrderItem
(1)        (N)
```
- Un libro puede estar en múltiples pedidos
- Acceso: `book.orderitems`

### Restricciones de Negocio

1. **No se puede eliminar si tiene pedidos**
   ```python
   if OrderItem.query.filter_by(book_id=book.id).first():
       flash("No puedes eliminar este libro porque tiene pedidos.")
   ```

2. **Stock se reduce al crear Order**
   ```python
   for item in cart.items:
       item.book.stock -= item.quantity
   ```

3. **Stock se restaura al cancelar Order**
   ```python
   for item in order.items:
       item.book.stock += item.quantity
   ```

### Ciclo de Vida

```
[Crear en admin] → [Validar datos]
    ↓
[Guardar portada (opcional)]
    ↓
[Guardar en BD]
    ↓
[Aparecer en /catalogo]
    ↓
[Usuarios pueden agregar al carrito]
    ↓
[Stock disminuye al comprar]
    ↓
[Se restaura al cancelar pedido]
```

---

## 🛒 Cart (Carrito)

**Tabla**: `carts`  
**Descripción**: Carrito de compras de cada usuario

### Campos

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---|---|
| `id` | Integer | PRIMARY KEY, AUTOINCREMENT | Identificador único |
| `user_id` | Integer | FK(users.id), NOT NULL, UNIQUE | Usuario propietario |
| `created_at` | DateTime | DEFAULT NOW() | Fecha de creación |

### Relación Foreign Key

```
carts.user_id → users.id (UNIQUE)
```
- Un carrito por usuario (1:1)
- ON DELETE CASCADE: Si se elimina usuario → se elimina carrito

### Relaciones

#### `user` (Relación 1:1 inversa)
```python
user = db.relationship('User', backref=db.backref('cart', uselist=False))
```
- Acceso: `cart.user` o `user.cart`
- `uselist=False`: Solo un carrito por usuario

#### `items` (Relación 1:N)
```python
items = db.backref('cart', cascade='all, delete-orphan')
```
- Acceso: `cart.items`
- Contenedor de CartItems
- ON DELETE CASCADE: Si se elimina carrito → se eliminan items

### Ciclo de Vida

```
[Usuario se registra/login]
    ↓
[Intenta agregar producto]
    ↓
[¿Tiene carrito?] → NO → [Crear carrito]
    ↓
[Agregar CartItem]
    ↓
[Usuario puede...]
├─ Continuar comprando
├─ Ver carrito
├─ Modificar cantidades
├─ Remover items
└─ Checkout
    ↓
[Checkout crea Order]
    ↓
[Vacía carrito]
```

---

## 📦 CartItem (Items del Carrito)

**Tabla**: `cart_items`  
**Descripción**: Productos individuales dentro de un carrito

### Campos

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---|---|
| `id` | Integer | PRIMARY KEY, AUTOINCREMENT | Identificador único |
| `cart_id` | Integer | FK(carts.id), NOT NULL | Carrito propietario |
| `book_id` | Integer | FK(books.id), NOT NULL | Libro en el carrito |
| `quantity` | Integer | NOT NULL, DEFAULT 1 | Cantidad del producto |

### Foreign Keys

```
cart_items.cart_id → carts.id (ON DELETE CASCADE)
cart_items.book_id → books.id (ON DELETE CASCADE)
```

### Relaciones

#### `cart` (Relación 1:N inversa)
```python
cart = db.relationship('Cart', backref=db.backref('items', cascade='all, delete-orphan'))
```
- Acceso: `item.cart` o `cart.items`

#### `book` (Relación 1:N inversa)
```python
book = db.relationship('Book')
```
- Acceso: `item.book`
- Contiene todos los datos del libro

### Métodos Python

#### `line_total() -> float`
```python
def line_total(self):
    """Calcula el subtotal del item (cantidad × precio)"""
    return (self.book.price or 0) * (self.quantity or 0)
```
- Retorna: `quantity × price`
- Uso: Cálculo de totales en carrito

### Ejemplo de Uso

```python
# Agregar producto al carrito
item = CartItem(cart_id=cart.id, book_id=book.id, quantity=2)
db.session.add(item)

# Obtener subtotal
subtotal = item.line_total()  # 2 × price

# Aumentar cantidad
item.quantity += 1
```

---

## 📋 Order (Pedidos)

**Tabla**: `orders`  
**Descripción**: Pedidos realizados por usuarios

### Campos

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---|---|
| `id` | Integer | PRIMARY KEY, AUTOINCREMENT | Identificador único del pedido |
| `user_id` | Integer | FK(users.id), NOT NULL | Usuario que realizó la compra |
| `created_at` | DateTime | DEFAULT NOW() | Fecha y hora de creación |
| `status` | String(50) | DEFAULT 'created' | Estado actual del pedido |
| `total` | Float | DEFAULT 0.0 | Monto total del pedido |

### Foreign Keys

```
orders.user_id → users.id (ON DELETE CASCADE)
```

### Estados Válidos

| Estado | Código | Descripción | Transición |
|--------|--------|-------------|-----------|
| `created` | 1️⃣ | Recién creado, sin pagar | → paid, cancelled |
| `paid` | 2️⃣ | Pagado | → shipped, cancelled |
| `shipped` | 3️⃣ | Enviado | → delivered |
| `delivered` | 4️⃣ | Entregado | (final) |
| `cancelled` | ❌ | Cancelado | (final) |

### Transiciones Permitidas

```
created ──→ paid ──────→ shipped ──→ delivered (✅)
  ↓                         
  └─→ cancelled (❌)────→ (final)
      ↓
      └─→ paid ──→ shipped ──→ delivered

paid ──→ shipped ──→ delivered (✅)
  ↓
  └─→ cancelled (❌)
```

### Relaciones

#### `user` (Relación N:1)
```python
user = db.relationship('User', backref=db.backref('orders', order_by='Order.id.desc()'))
```
- Acceso: `order.user`
- Ordenados: Por ID descendente

#### `items` (Relación 1:N)
```python
items = db.backref('order', cascade='all, delete-orphan')
```
- Acceso: `order.items`
- ON DELETE CASCADE: Si se elimina pedido → se eliminan items

### Ciclo de Vida de una Orden

```
[Usuario en /checkout]
    ↓
[Crear Order]
├─ status = 'created'
├─ total = 0.0
└─ user_id = current_user.id
    ↓
[Para cada CartItem]
├─ Crear OrderItem (copia)
├─ Reducir stock del libro
└─ Sumar al total
    ↓
[Guardar Order.total]
    ↓
[Vaciar carrito]
    ↓
[Usuario va a /payment]
    ↓
[Procesa pago]
    ↓
[Status = 'paid']
    ↓
[Admin puede cambiar estado]
├─ 'shipped' (enviado)
├─ 'delivered' (entregado)
└─ 'cancelled' (cancelado)
```

### Ejemplo de Uso

```python
# Crear orden
order = Order(user_id=user.id, status='created', total=0.0)
db.session.add(order)
db.session.flush()  # Para obtener order.id

# Agregar items
for item in cart.items:
    order_item = OrderItem(
        order_id=order.id,
        book_id=item.book_id,
        quantity=item.quantity,
        price=item.book.price
    )
    db.session.add(order_item)
    order.total += item.quantity * item.book.price

# Cambiar estado
order.status = 'paid'
db.session.commit()
```

---

## 📄 OrderItem (Items del Pedido)

**Tabla**: `order_items`  
**Descripción**: Productos individuales dentro de un pedido

### Campos

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---|---|
| `id` | Integer | PRIMARY KEY, AUTOINCREMENT | Identificador único |
| `order_id` | Integer | FK(orders.id), NOT NULL | Pedido propietario |
| `book_id` | Integer | FK(books.id), NOT NULL | Libro comprado |
| `quantity` | Integer | NOT NULL, DEFAULT 1 | Cantidad comprada |
| `price` | Float | NOT NULL | Precio unitario en momento de la compra |

### Foreign Keys

```
order_items.order_id → orders.id (ON DELETE CASCADE)
order_items.book_id → books.id (ON DELETE CASCADE)
```

### Relaciones

#### `order` (Relación N:1)
```python
order = db.relationship('Order', backref=db.backref('items', cascade='all, delete-orphan'))
```
- Acceso: `item.order` o `order.items`

#### `book` (Relación N:1)
```python
book = db.relationship('Book')
```
- Acceso: `item.book`
- Nota: Solo lectura, no se modifica

### Métodos Python

#### `line_total() -> float`
```python
def line_total(self):
    """Calcula el subtotal del item (cantidad × precio)"""
    return (self.price or 0) * (self.quantity or 0)
```
- Retorna: `quantity × price`
- Nota: Usa `price` (no `book.price`), para historicidad

### Importancia de Guardar Precio

```python
# ✅ CORRECTO: Guardar precio en momento de compra
order_item = OrderItem(
    order_id=order.id,
    book_id=book.id,
    quantity=item.quantity,
    price=item.book.price  # Precio en ese momento
)

# ❌ INCORRECTO: Usar precio actual
# Si el libro cambia de precio después:
# El pedido antiguo tendría precio nuevo (incorrecto)
```

### Ejemplo de Uso

```python
# Crear item de pedido
order_item = OrderItem(
    order_id=123,
    book_id=5,
    quantity=2,
    price=19.99
)

# Obtener subtotal
subtotal = order_item.line_total()  # 2 × 19.99 = 39.98

# Ver detalles
print(order_item.book.title)  # Título del libro
print(order_item.price)        # Precio pagado
print(order_item.quantity)     # Cantidad
```

---

## 🔗 Diagrama de Relaciones

```
┌─────────────┐
│    User     │
├─────────────┤
│ id (PK)     │────────────┐
│ username    │            │
│ email       │            │
│ password    │            │ 1:N
│ role        │            │
│ fav_cat1    │            │
│ fav_cat2    │            │
└─────────────┘            │
      │                    │
      │ 1:1                │
      └──────┐             │
             ▼             │
        ┌─────────────┐    │
        │   Cart      │    │
        ├─────────────┤    │
        │ id (PK)     │    │
        │ user_id(FK) │    │
        │ created_at  │    │
        └─────────────┘    │
             │              │
             │ 1:N          │
             ▼              │
        ┌──────────────┐    │
        │  CartItem    │    │
        ├──────────────┤    │
        │ id (PK)      │    │
        │ cart_id (FK) ├────┼──→ (Can be deleted)
        │ book_id (FK) │    │
        │ quantity     │    │
        └──────────────┘    │
             │              │
             │ FK           │
             ▼              │
        ┌─────────────┐     │
        │   Book      │     │
        ├─────────────┤     │
        │ id (PK)     │     │
        │ title       │     │
        │ author      │     │
        │ price       │     │
        │ stock       │     │
        │ category    │     │
        │ cover       │     │
        └─────────────┘     │
             ▲              │
             │              │
             │ 1:N        1:N
             │              │
        ┌──────────────┐    │
        │  OrderItem   │    │
        ├──────────────┤    │
        │ id (PK)      │    │
        │ order_id(FK) │    │
        │ book_id (FK) │    │
        │ quantity     │    │
        │ price        │    │
        └──────────────┘    │
             ▲              │
             │              │
             │ 1:N        N:1
             │              │
        ┌─────────────┐     │
        │   Order     │     │
        ├─────────────┤     │
        │ id (PK)     │     │
        │ user_id(FK) │◄────┘
        │ created_at  │
        │ status      │
        │ total       │
        └─────────────┘
```

---

## 💾 Esquema SQL Completo

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    fav_category1 VARCHAR(50),
    fav_category2 VARCHAR(50)
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(120) NOT NULL,
    author VARCHAR(120) NOT NULL,
    price FLOAT NOT NULL,
    stock INTEGER NOT NULL,
    description TEXT,
    category VARCHAR(50),
    cover_filename VARCHAR(255)
);

CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'created',
    total FLOAT DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    price FLOAT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);
```

---

## 🔍 Consultas Comunes

### Obtener carrito de un usuario
```python
cart = Cart.query.filter_by(user_id=user.id).first()
# O más simple:
cart = current_user.cart
```

### Obtener productos en carrito
```python
items = cart.items
for item in items:
    print(f"{item.book.title}: {item.quantity} × ${item.book.price}")
```

### Obtener total del carrito
```python
total = sum(item.line_total() for item in cart.items)
```

### Obtener pedidos de un usuario
```python
orders = Order.query.filter_by(user_id=user.id).order_by(Order.id.desc()).all()
```

### Obtener items de un pedido
```python
items = order.items
for item in items:
    print(f"{item.book.title}: {item.quantity} × ${item.price}")
```

### Calcular total de pedido
```python
total = sum(item.line_total() for item in order.items)
# O más simple:
total = order.total
```

### Obtener pedidos en estado "paid"
```python
paid_orders = Order.query.filter_by(status='paid').all()
```

### Obtener libros en una categoría
```python
fiction_books = Book.query.filter_by(category='Ficción').all()
```

### Cambiar estado de pedido
```python
order.status = 'shipped'
db.session.commit()
```

### Cancelar pedido (restaurar stock)
```python
for item in order.items:
    item.book.stock += item.quantity
order.status = 'cancelled'
db.session.commit()
```

---

## 📊 Estadísticas por Consulta

### Total de ingresos
```python
total_revenue = db.session.query(func.sum(Order.total)).filter_by(status='paid').scalar()
```

### Total de pedidos
```python
total_orders = Order.query.count()
```

### Total de usuarios
```python
total_users = User.query.count()
```

### Total de libros vendidos
```python
total_sold = db.session.query(func.sum(OrderItem.quantity)).scalar()
```

### Libro más vendido
```python
most_sold = db.session.query(
    Book.title,
    func.sum(OrderItem.quantity).label('total_sold')
).join(OrderItem).group_by(Book.id).order_by('total_sold').first()
```

---

**Documento actualizado**: Noviembre 2025
