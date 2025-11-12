# 📚 Índice de Documentación

Bienvenido a la documentación del Sistema de Tienda Online de Libros. Aquí encontrarás toda la información que necesitas para entender, instalar y usar la aplicación.

---

## 🗂️ Contenido Disponible

### 📖 [README.md](../README.md) - Comienza aquí
Información general del proyecto:
- 🎯 Características principales
- 🛠️ Tecnologías utilizadas
- ⚙️ Instalación rápida
- 👥 Roles de usuario
- 🔐 Seguridad
- 📊 Endpoints principales
- 🚀 Despliegue

**Tiempo de lectura**: 15 minutos

---

### 🏠 [INSTALACION.md](INSTALACION.md) - Guía Paso a Paso
Instrucciones detalladas de instalación:
- 📋 Requisitos previos
- 🖥️ Instalación por sistema operativo (Windows, Linux, macOS)
- 🐘 Instalación con PostgreSQL
- 🌐 Despliegue en Heroku
- 🐛 Solución de problemas
- ✅ Verificación de instalación
- 🔒 Seguridad en instalación

**Recomendado**: Leer antes de instalar

**Tiempo de lectura**: 20 minutos

---

### 📄 [PAGINAS.md](PAGINAS.md) - Documentación de Rutas
Descripción detallada de cada página:
- 🏠 Página principal
- 📝 Registro e inicio de sesión
- 🔑 Gestión de contraseña
- ⭐ Seleccionar categorías favoritas
- 📚 Catálogo con búsqueda y filtros
- 🛒 Carrito de compras
- 💳 Checkout y pago
- 📋 Pedidos e historial
- 📥 Facturas
- 🛠️ Panel administrativo

**Para**: Entender qué hace cada página

**Tiempo de lectura**: 30 minutos

---

### 🗄️ [MODELOS.md](MODELOS.md) - Base de Datos
Documentación de modelos y relaciones:
- 📌 User (Usuarios)
- 📖 Book (Libros)
- 🛒 Cart (Carrito)
- 📦 CartItem (Items del carrito)
- 📋 Order (Pedidos)
- 📄 OrderItem (Items del pedido)
- 🔗 Diagrama de relaciones
- 💾 Esquema SQL completo
- 🔍 Consultas comunes

**Para**: Entender la estructura de la base de datos

**Tiempo de lectura**: 25 minutos

---

## 🎯 Rutas Recomendadas de Lectura

### 👤 Si eres Usuario Final
1. Lee [README.md](../README.md) - Características
2. Lee [PAGINAS.md](PAGINAS.md) - Cómo usar
3. ¡Comienza a comprar! 📚

### 💻 Si eres Desarrollador
1. Lee [README.md](../README.md) - Introducción
2. Lee [INSTALACION.md](INSTALACION.md) - Instala el proyecto
3. Lee [PAGINAS.md](PAGINAS.md) - Rutas y lógica
4. Lee [MODELOS.md](MODELOS.md) - Base de datos
5. Explora el código en `app.py`, `models.py`, `forms.py`
6. ¡Comienza a contribuir! 🚀

### 🔧 Si necesitas Desplegar
1. Lee [README.md](../README.md) - General
2. Lee [INSTALACION.md](INSTALACION.md) - Especialmente sección de Heroku
3. Configura variables de entorno
4. Ejecuta migraciones
5. ¡Publica! 🌐

### 🐛 Si encontraste un Bug
1. Lee [PAGINAS.md](PAGINAS.md) - Verifica comportamiento esperado
2. Lee [MODELOS.md](MODELOS.md) - Entiende el flujo de datos
3. Revisa `app.py` - Encuentra el código relevante
4. Abre un issue en GitHub 📝

---

## 📚 Tabla Rápida de Referencias

