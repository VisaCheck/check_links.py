import requests
import csv
import time

# 🌍 KEYWORDS (MULTI LANGUAGE)
KEYWORDS_MULTI = {
    "tier1": {
        "en": {
            "core": [
                "visa requirements", "visa required", "visa free", "visa-free",
                "visa on arrival", "evisa", "e-visa", "entry requirements",
                "visa policy", "visa waiver"
            ]
        },
        "nl": {
            "core": ["visumvereisten", "visum nodig", "visumvrij", "visum bij aankomst"]
        },
        "es": {
            "core": ["requisitos de visa", "visa requerida", "sin visa", "visa a la llegada"]
        },
        "fr": {
            "core": ["conditions de visa", "visa requis", "sans visa"]
        },
        "de": {
            "core": ["visum erforderlich", "visumfrei"]
        },
        "pt": {
            "core": ["visto necessário", "isento de visto"]
        },
        "ar": {
            "core": ["متطلبات التأشيرة", "بدون تأشيرة"]
        }
    },
    "tier2": {
        "zh": {"core": ["签证要求", "免签", "落地签", "电子签证"]},
        "ru": {"core": ["визовые требования", "без визы"]},
        "hi": {"core": ["वीजा आवश्यक", "वीजा मुक्त"]},
        "id": {"core": ["persyaratan visa", "bebas visa"]}
    },
    "tier3": {
        "tr": {"core": ["vize gerekli", "vizesiz"]}
    }
}

# 🌍 LANDEN (JOUW VOLLEDIGE LIJST)
COUNTRIES = {
    "netherlands": ["netherlands", "holland"],
    "belgium": ["belgium"],
    "germany": ["germany", "deutschland"],
    "france": ["france"],
    "spain": ["spain", "españa"],
    "italy": ["italy", "italia"],
    "united states": ["usa", "us", "united states", "america"],
    "china": ["china"],
    "india": ["india"],
    "brazil": ["brazil", "brasil"],
    "south korea": ["south korea", "korea"],
    "turkey": ["turkey", "türkiye"],
    "russia": ["russia"],
    "japan": ["japan"],
    "indonesia": ["indonesia"],
    "thailand": ["thailand"],
    "mexico": ["mexico"],
    "egypt": ["egypt"],
    "south africa": ["south africa"],
    "australia": ["australia"],
    "canada": ["canada"],
    "united arab emirates": ["uae"],
    "saudi arabia": ["saudi arabia"],
    "argentina": ["argentina"],
    "nigeria": ["nigeria"]
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
    if "签证" in text:
        return "ZH"
    if "виза" in text:
        return "RU"
    if "वीजा" in text:
        return "HI"
    if "pasaporte" in text:
        return "ES"
    if "passeport" in text:
        return "FR"
    if "reisepass" in text:
        return "DE"
    if "visum" in text:
        return "NL"
    if "passport" in text:
        return "EN"
    return "UNKNOWN"

# 🧠 VISA DETECTIE (MULTI LANGUAGE)
def detect_visa_status(text):

    patterns = {
        "NO_VISA": [
            "visa free", "visa-free", "visumvrij", "sin visa",
            "sans visa", "免签", "без визы", "vizesiz"
        ],
        "VOA": [
            "visa on arrival", "visum bij aankomst",
            "visa a la llegada", "落地签", "виза по прибытии"
        ],
        "E_VISA": [
            "e-visa", "evisa", "电子签证"
        ],
        "VISA_REQUIRED": [
            "visa required", "visum nodig",
            "visa requerida", "需要签证"
        ]
    }

    for status, words in patterns.items():
        if any(w in text for w in words):
            return status

    return "UNKNOWN"

# 🌍 COUNTRY DETECTIE (SMART)
def detect_country(url, text):
    combined = (url + " " + text).lower()

    best_match = "UNKNOWN"
    max_hits = 0

    for country, aliases in COUNTRIES.items():
        hits = sum(1 for alias in aliases if alias in combined)

        if hits > max_hits:
            max_hits = hits
            best_match = country.upper()

    return best_match

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
        "url",
        "country",
        "language",
        "status_code",
        "score",
        "confidence",
        "visa_status"
    ])

    next(reader)

    for row in reader:

        url = row[0].strip()

        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla"})
            text = r.text.lower()

            # 🔎 keywords
            found_words = []
            for word in KEYWORDS:
                if word in text:
                    found_words.append(word)

            score = calculate_score(found_words)
            visa_status = detect_visa_status(text)
            confidence = get_confidence(score, visa_status)
            country = detect_country(url, text)
            language = detect_language(text)

            if score < 3:
                print(f"{url} → SKIP")
                continue

            print(f"{url} | {country} | {visa_status} | {confidence}")

            writer.writerow([
                url,
                country,
                language,
                r.status_code,
                score,
                confidence,
                visa_status
            ])

            time.sleep(1)

        except Exception as e:
            print(f"{url} → ERROR")
            writer.writerow([
                url, "UNKNOWN", "UNKNOWN",
                "ERROR", 0, "LOW", "ERROR"
            ])
