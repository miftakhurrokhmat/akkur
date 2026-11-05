"""
Seed data demo untuk uji end-to-end:
- 1 tahun akademik aktif
- 3 dosen, 3 mahasiswa
- 1 kelas TI012-A dengan konfigurasi bobot lengkap
- 1 KRS disetujui untuk Budi dengan nilai lengkap
"""
from app.database import SessionLocal
from app.models.kurikulum import CPMK, MK
from app.models.akademik import Mahasiswa, Dosen, TahunAkademik, Kelas
from app.models.krs import KRS, KRSDetail
from app.models.penilaian import (
    KomponenPenilaian, BobotKomponenMK, BobotCPMKMK,
    KonfigurasiPenilaianCPMK, NilaiKomponen,
)
from app.services.penilaian import hitung_nilai_cpmk, hitung_nilai_mk
from app.models.auth import User
from app.core.security import hash_password

db = SessionLocal()

# Tahun akademik
ta = db.query(TahunAkademik).filter_by(kode="2025/2026-Ganjil").first()
if not ta:
    ta = TahunAkademik(kode="2025/2026-Ganjil", tahun_mulai=2025,
                       semester="Ganjil", aktif=True)
    db.add(ta); db.commit()

# Dosen
dosen_data = [
    ("0512345678", "Dewi Anggraini, M.Kom", "dewi@amikom.ac.id", "Lektor"),
    ("0523456789", "Robi Prasetya, M.Kom", "robi@amikom.ac.id", "Asisten Ahli"),
    ("0534567890", "Hadis Setiawan, M.Kom", "hadis@amikom.ac.id", "Lektor Kepala"),
]
for nidn, nama, email, jab in dosen_data:
    if not db.query(Dosen).filter_by(nidn=nidn).first():
        db.add(Dosen(nidn=nidn, nama=nama, email=email, jabatan=jab))
db.commit()
dewi = db.query(Dosen).filter_by(nidn="0512345678").first()

# Mahasiswa
mhs_data = [
    ("21.01.0001", "Budi Santoso", 2021, "Teknologi Informasi"),
    ("21.01.0002", "Ani Wijaya", 2021, "Teknologi Informasi"),
    ("21.01.0003", "Cici Lestari", 2021, "Teknologi Informasi"),
]
for nim, nama, ang, prodi in mhs_data:
    if not db.query(Mahasiswa).filter_by(nim=nim).first():
        db.add(Mahasiswa(nim=nim, nama=nama, angkatan=ang, prodi=prodi))
db.commit()
budi = db.query(Mahasiswa).filter_by(nim="21.01.0001").first()

# Update user ref_id
user_budi = db.query(User).filter_by(username="budi").first()
if user_budi and not user_budi.ref_id:
    user_budi.ref_id = budi.id
user_dewi = db.query(User).filter_by(username="dewi").first()
if user_dewi and not user_dewi.ref_id:
    user_dewi.ref_id = dewi.id
db.commit()

# Kelas TI012-A
mk_ti012 = db.query(MK).filter_by(kode="TI012").first()
kelas = db.query(Kelas).filter_by(kode_kelas="TI012-A").first()
if not kelas:
    kelas = Kelas(
        mk_id=mk_ti012.id, tahun_akademik_id=ta.id,
        dosen_id=dewi.id, kode_kelas="TI012-A",
        kapasitas=40, jadwal="Senin 08:00-10:30", ruang="R301",
    )
    db.add(kelas); db.commit()

# Bobot komponen MK (Σ=100)
komp_map = {k.kode: k.id for k in db.query(KomponenPenilaian).all()}
bobot_komp = {"PART": 10, "TUGAS_IND": 20, "UTS": 30, "UAS": 40}
for kode, bobot in bobot_komp.items():
    if not db.query(BobotKomponenMK).filter_by(
        kelas_id=kelas.id, komponen_id=komp_map[kode]
    ).first():
        db.add(BobotKomponenMK(kelas_id=kelas.id,
                               komponen_id=komp_map[kode], bobot=bobot))
