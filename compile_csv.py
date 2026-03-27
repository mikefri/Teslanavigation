import os
import json
import csv

def compile_csv_to_geojson(folder_path):
    all_features = []
    
    if not os.path.exists(folder_path):
        print(f"Dossier '{folder_path}' non trouvé.")
        return {"type": "FeatureCollection", "features": []}

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            print(f"Traitement de : {filename}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    # On utilise DictReader ou un simple reader selon la structure
                    # Votre image montre : Longitude, Latitude, "Nom"
                    reader = csv.reader(f)
                    for row in reader:
                        if len(row) >= 3:
                            try:
                                lon = float(row[0].strip())
                                lat = float(row[1].strip())
                                name = row[2].strip().replace('"', '')
                                
                                feature = {
                                    "type": "Feature",
                                    "properties": {
                                        "nom": name,
                                        "fichier_source": filename
                                    },
                                    "geometry": {
                                        "type": "Point",
                                        "coordinates": [lon, lat]
                                    }
                                }
                                all_features.append(feature)
                            except ValueError:
                                # Saute les lignes d'en-tête si elles existent
                                continue
            except Exception as e:
                print(f"Erreur sur le fichier {filename}: {e}")

    return {
        "type": "FeatureCollection",
        "features": all_features
    }

if __name__ == "__main__":
    folder = "data" 
    output_file = "radars_complet.json"
    
    geojson_data = compile_csv_to_geojson(folder)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)
    
    print(f"Succès ! {len(geojson_data['features'])} radars compilés dans {output_file}")
