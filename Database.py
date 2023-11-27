import mysql.connector


config = {
    'user': 'root',
    'password': 'root_password',
    'host': 'localhost',
    'port': 3306,
    'database': 'musicDatabase',
}
connection = mysql.connector.connect(**config)

cursor = connection.cursor()