db.commit()

# Bobot CPMK dalam MK (Σ=100)
cpmk_map = {c.kode: c.id for c in db.query(CPMK).all()}
bobot_cpmk = {"CPMK051": 40, "CPMK052": 30, "CPMK053": 30}
for kode, bobot in bobot_cpmk.items():
    if not db.query(BobotCPMKMK).filter_by(
        kelas_id=kelas.id, cpmk_id=cpmk_map[kode]
    ).first():
        db.add(BobotCPMKMK(kelas_id=kelas.id,
                           cpmk_id=cpmk_map[kode], bobot=bobot))
db.commit()

# Konfigurasi teknik per CPMK
configs = {
    "CPMK051": [
        ("PART", "Awal", "Observasi", "Lembar kehadiran", "≥75 aktif", 25),
        ("UTS", "Tengah", "Tes tulis", "Soal uraian", "≥75", 75),
    ],
    "CPMK052": [
        ("TUGAS_IND", "Tengah", "Observasi", "Rubrik tugas", "≥70", 50),
        ("UAS", "Akhir", "Tes tulis", "Soal uraian", "≥70", 50),
    ],
    "CPMK053": [
        ("UTS", "Tengah", "Tes tulis", "Soal kasus", "≥70", 50),
        ("UAS", "Akhir", "Tes tulis", "Soal kasus", "≥70", 50),
    ],
}
for cpmk_kode, items in configs.items():
    for kode_komp, tahap, teknik, instrumen, kriteria, bobot in items:
        if not db.query(KonfigurasiPenilaianCPMK).filter_by(
            kelas_id=kelas.id, cpmk_id=cpmk_map[cpmk_kode],
            komponen_id=komp_map[kode_komp]
        ).first():
            db.add(KonfigurasiPenilaianCPMK(
                kelas_id=kelas.id, cpmk_id=cpmk_map[cpmk_kode],
                komponen_id=komp_map[kode_komp], tahap=tahap,
                teknik=teknik, instrumen=instrumen,
                kriteria=kriteria, bobot=bobot,
            ))
db.commit()

# KRS Budi
krs = db.query(KRS).filter_by(mahasiswa_id=budi.id, tahun_akademik_id=ta.id).first()
if not krs:
    krs = KRS(mahasiswa_id=budi.id, tahun_akademik_id=ta.id,
              status="disetujui", total_sks=3)
    db.add(krs); db.commit()

kd = db.query(KRSDetail).filter_by(krs_id=krs.id, kelas_id=kelas.id).first()
if not kd:
    kd = KRSDetail(krs_id=krs.id, kelas_id=kelas.id, status="aktif")
    db.add(kd); db.commit()

# Nilai Budi
nilai_budi = {"PART": 85, "TUGAS_IND": 80, "UTS": 75, "UAS": 90}
for kode, nilai in nilai_budi.items():
    if not db.query(NilaiKomponen).filter_by(
        krs_detail_id=kd.id, komponen_id=komp_map[kode]
    ).first():
        db.add(NilaiKomponen(
            krs_detail_id=kd.id, komponen_id=komp_map[kode],
            nilai=nilai, updated_by=dewi.id,
        ))
db.commit()

# Hitung nilai
cpmk_result = hitung_nilai_cpmk(db, kd.id)
mk_result = hitung_nilai_mk(db, kd.id)

print("\n" + "=" * 60)
print("✅ DEMO DATA SELESAI")
print("=" * 60)
print(f"  Tahun Akademik : {ta.kode}")
print(f"  Kelas          : {kelas.kode_kelas} ({mk_ti012.nama})")
print(f"  Mahasiswa      : {budi.nim} - {budi.nama}")
print(f"  Nilai CPMK     : {cpmk_result}")
print(f"  Nilai MK       : {mk_result}")
print("=" * 60)

db.close()