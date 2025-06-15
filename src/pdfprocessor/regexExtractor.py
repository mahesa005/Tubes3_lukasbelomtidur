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
            """Format skill name properly with better validation"""
            if not skill:
                return ""
            
            # Clean up the skill
            skill = skill.strip()
            skill = re.sub(r'\s+', ' ', skill)  # Replace multiple spaces with single space
            
            # Skip personal attributes and soft skills
            personal_attrs = [
                'self-motivated', 'honest', 'reliable', 'hard-working', 'committed',
                'good work ethic', 'team member', 'customer service', 'thorough',
                'effective working', 'attributes', 'qualifications', 'core',
                'and attributes', 'cooperative team member', 'excellent customer service'
            ]
            
            if any(attr in skill.lower() for attr in personal_attrs):
                return ""
              # Skip very generic words
            generic_words = ['and', 'or', 'the', 'in', 'on', 'at', 'to', 'for', 'with', 'as', 'a', 'point', 'intermediate', 'advanced']
            if skill.lower() in generic_words:
                return ""
            
            # Skip standalone level indicators without context
            if skill.lower() in ['intermediate', 'advanced', 'basic', 'beginner', 'expert']:
                return ""
            
            # Handle compound skills
            if 'microsoft' in skill.lower():
                # Handle Microsoft products
                if 'word' in skill.lower():
                    return "Microsoft Word"
                elif 'excel' in skill.lower():
                    return "Microsoft Excel" 
                elif 'powerpoint' in skill.lower():
                    return "Microsoft PowerPoint"
                elif 'outlook' in skill.lower():
                    return "Microsoft Outlook"
                elif 'access' in skill.lower():
                    return "Microsoft Access"
                else:
                    return skill.title()
              # Handle standalone Office applications
            if skill.lower() == 'word':
                return "Microsoft Word"
            elif skill.lower() == 'excel':
                return "Microsoft Excel"
            elif skill.lower() in ['powerpoint', 'power']:
                return "Microsoft PowerPoint"
            elif skill.lower() == 'outlook':
                return "Microsoft Outlook"
            elif skill.lower() == 'access':
                return "Microsoft Access"
            
            # Handle QuickBooks variations
            if 'quickbooks' in skill.lower() or (skill.lower() == 'quick' or skill.lower() == 'books'):
                return "QuickBooks"
            elif skill.lower() == 'enterprise' and 'quickbooks' in text.lower():
                return "QuickBooks Enterprise"
            
            # Handle level + skill combinations properly
            if any(level in skill.lower() for level in ['advanced', 'intermediate', 'basic']):
                return skill.title()
            
            # Only return skills that seem technical or have reasonable length
            tech_indicators = [
                'quickbooks', 'sql', 'database', 'accounting', 'financial', 'analysis',
                'reporting', 'tax', 'audit', 'budgeting', 'payroll', 'billing', 'invoicing'
            ]
            
            has_tech_indicator = any(indicator in skill.lower() for indicator in tech_indicators)
            reasonable_length = len(skill) >= 4
            
            if has_tech_indicator or reasonable_length:
                return skill.title()
            
            return ""# Define section boundaries with more variations
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
          # Process Work Experience into clean, concise chunks
        work_experience = []
        if experience_raw:
            def is_valid_work_experience(text):
                """Check if text represents valid work experience"""
                text_lower = text.lower()
                
                # Skip very short or meaningless text
                if len(text) < 20:
                    return False
                
                # Skip pure skills descriptions (should be in skills section)
                skills_indicators = ['skills', 'proficient', 'expertise', 'competencies', 'abilities']
                if any(indicator in text_lower for indicator in skills_indicators) and len(text) > 100:
                    return False
                
                # Skip personal statements that don't describe work activities
                personal_statements = [
                    'work ethic', 'fast learner', 'team player', 'hard working',
                    'dedicated', 'motivated', 'passionate', 'committed to excellence'
                ]
                if any(statement in text_lower for statement in personal_statements) and len(text) > 80:
                    return False
                
                # Prefer text that contains action verbs and concrete work activities
                work_verbs = [
                    'managed', 'developed', 'created', 'implemented', 'designed', 'coordinated',
                    'supervised', 'trained', 'maintained', 'operated', 'analyzed', 'processed',
                    'executed', 'performed', 'collaborated', 'delivered', 'achieved', 'led'
                ]
                
                has_work_verb = any(verb in text_lower for verb in work_verbs)
                return has_work_verb or len(text) < 80
            
            def clean_work_experience_text(text):
                """Clean and format work experience text"""
                # Remove extra whitespace and artifacts
                text = re.sub(r'\s+', ' ', text).strip()
                text = text.replace('ï1⁄4​', '')
                
                # Limit length to keep it concise
                if len(text) > 120:
                    # Try to cut at a natural break point
                    words = text.split()
                    if len(words) > 15:
                        text = ' '.join(words[:15]) + '...'
                    else:
                        text = text[:120] + '...'
                
                return text
            
            # Method 1: Try splitting by job titles and dates
            job_patterns = [
                r'(?=\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:January|February|March|April|May|June|July|August|September|October|November|December|\d{1,2}/\d{4}|\d{4}))',
                r'(?=\b(?:Manager|Director|Analyst|Specialist|Coordinator|Assistant|Administrator|Engineer|Developer|Consultant|Technician|Supervisor|Officer)\b)',
                r'(?=\d{1,2}/\d{4}\s+to\s+\d{1,2}/\d{4})',
                r'(?=\d{4}\s*[-–]\s*\d{4})'
            ]
            
            experience_found = False
            for pattern in job_patterns:
                exp_parts = re.split(pattern, experience_raw)
                if len(exp_parts) > 1:
                    for part in exp_parts:
                        part = part.strip()
                        if len(part) > 30:
                            # Split into individual accomplishments/responsibilities
                            sentences = re.split(r'[.!?]+', part)
                            for sentence in sentences:
                                sentence = sentence.strip()
                                if is_valid_work_experience(sentence):
                                    cleaned = clean_work_experience_text(sentence)
                                    if cleaned and cleaned not in work_experience:
                                        work_experience.append(cleaned)
                    experience_found = True
                    break
            
            # Method 2: If no clear job structure, use bullet point or sentence splitting
            if not experience_found:
                # Try bullet points first
                bullet_parts = re.split(r'[•·▪▫◦‣⁃∙]+', experience_raw)
                if len(bullet_parts) > 1:
                    for part in bullet_parts:
                        part = part.strip()
                        if is_valid_work_experience(part):
                            cleaned = clean_work_experience_text(part)
                            if cleaned and cleaned not in work_experience:
                                work_experience.append(cleaned)
                else:
                    # Fall back to sentence splitting
                    sentences = re.split(r'[.!?]+', experience_raw)
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if is_valid_work_experience(sentence):
                            cleaned = clean_work_experience_text(sentence)
                            if cleaned and cleaned not in work_experience:
                                work_experience.append(cleaned)
            
            # Limit to 7 most relevant work experiences
            work_experience = work_experience[:7]
          # Process Skills into clean list
        skills = []
        if skills_raw:
            # Handle special case where skill header is concatenated with first skill
            if 'skill highlight' in skills_raw.lower():
                # Find where the actual skills start after the header
                skills_raw = re.sub(r'skill\s*highlights?', '', skills_raw, flags=re.IGNORECASE)
            
            # Pre-process to identify and protect compound skills
            compound_skills = [
                'QuickBooks Enterprise', 'Accounts Receivable', 'Accounts Payable',
                'Microsoft Word', 'Microsoft Excel', 'Microsoft PowerPoint', 
                'Microsoft Outlook', 'Microsoft Access', 'Customer Service',
                'Data Entry', 'Credit Checks', 'Sales Reports'
            ]
            
            protected_skills = []
            remaining_text = skills_raw
            
            for compound in compound_skills:
                if compound.lower() in remaining_text.lower():
                    protected_skills.append(compound)
                    # Remove it from remaining text to avoid duplicate processing
                    remaining_text = re.sub(re.escape(compound), '', remaining_text, flags=re.IGNORECASE)
            
            # Process remaining skills normally
            skill_parts = re.split(r'(?=[A-Z][a-z])', remaining_text)
            
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
            
            # Add the protected compound skills
            for protected in protected_skills:
                if protected not in skills:
                    skills.append(protected)
        
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
          # Process Education into clean, meaningful entries
        education = []
        if education_raw:
            def is_valid_education_entry(text):
                """Check if text represents valid education information"""
                text_lower = text.lower()
                
                # Must contain education-related keywords
                education_keywords = [
                    'bachelor', 'master', 'phd', 'degree', 'university', 'college', 
                    'institute', 'school', 'diploma', 'certificate', 'graduation',
                    'major', 'minor', 'gpa', 'magna cum laude', 'summa cum laude'
                ]
                
                has_edu_keyword = any(keyword in text_lower for keyword in education_keywords)
                if not has_edu_keyword:
                    return False
                  # Skip if it's mostly a skills list
                skills_indicators = ['skills', 'proficient', 'expertise', 'competencies']
                if any(indicator in text_lower for indicator in skills_indicators):
                    # Check if it's followed by a long list (typical skills section)
                    if len(text) > 200 and text.count(',') > 10:
                        return False
                
                return True
            
            def clean_education_entry(text):
                """Clean education entry by removing skills lists and extra content"""
                # Remove skills section if it appears at the end
                if 'skills' in text.lower():
                    # Find where skills section starts
                    skills_pos = text.lower().find('skills')
                    if skills_pos > 20:  # Keep the main education info before skills
                        text = text[:skills_pos].strip()
                
                # Handle year and institution patterns better
                # Look for patterns like ": 2008 Martinez Adult Education"
                if ':' in text and re.search(r':\s*\d{4}', text):
                    # Split on the colon and reconstruct properly
                    parts = text.split(':')
                    if len(parts) >= 2:
                        program_part = parts[0].strip()
                        year_institution_part = parts[1].strip()
                        
                        # Extract year
                        year_match = re.search(r'\d{4}', year_institution_part)
                        if year_match:
                            year = year_match.group()
                            # Get institution part after year
                            year_end = year_match.end()
                            institution_part = year_institution_part[year_end:].strip()
                            
                            # Clean up institution name
                            if institution_part:
                                # Remove extra symbols and clean
                                institution_part = re.sub(r'^[^\w]*|[^\w]*$', '', institution_part)
                                text = f"{program_part} ({year}) - {institution_part}"
                            else:
                                text = f"{program_part} ({year})"
                
                # Remove excessive comma-separated lists (likely skills)
                parts = text.split(',')
                if len(parts) > 5:
                    # Keep only the first few parts that seem like education info
                    education_parts = []
                    for part in parts[:5]:
                        part = part.strip()
                        if any(keyword in part.lower() for keyword in 
                              ['bachelor', 'master', 'university', 'college', 'certificate', 'program']):
                            education_parts.append(part)
                        elif len(education_parts) < 3 and len(part) > 5:
                            education_parts.append(part)
                    
                    if education_parts:
                        text = ', '.join(education_parts)
                
                # Clean up formatting
                text = re.sub(r'\s+', ' ', text).strip()
                text = text.replace('ï1⁄4​', '')
                text = text.replace('ï¼​', '')
                
                # Limit length to keep it readable
                if len(text) > 150:
                    text = text[:150] + '...'
                
                return text
              # Method 1: Look for specific degree patterns
            degree_patterns = [
                r'Bachelor\s+of\s+[A-Za-z\s]+(?:\s+[A-Za-z\s]*(?:University|College|Institute))?[^,]*',
                r'Master\s+of\s+[A-Za-z\s]+(?:\s+[A-Za-z\s]*(?:University|College|Institute))?[^,]*',
                r'PhD\s+in\s+[A-Za-z\s]+(?:\s+[A-Za-z\s]*(?:University|College|Institute))?[^,]*',
                r'[A-Za-z\s]+\s+(?:Certificate|Diploma)\s+Program[^,]*',
                r'Associate\s+(?:of|in)\s+[A-Za-z\s]+[^,]*',
                r'[A-Za-z\s]+\s+Specialist\s+Certificate\s+Program[^,]*'
            ]
            
            for pattern in degree_patterns:
                matches = re.findall(pattern, education_raw, re.IGNORECASE)
                for match in matches:
                    cleaned = clean_education_entry(match)
                    if cleaned and len(cleaned) > 10 and cleaned not in education:
                        education.append(cleaned)
            
            # Method 2: Look for institution patterns if no degrees found
            if not education:
                institution_patterns = [
                    r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:University|College|Institute|School)[^,]*',
                    r'(?:University|College|Institute|School)\s+of\s+[A-Z][a-z]+[^,]*'
                ]
                
                for pattern in institution_patterns:
                    matches = re.findall(pattern, education_raw)
                    for match in matches:
                        cleaned = clean_education_entry(match)
                        if cleaned and len(cleaned) > 10 and cleaned not in education:
                            education.append(cleaned)
            
            # Method 3: General parsing if still no education found
            if not education:
                # Split by common delimiters and look for education-related chunks
                chunks = re.split(r'[.;]\s*', education_raw)
                for chunk in chunks:
                    chunk = chunk.strip()
                    if is_valid_education_entry(chunk):
                        cleaned = clean_education_entry(chunk)
                        if cleaned and len(cleaned) > 10 and cleaned not in education:
                            education.append(cleaned)
            
            # Limit to 3 most relevant education entries
            education = education[:3]
        
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