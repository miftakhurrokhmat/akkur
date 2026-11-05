from decimal import Decimal

# Konversi sesuai standar umum (bisa diubah prodi)
KONVERSI_HURUF = [
    (85, "A",  Decimal("4.00")),
    (80, "A-", Decimal("3.75")),
    (75, "B+", Decimal("3.50")),
    (70, "B",  Decimal("3.00")),
    (65, "B-", Decimal("2.75")),
    (60, "C+", Decimal("2.50")),
    (55, "C",  Decimal("2.00")),
    (45, "D",  Decimal("1.00")),
    (0,  "E",  Decimal("0.00")),
]


def angka_ke_huruf(nilai: float) -> tuple[str, Decimal, bool]:
    """Return (huruf, bobot, lulus)."""
    for batas, huruf, bobot in KONVERSI_HURUF:
        if nilai >= batas:
            return huruf, bobot, huruf not in ("D", "E")
    return "E", Decimal("0.00"), False