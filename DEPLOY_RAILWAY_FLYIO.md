# Despliegue con Railway (Base de Datos) + Fly.io (Aplicación)

## Paso 1: Configurar MySQL en Railway

### 1.1 Crear cuenta en Railway
1. Ve a https://railway.app/
2. Click en "Start a New Project"
3. Login con GitHub

### 1.2 Crear base de datos MySQL
1. Click en "New Project"
2. Selecciona "Provision MySQL"
3. Espera a que se cree (unos segundos)

### 1.3 Obtener credenciales de conexión
1. Click en el servicio MySQL creado
2. Ve a la pestaña "Connect"
3. Verás las variables:
   - `MYSQLHOST`
   - `MYSQLPORT`
   - `MYSQLDATABASE`
   - `MYSQLUSER`
   - `MYSQLPASSWORD`

**Guarda estas credenciales**, las necesitarás para Fly.io

### 1.4 Importar el Schema de la base de datos

**Opción A: Usando Railway CLI**
```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Conectar al proyecto
railway link

# Conectar a MySQL
railway connect MySQL

# Una vez conectado, ejecutar:
source .docker/mysql/database/init.sql
```

**Opción B: Usando MySQL Workbench**
1. Descarga MySQL Workbench
2. Crea una nueva conexión con las credenciales de Railway
3. Importa el archivo `.docker/mysql/database/init.sql`

**Opción C: Usando phpMyAdmin online**
1. Ve a https://www.phpmyadmin.co/
2. Conecta con las credenciales de Railway
3. Importa el archivo SQL

## Paso 2: Desplegar Aplicación en Fly.io

### 2.1 Login en Fly.io
```bash
fly auth login
```

### 2.2 Lanzar la aplicación
```bash
fly launch --no-deploy
```

Cuando te pregunte:
- **App name**: josevec-inventory (o el que prefieras)
- **Region**: mia (Miami) o la más cercana
- **Database**: NO (ya tienes Railway)

### 2.3 Configurar variables de entorno con credenciales de Railway

**IMPORTANTE**: Reemplaza con las credenciales que obtuviste de Railway:

```bash
# Credenciales de Railway MySQL
fly secrets set DB_HOST=containers-us-west-xxx.railway.app
fly secrets set DB_PORT=6543
fly secrets set DB_DATABASE=railway
fly secrets set MYSQL_USER=root
fly secrets set MYSQL_PASSWORD=tu_password_de_railway

# Configuración de Django
fly secrets set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
fly secrets set DEBUG=False
fly secrets set ALLOWED_HOSTS=josevec-inventory.fly.dev,*.fly.dev

# (Opcional) API de Gemini para chatbot
fly secrets set GEMINI_API_KEY=tu_api_key_si_la_tienes
```

### 2.4 Desplegar
```bash
fly deploy
```

### 2.5 Abrir la aplicación
```bash
fly open
```

## Paso 3: Verificar

1. **Base de datos en Railway**: https://railway.app/dashboard
2. **Aplicación en Fly.io**: https://josevec-inventory.fly.dev

## Comandos Útiles

### Railway
```bash
# Ver logs de MySQL
railway logs

# Conectar a MySQL
railway connect MySQL

# Variables de entorno
railway variables
```

### Fly.io
```bash
# Ver logs
fly logs

# Estado
fly status

# Reiniciar
fly apps restart

# SSH
fly ssh console

# Ver secretos
fly secrets list
```

## Ventajas de esta configuración

✅ **Base de datos gratis en Railway** (500MB)
✅ **Aplicación gratis en Fly.io** (3 apps, 256MB RAM)
✅ **Backups automáticos** en Railway
✅ **Fácil de escalar**

## Costos

- **Railway MySQL**: Gratis hasta 500MB de almacenamiento
- **Fly.io**: Gratis hasta 3 apps con 256MB RAM c/u

## Solución de Problemas

### Error de conexión a MySQL
```bash
# Verificar que las credenciales sean correctas
fly secrets list

# Verificar que Railway permite conexiones externas
# (Por defecto sí lo permite)
```

### Importar datos de prueba
Si necesitas los usuarios y datos de prueba, importa el SQL completo de `.docker/mysql/database/init.sql`

## URLs Finales

- **GitHub**: https://github.com/JoseVeC15/Inventario
- **Railway Dashboard**: https://railway.app/dashboard
- **Aplicación**: https://tu-app.fly.dev
- **Login**: https://tu-app.fly.dev/login

**Usuarios de prueba:**
- Admin: `admin` / `admin123`
- Vendedor: `jperez` / `vendedor123`
- Almacenero: `mgonzalez` / `almacen123`
