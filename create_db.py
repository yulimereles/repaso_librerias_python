import mysql.connector
from mysql.connector import errorcode
import random

# Configuración de conexión
config = {
    'user': 'root',  
    'password': '', 
    'host': 'localhost'  
}

def create_database_and_table():
    try:
        # Establecer conexión con el servidor MySQL
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Crear base de datos 'CompanyData' si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS CompanyData")
        
        # Usar la base de datos 'CompanyData'
        cursor.execute("USE CompanyData")

        # Crear tabla 'EmployeePerformance' si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EmployeePerformance (
                id INT AUTO_INCREMENT PRIMARY KEY,  # ID autoincremental como clave primaria
                employee_id INT,  # ID del empleado
                department VARCHAR(255),  # Departamento del empleado
                performance_score DECIMAL(5,2),  # Puntaje de rendimiento del empleado
                years_with_company INT,  # Años con la empresa
                salary DECIMAL(10,2)  # Salario del empleado
            )
        """)

        # Lista de departamentos ficticios
        departments = ['HR', 'Engineering', 'Sales', 'Marketing']
        
        # Poblar la tabla con 1000 registros ficticios
        for _ in range(1000):
            employee_id = random.randint(1000, 9999)  # Generar un ID de empleado aleatorio
            department = random.choice(departments)  # Seleccionar un departamento aleatorio
            performance_score = round(random.uniform(0, 10), 2)  # Generar un puntaje de rendimiento aleatorio
            years_with_company = random.randint(1, 30)  # Generar años con la empresa aleatorios
            salary = round(random.uniform(30000, 120000), 2)  # Generar un salario aleatorio
            
            # Insertar los datos generados en la tabla 'EmployeePerformance'
            cursor.execute("""
                INSERT INTO EmployeePerformance (employee_id, department, performance_score, years_with_company, salary)
                VALUES (%s, %s, %s, %s, %s)
            """, (employee_id, department, performance_score, years_with_company, salary))
        
        # Confirmar los cambios realizados en la base de datos
        conn.commit()
        print("Base de datos y tabla creadas y pobladas con éxito.")
    
    except mysql.connector.Error as err:
        # Manejo de errores comunes de MySQL
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe.")
        elif err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error de autenticación.")
        else:
            print(err)
    finally:
        # Cerrar el cursor y la conexión a la base de datos
        cursor.close()
        conn.close()

# Llamar a la función para crear la base de datos y la tabla, y poblarla con datos ficticios
create_database_and_table()
