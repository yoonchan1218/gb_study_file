# -*- coding: utf-8 -*-
"""
Build v7 PPTX by direct ZIP manipulation.
Reads v6.pptx as zip, modifies XML and images, writes new zip, then converts via LibreOffice.
"""
import zipfile
import shutil
import os
import subprocess
from PIL import Image

BASE = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오"
SRC_PPTX = os.path.join(BASE, "김윤찬_TRY-CATCH_화면_포트폴리오_v6.pptx")
OUT_PPTX = os.path.join(BASE, "김윤찬_TRY-CATCH_화면_포트폴리오_v7_done.pptx")
SCREENSHOTS = os.path.join(BASE, "screenshots")
SOFFICE = r"C:\Program Files\LibreOffice\program\soffice.exe"

# ── XML helper snippets ──────────────────────────────────────────────────────
NS = 'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'

FONT_SPEC = '<a:latin typeface="맑은 고딕" pitchFamily="34" charset="0"/><a:ea typeface="맑은 고딕" pitchFamily="34" charset="-122"/><a:cs typeface="맑은 고딕" pitchFamily="34" charset="-120"/>'

def text_run(text, sz, bold=False, color="333333"):
    b_attr = ' b="1"' if bold else ''
    return (f'<a:r><a:rPr lang="en-US" sz="{sz}"{b_attr} dirty="0">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'{FONT_SPEC}</a:rPr><a:t>{esc(text)}</a:t></a:r>')

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def accent_bar():
    return ('<p:sp><p:nvSpPr><p:cNvPr id="2" name="Shape 0"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            '<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="54864" cy="457200"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            '<a:solidFill><a:srgbClr val="333333"/></a:solidFill><a:ln/></p:spPr>'
            '<p:txBody><a:bodyPr/><a:p/></p:txBody></p:sp>')

def title_shape(id_num, text, x=182880, y=45720, cx=4572000, cy=320040, sz=1400, bold=True, color="333333"):
    b_attr = ' b="1"' if bold else ''
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{id_num}" name="Text {id_num-1}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>'
            f'<a:lstStyle/><a:p><a:pPr indent="0" marL="0"><a:buNone/></a:pPr>'
            f'<a:r><a:rPr lang="en-US" sz="{sz}"{b_attr} dirty="0">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>{FONT_SPEC}</a:rPr>'
            f'<a:t>{esc(text)}</a:t></a:r>'
            f'<a:endParaRPr lang="en-US" sz="{sz}" dirty="0"/></a:p></p:txBody></p:sp>')

def bg_box(id_num, x, y, cx, cy):
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{id_num}" name="Shape {id_num-1}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="FAFAFA"/></a:solidFill>'
            f'<a:ln w="12700"><a:solidFill><a:srgbClr val="DDDDDD"/></a:solidFill>'
            f'<a:prstDash val="solid"/></a:ln></p:spPr>'
            f'<p:txBody><a:bodyPr/><a:p/></p:txBody></p:sp>')

def image_shape(id_num, rid, x, y, cx, cy, descr="preencoded.png"):
    return (f'<p:pic><p:nvPicPr><p:cNvPr id="{id_num}" name="Image {id_num}" descr="{descr}">    </p:cNvPr>'
            f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>'
            f'<p:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')

def tag_badge(id_base, letter, x, y, size=256032, font_sz=1000):
    """Green square badge with white letter"""
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{id_base}" name="Shape {id_base}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{size}" cy="{size}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'<a:solidFill><a:srgbClr val="3A9D6E"/></a:solidFill><a:ln/></p:spPr>'
        f'<p:txBody><a:bodyPr/><a:p/></p:txBody></p:sp>'
        f'<p:sp><p:nvSpPr><p:cNvPr id="{id_base+1}" name="Text {id_base+1}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{size}" cy="{size}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln/></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="square" rtlCol="0" anchor="ctr"/><a:lstStyle/>'
        f'<a:p><a:pPr algn="ctr" indent="0" marL="0"><a:buNone/></a:pPr>'
        f'<a:r><a:rPr lang="en-US" sz="{font_sz}" b="1" dirty="0">'
        f'<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>{FONT_SPEC}</a:rPr>'
        f'<a:t>{letter}</a:t></a:r>'
        f'<a:endParaRPr lang="en-US" sz="{font_sz}" dirty="0"/></a:p></p:txBody></p:sp>'
    )

