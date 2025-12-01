# Guía de Despliegue en Fly.io desde GitHub

## Pasos Rápidos

### 1. Subir el proyecto a GitHub

```bash
# Inicializar repositorio Git (si no está inicializado)
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Preparar proyecto para despliegue en Fly.io"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
git branch -M main
git push -u origin main
```

### 2. Configurar Base de Datos MySQL Externa

**Opción Recomendada: PlanetScale (Gratis)**
1. Ve a https://planetscale.com
2. Crea una cuenta
3. Crea una nueva base de datos
4. Ve a "Connect" → "Django" para obtener las credenciales
5. Guarda: HOST, DATABASE, USER, PASSWORD

**Alternativa: FreeSQLDatabase.com**
1. Ve a https://www.freesqldatabase.com
2. Crea una base de datos gratuita
3. Guarda las credenciales que te envían por email

### 3. Importar el Schema de la Base de Datos

```bash
# Conectarte a tu MySQL externo y ejecutar el SQL
# El archivo SQL está en: .docker/mysql/database/init.sql
```

Usando MySQL Workbench, phpMyAdmin o comando:
```bash
mysql -h TU_HOST -u TU_USER -p TU_DATABASE < .docker/mysql/database/init.sql
```

### 4. Desplegar en Fly.io desde GitHub

```bash
# Login en Fly.io
fly auth login

# Crear app (sin desplegar aún)
fly launch --no-deploy

# Configurar secretos (IMPORTANTE: usa tus credenciales reales)
fly secrets set DB_HOST=tu-mysql-host.com
fly secrets set DB_PORT=3306
fly secrets set DB_DATABASE=tu_base_datos
fly secrets set MYSQL_USER=tu_usuario
fly secrets set MYSQL_PASSWORD=tu_password_segura

# Generar y configurar SECRET_KEY
fly secrets set SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")

# Configurar Django
fly secrets set DEBUG=False
fly secrets set ALLOWED_HOSTS=tu-app.fly.dev,*.fly.dev

# (Opcional) API de Gemini para chatbot
fly secrets set GEMINI_API_KEY=tu_api_key

# Desplegar
fly deploy

# Abrir la app
fly open
```

### 5. Conectar Fly.io con GitHub (Auto-deploy)

Fly.io puede desplegarse automáticamente cuando hagas push a GitHub:

```bash
# Configurar GitHub Actions
fly config save

# Esto creará un workflow en .github/workflows/fly.yml
```

**O usar Fly.io GitHub Integration:**
1. Ve a https://fly.io/dashboard
2. Selecciona tu app
3. Settings → GitHub Integration
4. Conecta tu repositorio
5. Cada push a `main` desplegará automáticamente

## Comandos Útiles Post-Despliegue

```bash
# Ver logs
fly logs

# Estado de la app
fly status

# Reiniciar
fly apps restart

# SSH a la app
fly ssh console

# Ver secretos configurados
fly secrets list
```

## Actualizar el Proyecto

```bash
# En tu repositorio local
git add .
git commit -m "Descripción de cambios"
git push

# Fly.io se actualizará automáticamente si configuraste GitHub Actions
# O manualmente:
fly deploy
```

## URLs Finales

- **Aplicación**: https://tu-app.fly.dev
- **Login**: https://tu-app.fly.dev/login

**Usuarios de prueba:**
- Admin: `admin` / `admin123`
- Vendedor: `jperez` / `vendedor123`
