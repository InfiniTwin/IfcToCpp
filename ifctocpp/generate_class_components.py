def strip_ifc_prefix(name: str) -> str:
    """
    If the class code starts with 'Ifc', remove that prefix.
    E.g. 'IfcWall' -> 'Wall', 'IfcDoor' -> 'Door', etc.
    """
    if name.startswith("Ifc"):
        return name[3:]  # remove the first 3 characters
    return name

def generate_class_header(classes):
    """
    Generate text for IfcClassComponents.h:
    - Each IFC class becomes a single-line empty struct.
    - If 'Definition' is non-empty, add a comment.
    - Remove 'Ifc' prefix from the class Code.
    - Wrap in namespace IFC.
    """
    lines = []
    lines.append("#ifndef IFC_CLASS_COMPONENTS_H")
    lines.append("#define IFC_CLASS_COMPONENTS_H")
    lines.append("")
    lines.append("namespace IFC {\n")
    lines.append("// ===== AUTO-GENERATED CLASSES =====\n")

    for cls in classes:
        code = cls.get("Code", "UnnamedClass")
        definition = cls.get("Definition", "").strip()

        # remove "Ifc" if present
        stripped_code = strip_ifc_prefix(code)

        if definition:
            lines.append(f"// {definition}")
        # Single-line empty struct
        lines.append(f"struct {stripped_code} {{}};")
        lines.append("")  # blank line

    lines.append("} // namespace IFC")
    lines.append("")
    lines.append("#endif // IFC_CLASS_COMPONENTS_H\n")
    return "\n".join(lines)
