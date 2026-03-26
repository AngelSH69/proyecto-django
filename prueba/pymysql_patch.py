import pymysql

# Parchear la versión de pymysql para que parezca más reciente
pymysql.version_info = (2, 2, 4, 'final', 0)
pymysql.__version__ = '2.2.4'

# Instalar el parche
pymysql.install_as_MySQLdb()
print("✅ pymysql parcheado correctamente como MySQLdb versión 2.2.4")