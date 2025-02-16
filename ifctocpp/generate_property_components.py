def map_to_cpp_type(data_type, property_value_kind):
    """
    Map 'DataType' + 'PropertyValueKind' to an optimized C++ type.
    For example:
      - data_type='BOOLEAN', property_value_kind='Single' -> bool
      - data_type='INTEGER', property_value_kind='Single' -> int
      - data_type='REAL',    property_value_kind='Single' -> double
      - ...
      - property_value_kind='List' -> std::vector<...> (if we wanted array types)
      - property_value_kind='Complex' -> std::string (placeholder or reference?)
    """
    dt = (data_type or "").upper()
    pk = (property_value_kind or "").upper()

    if pk == "LIST":
        base_type = "std::string"
        if dt == "BOOLEAN":
            base_type = "bool"
        elif dt == "INTEGER":
            base_type = "int"
        elif dt == "REAL":
            base_type = "double"
        return f"std::vector<{base_type}>"

    if pk == "SINGLE":
        if dt == "BOOLEAN":
            return "bool"
        elif dt == "INTEGER":
            return "int"
        elif dt == "REAL":
            return "double"
        elif dt == "STRING":
            return "std::string"
        return "std::string"

    if pk == "COMPLEX":
        return "std::string"

    # fallback
    return "std::string"


def generate_property_header(properties, enum_map):
    """
    Generate text for IfcPropertyComponents.h in the IFC namespace:
      - If a property has AllowedValues (enum), do NOT generate it.
      - Do not write any initial comment line.
    """
    lines = []
    lines.append("#ifndef IFC_PROPERTY_COMPONENTS_H")
    lines.append("#define IFC_PROPERTY_COMPONENTS_H")
    lines.append("")
    lines.append("namespace IFC {\n")

    for prop in properties:
        prop_code = prop.get("Code", "UnnamedProperty")
        description = prop.get("Description", "").strip()
        data_type = prop.get("DataType", "")  # e.g. 'BOOLEAN', 'REAL'
        prop_value_kind = prop.get("PropertyValueKind", "")  # e.g. 'Single', 'List'
        allowed_values = prop.get("AllowedValues", [])

        # Skip properties that are enums
        if allowed_values:
            continue

        if description:
            lines.append(f"// {description}")

        cpp_type = map_to_cpp_type(data_type, prop_value_kind)
        lines.append(f"struct {prop_code} {{ {cpp_type} value; }};")
        lines.append("")  # blank line

    lines.append("} // namespace IFC")
    lines.append("")
    lines.append("#endif // IFC_PROPERTY_COMPONENTS_H\n")
    return "\n".join(lines)
