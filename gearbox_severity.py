"""gearbox_severity.py

Basit bir gearbox condition scoring aracı.

Girdi parametreleri:
- fe_ppm (int): Oil analysis iron (Fe) ppm
- pitting (yes/no): Borescope ile pitting görülüyor mu?
- vibration (float): Titreşim hızı (mm/s)
- temperature (float): Sıcaklık (°C)

Severity üretim kuralları (istenen):
- Fe < 40            -> normal
- 40–80              -> elevated
- 80–120             -> high
- >120               -> critical
- pitting=yes ise minimum severity = 3
- final severity 1–5 arası

Not: Bu sürümde vibration/temperature değerleri severity hesabına katılmaz;
CLI çıktısında bağlam/uyarı amaçlı raporlanır.
"""

from __future__ import annotations

import argparse
import json


def classify_fe(fe_ppm: int) -> str:
    if fe_ppm < 40:
        return "normal"
    if fe_ppm <= 80:
        return "elevated"
    if fe_ppm <= 120:
        return "high"
    return "critical"


def base_severity_from_fe_class(fe_class: str) -> int:
    # Basit mapping: 4 sınıfı 1–5 ölçeğine oturtuyoruz.
    # (3 seviyesi pitting varsa devreye giriyor.)
    mapping = {
        "normal": 1,
        "elevated": 2,
        "high": 4,
        "critical": 5,
    }
    try:
        return mapping[fe_class]
    except KeyError as e:
        raise ValueError(f"Unknown fe_class: {fe_class}") from e


def compute_severity(*, fe_ppm: int, pitting: str) -> tuple[int, str]:
    fe_class = classify_fe(fe_ppm)
    severity = base_severity_from_fe_class(fe_class)

    pitting_norm = pitting.strip().lower()
    if pitting_norm not in {"yes", "no"}:
        raise ValueError("pitting must be yes/no")

    if pitting_norm == "yes":
        severity = max(severity, 3)

    severity = max(1, min(5, severity))
    return severity, fe_class


def recommendation_for_severity(severity: int) -> str:
    rec_map = {
        1: "Normal: rutin izleme yeterli.",
        2: "Elevated: izleme sıklığını artır ve Fe trendini takip et.",
        3: "Kontrollü izleme: (ör.) 3 ayda bir takip + borescope/yağ analizi.",
        4: "Yüksek risk: kısa vadede müdahale planla (detaylı titreşim + yağ analizi).",
        5: "Kritik: mümkünse durdurma ve acil inceleme/onarım.",
    }
    return rec_map.get(severity, "")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Gearbox severity (1–5) hesaplar ve öneri üretir."
    )
    p.add_argument("--fe-ppm", type=int, required=True, help="Oil iron (Fe) ppm")
    p.add_argument(
        "--pitting",
        type=str,
        required=True,
        choices=["yes", "no"],
        help="Pitting var mı? (yes/no)",
    )
    p.add_argument(
        "--vibration",
        type=float,
        required=True,
        help="Vibration (mm/s) (bilgi amaçlı)",
    )
    p.add_argument(
        "--temperature",
        type=float,
        required=True,
        help="Temperature (°C) (bilgi amaçlı)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="JSON çıktı üret (text output yerine)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    severity, fe_class = compute_severity(fe_ppm=args.fe_ppm, pitting=args.pitting)
    rec = recommendation_for_severity(severity)

    if args.json:
        payload = {
            "severity": severity,
            "fe_class": fe_class,
            "recommendation": rec,
            "context": {
                "pitting": args.pitting,
                "vibration": args.vibration,
                "temperature": args.temperature,
            },
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(f"Severity: {severity}/5")
    print(f"Fe class: {fe_class} ({args.fe_ppm} ppm)")
    print(f"Recommendation: {rec}")
    print(
        f"Context: pitting={args.pitting}, vibration={args.vibration} mm/s, temperature={args.temperature} °C"
    )


if __name__ == "__main__":
    main()
