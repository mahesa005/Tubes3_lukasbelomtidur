
class SummaryData:
    def __init__(self,
                 full_name: str = "",
                 birth_date: str = "",
                 phone_number: str = "",
                 skills: list = None,  # array of string
                 cv_path: str = "",
                 work_experience: list = None,  # array of string
                 education: list = None):
        self.full_name = full_name
        self.birth_date = birth_date
        self.phone_number = phone_number
        self.skills = skills if skills is not None else []
        self.cv_path = cv_path
        self.work_experience = work_experience if work_experience is not None else []
        self.education = education if education is not None else []

    
