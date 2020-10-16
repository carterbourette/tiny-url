import mysql.connector
import multiprocessing, threading, os

class Database:
    """A thread-safe database adapter for use with the tinyurl database."""
    POOL = {}

    def __new__(cls, *args, **kwargs):
        tid = Database.pool_id()
        
        if tid in Database.POOL:
            return Database.POOL[tid]

        inst = object.__new__(cls, *args, **kwargs)
        Database.POOL[tid] = inst.init()

        return inst


    def __del__(self):
        self.close()


    @staticmethod
    def pool_id():
        return f'{multiprocessing.current_process().pid}.{threading.get_ident()}'


    @staticmethod
    def close_thread_connection():
        tid = Database.pool_id()
        
        if tid in Database.POOL:
            del Database.POOL[tid]


    def _connect(self):
        """Connect to the database."""
        self.conn = mysql.connector.connect(
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )        
        return self

    
    def init(self):
        self.conn, self.cursor = None, None

        return self


    def close(self):
        """Close the database connection."""
        try:
            if self.cursor:
                self.cursor.close()

            if self.conn:
                self.conn.close()
        except: 
            self.init()

    
    def _cursor(self):
        """Create a new cursor"""
        self.conn.autocommit = True
        self.cursor = self.conn.cursor(dictionary=True)


    def _execute(self, sql, args):
        if self.conn is None:
            self._connect()
        
        self._cursor()

        try:
            self.cursor.execute(sql, args)
            return self.cursor
        except:
            self.conn.rollback()
            return None


    @classmethod
    def query(cls, sql, args, get_one=False):
        db = cls() \
            ._execute(sql, args)

        try:
            return db.fetchone() if get_one else db.fetchall()
        except:
            return None if get_one else []


    @classmethod
    def execute(cls, sql, args):
        db = cls() \
            ._execute(sql, args)
        
        return db
