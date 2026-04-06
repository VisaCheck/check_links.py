import requests
import csv

print("Start checking links...\n")

with open("urls.csv", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        url = row["url"]

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
