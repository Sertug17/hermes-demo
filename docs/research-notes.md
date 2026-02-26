# Research Notes — NousResearch/hermes-agent (PR #80, PR #70, Issue #54)

Kaynak repo: https://github.com/NousResearch/hermes-agent

Bu notlar; PR #80, PR #70 ve Issue #54 içeriklerini (açıklamalar + diff/patch) okuyup teknik özet çıkarmak için hazırlanmıştır.

---

## Issue #54 — “Clarification: Where is the current Notion integration implemented?”

- Problem: Repoda Notion entegrasyonunun **nerede/ nasıl** uygulandığı belirsiz bulunmuş.
  - `tools/` altında native bir Python tool görülmemiş.
  - “MCP mi, dış connector mı, LLM-skill prompting mi?” soruları sorulmuş.
- Yorumlar:
  - `mrshu`, mevcut Notion entegrasyonunun `skills/productivity/notion/SKILL.md` içinde olduğuna işaret ediyor.
  - Issue yazarı (Sertug17) devamında: bunun sadece **skill-level prompting** olup olmadığını, yoksa altta bir backend/tool olup olmadığını netleştirmek istiyor.

Özet: Issue #54, Notion entegrasyonunun “tool mu / skill mi?” ayrımındaki dokümantasyon eksikliğini gündeme getiriyor.

---

## PR #70 — “Clarify Notion skill execution model and architecture”

PR linki: https://github.com/NousResearch/hermes-agent/pull/70

Değişiklik:
- `skills/productivity/notion/SKILL.md` dosyasına **Architecture & Execution Model** başlığı ekleniyor.

Teknik mesaj:
- Notion entegrasyonu **command layer**’da çalışıyor:
  - Terminal üzerinden `curl` ile doğrudan Notion API çağrıları.
  - Bu yüzden `tools/` altında Notion için dedicated bir Python backend tool’a dayanmıyor.
- Çalışma biçimleri (dokümante edilen):
  1) Terminal-driven API calls (`curl`)
  2) LLM-guided command generation
  3) İsteğe bağlı `jq` gibi araçlara pipe ederek çıktıyı yapılandırma
- Not: İleride native Python tool veya MCP connector gelirse doküman güncellenebilir.
- Amaç: “skill-level integration (prompt + shell)” ile “native tool-level integration (Python registry tools)” ayrımını netleştirmek.

Özet: PR #70, Issue #54’teki belirsizliği gidermek için Notion skill’inin **tool değil, shell/curl tabanlı skill** olduğunu açıkça yazıyor.

---

## PR #80 — “Add Wind Turbine Gearbox Maintenance Intelligence skill (v1)”

PR linki: https://github.com/NousResearch/hermes-agent/pull/80

Kapsam:
- Yeni bir domain-specific skill ekliyor (enerji / rüzgar türbini bakımı odaklı).
- Eklenen dosyalar:
  - `docs/adventures/wind-turbine-gearbox-intelligence.md` (senaryo + örnek çalışma / “adventure log”)
  - `skills/energy/wind-turbine-gearbox-intelligence/SKILL.md` (yeniden kullanılabilir skill tanımı)

Skill’in amacı:
- Rüzgar türbini gearbox condition assessment için karar destek çıktısı üretmek.
- Sinyaller:
  - Borescope / görsel bulgular
  - Yağ analizi (Fe ppm)
  - Vibration durumu
  - Sıcaklık anomalileri

İçerik/kurallar:
- Başlangıçta desteklenen model: **Sinovel SL1500** (genişletilebilir olarak belirtilmiş).
- Fault mode örnekleri: main bearing pitting, spalling, surface fatigue, lubrication degradation indicators.
- Severity Index (1–5) ölçeği tanımlı.
  - Önemli kural: “confirmed pitting” varsa (vibration normal olsa bile) **minimum severity = 3**.
- Oil Iron (Fe ppm) sınıflaması:
  - < 40 → Normal
  - 40–80 → Elevated
  - 80–120 → High
  - > 120 → Critical
- Çıktı formatı (decision output):
  - Root cause
  - Severity index
  - Shutdown recommendation
  - Monitoring interval
  - Escalation triggers

Örnek senaryo (adventure log + skill example):
- Girdi:
  - Main bearing rotor-side pitting
  - Vibration: anomaly yok
  - Oil Fe: 54 ppm
- Örnek çıktı:
  - Severity: 3/5
  - Shutdown: No
  - Monitoring: Quarterly (3 ay)
  - Trigger’lar: Fe > 80 ppm, vibration onset, belirgin temperature drift

Not:
- Skill, condition-based maintenance desteği için tasarlanmış.
- OEM önerileri / mühendislik değerlendirmesinin yerine geçmediği açıkça yazılmış.

---

## Genel Teknik Çıkarımlar

1) Hermes’te entegrasyonlar her zaman `tools/` gibi native backend’lere bağlı değil; bazıları “skill + terminal komutları (curl)” olarak çalışıyor.
2) Bu ayrım dokümante edilmediğinde Issue #54 benzeri belirsizlikler oluşabiliyor; PR #70 bu boşluğu hedefliyor.
3) PR #80, skill sisteminin domain-specific karar iş akışlarını (eşikler, sınıflandırma, structured output, escalation trigger’lar) paketleyebildiğini gösteren bir örnek.
