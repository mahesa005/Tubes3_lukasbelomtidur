import mysql.connector
from mysql.connector import Error
import logging
from config import DATABASE_CONFIG
from .models import DatabaseSchema 

logger = logging.getLogger(__name__)
if not logger.handlers:
    h = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    h.setFormatter(fmt)
    logger.addHandler(h)
    logger.setLevel(logging.INFO)


class DatabaseConnection:
    def __init__(self):
        """Inisialisasi koneksi database"""
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host     = DATABASE_CONFIG['host'],
                user     = DATABASE_CONFIG['user'],
                password = DATABASE_CONFIG['password'],
                database = DATABASE_CONFIG['database'],
                port     = DATABASE_CONFIG['port']
            )
            self.cursor = self.connection.cursor(buffered=True)
            logger.info("Koneksi ke database berhasil.")
            return True
        except Error as e:
            logger.error(f"Gagal terkoneksi ke MySQL: {e}")
            return False

    def disconnect(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info("Koneksi database ditutup.")
        except Error as e:
            logger.error(f"Error saat menutup koneksi: {e}")

    def execute(self, query, params=None):
        if self.connection is None or self.cursor is None:
            if not self.connect():
                return False
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            # jika query ubah data, commit perubahan
            if query.strip().upper().startswith(
                ("INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER", "TRUNCATE")
            ):
                self.connection.commit()
            return True
        except Error as e:
            logger.error(f"Gagal menjalankan query:\n{query}\nError: {e}")
            return False

    def fetchOne(self, query, params=None):
        if self.connection is None or self.cursor is None:
            if not self.connect():
                return None
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except Error as e:
            logger.error(f"fetchOne gagal: {e}")
            return None

    def fetchAll(self, query, params=None):
        if self.connection is None or self.cursor is None:
            if not self.connect():
                return []
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
            logger.error(f"fetchAll gagal: {e}")
            return []

    def createTables(self):
        # ambil perintah create tabel dari DatabaseSchema
        statements = [
            DatabaseSchema.CREATE_APPLICANT_PROFILE,
            DatabaseSchema.CREATE_APPLICATION_DETAIL
        ]

        # ini pastiin koneksi dibuka
        if self.connection is None or self.cursor is None:
            if not self.connect():
                return

        for stmt in statements:
            try:
                self.cursor.execute(stmt)
                logger.info("Berhasil menjalankan create query:\n" + stmt.strip())
            except Error as e:
                logger.error(f"Gagal menciptakan/memperbarui tabel: {e}\nQuery:\n{stmt}")

        try:
            self.connection.commit()
        except Error as e:
            logger.error(f"Gagal commit setelah createTables: {e}")
        finally:
            self.disconnect()
    
    def createDatabase(self, db_name: str) -> bool:
        # koneksi tanpa database dulu
        try:
            tmp_conn = mysql.connector.connect(
                host     = DATABASE_CONFIG['host'],
                user     = DATABASE_CONFIG['user'],
                password = DATABASE_CONFIG['password'],
                port     = DATABASE_CONFIG['port']
            )
            tmp_cursor = tmp_conn.cursor()
            tmp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            tmp_conn.commit()
            tmp_cursor.close()
            tmp_conn.close()
            logger.info(f"Database `{db_name}` berhasil dibuat atau sudah ada.")
            return True
        except Error as e:
            logger.error(f"createDatabase error: {e}")
            return False

    def useDatabase(self, db_name: str) -> bool:
        if self.connection is None or self.cursor is None:
            if not self.connect():
                return False
        try:
            self.cursor.execute(f"USE `{db_name}`;")
            logger.info(f"Switched to database `{db_name}`.")
            return True
        except Error as e:
            logger.error(f"useDatabase error: {e}")
            return False
    
    def dropDatabase(self, db_name: str) -> bool:
        from mysql.connector import connect, Error

        try:
            # koneksi sementara tanpa pilih database
            tmp = connect(
                host     = DATABASE_CONFIG['host'],
                user     = DATABASE_CONFIG['user'],
                password = DATABASE_CONFIG['password'],
                port     = DATABASE_CONFIG['port']
            )
            cur = tmp.cursor()
            cur.execute(f"DROP DATABASE IF EXISTS `{db_name}`;")
            tmp.commit()
            cur.close()
            tmp.close()
            logger.info(f"Database `{db_name}` berhasil di-drop (jika ada).")
            return True
        except Error as e:
            logger.error(f"dropDatabase error: {e}")
            return False
