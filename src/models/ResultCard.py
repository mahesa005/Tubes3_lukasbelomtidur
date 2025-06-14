
class ResultCard:
    def __init__(self,
        full_name: str = "",
        cv_path: str = "",
        matched_keywords: dict = None, # key: Word, value: total occurrence
        total_matches: int = 0 # sum of total occurence
    ):
        
        self.full_name = full_name
        self.cv_path = cv_path
        self.matched_keywords = matched_keywords if matched_keywords is not None else {}
        self.total_matches = total_matches

     # how to use
    """
    new_card = ResultCard(
        full_name=name,
        cv_path=path,
        matched_keywords=keywords,
        total_matches=total
    )
    """