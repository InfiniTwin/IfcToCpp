def collect_enums(properties):
    """
    Gather all 'AllowedValues' from properties.
    Returns a dict { propertyCode -> list_of_raw_values }.
    We do NOT rename the code to "...Enum", so if a property
    is 'PoleUsage', we'll just call the struct 'PoleUsage'.
    """
    enum_map = {}
    for prop in properties:
        prop_code = prop.get("Code", "UnnamedProperty")
        allowed = prop.get("AllowedValues", [])
        if allowed:
            # We'll produce a struct named exactly prop_code
            enumerators = []
            for val in allowed:
                # Keep the raw string exactly as is
                raw_value = val.get("Value", "UNKNOWN")
                enumerators.append(raw_value)
            enum_map[prop_code] = enumerators
    return enum_map


def sanitize_identifier(name):
    """
    Convert a raw string (like '1P', '3PN') into a valid C++ identifier,
    used as the static field name. We'll prefix with underscore if it
    starts with a digit, etc.
    """
    if not name:
        return "UNKNOWN"

    result = []
    # If first char is digit, prefix underscore:
    if name[0].isdigit():
        result.append('_')

    for ch in name:
        # Keep alphanumeric or underscore; else convert to '_'
        if ch.isalnum() or ch == '_':
            result.append(ch)
        else:
            result.append('_')

    return "".join(result).upper()


def generate_enum_header(enum_map):
    """
    Generates IfcEnumComponents.h, but actually produces
    structs of static constexpr const char* for each property code.
    """
    lines = []
    lines.append("#ifndef IFC_ENUM_COMPONENTS_H")
    lines.append("#define IFC_ENUM_COMPONENTS_H")
    lines.append("")
    lines.append("namespace IFC {\n")
    lines.append("// ===== AUTO-GENERATED ENUM-STRINGS =====\n")

    for prop_code, values in enum_map.items():
        lines.append(f"struct {prop_code} {{")
        for val in values:
            identifier = sanitize_identifier(val)
            # We keep the raw string exactly the same
            lines.append(f'    static constexpr const char* {identifier} = "{val}";')
        lines.append("};\n")

    lines.append("} // namespace IFC")
    lines.append("")
    lines.append("#endif // IFC_ENUM_COMPONENTS_H\n")
    return "\n".join(lines)
