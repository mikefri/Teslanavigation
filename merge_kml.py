import os
import json
import re

def extract_kml_data(folder_path):
    all_features = []
    if not os.path.exists(folder_path):
        return {"type": "FeatureCollection", "features": []}

    for filename in os.listdir(folder_path):
        if filename.endswith(".kml"):
            # On devine la vitesse depuis le nom du fichier
            v_match = re.search(r'(\d+)', filename)
            vitesse = v_match.group(1) if v_match else "Inconnu"
            
            file_path = os.path.join(folder_path, filename)
            try:
                # 'errors=ignore' est crucial pour ne pas planter sur les accents
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # On découpe chaque bloc radar manuellement
                placemarks = re.findall(r'<Placemark>.*?</Placemark>', content, re.DOTALL)
                
                for pm in placemarks:
                    # Extraction Nom
                    name_search = re.search(r'<name>(.*?)</name>', pm)
                    name = name_search.group(1) if name_search else "Radar"
                    
                    # Extraction Coordonnées
                    coord_search = re.search(r'<coordinates>(.*?)</coordinates>', pm)
                    if coord_search:
                        c = coord_search.group(1).strip().split(',')
                        if len(c) >= 2:
                            all_features.append({
                                "type": "Feature",
                                "properties": {
                                    "nom": name,
                                    "vitesse": vitesse,
                                    "type": filename.split('.')[0]
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [float(c[0]), float(c[1])]
                                }
                            })
            except Exception as e:
                print(f"Saut du fichier {filename} : {e}")
                
    return {"type": "FeatureCollection", "features": all_features}

if __name__ == "__main__":
    folder = "data" # Vérifiez que vos KML sont bien dans ce dossier
    output_file = "radars_complet.json"
    data = extract_kml_data(folder)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"OK : {len(data['features'])} radars compilés.")
