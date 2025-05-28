# ===== src/utils/helpers.py =====
"""
Fungsi Helper dan Utilitas
Tujuan: Fungsi-fungsi helper yang digunakan di berbagai bagian
"""

import re
import time
from datetime import datetime
import hashlib

def formatExecutionTime(timeInSeconds):
    """
    Format waktu eksekusi untuk ditampilkan
    
    Args:
        timeInSeconds (float): Waktu dalam detik
        
    Returns:
        str: Formatted time string
    """
    if timeInSeconds < 1:
        return f"{timeInSeconds * 1000:.2f}ms"
    else:
        return f"{timeInSeconds:.2f}s"

def cleanText(text):
    """
    Bersihkan teks dari karakter yang tidak diinginkan
    
    Args:
        text (str): Raw text
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.,;:!?()-]', '', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def normalizeKeyword(keyword):
    """
    Normalize keyword untuk pencarian
    
    Args:
        keyword (str): Raw keyword
        
    Returns:
        str: Normalized keyword
    """
    return keyword.strip().lower()

def parseKeywords(keywordString):
    """
    Parse string keywords yang dipisahkan koma
    
    Args:
        keywordString (str): String keywords separated by comma
        
    Returns:
        list: List of normalized keywords
    """
    if not keywordString:
        return []
    
    keywords = [normalizeKeyword(kw) for kw in keywordString.split(',')]
    return [kw for kw in keywords if kw]  # Remove empty strings

def calculateMatchScore(totalKeywords, matchedKeywords, keywordFrequencies):
    """
    Hitung skor match berdasarkan keyword yang ditemukan
    
    Args:
        totalKeywords (int): Total jumlah keyword yang dicari
        matchedKeywords (int): Jumlah keyword yang ditemukan
        keywordFrequencies (dict): Dictionary frekuensi setiap keyword
        
    Returns:
        float: Match score (0.0 to 1.0)
    """
    if totalKeywords == 0:
        return 0.0
    
    # Base score berdasarkan coverage
    baseScore = matchedKeywords / totalKeywords
    
    # Bonus berdasarkan frekuensi
    totalFrequency = sum(keywordFrequencies.values())
    frequencyBonus = min(totalFrequency / (totalKeywords * 10), 0.5)  # Max 0.5 bonus
    
    return min(baseScore + frequencyBonus, 1.0)

def generateHash(text):
    """
    Generate hash untuk teks (useful untuk caching)
    
    Args:
        text (str): Text to hash
        
    Returns:
        str: SHA256 hash
    """
    return hashlib.sha256(text.encode()).hexdigest()

def validateEmail(email):
    """
    Validasi format email
    
    Args:
        email (str): Email address
        
    Returns:
        bool: True jika format email valid
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    return re.match(pattern, email) is not None

def validatePhone(phone):
    """
    Validasi format nomor telepon
    
    Args:
        phone (str): Phone number
        
    Returns:
        bool: True jika format nomor telepon valid
    """
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    # Check if length is reasonable (10-15 digits)
    return 10 <= len(digits) <= 15

class Timer:
    """Context manager untuk mengukur waktu eksekusi"""
    
    def __init__(self):
        self.startTime = None
        self.endTime = None
    
    def __enter__(self):
        self.startTime = time.time()
        return self
    
    def __exit__(self, excType, excVal, excTb):
        self.endTime = time.time()
    
    @property
    def elapsedTime(self):
        """Waktu yang telah berlalu dalam detik"""
        if self.startTime and self.endTime:
            return self.endTime - self.startTime
        return 0
