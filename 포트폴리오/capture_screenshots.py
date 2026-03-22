"""
TRY-CATCH 웹앱 스크린샷 촬영
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

        # 1. 로그인
        print("Logging in...")
        await page.goto(f"{BASE}/main/log-in")
        await page.wait_for_load_state("networkidle")
        # 로그인 폼 찾기
        try:
            await page.fill('input[name="userId"]', 'user_demo', timeout=3000)
            await page.fill('input[name="userPassword"]', 'password123', timeout=3000)
            await page.click('button[type="submit"]', timeout=3000)
            await page.wait_for_load_state("networkidle")
            print(f"  Current URL: {page.url}")
        except:
            print("  Login form not found, trying alternative...")
            try:
                inputs = await page.query_selector_all('input[type="text"], input[type="email"]')
                passwords = await page.query_selector_all('input[type="password"]')
                if inputs and passwords:
                    await inputs[0].fill('user_demo')
                    await passwords[0].fill('password123')
                    buttons = await page.query_selector_all('button, input[type="submit"]')
                    for btn in buttons:
                        text = await btn.inner_text()
                        if '로그인' in text or 'login' in text.lower():
                            await btn.click()
                            break
                    await page.wait_for_load_state("networkidle")
                    print(f"  Current URL: {page.url}")
            except Exception as e:
                print(f"  Login failed: {e}")

        # 로그인 페이지 스크린샷 (로그인 전 상태용)
        await page.goto(f"{BASE}/main/log-in")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "login.png"), full_page=True)
        print("  login.png")

        # 다시 로그인 시도 (DB에 있는 계정 확인 필요)
        # 일단 비로그인 상태로 진행

        # ── QnA 페이지들 ──
        # Slide 7용: QnA 상세 (댓글 있는 페이지)
        print("\nCapturing QnA pages...")
        await page.goto(f"{BASE}/qna/list")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "qna_list.png"), full_page=True)
        print("  qna_list.png")

        # QnA 상세 - 첫번째 글 클릭
        links = await page.query_selector_all('a[href*="/qna/detail"]')
        if links:
            href = await links[0].get_attribute('href')
            await page.goto(f"{BASE}{href}" if not href.startswith('http') else href)
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=os.path.join(OUT, "qna_detail.png"), full_page=True)
            print("  qna_detail.png")

        # ── 마이페이지 ──
        print("\nCapturing MyPage pages...")

        # 푸터 (아무 페이지 하단)
        await page.goto(f"{BASE}/qna/list")
        await page.wait_for_load_state("networkidle")
        # 스크롤 끝까지
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1)
        await page.screenshot(path=os.path.join(OUT, "footer.png"), full_page=True)
        print("  footer.png (full page with footer)")

        # 마이페이지
        await page.goto(f"{BASE}/mypage/mypage")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "mypage_home.png"), full_page=True)
        print("  mypage_home.png")

        # 회원정보 수정
        await page.goto(f"{BASE}/mypage/change-my-information")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "mypage_edit_info.png"), full_page=True)
        print("  mypage_edit_info.png")

        # 알림
        await page.goto(f"{BASE}/mypage/notification")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "mypage_notification.png"), full_page=True)
        print("  mypage_notification.png")

        # 활동 내역
        await page.goto(f"{BASE}/mypage/experience")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "mypage_experience.png"), full_page=True)
        print("  mypage_experience.png")

        # 회원 탈퇴
        await page.goto(f"{BASE}/mypage/unsubscribe")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "mypage_unsubscribe.png"), full_page=True)
        print("  mypage_unsubscribe.png")

        # 포인트
        await page.goto(f"{BASE}/point/point")
        await page.wait_for_load_state("networkidle")
        await page.screenshot(path=os.path.join(OUT, "point.png"), full_page=True)
        print("  point.png")

        # ── 헤더/GNB 상태들 ──
        print("\nCapturing header states...")
        await page.goto(f"{BASE}/qna/list")
        await page.wait_for_load_state("networkidle")

        # GNB 드롭다운 (hover 메뉴)
        nav_items = await page.query_selector_all('nav a, .gnb a, .nav a, header a')
        for item in nav_items[:5]:
            await item.hover()
            await asyncio.sleep(0.5)
        await page.screenshot(path=os.path.join(OUT, "header_dropdown.png"))
        print("  header_dropdown.png")

        # 알림 드롭다운
        bell = await page.query_selector('.notification, .alarm, [class*="bell"], [class*="alarm"], [class*="noti"]')
        if bell:
            await bell.click()
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "header_alarm.png"))
            print("  header_alarm.png")

        # 검색 자동완성
        search = await page.query_selector('input[type="search"], input[name="keyword"], .search-input, input[placeholder*="검색"], input[placeholder*="search"]')
        if search:
            await search.click()
            await search.fill("Spring")
            await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "header_search.png"))
            print("  header_search.png")

        await browser.close()
        print("\nAll screenshots captured!")

asyncio.run(main())
