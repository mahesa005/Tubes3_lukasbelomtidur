from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class ApplicantProfile:
    applicant_id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    date_of_birth: Optional[date] = None
    address: str = ""
    phone_number: str = ""

    def validate(self) -> bool:

        # periksa
        # 1.first_name dan last_name tidak boleh kosong
        # 2.date_of_birth (jika diisi) harus berupa date
        # 3.phone_number (jika diisi) hanya mengandung digit atau spasi/dash

        if not self.first_name.strip() or not self.last_name.strip():
            return False

        if self.date_of_birth is not None and not isinstance(self.date_of_birth, date):
            return False

        digits = self.phone_number.replace(" ", "").replace("-", "")
        if self.phone_number and not digits.isdigit():
            return False

        return True

    def to_dict(self) -> dict:
        # ini konversi model ke dictionary sesuai nama kolom di DB
        return {
            "applicant_id":   self.applicant_id,
            "first_name":     self.first_name,
            "last_name":      self.last_name,
            "date_of_birth":  self.date_of_birth,
            "address":        self.address,
            "phone_number":   self.phone_number,
        }


@dataclass
class ApplicationDetail:

    application_id: Optional[int] = None
    applicant_id: int = 0
    application_role: str = ""
    cv_path: str = ""

    def validate(self) -> bool:
        #  periksa
        #  1.applicant_id harus > 0
        #  2.cv_path harus diisi dan berakhiran '.pdf'

        if self.applicant_id <= 0:
            return False
        if not self.cv_path.lower().endswith(".pdf"):
            return False
        return True

    def to_dict(self) -> dict:
        # ini juga sama konversi model ke dictionary sesuai nama kolom di DB
        return {
            "application_id":   self.application_id,
            "applicant_id":     self.applicant_id,
            "application_role": self.application_role,
            "cv_path":          self.cv_path,
        }

class DatabaseSchema:

    CREATE_APPLICANT_PROFILE = """
    CREATE TABLE IF NOT EXISTS ApplicantProfile (
        applicant_id   INT(11)        NOT NULL AUTO_INCREMENT,
        first_name     VARCHAR(50)    NOT NULL,
        last_name      VARCHAR(50)    NOT NULL,
        date_of_birth  DATE            DEFAULT NULL,
        address        VARCHAR(255)    DEFAULT NULL,
        phone_number   VARCHAR(20)     DEFAULT NULL,
        PRIMARY KEY (applicant_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    CREATE_APPLICATION_DETAIL = """
    CREATE TABLE IF NOT EXISTS ApplicationDetail (
        application_id    INT              NOT NULL AUTO_INCREMENT,
        applicant_id      INT              NOT NULL,
        application_role  VARCHAR(100)     DEFAULT NULL,
        cv_path           TEXT             NOT NULL,
        PRIMARY KEY (application_id),
        FOREIGN KEY (applicant_id)
            REFERENCES ApplicantProfile(applicant_id)
            ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
