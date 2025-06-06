
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
    """
    Manajer koneksi database MySQL
    """

    def __init__(self):
        """Inisialisasi koneksi database"""
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Membuka koneksi ke database menggunakan konfigurasi di DATABASE_CONFIG

        Returns:
            bool: True jika koneksi berhasil, False jika gagal

        TODO:
        - Implementasi connection pooling (nanti)
        - Atur timeout reconnect (nanti)
        """
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
        """
        Menutup koneksi database

        TODO:
        - Tangani error saat cleanup (misal jika cursor sudah tertutup)
        """
        try:
            if self.cursor:
                self.cursor.close()
                logger.info("Cursor ditutup.")
            if self.connection:
                self.connection.close()
                logger.info("Koneksi database ditutup.")
        except Error as e:
            logger.error(f"Error saat menutup koneksi: {e}")

    def execute(self, query, params=None):
        """
        Menjalankan query SQL

        Args:
            query (str): Query SQL yang akan dijalankan
            params (tuple): Parameter query

        Returns:
            bool: True jika berhasil, False jika gagal

        TODO:
        - Logging lebih detail (levels)
        - Tangani deadlock / retry jika perlu
        """
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
        """
        Menjalankan query SELECT dan mengambil satu hasil

        Args:
            query (str): Query SQL
            params (tuple): Parameter query

        Returns:
            tuple: Hasil query atau None

        TODO:
        - Tangani kasus timeout atau reconnect otomatis
        """
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
        """
        Menjalankan query SELECT dan mengambil semua hasil

        Args:
            query (str): Query SQL
            params (tuple): Parameter query

        Returns:
            list: Daftar hasil query

        TODO:
        - Support paginasi di query besar
        """
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
        """
        Membuat tabel database jika belum ada, berdasarkan skema di DatabaseSchema.

        TODO:
        - Tambahkan pembuatan index setelah tabel dibuat (misal index di email, status)
        - Tangani migration (versi skema) jika struktur berubah ke depan
        """
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
