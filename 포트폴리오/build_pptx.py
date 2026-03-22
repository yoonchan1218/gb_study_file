"""
Build final portfolio PPTX via direct ZIP editing.
No python-pptx save() - only zip read/modify/write.
"""
import zipfile
import re
import os
import struct

BASE = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오"
SRC = os.path.join(BASE, "김윤찬_TRY-CATCH_화면_포트폴리오_v6.pptx")
DST = os.path.join(BASE, "김윤찬_TRY-CATCH_화면_포트폴리오_DONE.pptx")
SCREENSHOTS = os.path.join(BASE, "screenshots", "final")

# ── Step 1: Read entire ZIP into memory ──────────────────────────────────────
zin = zipfile.ZipFile(SRC, 'r')
file_data = {}
file_info = {}
for info in zin.infolist():
    file_data[info.filename] = zin.read(info.filename)
    file_info[info.filename] = info
zin.close()
print(f"Read {len(file_data)} entries from source PPTX")

# ── Helper: decode/encode XML entries ────────────────────────────────────────
def get_xml(name):
    return file_data[name].decode('utf-8')

def set_xml(name, xml_str):
    file_data[name] = xml_str.encode('utf-8')

# ── Step 2: Fix Int32 overflow in ALL XML files ─────────────────────────────
def fix_overflow_ids(xml):
    def replace_id(m):
        val = int(m.group(1))
        if val > 2147483647:
            new_val = val - 10  # reduce by 10
            while new_val > 2147483647:
                new_val -= 1000000
            return f'id="{new_val}"'
        return m.group(0)
    return re.sub(r'id="(\d+)"', replace_id, xml)

overflow_fixed = 0
for name in list(file_data.keys()):
    if name.endswith('.xml') or name.endswith('.rels'):
        xml = get_xml(name)
        new_xml = fix_overflow_ids(xml)
        if new_xml != xml:
            set_xml(name, new_xml)
            overflow_fixed += 1
            print(f"  Fixed overflow IDs in {name}")
print(f"Fixed overflow in {overflow_fixed} files")

# ── Step 3: Slide 3 - Green overlay transparency ────────────────────────────
s3 = get_xml('ppt/slides/slide3.xml')
# Handle self-closing tag
s3 = s3.replace(
    '<a:srgbClr val="DBEEE0"/>',
    '<a:srgbClr val="DBEEE0"><a:alpha val="40000"/></a:srgbClr>'
)
# Handle opening tag without alpha child - insert alpha after opening tag
# Only if no alpha already exists inside
def add_alpha_to_dbeee0(xml):
    pattern = r'(<a:srgbClr val="DBEEE0">)((?:(?!<a:alpha).)*?)(</a:srgbClr>)'
    def repl(m):
        return m.group(1) + '<a:alpha val="40000"/>' + m.group(2) + m.group(3)
    return re.sub(pattern, repl, xml, flags=re.DOTALL)

s3 = add_alpha_to_dbeee0(s3)
set_xml('ppt/slides/slide3.xml', s3)
print("Slide 3: Added green overlay transparency")

# ── Step 4: Slides 5-8 - Remove ALL connector shapes ────────────────────────
for sn in [5, 6, 7, 8]:
    name = f'ppt/slides/slide{sn}.xml'
    xml = get_xml(name)
    new_xml = re.sub(r'<p:cxnSp>.*?</p:cxnSp>', '', xml, flags=re.DOTALL)
    removed = (len(xml) - len(new_xml))
    set_xml(name, new_xml)
    print(f"Slide {sn}: Removed connectors (saved {removed} chars)")

# ── Step 5: Slides 9-14, 15 - Remove connectors + resize tags ───────────────
TAG_OLD_SIZE = 256032
TAG_NEW_SIZE = 146304
SIZE_DELTA = (TAG_OLD_SIZE - TAG_NEW_SIZE) // 2  # offset adjustment = 54864

