import asyncio
import traceback
from playwright.async_api import async_playwright

BASE = "http://localhost:10000"
OUT = r"C:\Users\pigch\Desktop\gb_0090_kyc\포트폴리오\screenshots\final"
NAV_TIMEOUT = 15000

async def login(page):
    await page.goto(f"{BASE}/main/log-in", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
    await page.wait_for_timeout(1000)
    await page.fill('input[name="memberId"]', "user_demo")
    await page.fill('input[name="memberPassword"]', "1234")
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

        await login(page)

        # ── FIX 1: footer_crop ──
        try:
            await page.goto(f"{BASE}/qna/list", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            # Get full page height and screenshot the bottom portion
            full_height = await page.evaluate("document.body.scrollHeight")
            print(f"  Page height: {full_height}")
            # Scroll to very bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(1000)

            # Try to get footer bounding box via JS
            box = await page.evaluate("""() => {
                const el = document.querySelector('footer') || document.querySelector('.footer') || document.querySelector('#footer');
                if (el) {
                    const r = el.getBoundingClientRect();
                    return {x: r.x, y: r.y, width: r.width, height: r.height, tag: el.tagName, cls: el.className};
                }
                return null;
            }""")
            print(f"  Footer box: {box}")

            if box and box['height'] > 0:
                # Use clip on the current viewport
                await page.screenshot(
                    path=f"{OUT}/footer_crop.png",
                    clip={"x": 0, "y": max(0, box['y']), "width": 1440, "height": min(box['height'] + 20, 900)}
                )
                print("  [OK] footer_crop (clip from bbox)")
            else:
                # Fallback: bottom 250px of viewport
                await page.screenshot(
                    path=f"{OUT}/footer_crop.png",
                    clip={"x": 0, "y": 650, "width": 1440, "height": 250}
                )
                print("  [OK] footer_crop (fallback clip)")
        except Exception as e:
            print(f"  [FAIL] footer_crop: {e}")
            traceback.print_exc()

        # ── FIX 2: unsubscribe_error ──
        try:
            await page.goto(f"{BASE}/mypage/unsubscribe", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)

            # Dump page structure for debugging
            html_snippet = await page.evaluate("""() => {
                const main = document.querySelector('main') || document.querySelector('.content') || document.body;
                return main.innerHTML.substring(0, 3000);
            }""")
            print(f"  Page HTML snippet: {html_snippet[:1500]}")

            # Handle dialogs
            dialog_messages = []
            async def handle_dialog(dialog):
                dialog_messages.append(dialog.message)
                print(f"  Dialog: {dialog.message}")
                await dialog.accept()
            page.on("dialog", handle_dialog)

            # Fill wrong name using JS to bypass visibility
            await page.evaluate("""() => {
                const inp = document.querySelector('input[name="memberName"]') || document.querySelector('input[name="name"]');
                if (inp) { inp.value = 'wrong_name_xxx'; inp.dispatchEvent(new Event('input')); }
            }""")

            # Check checkbox using JS
            await page.evaluate("""() => {
                const cb = document.querySelector('input[type="checkbox"]');
                if (cb) { cb.checked = true; cb.dispatchEvent(new Event('change')); }
            }""")

            await page.wait_for_timeout(500)

            # Click submit using JS
            await page.evaluate("""() => {
                const btns = [...document.querySelectorAll('button, input[type="submit"]')];
                const btn = btns.find(b => b.textContent.includes('탈퇴') || b.textContent.includes('확인') || b.type === 'submit');
                if (btn) btn.click();
            }""")

            await page.wait_for_timeout(2000)
            await page.screenshot(path=f"{OUT}/unsubscribe_error.png", full_page=True)
            print(f"  [OK] unsubscribe_error, dialogs: {dialog_messages}")
            page.remove_listener("dialog", handle_dialog)
        except Exception as e:
            print(f"  [FAIL] unsubscribe_error: {e}")
            traceback.print_exc()

        # Re-login in case
        try:
            await login(page)
        except:
            pass

        # ── FIX 3: qna_write_category_modal ──
        try:
            await page.goto(f"{BASE}/qna/write", timeout=NAV_TIMEOUT, wait_until="domcontentloaded")
            await page.wait_for_timeout(1500)

            # Debug: dump form elements
            form_info = await page.evaluate("""() => {
                const selects = [...document.querySelectorAll('select')].map(s => ({name: s.name, id: s.id, cls: s.className, opts: s.options.length, visible: s.offsetHeight > 0}));
                const buttons = [...document.querySelectorAll('button, [class*="category"], [class*="tag"]')].map(b => ({tag: b.tagName, text: b.textContent.trim().substring(0,50), cls: b.className, visible: b.offsetHeight > 0}));
                return {selects, buttons};
            }""")
            print(f"  Form selects: {form_info['selects']}")
            print(f"  Form buttons (first 10): {form_info['buttons'][:10]}")

            # Try to expand visible select elements
            expanded = await page.evaluate("""() => {
                const selects = document.querySelectorAll('select');
                let count = 0;
                for (const s of selects) {
                    if (s.offsetHeight > 0) {
                        s.setAttribute('size', s.options.length);
                        s.focus();
                        count++;
                    }
                }
                return count;
            }""")
            print(f"  Expanded {expanded} visible selects")

            if expanded == 0:
                # Try clicking visible category-like elements
                await page.evaluate("""() => {
                    const els = document.querySelectorAll('[class*="category"], [class*="tag"], [class*="select"]');
                    for (const el of els) {
                        if (el.offsetHeight > 0 && el.offsetWidth > 0) {
                            el.click();
                            break;
                        }
                    }
                }""")

            await page.wait_for_timeout(1000)
            await page.screenshot(path=f"{OUT}/qna_write_category_modal.png", full_page=True)
            print("  [OK] qna_write_category_modal")
        except Exception as e:
            print(f"  [FAIL] qna_write_category_modal: {e}")
            traceback.print_exc()

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
