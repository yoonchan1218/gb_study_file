"""
python-pptx 사용 안 함 - 원본 zip에서 XML만 직접 수정 후 다시 zip
한쇼 호환 보장
"""
import zipfile
import os
import re
import shutil

SRC = "김윤찬_TRY-CATCH_화면_포트폴리오_v6.pptx"
OUT = "김윤찬_TRY-CATCH_화면_포트폴리오_v7_clean.pptx"

# 원본에서 모든 파일 읽기
entries = {}
with zipfile.ZipFile(SRC, 'r') as zin:
    for info in zin.infolist():
        entries[info.filename] = (info, zin.read(info.filename))

def get_xml(name):
    return entries[name][1].decode('utf-8')

def set_xml(name, content):
    info = entries[name][0]
    entries[name] = (info, content.encode('utf-8'))

# ── 1. slide3.xml: 초록 오버레이 투명도 ──
s3 = get_xml('ppt/slides/slide3.xml')
s3 = s3.replace(
    '<a:srgbClr val="DBEEE0"/>',
    '<a:srgbClr val="DBEEE0"><a:alpha val="45000"/></a:srgbClr>'
)
s3 = re.sub(
    r'(<a:srgbClr val="DBEEE0">)(?!<a:alpha)',
    r'\1<a:alpha val="45000"/>',
    s3
)
set_xml('ppt/slides/slide3.xml', s3)
print("1. Slide 3 투명도 완료")

# ── 2. Slides 5-14: connector 제거 + 태그 수정 ──
TAG = 146304
INSET = 80000

for n in range(5, 16):
    fname = f'ppt/slides/slide{n}.xml'
    xml = get_xml(fname)

    # connector 제거
    xml = re.sub(r'<p:cxnSp>.*?</p:cxnSp>', '', xml, flags=re.DOTALL)

    # 메인 이미지 우측 경계 찾기 (가장 큰 이미지)
    # <a:ext cx="3130117" 같은 패턴에서 가장 큰 cx 찾기
    img_rights = []
    for m in re.finditer(r'<p:pic>.*?<a:off x="(\d+)".*?<a:ext cx="(\d+)"', xml, re.DOTALL):
        x = int(m.group(1))
        cx = int(m.group(2))
        if cx > 2000000:
            img_rights.append(x + cx)

    if not img_rights:
        set_xml(fname, xml)
        continue

    img_right = max(img_rights)
    new_x = img_right - TAG - INSET

    # 태그 배경(3A9D6E fill, 256032 size) + 태그 텍스트(A-G, 256032 size)
    def fix_tag_shape(m):
        block = m.group(0)
        if '256032' not in block:
            return block

        is_tag_bg = ('3A9D6E' in block and '<a:t>' not in block and '256032' in block)
        is_tag_text = bool(re.search(r'<a:t>[A-G]</a:t>', block)) and '256032' in block

        if not is_tag_bg and not is_tag_text:
            return block

        # 현재 위치에서 y 중심 계산
        off_m = re.search(r'<a:off x="\d+" y="(\d+)"/>', block)
        if not off_m:
            return block
        old_y = int(off_m.group(1))
        center_y = old_y + 256032 // 2
        ny = center_y - TAG // 2

        # 위치/크기 변경
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
        # rect → ellipse
        block = block.replace('prst="rect"', 'prst="ellipse"')

        if is_tag_text:
            # 폰트 크기 변경
            block = re.sub(r'sz="\d+"', 'sz="700"', block)
            # 텍스트 색상 → 흰색 (333333이나 다른 색을 FFFFFF로)
            # rPr 안의 srgbClr만 변경
            block = re.sub(
                r'(<a:rPr[^>]*>)\s*<a:solidFill>\s*<a:srgbClr val="[^"]*"/>\s*</a:solidFill>',
                r'\1<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>',
                block
            )
            # bold 추가 (이미 있으면 무시)
            if 'b="1"' not in block:
                block = re.sub(r'(<a:rPr )', r'\1b="1" ', block)
            # 중앙 정렬
            if 'anchor="ctr"' not in block:
                block = re.sub(r'<a:bodyPr([^/]*)/>', r'<a:bodyPr\1 anchor="ctr" lIns="0" tIns="0" rIns="0" bIns="0"/>', block)
                block = re.sub(r'<a:bodyPr([^>]*)>', r'<a:bodyPr\1 anchor="ctr" lIns="0" tIns="0" rIns="0" bIns="0">', block)
            if 'algn="ctr"' not in block:
                block = re.sub(r'<a:pPr([^>]*?)(/?)>', r'<a:pPr algn="ctr"\1\2>', block)

        return block

    xml = re.sub(r'<p:sp>.*?</p:sp>', fix_tag_shape, xml, flags=re.DOTALL)
    set_xml(fname, xml)
    print(f"  Slide {n} done")

# ── 저장: 원본 zip 구조 그대로 유지 ──
if os.path.exists(OUT):
    os.remove(OUT)

with zipfile.ZipFile(SRC, 'r') as zin:
    with zipfile.ZipFile(OUT, 'w') as zout:
        for info in zin.infolist():
            if info.filename in entries:
                new_info, data = entries[info.filename]
                # 원본 info 객체를 그대로 사용하되 데이터만 교체
                zout.writestr(info, data)
            else:
                zout.writestr(info, zin.read(info.filename))

print(f"\nSaved: {OUT} ({os.path.getsize(OUT):,} bytes)")
print("원본 zip 구조 유지 - 한쇼 호환")
