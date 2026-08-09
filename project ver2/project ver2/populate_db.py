import sqlite3
import hashlib

# دالة لتوليد الهاشات
def generate_hashes(text):
    text = text.strip()
    return {
        'md5': hashlib.md5(text.encode()).hexdigest(),
        'sha1': hashlib.sha1(text.encode()).hexdigest(),
        'sha256': hashlib.sha256(text.encode()).hexdigest(),
        'sha512': hashlib.sha512(text.encode()).hexdigest()
    }

# دالة بناء القاعدة
def populate():
    # فتح الملف وقراءة أول 10 آلاف سطر
    try:
        with open('rockyou.txt', 'r', encoding='latin-1') as f:
            lines = f.readlines()[:10000]
    except FileNotFoundError:
        print("خطأ: ملف rockyou.txt غير موجود في المجلد!")
        return

    conn = sqlite3.connect('rainbow_table.db')
    cursor = conn.cursor()

    # إنشاء الجدول
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rainbow_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_password TEXT NOT NULL,
            md5_hash TEXT UNIQUE,
            sha1_hash TEXT UNIQUE,
            sha256_hash TEXT UNIQUE,
            sha512_hash TEXT UNIQUE
        )
    ''')

    count = 0
    for line in lines:
        password = line.strip()
        if not password: continue
        
        hashes = generate_hashes(password)
        
        try:
            cursor.execute('''
                INSERT INTO rainbow_table (original_password, md5_hash, sha1_hash, sha256_hash, sha512_hash)
                VALUES (?, ?, ?, ?, ?)
            ''', (password, hashes['md5'], hashes['sha1'], hashes['sha256'], hashes['sha512']))
            count += 1
            if count % 1000 == 0:
                print(f"تمت معالجة {count} كلمة...")
        except sqlite3.IntegrityError:
            continue 

    conn.commit()
    conn.close()
    print("تم الانتهاء! القاعدة جاهزة للاختبار.")

if __name__ == '__main__':
    populate()
