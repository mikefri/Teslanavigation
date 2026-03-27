import os
import json
import csv

def run():
    all_features = []
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        print(f"Erreur : Le dossier '{data_dir}' est introuvable.")
        return

    for filename in os.listdir(data_dir):
        if filename.endswith(".csv"):
            path = os.path.join(data_dir, filename)
            try:
                # 'errors=ignore' évite de planter si un caractère spécial est mal codé
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        # On vérifie qu'il y a bien au moins 3 colonnes (Lon, Lat, Nom)
                        if len(row) >= 3:
                            try:
                                lon = float(row[0].strip())
                                lat = float(row[1].strip())
                                name = row[2].strip().replace('"', '')
                                
                                all_features.append({
                                    "type": "Feature",
                                    "properties": {
                                        "nom": name,
                                        "vitesse": "".join(filter(str.isdigit, filename)) or "N/A"
                                    },
                                    "geometry": {
                                        "type": "Point",
                                        "coordinates": [lon, lat]
                                    }
                                })
                            except ValueError:
                                continue # Saute la ligne si ce ne sont pas des chiffres
            except Exception as e:
                print(f"Erreur sur {filename}: {e}")

    # Création du fichier final
    with open("radars_complet.json", "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": all_features}, f, ensure_ascii=False)
    
    print(f"Succès : {len(all_features)} radars extraits des fichiers CSV.")

if __name__ == "__main__":
    run()
