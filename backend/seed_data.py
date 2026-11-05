"""
Seed data lengkap kurikulum sesuai 20 file HTML:
- 11 CPL, 33 CPMK, 56 Sub-CPMK, 60 MK
- 68 relasi CPMK↔MK
- 13 komponen penilaian
- Admin user default
"""
from app.database import SessionLocal, engine, Base
from app.models.kurikulum import CPL, CPMK, SubCPMK, MK
from app.models.penilaian import KomponenPenilaian
from app.models.auth import User
from app.core.security import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ============================================================
# 1. CPL (11)
# ============================================================
CPL_DATA = [
    ("CPL01", "Mempunyai pengetahuan matematika, computing, dan ilmu pengetahuan lain yang relevan untuk menyelesaikan permasalahan computing yang kompleks dengan pendekatan teknologi informasi.", "Pengetahuan"),
    ("CPL02", "Mampu menganalisis, mengidentifikasi, dan mendefinisikan permasalahan computing yang kompleks, dan memberikan pendekatan teknologi informasi sebagai solusi penyelesaian permasalahan tersebut.", "Pengetahuan"),
    ("CPL03", "Mampu merancang, mengimplementasi, dan mengevaluasi solusi berbasis computing yang sesuai dengan kebutuhan dan solusi teknologi informasi yang diusulkan menggunakan sumberdaya, sarana, dan cara-cara computing modern.", "Keterampilan Khusus"),
    ("CPL04", "Mampu memilih, mengintegrasikan, dan mengadministrasikan infrastruktur teknologi informasi sebagai solusi penyelesaian permasalahan computing yang kompleks.", "Keterampilan Khusus"),
    ("CPL05", "Mampu mengimplementasikan, mengelola, dan mengamankan sistem dan informasi yang didistribusikan melalui jaringan komputer untuk menjamin kerahasiaan, integritas, dan ketersediaan informasi.", "Keterampilan Khusus"),
    ("CPL06", "Mampu menerapkan pemikiran logis, kritis, sistematis, dan inovatif dalam konteks pengembangan atau implementasi ilmu pengetahuan dan teknologi yang memperhatikan nilai humaniora.", "Keterampilan Umum"),
    ("CPL07", "Mampu menunjukkan kinerja mandiri, bermutu, dan terukur.", "Keterampilan Umum"),
    ("CPL08", "Mampu mengkaji implikasi pengembangan atau implementasi ilmu pengetahuan dan teknologi yang memperhatikan nilai humaniora berdasarkan kaidah, tata cara, dan etika ilmiah.", "Keterampilan Umum"),
    ("CPL09", "Menyusun deskripsi saintifik hasil kajian dalam bentuk skripsi atau laporan tugas akhir, dan mengunggahnya dalam laman perguruan tinggi.", "Keterampilan Umum"),
    ("CPL10", "Bertakwa kepada Tuhan Yang Maha Esa dan mampu menunjukkan sikap religius.", "Sikap"),
    ("CPL11", "Berkontribusi dalam peningkatan mutu kehidupan bermasyarakat, berbangsa, bernegara, dan kemajuan peradaban berdasarkan Pancasila.", "Sikap"),
]
for kode, desk, aspek in CPL_DATA:
    if not db.query(CPL).filter_by(kode=kode).first():
        db.add(CPL(kode=kode, deskripsi=desk, aspek=aspek))
db.commit()
print(f"✅ CPL: {db.query(CPL).count()}")
cpl_map = {c.kode: c.id for c in db.query(CPL).all()}

