import requests
import csv
import time

# 🔧 CONFIG
LIMIT = 20   # zet op None voor alles

# 🌍 KEYWORDS (MULTI LANGUAGE)
KEYWORDS_MULTI = {
    "tier1": {
        "en": {"core": [
            "visa requirements", "visa required", "visa free", "visa-free",
            "visa on arrival", "evisa", "e-visa", "entry requirements",
            "visa policy", "visa waiver", "tourism visa", "visa", "etias", "voa",
            "work visa", "student", "student visa", "business visa", "eta", "etias",
            "visa on arrival", "VOA"
        ]},
        "nl": {"core": [
            "visum", "visumvereisten", "visum nodig", "visumvrij",
            "visum bij aankomst", "toeristenvisum", "werkvisum",
            "studentenvisum", "paspoort", "toegangseisen"
        ]},
        "es": {"core": [
            "requisitos de visa", "visa requerida", "sin visa",
            "visa a la llegada", "visado", "student visas", "visas"
        ]},
        "fr": {"core": [
            "conditions de visa", "visa requis", "sans visa"
        ]},
        "de": {"core": [
            "visum", "visum erforderlich", "visumfrei"
        ]},
        "pt": {"core": [
            "visto", "visto necessário", "isento de visto"
        ]},
        "it": {"core": [
            "visto", "visto richiesto"
        ]},
        "tr": {"core": [
            "vize", "vize gerekli", "vize muafiyeti"
        ]},
        "ru": {"core": [
            "виза", "виза требуется", "безвизовый"
        ]},
        "zh": {"core": [
            "签证", "免签", "落地签"
        ]}
    },
    "tier2": {
        "hi": {"core": ["वीजा", "वीजा आवश्यक"]},
        "id": {"core": ["visa", "bebas visa"]},
        "th": {"core": ["วีซ่า"]},
        "vi": {"core": ["thị thực"]}
    }
}

# 🔧 Flatten keywords
def flatten_keywords(k):
    flat = []
    for tier in k.values():
        for lang in tier.values():
            for cat in lang.values():
                flat.extend(cat)
    return list(set(flat))

KEYWORDS = flatten_keywords(KEYWORDS_MULTI)

# 🌍 LANGUAGE DETECTIE
def detect_language(text):
    if "签证" in text: return "ZH"
    if "виза" in text: return "RU"
    if "वीजा" in text: return "HI"
    if "visum" in text: return "NL"
    if "visa" in text: return "EN"
    return "UNKNOWN"

# 🧠 VISA STATUS
def detect_visa_status(text):
    if "visa free" in text or "visumvrij" in text: return "NO_VISA"
    if "visa on arrival" in text: return "VOA"
    if "e-visa" in text or "evisa" in text: return "E_VISA"
    if "visa required" in text: return "VISA_REQUIRED"
    return "UNKNOWN"

# 📊 SCORE
def calculate_score(found_words):
    return len(found_words)

# 🎯 CONFIDENCE
def get_confidence(score, visa_status):
    if visa_status != "UNKNOWN" and score >= 5:
        return "HIGH"
    elif score >= 3:
        return "MEDIUM"
    else:
        return "LOW"

print("🚀 START\n")

with open("urls.csv", newline="", encoding="utf-8") as infile, \
     open("results.csv", "w", newline="", encoding="utf-8") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    writer.writerow([
        "url", "language", "status_code",
        "score", "confidence", "visa_status"
    ])

    next(reader)

    for i, row in enumerate(reader):

        if LIMIT and i >= LIMIT:
            break

        if not row:
            continue

        url = row[0].strip()

        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla"})
            text = r.text.lower()

            found_words = [word for word in KEYWORDS if word in text]

            score = calculate_score(found_words)
            visa_status = detect_visa_status(text)
            confidence = get_confidence(score, visa_status)
            language = detect_language(text)

            print(f"\n🔗 {url}")
            print(f"🌍 {language} | 📊 score={score} | 🎯 {confidence} | 🛂 {visa_status}")

            writer.writerow([
                url,
                language,
                r.status_code,
                score,
                confidence,
                visa_status
            ])

            time.sleep(1)

        except Exception:
            print(f"{url} → ERROR")
            writer.writerow([url, "UNKNOWN", "ERROR", 0, "LOW", "ERROR"])