def process_tag_slides(xml):
    """Remove connectors, resize tag shapes, fix tag text."""
    # 1. Remove all connectors
    xml = re.sub(r'<p:cxnSp>.*?</p:cxnSp>', '', xml, flags=re.DOTALL)

    # 2. Process shapes with 256032 dimensions
    # Find all <p:sp>...</p:sp> blocks
    def process_shape(m):
        shape = m.group(0)
        if '256032' not in shape:
            return shape

        # This is a tag shape (green fill or text overlay)
        # Adjust position: add SIZE_DELTA to x and y to keep center
        def adjust_offset(off_m):
            x = int(off_m.group(1))
            y = int(off_m.group(2))
            return f'<a:off x="{x + SIZE_DELTA}" y="{y + SIZE_DELTA}"/>'

        shape = re.sub(
            r'<a:off x="(\d+)" y="(\d+)"/>',
            adjust_offset,
            shape
        )

        # Change size from 256032 to 146304
        shape = shape.replace(
            f'<a:ext cx="{TAG_OLD_SIZE}" cy="{TAG_OLD_SIZE}"/>',
            f'<a:ext cx="{TAG_NEW_SIZE}" cy="{TAG_NEW_SIZE}"/>'
        )

        # Change geometry from rect to ellipse
        shape = shape.replace(
            'prst="rect"',
            'prst="ellipse"'
        )

        # Change font size to 700 for tag text shapes
        shape = re.sub(r'sz="1000"', 'sz="700"', shape)

        return shape

    xml = re.sub(r'<p:sp>.*?</p:sp>', process_shape, xml, flags=re.DOTALL)
    return xml

for sn in [9, 10, 11, 12, 13, 14, 15]:
    name = f'ppt/slides/slide{sn}.xml'
    xml = get_xml(name)
    xml = process_tag_slides(xml)
    set_xml(name, xml)
    print(f"Slide {sn}: Processed connectors + tags")

# ── Step 6: Slides 9-14 - Text replacements ─────────────────────────────────
for sn in [9, 10, 11, 12, 13, 14]:
    name = f'ppt/slides/slide{sn}.xml'
    xml = get_xml(name)
    xml = xml.replace('GNB', 'Header')
    # 캐러셀 -> 슬라이더 (need to handle encoded Korean)
    xml = xml.replace('캐러셀', '슬라이더')
    set_xml(name, xml)
    print(f"Slide {sn}: Text replacements done")

# ── Step 7: Replace images for slides 9-14 ──────────────────────────────────
image_map = {
    'ppt/media/image-9-1.png': os.path.join(SCREENSHOTS, 'footer_crop.png'),
    'ppt/media/image-10-1.png': os.path.join(SCREENSHOTS, 'mypage_home.png'),
    'ppt/media/image-11-1.png': os.path.join(SCREENSHOTS, 'edit_info.png'),
    'ppt/media/image-12-1.png': os.path.join(SCREENSHOTS, 'notification.png'),
    'ppt/media/image-13-1.png': os.path.join(SCREENSHOTS, 'experience.png'),
    'ppt/media/image-14-1.png': os.path.join(SCREENSHOTS, 'unsubscribe.png'),
}

for media_path, screenshot_path in image_map.items():
    with open(screenshot_path, 'rb') as f:
        new_bytes = f.read()
    old_size = len(file_data[media_path])
    file_data[media_path] = new_bytes
    print(f"  Replaced {media_path}: {old_size} -> {len(new_bytes)} bytes")

