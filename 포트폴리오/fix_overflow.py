"""
Fix Int32 overflow in PPTX + slide 3 transparency + all slide fixes.
Direct zip edit approach (no python-pptx save).
"""
import zipfile, re, os, shutil

SRC = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\김윤찬_TRY-CATCH_화면_포트폴리오_FINAL.pptx"
OUT_RAW = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\김윤찬_TRY-CATCH_화면_포트폴리오_v9_raw.pptx"
OUT = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\김윤찬_TRY-CATCH_화면_포트폴리오_v9.pptx"

entries = {}
with zipfile.ZipFile(SRC, 'r') as z:
    for info in z.infolist():
        entries[info.filename] = (info, z.read(info.filename))

def fix_xml(name):
    info, data = entries[name]
    text = data.decode('utf-8')
    return info, text

def save_xml(name, info, text):
    entries[name] = (info, text.encode('utf-8'))

# ── 1. Fix Int32 overflow in presentation.xml ──
info, xml = fix_xml('ppt/presentation.xml')
# 2147483648 -> 2147483640 (valid Int32 range)
xml = xml.replace('id="2147483648"', 'id="2147483640"')
save_xml('ppt/presentation.xml', info, xml)
print("1. Fixed presentation.xml overflow")

# ── 2. Fix Int32 overflow in slideMaster1.xml ──
info2, xml2 = fix_xml('ppt/slideMasters/slideMaster1.xml')
xml2 = xml2.replace('id="2147483649"', 'id="2147483641"')
# Check for more overflows
xml2 = re.sub(r'id="(214748364[89]|21474836[5-9]\d)"', lambda m: f'id="{int(m.group(1)) - 10}"', xml2)
save_xml('ppt/slideMasters/slideMaster1.xml', info2, xml2)
print("2. Fixed slideMaster1.xml overflow")

# ── 3. Slide 3: 초록 오버레이 투명도 ──
info3, xml3 = fix_xml('ppt/slides/slide3.xml')
# DBEEE0 self-closing -> add alpha
xml3 = xml3.replace(
    '<a:srgbClr val="DBEEE0"/>',
    '<a:srgbClr val="DBEEE0"><a:alpha val="40000"/></a:srgbClr>'
)
# DBEEE0 with children but no alpha
xml3 = re.sub(
    r'(<a:srgbClr val="DBEEE0">)(?!<a:alpha)',
    r'\1<a:alpha val="40000"/>',
    xml3
)
save_xml('ppt/slides/slide3.xml', info3, xml3)
print("3. Slide 3 green overlay transparency (40%)")

# ── 4. Check ALL XMLs for remaining overflows ──
for name in list(entries.keys()):
    if not name.endswith('.xml'):
        continue
    info, data = entries[name]
    text = data.decode('utf-8', errors='ignore')
    fixed = False
    for m in re.finditer(r'id="(\d{10,})"', text):
        val = int(m.group(1))
        if val > 2147483647:
            new_val = val - 10
            text = text.replace(f'id="{val}"', f'id="{new_val}"')
            print(f"4. Fixed overflow in {name}: {val} -> {new_val}")
            fixed = True
    if fixed:
        entries[name] = (info, text.encode('utf-8'))

# ── 5. Save ──
if os.path.exists(OUT_RAW):
    os.remove(OUT_RAW)

with zipfile.ZipFile(SRC, 'r') as zin:
    with zipfile.ZipFile(OUT_RAW, 'w') as zout:
        for info_orig in zin.infolist():
            if info_orig.filename in entries:
                _, data = entries[info_orig.filename]
                zout.writestr(info_orig, data)
            else:
                zout.writestr(info_orig, zin.read(info_orig.filename))

print(f"\n5. Raw saved: {os.path.getsize(OUT_RAW):,} bytes")

# ── 6. LibreOffice conversion ──
tmp_dir = r"C:\Users\pigch\AppData\Local\Temp\pptx_v9"
os.makedirs(tmp_dir, exist_ok=True)
tmp_out = os.path.join(tmp_dir, "out")
os.makedirs(tmp_out, exist_ok=True)
tmp_in = os.path.join(tmp_dir, "input.pptx")
shutil.copy2(OUT_RAW, tmp_in)

import subprocess
result = subprocess.run([
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    "--headless", "--convert-to", "pptx",
    "--outdir", tmp_out, tmp_in
], capture_output=True, text=True, timeout=120)

converted = os.path.join(tmp_out, "input.pptx")
if os.path.exists(converted):
    if os.path.exists(OUT):
        os.remove(OUT)
    shutil.copy2(converted, OUT)
    print(f"6. Final: {OUT} ({os.path.getsize(OUT):,} bytes)")

    # Verify no more overflows
    with zipfile.ZipFile(OUT, 'r') as z:
        overflow_count = 0
        for info in z.infolist():
            if not info.filename.endswith('.xml'):
                continue
            data = z.read(info.filename).decode('utf-8', errors='ignore')
            for m2 in re.finditer(r'="(\d{10,})"', data):
                v = int(m2.group(1))
                if v > 2147483647:
                    overflow_count += 1
                    print(f"  STILL OVERFLOW: {info.filename} val={v}")
        if overflow_count == 0:
            print("  No Int32 overflows remaining!")
else:
    print(f"LibreOffice failed: {result.stderr}")
    shutil.copy2(OUT_RAW, OUT)
