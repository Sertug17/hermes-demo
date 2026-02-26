# Hermes Demo (Python)

Bu depo, GitHub akışını test etmek için hazırlanmış basit bir Python projesidir.

## Çalıştırma

Python 3 ile:

```bash
python main.py
```

Beklenen çıktı:

```
Hermes GitHub testi başarılı
```

## Gearbox Severity Tool

`gearbox_severity.py`, yağ analizi (Fe ppm) + pitting bilgisine göre 1–5 arası severity üretir ve kısa bir öneri yazar.

Parametreler:
- `--fe-ppm` (int)
- `--pitting` (yes/no)
- `--vibration` (float, mm/s) (bu sürümde bilgi amaçlı)
- `--temperature` (float, °C) (bu sürümde bilgi amaçlı)

Örnek:

```bash
python gearbox_severity.py --fe-ppm 54 --pitting yes --vibration 0.8 --temperature 65
```
