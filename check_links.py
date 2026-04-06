import requests
import csv

# 🌍 MULTI KEYWORDS (flat maken voor matching)
from collections import defaultdict

KEYWORDS_MULTI = {
    "tier1": {
        "en": {
            "core": ["visa requirements", "visa required", "visa free", "visa on arrival", "e-visa"],
            "types": ["tourist visa", "work visa", "student visa", "business visa", "transit visa"],
            "docs": ["passport", "passport validity"],
            "process": ["visa application", "apply for visa"]
        },
        "nl": {
            "core": ["visumvereisten", "visum nodig", "visumvrij", "visum bij aankomst"],
            "types": ["toeristenvisum", "werkvisum", "studentenvisum"],
            "docs": ["paspoort"],
            "process": ["visumaanvraag"]
        }
    },
    "tier2": {
        "es": {
            "core": ["requisitos de visa", "visa requerida", "sin visa", "visa a la llegada"],
            "types": ["visa de turista", "visa de trabajo"],
            "docs": ["pasaporte"],
            "process": ["solicitud de visa"]
        }
    }
}

# 🔧 Flatten functie
def flatten_keywords(keywords_multi):
    flat = []
    for tier in keywords_multi.values():
        for lang in tier.values():
            for category in lang.values():
                flat.extend(category)
    return list(set(flat))

KEYWORDS = flatten_keywords(KEYWORDS_MULTI)

# 🧠 Visa decision engine
def detect_visa_status(text):
    text = text.lower()

    if any(x in text for x in ["visa free", "visumvrij", "sin visa"]):
        return "NO_VISA"

    if any(x in text for x in ["visa on arrival", "visum bij aankomst", "visa a la llegada"]):
        return "VOA"

    if any(x in text for x in ["e-visa", "evisa"]):
        return "E_VISA"

    if any(x in text for x in ["visa required", "visum nodig", "visa requerida"]):
        return "VISA_REQUIRED"

    return "UNKNOWN"


print("Start checking links...\n")

with open("urls.csv", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)

    LIMIT = 10

    for i, row in enumerate(reader):
        if i >= LIMIT:
            break

        if not row:
            continue

        url = row[0].strip()
        if not url:
            continue

        try:
            response = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            text = response.text.lower()

            found_words = [word for word in KEYWORDS if word in text]
            visa_status = detect_visa_status(text)

            print(f"\n{url} → {response.status_code}")

            if found_words:
                print(f"  ✅ Keywords: {len(found_words)} found")
                print(f"  🔎 Sample: {', '.join(found_words[:5])}")
            else:
                print("  ❌ No keywords found")

            print(f"  🧠 Visa status: {visa_status}")

        except requests.exceptions.Timeout:
            print(f"{url} → TIMEOUT")

        except requests.exceptions.ConnectionError:
            print(f"{url} → DOWN")

        except Exception as e:
            print(f"{url} → ERROR: {e}")
