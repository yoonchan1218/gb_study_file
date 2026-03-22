"""
Edit unpacked slide XMLs directly:
1. slide3.xml: green overlay transparency
2. slide5-14: remove connectors, fix tag circles
"""
import re
import os

BASE = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\unpacked_v7\ppt\slides"

# ============================================================
# Helper: Add alpha to DBEEE0 fills in a slide XML
# ============================================================
def add_green_overlay_alpha(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find <a:srgbClr val="DBEEE0"/> and add alpha child
    # Replace self-closing tag
    content = content.replace(
        '<a:srgbClr val="DBEEE0"/>',
        '<a:srgbClr val="DBEEE0"><a:alpha val="45000"/></a:srgbClr>'
    )
    # Replace opening tag without alpha child
    # Pattern: <a:srgbClr val="DBEEE0"> without alpha following
    content = re.sub(
        r'<a:srgbClr val="DBEEE0">(?!\s*<a:alpha)',
        '<a:srgbClr val="DBEEE0"><a:alpha val="45000"/>',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  {os.path.basename(filepath)}: Added alpha to DBEEE0 fills")

# ============================================================
# Helper: Remove bentConnector shapes and fix tags
# ============================================================
def fix_slide_connectors_and_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_len = len(content)

    # Remove entire <p:cxnSp> blocks (connector shapes)
    connector_pattern = r'<p:cxnSp>.*?</p:cxnSp>'
    content = re.sub(connector_pattern, '', content, flags=re.DOTALL)

    removed = (original_len - len(content))

    # Fix tag background shapes: change rect to ellipse, make smaller
    # Tag backgrounds: shapes with fill=3A9D6E and size 256032x256032
    # Change geometry from rect to ellipse
    # Make size 164592x164592 (centered)

    def shrink_tag_shape(match):
        block = match.group(0)
        # Only process if it has 3A9D6E fill and 256032 size
        if '3A9D6E' in block and '256032' in block:
            # Change rect to ellipse
            block = block.replace('prst="rect"', 'prst="ellipse"')
            # Adjust position and size
            # Find offset and extent
            off_match = re.search(r'<a:off x="(\d+)" y="(\d+)"/>', block)
            ext_match = re.search(r'<a:ext cx="256032" cy="256032"/>', block)
            if off_match and ext_match:
                old_x = int(off_match.group(1))
                old_y = int(off_match.group(2))
                # Center the smaller shape
                delta = (256032 - 164592) // 2
                new_x = old_x + delta
                new_y = old_y + delta
                block = block.replace(
                    f'<a:off x="{old_x}" y="{old_y}"/>',
                    f'<a:off x="{new_x}" y="{new_y}"/>'
                )
                block = block.replace(
                    '<a:ext cx="256032" cy="256032"/>',
                    '<a:ext cx="164592" cy="164592"/>'
                )
        return block

    # Process each <p:sp> block
    content = re.sub(r'<p:sp>.*?</p:sp>', shrink_tag_shape, content, flags=re.DOTALL)

    # Fix tag text: make font smaller (800 = 8pt), white, bold, centered
    # Tag text shapes have single letter A-G
    def fix_tag_text(match):
        block = match.group(0)
        # Check if this is a single-letter tag text
        text_match = re.search(r'<a:t>([A-G])</a:t>', block)
        if text_match and '256032' not in block:  # Already processed bg shape
            pass  # Will be handled by the size change above
        if text_match:
            # Change font size to 800 (8pt)
            block = re.sub(r'sz="\d+"', 'sz="800"', block)
            # Ensure bold
            block = re.sub(r'(lang="[^"]*")', r'\1 b="1"', block)
            # Remove duplicate b attributes
            block = re.sub(r'b="1"\s+b="1"', 'b="1"', block)
            # Change text color to white
            # Find rPr and replace/add solidFill
            if 'val="333333"' in block or 'val="555555"' in block:
                block = block.replace('val="333333"', 'val="FFFFFF"')
                block = block.replace('val="555555"', 'val="FFFFFF"')
            # Add center alignment
            if '<a:bodyPr' in block and 'anchor="ctr"' not in block:
                block = block.replace('<a:bodyPr', '<a:bodyPr anchor="ctr" lIns="0" tIns="0" rIns="0" bIns="0"')
            if '<a:pPr' in block and 'algn="ctr"' not in block:
                block = re.sub(r'<a:pPr([^>]*?)>', r'<a:pPr algn="ctr"\1>', block)
        return block

    content = re.sub(r'<p:sp>.*?</p:sp>', fix_tag_text, content, flags=re.DOTALL)

    # Style A./B./C. labels: green bold
    def fix_label_text(match):
        block = match.group(0)
        label_match = re.search(r'<a:t>([A-G])\.</a:t>', block)
        if label_match:
            # Make bold and green
            block = re.sub(r'(sz="\d+")', r'\1 b="1"', block)
            block = re.sub(r'b="1"\s+b="1"', 'b="1"', block)
            # Change color to green
            if 'val="333333"' in block:
                block = block.replace('val="333333"', 'val="3A9D6E"')
        return block

    content = re.sub(r'<p:sp>.*?</p:sp>', fix_label_text, content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  {os.path.basename(filepath)}: removed {removed} bytes of connectors, fixed tags")

# ============================================================
# Process slides
# ============================================================
print("=== Fixing slide3.xml (green overlay alpha) ===")
add_green_overlay_alpha(os.path.join(BASE, "slide3.xml"))

print("\n=== Fixing slides 5-14 (connectors + tags) ===")
for n in range(5, 16):  # slide5 to slide15
    filepath = os.path.join(BASE, f"slide{n}.xml")
    if os.path.exists(filepath):
        fix_slide_connectors_and_tags(filepath)

print("\nDone!")