# ============================================================
# 2. CPMK (33)
# ============================================================
CPMK_DATA = [
    ("CPMK011", "Mampu menerapkan konsep dasar matematika dalam komputasi.", "CPL01"),
    ("CPMK012", "Mampu menerapkan konsep dasar computing, termasuk pemrograman dan algoritma, dalam penyelesaian masalah komputasi.", "CPL01"),
    ("CPMK013", "Mampu menerapkan ilmu pengetahuan lain yang mendukung komputasi, seperti teknologi informasi dan jaringan.", "CPL01"),
    ("CPMK014", "Mampu menganalisis permasalahan computing yang kompleks menggunakan pendekatan teknologi informasi.", "CPL01"),
    ("CPMK021", "Mampu menganalisis permasalahan computing yang kompleks.", "CPL02"),
    ("CPMK022", "Mampu mengidentifikasi permasalahan computing yang kompleks.", "CPL02"),
    ("CPMK023", "Mampu mendefinisikan permasalahan computing yang kompleks.", "CPL02"),
    ("CPMK024", "Mampu memberikan pendekatan teknologi informasi sebagai solusi penyelesaian permasalahan.", "CPL02"),
    ("CPMK031", "Mampu merancang solusi berbasis computing yang sesuai dengan kebutuhan.", "CPL03"),
    ("CPMK032", "Mampu mengimplementasi solusi berbasis computing sesuai dengan solusi teknologi informasi yang diusulkan.", "CPL03"),
    ("CPMK033", "Mampu mengevaluasi solusi berbasis computing menggunakan sumberdaya, sarana, dan cara-cara computing modern.", "CPL03"),
    ("CPMK041", "Mampu memilih infrastruktur teknologi informasi yang sesuai untuk menyelesaikan permasalahan computing yang kompleks.", "CPL04"),
    ("CPMK042", "Mampu mengintegrasikan infrastruktur teknologi informasi sebagai solusi penyelesaian permasalahan computing yang kompleks.", "CPL04"),
    ("CPMK043", "Mampu mengadministrasikan infrastruktur teknologi informasi secara efektif.", "CPL04"),
    ("CPMK051", "Mampu mengimplementasikan sistem dan informasi yang didistribusikan melalui jaringan komputer.", "CPL05"),
    ("CPMK052", "Mampu mengelola sistem dan informasi yang didistribusikan melalui jaringan komputer.", "CPL05"),
    ("CPMK053", "Mampu mengamankan sistem dan informasi yang didistribusikan melalui jaringan komputer untuk menjamin kerahasiaan, integritas, dan ketersediaan informasi.", "CPL05"),
    ("CPMK061", "Mampu menerapkan pemikiran logis dalam pengembangan atau implementasi IPTEK.", "CPL06"),
    ("CPMK062", "Mampu menerapkan pemikiran kritis dalam pengembangan atau implementasi IPTEK.", "CPL06"),
    ("CPMK063", "Mampu menerapkan pemikiran sistematis dalam pengembangan atau implementasi IPTEK.", "CPL06"),
    ("CPMK064", "Mampu menerapkan pemikiran inovatif dalam pengembangan atau implementasi IPTEK yang sesuai nilai humaniora.", "CPL06"),
    ("CPMK071", "Mampu menunjukkan kinerja mandiri dalam berbagai tugas dan proyek.", "CPL07"),
    ("CPMK072", "Mampu menghasilkan pekerjaan yang bermutu tinggi.", "CPL07"),
    ("CPMK073", "Mampu memastikan hasil kerja yang terukur sesuai dengan standar yang ditetapkan.", "CPL07"),
    ("CPMK081", "Mampu mengkaji implikasi pengembangan IPTEK yang memperhatikan nilai humaniora.", "CPL08"),
    ("CPMK082", "Mampu menerapkan nilai humaniora dalam implementasi IPTEK.", "CPL08"),
    ("CPMK083", "Mampu menghasilkan solusi, gagasan, desain, atau kritik seni berdasarkan kaidah, tata cara, dan etika ilmiah.", "CPL08"),
    ("CPMK091", "Mampu menyusun deskripsi saintifik hasil kajian dalam bentuk skripsi atau laporan tugas akhir.", "CPL09"),
    ("CPMK092", "Mampu mengunggah skripsi atau laporan tugas akhir dalam laman perguruan tinggi sesuai prosedur.", "CPL09"),
    ("CPMK101", "Mampu menunjukkan sikap bertakwa kepada Tuhan YME dalam kehidupan sehari-hari.", "CPL10"),
    ("CPMK102", "Mampu menunjukkan sikap religius dalam berbagai aktivitas akademik dan non-akademik.", "CPL10"),
    ("CPMK111", "Mampu berkontribusi dalam peningkatan mutu kehidupan bermasyarakat berdasarkan Pancasila.", "CPL11"),
    ("CPMK112", "Mampu berkontribusi dalam peningkatan mutu kehidupan berbangsa dan bernegara berdasarkan Pancasila.", "CPL11"),
    ("CPMK113", "Mampu berkontribusi dalam kemajuan peradaban berdasarkan Pancasila.", "CPL11"),
]
for kode, desk, cpl_kode in CPMK_DATA:
    if not db.query(CPMK).filter_by(kode=kode).first():
        db.add(CPMK(kode=kode, deskripsi=desk, cpl_id=cpl_map[cpl_kode]))
