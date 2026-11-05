-- ===== CPL =====
CREATE TABLE cpl (
    id SERIAL PRIMARY KEY,
    kode VARCHAR(20) UNIQUE NOT NULL,
    deskripsi TEXT NOT NULL,
    aspek VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_cpl_kode ON cpl(kode);

-- ===== CPMK =====
CREATE TABLE cpmk (
    id SERIAL PRIMARY KEY,
    kode VARCHAR(20) UNIQUE NOT NULL,
    deskripsi TEXT NOT NULL,
    cpl_id INT NOT NULL REFERENCES cpl(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_cpmk_cpl ON cpmk(cpl_id);

-- ===== SubCPMK =====
CREATE TABLE sub_cpmk (
    id SERIAL PRIMARY KEY,
    kode VARCHAR(50) NOT NULL,
    deskripsi TEXT NOT NULL,
    cpmk_id INT NOT NULL REFERENCES cpmk(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(cpmk_id, kode)
);

-- ===== MK =====
CREATE TABLE mk (
    id SERIAL PRIMARY KEY,
    kode VARCHAR(20) UNIQUE NOT NULL,
    nama VARCHAR(200) NOT NULL,
    sks INT NOT NULL CHECK (sks > 0),
    semester INT NOT NULL CHECK (semester BETWEEN 1 AND 8),
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_mk_semester ON mk(semester);

-- ===== CPMK_MK (many-to-many) =====
CREATE TABLE cpmk_mk (
    cpmk_id INT NOT NULL REFERENCES cpmk(id) ON DELETE CASCADE,
    mk_id INT NOT NULL REFERENCES mk(id) ON DELETE CASCADE,
    PRIMARY KEY (cpmk_id, mk_id)
);

-- ===== Mahasiswa =====
CREATE TABLE mahasiswa (
    id SERIAL PRIMARY KEY,
    nim VARCHAR(20) UNIQUE NOT NULL,
    nama VARCHAR(200) NOT NULL,
    angkatan INT NOT NULL,
    prodi VARCHAR(100),
    status VARCHAR(20) DEFAULT 'aktif',
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_mhs_angkatan ON mahasiswa(angkatan);

-- ===== Dosen =====
CREATE TABLE dosen (
    id SERIAL PRIMARY KEY,
    nidn VARCHAR(20) UNIQUE NOT NULL,
    nama VARCHAR(200) NOT NULL,
    email VARCHAR(100),
    jabatan VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ===== TahunAkademik =====
CREATE TABLE tahun_akademik (
    id SERIAL PRIMARY KEY,
    kode VARCHAR(30) UNIQUE NOT NULL,
    tahun_mulai INT NOT NULL,
    semester VARCHAR(10) NOT NULL CHECK (semester IN ('Ganjil', 'Genap')),
    tgl_mulai DATE,
    tgl_selesai DATE,
    aktif BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ===== Kelas =====
CREATE TABLE kelas (
    id SERIAL PRIMARY KEY,
    mk_id INT NOT NULL REFERENCES mk(id),
    tahun_akademik_id INT NOT NULL REFERENCES tahun_akademik(id),
    dosen_id INT REFERENCES dosen(id),
    kode_kelas VARCHAR(20) NOT NULL,
    kapasitas INT DEFAULT 40,
    jadwal VARCHAR(100),
    ruang VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(mk_id, tahun_akademik_id, kode_kelas)
);

-- ===== KRS =====
CREATE TABLE krs (
    id SERIAL PRIMARY KEY,
    mahasiswa_id INT NOT NULL REFERENCES mahasiswa(id) ON DELETE CASCADE,
    tahun_akademik_id INT NOT NULL REFERENCES tahun_akademik(id),
    tanggal_isi DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'draft',
    total_sks INT DEFAULT 0,
    approved_by INT REFERENCES dosen(id),
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(mahasiswa_id, tahun_akademik_id)
);

-- ===== KRSDetail =====
CREATE TABLE krs_detail (
    id SERIAL PRIMARY KEY,
    krs_id INT NOT NULL REFERENCES krs(id) ON DELETE CASCADE,
    kelas_id INT NOT NULL REFERENCES kelas(id),
    status VARCHAR(20) DEFAULT 'aktif',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(krs_id, kelas_id)
);

-- ===== KomponenPenilaian =====
CREATE TABLE komponen_penilaian (
    id SERIAL PRIMARY KEY,
    kode VARCHAR(30) UNIQUE NOT NULL,
    nama VARCHAR(100) NOT NULL,
    kategori VARCHAR(30),
    deskripsi TEXT,
    aktif BOOLEAN DEFAULT TRUE
);

-- ===== BobotKomponenMK =====
CREATE TABLE bobot_komponen_mk (
    id SERIAL PRIMARY KEY,
    kelas_id INT NOT NULL REFERENCES kelas(id) ON DELETE CASCADE,
    komponen_id INT NOT NULL REFERENCES komponen_penilaian(id),
    bobot NUMERIC(5,2) NOT NULL CHECK (bobot BETWEEN 0 AND 100),
    UNIQUE(kelas_id, komponen_id)
);

-- ===== BobotCPMKMK =====
CREATE TABLE bobot_cpmk_mk (
    id SERIAL PRIMARY KEY,
    kelas_id INT NOT NULL REFERENCES kelas(id) ON DELETE CASCADE,
    cpmk_id INT NOT NULL REFERENCES cpmk(id),
    bobot NUMERIC(5,2) NOT NULL CHECK (bobot BETWEEN 0 AND 100),
    UNIQUE(kelas_id, cpmk_id)
);

-- ===== KonfigurasiPenilaianCPMK =====
CREATE TABLE konfigurasi_penilaian_cpmk (
    id SERIAL PRIMARY KEY,
    kelas_id INT NOT NULL REFERENCES kelas(id) ON DELETE CASCADE,
    cpmk_id INT NOT NULL REFERENCES cpmk(id),
    komponen_id INT NOT NULL REFERENCES komponen_penilaian(id),
    tahap VARCHAR(50),
    teknik VARCHAR(100),
    instrumen TEXT,
    kriteria TEXT,
    bobot NUMERIC(5,2) NOT NULL,
    UNIQUE(kelas_id, cpmk_id, komponen_id)
);

-- ===== NilaiKomponen =====
CREATE TABLE nilai_komponen (
    id SERIAL PRIMARY KEY,
    krs_detail_id INT NOT NULL REFERENCES krs_detail(id) ON DELETE CASCADE,
    komponen_id INT NOT NULL REFERENCES komponen_penilaian(id),
    nilai NUMERIC(5,2) CHECK (nilai BETWEEN 0 AND 100),
    catatan TEXT,
    updated_by INT REFERENCES dosen(id),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(krs_detail_id, komponen_id)
);

-- ===== NilaiCPMK =====
CREATE TABLE nilai_cpmk (
    id SERIAL PRIMARY KEY,
    krs_detail_id INT NOT NULL REFERENCES krs_detail(id) ON DELETE CASCADE,
    cpmk_id INT NOT NULL REFERENCES cpmk(id),
    nilai NUMERIC(5,2),
    UNIQUE(krs_detail_id, cpmk_id)
);

-- ===== NilaiMK =====
CREATE TABLE nilai_mk (
    id SERIAL PRIMARY KEY,
    krs_detail_id INT NOT NULL UNIQUE REFERENCES krs_detail(id) ON DELETE CASCADE,
    nilai_angka NUMERIC(5,2),
    nilai_huruf VARCHAR(3),
    bobot_nilai NUMERIC(4,2),
    lulus BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ===== KetercapaianCPL =====
CREATE TABLE ketercapaian_cpl (
    id SERIAL PRIMARY KEY,
    mahasiswa_id INT NOT NULL REFERENCES mahasiswa(id) ON DELETE CASCADE,
    cpl_id INT NOT NULL REFERENCES cpl(id),
    tahun_akademik_id INT NOT NULL REFERENCES tahun_akademik(id),
    skor_maks NUMERIC(8,2) DEFAULT 0,
    total_skor NUMERIC(8,2) DEFAULT 0,
    nilai_rata_rata NUMERIC(5,2),
    status VARCHAR(20),
    UNIQUE(mahasiswa_id, cpl_id, tahun_akademik_id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    ref_id INT,
    aktif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_users_username ON users(username);