import asyncio
from playwright.async_api import async_playwright
import os

BASE = "http://localhost:10000"
OUT = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\screenshots"

async def shot(page, path, full=True):
    await page.screenshot(path=os.path.join(OUT, path), full_page=full)
    print(f"  {path}")

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page = await ctx.new_page()

        # 로그인
        await page.goto(f"{BASE}/main/log-in")
        await page.wait_for_load_state("networkidle")
        await page.fill('input[name="memberId"]', 'user_demo')
        await page.fill('input[name="memberPassword"]', '1234')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle")
        print(f"Login: {page.url}")

        async def safe(name, coro):
            try:
                await coro
            except Exception as e:
                print(f"  ERROR [{name}]: {e}")

        # QnA 상세 (댓글 포함)
        print("\n-- QnA Detail --")
        await page.goto(f"{BASE}/qna/detail?id=1")
        await page.wait_for_load_state("networkidle")
        await shot(page, "new_qna_detail.png")

        # 푸터
        print("\n-- Footer --")
        await page.goto(f"{BASE}/qna/list")
        await page.wait_for_load_state("networkidle")
        await shot(page, "new_footer_full.png")
        footer = await page.query_selector('footer')
        if footer:
            await footer.screenshot(path=os.path.join(OUT, "new_footer_crop.png"))
            print("  new_footer_crop.png")

        # 마이페이지 홈
        print("\n-- MyPage Home --")
        await page.goto(f"{BASE}/mypage/mypage")
        await page.wait_for_load_state("networkidle")
        await shot(page, "new_mypage_home.png")

        # 프로필 사진 변경 영역 확대
        cam = await page.query_selector('[class*="camera"], [class*="profile-img"], .profile-photo, .profile-image')
        if cam:
            await cam.screenshot(path=os.path.join(OUT, "new_profile_photo_area.png"))
            print("  new_profile_photo_area.png")

        # 회원정보 수정
        print("\n-- Edit Info --")
        await page.goto(f"{BASE}/mypage/change-my-information")
        await page.wait_for_load_state("networkidle")
        await shot(page, "new_mypage_edit.png")

        # 유효성 검사 - 이름 비우고 저장
        name_input = await page.query_selector('input[name*="memberName"], input[name*="name"]')
        if name_input:
            await name_input.fill('')
            btn = await page.query_selector('button:has-text("수정"), button:has-text("저장"), button[type="submit"]')
            if btn:
                await btn.click()
                await asyncio.sleep(1)
                await shot(page, "new_edit_validation.png")

        # 알림
        print("\n-- Notifications --")
        await page.goto(f"{BASE}/mypage/notification")
        await page.wait_for_load_state("networkidle")
        await shot(page, "new_notification.png")
        # 필터 드롭다운
        sel = await page.query_selector('select')
        if sel:
            await sel.select_option(index=0)
            await sel.evaluate("el => { el.size = el.options.length; el.style.position='absolute'; el.style.zIndex='9999'; }")
            await asyncio.sleep(0.5)
            await shot(page, "new_notification_filter_open.png", full=False)
            await sel.evaluate("el => { el.size = 1; }")

        # 활동 내역
        print("\n-- Experience --")
        await page.goto(f"{BASE}/mypage/experience")
        await page.wait_for_load_state("networkidle")
        await shot(page, "new_experience.png")
        # 필터
        sels = await page.query_selector_all('select')
        if sels:
            for s in sels[:1]:
                await s.evaluate("el => { el.size = el.options.length; el.style.position='absolute'; el.style.zIndex='9999'; }")
            await asyncio.sleep(0.5)
            await shot(page, "new_experience_filter_open.png", full=False)

        # 회원 탈퇴
        print("\n-- Unsubscribe --")
        await page.goto(f"{BASE}/mypage/unsubscribe")
        await page.wait_for_load_state("networkidle")
        await shot(page, "new_unsubscribe.png")
        # 오류 상태
        name2 = await page.query_selector('input[name*="name"], input[placeholder*="이름"]')
        if name2:
            await name2.fill('잘못된이름테스트')
        chk = await page.query_selector('input[type="checkbox"]')
        if chk:
            await chk.check()
        btn2 = await page.query_selector('button:has-text("탈퇴")')
        if btn2:
            await btn2.click()
            await asyncio.sleep(1)
            await shot(page, "new_unsubscribe_error.png")

        # 포인트
        print("\n-- Point --")
        await page.goto(f"{BASE}/point/point")
        await page.wait_for_load_state("networkidle")
        await shot(page, "new_point.png")

        # 헤더 상태들
        print("\n-- Header States --")
        await page.goto(f"{BASE}/qna/list")
        await page.wait_for_load_state("networkidle")

        # GNB 메뉴 hover
        gnb = await page.query_selector_all('header nav > ul > li, .gnb > ul > li, nav > ul > li')
        if gnb:
            await gnb[0].hover()
            await asyncio.sleep(1)
            await shot(page, "new_gnb_hover.png", full=False)

        # 알림 아이콘
        alarm_icon = await page.query_selector('header [class*="alarm"], header [class*="bell"], header [class*="noti"]')
        if alarm_icon:
            await alarm_icon.click()
            await asyncio.sleep(1)
            await shot(page, "new_alarm_dropdown.png", full=False)

        # 프로필 메뉴
        await page.goto(f"{BASE}/qna/list")
        await page.wait_for_load_state("networkidle")
        profile = await page.query_selector('header [class*="profile"], header [class*="member"], header [class*="user"]')
        if profile:
            await profile.click()
            await asyncio.sleep(1)
            await shot(page, "new_profile_menu.png", full=False)

        # 검색
        await page.goto(f"{BASE}/qna/list")
        await page.wait_for_load_state("networkidle")
        search = await page.query_selector('input[type="search"], input[name="keyword"], input[placeholder*="try"]')
        if search:
            await search.click()
            await search.fill("Spring")
            await asyncio.sleep(1)
            await shot(page, "new_search_autocomplete.png", full=False)

        # 비로그인 상태 헤더
        await ctx.clear_cookies()
        await page.goto(f"{BASE}/qna/list")
        await page.wait_for_load_state("networkidle")
        await shot(page, "new_header_loggedout.png", full=False)

        # 비로그인 GNB hover
        gnb2 = await page.query_selector_all('header nav > ul > li, .gnb > ul > li, nav > ul > li')
        if gnb2:
            await gnb2[0].hover()
            await asyncio.sleep(1)
            await shot(page, "new_gnb_hover_loggedout.png", full=False)

        await browser.close()
        print("\n=== ALL DONE ===")

asyncio.run(main())
