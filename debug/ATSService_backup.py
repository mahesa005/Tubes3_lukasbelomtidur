# ===== src/services/ATSService.py =====
"""
ATS Service - Service layer untuk integrasi semua komponen
Tujuan: Mengintegrasikan PDF extraction, pattern matching, dan database operations
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any
import time
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.pdfprocessor.pdfExtractor import PDFExtractor
from src.pdfprocessor.regexExtractor import RegexExtractor
from src.algorithm.PatternMatcher import PatternMatcher
from src.database.connection import DatabaseConnection
from src.database.queries import *
from src.utils.FileManager import FileManager
from src.models.ResultCard import ResultCard
from src.models.SummaryCard import SummaryData
from config import DATA_DIR


class ATSService:
    """
    Service untuk integrasi semua komponen ATS dengan optimasi performa
    """
    
    def __init__(self):
        """Inisialisasi service"""
        self.logger = logging.getLogger(__name__)
        self.pdfExtractor = PDFExtractor()
        self.regexExtractor = RegexExtractor()
        self.patternMatcher = PatternMatcher()
        self.fileManager = FileManager()
        self.db = DatabaseConnection()
        
        # Cache untuk teks PDF yang sudah di-extract
        self.text_cache = {}
        self.cache_file = os.path.join(DATA_DIR, "text_cache.json")
        self.lock = threading.Lock()
        
        # Load cache yang sudah ada
        self._load_cache()
        
    def _load_cache(self):
        """Load cache dari file jika ada"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.text_cache = json.load(f)
                self.logger.info(f"Loaded cache with {len(self.text_cache)} entries")
        except Exception as e:
            self.logger.warning(f"Could not load cache: {e}")
            self.text_cache = {}
    
    def _save_cache(self):
        """Save cache ke file"""
        try:
            with self.lock:
                with open(self.cache_file, 'w', encoding='utf-8') as f:
                    json.dump(self.text_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.warning(f"Could not save cache: {e}")
    
    def _get_file_hash(self, file_path: str) -> str:
        """Generate hash untuk file berdasarkan path dan modified time"""
        try:
            stat = os.stat(file_path)
            content = f"{file_path}_{stat.st_mtime}_{stat.st_size}"
            return hashlib.md5(content.encode()).hexdigest()
        except:
            return hashlib.md5(file_path.encode()).hexdigest()
    
    def _get_cached_text(self, pdf_path: str) -> str:
        """Dapatkan teks dari cache atau extract jika belum ada"""
        file_hash = self._get_file_hash(pdf_path)
        
        if file_hash in self.text_cache:
            return self.text_cache[file_hash]
        
        # Extract text dan simpan ke cache
        try:
            text = self.pdfExtractor.PDFExtractForMatch(pdf_path)
            if text:
                with self.lock:
                    self.text_cache[file_hash] = text
            return text or ""
        except Exception as e:
            self.logger.error(f"Error extracting text from {pdf_path}: {e}")
            return ""
    
    def _process_single_pdf(self, pdf_path: str, keywords: List[str], algorithm: str) -> Dict[str, Any]:
        """Proses satu file PDF untuk pencarian"""
        try:
            # Dapatkan text (dari cache atau extract)
            text = self._get_cached_text(pdf_path)
            if not text:
                return None
            
            # Lakukan pattern matching
            match_result = self.patternMatcher.exactMatch(text, keywords, algorithm)
            
            # Hitung total matches
            total_matches = sum(
                match_data['count'] 
                for match_data in match_result['matches'].values()
            )
            
            if total_matches > 0:
                return {
                    'cv_path': pdf_path,
                    'total_matches': total_matches,
                    'matched_keywords': {
                        keyword: data['count'] 
                        for keyword, data in match_result['matches'].items()
                        if data['count'] > 0
                    }
                }
            
            return None            
        except Exception as e:
            self.logger.error(f"Error processing {pdf_path}: {e}")
            return None
    
    def searchCVs(self, keywords: List[str], algorithm: str = 'KMP', topMatches: int = 5) -> Dict[str, Any]:
        """
        Mencari CV berdasarkan keywords dengan optimasi performa
        
        Args:
            keywords: List kata kunci yang dicari
            algorithm: Algoritma pencarian ('KMP' atau 'BM')
            topMatches: Jumlah hasil teratas yang dikembalikan
              Returns:
            Dict berisi hasil pencarian dan metadata
        """
        start_time = time.time()
        results = []
        db_connected = False
        
        try:
            # Dapatkan semua file PDF dari data directory
            pdf_files = self.fileManager.listPDFFiles(str(DATA_DIR))
            self.logger.info(f"Found {len(pdf_files)} PDF files total")
            self.logger.info(f"Looking for {topMatches} top matches")
            
            # Buka koneksi database sekali untuk semua operasi
            db_connected = self.db.connect()
            if not db_connected:
                self.logger.warning("Database connection failed, proceeding without database lookup")
            
            # Proses PDF files secara paralel sampai mendapat hasil yang cukup
            matches_found = []
            max_workers = min(6, os.cpu_count() or 1)  # Lebih banyak worker untuk proses lebih cepat
            batch_size = 50  # Batch yang lebih besar untuk efisiensi
            processed_count = 0
              # Process files in batches, stop when we have enough matches
            for i in range(0, len(pdf_files), batch_size):
                if len(matches_found) >= topMatches:  # Berhenti segera setelah dapat hasil yang cukup
                    self.logger.info(f"Found {topMatches} matches, stopping search")
                    break
                    
                batch = pdf_files[i:i + batch_size]
                self.logger.info(f"Processing batch {i//batch_size + 1}: {len(batch)} files")
                
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # Submit batch tasks
                    future_to_path = {
                        executor.submit(self._process_single_pdf, pdf_path, keywords, algorithm): pdf_path
                        for pdf_path in batch
                    }
                    
                    # Collect results from this batch
                    for future in as_completed(future_to_path):
                        result = future.result()
                        if result:
                            matches_found.append(result)
                        processed_count += 1
                          # Early exit if we have enough matches
                        if len(matches_found) >= topMatches:
                            # Cancel remaining futures in this batch
                            for f in future_to_path:
                                if not f.done():
                                    f.cancel()
                            break
            
            self.logger.info(f"Processed {processed_count} files, found {len(matches_found)} matching PDFs")
            
            # Batch query database untuk semua matching files
            if db_connected and self.db.connection and matches_found:
                cv_paths = [match['cv_path'] for match in matches_found]
                db_info = self._batch_get_cv_info(cv_paths)
            else:
                db_info = {}
            
            # Build final results
            for match in matches_found:
                pdf_path = match['cv_path']
                
                # Dapatkan nama dari database atau fallback ke nama file
                if pdf_path in db_info:
                    info = db_info[pdf_path]
                    full_name = f"{info['first_name']} {info['last_name']}".strip()
                    application_id = info['application_id']
                else:
                    full_name = Path(pdf_path).stem
                    application_id = None
                
                # Hitung match score
                match_score = min(100, (match['total_matches'] / len(keywords)) * 100)
                
                results.append({
                    'application_id': application_id,
                    'name': full_name,
                    'match_score': match_score,
                    'keywords': match['matched_keywords'],
                    'cv_path': pdf_path,
                    'total_matches': match['total_matches']
                })
            
            # Sort berdasarkan match score dan ambil top matches
            results.sort(key=lambda x: x['match_score'], reverse=True)
            results = results[:topMatches]
            
            # Save cache setelah selesai
            self._save_cache()
            end_time = time.time()
            
            return {
                'results': results,
                'metadata': {
                    'total_files_available': len(pdf_files),
                    'total_processed': processed_count,
                    'total_matches': len(results),
                    'algorithm': algorithm,
                    'keywords': keywords,
                    'processing_time_ms': (end_time - start_time) * 1000,
                    'early_termination': processed_count < len(pdf_files)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error in searchCVs: {e}")
            return {
                'results': [],
                'metadata': {
                    'error': str(e),
                    'total_processed': 0,
                    'total_matches': 0
                }
            }
        finally:
            # Pastikan koneksi database ditutup
            if db_connected and self.db.connection:
                self.db.disconnect()
    
    def _batch_get_cv_info(self, cv_paths: List[str]) -> Dict[str, Dict[str, Any]]:
        """Batch query untuk mendapatkan info CV dari database"""
        try:
            if not cv_paths:
                return {}
              # Create placeholders for IN clause
            placeholders = ','.join(['%s'] * len(cv_paths))
            query = f"""
                SELECT ad.cv_path, ap.first_name, ap.last_name, ad.application_id 
                FROM ApplicationDetail ad
                LEFT JOIN ApplicantProfile ap ON ad.applicant_id = ap.applicant_id
                WHERE ad.cv_path IN ({placeholders})
            """
            
            cursor = self.db.connection.cursor()
            cursor.execute(query, cv_paths)
            results = cursor.fetchall()
            cursor.close()
            
            # Build lookup dict
            cv_info = {}
            for row in results:
                cv_path, first_name, last_name, application_id = row
                cv_info[cv_path] = {
                    'first_name': first_name or '',
                    'last_name': last_name or '',
                    'application_id': application_id
                }
            
            return cv_info
            
        except Exception as e:
            self.logger.error(f"Error in batch CV info query: {e}")
            return {}
    
    def getSummary(self, application_id: int = None, cv_path: str = None) -> SummaryData:
        """
        Mendapatkan ringkasan CV berdasarkan application_id atau cv_path
        
        Args:
            application_id: ID aplikasi
            cv_path: Path ke file CV
            
        Returns:
            SummaryData object
        """
        try:
            if not self.db.connect():
                raise Exception("Gagal koneksi database")
            
            # Jika ada application_id, dapatkan cv_path dari database
            if application_id and not cv_path:
                query = "SELECT cv_path FROM ApplicationDetail WHERE application_id = %s"
                result = self.db.fetchOne(query, (application_id,))
                if result:
                    cv_path = result[0]
            
            if not cv_path or not os.path.exists(cv_path):
                raise Exception("File CV tidak ditemukan")
            
            # Extract informasi dari PDF
            text = self.pdfExtractor.PDFtoText(cv_path)
            extracted_info = self.regexExtractor.extractAllInformation(text)
            
            # Dapatkan data dari database
            first_name = get_first_name_by_cv_path(self.db.connection, cv_path) or ""
            last_name = get_last_name_by_cv_path(self.db.connection, cv_path) or ""
            date_of_birth = get_date_of_birth_by_cv_path(self.db.connection, cv_path)
            phone_number = get_phone_number_by_cv_path(self.db.connection, cv_path) or ""
            
            # Gabungkan informasi
            full_name = f"{first_name} {last_name}".strip()
            birth_date = str(date_of_birth) if date_of_birth else ""
            
            # Ambil skills dari extracted info atau gunakan default
            skills = extracted_info.get('skills', [])
            if not skills and extracted_info.get('summary'):
                # Fallback: extract skills dari summary
                skills = self._extractSkillsFromSummary(extracted_info['summary'])
            
            # Format work experience
            work_experience = [
                exp['desc'] for exp in extracted_info.get('experience', [])
            ]
            
            # Format education
            education = [
                edu['desc'] for edu in extracted_info.get('education', [])
            ]
            
            summary_data = SummaryData(
                full_name=full_name,
                birth_date=birth_date,
                phone_number=phone_number,
                skills=skills,
                cv_path=cv_path,
                work_experience=work_experience,
                education=education
            )
            
            self.db.disconnect()
            return summary_data
            
        except Exception as e:
            self.logger.error(f"Error in getSummary: {e}")
            self.db.disconnect()
            return SummaryData()
    
    def _extractSkillsFromSummary(self, summary: str) -> List[str]:
        """Helper untuk extract skills dari summary"""
        common_skills = [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'SQL', 'HTML', 'CSS',
            'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'Spring',
            'Machine Learning', 'Data Science', 'AI', 'Deep Learning',
            'Git', 'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP'        ]
        
        found_skills = []
        summary_lower = summary.lower()
        
        for skill in common_skills:
            if skill.lower() in summary_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def getAllCVPaths(self) -> List[str]:
        """Mendapatkan semua path CV dari data directory"""
        return self.fileManager.listPDFFiles(str(DATA_DIR))
    
    def validatePDF(self, pdf_path: str) -> bool:
        """Validasi file PDF"""
        return self.fileManager.isValidPDF(pdf_path)
    
    def clear_cache(self):
        """Clear the text cache"""
        with self.lock:
            self.text_cache = {}
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
        except Exception as e:
            self.logger.warning(f"Could not remove cache file: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            'cache_size': len(self.text_cache),
            'cache_file_exists': os.path.exists(self.cache_file)
        }
