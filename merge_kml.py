import os
import json
import xml.etree.ElementTree as ET

def extract_kml_data(folder_path):
    all_features = []
    
    # Parcourir tous les fichiers du dossier
    for filename in os.listdir(folder_path):
        if filename.endswith(".kml"):
            tree = ET.parse(os.path.join(folder_path, filename))
            root = tree.getroot()
            
            # Gestion des espaces de noms KML
            ns = {'kml': 'http://www.opengis.net/kml/2.2'}
            
            # On cherche tous les points (Placemark)
            for pm in root.findall('.//kml:Placemark', ns):
                name = pm.find('kml:name', ns)
                coords = pm.find('.//kml:coordinates', ns)
                
                if coords is not None:
                    # Nettoyage des coordonnées (long,lat,alt)
                    c_text = coords.text.strip().split(',')
                    if len(c_text) >= 2:
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
    
    return {
        "type": "FeatureCollection",
        "features": all_features
    }

# Execution
if __name__ == "__main__":
    folder = "data" # Nom de votre répertoire contenant les KML
    output_file = "radars_complet.json"
    
    data = extract_kml_data(folder)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Fusion terminée : {len(data['features'])} points compilés dans {output_file}")
