import asyncio
from playwright.async_api import async_playwright
import os

BASE = "http://localhost:10000"
OUT = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\screenshots"

async def shot(page, name, full=True, timeout=15000):
    path = os.path.join(OUT, name)
    await page.screenshot(path=path, full_page=full, timeout=timeout)
    sz = os.path.getsize(path)
    print(f"  {name} ({sz//1024}KB)")

async def goto(page, url, timeout=15000):
    await page.goto(url, timeout=timeout)
    await page.wait_for_load_state("networkidle", timeout=timeout)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page = await ctx.new_page()
        page.set_default_timeout(15000)

        # 로그인
        await goto(page, f"{BASE}/main/log-in")
        await page.fill('input[name="memberId"]', 'user_demo')
        await page.fill('input[name="memberPassword"]', '1234')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle", timeout=15000)
        print(f"Login OK: {page.url}")

        # ── Slide 7: QnA 상세 (댓글 포함) ──
        print("\n[Slide 7] QnA Detail + Comments")
        try:
            await goto(page, f"{BASE}/qna/detail?id=7001")
            await shot(page, "s7_qna_detail_comments.png")
        except Exception as e:
            print(f"  ERROR: {e}")

        # ── Slide 9: 푸터 ──
        print("\n[Slide 9] Footer")
        try:
            await goto(page, f"{BASE}/qna/list")
            footer = await page.query_selector('footer')
            if footer:
                box = await footer.bounding_box()
                if box:
                    await page.evaluate(f"window.scrollTo(0, {box['y'] - 100})")
                    await asyncio.sleep(0.5)
            await shot(page, "s9_footer.png")
            if footer:
                await footer.screenshot(path=os.path.join(OUT, "s9_footer_crop.png"))
                print("  s9_footer_crop.png")
        except Exception as e:
            print(f"  ERROR: {e}")

        # ── Slide 10: 마이페이지 홈 ──
        print("\n[Slide 10] MyPage Home")
        try:
            await goto(page, f"{BASE}/mypage/mypage")
            await shot(page, "s10_mypage_home.png")
            # 프로필 영역 확대
            profile_section = await page.query_selector('[class*="profile"], .mypage-profile, .user-profile')
            if profile_section:
                await profile_section.screenshot(path=os.path.join(OUT, "s10_profile_section.png"))
                print("  s10_profile_section.png")
        except Exception as e:
            print(f"  ERROR: {e}")

        # ── Slide 11: 회원정보 수정 ──
        print("\n[Slide 11] Edit Info")
        try:
            await goto(page, f"{BASE}/mypage/change-my-information")
            await shot(page, "s11_edit_info.png")
            # 유효성 - 이름 비우고 제출
            name_input = await page.query_selector('input[name="memberName"]')
            if name_input:
                await name_input.fill('')
                btn = await page.query_selector('button:has-text("수정")')
                if btn:
                    await btn.click()
                    await asyncio.sleep(1)
                    await shot(page, "s11_edit_validation.png")
        except Exception as e:
            print(f"  ERROR: {e}")

        # ── Slide 12: 알림 ──
        print("\n[Slide 12] Notifications")
        try:
            await goto(page, f"{BASE}/mypage/notification")
            await shot(page, "s12_notification.png")
            # 필터 드롭다운
            sel = await page.query_selector('select')
            if sel:
                await sel.click()
                await asyncio.sleep(0.5)
                await shot(page, "s12_notification_filter.png", full=False)
        except Exception as e:
            print(f"  ERROR: {e}")

        # ── Slide 13: 활동 내역 ──
        print("\n[Slide 13] Experience")
        try:
            await goto(page, f"{BASE}/mypage/experience")
            await shot(page, "s13_experience.png")
            sels = await page.query_selector_all('select')
            if sels:
                await sels[0].click()
                await asyncio.sleep(0.5)
                await shot(page, "s13_experience_filter.png", full=False)
        except Exception as e:
            print(f"  ERROR: {e}")

        # ── Slide 14: 회원 탈퇴 ──
        print("\n[Slide 14] Unsubscribe")
        try:
            await goto(page, f"{BASE}/mypage/unsubscribe")
            await shot(page, "s14_unsubscribe.png")
            # 오류 상태
            name2 = await page.query_selector('input[placeholder*="이름"], input[name*="name"]')
            if name2:
                await name2.fill('틀린이름')
            chk = await page.query_selector('input[type="checkbox"]')
            if chk:
                await chk.check()
            btn2 = await page.query_selector('button:has-text("탈퇴")')
            if btn2:
                await btn2.click()
                await asyncio.sleep(1)
                await shot(page, "s14_unsubscribe_error.png")
        except Exception as e:
            print(f"  ERROR: {e}")

        # ── Slide 15: 헤더 상태들 ──
        print("\n[Slide 15] Header States")
        try:
            await goto(page, f"{BASE}/qna/list")
            # GNB hover
            gnb = await page.query_selector_all('header nav > ul > li')
            if gnb and len(gnb) > 0:
                await gnb[0].hover()
                await asyncio.sleep(1)
                await shot(page, "s15_gnb_hover.png", full=False)

            # 알림 드롭다운
            await goto(page, f"{BASE}/qna/list")
            alarm = await page.query_selector('[class*="alarm"] a, [class*="bell"] a, [class*="noti"] a')
            if not alarm:
                alarm = await page.query_selector('[class*="alarm"], [class*="bell"]')
            if alarm:
                await alarm.click()
                await asyncio.sleep(1)
                await shot(page, "s15_alarm_dropdown.png", full=False)

            # 프로필 드롭다운
            await goto(page, f"{BASE}/qna/list")
            prof = await page.query_selector('[class*="user-name"], [class*="member-name"], header [class*="profile"]')
            if prof:
                await prof.click()
                await asyncio.sleep(1)
                await shot(page, "s15_profile_dropdown.png", full=False)

            # 검색 자동완성
            await goto(page, f"{BASE}/qna/list")
            search = await page.query_selector('input[placeholder*="try"], input[type="search"]')
            if search:
                await search.click()
                await search.fill("Spring")
                await asyncio.sleep(1)
                await shot(page, "s15_search_autocomplete.png", full=False)

            # 비로그인 헤더
            await ctx.clear_cookies()
            await goto(page, f"{BASE}/qna/list")
            await shot(page, "s15_loggedout.png", full=False)

        except Exception as e:
            print(f"  ERROR: {e}")

        # ── 포인트 ──
        print("\n[Slide 16] Point")
        try:
            # 다시 로그인
            await goto(page, f"{BASE}/main/log-in")
            await page.fill('input[name="memberId"]', 'user_demo')
            await page.fill('input[name="memberPassword"]', '1234')
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle", timeout=15000)

            await goto(page, f"{BASE}/point/point")
            await shot(page, "s16_point.png")
        except Exception as e:
            print(f"  ERROR: {e}")

        await browser.close()
        print("\n=== DONE ===")

asyncio.run(main())
