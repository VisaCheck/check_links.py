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

    for row in reader:
        if not row:
            continue # sla lege waarde over
            
        url = row[0].strip()
        if not url:
            continue # sla lege waarde over

        try:
            response = requests.get(
                url,
                timeout=5,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            print(f"{url} → {response.status_code}")

        except requests.exceptions.Timeout:
            print(f"{url} → TIMEOUT")

        except requests.exceptions.ConnectionError:
            print(f"{url} → DOWN")

        except Exception:
            print(f"{url} → ERROR")
