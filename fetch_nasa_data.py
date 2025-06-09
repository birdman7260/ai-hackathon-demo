# fetch_nasa_data.py
import os, requests
URLS = {
  "nasa_se_handbook.pdf":
    "https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf",
  "artemis_i_press_kit.pdf":
    "https://www.nasa.gov/wp-content/uploads/static/artemis-i-press-kit/img/Artemis%20I_Press%20Kit.pdf",
  "clps_press_kit.pdf":
    "https://www.nasa.gov/wp-content/uploads/2024/01/np-2023-12-016-jsc-clps-im-press-kit-web-508.pdf",
}
os.makedirs("data", exist_ok=True)
for fn, url in URLS.items():
    print(f"↓ {fn}")
    with open(f"data/{fn}", "wb") as f:
        f.write(requests.get(url, timeout=90).content)
print("NASA docs ready → ./data")