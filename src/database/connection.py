"""
Manajemen Koneksi Database
Tujuan: Mengelola koneksi dan operasi database MySQL
"""

import mysql.connector
from mysql.connector import Error
import logging

# Ganti import ini agar mengimpor config.py yang ada di root proyek
from config import DATABASE_CONFIG

# Setting sederhana untuk logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    # Jika belum ada handler, tambahkan satu handler default
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)  # Anda bisa ubah ke DEBUG jika perlu detail


class DatabaseConnection:
    """
    Manajer koneksi database MySQL

    TODO:
    - Implementasi connection pooling
    - Tambahkan dukungan transaksi
    - Tangani error koneksi dengan baik
    - Implementasi logika rekoneksi
    """

    def __init__(self):
        """Inisialisasi koneksi database"""
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Membuka koneksi ke database

        Returns:
            bool: True jika koneksi berhasil, False jika gagal
        """
        try:
            # Gunakan konfigurasi dari config.py
            cfg = DATABASE_CONFIG
            self.connection = mysql.connector.connect(
                host=cfg['host'],
                user=cfg['user'],
                password=cfg['password'],
                database=cfg['database'],
                port=cfg.get('port', 3306)
            )
            self.cursor = self.connection.cursor(buffered=True)
            logger.info("Koneksi ke database MySQL berhasil.")
            return True
        except Error as e:
            logger.error(f"Gagal terkoneksi ke MySQL: {e}")
            return False

    def disconnect(self):
        """
        Menutup koneksi database

        TODO:
        - Tutup cursor dan koneksi
        - Tangani error saat cleanup
        """
        try:
            if self.cursor:
                self.cursor.close()
                logger.info("Cursor database ditutup.")
            if self.connection:
                self.connection.close()
                logger.info("Koneksi database ditutup.")
        except Error as e:
            logger.error(f"Error saat menutup koneksi database: {e}")

    def execute(self, query, params=None):
        """
        Menjalankan query SQL

        Args:
            query (str): Query SQL yang akan dijalankan
            params (tuple): Parameter query

        Returns:
            bool: True jika berhasil, False jika gagal
        """
        if self.connection is None or self.cursor is None:
            logger.warning("Belum terkoneksi. Memanggil connect().")
            if not self.connect():
                return False

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            # Jika query-nya INSERT/UPDATE/DELETE, commit agar perubahan disimpan
            if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER")):
                self.connection.commit()
            logger.debug(f"Eksekusi query berhasil: {query} | params: {params}")
            return True
        except Error as e:
            logger.error(f"Gagal menjalankan query: {query}\nError: {e}")
            return False

    def fetchOne(self, query, params=None):
        """
        Menjalankan query dan mengambil satu hasil

        Args:
            query (str): Query SQL
            params (tuple): Parameter query

        Returns:
            tuple: Hasil query atau None
        """
        if self.connection is None or self.cursor is None:
            logger.warning("Belum terkoneksi. Memanggil connect().")
            if not self.connect():
                return None

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            result = self.cursor.fetchone()
            logger.debug(f"fetchOne: {query} | params: {params} → {result}")
            return result
        except Error as e:
            logger.error(f"fetchOne gagal untuk query: {query}\nError: {e}")
            return None

    def fetchAll(self, query, params=None):
        """
        Menjalankan query dan mengambil semua hasil

        Args:
            query (str): Query SQL
            params (tuple): Parameter query

        Returns:
            list: Daftar hasil query (bisa kosong)
        """
        if self.connection is None or self.cursor is None:
            logger.warning("Belum terkoneksi. Memanggil connect().")
            if not self.connect():
                return []

        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            results = self.cursor.fetchall()
            logger.debug(f"fetchAll: {query} | params: {params} → {len(results)} baris")
            return results
        except Error as e:
            logger.error(f"fetchAll gagal untuk query: {query}\nError: {e}")
            return []

    def createTables(self):
        """
        Membuat tabel database jika belum ada

        TODO:
        - Jalankan perintah CREATE TABLE
        - Tangani error pembuatan tabel
        - Buat index
        """
        # Contoh struktur tabel untuk ApplicantProfile dan ApplicationDetail.
        # Sesuaikan nama kolom maupun tipe data jika di seed.py ada definisi berbeda.
        table_statements = [
            """
            CREATE TABLE IF NOT EXISTS ApplicantProfile (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                phone VARCHAR(50),
                resume_path VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            """
            CREATE TABLE IF NOT EXISTS ApplicationDetail (
                id INT AUTO_INCREMENT PRIMARY KEY,
                applicant_id INT NOT NULL,
                keyword VARCHAR(255) NOT NULL,
                match_count INT DEFAULT 0,
                similarity_score FLOAT DEFAULT 0,
                FOREIGN KEY (applicant_id) REFERENCES ApplicantProfile(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
            # Tambahkan lebih banyak CREATE TABLE jika perlu
        ]

        # Pastikan terkoneksi sebelum membuat tabel
        if self.connection is None or self.cursor is None:
            if not self.connect():
                return

        for stmt in table_statements:
            try:
                self.cursor.execute(stmt)
                logger.info("Berhasil menjalankan: \n" + stmt.strip())
            except Error as e:
                logger.error(f"Gagal membuat/mengupdate tabel: {e}")

        # Commit sekali lagi jika ada perubahan
        try:
            self.connection.commit()
        except Error as e:
            logger.error(f"Gagal commit setelah createTables: {e}")
