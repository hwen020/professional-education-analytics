import openpyxl
import pandas as pd
import pymupdf
import pytest
from streamlit.testing.v1 import AppTest

from analytics import ROOT
from build import OUT
from market import market


def test_public_export_reconciles():
    export = pd.read_csv(OUT/"market-evidence.csv")
    pd.testing.assert_frame_equal(export, market()[export.columns])
    assert export.soc.is_unique
    assert not list(OUT.glob("synthetic-*"))


def test_workbook_structure():
    file = OUT/"analysis-workbook.xlsx"
    book = openpyxl.load_workbook(file)
    assert book.calculation.calcMode in (None,"auto")
    assert book.calculation.fullCalcOnLoad
    pilot = book["Pilot inputs"]
    assert all(pilot[key].value is None for key in ("B1","B2","B3","B6","B7","B8"))
    assert pilot["C7"].value.startswith("=")
    rendered = openpyxl.load_workbook(file,data_only=True)
    assert rendered["QA"]["B1"].value == 0
    assert rendered["QA"]["B2"].value == len(market())


@pytest.mark.parametrize("file,count", [("executive-summary.pdf",1),("integrated-report.pdf",9)])
def test_pdf_render(file,count):
    with pymupdf.open(OUT/file) as document:
        assert len(document) == count
        for page in document:
            assert len(page.get_text()) > 250
            assert all(page.rect.contains(pymupdf.Rect(block[:4])) for block in page.get_text("blocks"))
            assert min(page.get_pixmap().samples) < 100


@pytest.mark.parametrize("page", ["Portfolio","Instructor recruitment","Instructor services",
                                   "Qualitative insights","Market intelligence","Business case","Delivery & governance"])
def test_dashboard(page):
    app = AppTest.from_file(str(ROOT/"app.py")).run(timeout=30)
    app.sidebar.radio[0].set_value(page).run(timeout=30)
    assert not app.exception
    assert app.header[0].value == page
    if page in ("Portfolio","Instructor recruitment","Instructor services","Qualitative insights"):
        assert "No verified" in app.info[0].value
    if page == "Business case":
        assert all(field.value is None for field in app.number_input)