db.commit()
print(f"✅ CPMK: {db.query(CPMK).count()}")
cpmk_map = {c.kode: c.id for c in db.query(CPMK).all()}

# ============================================================
# 3. MK (60)
# ============================================================
MK_DATA = [
    ("MK001", "Pendidikan Agama", 2, 1), ("MK002", "Pendidikan Pancasila", 2, 1),
    ("TI001", "Bahasa Inggris I", 2, 1), ("MK003", "Etika Profesi", 2, 1),
    ("TI002", "Matematika Diskrit", 2, 1), ("TI003", "Interaksi Manusia dan Komputer", 2, 1),
    ("TI004", "Pemrograman Dasar", 3, 1), ("TI005", "Pengantar Teknologi Informasi", 2, 1),
    ("MA001", "Teknologi Visualisasi", 3, 1),
    ("TI006", "Bahasa Inggris II", 2, 2), ("TI007", "Teknik Basis Data", 3, 2),
    ("TI008", "Sistem Operasi", 3, 2), ("TI009", "Algoritma dan Struktur Data", 3, 2),
    ("MA002", "Fotografi", 2, 2), ("TI010", "Fundamental Pemrograman Objek", 3, 2),
    ("TI011", "Statistik dan Probabilitas", 2, 2), ("MA003", "Kewirausahaan", 2, 2),
    ("TI012", "Jaringan Komputer", 3, 3), ("TI013", "Teknologi Platform", 2, 3),
    ("TI014", "Pemrograman Berorientasi Objek", 3, 3), ("TI015", "Desain Web", 3, 3),
    ("MA004", "Teknologi Visualisasi Lanjut", 3, 3), ("MA005", "Komputer Grafis", 2, 3),
    ("TI016", "Dasar-Dasar Integrasi Sistem", 2, 3), ("MK004", "Pendidikan Kewarganegaraan", 2, 3),
    ("TI017", "Kecerdasan Buatan", 3, 4), ("TI018", "E-business", 2, 4),
    ("MA006", "Pemodelan Visual", 3, 4), ("TI019", "Pemrograman Web", 3, 4),
    ("TI020", "Etika dan Hukum Siber", 2, 4), ("TI021", "UI/UX", 3, 4),
    ("TI022", "Analisis Kinerja Sistem", 2, 4), ("TI023", "Manajemen Infrastruktur Digital", 2, 4),
    ("TI024", "Big Data", 2, 5), ("TI025", "Cloud Computing", 3, 5),
    ("TI026", "Manajemen Proyek Teknologi Informasi", 2, 5), ("TI027", "Internet of Things", 3, 5),
    ("TI028", "Cyber Security", 2, 5), ("TI029", "E-commerce", 2, 5),
    ("MP001", "Visualisasi 3D Interaktif", 3, 5), ("MP002", "Pemodelan Visual Lanjut", 3, 5),
    ("MP003", "Pengembangan Berbasis Web", 3, 5), ("MP004", "Pengembangan Aplikasi Mobile", 3, 5),
    ("TI030", "Metodologi Penelitian", 2, 6), ("TI031", "Manajemen Bisnis Berbasis Data", 2, 6),
    ("TI032", "Manajemen Infrastruktur Virtual", 3, 6), ("MK005", "Bahasa Indonesia", 2, 6),
    ("TI033", "Virtual Reality", 3, 6), ("TI034", "Pemrograman Client Server", 3, 6),
    ("MP005", "Proyek Visualisasi", 3, 6), ("MP006", "Proyek Aplikasi Berbasis Platform (RPL)", 3, 6),
    ("TI035", "Sistem Cerdas", 3, 7), ("MA007", "Technopreneur", 2, 7),
    ("TI036", "Publikasi dan Pemasaran", 2, 7), ("TI037", "Data Science", 3, 7),
    ("MA008", "Interpersonal Skill", 2, 7), ("TI038", "Backup dan Pemulihan Data", 2, 7),
    ("TI039", "Pengelolaan Data IoT", 2, 7),
    ("TI040", "Skripsi", 6, 8), ("TI041", "KKN", 4, 8),
]
for kode, nama, sks, smt in MK_DATA:
    if not db.query(MK).filter_by(kode=kode).first():
        db.add(MK(kode=kode, nama=nama, sks=sks, semester=smt))
