from .connection import DatabaseConnection
from .models import ApplicantProfile, ApplicationDetail
import logging

class DatabaseQueries:
    def __init__(self):
        # nisialisasi database queries
        self.db = DatabaseConnection()
        self.logger = logging.getLogger(__name__)

    # untuk ApplicantProfile

    def insertApplicant(self, applicant: ApplicantProfile) -> int:
        if not self.db.connect():
            self.logger.error("insertApplicant: Gagal koneksi.")
            return None

        sql = """
            INSERT INTO ApplicantProfile
              (first_name, last_name, date_of_birth, address, phone_number)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            applicant.first_name,
            applicant.last_name,
            applicant.date_of_birth,
            applicant.address,
            applicant.phone_number,
        )

        success = self.db.execute(sql, params)
        if not success:
            self.logger.error("insertApplicant: Gagal menjalankan INSERT.")
            self.db.disconnect()
            return None

        new_id = self.db.cursor.lastrowid
        self.db.disconnect()
        return new_id

    def getApplicantById(self, applicantId: int) -> ApplicantProfile:
        if not self.db.connect():
            self.logger.error("getApplicantById: Gagal koneksi.")
            return None

        sql = """
            SELECT applicant_id, first_name, last_name, date_of_birth, address, phone_number
            FROM ApplicantProfile
            WHERE applicant_id = %s
        """
        row = self.db.fetchOne(sql, (applicantId,))
        self.db.disconnect()

        if not row:
            return None

        return ApplicantProfile(
            applicant_id=row[0],
            first_name=row[1] or "",
            last_name=row[2] or "",
            date_of_birth=row[3],
            address=row[4] or "",
            phone_number=row[5] or ""
        )

    def getAllApplicants(self) -> list:
        if not self.db.connect():
            self.logger.error("getAllApplicants: Gagal koneksi.")
            return []

        sql = """
            SELECT applicant_id, first_name, last_name, date_of_birth, address, phone_number
            FROM ApplicantProfile
            ORDER BY applicant_id
        """
        rows = self.db.fetchAll(sql)
        self.db.disconnect()

        result = []
        for row in rows:
            result.append(ApplicantProfile(
                applicant_id=row[0],
                first_name=row[1] or "",
                last_name=row[2] or "",
                date_of_birth=row[3],
                address=row[4] or "",
                phone_number=row[5] or ""
            ))
        return result

    def updateApplicant(self, applicant: ApplicantProfile) -> bool:
        if applicant.applicant_id is None:
            self.logger.error("updateApplicant: applicant_id tidak boleh None.")
            return False

        if not self.db.connect():
            self.logger.error("updateApplicant: Gagal koneksi.")
            return False

        sql = """
            UPDATE ApplicantProfile
            SET first_name = %s,
                last_name = %s,
                date_of_birth = %s,
                address = %s,
                phone_number = %s
            WHERE applicant_id = %s
        """
        params = (
            applicant.first_name,
            applicant.last_name,
            applicant.date_of_birth,
            applicant.address,
            applicant.phone_number,
            applicant.applicant_id
        )

        success = self.db.execute(sql, params)
        self.db.disconnect()
        return success

    def deleteApplicant(self, applicantId: int) -> bool:
        if not self.db.connect():
            self.logger.error("deleteApplicant: Gagal koneksi.")
            return False

        sql = "DELETE FROM ApplicantProfile WHERE applicant_id = %s"
        success = self.db.execute(sql, (applicantId,))
        self.db.disconnect()
        return success


    #  dibawah ini untuk ApplicationDetail

    def insertApplication(self, application: ApplicationDetail) -> int:
        if not self.db.connect():
            self.logger.error("insertApplication: Gagal koneksi.")
            return None

        sql = """
            INSERT INTO ApplicationDetail
              (applicant_id, application_role, cv_path)
            VALUES (%s, %s, %s)
        """
        params = (
            application.applicant_id,
            application.application_role,
            application.cv_path
        )

        success = self.db.execute(sql, params)
        if not success:
            self.logger.error("insertApplication: Gagal menjalankan INSERT.")
            self.db.disconnect()
            return None

        new_id = self.db.cursor.lastrowid
        self.db.disconnect()
        return new_id

    def getApplicationById(self, applicationId: int) -> ApplicationDetail:
        if not self.db.connect():
            self.logger.error("getApplicationById: Gagal koneksi.")
            return None

        sql = """
            SELECT application_id, applicant_id, application_role, cv_path
            FROM ApplicationDetail
            WHERE application_id = %s
        """
        row = self.db.fetchOne(sql, (applicationId,))
        self.db.disconnect()

        if not row:
            return None

        return ApplicationDetail(
            application_id=row[0],
            applicant_id=row[1],
            application_role=row[2] or "",
            cv_path=row[3] or ""
        )

    def getApplicationsByApplicant(self, applicantId: int) -> list:
        if not self.db.connect():
            self.logger.error("getApplicationsByApplicant: Gagal koneksi.")
            return []

        sql = """
            SELECT application_id, applicant_id, application_role, cv_path
            FROM ApplicationDetail
            WHERE applicant_id = %s
            ORDER BY application_id
        """
        rows = self.db.fetchAll(sql, (applicantId,))
        self.db.disconnect()

        result = []
        for row in rows:
            result.append(ApplicationDetail(
                application_id=row[0],
                applicant_id=row[1],
                application_role=row[2] or "",
                cv_path=row[3] or ""
            ))
        return result

    def getAllApplications(self) -> list:
        if not self.db.connect():
            self.logger.error("getAllApplications: Gagal koneksi.")
            return []

        sql = """
            SELECT
              d.application_id,
              d.applicant_id,
              d.application_role,
              d.cv_path,
              a.first_name,
              a.last_name,
              a.date_of_birth,
              a.address,
              a.phone_number
            FROM ApplicationDetail AS d
            JOIN ApplicantProfile AS a
              ON d.applicant_id = a.applicant_id
            ORDER BY d.application_id
        """
        rows = self.db.fetchAll(sql)
        self.db.disconnect()

        result = []
        for row in rows:
            detail = ApplicationDetail(
                application_id=row[0],
                applicant_id=row[1],
                application_role=row[2] or "",
                cv_path=row[3] or ""
            )
            profile = ApplicantProfile(
                applicant_id=row[1],
                first_name=row[4] or "",
                last_name=row[5] or "",
                date_of_birth=row[6],
                address=row[7] or "",
                phone_number=row[8] or ""
            )
            result.append((detail, profile))
        return result

    def updateApplication(self, application: ApplicationDetail) -> bool:
        if application.application_id is None:
            self.logger.error("updateApplication: application_id tidak boleh None.")
            return False

        if not self.db.connect():
            self.logger.error("updateApplication: Gagal koneksi.")
            return False

        sql = """
            UPDATE ApplicationDetail
            SET application_role = %s,
                cv_path = %s
            WHERE application_id = %s
        """
        params = (
            application.application_role,
            application.cv_path,
            application.application_id
        )

        success = self.db.execute(sql, params)
        self.db.disconnect()
        return success

    def searchApplicationsByKeywords(self, keywords: list) -> list:
        if not self.db.connect():
            self.logger.error("searchApplicationsByKeywords: Gagal koneksi.")
            return []

        like_clauses = []
        params = []
        for kw in keywords:
            pattern = f"%{kw}%"
            like_clauses.append("(cv_path LIKE %s OR application_role LIKE %s)")
            params.extend([pattern, pattern])

        where_clause = " OR ".join(like_clauses)
        sql = f"""
            SELECT application_id, applicant_id, application_role, cv_path
            FROM ApplicationDetail
            WHERE {where_clause}
            ORDER BY application_id
        """
        rows = self.db.fetchAll(sql, tuple(params))
        self.db.disconnect()

        result = []
        for row in rows:
            result.append(ApplicationDetail(
                application_id=row[0],
                applicant_id=row[1],
                application_role=row[2] or "",
                cv_path=row[3] or ""
            ))
        return result

    def getApplicationsForProcessing(self) -> list:
        if not self.db.connect():
            self.logger.error("getApplicationsForProcessing: Gagal koneksi.")
            return []

        sql = """
            SELECT application_id, applicant_id, application_role, cv_path
            FROM ApplicationDetail
            ORDER BY application_id
        """
        rows = self.db.fetchAll(sql)
        self.db.disconnect()

        result = []
        for row in rows:
            result.append(ApplicationDetail(
                application_id=row[0],
                applicant_id=row[1],
                application_role=row[2] or "",
                cv_path=row[3] or ""
            ))
        return result