def desc_area_title(id_num, text, x, y=384048, cx=5373803, cy=228600):
    return title_shape(id_num, text, x=x, y=y, cx=cx, cy=cy, sz=1000, bold=True, color="006E3F")

def separator_line(id_num, x, y=594360, cx=5373803, cy=9144):
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{id_num}" name="Sep {id_num}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:solidFill><a:srgbClr val="DDDDDD"/></a:solidFill><a:ln/></p:spPr>'
            f'<p:txBody><a:bodyPr/><a:p/></p:txBody></p:sp>')

def desc_group(id_base, letter, title_text, detail_text, desc_left, y_start):
    """One description entry: letter label + title + detail"""
    label_x = desc_left
    text_x = desc_left + 228560
    text_cx = 9144000 - text_x - 137160  # extend to near right edge
    return (
        # Letter label "A."
        f'<p:sp><p:nvSpPr><p:cNvPr id="{id_base}" name="Text {id_base}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{label_x}" y="{y_start}"/><a:ext cx="228600" cy="182880"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln/></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>'
        f'<a:lstStyle/><a:p><a:pPr indent="0" marL="0"><a:buNone/></a:pPr>'
        f'{text_run(letter + ".", 1000, bold=True, color="3A9D6E")}'
        f'<a:endParaRPr lang="en-US" sz="1000" dirty="0"/></a:p></p:txBody></p:sp>'
        # Title
        f'<p:sp><p:nvSpPr><p:cNvPr id="{id_base+1}" name="Text {id_base+1}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{text_x}" y="{y_start}"/><a:ext cx="{text_cx}" cy="137160"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln/></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>'
        f'<a:lstStyle/><a:p><a:pPr indent="0" marL="0"><a:buNone/></a:pPr>'
        f'{text_run(title_text, 900, bold=True, color="333333")}'
        f'<a:endParaRPr lang="en-US" sz="900" dirty="0"/></a:p></p:txBody></p:sp>'
        # Detail
        f'<p:sp><p:nvSpPr><p:cNvPr id="{id_base+2}" name="Text {id_base+2}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{text_x}" y="{y_start + 137160}"/><a:ext cx="{text_cx}" cy="338328"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln/></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" rtlCol="0" anchor="ctr"/>'
        f'<a:lstStyle/><a:p><a:pPr indent="0" marL="0"><a:buNone/></a:pPr>'
        f'{text_run(detail_text, 700, bold=False, color="666666")}'
        f'<a:endParaRPr lang="en-US" sz="700" dirty="0"/></a:p></p:txBody></p:sp>'
    )

def page_number(id_num, num, x=8686800, y=4846320):
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{id_num}" name="PageNum"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="274320" cy="182880"/></a:xfrm>'
            f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" rtlCol="0" anchor="ctr"/><a:lstStyle/>'
            f'<a:p><a:pPr algn="r" indent="0" marL="0"><a:buNone/></a:pPr>'
            f'<a:r><a:rPr lang="en-US" sz="800" dirty="0">'
            f'<a:solidFill><a:srgbClr val="888888"/></a:solidFill></a:rPr>'
            f'<a:t>{num}</a:t></a:r>'
            f'<a:endParaRPr lang="en-US" sz="800" dirty="0"/></a:p></p:txBody></p:sp>')

def get_image_size_emu(path):
    """Get image dimensions in EMU (1 inch = 914400 EMU, assuming 96 DPI)"""
    img = Image.open(path)
    w, h = img.size
    # Convert pixels to EMU (at 96 DPI)
    emu_w = int(w * 914400 / 96)
    emu_h = int(h * 914400 / 96)
    return emu_w, emu_h

def fit_image_to_area(img_path, max_cx, max_cy):
    """Scale image to fit within max_cx x max_cy keeping aspect ratio. Returns (cx, cy) in EMU."""
    emu_w, emu_h = get_image_size_emu(img_path)
    ratio_w = max_cx / emu_w
    ratio_h = max_cy / emu_h
    ratio = min(ratio_w, ratio_h)
    return int(emu_w * ratio), int(emu_h * ratio)