db.commit()
print(f"✅ MK: {db.query(MK).count()}")
mk_map = {m.kode: m.id for m in db.query(MK).all()}

# ============================================================
# 4. Sub-CPMK (56)
# ============================================================
SUB_CPMK_DATA = [
    ("Sub-CPMK01", "Mampu menulis program sederhana menggunakan bahasa pemrograman dasar.", "CPMK032"),
    ("Sub-CPMK02", "Mampu menggunakan variabel dan tipe data dasar dalam pemrograman.", "CPMK032"),
    ("Sub-CPMK03", 'Mampu membuat keputusan sederhana dalam program menggunakan struktur kontrol seperti "if" dan "loop".', "CPMK032"),
    ("Sub-CPMK04", "Mampu membuat fungsi sederhana untuk memecah program menjadi bagian-bagian kecil.", "CPMK032"),
    ("Sub-CPMK01", "Mampu menginstal sistem operasi dengan prosedur yang benar dan sesuai standar.", "CPMK021"),
    ("Sub-CPMK02", "Mampu menjalankan dan mengelola sistem pada sistem operasi dengan efektif dan efisien.", "CPMK021"),
    ("Sub-CPMK03", "Mampu mendeteksi dan mengatasi permasalahan dasar dalam kinerja sistem operasi.", "CPMK021"),
    ("Sub-CPMK04", "Mampu mengidentifikasi dan menyelesaikan masalah umum dalam manajemen file.", "CPMK021"),
    ("Sub-CPMK01", "Mampu menginstal dan mengkonfigurasi perangkat jaringan dengan benar sesuai standar industri.", "CPMK051"),
    ("Sub-CPMK02", "Mampu mengimplementasikan dan mengelola jaringan lokal (LAN) dan jaringan luas (WAN).", "CPMK051"),
    ("Sub-CPMK03", "Mampu mengkonfigurasi protokol jaringan untuk memastikan distribusi data yang aman dan efisien.", "CPMK051"),
    ("Sub-CPMK04", "Mampu mengidentifikasi dan menyelesaikan permasalahan umum dalam jaringan komputer.", "CPMK051"),
    ("Sub-CPMK01", "Mampu menjelaskan konsep dasar dan teori terkait integrasi sistem.", "CPMK042"),
    ("Sub-CPMK02", "Mampu memahami teori dan prinsip-prinsip interoperabilitas antar sistem.", "CPMK042"),
    ("Sub-CPMK03", "Mampu mengidentifikasi dan menganalisis berbagai pendekatan teoretis dalam integrasi sistem.", "CPMK042"),
    ("Sub-CPMK04", "Mampu menguraikan langkah-langkah teoretis untuk mengatasi tantangan integrasi sistem.", "CPMK042"),
    ("Sub-CPMK01", "Mampu menjelaskan konsep dasar etika dan hukum dalam konteks siber.", "CPMK062"),
    ("Sub-CPMK02", "Mampu menganalisis kasus-kasus pelanggaran etika dan hukum dalam dunia siber.", "CPMK062"),
    ("Sub-CPMK03", "Mampu mengidentifikasi isu-isu etis yang kompleks dalam pengembangan TI.", "CPMK062"),
    ("Sub-CPMK04", "Mampu menguraikan prinsip-prinsip etika profesional dalam penerapan TI.", "CPMK062"),
    ("Sub-CPMK01", "Mampu menjelaskan konsep dasar dan teori big data dalam evaluasi solusi computing.", "CPMK033"),
    ("Sub-CPMK02", "Mampu memahami prinsip-prinsip analisis data besar untuk evaluasi sistem.", "CPMK033"),
    ("Sub-CPMK03", "Mampu mengidentifikasi metode teoretis dalam pengolahan dan evaluasi data besar.", "CPMK033"),
    ("Sub-CPMK04", "Mampu menganalisis dampak dan manfaat penggunaan big data dalam evaluasi computing.", "CPMK033"),
    ("Sub-CPMK05", "Mampu menjelaskan konsep dasar big data untuk solusi berbasis ilmiah.", "CPMK113"),
    ("Sub-CPMK06", "Mampu memahami prinsip-prinsip desain dan analisis data besar.", "CPMK113"),
    ("Sub-CPMK07", "Mampu mengidentifikasi metode teoretis untuk mengolah data besar secara ilmiah.", "CPMK113"),
    ("Sub-CPMK08", "Mampu menerapkan prinsip-prinsip etika ilmiah dalam analisis data besar.", "CPMK113"),
    ("Sub-CPMK01", "Mampu menjelaskan konsep dasar keamanan jaringan dan prinsip-prinsip utama perlindungan informasi.", "CPMK053"),
    ("Sub-CPMK02", "Mampu memahami teori ancaman dan kerentanan yang mempengaruhi CIA triad.", "CPMK053"),
    ("Sub-CPMK03", "Mampu mengidentifikasi metode teoretis untuk menerapkan langkah-langkah keamanan.", "CPMK053"),
    ("Sub-CPMK04", "Mampu menganalisis strategi keamanan berdasarkan standar industri dan etika ilmiah.", "CPMK053"),
    ("Sub-CPMK01", "Mampu menjelaskan konsep dasar dan teori infrastruktur TI dalam manajemen virtual.", "CPMK041"),
    ("Sub-CPMK02", "Mampu memahami kriteria teoretis dalam pemilihan infrastruktur TI.", "CPMK041"),
    ("Sub-CPMK03", "Mampu mengidentifikasi jenis-jenis infrastruktur virtual dan keunggulannya.", "CPMK041"),
    ("Sub-CPMK04", "Mampu mengaplikasikan teori dalam pemilihan infrastruktur TI melalui studi kasus.", "CPMK041"),
    ("Sub-CPMK05", "Mampu melakukan konfigurasi dasar pada infrastruktur virtual yang dipilih.", "CPMK041"),
    ("Sub-CPMK06", "Mampu mengevaluasi efektivitas infrastruktur TI melalui pengujian praktis.", "CPMK041"),
    ("Sub-CPMK01", "Mampu menjelaskan konsep dasar dan strategi teori dalam publikasi dan pemasaran produk digital.", "CPMK072"),
    ("Sub-CPMK02", "Mampu memahami teori-teori pemasaran efektif untuk produk kreatif dan teknologi.", "CPMK072"),
    ("Sub-CPMK03", "Mampu menganalisis pasar sasaran dan strategi positioning produk digital.", "CPMK072"),
    ("Sub-CPMK04", "Mampu mengidentifikasi elemen penting dalam pembuatan rencana publikasi dan pemasaran.", "CPMK072"),
    ("Sub-CPMK01", "Mampu merumuskan masalah penelitian dan mengembangkan tujuan penelitian dalam skripsi.", "CPMK092"),
    ("Sub-CPMK02", "Mampu menyusun kerangka teori dan tinjauan pustaka sebagai dasar ilmiah.", "CPMK092"),
    ("Sub-CPMK03", "Mampu memilih dan menerapkan metode penelitian yang tepat.", "CPMK092"),
    ("Sub-CPMK04", "Mampu menganalisis data penelitian dan menyajikan hasil sesuai standar akademik.", "CPMK092"),
    ("Sub-CPMK01", "Mampu memahami konsep dasar etika profesi dalam bidang teknologi.", "CPMK061"),
    ("Sub-CPMK02", "Mampu menjelaskan pentingnya logika dalam pengambilan keputusan etis.", "CPMK061"),
    ("Sub-CPMK03", "Mampu mengidentifikasi contoh penerapan etika profesi dalam situasi nyata.", "CPMK061"),
    ("Sub-CPMK04", "Mampu menjelaskan standar dasar etika profesional yang relevan.", "CPMK061"),
    ("Sub-CPMK01", "Mampu memahami peran Bahasa Indonesia sebagai pemersatu bangsa.", "CPMK112"),
    ("Sub-CPMK02", "Mampu menjelaskan pentingnya penggunaan Bahasa Indonesia yang baik dan benar.", "CPMK112"),
    ("Sub-CPMK03", "Mampu mengidentifikasi kontribusi Bahasa Indonesia dalam membangun karakter bangsa.", "CPMK112"),
    ("Sub-CPMK04", "Mampu menjelaskan bagaimana Bahasa Indonesia mendukung nilai-nilai Pancasila.", "CPMK112"),
    ("Sub-CPMK01", "Mampu memahami teori dasar visualisasi dalam konteks multimedia dan humaniora.", "CPMK081"),
    ("Sub-CPMK02", "Mampu mengidentifikasi dampak teknologi visualisasi terhadap aspek sosial budaya.", "CPMK081"),
    ("Sub-CPMK03", "Mampu mengaplikasikan prinsip desain visualisasi yang mempertimbangkan humaniora.", "CPMK081"),
    ("Sub-CPMK04", "Mampu menganalisis dan mengevaluasi karya multimedia.", "CPMK081"),
    ("Sub-CPMK01", "Mampu menjelaskan teori dan konsep dasar proyek aplikasi berbasis platform.", "CPMK091"),
    ("Sub-CPMK02", "Mampu mendokumentasikan proses pengembangan aplikasi secara sistematis.", "CPMK091"),
    ("Sub-CPMK03", "Mampu menganalisis hasil proyek aplikasi dan menyajikan temuan saintifik.", "CPMK091"),
    ("Sub-CPMK04", "Mampu menyusun kesimpulan dan rekomendasi berdasarkan kajian ilmiah.", "CPMK091"),
]
for kode, desk, cpmk_kode in SUB_CPMK_DATA:
    cid = cpmk_map.get(cpmk_kode)
    if cid and not db.query(SubCPMK).filter_by(kode=kode, cpmk_id=cid).first():
        db.add(SubCPMK(kode=kode, deskripsi=desk, cpmk_id=cid))
