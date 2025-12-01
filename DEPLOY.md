# Guía de Despliegue en Fly.io

## Prerrequisitos

1. **Instalar Fly CLI**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Crear cuenta en Fly.io**
   - Ve a https://fly.io/app/sign-up
   - Registra tu cuenta (gratis para empezar)

## Configurar Base de Datos MySQL

Fly.io no tiene MySQL nativo. Tienes 3 opciones:

### Opción 1: Usar PlanetScale (MySQL gratis)
1. Ve a https://planetscale.com/ y crea una cuenta
2. Crea una base de datos
3. Obtén las credenciales de conexión

### Opción 2: Usar FreeSQLDatabase.com (MySQL gratis)
1. Ve a https://www.freesqldatabase.com/
2. Crea una base de datos gratuita
3. Obtén las credenciales

### Opción 3: Usar Railway o Render para MySQL
1. Crea una base de datos MySQL en Railway.app o Render.com
2. Obtén las credenciales

## Pasos para Desplegar

### 1. Iniciar sesión en Fly.io
```bash
fly auth login
```

### 2. Crear la aplicación (primera vez)
```bash
fly launch --no-deploy
```

Cuando te pregunte:
- **App name**: josevec-inventory (o el que prefieras)
- **Region**: Elige la más cercana (mia = Miami)
- **Database**: NO (usaremos MySQL externo)
- **Deploy now**: NO

### 3. Configurar secretos (variables de entorno)

**IMPORTANTE**: Reemplaza los valores con tus credenciales reales de MySQL:

```bash
# Configuración de base de datos (REEMPLAZA CON TUS DATOS)
fly secrets set DB_HOST=tu-host-mysql.com
fly secrets set DB_PORT=3306
fly secrets set DB_DATABASE=tu_base_datos
fly secrets set MYSQL_USER=tu_usuario
fly secrets set MYSQL_PASSWORD=tu_contraseña_segura

# Configuración de Django
fly secrets set SECRET_KEY=genera-una-clave-secreta-muy-larga-y-aleatoria
fly secrets set DEBUG=False
fly secrets set ALLOWED_HOSTS=josevec-inventory.fly.dev,*.fly.dev

# API de Gemini (opcional, para el chatbot)
fly secrets set GEMINI_API_KEY=tu_api_key_de_gemini
```

**Generar SECRET_KEY seguro**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4. Desplegar la aplicación
```bash
fly deploy
```

### 5. Verificar el despliegue
```bash
fly status
fly logs
```

### 6. Abrir la aplicación
```bash
fly open
```

## Inicializar la Base de Datos

Después del primer despliegue, necesitas crear las tablas:

```bash
# Conectar al contenedor
fly ssh console

# Una vez dentro, ejecutar migraciones
cd /app
python -c "from django.core.management import execute_from_command_line; execute_from_command_line(['manage.py', 'migrate'])"

# Salir
exit
```

**ALTERNATIVA**: Importar el SQL directamente a tu base de datos MySQL externa usando phpMyAdmin o MySQL Workbench.

## Comandos Útiles

```bash
# Ver logs en tiempo real
fly logs

# Reiniciar la app
fly apps restart josevec-inventory

# Ver información de la app
fly status

# Escalar recursos (si necesitas más)
fly scale vm shared-cpu-1x --memory 512

# Ver secretos configurados
fly secrets list

# SSH a la aplicación
fly ssh console

# Destruir la app (cuidado!)
fly apps destroy josevec-inventory
```

## Archivos SQL de Inicialización

Los archivos SQL para crear las tablas están en:
`.docker/mysql/database/init.sql`

Importa este archivo a tu base de datos MySQL externa.

## Dominios Personalizados

Para usar tu propio dominio:

```bash
fly certs add tudominio.com
fly certs add www.tudominio.com
```

Luego configura los DNS:
- A record: @ -> (IP que te dará Fly.io)
- CNAME record: www -> josevec-inventory.fly.dev

## Costos

- **Gratis**: Hasta 3 aplicaciones pequeñas (256MB RAM, shared CPU)
- **Pago**: Si necesitas más recursos o más apps

## Solución de Problemas

### Error de conexión a MySQL
- Verifica que las credenciales sean correctas
- Verifica que el host MySQL permita conexiones externas
- Revisa los logs: `fly logs`

### La aplicación no inicia
```bash
# Ver logs detallados
fly logs

# Verificar secretos
fly secrets list

# Verificar estado
fly status
```

### Cambiar variables de entorno
```bash
fly secrets set NOMBRE_VARIABLE=nuevo_valor
```

## URLs de la Aplicación

Después del despliegue:
- **App**: https://josevec-inventory.fly.dev
- **Panel Admin**: https://josevec-inventory.fly.dev/login/

**Usuarios de prueba**:
- Admin: admin / admin123
- Vendedor: jperez / vendedor123
