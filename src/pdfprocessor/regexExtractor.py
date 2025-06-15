# ===== src/pdfProcessor/regexExtractor.py =====
"""
Ekstraksi Informasi Berbasis Regex dari CV
Tujuan: Mengekstrak informasi spesifik dari teks CV menggunakan regex
"""

import re
from datetime import datetime
import logging
import unicodedata

class RegexExtractor:
    """
    Kelas untuk ekstraksi informasi menggunakan regex
    
    TODO:
    - Definisikan pola regex untuk berbagai informasi
    - Ekstrak nama, email, nomor telepon, dll
    - Ekstrak pengalaman kerja, pendidikan, keterampilan
    - Tangani berbagai format CV
    """
    
    def __init__(self):
        """Inisialisasi regex extractor"""
        self.logger = logging.getLogger(__name__)
        self.setupPatterns()
    
    def setupPatterns(self):
        """
        Menyiapkan pola regex untuk berbagai informasi
        
        TODO:
        - Pola email
        - Pola nomor telepon (berbagai format)
        - Pola tanggal
        - Pola pengalaman kerja
        - Pola pendidikan
        - Pola keterampilan
        """
        # Pola email
        self.emailPattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Pola nomor telepon (berbagai format)
        self.phonePatterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # Format US
            r'\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US dengan kode negara
            r'\+\d{1,3}[-.\s]?\d{1,14}',  # Format internasional
        ]
        
        # Pola tanggal
        self.datePatterns = [
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',  # MM/DD/YYYY
            r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',  # YYYY/MM/DD
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\b',  # Bulan Tahun
        ]
    
    def extractEmail(self, text):
        """
        Mengekstrak alamat email dari teks
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar alamat email yang ditemukan
        """
        pass
    
    def extractPhone(self, text):
        """
        Mengekstrak nomor telepon dari teks
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar nomor telepon yang ditemukan
        """
        pass
    
    def extractSummary(self, text):
        """
        Mengekstrak ringkasan/tujuan dari CV
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            str: Teks ringkasan atau string kosong
            
        TODO:
        - Cari bagian summary/objective/profile
        - Ekstrak paragraf yang relevan
        - Bersihkan hasil ekstraksi
        """
        pass
    
    def extractSkills(self, text):
        """
        Mengekstrak keterampilan dari CV
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar keterampilan yang ditemukan
            
        TODO:
        - Cari bagian skills/competencies
        - Ekstrak keterampilan satu per satu
        - Tangani berbagai format (poin, dipisahkan koma, dll)
        """
        pass
    
    def extractExperience(self, text):
        """
        Mengekstrak pengalaman kerja dari CV
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar dict dengan informasi pekerjaan
            
        TODO:
        - Cari bagian pengalaman kerja/riwayat pekerjaan
        - Ekstrak jabatan, perusahaan, tanggal
        - Parsing deskripsi pekerjaan
        """
        pass
    
    def extractEducation(self, text):
        """
        Mengekstrak informasi pendidikan dari CV
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            list: Daftar dict dengan informasi pendidikan
            
        TODO:
        - Cari bagian pendidikan
        - Ekstrak gelar, institusi, tanggal kelulusan
        - Tangani berbagai format entri pendidikan
        """
        pass
    
    def extractAllInformation(self, text):
        """
        Mengekstrak semua informasi dari CV
        
        Argumen:
            text (str): Teks CV
            
        Mengembalikan:
            dict: Dictionary dengan semua informasi yang diekstrak
            
        TODO:        - Panggil semua metode ekstraksi
        - Gabungkan hasil dalam format standar
        - Tangani error dari masing-masing ekstraktor
        """
        pass

    def extract_cv_sections(self, text):
        """
        Extract skills, work experience, and education from CV text using heuristic patterns
        Returns properly formatted lists for each section.
        """
        
        def extract_section_between_keywords(text, start_keywords, end_keywords=None):
            """Extract text between start and end keywords"""
            text_lower = text.lower()
            
            for start_kw in start_keywords:
                start_pos = text_lower.find(start_kw.lower())
                if start_pos != -1:
                    # Find the actual start position after the keyword
                    start_pos = start_pos + len(start_kw)
                    
                    # Find end position
                    end_pos = len(text)
                    if end_keywords:
                        for end_kw in end_keywords:
                            temp_end = text_lower.find(end_kw.lower(), start_pos)
                            if temp_end != -1 and temp_end < end_pos:
                                end_pos = temp_end
                    
                    # Extract the section
                    section_text = text[start_pos:end_pos].strip()
                    return section_text
            
            return ""
        
        def format_skill_name(skill):
            """Format skill name to proper case"""
            # Remove artifacts and clean
            skill = skill.replace('ï1⁄4​', '').strip()
            if not skill:
                return ""
            
            # Title case each word
            words = skill.split()
            formatted_words = []
            for word in words:
                # Handle special cases
                if word.lower() in ['sql', 'ms', 'it', 'hr', 'api', 'ui', 'ux']:
                    formatted_words.append(word.upper())
                elif word.lower() in ['and', 'or', 'of', 'the', 'in', 'on', 'at', 'to']:
                    formatted_words.append(word.lower())
                else:
                    formatted_words.append(word.capitalize())
            
            return ' '.join(formatted_words)        # Define section boundaries with more variations
        skills_keywords = ['Skills', 'Skill Highlights', 'SkillHighlights', 'Technical Skills', 'Core Competencies', 'Key Skills']
        experience_keywords = ['Experience', 'Professional Experience', 'Work Experience', 'Employment History'] 
        education_keywords = ['Education and Training', 'Education', 'Academic Background', 'Qualifications']
        
        # Extract raw sections
        skills_raw = extract_section_between_keywords(text, skills_keywords, experience_keywords)
        
        # If no skills found with standard keywords, try alternative detection
        if not skills_raw:
            # Look for text that contains skills-related content
            skill_indicators = ['Microsoft', 'VMware', 'Server', 'Exchange', 'programming', 'database', 'management']
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                line_lower = line.lower()
                if any(indicator in line_lower for indicator in ['skill', 'competenc', 'technical']):
                    # Found a skills section, extract next several lines
                    start_pos = text.find(line)
                    if start_pos != -1:
                        # Look for the end (next major section)
                        remaining_text = text[start_pos:]
                        end_markers = ['Professional Experience', 'Experience', 'Education', 'Certification', 'Accomplishment']
                        end_pos = len(remaining_text)
                        
                        for marker in end_markers:
                            marker_pos = remaining_text.find(marker)
                            if marker_pos != -1 and marker_pos < end_pos:
                                end_pos = marker_pos
                        
                        skills_raw = remaining_text[:end_pos].strip()
                        break
        experience_raw = extract_section_between_keywords(text, experience_keywords, education_keywords)
        education_raw = extract_section_between_keywords(text, education_keywords)
        
        # Process Work Experience into meaningful chunks FIRST
        work_experience = []
        if experience_raw:
            # Split by meaningful patterns (dates, positions, etc.)
            exp_parts = re.split(r'(?=\d{2}/\d{4}|\d{4}[/-]\d{4}|(?:[A-Z][a-z]+\s+){2,}(?:Manager|Director|Senior|Lead|Analyst|Engineer|Developer))', experience_raw)
            
            for part in exp_parts:
                part = part.strip()
                if len(part) > 20:  # Only meaningful experience chunks
                    # Clean up the text
                    cleaned = part.replace('ï1⁄4​', '').strip()
                    # Split into sentences and take meaningful ones
                    sentences = re.split(r'[.!?]+', cleaned)
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if len(sentence) > 15 and not sentence.isdigit():
                            work_experience.append(sentence)
            
            # Limit to reasonable number
            work_experience = work_experience[:10]
        
        # Process Skills into clean list
        skills = []
        if skills_raw:
            # Handle special case where skill header is concatenated with first skill
            if 'skill highlight' in skills_raw.lower():
                # Find where the actual skills start after the header
                skills_raw = re.sub(r'skill\s*highlights?', '', skills_raw, flags=re.IGNORECASE)
            
            # Process normally found skills
            skill_parts = re.split(r'(?=[A-Z][a-z])', skills_raw)
            
            for part in skill_parts:
                part = part.strip()
                if len(part) > 2:
                    # Split by common delimiters and patterns for technology skills
                    sub_parts = re.split(r'[,;]\s*|(?<=[a-z])\s+(?=[A-Z])|(?<=\d)\s+(?=[A-Z])|(?=VMware)|(?=Microsoft)|(?=Cisco)', part)
                    for sub_part in sub_parts:
                        sub_part = sub_part.strip()
                        if len(sub_part) > 2 and not sub_part.isdigit():
                            # Clean up extra characters
                            sub_part = re.sub(r'^[^\w]*|[^\w]*$', '', sub_part)
                            if sub_part and len(sub_part) > 2:
                                formatted_skill = format_skill_name(sub_part)
                                if formatted_skill and formatted_skill not in skills:
                                    skills.append(formatted_skill)
        
        # If no skills found, check work experience for skills section
        if not skills and work_experience:
            for exp_item in work_experience:
                if 'skill' in exp_item.lower() and any(tech in exp_item for tech in ['Microsoft', 'VMware', 'Server', 'Exchange']):
                    # Found skills in work experience, extract them
                    # Remove the "Skill Highlights" prefix
                    skills_text = exp_item
                    if 'skill' in skills_text.lower():
                        start_pos = skills_text.lower().find('skill')
                        # Skip past "Skill Highlights" or similar
                        skills_content = skills_text[start_pos:]
                        # Remove the word "Skill" and "Highlights" 
                        skills_content = re.sub(r'skill\s*highlights?', '', skills_content, flags=re.IGNORECASE)
                        
                        # Extract individual skills
                        # Split by known patterns
                        skill_items = re.split(r'(?=[A-Z][a-z]+\s+[A-Z])|(?=VMware)|(?=Microsoft)|(?=Cisco)|(?=ITIL)', skills_content)
                        
                        for skill_item in skill_items:
                            skill_item = skill_item.strip()
                            if len(skill_item) > 3 and not skill_item.isdigit():
                                # Clean up and format
                                skill_item = re.sub(r'[^a-zA-Z0-9\s\.-]', '', skill_item)
                                skill_item = skill_item.strip()
                                if skill_item and len(skill_item) > 2:
                                    formatted_skill = format_skill_name(skill_item)
                                    if formatted_skill and formatted_skill not in skills:
                                        skills.append(formatted_skill)
                    
                    # Remove this item from work experience since it's skills
                    work_experience.remove(exp_item)
                    break
          # Limit to reasonable number and remove duplicates
        skills = skills[:15]
        
        # Process Education into meaningful entries
        education = []
        if education_raw:
            # Look for degree patterns
            degree_patterns = [
                r'Bachelor\s+of\s+\w+[^.]*',
                r'Master\s+of\s+\w+[^.]*',
                r'PhD\s+in\s+\w+[^.]*',
                r'\w+\s+University[^.]*',
                r'\w+\s+College[^.]*',
                r'Magna\s+Cum\s+Laude[^.]*'
            ]
            
            for pattern in degree_patterns:
                matches = re.findall(pattern, education_raw, re.IGNORECASE)
                for match in matches:
                    cleaned = match.replace('ï1⁄4​', '').strip()
                    if cleaned and len(cleaned) > 5 and cleaned not in education:
                        education.append(cleaned)
            
            # If no patterns found, split by meaningful chunks
            if not education:
                edu_parts = education_raw.split()
                current_chunk = ""
                for word in edu_parts:
                    if word and not word.isdigit():
                        current_chunk += word + " "
                        # If we have a meaningful chunk, add it
                        if len(current_chunk.strip()) > 10 and any(keyword in current_chunk.lower() 
                                                                 for keyword in ['university', 'college', 'bachelor', 'master', 'degree', 'science']):
                            education.append(current_chunk.strip().replace('ï1⁄4​', ''))
                            current_chunk = ""
                
                # Add remaining chunk if meaningful
                if len(current_chunk.strip()) > 10:
                    education.append(current_chunk.strip().replace('ï1⁄4​', ''))
            
            # Limit and clean
            education = [edu for edu in education if len(edu) > 5][:5]
        
        return {
            'skills': skills,
            'work_experience': work_experience,
            'education': education
        }

    def cleanseText(self, text):
        
        # 1. Normalize unicode
        cleaned_text = unicodedata.normalize('NFKC', text)

        # 2. Remove non-visual characters
        cleaned_text = re.sub(r'[\x00-\x1F\x7F]', '', cleaned_text)

        # 3. Remove bullet and other unneccessary symbols
        cleaned_text = re.sub(r'[•▪●◦\uf0b7\u2022\u25cf]', '', cleaned_text)

        # 4. Remove extra whitspace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

        # 5. Remove extra white space and beginning and end of string
        cleaned_text = cleaned_text.strip()

        # 6. Clean up spacing around punctuation
        cleaned_text = re.sub(r'\s+([,.;:!?])', r'\1', cleaned_text)  # Remove space before punctuation
        
        return cleaned_text
    

    def cleanseTextN(self, text):
        """
        cleanse text but keep the newlines
        """
        # 1. Normalize unicode
        cleaned_text = unicodedata.normalize('NFKC', text)

        # 2. Remove non-visual characters
        cleaned_text = re.sub(r'[\x00-\x09\x0B-\x1F\x7F]', '', cleaned_text)

        # 3. Remove bullet and other unneccessary symbols
        cleaned_text = re.sub(r'[•▪●◦\uf0b7\u2022\u25cf]', '', cleaned_text)

        # 4. Remove extra whitspace
        # 4. Clean multiple spaces/tabs but keep single newlines
        cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)  # Multiple spaces/tabs -> single space
        cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)  # Multiple newlines -> double newline max

        # 5. Remove extra white space and beginning and end of string
        cleaned_text = cleaned_text.strip()

        # 6. Clean up spacing around punctuation
        cleaned_text = re.sub(r'\s+([,.;:!?])', r'\1', cleaned_text)  # Remove space before punctuation
        
        return cleaned_text
    
    def seperatePunctuations(self, text):
        """
        Memisahkan semua tanda baca dalam teks dengan sebuah spasi.
        Contoh: "Hello,world!" -> "Hello , world !"
                "Test.One" -> "Test . One"
                "Buy 1 get 1." -> "Buy 1 get 1 ."
                "end-to-end" -> "end - to - end" (jika '-' dianggap dipisah)

        Args:
            text (str): String teks yang akan diproses.

        Returns:
            str: String teks dengan tanda baca yang sudah dipisahkan spasi.
        """
        if not text:
            return ""
        # 1. Add whitespace sebelum punctuation
        text = re.sub(r'(\S)([^\w\s])', r'\1 \2', text)

        # 2. Add whitespace setelah punctuation
        text = re.sub(r'([^\w\s])(\S)', r'\1 \2', text)

        # 3. Remove every extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text