db.commit()
print(f"✅ Sub-CPMK: {db.query(SubCPMK).count()}")

# ============================================================
# 5. Relasi CPMK <-> MK (68 pasang)
# ============================================================
CPMK_MK_MAP = {
    "CPMK011": ["TI011", "TI002"], "CPMK012": ["TI009", "TI010"],
    "CPMK013": ["TI005"], "CPMK014": ["TI009"],
    "CPMK021": ["TI008", "TI022"], "CPMK022": ["TI007"],
    "CPMK023": ["TI031"], "CPMK024": ["TI027"],
    "CPMK031": ["TI039", "MP003", "TI015"],
    "CPMK032": ["TI034", "TI019", "MP004", "TI014", "TI004"],
    "CPMK033": ["TI035", "TI017", "TI024", "TI037"],
    "CPMK041": ["TI032", "TI013"], "CPMK042": ["TI027", "TI016"],
    "CPMK043": ["TI023"], "CPMK051": ["TI025", "TI012"],
    "CPMK052": ["TI038"], "CPMK053": ["TI028"],
    "CPMK061": ["MK003"], "CPMK062": ["TI020"],
    "CPMK063": ["MA008"], "CPMK064": ["MA008"],
    "CPMK071": ["MA003", "MA007"], "CPMK072": ["TI036", "TI003"],
    "CPMK073": ["TI030", "TI018"],
    "CPMK081": ["TI033", "MA001", "MP001"],
    "CPMK082": ["TI021", "MA002", "MA006"],
    "CPMK083": ["TI029", "MA004", "MA005", "MP002"],
    "CPMK091": ["MP006", "MP005"], "CPMK092": ["TI040"],
    "CPMK101": ["MK001"], "CPMK102": ["MK001"],
    "CPMK111": ["MK002", "MK004"], "CPMK112": ["MK005", "TI041"],
    "CPMK113": ["TI024", "TI001", "TI006"],
}
for cpmk_kode, mk_list in CPMK_MK_MAP.items():
    cpmk = db.query(CPMK).filter_by(kode=cpmk_kode).first()
    if cpmk:
        for mk_kode in mk_list:
            mk = db.query(MK).filter_by(kode=mk_kode).first()
            if mk and mk not in cpmk.mk_list:
                cpmk.mk_list.append(mk)
