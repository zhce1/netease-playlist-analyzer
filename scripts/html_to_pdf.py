#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将HTML报告转换为PDF
用法: python html_to_pdf.py <input_html> <output_pdf>
依赖: playwright (pip install playwright && playwright install chromium)
"""
import asyncio
import sys
import os


async def html_to_pdf(html_path, pdf_path):
    """使用playwright将HTML转为PDF"""
    from playwright.async_api import async_playwright

    html_path = os.path.abspath(html_path)
    pdf_path = os.path.abspath(pdf_path)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f"file://{html_path}", wait_until="networkidle")
        await page.wait_for_timeout(3000)  # 等待字体加载

        await page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={
                "top": "0",
                "right": "0",
                "bottom": "0",
                "left": "0"
            }
        )

        await browser.close()
        print(f"✅ PDF已生成: {pdf_path}")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python html_to_pdf.py <input_html> <output_pdf>")
        sys.exit(1)
    asyncio.run(html_to_pdf(sys.argv[1], sys.argv[2]))
