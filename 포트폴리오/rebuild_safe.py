"""
v6 원본에서 slide1~slide8 완전 보존.
slide9~slide18만 수정. slide7 이미지 교체 + GNB->Header도 9~18에만 적용.
"""
import zipfile
import os
import re
from PIL import Image
import io

SRC = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\김윤찬_TRY-CATCH_화면_포트폴리오_v6.pptx"
SHOTS = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\screenshots"
OUT_RAW = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\김윤찬_TRY-CATCH_화면_포트폴리오_v8_raw.pptx"
OUT_FINAL = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\김윤찬_TRY-CATCH_화면_포트폴리오_v8.pptx"

# Read all entries from original
entries = {}
with zipfile.ZipFile(SRC, 'r') as zin:
    for info in zin.infolist():
        entries[info.filename] = zin.read(info.filename)

def get_xml(name):
    return entries[name].decode('utf-8')

def set_xml(name, content):
    entries[name] = content.encode('utf-8')

def load_image(filename):
    path = os.path.join(SHOTS, filename)
    with open(path, 'rb') as f:
        return f.read()

# ============================================================
# PROTECTED: slides 1-8 are NOT touched at all
# Only modify slide9.xml through slide18.xml
# ============================================================

SAFE_SLIDES = set(f'ppt/slides/slide{i}.xml' for i in range(9, 19))
SAFE_RELS = set(f'ppt/slides/_rels/slide{i}.xml.rels' for i in range(9, 19))

# ── Slide 3: 초록 오버레이 투명도만 (slide3은 사용자가 수정한거라 투명도만) ──
# 사용자가 8페이지까지 건드리지 말라고 했으므로 slide3도 안 건드림

# ── Slide 9 (공통 푸터): connector 제거 + 태그 수정 + GNB->Header ──
for n in range(9, 19):
    fname = f'ppt/slides/slide{n}.xml'
    if fname not in entries:
        continue
    xml = get_xml(fname)

    # connector 제거
    xml = re.sub(r'<p:cxnSp>.*?</p:cxnSp>', '', xml, flags=re.DOTALL)

    # GNB -> Header (9~18 슬라이드만)
    xml = xml.replace('>GNB<', '>Header<')
    xml = xml.replace('>GNB ', '>Header ')
    xml = xml.replace(' GNB<', ' Header<')
    xml = xml.replace(' GNB ', ' Header ')
    xml = xml.replace('(GNB)', '(Header)')
    xml = re.sub(r'>GNB</a:t>', '>Header</a:t>', xml)
    xml = re.sub(r'>헤더 \(GNB\)</a:t>', '>Header</a:t>', xml)
    xml = re.sub(r'>공통 \(GNB\)</a:t>', '>Header</a:t>', xml)

    # 캐러셀 -> 슬라이더
    xml = xml.replace('캐러셀', '슬라이더')

    # 태그 원형: 256032 사각형 -> 146304 타원
    TAG = 146304

    def fix_tag(m):
        block = m.group(0)
        if '256032' not in block:
            return block

        is_green_bg = ('3A9D6E' in block and '<a:t>' not in block)
        is_tag_letter = bool(re.search(r'<a:t>[A-G]</a:t>', block))

        if not is_green_bg and not is_tag_letter:
            return block

        off_m = re.search(r'<a:off x="(\d+)" y="(\d+)"/>', block)
        if not off_m:
            return block

        old_x = int(off_m.group(1))
        old_y = int(off_m.group(2))

        # 이미지 안쪽으로 이동 (x를 좌측으로 약간)
        new_x = old_x - 100000
        cy = old_y + 256032 // 2
        ny = cy - TAG // 2

        block = re.sub(
            r'<a:off x="\d+" y="\d+"/>',
            f'<a:off x="{new_x}" y="{ny}"/>',
            block, count=1
        )
        block = re.sub(
            r'<a:ext cx="256032" cy="256032"/>',
            f'<a:ext cx="{TAG}" cy="{TAG}"/>',
            block, count=1
        )
        block = block.replace('prst="rect"', 'prst="ellipse"')

        if is_tag_letter:
            block = re.sub(r'sz="\d+"', 'sz="700"', block)
            block = re.sub(
                r'(<a:rPr[^>]*>)\s*<a:solidFill>\s*<a:srgbClr val="[^"]*"/>\s*</a:solidFill>',
                r'\1<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>',
                block
            )
            if 'b="1"' not in block:
                block = re.sub(r'(<a:rPr )', r'\1b="1" ', block)

        return block

    xml = re.sub(r'<p:sp>.*?</p:sp>', fix_tag, xml, flags=re.DOTALL)

    set_xml(fname, xml)
    print(f"  slide{n}.xml updated")

# ── Slide 16, 18: 이미지 슬라이드에 헤더 추가 ──
# slide16.xml과 slide18.xml에 헤더바 + 타이틀 도형 추가
for n, subtitle in [(16, '「Q&A 작성/수정 세부 인터랙션」'), (18, '「공통 상태 변화: 로그인 / 알림 / 검색」')]:
    fname = f'ppt/slides/slide{n}.xml'
    xml = get_xml(fname)

    # 이미지 위치를 헤더 아래로 이동
    # <a:off x="0" y="0"/> -> y를 457200으로
    # <a:ext cx="9144000" cy="5143500"/> -> cy를 4686300으로
    xml = re.sub(
        r'(<a:off x="0" y=")0(")',
        r'\g<1>457200\2',
        xml, count=1
    )
    xml = re.sub(
        r'(<a:ext cx="9144000" cy=")5143500(")',
        r'\g<1>4686300\2',
        xml, count=1
    )

    # spTree 닫기 전에 헤더 도형 삽입
    header_shapes = f'''
      <p:sp>
        <p:nvSpPr><p:cNvPr id="900" name="AccentBar"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="0" y="0"/><a:ext cx="54864" cy="457200"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="333333"/></a:solidFill>
          <a:ln/>
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
        <p:nvSpPr><p:cNvPr id="902" name="Subtitle"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
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
              <a:t>{subtitle}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>'''

    xml = xml.replace('</p:spTree>', header_shapes + '\n    </p:spTree>')
    set_xml(fname, xml)
    print(f"  slide{n}.xml: header added")

