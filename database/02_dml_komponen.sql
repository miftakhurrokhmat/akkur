INSERT INTO komponen_penilaian (kode, nama, kategori, deskripsi) VALUES
('PART',       'Partisipasi',                'observasi',   'Keaktifan dalam perkuliahan'),
('TUGAS_IND',  'Tugas Teori (Individu)',    'observasi',   'Tugas teori individu'),
('TUGAS_KLG',  'Tugas Teori (Kelompok)',    'observasi',   'Tugas teori kelompok'),
('KUIS',       'Kuis',                       'tes_tulis',   'Kuis singkat'),
('UNJUK_KRJ',  'Unjuk Kerja (Presentasi)',  'unjuk_kerja', 'Presentasi'),
('UTS',        'Tes Tulis (UTS)',            'tes_tulis',   'Ujian Tengah Semester'),
('UAS',        'Tes Tulis (UAS)',            'tes_tulis',   'Ujian Akhir Semester'),
('PRKT_IND',   'Tugas Praktikum (Individu)', 'praktik',     'Praktikum individu'),
('PRKT_KLG',   'Tugas Praktikum (Kelompok)', 'praktik',     'Praktikum kelompok'),
('RESPONSI',   'Responsi',                    'praktik',     'Sesi responsi'),
('PROJECT_IND','Project Individu',             'praktik',     'Proyek akhir'),
('TES_LISAN',  'Tes Lisan (Tugas Kelompok)',  'tes_lisan',   'Presentasi lisan'),
('OBSERVASI',  'Observasi (Praktek)',         'observasi',   'Observasi praktik')
ON CONFLICT (kode) DO NOTHING;

INSERT INTO tahun_akademik (kode, tahun_mulai, semester, aktif) VALUES
('2025/2026-Ganjil', 2025, 'Ganjil', TRUE),
('2025/2026-Genap',  2025, 'Genap',  FALSE);

INSERT INTO dosen (nidn, nama, email, jabatan) VALUES
('0512345678', 'Dewi Anggraini, M.Kom', 'dewi@amikom.ac.id', 'Lektor'),
('0523456789', 'Robi Prasetya, M.Kom', 'robi@amikom.ac.id', 'Asisten Ahli');

INSERT INTO mahasiswa (nim, nama, angkatan, prodi) VALUES
('21.01.0001', 'Budi Santoso', 2021, 'Teknologi Informasi'),
('21.01.0002', 'Ani Wijaya',   2021, 'Teknologi Informasi'),
('21.01.0003', 'Cici Lestari', 2021, 'Teknologi Informasi');

INSERT INTO kelas (mk_id, tahun_akademik_id, dosen_id, kode_kelas, kapasitas, jadwal, ruang)
SELECT mk.id, ta.id, d.id, 'TI012-A', 40, 'Senin 08:00-10:30', 'R301'
FROM mk, tahun_akademik ta, dosen d
WHERE mk.kode = 'TI012'
  AND ta.kode = '2025/2026-Ganjil'
  AND d.nidn = '0512345678';

INSERT INTO bobot_komponen_mk (kelas_id, komponen_id, bobot)
SELECT k.id, kp.id, v.bobot
FROM kelas k
CROSS JOIN (VALUES
    ('PART', 10.00),
    ('TUGAS_IND', 20.00),
    ('UTS', 30.00),
    ('UAS', 40.00)
) AS v(kode, bobot)
JOIN komponen_penilaian kp ON kp.kode = v.kode
WHERE k.kode_kelas = 'TI012-A';

INSERT INTO bobot_cpmk_mk (kelas_id, cpmk_id, bobot)
SELECT k.id, c.id, v.bobot
FROM kelas k
CROSS JOIN (VALUES
    ('CPMK051', 40.00),
    ('CPMK052', 30.00),
    ('CPMK053', 30.00)
) AS v(kode, bobot)
JOIN cpmk c ON c.kode = v.kode
WHERE k.kode_kelas = 'TI012-A';