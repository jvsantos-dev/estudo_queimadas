from utils.functions import read_yaml
import psycopg2
class PostgreSQL:
    def __init__(self):
        config = read_yaml("D:\\Desktop\\EstudoQueimadas\\postgresql.yaml")
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 5432)
        self.user = config['user']
        self.password = config['password']
        self.database = config['database']

    def connect(self):
        try:
            connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                dbname=self.database
            )
            return connection
        except Exception as e:
            print(f"Error connecting to PostgreSQL database: {e}")
            return None