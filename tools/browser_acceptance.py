"""Optional Playwright validation against a running Streamlit app."""
import argparse
from pathlib import Path
from zipfile import ZipFile

from playwright.sync_api import sync_playwright


def select(page, name, mobile):
    if mobile:
        page.get_by_role("button",name="Expand sidebar").click()
    page.get_by_test_id("stSidebar").get_by_text(name,exact=True).click()
    page.get_by_role("heading",name=name,exact=True).wait_for()
    if mobile:
        control = page.get_by_role("button",name="Collapse sidebar")
        if control.is_visible():
            control.click()


def verify(url, edge, screenshots):
    out = Path(__file__).resolve().parents[1]/"deliverables"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=edge)
        for width,height in ((1440,900),(390,844)):
            mobile = width==390
            page = browser.new_page(viewport={"width":width,"height":height},accept_downloads=True)
            try:
                page.goto(url,wait_until="domcontentloaded",timeout=60000)
                page.get_by_text("No verified operational observations",exact=False).wait_for(timeout=60000)
                select(page,"Public education evidence",mobile)
                page.get_by_text("57,973.64 noncredit CDCP FTES",exact=False).wait_for()
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                if screenshots:
                    page.screenshot(path=str(screenshots/f"public-education-{width}.png"),animations="disabled")
                with page.expect_download() as csv:
                    page.get_by_role("button",name="Download public FTES CSV").click()
                ftes = Path(csv.value.path()).read_text(encoding="utf-8")
                assert "57973.64" in ftes and "California statewide" in ftes and "CDCP-2025" in ftes
                with page.expect_download() as csv:
                    page.get_by_role("button",name="Download public outcomes CSV").click()
                outcomes = Path(csv.value.path()).read_text(encoding="utf-8")
                assert "2025,7660,1019" in outcomes and "LAO-5150" in outcomes
                select(page,"Market intelligence",mobile)
                page.get_by_role("heading",name="Public Market Evidence").wait_for()
                with page.expect_download() as csv:
                    page.get_by_role("button",name="Download CSV").first.click()
                assert "15-2051" in Path(csv.value.path()).read_text(encoding="utf-8")
                if not mobile:
                    select(page,"Delivery & governance",mobile)
                    with page.expect_download() as excel:
                        page.get_by_role("button",name="analysis-workbook.xlsx").click()
                    with ZipFile(excel.value.path()) as workbook:
                        assert any(part.startswith("xl/pivotTables/pivotTable") for part in workbook.namelist())
                    with page.expect_download() as pdf:
                        page.get_by_role("button",name="public-education-case-study.pdf").click()
                    assert Path(pdf.value.path()).read_bytes()==(out/"public-education-case-study.pdf").read_bytes()
                print(f"{width}x{height} passed: navigation, layout and real downloads",flush=True)
            finally:
                page.close()


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--edge")
    parser.add_argument("--screenshots",type=Path)
    options = parser.parse_args()
    verify(options.url,options.edge,options.screenshots)
