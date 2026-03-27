import os
import json
import csv

def run():
    all_features = []
    seen = set()
    data_dir = "data"

    if not os.path.exists(data_dir):
        print(f"Erreur : Le dossier '{data_dir}' est introuvable.")
        return

    for filename in sorted(os.listdir(data_dir)):
        if not filename.endswith(".csv"):
            continue

        path = os.path.join(data_dir, filename)
        speed = "".join(filter(str.isdigit, filename)) or "N/A"
        count = 0

        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 3:
                        continue
                    try:
                        lon = float(row[0].strip())
                        lat = float(row[1].strip())
                        name = row[2].strip().replace('"', '')
                    except ValueError:
                        continue

                    key = (round(lon, 6), round(lat, 6))
                    if key in seen:
                        continue
                    seen.add(key)

                    all_features.append({
                        "type": "Feature",
                        "properties": {
                            "nom": name,
                            "vitesse": speed
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [lon, lat]
                        }
                    })
                    count += 1

            print(f"  {filename} → {count} radars")

        except Exception as e:
            print(f"Erreur sur {filename}: {e}")

    output_path = "radars_complet.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(
            {"type": "FeatureCollection", "features": all_features},
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"\nSuccès : {len(all_features)} radars extraits → {output_path}")

if __name__ == "__main__":
    run()
