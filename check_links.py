import requests
import csv

KEYWORDS = [
    "visa",
    "visum",
    "tourism",
    "tourist visa",
    "work visa",
    "student visa",
    "eta",
    "etias",
    "visa required",
    "passport",
    "business visa",
    "transit visa"
]

print("Start checking links...\n")

with open("urls.csv", newline="") as file:
    reader = csv.reader(file)
    next(reader)

    for i, row in enumerate(reader):
    if i >= 10:
        break
        
        if not row:
            continue # sla lege waarde over
            
        url = row[0].strip()
        if not url:
            continue # sla lege waarde over

   try:
    response = requests.get(
        url,
        timeout=10,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    text = response.text.lower()

    found_words = [word for word in KEYWORDS if word in text]

    print(f"\n{url} → {response.status_code}")

    if found_words:
        print(f"  ✅ Found: {', '.join(found_words)}")
    else:
        print("  ❌ No keywords found")

        except requests.exceptions.Timeout:
            print(f"{url} → TIMEOUT")

        except requests.exceptions.ConnectionError:
            print(f"{url} → DOWN")

        except Exception:
            print(f"{url} → ERROR")
