from config.database import Database

class Config:
    """Modelo para la configuración del sistema"""
    
    @staticmethod
    def get_user_info(user_id):
        """Obtiene información completa del usuario"""
        query = """
            SELECT 
                u.id,
                u.username,
                u.nombre_completo,
                u.email,
                u.activo,
                u.created_at,
                r.nombre as rol
            FROM JoseVeC.usuarios u
            INNER JOIN JoseVeC.roles r ON u.rol_id = r.id
            WHERE u.id = %s
        """
        result = Database.execute_query(query, (user_id,))
        return result[0] if result else None
    
    @staticmethod
    def get_system_stats():
        """Obtiene estadísticas generales del sistema"""
        query = """
            SELECT 
                (SELECT COUNT(*) FROM JoseVeC.usuarios WHERE activo = 1) as total_usuarios,
                (SELECT COUNT(*) FROM JoseVeC.productos WHERE activo = 1) as total_productos,
                (SELECT COUNT(*) FROM JoseVeC.categorias WHERE activo = 1) as total_categorias,
                (SELECT COUNT(*) FROM JoseVeC.clientes WHERE activo = 1) as total_clientes,
                (SELECT COUNT(*) FROM JoseVeC.proveedores WHERE activo = 1) as total_proveedores,
                (SELECT COUNT(*) FROM JoseVeC.ventas) as total_ventas,
                (SELECT COUNT(*) FROM JoseVeC.compras) as total_compras
        """
        result = Database.execute_query(query)
        return result[0] if result else {}
    
    @staticmethod
    def get_all_users(include_superadmin=False):
        """Obtiene todos los usuarios del sistema"""
        where_clause = "" if include_superadmin else "WHERE u.username != 'superadmin'"
        
        query = f"""
            SELECT 
                u.id,
                u.username,
                u.nombre_completo,
                u.email,
                u.activo,
                r.nombre as rol
            FROM JoseVeC.usuarios u
            INNER JOIN JoseVeC.roles r ON u.rol_id = r.id
            {where_clause}
            ORDER BY u.created_at DESC
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_database_info():
        """Obtiene información de la base de datos"""
        query = """
            SELECT 
                TABLE_NAME as table_name,
                TABLE_ROWS as table_rows,
                ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS size_mb
            FROM information_schema.tables
            WHERE table_schema = 'JoseVeC'
            AND TABLE_NAME NOT LIKE 'django_%%'
            ORDER BY TABLE_ROWS DESC
        """
        return Database.execute_query(query)
    
    @staticmethod
    def get_user_by_id(user_id):
        """Obtiene un usuario por ID"""
        query = """
            SELECT 
                u.id,
                u.username,
                u.nombre_completo,
                u.email,
                u.rol_id,
                u.activo
            FROM JoseVeC.usuarios u
            WHERE u.id = %s
        """
        result = Database.execute_query(query, (user_id,))
        return result[0] if result else None
    
    @staticmethod
    def create_user(data):
        """Crea un nuevo usuario"""
        query = """
            INSERT INTO JoseVeC.usuarios 
            (username, password, nombre_completo, email, rol_id, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            data['username'],
            data['password'],
            data['nombre_completo'],
            data.get('email', ''),
            data['rol_id'],
            data.get('activo', 1)
        )
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def update_user(user_id, data):
        """Actualiza un usuario existente"""
        query = """
            UPDATE JoseVeC.usuarios 
            SET username = %s,
                nombre_completo = %s,
                email = %s,
                rol_id = %s,
                activo = %s
            WHERE id = %s
        """
        params = (
            data['username'],
            data['nombre_completo'],
            data.get('email', ''),
            data['rol_id'],
            data.get('activo', 1),
            user_id
        )
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def delete_user(user_id):
        """Desactiva un usuario (soft delete)"""
        query = "UPDATE JoseVeC.usuarios SET activo = 0 WHERE id = %s"
        return Database.execute_query(query, (user_id,), fetch=False)
    
    @staticmethod
    def get_roles():
        """Obtiene todos los roles disponibles"""
        query = "SELECT id, nombre FROM JoseVeC.roles ORDER BY nombre"
        return Database.execute_query(query)
    
    @staticmethod
    def update_profile(user_id, data):
        """Actualiza el perfil del usuario actual"""
        # Construir query dinámicamente según los campos disponibles
        fields = ['nombre_completo = %s', 'email = %s']
        params = [data['nombre_completo'], data.get('email', '')]
        
        # Solo actualizar activo si está en data (es administrador)
        if 'activo' in data:
            fields.append('activo = %s')
            params.append(data['activo'])
        
        params.append(user_id)
        
        query = f"""
            UPDATE JoseVeC.usuarios 
            SET {', '.join(fields)}
            WHERE id = %s
        """
        
        return Database.execute_query(query, params, fetch=False)
    
    @staticmethod
    def change_password(user_id, new_password):
        """Cambia la contraseña del usuario actual"""
        query = """
            UPDATE JoseVeC.usuarios 
            SET password = %s
            WHERE id = %s
        """
        return Database.execute_query(query, (new_password, user_id), fetch=False)

