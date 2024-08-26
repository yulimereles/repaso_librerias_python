import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import random
import matplotlib.pyplot as plt

# Clase base para manejar la conexión a la base de datos
class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.conn = None
    
    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Error de autenticación.")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de datos no existe.")
            else:
                print(err)
            self.conn = None
    
    def close(self):
        if self.conn:
            self.conn.close()

# Clase para manejar la creación y población de la base de datos
class EmployeeDatabase(DatabaseManager):
    def create_database_and_table(self):
        if not self.conn:
            self.connect()
        
        cursor = self.conn.cursor()
        try:
            cursor.execute("CREATE DATABASE IF NOT EXISTS CompanyData")
            cursor.execute("USE CompanyData")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS EmployeePerformance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    employee_id INT,
                    department VARCHAR(255),
                    performance_score DECIMAL(5,2),
                    years_with_company INT,
                    salary DECIMAL(10,2)
                )
            """)
            self.populate_table(cursor)
            self.conn.commit()
            print("Base de datos y tabla creadas y pobladas con éxito.")
        except mysql.connector.Error as err:
            print(err)
        finally:
            cursor.close()

    def populate_table(self, cursor):
        departments = ['HR', 'Engineering', 'Sales', 'Marketing']
        for _ in range(1000):
            employee_id = random.randint(1000, 9999)
            department = random.choice(departments)
            performance_score = round(random.uniform(0, 10), 2)
            years_with_company = random.randint(1, 30)
            salary = round(random.uniform(30000, 120000), 2)
            cursor.execute("""
                INSERT INTO EmployeePerformance (employee_id, department, performance_score, years_with_company, salary)
                VALUES (%s, %s, %s, %s, %s)
            """, (employee_id, department, performance_score, years_with_company, salary))

# Clase para manejar el análisis y visualización de datos
class DataAnalyzer:
    def __init__(self, connection):
        self.connection = connection
    
    def fetch_data(self, query):
        if self.connection.conn:
            df = pd.read_sql(query, self.connection.conn)
            return df
        else:
            raise ConnectionError("La conexión a la base de datos no está disponible.")
    
    def analyze_data(self, df):
        department_stats = df.groupby('department').agg({
            'performance_score': ['mean', 'median', 'std'],
            'salary': ['mean', 'median', 'std'],
            'employee_id': 'count'
        }).rename(columns={'employee_id': 'total_employees'})
        
        correlation_years_performance = df[['years_with_company', 'performance_score']].corr().iloc[0, 1]
        correlation_salary_performance = df[['salary', 'performance_score']].corr().iloc[0, 1]
        
        return department_stats, correlation_years_performance, correlation_salary_performance

    def plot_data(self, df):
        plt.figure(figsize=(12, 12))
        
        # Histograma del performance_score por departamento
        plt.subplot(3, 1, 1)
        for department in df['department'].unique():
            department_data = df[df['department'] == department]
            plt.hist(department_data['performance_score'], bins=20, alpha=0.5, label=department)
        plt.title('Histograma del performance_score por Departamento')
        plt.xlabel('Performance Score')
        plt.ylabel('Frecuencia')
        plt.legend()
        
        # Gráfico de dispersión years_with_company vs. performance_score
        plt.subplot(3, 1, 2)
        plt.scatter(df['years_with_company'], df['performance_score'], alpha=0.5)
        plt.title('Years with Company vs. Performance Score')
        plt.xlabel('Years with Company')
        plt.ylabel('Performance Score')
        
        # Gráfico de dispersión salary vs. performance_score
        plt.subplot(3, 1, 3)
        plt.scatter(df['salary'], df['performance_score'], alpha=0.5)
        plt.title('Salary vs. Performance Score')
        plt.xlabel('Salary')
        plt.ylabel('Performance Score')
        
        plt.tight_layout()
        plt.show()

# Configuración de la base de datos
db_config = {
    'user': 'root',  
    'password': '', 
    'host': 'localhost', 
    'database': 'CompanyData'
}

# Crear y poblar la base de datos
db_manager = EmployeeDatabase(config=db_config)
db_manager.connect()
db_manager.create_database_and_table()

# Analizar los datos
data_analyzer = DataAnalyzer(connection=db_manager)
query = "SELECT * FROM EmployeePerformance"

try:
    df = data_analyzer.fetch_data(query)
    department_stats, correlation_years_performance, correlation_salary_performance = data_analyzer.analyze_data(df)

    print("Estadísticas por departamento:")
    print(department_stats)
    print(f"Correlación entre years_with_company y performance_score: {correlation_years_performance:.2f}")
    print(f"Correlación entre salary y performance_score: {correlation_salary_performance:.2f}")

    data_analyzer.plot_data(df)
except ConnectionError as e:
    print(e)
finally:
    db_manager.close()
