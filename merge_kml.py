import os
import json
import re

def extract_kml_data(folder_path):
    all_features = []
    
    if not os.path.exists(folder_path):
        print(f"Dossier '{folder_path}' introuvable.")
        return {"type": "FeatureCollection", "features": []}

    for filename in os.listdir(folder_path):
        if filename.endswith(".kml"):
            file_path = os.path.join(folder_path, filename)
            print(f"Traitement de : {filename}")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # On cherche tous les blocs <Placemark>...</Placemark>
                placemarks = re.findall(r'<Placemark>.*?</Placemark>', content, re.DOTALL)
                
                for pm in placemarks:
                    # Extraction du nom
                    name_match = re.search(r'<name>(.*?)</name>', pm)
                    name = name_match.group(1) if name_match else "Radar"
                    
                    # Extraction des coordonnées
                    coord_match = re.search(r'<coordinates>(.*?)</coordinates>', pm)
                    if coord_match:
                        coords = coord_match.group(1).strip().split(',')
                        if len(coords) >= 2:
                            lon, lat = float(coords[0]), float(coords[1])
                            
                            feature = {
                                "type": "Feature",
                                "properties": {
                                    "source": filename,
                                    "name": name
                                },
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [lon, lat]
                                }
                            }
                            all_features.append(feature)
            except Exception as e:
                print(f"Erreur sur {filename} : {e}")
                
    return {
        "type": "FeatureCollection",
        "features": all_features
    }

if __name__ == "__main__":
    folder = "data" 
    output_file = "radars_complet.json"
    
    data = extract_kml_data(folder)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Terminé : {len(data['features'])} points extraits.")
