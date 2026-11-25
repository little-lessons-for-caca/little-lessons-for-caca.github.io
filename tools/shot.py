#!/usr/bin/env python3
"""Screenshot a lesson at desktop, phone-portrait and phone-landscape sizes.

Usage: python3 tools/shot.py day-night   (writes /tmp/shot-*.png)
Needs: pip install playwright, and a Chrome/Chromium binary (CHROME env var).
The page is served from a local web server so the voice clips load.
"""
import asyncio, functools, http.server, os, pathlib, sys, threading

from playwright.async_api import async_playwright

root = pathlib.Path(__file__).resolve().parent.parent
lesson = sys.argv[1]
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{server.server_address[1]}/{lesson}/"
SIZES = {"desktop": (1280, 720), "phone-portrait": (393, 660), "phone-landscape": (760, 345)}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=os.environ.get("CHROME", "/usr/bin/google-chrome"),
                                    args=["--no-sandbox", "--autoplay-policy=no-user-gesture-required"])
        for name, (w, h) in SIZES.items():
            pg = await b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
            errors = []
            pg.on("pageerror", lambda e: errors.append(str(e)))
            await pg.goto(url)
            await pg.wait_for_timeout(600)
            if await pg.locator("#start").count():
                await pg.click("#start")
            await pg.wait_for_timeout(6000)
            await pg.screenshot(path=f"/tmp/shot-{name}.png")
            wide = await pg.evaluate("document.documentElement.scrollWidth")
            print(name, "sideways scroll!" if wide > w else "ok", errors or "")
            await pg.close()
        await b.close()

asyncio.run(main())