db.commit()
print(f"✅ Relasi CPMK↔MK: {sum(len(c.mk_list) for c in db.query(CPMK).all())}")

# ============================================================
# 6. Komponen Penilaian (13)
# ============================================================
KOMPONEN_DATA = [
    ("PART", "Partisipasi", "observasi", "Keaktifan dalam perkuliahan dan praktikum"),
    ("TUGAS_IND", "Tugas Teori (Individu)", "observasi", "Tugas teori individu"),
    ("TUGAS_KLG", "Tugas Teori (Kelompok)", "observasi", "Tugas teori kelompok"),
    ("KUIS", "Kuis", "tes_tulis", "Kuis singkat di kelas"),
    ("UNJUK_KRJ", "Unjuk Kerja (Presentasi)", "unjuk_kerja", "Presentasi hasil tugas/proyek"),
    ("UTS", "Tes Tulis (UTS)", "tes_tulis", "Ujian Tengah Semester"),
    ("UAS", "Tes Tulis (UAS)", "tes_tulis", "Ujian Akhir Semester"),
    ("PRKT_IND", "Tugas Praktikum (Individu)", "praktik", "Praktikum individu"),
    ("PRKT_KLG", "Tugas Praktikum (Kelompok)", "praktik", "Praktikum kelompok"),
    ("RESPONSI", "Responsi", "praktik", "Sesi responsi/tutorial"),
    ("PROJECT_IND", "Project Individu", "praktik", "Proyek akhir individual"),
    ("TES_LISAN", "Tes Lisan (Tugas Kelompok)", "tes_lisan", "Presentasi lisan"),
    ("OBSERVASI", "Observasi (Praktek)", "observasi", "Observasi langsung praktik"),
]
for kode, nama, kat, desk in KOMPONEN_DATA:
    if not db.query(KomponenPenilaian).filter_by(kode=kode).first():
        db.add(KomponenPenilaian(kode=kode, nama=nama, kategori=kat, deskripsi=desk))