# ── 이미지 교체 ──
# slide9의 이미지를 푸터 스크린샷으로 교체
# slide9 rels에서 이미지 파일명 확인
rels9 = get_xml('ppt/slides/_rels/slide9.xml.rels')
img9_match = re.search(r'Target="\.\./(media/[^"]+)"', rels9)
if img9_match:
    img9_path = 'ppt/' + img9_match.group(1)
    new_img = load_image('s9_footer.png')
    entries[img9_path] = new_img
    print(f"  Replaced {img9_path} with s9_footer.png")

# slide10 이미지 교체
rels10 = get_xml('ppt/slides/_rels/slide10.xml.rels')
img10_matches = re.findall(r'Target="\.\./(media/[^"]+)"', rels10)
if img10_matches:
    img10_path = 'ppt/' + img10_matches[0]
    entries[img10_path] = load_image('s10_mypage_home.png')
    print(f"  Replaced {img10_path} with s10_mypage_home.png")

# slide11 이미지 교체
rels11 = get_xml('ppt/slides/_rels/slide11.xml.rels')
img11_matches = re.findall(r'Target="\.\./(media/[^"]+)"', rels11)
if img11_matches:
    entries['ppt/' + img11_matches[0]] = load_image('s11_edit_info.png')
    print(f"  Replaced slide11 image with s11_edit_info.png")

# slide12 이미지 교체
rels12 = get_xml('ppt/slides/_rels/slide12.xml.rels')
img12_matches = re.findall(r'Target="\.\./(media/[^"]+)"', rels12)
if img12_matches:
    entries['ppt/' + img12_matches[0]] = load_image('s12_notification.png')
    print(f"  Replaced slide12 image with s12_notification.png")

# slide13 이미지 교체
rels13 = get_xml('ppt/slides/_rels/slide13.xml.rels')
img13_matches = re.findall(r'Target="\.\./(media/[^"]+)"', rels13)
if img13_matches:
    entries['ppt/' + img13_matches[0]] = load_image('s13_experience.png')
    print(f"  Replaced slide13 image with s13_experience.png")

# slide14 이미지 교체
rels14 = get_xml('ppt/slides/_rels/slide14.xml.rels')
img14_matches = re.findall(r'Target="\.\./(media/[^"]+)"', rels14)
if img14_matches:
    entries['ppt/' + img14_matches[0]] = load_image('s14_unsubscribe.png')
    print(f"  Replaced slide14 image with s14_unsubscribe.png")

# ── 저장 (원본 zip 구조 그대로) ──
if os.path.exists(OUT_RAW):
    os.remove(OUT_RAW)

with zipfile.ZipFile(SRC, 'r') as zin:
    with zipfile.ZipFile(OUT_RAW, 'w') as zout:
        for info in zin.infolist():
            if info.filename in entries:
                zout.writestr(info, entries[info.filename])
            else:
                zout.writestr(info, zin.read(info.filename))

print(f"\nRaw saved: {OUT_RAW} ({os.path.getsize(OUT_RAW):,} bytes)")

# ── LibreOffice 변환 (한쇼 호환) ──
import shutil, subprocess

tmp_dir = r"C:\Users\pigch\AppData\Local\Temp\pptx_convert"
os.makedirs(tmp_dir, exist_ok=True)
tmp_in = os.path.join(tmp_dir, "input.pptx")
tmp_out_dir = os.path.join(tmp_dir, "out")
os.makedirs(tmp_out_dir, exist_ok=True)

shutil.copy2(OUT_RAW, tmp_in)

result = subprocess.run([
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    "--headless", "--convert-to", "pptx",
    "--outdir", tmp_out_dir,
    tmp_in
], capture_output=True, text=True, timeout=120)

converted = os.path.join(tmp_out_dir, "input.pptx")
if os.path.exists(converted):
    if os.path.exists(OUT_FINAL):
        os.remove(OUT_FINAL)
    shutil.copy2(converted, OUT_FINAL)
    print(f"Final (한쇼 호환): {OUT_FINAL} ({os.path.getsize(OUT_FINAL):,} bytes)")
else:
    print(f"LibreOffice conversion failed: {result.stderr}")
    # fallback: use raw
    shutil.copy2(OUT_RAW, OUT_FINAL)
    print(f"Fallback (raw): {OUT_FINAL}")

# 슬라이드 1-8 무결성 검증
print("\n=== 슬라이드 1-8 무결성 검증 ===")
with zipfile.ZipFile(SRC, 'r') as z_orig:
    with zipfile.ZipFile(OUT_RAW, 'r') as z_new:
        for i in range(1, 9):
            fname = f'ppt/slides/slide{i}.xml'
            orig = z_orig.read(fname)
            new = z_new.read(fname)
            status = "OK (동일)" if orig == new else "CHANGED!"
            print(f"  slide{i}.xml: {status}")
