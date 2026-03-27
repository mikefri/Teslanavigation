import os
import json
import xml.etree.ElementTree as ET
import re

def extract_kml_data(folder_path):
    all_features = []
    
    if not os.path.exists(folder_path):
        print(f"Erreur : Le dossier '{folder_path}' n'existe pas.")
        return {"type": "FeatureCollection", "features": []}

    for filename in os.listdir(folder_path):
        if filename.endswith(".kml"):
            file_path = os.path.join(folder_path, filename)
            
            try:
                # Lecture brute pour nettoyer les caractères problématiques comme '&'
                with open(file_path, 'r', encoding='utf-8') as f:
                    xml_data = f.read()
                    # On remplace les '&' qui ne sont pas déjà des entités XML
                    xml_data = re.sub(r'&(?!(amp|lt|gt|apos|quot);)', '&amp;', xml_data)
                
                root = ET.fromstring(xml_data)
                
                # Namespace KML standard
                ns = {'kml': 'http://www.opengis.net/kml/2.2'}
                
                for pm in root.findall('.//kml:Placemark', ns):
                    name = pm.find('kml:name', ns)
                    coords = pm.find('.//kml:coordinates', ns)
                    
                    if coords is not None:
                        c_text = coords.text.strip().split(',')
                        if len(c_text) >= 2:
                            try:
                                lon, lat = float(c_text[0]), float(c_text[1])
                                
                                feature = {
                                    "type": "Feature",
                                    "properties": {
                                        "source": filename,
                                        "name": name.text if name is not None else "Radar"
                                    },
                                    "geometry": {
                                        "type": "Point",
                                        "coordinates": [lon, lat]
                                    }
                                }
                                all_features.append(feature)
                            except ValueError:
                                continue # Saute les coordonnées mal formées
            except Exception as e:
                print(f"Erreur lors de la lecture de {filename}: {e}")
                
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
    
    print(f"Succès : {len(data['features'])} points compilés dans {output_file}")