def build_standard_slide(slide_name, subtitle, desc_area_subtitle, descriptions, img_rid="rId1",
                         img_path=None, tag_positions=None, page_num="5",
                         desc_left=3678757, img_area_cx=3130117, img_area_cy=4114800,
                         y_spacing=502920):
    """Build a standard layout slide XML.
    descriptions: list of (letter, title, detail)
    tag_positions: list of (letter, x, y) for green badges on image
    """
    # Calculate image fit
    box_x = 118872
    box_y = 640080
    img_x = 137160
    img_y = 658368

    if img_path and os.path.exists(img_path):
        img_cx, img_cy = fit_image_to_area(img_path, img_area_cx, img_area_cy)
    else:
        img_cx, img_cy = img_area_cx, img_area_cy

    box_cx = img_cx + 36576
    box_cy = img_cy + 36576

    parts = []
    parts.append(f'<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>')
    parts.append(f'<p:sld {NS}><p:cSld name="{slide_name}"><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></p:bgPr></p:bg><p:spTree>')
    parts.append('<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>')
    parts.append('<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>')

    # Accent bar
    parts.append(accent_bar())
    # Title
    parts.append(title_shape(3, "TRY-CATCH    화면 내 영역 설명"))
    # Subtitle
    parts.append(title_shape(4, subtitle, y=384048, cy=201168, sz=1100))
    # BG box
    parts.append(bg_box(5, box_x, box_y, box_cx, box_cy))
    # Image
    parts.append(image_shape(6, img_rid, img_x, img_y, img_cx, img_cy))

    id_counter = 7

    # Tag badges on image
    if tag_positions:
        for letter, tx, ty in tag_positions:
            parts.append(tag_badge(id_counter, letter, tx, ty))
            id_counter += 2

    # Description area title
    parts.append(desc_area_title(id_counter, desc_area_subtitle, desc_left))
    id_counter += 1

    # Separator
    parts.append(separator_line(id_counter, desc_left))
    id_counter += 1

    # Description groups
    y_start = 685800
    for i, (letter, dtitle, detail) in enumerate(descriptions):
        parts.append(desc_group(id_counter, letter, dtitle, detail, desc_left, y_start + i * y_spacing))
        id_counter += 3

    # Page number
    parts.append(page_number(id_counter, page_num))

    parts.append('</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')

    return ''.join(parts)