db.commit()
print(f"✅ Komponen Penilaian: {db.query(KomponenPenilaian).count()}")

# ============================================================
# 7. User Admin Default
# ============================================================
if not db.query(User).filter_by(username="admin").first():
    db.add(User(
        username="admin",
        password_hash=hash_password("admin123"),
        role="admin",
    ))
if not db.query(User).filter_by(username="dewi").first():
    db.add(User(
        username="dewi",
        password_hash=hash_password("dosen123"),
        role="dosen",
    ))
if not db.query(User).filter_by(username="budi").first():
    db.add(User(
        username="budi",
        password_hash=hash_password("mhs123"),
        role="mahasiswa",
    ))
db.commit()
print(f"✅ Users: {db.query(User).count()}")

# ============================================================
# Ringkasan
# ============================================================
print("\n" + "=" * 60)
print("✅ SEED DATA SELESAI")
print("=" * 60)
print(f"  CPL      : {db.query(CPL).count()}")
print(f"  CPMK     : {db.query(CPMK).count()}")
print(f"  Sub CPMK : {db.query(SubCPMK).count()}")
print(f"  MK       : {db.query(MK).count()}")
print(f"  Komponen : {db.query(KomponenPenilaian).count()}")
print(f"  Users    : {db.query(User).count()}")
print("=" * 60)
print("Login default:")
print("  admin / admin123   (Admin Prodi)")
print("  dewi  / dosen123   (Dosen Pengampu)")
print("  budi  / mhs123     (Mahasiswa)")
print("=" * 60)

db.close()