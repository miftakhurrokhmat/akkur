"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-11-05
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ===== CPL =====
    op.create_table(
        'cpl',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('kode', sa.String(20), unique=True, nullable=False),
        sa.Column('deskripsi', sa.Text, nullable=False),
        sa.Column('aspek', sa.String(50)),
        sa.Column('created_at', sa.DateTime),
    )
    op.create_index('idx_cpl_kode', 'cpl', ['kode'])

    # ===== CPMK =====
    op.create_table(
        'cpmk',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('kode', sa.String(20), unique=True, nullable=False),
        sa.Column('deskripsi', sa.Text, nullable=False),
        sa.Column('cpl_id', sa.Integer, sa.ForeignKey('cpl.id', ondelete='CASCADE'),
                  nullable=False),
        sa.Column('created_at', sa.DateTime),
    )
    op.create_index('idx_cpmk_kode', 'cpmk', ['kode'])
    op.create_index('idx_cpmk_cpl', 'cpmk', ['cpl_id'])

    # ===== Sub CPMK =====
    op.create_table(
        'sub_cpmk',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('kode', sa.String(50), nullable=False),
        sa.Column('deskripsi', sa.Text, nullable=False),
        sa.Column('cpmk_id', sa.Integer, sa.ForeignKey('cpmk.id', ondelete='CASCADE'),
                  nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.UniqueConstraint('cpmk_id', 'kode'),
    )

    # ===== MK =====
    op.create_table(
        'mk',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('kode', sa.String(20), unique=True, nullable=False),
        sa.Column('nama', sa.String(200), nullable=False),
        sa.Column('sks', sa.Integer, nullable=False),
        sa.Column('semester', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime),
    )
    op.create_index('idx_mk_semester', 'mk', ['semester'])

    # ===== CPMK_MK =====
    op.create_table(
        'cpmk_mk',
        sa.Column('cpmk_id', sa.Integer, sa.ForeignKey('cpmk.id', ondelete='CASCADE'),
                  primary_key=True),
        sa.Column('mk_id', sa.Integer, sa.ForeignKey('mk.id', ondelete='CASCADE'),
                  primary_key=True),
    )

    # ===== Mahasiswa =====
    op.create_table(
        'mahasiswa',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nim', sa.String(20), unique=True, nullable=False),
        sa.Column('nama', sa.String(200), nullable=False),
        sa.Column('angkatan', sa.Integer, nullable=False),
        sa.Column('prodi', sa.String(100)),
        sa.Column('status', sa.String(20)),
        sa.Column('created_at', sa.DateTime),
    )
    op.create_index('idx_mhs_angkatan', 'mahasiswa', ['angkatan'])

    # ===== Dosen =====
    op.create_table(
        'dosen',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nidn', sa.String(20), unique=True, nullable=False),
        sa.Column('nama', sa.String(200), nullable=False),
        sa.Column('email', sa.String(100)),
        sa.Column('jabatan', sa.String(100)),
        sa.Column('created_at', sa.DateTime),
    )

    # ===== Tahun Akademik =====
    op.create_table(
        'tahun_akademik',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('kode', sa.String(30), unique=True, nullable=False),
        sa.Column('tahun_mulai', sa.Integer, nullable=False),
        sa.Column('semester', sa.String(10), nullable=False),
        sa.Column('tgl_mulai', sa.Date),
        sa.Column('tgl_selesai', sa.Date),
        sa.Column('aktif', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime),
    )

    # ===== Kelas =====
    op.create_table(
        'kelas',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('mk_id', sa.Integer, sa.ForeignKey('mk.id'), nullable=False),
        sa.Column('tahun_akademik_id', sa.Integer,
                  sa.ForeignKey('tahun_akademik.id'), nullable=False),
        sa.Column('dosen_id', sa.Integer, sa.ForeignKey('dosen.id')),
        sa.Column('kode_kelas', sa.String(20), nullable=False),
        sa.Column('kapasitas', sa.Integer, default=40),
        sa.Column('jadwal', sa.String(100)),
        sa.Column('ruang', sa.String(50)),
        sa.Column('created_at', sa.DateTime),
        sa.UniqueConstraint('mk_id', 'tahun_akademik_id', 'kode_kelas'),
    )

    # ===== KRS =====
    op.create_table(
        'krs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('mahasiswa_id', sa.Integer,
                  sa.ForeignKey('mahasiswa.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tahun_akademik_id', sa.Integer,
                  sa.ForeignKey('tahun_akademik.id'), nullable=False),
        sa.Column('tanggal_isi', sa.Date),
        sa.Column('status', sa.String(20), default='draft'),
        sa.Column('total_sks', sa.Integer, default=0),
        sa.Column('approved_by', sa.Integer, sa.ForeignKey('dosen.id')),
        sa.Column('approved_at', sa.DateTime),
        sa.Column('created_at', sa.DateTime),
        sa.UniqueConstraint('mahasiswa_id', 'tahun_akademik_id'),
    )

    # ===== KRS Detail =====
    op.create_table(
        'krs_detail',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('krs_id', sa.Integer,
                  sa.ForeignKey('krs.id', ondelete='CASCADE'), nullable=False),
        sa.Column('kelas_id', sa.Integer, sa.ForeignKey('kelas.id'), nullable=False),
        sa.Column('status', sa.String(20), default='aktif'),
        sa.Column('created_at', sa.DateTime),
        sa.UniqueConstraint('krs_id', 'kelas_id'),
    )

    # ===== Komponen Penilaian =====
    op.create_table(
        'komponen_penilaian',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('kode', sa.String(30), unique=True, nullable=False),
        sa.Column('nama', sa.String(100), nullable=False),
        sa.Column('kategori', sa.String(30)),
        sa.Column('deskripsi', sa.Text),
        sa.Column('aktif', sa.Boolean, default=True),
    )

    # ===== Bobot Komponen MK =====
    op.create_table(
        'bobot_komponen_mk',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('kelas_id', sa.Integer,
                  sa.ForeignKey('kelas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('komponen_id', sa.Integer,
                  sa.ForeignKey('komponen_penilaian.id'), nullable=False),
        sa.Column('bobot', sa.Numeric(5, 2), nullable=False),
        sa.UniqueConstraint('kelas_id', 'komponen_id'),
    )

    # ===== Bobot CPMK MK =====
    op.create_table(
        'bobot_cpmk_mk',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('kelas_id', sa.Integer,
                  sa.ForeignKey('kelas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('cpmk_id', sa.Integer, sa.ForeignKey('cpmk.id'), nullable=False),
        sa.Column('bobot', sa.Numeric(5, 2), nullable=False),
        sa.UniqueConstraint('kelas_id', 'cpmk_id'),
    )

    # ===== Konfigurasi Penilaian CPMK =====
    op.create_table(
        'konfigurasi_penilaian_cpmk',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('kelas_id', sa.Integer,
                  sa.ForeignKey('kelas.id', ondelete='CASCADE'), nullable=False),
        sa.Column('cpmk_id', sa.Integer, sa.ForeignKey('cpmk.id'), nullable=False),
        sa.Column('komponen_id', sa.Integer,
                  sa.ForeignKey('komponen_penilaian.id'), nullable=False),
        sa.Column('tahap', sa.String(50)),
        sa.Column('teknik', sa.String(100)),
        sa.Column('instrumen', sa.Text),
        sa.Column('kriteria', sa.Text),
        sa.Column('bobot', sa.Numeric(5, 2), nullable=False),
        sa.UniqueConstraint('kelas_id', 'cpmk_id', 'komponen_id'),
    )

    # ===== Nilai Komponen =====
    op.create_table(
        'nilai_komponen',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('krs_detail_id', sa.Integer,
                  sa.ForeignKey('krs_detail.id', ondelete='CASCADE'), nullable=False),
        sa.Column('komponen_id', sa.Integer,
                  sa.ForeignKey('komponen_penilaian.id'), nullable=False),
        sa.Column('nilai', sa.Numeric(5, 2)),
        sa.Column('catatan', sa.Text),
        sa.Column('updated_by', sa.Integer, sa.ForeignKey('dosen.id')),
        sa.Column('updated_at', sa.DateTime),
        sa.UniqueConstraint('krs_detail_id', 'komponen_id'),
    )

    # ===== Nilai CPMK =====
    op.create_table(
        'nilai_cpmk',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('krs_detail_id', sa.Integer,
                  sa.ForeignKey('krs_detail.id', ondelete='CASCADE'), nullable=False),
        sa.Column('cpmk_id', sa.Integer, sa.ForeignKey('cpmk.id'), nullable=False),
        sa.Column('nilai', sa.Numeric(5, 2)),
        sa.UniqueConstraint('krs_detail_id', 'cpmk_id'),
    )

    # ===== Nilai MK =====
    op.create_table(
        'nilai_mk',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('krs_detail_id', sa.Integer,
                  sa.ForeignKey('krs_detail.id', ondelete='CASCADE'),
                  nullable=False, unique=True),
        sa.Column('nilai_angka', sa.Numeric(5, 2)),
        sa.Column('nilai_huruf', sa.String(3)),
        sa.Column('bobot_nilai', sa.Numeric(4, 2)),
        sa.Column('lulus', sa.Boolean, default=False),
        sa.Column('updated_at', sa.DateTime),
    )

    # ===== Ketercapaian CPL =====
    op.create_table(
        'ketercapaian_cpl',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('mahasiswa_id', sa.Integer,
                  sa.ForeignKey('mahasiswa.id', ondelete='CASCADE'), nullable=False),
        sa.Column('cpl_id', sa.Integer, sa.ForeignKey('cpl.id'), nullable=False),
        sa.Column('tahun_akademik_id', sa.Integer,
                  sa.ForeignKey('tahun_akademik.id'), nullable=False),
        sa.Column('skor_maks', sa.Numeric(8, 2), default=0),
        sa.Column('total_skor', sa.Numeric(8, 2), default=0),
        sa.Column('nilai_rata_rata', sa.Numeric(5, 2)),
        sa.Column('status', sa.String(20)),
        sa.UniqueConstraint('mahasiswa_id', 'cpl_id', 'tahun_akademik_id'),
    )

    # ===== Users =====
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('ref_id', sa.Integer),
        sa.Column('aktif', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime),
    )


def downgrade() -> None:
    for t in [
        'users', 'ketercapaian_cpl', 'nilai_mk', 'nilai_cpmk',
        'nilai_komponen', 'konfigurasi_penilaian_cpmk', 'bobot_cpmk_mk',
        'bobot_komponen_mk', 'komponen_penilaian', 'krs_detail', 'krs',
        'kelas', 'tahun_akademik', 'dosen', 'mahasiswa',
        'cpmk_mk', 'mk', 'sub_cpmk', 'cpmk', 'cpl',
    ]:
        op.drop_table(t)