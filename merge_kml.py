import os
import json
import re

def extract_kml_data(folder_path):
    all_features = []
    
    if not os.path.exists(folder_path):
        return {"type": "FeatureCollection", "features": []}

    for filename in os.listdir(folder_path):
        if filename.endswith(".kml"):
            # Extraction de la vitesse depuis le nom du fichier (ex: 110 depuis FRFixeFR110.kml)
            vitesse_match = re.search(r'(\d+)', filename)
            vitesse = vitesse_match.group(1) if vitesse_match else "Inconnue"
            
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Extraction par bloc Placemark
                placemarks = re.findall(r'<Placemark>.*?</Placemark>', content, re.DOTALL)
                
                for pm in placemarks:
                    name_match = re.search(r'<name>(.*?)</name>', pm)
                    name = name_match.group(1) if name_match else "Radar"
                    
                    coord_match = re.search(r'<coordinates>(.*?)</coordinates>', pm)
                    if coord_match:
                        coords = coord_match.group(1).strip().split(',')
                        if len(coords) >= 2:
                            feature = {
                                "type": "Feature",
                                "properties": {
                                    "nom": name,
                                    "vitesse": vitesse,
                                    "type": filename.replace(".kml", "")
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [float(coords[0]), float(coords[1])]
                                }
                            }
                            all_features.append(feature)
            except Exception as e:
                print(f"Erreur sur {filename}: {e}")
                
    return {"type": "FeatureCollection", "features": all_features}

if __name__ == "__main__":
    folder = "data"
    output = "radars_complet.json"
    data = extract_kml_data(folder)
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"Succès : {len(data['features'])} radars compilés.")
