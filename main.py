import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# Configuración de conexión
config = {
    'user': 'root',  
    'password': '', 
    'host': 'localhost',
    'database': 'CompanyData'
}

def fetch_data(query):
    conn = mysql.connector.connect(**config)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def analyze_data(df):
    # Calcular estadísticas por departamento
    department_stats = df.groupby('department').agg({
        'performance_score': ['mean', 'median', 'std'],
        'salary': ['mean', 'median', 'std'],
        'employee_id': 'count'
    }).rename(columns={'employee_id': 'total_employees'})
    
    # Calcular correlaciones
    correlation_years_performance = df[['years_with_company', 'performance_score']].corr().iloc[0, 1]
    correlation_salary_performance = df[['salary', 'performance_score']].corr().iloc[0, 1]
    
    return department_stats, correlation_years_performance, correlation_salary_performance

def plot_data(df):
    plt.figure(figsize=(12, 8))
    
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
    plt.title('years_with_company vs. performance_score')
    plt.xlabel('Years with Company')
    plt.ylabel('Performance Score')
    
    # Gráfico de dispersión salary vs. performance_score
    plt.subplot(3, 1, 3)
    plt.scatter(df['salary'], df['performance_score'], alpha=0.5)
    plt.title('Salary vs. performance_score')
    plt.xlabel('Salary')
    plt.ylabel('Performance Score')
    
    plt.tight_layout()
    plt.show()

# Consulta SQL
query = "SELECT * FROM EmployeePerformance"

# Obtener datos, analizar y visualizar
df = fetch_data(query)
department_stats, correlation_years_performance, correlation_salary_performance = analyze_data(df)

print("Estadísticas por departamento:")
print(department_stats)
print(f"Correlación entre years_with_company y performance_score: {correlation_years_performance:.2f}")
print(f"Correlación entre salary y performance_score: {correlation_salary_performance:.2f}")

plot_data(df)
