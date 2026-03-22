import asyncio
import traceback
from playwright.async_api import async_playwright

BASE = "http://localhost:10000"
OUT = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\screenshots\final"
NAV_TIMEOUT = 15000
results = []

def log(name, ok, msg=""):
    status = "OK" if ok else "FAIL"
    results.append((name, status, msg))
    print(f"[{status}] {name} {msg}")


async def login(page):
    """Login and return True on success."""
    await page.goto(f"{BASE}/main/log-in", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
    await page.wait_for_timeout(1000)
    # Fill login form
    await page.fill('input[name="memberId"]', "user_demo")
    await page.fill('input[name="memberPassword"]', "1234")
    # Click submit
    btn = page.locator('button[type="submit"], input[type="submit"]')
    if await btn.count() > 0:
        await btn.first.click()
    else:
        await page.locator('form').first.evaluate("el => el.submit()")
    await page.wait_for_timeout(2000)
    print(f"  After login URL: {page.url}")


async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,
            locale="ko-KR",
        )
        page = await context.new_page()
        page.set_default_timeout(10000)

        # ── Login ──
        try:
            await login(page)
            log("login", True)
        except Exception as e:
            log("login", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 1. QnA detail full
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/qna/detail?id=7001", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"{OUT}/qna_detail_full.png", full_page=True)
            log("qna_detail_full", True)
        except Exception as e:
            log("qna_detail_full", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 2 & 3. Footer
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/qna/list", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            # Scroll to bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)
            # Try to find footer element
            footer = page.locator("footer, .footer, #footer, [class*='footer']").first
            if await footer.count() > 0:
                await footer.screenshot(path=f"{OUT}/footer_crop.png")
                log("footer_crop", True)
            else:
                # Fallback: clip bottom 300px
                await page.screenshot(path=f"{OUT}/footer_crop.png", clip={"x": 0, "y": 700, "width": 1440, "height": 200})
                log("footer_crop", True, "(fallback clip)")
        except Exception as e:
            log("footer_crop", False, str(e))
            traceback.print_exc()

        try:
            await page.goto(f"{BASE}/qna/list", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)
            await page.screenshot(path=f"{OUT}/footer_full.png", full_page=True)
            log("footer_full", True)
        except Exception as e:
            log("footer_full", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 4. Mypage home
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/mypage/mypage", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"{OUT}/mypage_home_full.png", full_page=True)
            log("mypage_home_full", True)
        except Exception as e:
            log("mypage_home_full", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 5. Mypage profile camera click
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/mypage/mypage", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)
            # Try clicking profile image area
            profile_selectors = [
                ".profile-image", ".profile-img", ".profile",
                "img[class*='profile']", ".camera", ".avatar",
                ".mypage-profile", "[class*='profile'] img",
                ".profile-area", ".user-image"
            ]
            clicked = False
            for sel in profile_selectors:
                loc = page.locator(sel).first
                if await loc.count() > 0:
                    await loc.click()
                    clicked = True
                    print(f"  Clicked profile: {sel}")
                    break
            if not clicked:
                # Try any img in the main content area
                imgs = page.locator("main img, .content img, .container img").first
                if await imgs.count() > 0:
                    await imgs.click()
                    print("  Clicked first content image")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=f"{OUT}/mypage_profile_camera.png", full_page=True)
            log("mypage_profile_camera", True)
        except Exception as e:
            log("mypage_profile_camera", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 6. Edit info full
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/mypage/change-my-information", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"{OUT}/edit_info_full.png", full_page=True)
            log("edit_info_full", True)
        except Exception as e:
            log("edit_info_full", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 7. Edit info validation error
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/mypage/change-my-information", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)

            # Handle any dialog that might appear
            dialog_msg = []
            page.on("dialog", lambda d: asyncio.ensure_future(_handle_dialog(d, dialog_msg)))

            # Clear name field
            name_selectors = [
                'input[name="memberName"]', 'input[name="name"]',
                'input[name="memberNickname"]', 'input[name="nickname"]',
                'input#memberName', 'input#name'
            ]
            for sel in name_selectors:
                loc = page.locator(sel).first
                if await loc.count() > 0:
                    await loc.fill("")
                    print(f"  Cleared name field: {sel}")
                    break

            # Click submit
            submit_selectors = [
                'button[type="submit"]', 'input[type="submit"]',
                'button:has-text("수정")', 'button:has-text("변경")',
                'button:has-text("저장")', 'button:has-text("확인")',
                '.btn-submit', '.submit-btn'
            ]
            for sel in submit_selectors:
                loc = page.locator(sel).first
                if await loc.count() > 0:
                    await loc.click()
                    print(f"  Clicked submit: {sel}")
                    break

            await page.wait_for_timeout(1500)
            await page.screenshot(path=f"{OUT}/edit_info_validation.png", full_page=True)
            log("edit_info_validation", True)
        except Exception as e:
            log("edit_info_validation", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 8. Notification full
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/mypage/notification", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"{OUT}/notification_full.png", full_page=True)
            log("notification_full", True)
        except Exception as e:
            log("notification_full", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 9. Notification filter open
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/mypage/notification", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)
            # Find select element and expand it
            sel_el = page.locator("select").first
            if await sel_el.count() > 0:
                await sel_el.evaluate("el => el.setAttribute('size', el.options.length)")
                await page.wait_for_timeout(500)
                log_text = "expanded select"
            else:
                # Try clicking a filter button/dropdown
                filter_sels = [".filter", ".dropdown", "[class*='filter']", "button:has-text('필터')"]
                for fs in filter_sels:
                    loc = page.locator(fs).first
                    if await loc.count() > 0:
                        await loc.click()
                        log_text = f"clicked {fs}"
                        break
                else:
                    log_text = "no filter found"
            await page.wait_for_timeout(800)
            await page.screenshot(path=f"{OUT}/notification_filter_open.png", full_page=True)
            log("notification_filter_open", True, log_text)
        except Exception as e:
            log("notification_filter_open", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 10. Experience full
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/mypage/experience", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"{OUT}/experience_full.png", full_page=True)
            log("experience_full", True)
        except Exception as e:
            log("experience_full", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 11. Experience filter open
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/mypage/experience", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)
            selects = page.locator("select")
            count = await selects.count()
            for i in range(count):
                await selects.nth(i).evaluate("el => el.setAttribute('size', el.options.length)")
            await page.wait_for_timeout(800)
            await page.screenshot(path=f"{OUT}/experience_filter_open.png", full_page=True)
            log("experience_filter_open", True, f"{count} selects expanded")
        except Exception as e:
            log("experience_filter_open", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 12. Unsubscribe full
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/mypage/unsubscribe", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"{OUT}/unsubscribe_full.png", full_page=True)
            log("unsubscribe_full", True)
        except Exception as e:
            log("unsubscribe_full", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 13. Unsubscribe error
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/mypage/unsubscribe", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)

            # Set up dialog handler
            dialog_messages = []
            async def handle_unsub_dialog(dialog):
                dialog_messages.append(dialog.message)
                print(f"  Dialog: {dialog.message}")
                await dialog.accept()
            page.on("dialog", handle_unsub_dialog)

            # Enter wrong name
            name_inputs = [
                'input[name="memberName"]', 'input[name="name"]',
                'input[type="text"]'
            ]
            for sel in name_inputs:
                loc = page.locator(sel).first
                if await loc.count() > 0:
                    await loc.fill("wrong_name_xxx")
                    print(f"  Filled wrong name in: {sel}")
                    break

            # Click checkbox LABEL
            label_selectors = [
                'label[for*="agree"]', 'label[for*="check"]', 'label[for*="confirm"]',
                'label:has(input[type="checkbox"])', 'label'
            ]
            for sel in label_selectors:
                loc = page.locator(sel).first
                if await loc.count() > 0:
                    await loc.click()
                    print(f"  Clicked label: {sel}")
                    break

            await page.wait_for_timeout(500)

            # Click unsubscribe button
            unsub_btns = [
                'button:has-text("탈퇴")', 'button:has-text("회원탈퇴")',
                'input[type="submit"]', 'button[type="submit"]',
                'button:has-text("확인")', '.btn-danger', '.btn-delete'
            ]
            for sel in unsub_btns:
                loc = page.locator(sel).first
                if await loc.count() > 0:
                    await loc.click()
                    print(f"  Clicked unsub btn: {sel}")
                    break

            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"{OUT}/unsubscribe_error.png", full_page=True)
            log("unsubscribe_error", True, f"dialogs: {dialog_messages}")

            # Remove handler
            page.remove_listener("dialog", handle_unsub_dialog)
        except Exception as e:
            log("unsubscribe_error", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # Re-login in case unsubscribe messed things up
        # ──────────────────────────────────────────
        try:
            await login(page)
        except:
            pass

        # ──────────────────────────────────────────
        # 14. Header logged in
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/qna/list", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)
            header = page.locator("header, .header, #header, nav, .navbar, .gnb").first
            if await header.count() > 0:
                await header.screenshot(path=f"{OUT}/header_loggedin.png")
                log("header_loggedin", True, "element screenshot")
            else:
                await page.screenshot(path=f"{OUT}/header_loggedin.png", clip={"x": 0, "y": 0, "width": 1440, "height": 120})
                log("header_loggedin", True, "clip fallback")
        except Exception as e:
            log("header_loggedin", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 17. Header profile dropdown (do BEFORE logout)
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/qna/list", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)
            profile_triggers = [
                ".profile-dropdown", ".user-menu", ".user-dropdown",
                "[class*='profile']", ".dropdown-toggle:has-text('user')",
                "a:has-text('user_demo')", ".username", ".member-name",
                ".header .profile", "header .dropdown", ".gnb .profile"
            ]
            for sel in profile_triggers:
                loc = page.locator(sel).first
                if await loc.count() > 0:
                    await loc.click()
                    print(f"  Clicked profile trigger: {sel}")
                    break
            await page.wait_for_timeout(1000)
            await page.screenshot(path=f"{OUT}/header_profile_dropdown.png", clip={"x": 0, "y": 0, "width": 1440, "height": 500})
            log("header_profile_dropdown", True)
        except Exception as e:
            log("header_profile_dropdown", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 18. Header alarm dropdown
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/qna/list", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)
            alarm_triggers = [
                ".alarm", ".notification-bell", ".bell", "[class*='alarm']",
                "[class*='bell']", "[class*='noti']", "i.fa-bell",
                ".bi-bell", "svg.bell", "[class*='alert-icon']",
                "button[class*='alarm']", "a[class*='alarm']",
                "button[class*='noti']", "a[class*='noti']",
                ".header-alarm", ".header-notification"
            ]
            for sel in alarm_triggers:
                loc = page.locator(sel).first
                if await loc.count() > 0:
                    await loc.click()
                    print(f"  Clicked alarm trigger: {sel}")
                    break
            await page.wait_for_timeout(1000)
            await page.screenshot(path=f"{OUT}/header_alarm_dropdown.png", clip={"x": 0, "y": 0, "width": 1440, "height": 600})
            log("header_alarm_dropdown", True)
        except Exception as e:
            log("header_alarm_dropdown", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 16. Header GNB hover
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/qna/list", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)
            nav_items = page.locator("nav a, .gnb a, .nav-item, .menu-item, header a").first
            if await nav_items.count() > 0:
                await nav_items.hover()
                print("  Hovered nav item")
            await page.wait_for_timeout(1000)
            await page.screenshot(path=f"{OUT}/header_gnb_hover.png", clip={"x": 0, "y": 0, "width": 1440, "height": 400})
            log("header_gnb_hover", True)
        except Exception as e:
            log("header_gnb_hover", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 19. Header search autocomplete
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/qna/list", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)
            search_inputs = [
                'input[type="search"]', 'input[name="search"]',
                'input[name="keyword"]', 'input[name="query"]',
                'input[placeholder*="검색"]', 'input[placeholder*="search"]',
                '.search-input', '#search', '.header input', 'header input'
            ]
            typed = False
            for sel in search_inputs:
                loc = page.locator(sel).first
                if await loc.count() > 0:
                    await loc.click()
                    await page.wait_for_timeout(300)
                    await loc.type("Spring", delay=150)
                    typed = True
                    print(f"  Typed in search: {sel}")
                    break
            await page.wait_for_timeout(1500)
            await page.screenshot(path=f"{OUT}/header_search_autocomplete.png", clip={"x": 0, "y": 0, "width": 1440, "height": 500})
            log("header_search_autocomplete", True, f"typed={typed}")
        except Exception as e:
            log("header_search_autocomplete", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 15. Header logged out
        # ──────────────────────────────────────────
        try:
            await context.clear_cookies()
            await page.goto(f"{BASE}/qna/list", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)
            header = page.locator("header, .header, #header, nav, .navbar, .gnb").first
            if await header.count() > 0:
                await header.screenshot(path=f"{OUT}/header_loggedout.png")
                log("header_loggedout", True, "element screenshot")
            else:
                await page.screenshot(path=f"{OUT}/header_loggedout.png", clip={"x": 0, "y": 0, "width": 1440, "height": 120})
                log("header_loggedout", True, "clip fallback")
        except Exception as e:
            log("header_loggedout", False, str(e))
            traceback.print_exc()

        # ── Re-login for remaining pages ──
        try:
            await login(page)
        except:
            pass

        # ──────────────────────────────────────────
        # 20. Point full
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/point/point", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"{OUT}/point_full.png", full_page=True)
            log("point_full", True)
        except Exception as e:
            log("point_full", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 22. QnA write full (do before category modal)
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/qna/write", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"{OUT}/qna_write_full.png", full_page=True)
            log("qna_write_full", True)
        except Exception as e:
            log("qna_write_full", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        # 21. QnA write category modal
        # ──────────────────────────────────────────
        try:
            await page.goto(f"{BASE}/qna/write", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)
            # Try select element first
            cat_select = page.locator("select[name*='category'], select[name*='type'], select").first
            if await cat_select.count() > 0:
                await cat_select.evaluate("el => el.setAttribute('size', el.options.length)")
                await page.wait_for_timeout(500)
                print("  Expanded category select")
            else:
                # Try clicking a category button/dropdown
                cat_triggers = [
                    "[class*='category']", "button:has-text('카테고리')",
                    ".dropdown", "[class*='tag']"
                ]
                for sel in cat_triggers:
                    loc = page.locator(sel).first
                    if await loc.count() > 0:
                        await loc.click()
                        print(f"  Clicked category trigger: {sel}")
                        break
            await page.wait_for_timeout(800)
            await page.screenshot(path=f"{OUT}/qna_write_category_modal.png", full_page=True)
            log("qna_write_category_modal", True)
        except Exception as e:
            log("qna_write_category_modal", False, str(e))
            traceback.print_exc()

        # ──────────────────────────────────────────
        await browser.close()

    # Summary
    print("\n" + "="*60)
    print("SCREENSHOT CAPTURE SUMMARY")
    print("="*60)
    ok_count = sum(1 for _, s, _ in results if s == "OK")
    fail_count = sum(1 for _, s, _ in results if s == "FAIL")
    for name, status, msg in results:
        print(f"  [{status}] {name}  {msg}")
    print(f"\nTotal: {ok_count} OK, {fail_count} FAIL out of {len(results)}")


async def _handle_dialog(dialog, msg_list):
    msg_list.append(dialog.message)
    print(f"  Dialog appeared: {dialog.message}")
    await dialog.accept()


if __name__ == "__main__":
    asyncio.run(run())