# ── Step 8: Slides 16, 18 - Add header bar ──────────────────────────────────
HEADER_TEMPLATE = '''<p:sp>
  <p:nvSpPr><p:cNvPr id="900" name="Bar"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="0" y="0"/><a:ext cx="54864" cy="457200"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:solidFill><a:srgbClr val="333333"/></a:solidFill><a:ln/>
  </p:spPr>
  <p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="ko-KR"/></a:p></p:txBody>
</p:sp>
<p:sp>
  <p:nvSpPr><p:cNvPr id="901" name="Title"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="182880" y="45720"/><a:ext cx="8229600" cy="320040"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:noFill/><a:ln/>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>
    <a:lstStyle/>
    <a:p>
      <a:pPr indent="0" marL="0"><a:buNone/></a:pPr>
      <a:r>
        <a:rPr lang="ko-KR" sz="1400" b="1" dirty="0">
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:latin typeface="\ub9d1\uc740 \uace0\ub515" pitchFamily="34" charset="0"/>
          <a:ea typeface="\ub9d1\uc740 \uace0\ub515" pitchFamily="34" charset="-122"/>
        </a:rPr>
        <a:t>TRY-CATCH    \ud654\uba74 \ub0b4 \uc601\uc5ed \uc124\uba85</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>
<p:sp>
  <p:nvSpPr><p:cNvPr id="902" name="Sub"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="182880" y="384048"/><a:ext cx="4572000" cy="201168"/></a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
    <a:noFill/><a:ln/>
  </p:spPr>
  <p:txBody>
    <a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>
    <a:lstStyle/>
    <a:p>
      <a:pPr indent="0" marL="0"><a:buNone/></a:pPr>
      <a:r>
        <a:rPr lang="ko-KR" sz="1100" b="1" dirty="0">
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:latin typeface="\ub9d1\uc740 \uace0\ub515" pitchFamily="34" charset="0"/>
          <a:ea typeface="\ub9d1\uc740 \uace0\ub515" pitchFamily="34" charset="-122"/>
        </a:rPr>
        <a:t>SUBTITLE_PLACEHOLDER</a:t>
      </a:r>
    </a:p>
  </p:txBody>
</p:sp>'''

subtitles = {
    16: '\u300cQ&amp;A \uc791\uc131/\uc218\uc815 \uc138\ubd80 \uc778\ud130\ub799\uc158\u300d',
    18: '\u300c\uacf5\ud1b5 \uc0c1\ud0dc \ubcc0\ud654: \ub85c\uadf8\uc778 / \uc54c\ub9bc / \uac80\uc0c9\u300d',
}

for sn in [16, 18]:
    name = f'ppt/slides/slide{sn}.xml'
    xml = get_xml(name)

    # Move image down
    xml = xml.replace(
        '<a:off x="0" y="0"/><a:ext cx="9144000" cy="5143500"/>',
        '<a:off x="0" y="457200"/><a:ext cx="9144000" cy="4686300"/>'
    )

    # Insert header shapes before </p:spTree>
    header = HEADER_TEMPLATE.replace('SUBTITLE_PLACEHOLDER', subtitles[sn])
    xml = xml.replace('</p:spTree>', header + '</p:spTree>')

    set_xml(name, xml)
    print(f"Slide {sn}: Added header bar with subtitle")

# ── Step 9: Final Int32 overflow verification ────────────────────────────────
remaining_overflow = 0
for name in file_data:
    if name.endswith('.xml') or name.endswith('.rels'):
        xml = get_xml(name)
        ids = re.findall(r'id="(\d+)"', xml)
        for i in ids:
            if int(i) > 2147483647:
                remaining_overflow += 1
                print(f"  WARNING: Overflow still in {name}: id={i}")
print(f"Final overflow check: {remaining_overflow} remaining")

# ── Step 10: Write output ZIP ────────────────────────────────────────────────
with zipfile.ZipFile(DST, 'w') as zout:
    for name in file_data:
        info = file_info[name]
        # Create new ZipInfo to avoid issues
        new_info = zipfile.ZipInfo(name)
        new_info.compress_type = zipfile.ZIP_DEFLATED
        new_info.date_time = info.date_time
        zout.writestr(new_info, file_data[name])

print(f"\nOutput written to: {DST}")
print(f"File size: {os.path.getsize(DST):,} bytes")

# ── Step 11: Sanity check with python-pptx ──────────────────────────────────
try:
    from pptx import Presentation
    prs = Presentation(DST)
    print(f"python-pptx sanity check: OK ({len(prs.slides)} slides)")
except Exception as e:
    print(f"python-pptx sanity check: {e}")
