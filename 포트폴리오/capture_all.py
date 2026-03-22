import asyncio, os
from playwright.async_api import async_playwright

BASE = "http://localhost:10000"
OUT = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\screenshots\final"
os.makedirs(OUT, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
        page = await ctx.new_page()
        page.set_default_timeout(10000)

        # Login
        await page.goto(f"{BASE}/main/log-in")
        await page.wait_for_load_state("networkidle")
        await page.fill('input[name="memberId"]', 'user_demo')
        await page.fill('input[name="memberPassword"]', '1234')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle")
        print(f"Login: {page.url}")

        async def safe_shot(name, fn):
            try:
                await fn()
                sz = os.path.getsize(os.path.join(OUT, name))
                print(f"  OK: {name} ({sz//1024}KB)")
            except Exception as e:
                print(f"  FAIL: {name} - {str(e)[:100]}")

        # -- QnA Detail with comments --
        async def f1():
            await page.goto(f"{BASE}/qna/detail?id=7001", timeout=15000)
            await page.wait_for_load_state("networkidle", timeout=15000)
            await page.screenshot(path=os.path.join(OUT, "qna_detail.png"), full_page=True)
        await safe_shot("qna_detail.png", f1)

        # -- Footer --
        async def f2():
            await page.goto(f"{BASE}/qna/list")
            await page.wait_for_load_state("networkidle")
            ft = await page.query_selector("footer")
            if ft:
                await ft.screenshot(path=os.path.join(OUT, "footer_crop.png"))
            else:
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(0.5)
                await page.screenshot(path=os.path.join(OUT, "footer_crop.png"), clip={"x":0,"y":700,"width":1440,"height":200})
        await safe_shot("footer_crop.png", f2)

        # -- MyPage Home --
        async def f3():
            await page.goto(f"{BASE}/mypage/mypage")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=os.path.join(OUT, "mypage_home.png"), full_page=True)
        await safe_shot("mypage_home.png", f3)

        # -- Edit Info --
        async def f4():
            await page.goto(f"{BASE}/mypage/change-my-information")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=os.path.join(OUT, "edit_info.png"), full_page=True)
        await safe_shot("edit_info.png", f4)

        # -- Edit Info Validation --
        async def f4v():
            await page.goto(f"{BASE}/mypage/change-my-information")
            await page.wait_for_load_state("networkidle")
            nm = await page.query_selector('input[name="memberName"]')
            if nm:
                await nm.fill("")
            btn = await page.query_selector('button:has-text("수정"), button[type="submit"]')
            if btn:
                await btn.click()
                await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "edit_validation.png"), full_page=True)
        await safe_shot("edit_validation.png", f4v)

        # -- Notifications --
        async def f5():
            await page.goto(f"{BASE}/mypage/notification")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=os.path.join(OUT, "notification.png"), full_page=True)
        await safe_shot("notification.png", f5)

        # -- Notification Filter --
        async def f5f():
            await page.goto(f"{BASE}/mypage/notification")
            await page.wait_for_load_state("networkidle")
            sel = await page.query_selector("select")
            if sel:
                await sel.evaluate("el => { el.size = el.options.length; }")
                await asyncio.sleep(0.3)
            await page.screenshot(path=os.path.join(OUT, "notification_filter.png"), full_page=True)
        await safe_shot("notification_filter.png", f5f)

        # -- Experience --
        async def f6():
            await page.goto(f"{BASE}/mypage/experience")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=os.path.join(OUT, "experience.png"), full_page=True)
        await safe_shot("experience.png", f6)

        # -- Experience Filter --
        async def f6f():
            await page.goto(f"{BASE}/mypage/experience")
            await page.wait_for_load_state("networkidle")
            sels = await page.query_selector_all("select")
            for s in sels[:2]:
                await s.evaluate("el => { el.size = Math.min(el.options.length, 5); }")
            await asyncio.sleep(0.3)
            await page.screenshot(path=os.path.join(OUT, "experience_filter.png"), full_page=True)
        await safe_shot("experience_filter.png", f6f)

        # -- Unsubscribe --
        async def f7():
            await page.goto(f"{BASE}/mypage/unsubscribe")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=os.path.join(OUT, "unsubscribe.png"), full_page=True)
        await safe_shot("unsubscribe.png", f7)

        # -- Unsubscribe Error --
        async def f7e():
            await page.goto(f"{BASE}/mypage/unsubscribe")
            await page.wait_for_load_state("networkidle")
            page.on("dialog", lambda d: d.accept())
            nm = await page.query_selector('input[placeholder*="이름"], input[name*="name"]')
            if nm:
                await nm.fill("틀린이름")
            lbl = await page.query_selector('label[for*="chk"], label[for*="agree"]')
            if lbl:
                await lbl.click()
                await asyncio.sleep(0.3)
            btn = await page.query_selector('button:has-text("탈퇴")')
            if btn:
                await btn.click()
                await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "unsubscribe_error.png"), full_page=True)
        await safe_shot("unsubscribe_error.png", f7e)

        # -- Header States --
        # Logged in header
        async def fh1():
            await page.goto(f"{BASE}/qna/list")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=os.path.join(OUT, "header_loggedin.png"), clip={"x":0,"y":0,"width":1440,"height":140})
        await safe_shot("header_loggedin.png", fh1)

        # GNB hover
        async def fh2():
            await page.goto(f"{BASE}/qna/list")
            await page.wait_for_load_state("networkidle")
            items = await page.query_selector_all("header nav > ul > li, .gnb > ul > li, nav > ul > li")
            if items:
                await items[0].hover()
                await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "gnb_hover.png"), clip={"x":0,"y":0,"width":1440,"height":350})
        await safe_shot("gnb_hover.png", fh2)

        # Profile dropdown
        async def fh3():
            await page.goto(f"{BASE}/qna/list")
            await page.wait_for_load_state("networkidle")
            prof = await page.query_selector('[class*="user-name"], [class*="member"], header [class*="profile"] a')
            if not prof:
                prof = await page.query_selector("header a:has-text('Demo')")
            if prof:
                await prof.click()
                await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "profile_dropdown.png"), clip={"x":800,"y":0,"width":640,"height":400})
        await safe_shot("profile_dropdown.png", fh3)

        # Alarm dropdown
        async def fh4():
            await page.goto(f"{BASE}/qna/list")
            await page.wait_for_load_state("networkidle")
            bell = await page.query_selector('[class*="alarm"] a, [class*="bell"] a, [class*="noti"] a')
            if not bell:
                bell = await page.query_selector('header svg, header [class*="alarm"]')
            if bell:
                await bell.click()
                await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "alarm_dropdown.png"), clip={"x":600,"y":0,"width":840,"height":500})
        await safe_shot("alarm_dropdown.png", fh4)

        # Search autocomplete
        async def fh5():
            await page.goto(f"{BASE}/qna/list")
            await page.wait_for_load_state("networkidle")
            search = await page.query_selector('input[placeholder*="try"], input[type="search"], input[name="keyword"]')
            if search:
                await search.click()
                await search.fill("Spring")
                await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "search_autocomplete.png"), clip={"x":200,"y":0,"width":800,"height":300})
        await safe_shot("search_autocomplete.png", fh5)

        # Logged out header
        async def fh6():
            await ctx.clear_cookies()
            await page.goto(f"{BASE}/qna/list")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=os.path.join(OUT, "header_loggedout.png"), clip={"x":0,"y":0,"width":1440,"height":140})
        await safe_shot("header_loggedout.png", fh6)

        # -- Re-login for remaining --
        await page.goto(f"{BASE}/main/log-in")
        await page.wait_for_load_state("networkidle")
        await page.fill('input[name="memberId"]', 'user_demo')
        await page.fill('input[name="memberPassword"]', '1234')
        await page.click('button[type="submit"]')
        await page.wait_for_load_state("networkidle")

        # Point
        async def fp():
            await page.goto(f"{BASE}/point/point")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=os.path.join(OUT, "point.png"), full_page=True)
        await safe_shot("point.png", fp)

        # QnA Write
        async def fqw():
            await page.goto(f"{BASE}/qna/write")
            await page.wait_for_load_state("networkidle")
            await page.screenshot(path=os.path.join(OUT, "qna_write.png"), full_page=True)
        await safe_shot("qna_write.png", fqw)

        # QnA Write - Category modal
        async def fqwc():
            await page.goto(f"{BASE}/qna/write")
            await page.wait_for_load_state("networkidle")
            cat = await page.query_selector('[class*="category"], select[name*="category"], [class*="job"]')
            if cat:
                await cat.click()
                await asyncio.sleep(1)
            await page.screenshot(path=os.path.join(OUT, "qna_category.png"), full_page=True)
        await safe_shot("qna_category.png", fqwc)

        await browser.close()
        print("\n=== COMPLETE ===")
        # List all files
        for f in sorted(os.listdir(OUT)):
            sz = os.path.getsize(os.path.join(OUT, f))
            print(f"  {f}: {sz//1024}KB")

asyncio.run(main())