def build_rels(image_targets, slide_layout="../slideLayouts/slideLayout1.xml", notes_slide=None):
    """Build a .rels file for a slide."""
    parts = ['<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>']
    parts.append('<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">')
    rid = 1
    for target in image_targets:
        parts.append(f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{target}"/>')
        rid += 1
    parts.append(f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="{slide_layout}"/>')
    rid += 1
    if notes_slide:
        parts.append(f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="{notes_slide}"/>')
    parts.append('</Relationships>')
    return ''.join(parts)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN BUILD
# ══════════════════════════════════════════════════════════════════════════════

def main():
    import tempfile

    # Read original zip
    print("Reading original PPTX...")
    zin = zipfile.ZipFile(SRC_PPTX, 'r')
    file_data = {}
    for name in zin.namelist():
        file_data[name] = zin.read(name)
    zin.close()

    # ── Helper to replace media ──
    def replace_media(media_name, screenshot_name):
        img_path = os.path.join(SCREENSHOTS, screenshot_name)
        with open(img_path, 'rb') as f:
            file_data[f'ppt/media/{media_name}'] = f.read()
        return img_path

    def add_new_media(media_name, screenshot_name):
        img_path = os.path.join(SCREENSHOTS, screenshot_name)
        with open(img_path, 'rb') as f:
            file_data[f'ppt/media/{media_name}'] = f.read()
        return img_path

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 7: Replace image only
    # ══════════════════════════════════════════════════════════════════════════
    print("Processing slide 7...")
    img7 = replace_media('image-7-1.png', 's7_qna_detail_comments.png')
    # Recalculate image size in existing XML
    xml7 = file_data['ppt/slides/slide7.xml'].decode('utf-8')
    # Get new image dimensions fitted to old area (4572000 x 3624263)
    new_cx7, new_cy7 = fit_image_to_area(img7, 4572000, 3624263)
    # Replace image extent in XML
    xml7 = xml7.replace(
        '<a:ext cx="4572000" cy="3624263"/>',
        f'<a:ext cx="{new_cx7}" cy="{new_cy7}"/>'
    )
    # Also update bg box
    old_box_cx7 = 4608576
    old_box_cy7 = 3660838
    new_box_cx7 = new_cx7 + 36576
    new_box_cy7 = new_cy7 + 36576
    xml7 = xml7.replace(
        f'<a:ext cx="{old_box_cx7}" cy="{old_box_cy7}"/>',
        f'<a:ext cx="{new_box_cx7}" cy="{new_box_cy7}"/>'
    )
    # GNB -> Header replacement
    xml7 = xml7.replace('GNB', 'Header')
    xml7 = xml7.replace('캐러셀', '슬라이더')
    file_data['ppt/slides/slide7.xml'] = xml7.encode('utf-8')

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 9: 공통 푸터 (Footer) - replace image & fix descriptions
    # ══════════════════════════════════════════════════════════════════════════
    print("Processing slide 9...")
    img9 = replace_media('image-9-1.png', 's9_footer.png')
    img_cx9, img_cy9 = fit_image_to_area(img9, 4572000, 4114800)

    # Tag positions for footer - along the image area
    footer_tags = [
        ("A", 4754880, int(img_cy9 * 0.05) + 658368),
        ("B", 4754880, int(img_cy9 * 0.30) + 658368),
        ("C", 4754880, int(img_cy9 * 0.55) + 658368),
        ("D", 4754880, int(img_cy9 * 0.80) + 658368),
    ]

    desc_left_wide = 5257800

    slide9_xml = build_standard_slide(
        slide_name="Slide 9",
        subtitle="「공통 푸터 (Footer)」",
        desc_area_subtitle="공통 푸터 (Footer) 화면 구성 설명",
        descriptions=[
            ("A", "제휴 광고", "체험 관련 외부 광고, 배너/채팅 안내"),
            ("B", "공지사항", "사이트 주요 공지사항 한줄 표시"),
            ("C", "사이트 정책 링크", "회사소개, 이용약관, 개인정보처리방침, 고객센터"),
            ("D", "연락처/저작권", "전화, 운영시간, FAX, 이메일, ©표시"),
        ],
        img_rid="rId1",
        img_path=img9,
        tag_positions=footer_tags,
        page_num="9",
        desc_left=desc_left_wide,
        img_area_cx=4572000,
        img_area_cy=4114800,
    )
    file_data['ppt/slides/slide9.xml'] = slide9_xml.encode('utf-8')
    file_data['ppt/slides/_rels/slide9.xml.rels'] = build_rels(
        ["../media/image-9-1.png"],
        notes_slide="../notesSlides/notesSlide9.xml"
    ).encode('utf-8')

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 10: 마이페이지 프로필/홈
    # ══════════════════════════════════════════════════════════════════════════
    print("Processing slide 10...")
    img10 = replace_media('image-10-1.png', 's10_mypage_home.png')

    img_cx10, img_cy10 = fit_image_to_area(img10, 3130117, 4114800)

    tag_y_start = 658368
    tag_spacing = int(img_cy10 / 7)
    tags10 = [
        ("A", 3312997, tag_y_start + int(img_cy10 * 0.05)),
        ("B", 3312997, tag_y_start + int(img_cy10 * 0.18)),
        ("C", 3312997, tag_y_start + int(img_cy10 * 0.35)),
        ("D", 3312997, tag_y_start + int(img_cy10 * 0.52)),
        ("E", 3312997, tag_y_start + int(img_cy10 * 0.70)),
        ("F", 3312997, tag_y_start + int(img_cy10 * 0.85)),
    ]

    slide10_xml = build_standard_slide(
        slide_name="Slide 10",
        subtitle="「마이페이지 프로필/홈」",
        desc_area_subtitle="마이페이지 프로필/홈 화면 구성 설명",
        descriptions=[
            ("A", "사이드 네비게이션", "개인회원 홈, 기술블로그, 체험지원관리, QnA, 회원정보 관리"),
            ("B", "프로필 카드", "프로필 사진 업로드, 닉네임, 레벨, 포인트"),
            ("C", "최근 체험 슬라이더", "추천 체험 프로그램 Swiper 슬라이드 (좌우 넘김)"),
            ("D", "인기글/최근글", "인기 Q&A 목록, 태그/카테고리 표시"),
            ("E", "최근 체험공고/TOP100", "최근 프로그램, TOP100 추천 카드"),
            ("F", "포인트 매칭 (선택)", "최근 별 내역/스크랩 게시물 전환"),
        ],
        img_rid="rId1",
        img_path=img10,
        tag_positions=tags10,
        page_num="10",
        desc_left=3678757,
        img_area_cx=3130117,
        img_area_cy=4114800,
    )
    file_data['ppt/slides/slide10.xml'] = slide10_xml.encode('utf-8')
    file_data['ppt/slides/_rels/slide10.xml.rels'] = build_rels(
        ["../media/image-10-1.png"],
        notes_slide="../notesSlides/notesSlide10.xml"
    ).encode('utf-8')

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 11: 개인정보 수정
    # ══════════════════════════════════════════════════════════════════════════
    print("Processing slide 11...")
    img11 = replace_media('image-11-1.png', 's11_edit_info.png')
    img_cx11, img_cy11 = fit_image_to_area(img11, 3130117, 4114800)

    tags11 = [
        ("A", 3312997, 658368 + int(img_cy11 * 0.02)),
        ("B", 3312997, 658368 + int(img_cy11 * 0.12)),
        ("C", 3312997, 658368 + int(img_cy11 * 0.30)),
        ("D", 3312997, 658368 + int(img_cy11 * 0.55)),
        ("E", 3312997, 658368 + int(img_cy11 * 0.85)),
    ]

    slide11_xml = build_standard_slide(
        slide_name="Slide 11",
        subtitle="「개인정보 수정」",
        desc_area_subtitle="개인정보 수정 화면 구성 설명",
        descriptions=[
            ("A", "수정화면 타이틀", "'회원정보 수정' 타이틀"),
            ("B", "사이드 (읽기전용)", "회원 아이디 표시 (수정 불가)"),
            ("C", "기본 정보 수정", "이름, 생년월일 드롭다운, 성별 선택, 학력"),
            ("D", "연락처 수정", "휴대폰, 일반전화, 이메일(@도메인)"),
            ("E", "수정하기/취소 버튼", "폼 전송, 유효성 검증"),
        ],
        img_rid="rId1",
        img_path=img11,
        tag_positions=tags11,
        page_num="11",
        desc_left=3678757,
        img_area_cx=3130117,
        img_area_cy=4114800,
    )
    file_data['ppt/slides/slide11.xml'] = slide11_xml.encode('utf-8')
    file_data['ppt/slides/_rels/slide11.xml.rels'] = build_rels(
        ["../media/image-11-1.png"],
        notes_slide="../notesSlides/notesSlide11.xml"
    ).encode('utf-8')

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 12: 알림 목록
    # ══════════════════════════════════════════════════════════════════════════
    print("Processing slide 12...")
    img12 = replace_media('image-12-1.png', 's12_notification.png')
    img_cx12, img_cy12 = fit_image_to_area(img12, 3130117, 4114800)

    tags12 = [
        ("A", 3312997, 658368 + int(img_cy12 * 0.05)),
        ("B", 3312997, 658368 + int(img_cy12 * 0.15)),
        ("C", 3312997, 658368 + int(img_cy12 * 0.28)),
        ("D", 3312997, 658368 + int(img_cy12 * 0.50)),
    ]

    slide12_xml = build_standard_slide(
        slide_name="Slide 12",
        subtitle="「알림 목록」",
        desc_area_subtitle="알림 목록 화면 구성 설명",
        descriptions=[
            ("A", "사이드 네비게이션", "개인회원 홈, 기술블로그, 체험지원관리, QnA, 회원정보 관리"),
            ("B", "수신 알림 타이틀", "'수신 알림', 최근 30일 알림 안내"),
            ("C", "카테고리 필터", "전체/체험지원/체험안내/기술블로그 필터링"),
            ("D", "알림 목록/빈 상태", "날짜별 그룹핑 또는 '알림 없음' 안내"),
        ],
        img_rid="rId1",
        img_path=img12,
        tag_positions=tags12,
        page_num="12",
        desc_left=3678757,
        img_area_cx=3130117,
        img_area_cy=4114800,
    )
    file_data['ppt/slides/slide12.xml'] = slide12_xml.encode('utf-8')
    file_data['ppt/slides/_rels/slide12.xml.rels'] = build_rels(
        ["../media/image-12-1.png"],
        notes_slide="../notesSlides/notesSlide12.xml"
    ).encode('utf-8')

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 13: 활동 내역 (체험지원 현황)
    # ══════════════════════════════════════════════════════════════════════════
    print("Processing slide 13...")
    img13 = replace_media('image-13-1.png', 's13_experience.png')
    img_cx13, img_cy13 = fit_image_to_area(img13, 3130117, 4114800)

    tags13 = [
        ("A", 3312997, 658368 + int(img_cy13 * 0.05)),
        ("B", 3312997, 658368 + int(img_cy13 * 0.18)),
        ("C", 3312997, 658368 + int(img_cy13 * 0.35)),
        ("D", 3312997, 658368 + int(img_cy13 * 0.70)),
        ("E", 3312997, 658368 + int(img_cy13 * 0.85)),
    ]

    slide13_xml = build_standard_slide(
        slide_name="Slide 13",
        subtitle="「활동 내역 (체험지원 현황)」",
        desc_area_subtitle="활동 내역 (체험지원 현황) 화면 구성 설명",
        descriptions=[
            ("A", "상태 요약 카드", "참여완료/참여중/심사완료/심사중 카운트"),
            ("B", "날짜/상태 검색", "조회기간, 날짜, 진행/합격/불합격여부 필터"),
            ("C", "지원 현황 목록", "기업명, 프로그램, 지원분야별, 상태표시 버튼"),
            ("D", "페이지네이션", "지원 목록 페이지 이동"),
            ("E", "유의사항/푸터", "유의사항 5가지, 연락 정보, 회사 정보"),
        ],
        img_rid="rId1",
        img_path=img13,
        tag_positions=tags13,
        page_num="13",
        desc_left=3678757,
        img_area_cx=3130117,
        img_area_cy=4114800,
    )
    file_data['ppt/slides/slide13.xml'] = slide13_xml.encode('utf-8')
    file_data['ppt/slides/_rels/slide13.xml.rels'] = build_rels(
        ["../media/image-13-1.png"],
        notes_slide="../notesSlides/notesSlide13.xml"
    ).encode('utf-8')

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 14: 회원 탈퇴
    # ══════════════════════════════════════════════════════════════════════════
    print("Processing slide 14...")
    img14 = replace_media('image-14-1.png', 's14_unsubscribe.png')
    img_cx14, img_cy14 = fit_image_to_area(img14, 3130117, 4114800)

    tags14 = [
        ("A", 3312997, 658368 + int(img_cy14 * 0.02)),
        ("B", 3312997, 658368 + int(img_cy14 * 0.20)),
        ("C", 3312997, 658368 + int(img_cy14 * 0.52)),
        ("D", 3312997, 658368 + int(img_cy14 * 0.78)),
    ]

    slide14_xml = build_standard_slide(
        slide_name="Slide 14",
        subtitle="「회원 탈퇴」",
        desc_area_subtitle="회원 탈퇴 화면 구성 설명",
        descriptions=[
            ("A", "탈퇴 화면 진입", "로고, '회원정보 관리', 수정/탈퇴 탭"),
            ("B", "유의사항 목록", "계정 불가능, ID 재사용 불가, 동시 탈퇴, 데이터 삭제"),
            ("C", "본인 확인 폼", "아이디(읽기전용), 탈퇴요청자 이름 입력"),
            ("D", "동의 및 탈퇴 버튼", "체크박스 선택 후 탈퇴하기 활성화"),
        ],
        img_rid="rId1",
        img_path=img14,
        tag_positions=tags14,
        page_num="14",
        desc_left=3678757,
        img_area_cx=3130117,
        img_area_cy=4114800,
    )
    file_data['ppt/slides/slide14.xml'] = slide14_xml.encode('utf-8')
    file_data['ppt/slides/_rels/slide14.xml.rels'] = build_rels(
        ["../media/image-14-1.png"],
        notes_slide="../notesSlides/notesSlide14.xml"
    ).encode('utf-8')

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 15: 공통 Header 상태 + 드롭다운 (multi-image)
    # ══════════════════════════════════════════════════════════════════════════
    print("Processing slide 15...")
    img15_1 = replace_media('image-15-1.png', 's15_loggedout.png')
    img15_2 = replace_media('image-15-2.png', 's15_profile_dropdown.png')
    img15_3 = replace_media('image-15-3.png', 's15_search_autocomplete.png')
    # Add alarm dropdown as 4th image
    img15_4 = replace_media('image-15-4.png', 's15_alarm_dropdown.png')

    # Multi-image layout: 2x2 grid + description area
    # Top row: y=640080, Bottom row: y~2600000
    # Each image about 2700000 wide
    img_max_w = 2700000
    img_max_h = 1700000

    cx15_1, cy15_1 = fit_image_to_area(img15_1, img_max_w, img_max_h)
    cx15_2, cy15_2 = fit_image_to_area(img15_2, img_max_w, img_max_h)
    cx15_3, cy15_3 = fit_image_to_area(img15_3, img_max_w, img_max_h)
    cx15_4, cy15_4 = fit_image_to_area(img15_4, 1200000, 1200000)

    row1_y = 658368
    row2_y = row1_y + max(cy15_1, cy15_2) + 54864
    col1_x = 137160
    col2_x = col1_x + cx15_1 + 54864

    desc_left_15 = 5600000

    parts15 = []
    parts15.append(f'<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>')
    parts15.append(f'<p:sld {NS}><p:cSld name="Slide 15"><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></p:bgPr></p:bg><p:spTree>')
    parts15.append('<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>')
    parts15.append('<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>')
    parts15.append(accent_bar())
    parts15.append(title_shape(3, "TRY-CATCH    화면 내 영역 설명"))
    parts15.append(title_shape(4, "「공통 Header 상태 + 드롭다운」", y=384048, cy=201168, sz=1100))

    # 4 BG boxes + images
    for i, (rid, cx, cy, ix, iy) in enumerate([
        ("rId1", cx15_1, cy15_1, col1_x, row1_y),
        ("rId2", cx15_2, cy15_2, col2_x, row1_y),
        ("rId3", cx15_3, cy15_3, col1_x, row2_y),
        ("rId4", cx15_4, cy15_4, col2_x, row2_y),
    ]):
        box_id = 10 + i * 3
        parts15.append(bg_box(box_id, ix - 18288, iy - 18288, cx + 36576, cy + 36576))
        parts15.append(image_shape(box_id + 1, rid, ix, iy, cx, cy, f"screenshot_{i}.png"))

    # Labels on images
    labels15 = ["비로그인 상태", "프로필 드롭다운", "검색 자동완성", "알림 드롭다운"]
    label_positions = [(col1_x, row1_y - 27432), (col2_x, row1_y - 27432), (col1_x, row2_y - 27432), (col2_x, row2_y - 27432)]
    id_c = 30
    for lbl, (lx, ly) in zip(labels15, label_positions):
        parts15.append(title_shape(id_c, lbl, x=lx, y=ly, cx=2700000, cy=27432, sz=600, bold=True, color="888888"))
        id_c += 1

    # Description area
    parts15.append(desc_area_title(id_c, "공통 Header 상태 + 드롭다운 구성 설명", desc_left_15))
    id_c += 1
    parts15.append(separator_line(id_c, desc_left_15))
    id_c += 1

    descs15 = [
        ("A", "Header 드롭다운", "서비스소개/체험정보/기술블로그/커뮤니티, hover 시 하위 메뉴 표시"),
        ("B", "비회원서비스 드롭다운", "비로그인 시 비회원서비스 버튼 클릭 시 체험 신청하기/개인회원 홈 안내"),
        ("C", "프로필 드롭다운", "로그인 후 회원 이름 클릭 시 개인회원홈/기술블로그/체험지원/개인정보/로그아웃"),
        ("D", "검색 자동완성", "키워드 자동완성 드롭다운, 자동완성 끄기/닫기 옵션 지원"),
        ("E", "알림 드롭다운", "새 알림 표시, 클릭 시 알림 목록"),
    ]
    y_s = 685800
    for i, (letter, dtitle, detail) in enumerate(descs15):
        parts15.append(desc_group(id_c, letter, dtitle, detail, desc_left_15, y_s + i * 502920))
        id_c += 3

    parts15.append(page_number(id_c, "15"))
    parts15.append('</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')

    file_data['ppt/slides/slide15.xml'] = ''.join(parts15).encode('utf-8')
    file_data['ppt/slides/_rels/slide15.xml.rels'] = build_rels(
        ["../media/image-15-1.png", "../media/image-15-2.png", "../media/image-15-3.png", "../media/image-15-4.png"],
        notes_slide="../notesSlides/notesSlide15.xml"
    ).encode('utf-8')

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 16: Q&A 작성/수정 세부 인터랙션 - add header bar
    # ══════════════════════════════════════════════════════════════════════════
    print("Processing slide 16...")
    # Keep existing image but add header bar, resize image to fit below
    parts16 = []
    parts16.append(f'<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>')
    parts16.append(f'<p:sld {NS}><p:cSld name="Slide 16"><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></p:bgPr></p:bg><p:spTree>')
    parts16.append('<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>')
    parts16.append('<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>')
    parts16.append(accent_bar())
    parts16.append(title_shape(3, "TRY-CATCH    화면 내 영역 설명"))
    parts16.append(title_shape(4, "「Q&A 작성/수정 세부 인터랙션」", y=384048, cy=201168, sz=1100))
    # Image below header - full width, below header bar
    parts16.append(image_shape(6, "rId2", 0, 457200, 9144000, 4686300, "slide_16.png"))
    parts16.append(page_number(99, "16"))
    parts16.append('</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')
    file_data['ppt/slides/slide16.xml'] = ''.join(parts16).encode('utf-8')

    # ══════════════════════════════════════════════════════════════════════════
    # SLIDE 17: 공통 상태 변화 - add header bar (currently slide17=image only)
    # ══════════════════════════════════════════════════════════════════════════
    print("Processing slide 17...")
    parts17 = []
    parts17.append(f'<?xml version=\'1.0\' encoding=\'UTF-8\' standalone=\'yes\'?>')
    parts17.append(f'<p:sld {NS}><p:cSld name="Slide 17"><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></p:bgPr></p:bg><p:spTree>')
    parts17.append('<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>')
    parts17.append('<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>')
    parts17.append(accent_bar())
    parts17.append(title_shape(3, "TRY-CATCH    화면 내 영역 설명"))
    parts17.append(title_shape(4, "「공통 상태 변화: 로그인 / 알림 / 검색」", y=384048, cy=201168, sz=1100))
    parts17.append(image_shape(6, "rId2", 0, 457200, 9144000, 4686300, "slide_17.png"))
    parts17.append(page_number(99, "17"))
    parts17.append('</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')
    file_data['ppt/slides/slide17.xml'] = ''.join(parts17).encode('utf-8')

    # ══════════════════════════════════════════════════════════════════════════
    # Global replacements across ALL slides: GNB -> Header, 캐러셀 -> 슬라이더
    # ══════════════════════════════════════════════════════════════════════════
    print("Applying global text replacements...")
    for name in list(file_data.keys()):
        if name.startswith('ppt/slides/slide') and name.endswith('.xml'):
            xml = file_data[name].decode('utf-8')
            changed = False
            if 'GNB' in xml:
                xml = xml.replace('GNB', 'Header')
                changed = True
            if '캐러셀' in xml:
                xml = xml.replace('캐러셀', '슬라이더')
                changed = True
            # Also handle encoded Korean in the XML
            if changed:
                file_data[name] = xml.encode('utf-8')

    # ══════════════════════════════════════════════════════════════════════════
    # Write output ZIP
    # ══════════════════════════════════════════════════════════════════════════
    print("Writing output PPTX...")
    tmp_path = os.path.join(BASE, "_tmp_v7.pptx")

    with zipfile.ZipFile(tmp_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for name in sorted(file_data.keys()):
            zout.writestr(name, file_data[name])

    # ══════════════════════════════════════════════════════════════════════════
    # Convert through LibreOffice for 한쇼 compatibility
    # ══════════════════════════════════════════════════════════════════════════
    print("Converting through LibreOffice...")
    outdir = os.path.join(BASE, "_tmp_lo_out")
    os.makedirs(outdir, exist_ok=True)

    cmd = [
        SOFFICE,
        "--headless",
        "--convert-to", "pptx",
        "--outdir", outdir,
        tmp_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    print(f"LibreOffice stdout: {result.stdout}")
    print(f"LibreOffice stderr: {result.stderr}")

    converted = os.path.join(outdir, "_tmp_v7.pptx")
    if os.path.exists(converted):
        shutil.copy2(converted, OUT_PPTX)
        print(f"SUCCESS: Output saved to {OUT_PPTX}")
        # Cleanup
        os.remove(tmp_path)
        shutil.rmtree(outdir, ignore_errors=True)
    else:
        # If LibreOffice conversion failed, use the direct zip output
        print("LibreOffice conversion did not produce output, using direct ZIP...")
        shutil.copy2(tmp_path, OUT_PPTX)
        os.remove(tmp_path)
        shutil.rmtree(outdir, ignore_errors=True)
        print(f"Output saved to {OUT_PPTX} (without LO conversion)")


if __name__ == "__main__":
    main()