### Instalación
- **Primera vez**: [INSTALACION.md - Paso 1-7](INSTALACION.md#windows)
- **Producción**: [INSTALACION.md - PostgreSQL](INSTALACION.md#instalación-con-postgresql-producción)
- **Heroku**: [INSTALACION.md - Heroku](INSTALACION.md#despliegue-en-heroku)
- **Problemas**: [INSTALACION.md - Solución de Problemas](INSTALACION.md#-solución-de-problemas)

### Características
- **Autenticación**: [PAGINAS.md - Registro y Login](PAGINAS.md#📝-registro-registro)
- **Catálogo**: [PAGINAS.md - Catálogo](PAGINAS.md#📚-catálogo-catalogo)
- **Compra**: [PAGINAS.md - Checkout](PAGINAS.md#💳-checkout-checkout)
- **Admin**: [PAGINAS.md - Panel Admin](PAGINAS.md#-panel-admin-admin)

### Técnico
- **Modelos**: [MODELOS.md](MODELOS.md)
- **Rutas**: [PAGINAS.md](PAGINAS.md)
- **Seguridad**: [README.md - Seguridad](../README.md#-seguridad-implementada)
- **Despliegue**: [README.md - Despliegue](../README.md#-despliegue)

---

## 🔗 Links Rápidos

### Repositorio
- **GitHub**: [Luisa-0o/ProyectoFlask_POO1](https://github.com/Luisa-0o/ProyectoFlask_POO1)
- **Issues**: [Reportar problemas](https://github.com/Luisa-0o/ProyectoFlask_POO1/issues)
- **Discussions**: [Hacer preguntas](https://github.com/Luisa-0o/ProyectoFlask_POO1/discussions)

### Tecnologías
- **Flask**: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- **SQLAlchemy**: [sqlalchemy.org](https://www.sqlalchemy.org/)
- **Bootstrap**: [getbootstrap.com](https://getbootstrap.com/)
- **PostgreSQL**: [postgresql.org](https://www.postgresql.org/)

### Herramientas
- **Python**: [python.org](https://www.python.org/)
- **Git**: [git-scm.com](https://git-scm.com/)
- **Heroku**: [heroku.com](https://www.heroku.com/)

---

## ❓ Preguntas Frecuentes (FAQ)

### ¿Cómo instalo el proyecto?
Ver [INSTALACION.md](INSTALACION.md) - Guía completa paso a paso.

### ¿Cuáles son las características principales?
Ver [README.md - Características](../README.md#-características-principales).

### ¿Qué rol tengo después de registrarme?
El primer usuario es admin. Los siguientes son usuarios normales.
Ver [README.md - Roles](../README.md#-tipos-de-usuario-y-roles).

### ¿Cómo cambio de contraseña?
Ir a `http://localhost:5000/change-password`.
Ver [PAGINAS.md - Cambiar Contraseña](PAGINAS.md#-cambiar-contraseña-change-password).

### ¿Cómo cargo libros?
Siendo admin, ir a `/admin/books/create`.
Ver [PAGINAS.md - Crear Libro](PAGINAS.md#crear-libro-admin-bookscreate).

### ¿Cómo compro un libro?
1. Navega al catálogo (`/catalogo`)
2. Haz click en un libro
3. Selecciona cantidad
4. "Agregar al carrito"
5. Revisa carrito (`/cart`)
6. "Checkout"
7. Completa formulario de pago

Ver [PAGINAS.md - Flujo de Compra](PAGINAS.md#-agregar-al-carrito-cart-addbook_id).

### ¿Cómo veo mis facturas?
Ve a `/orders`, haz click en un pedido, luego "Ver Factura".
Ver [PAGINAS.md - Facturas](PAGINAS.md#-ver-factura-invoiceorder_id).

### ¿Qué bases de datos se soportan?
- **Desarrollo**: SQLite (por defecto)
- **Producción**: PostgreSQL (recomendado)

Ver [INSTALACION.md - PostgreSQL](INSTALACION.md#-instalación-con-postgresql-producción).

### ¿Cómo despliega en Heroku?
Ver [INSTALACION.md - Heroku](INSTALACION.md#-despliegue-en-heroku).

### ¿Qué pasa si olvido la contraseña?
No hay función de "Olvidé contraseña" implementada.
**Soluciones**:
1. Contactar a admin para reset
2. Usar script `make_admin.py`
3. Editar BD directamente

### ¿Es segura la aplicación?
Sí. Tiene protección CSRF, contraseñas encriptadas, rutas protegidas.
Ver [README.md - Seguridad](../README.md#-seguridad-implementada).

### ¿Puedo contribuir?
¡Claro! Lee [README.md - Contribuir](../README.md#-contribuir).

---

## 📞 Contacto y Soporte

- **Autor**: Luisa Builes
- **GitHub**: [@Luisa-0o](https://github.com/Luisa-0o)
- **Email**: (Ver perfil de GitHub)

---

## 📋 Checklist para Comenzar

- [ ] Leí el README.md
- [ ] Instalé el proyecto siguiendo INSTALACION.md
- [ ] Ejecuté la aplicación sin errores
- [ ] Creé usuario admin (primer registro)
- [ ] Exploré el panel admin
- [ ] Agregué algunos libros
- [ ] Hice una compra de prueba
- [ ] Descargué una factura
- [ ] Cambié de contraseña
- [ ] Exploré el código en app.py

---

## 📊 Estadísticas de Documentación

| Documento | Páginas | Tiempo Lectura | Audiencia |
|-----------|---------|---|---|
| README.md | 4-5 | 15 min | Todos |
| INSTALACION.md | 5-6 | 20 min | Desarrolladores |
| PAGINAS.md | 8-10 | 30 min | Desarrolladores |
| MODELOS.md | 6-8 | 25 min | Desarrolladores/BD |
| **Total** | **23-29** | **90 min** | - |

---

## 🎓 Material de Aprendizaje

### Para Entender la Arquitectura
1. Lee [MODELOS.md - Diagrama de Relaciones](MODELOS.md#-diagrama-de-relaciones)
2. Lee [PAGINAS.md - Flujos](PAGINAS.md)
3. Abre `app.py` en VS Code y explora

### Para Contribuir
1. Fork el repositorio
2. Lee [README.md - Contribuir](../README.md#-contribuir)
3. Lee [PAGINAS.md](PAGINAS.md) - Entiende las rutas
4. Lee [MODELOS.md](MODELOS.md) - Entiende la BD
5. Crea una rama: `git checkout -b feature/tu-feature`
6. Realiza cambios y commits
7. Push y crea Pull Request

### Para Resolver Bugs
1. Lee [INSTALACION.md - Solución de Problemas](INSTALACION.md#-solución-de-problemas)
2. Lee [PAGINAS.md](PAGINAS.md) - Comportamiento esperado
3. Examina `app.py` - Encuentra el código
4. Verifica `models.py` - Lógica de datos
5. Abre issue si es problema general

---

## 🗺️ Roadmap de Documentación

En el futuro, se agregarán:
- [ ] Guía de API (si se convierte en API REST)
- [ ] Video tutoriales
- [ ] Tests unitarios
- [ ] Diagrama de arquitectura mejorado
- [ ] Guía de buenas prácticas

---

**Última actualización**: Noviembre 2025

**¿Algo no está claro?** Abre un issue en GitHub.
