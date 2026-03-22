"""
TRY-CATCH 스크린샷 v2 - 올바른 로그인 + 필요한 페이지만
"""
import asyncio
from playwright.async_api import async_playwright
import os

BASE = "http://localhost:10000"
OUT = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\screenshots"
os.makedirs(OUT, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2
        )
        page = await context.new_page()

        # ── 로그인 ──
        print("1. Logging in...")
        await page.goto(f"{BASE}/main/log-in")
        await page.wait_for_load_state("networkidle")
        await page.fill('input[name="memberId"]', 'user_demo')
        await page.fill('input[name="memberPassword"]', '1234')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle")
        print(f"   URL after login: {page.url}")

        logged_in = '/log-in' not in page.url
        if not logged_in:
            print("   LOGIN FAILED - trying JS submit")
            await page.goto(f"{BASE}/main/log-in")
            await page.wait_for_load_state("networkidle")
            await page.fill('input[name="memberId"]', 'user_demo')
            await page.fill('input[name="memberPassword"]', '1234')
            await page.evaluate("document.querySelector('form').submit()")
            await page.wait_for_load_state("networkidle")
            print(f"   URL: {page.url}")
            logged_in = '/log-in' not in page.url

        if not logged_in:
            print("   STILL FAILED - check credentials")

        # ── Slide 7: QnA 상세 (댓글 포함) ──
        print("\n2. QnA detail with comments...")
        # 먼저 댓글 있는 글 찾기
        await page.goto(f"{BASE}/qna/list")
        await page.wait_for_load_state("networkidle")
        # 첫번째 글 상세
        links = await page.query_selector_all('a[href*="/qna/detail"]')
        if links:
            await links[0].click()
            await page.wait_for_load_state("networkidle")
            # 댓글 입력 시도
            comment_input = await page.query_selector('textarea[name*="comment"], textarea[name*="reply"], .comment-input, .reply-input, textarea')
            if comment_input:
                await comment_input.fill('실무에서 @Transactional 범위를 서비스 메서드 단위로만 가져가도 충분한지 궁금합니다.')
            await page.screenshot(path=os.path.join(OUT, "new_qna_detail.png"), full_page=True)
            print("   new_qna_detail.png")

        # ── Slide 9: 푸터 ──
        print("\n3. Footer...")
        await page.goto(f"{BASE}/qna/list")
        await page.wait_for_load_state("networkidle")
        footer = await page.query_selector('footer, .footer, .site-footer')
        if footer:
            await footer.screenshot(path=os.path.join(OUT, "new_footer_only.png"))
            print("   new_footer_only.png (footer element)")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1)
        await page.screenshot(path=os.path.join(OUT, "new_footer_full.png"), full_page=True)
        print("   new_footer_full.png")

        # ── Slide 10: 마이페이지 홈 + 프로필 ──
        print("\n4. MyPage home...")
        await page.goto(f"{BASE}/mypage/mypage")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "new_mypage_home.png"), full_page=True)
        print("   new_mypage_home.png")

        # 프로필 수정 버튼/사진 변경 영역
        profile_btn = await page.query_selector('[class*="profile"] button, .profile-edit, .camera-icon, [class*="camera"]')
        if profile_btn:
            await profile_btn.click()
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "new_mypage_profile_edit.png"))
            print("   new_mypage_profile_edit.png")

        # ── Slide 11: 회원정보 수정 + 유효성 ──
        print("\n5. Edit info + validation...")
        await page.goto(f"{BASE}/mypage/change-my-information")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "new_mypage_edit.png"), full_page=True)
        print("   new_mypage_edit.png")

        # 유효성 검사 트리거 - 이름 비우고 제출 시도
        name_input = await page.query_selector('input[name*="name"], input[name*="Name"]')
        if name_input:
            await name_input.fill('')
        submit_btn = await page.query_selector('button[type="submit"], .btn-submit, .btn-save')
        if submit_btn:
            await submit_btn.click()
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "new_mypage_edit_validation.png"), full_page=True)
            print("   new_mypage_edit_validation.png")

        # ── Slide 12: 알림 목록 + 필터 ──
        print("\n6. Notifications + filter...")
        await page.goto(f"{BASE}/mypage/notification")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "new_notification.png"), full_page=True)
        print("   new_notification.png")

        # 필터 드롭다운 열기
        filter_el = await page.query_selector('select, .filter, .dropdown, [class*="filter"]')
        if filter_el:
            tag_name = await filter_el.evaluate("el => el.tagName")
            if tag_name == "SELECT":
                # select 요소의 옵션 보여주기 위해 클릭
                await filter_el.click()
                await asyncio.sleep(0.5)
            else:
                await filter_el.click()
                await asyncio.sleep(0.5)
            await page.screenshot(path=os.path.join(OUT, "new_notification_filter.png"))
            print("   new_notification_filter.png")

        # ── Slide 13: 활동 내역 + 필터 ──
        print("\n7. Experience + filter...")
        await page.goto(f"{BASE}/mypage/experience")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "new_experience.png"), full_page=True)
        print("   new_experience.png")

        filter_el2 = await page.query_selector('select, .filter, [class*="filter"]')
        if filter_el2:
            tag_name2 = await filter_el2.evaluate("el => el.tagName")
            if tag_name2 == "SELECT":
                await filter_el2.click()
                await asyncio.sleep(0.5)
            else:
                await filter_el2.click()
                await asyncio.sleep(0.5)
            await page.screenshot(path=os.path.join(OUT, "new_experience_filter.png"))
            print("   new_experience_filter.png")

        # ── Slide 14: 회원 탈퇴 + 오류 ──
        print("\n8. Unsubscribe + error...")
        await page.goto(f"{BASE}/mypage/unsubscribe")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "new_unsubscribe.png"), full_page=True)
        print("   new_unsubscribe.png")

        # 잘못된 이름으로 탈퇴 시도
        name_input2 = await page.query_selector('input[name*="name"], input[name*="Name"], input[placeholder*="이름"]')
        if name_input2:
            await name_input2.fill('잘못된이름')
        check = await page.query_selector('input[type="checkbox"]')
        if check:
            await check.click()
        unsub_btn = await page.query_selector('button[class*="unsub"], button[class*="delete"], .btn-unsubscribe, button:has-text("탈퇴")')
        if unsub_btn:
            await unsub_btn.click()
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "new_unsubscribe_error.png"), full_page=True)
            print("   new_unsubscribe_error.png")

        # ── Slide 15: 헤더 상태 + 알림 드롭다운 ──
        print("\n9. Header states...")
        await page.goto(f"{BASE}/qna/list")
        await page.wait_for_load_state("networkidle")

        # 알림 아이콘 클릭
        alarm = await page.query_selector('[class*="alarm"], [class*="bell"], [class*="noti"] a, .header [class*="alarm"]')
        if alarm:
            await alarm.click()
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "new_header_alarm.png"))
            print("   new_header_alarm.png")

            # 알림 드롭다운 영역만 확대 캡쳐
            alarm_dropdown = await page.query_selector('[class*="alarm-dropdown"], [class*="notification-dropdown"], [class*="alarm-list"]')
            if alarm_dropdown:
                await alarm_dropdown.screenshot(path=os.path.join(OUT, "new_header_alarm_zoom.png"))
                print("   new_header_alarm_zoom.png")

        # 프로필 드롭다운
        profile_menu = await page.query_selector('[class*="profile"] a, .user-menu, [class*="member-name"]')
        if profile_menu:
            await profile_menu.click()
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "new_header_profile_dropdown.png"))
            print("   new_header_profile_dropdown.png")

        # GNB 메뉴 hover
        await page.goto(f"{BASE}/qna/list")
        await page.wait_for_load_state("networkidle")
        gnb_items = await page.query_selector_all('header nav a, .gnb a, nav.main-nav a')
        if gnb_items:
            await gnb_items[0].hover()
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "new_header_gnb_hover.png"))
            print("   new_header_gnb_hover.png")

        # 검색 자동완성
        search = await page.query_selector('input[type="search"], input[name="keyword"], .search-input, input[placeholder*="search"], input[placeholder*="try"]')
        if search:
            await search.click()
            await search.fill("Spring")
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "new_header_search.png"))
            print("   new_header_search.png")

        # ── 포인트 ──
        print("\n10. Point page...")
        await page.goto(f"{BASE}/point/point")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "new_point.png"), full_page=True)
        print("   new_point.png")

        await browser.close()
        print("\n=== ALL DONE ===")

asyncio.run(main())
