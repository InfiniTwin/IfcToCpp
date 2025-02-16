import sys
import os
import json

from .generate_enums import collect_enums, generate_enum_header
from .generate_class_components import generate_class_header
from .generate_property_components import generate_property_header

def main():
    if len(sys.argv) < 3:
        print(f"Usage: python -m ifctocpp <IFC.json> <output_folder>")
        sys.exit(1)

    ifc_json_path = sys.argv[1]
    out_folder = sys.argv[2]

    # Make sure output folder exists
    if not os.path.isdir(out_folder):
        os.makedirs(out_folder, exist_ok=True)

    # Load IFC.json
    with open(ifc_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract arrays
    classes = data.get("Classes", [])
    properties = data.get("Properties", [])

    # 1) Gather enumerations
    enum_map = collect_enums(properties)

    # 2) Generate IfcEnumComponents.h
    enum_header = generate_enum_header(enum_map)
    enum_file_path = os.path.join(out_folder, "IfcEnums.h")
    with open(enum_file_path, "w", encoding="utf-8") as ef:
        ef.write(enum_header)

    # 3) Generate IfcClassComponents.h
    class_header = generate_class_header(classes)
    class_file_path = os.path.join(out_folder, "IfcClassComponents.h")
    with open(class_file_path, "w", encoding="utf-8") as cf:
        cf.write(class_header)

    # 4) Generate IfcPropertyComponents.h
    property_header = generate_property_header(properties, enum_map)
    property_file_path = os.path.join(out_folder, "IfcPropertyComponents.h")
    with open(property_file_path, "w", encoding="utf-8") as pf:
        pf.write(property_header)

    print("[INFO] Generated the following files:")
    print("  " + enum_file_path)
    print("  " + class_file_path)
    print("  " + property_file_path)

if __name__ == "__main__":
    main()

# If you install this as a package with a console script entry point,
# Python will call main() automatically. If you run via:
#    python -m ifctocpp IFC.json out_folder
# it also calls main().
