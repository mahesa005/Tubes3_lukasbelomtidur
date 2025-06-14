from regexExtractor import RegexExtractor

# Contoh teks CV sederhana untuk pengujian
sample_text = '''
Nama: John Doe
Email: john.doe@email.com
Phone: 081234567891, +62 812-3456-7890

Summary:
Professional with 5+ years experience in software engineering.

Skills: Python, SQL, Machine Learning, Communication

Experience:
Software Engineer at ABC Corp (2020-2023)
Intern at XYZ (2019-2020)

Education:
S1 Informatika ITB 2016-2020
SMA 1 Bandung 2013-2016
'''

def main():
    print("=== RegexExtractor Test ===\n")
    extractor = RegexExtractor()

    print("--- Testing extractEmail ---")
    print(extractor.extractEmail(sample_text))

    print("\n--- Testing extractPhones (hanya digit, 12 digit) ---")
    print(extractor.extractPhones(sample_text, digit_length=12))

    print("\n--- Testing extractPhone (semua format mentah) ---")
    print(extractor.extractPhone(sample_text))

    print("\n--- Testing extractSummary ---")
    print(extractor.extractSummary(sample_text))

    print("\n--- Testing extractSkills ---")
    print(extractor.extractSkills(sample_text))

    print("\n--- Testing extractExperience ---")
    print(extractor.extractExperience(sample_text))

    print("\n--- Testing extractEducation ---")
    print(extractor.extractEducation(sample_text))

    print("\n--- Testing extractAllInformation ---")
    from pprint import pprint
    pprint(extractor.extractAllInformation(sample_text))

    print("\n=== Test Selesai ===\n")

if __name__ == "__main__":
    main()
