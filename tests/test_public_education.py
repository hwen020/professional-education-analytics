import openpyxl
import pandas as pd
import pymupdf
import pytest
from streamlit.testing.v1 import AppTest

from analytics import ROOT, load
from build import OUT
from public_education import SOURCE, STATE, observations


def test_public_time_series_and_grain():
    ftes, awards = observations()
    assert len(ftes)==85 and not ftes.duplicated(["district","fiscal_year"]).any()
    assert ftes.district.nunique()==17
    assert ftes.ftes.ge(0).all()
    assert set(ftes.source_id)=={"CDCP-2025"} and set(awards.source_id)=={"LAO-5150"}
    assert set(load("education_sources").source_id)=={"CDCP-2025","LAO-5150"}
    assert ftes.source_type.eq(SOURCE).all() and awards.source_type.eq(SOURCE).all()
    assert not awards.year.duplicated().any() and len(awards)==6


def test_public_year_over_year_boundaries():
    ftes, awards = observations()
    state = ftes[ftes.district.eq(STATE)].iloc[-1]
    assert state.ftes==57973.64 and state.change_ftes==6271.19
    assert state.yoy_rate==pytest.approx(57973.64/51702.45-1)
    compton = ftes[ftes.district.eq("Compton")].iloc[2]
    assert pd.isna(compton.yoy_rate) and compton.ftes==33.23
    assert pd.isna(awards.calendar_year_awards_yoy.iloc[0])
    assert awards.june_30_enrollment_yoy.iloc[-1]==pytest.approx(7660/4582-1)
    assert awards.calendar_year_awards_yoy.iloc[-1]==pytest.approx(1019/639-1)
    assert all("completion_rate" not in col for col in awards)


def test_public_education_export_reconciliation():
    for name, expected in zip(("public-cdcp-ftes","public-calbright-outcomes"),observations()):
        pd.testing.assert_frame_equal(pd.read_csv(OUT/f"{name}.csv"),expected)
    assert "source_id" not in pd.read_csv(OUT/"market-evidence.csv")
    assert not list(OUT.glob("ops-*.csv"))


def test_public_education_excel_reconciliation():
    path = OUT/"analysis-workbook.xlsx"
    book = openpyxl.load_workbook(path,data_only=True)
    table = book["Public FTES Explorer"]
    assert table["B9"].value==57973.64
    assert table["C9"].value==pytest.approx(57973.64/51702.45-1)
    assert book["Public Calbright"]["C7"].value==1019
    workbook = openpyxl.load_workbook(path)
    assert workbook["Public FTES Explorer"]["B9"].value.startswith("=SUMIFS")
    assert workbook["Public FTES Explorer"].data_validations.count==1
    if "Public FTES Pivot" in workbook:
        pivot, = workbook["Public FTES Pivot"]._pivots
        assert pivot.name=="PublicFTESPivot" and not (pivot.rowGrandTotals or pivot.colGrandTotals)


@pytest.mark.parametrize("name,pages",[("management-executive-brief",1),("public-education-case-study",8)])
def test_public_education_pdf(name,pages):
    with pymupdf.open(OUT/f"{name}.pdf") as pdf:
        assert len(pdf)==pages
        text = "".join(page.get_text() for page in pdf)
        for value in ("57,973.64","7,660","1,019"):
            assert value in text
        for page in pdf:
            assert "Public Education Evidence" in page.get_text()
            assert all(page.rect.contains(pymupdf.Rect(block[:4])) for block in page.get_text("blocks"))
            assert min(page.get_pixmap().samples)<100


def test_public_education_dashboard_filter():
    app = AppTest.from_file(str(ROOT/"app.py")).run(timeout=30)
    app.sidebar.radio[0].set_value("Public education evidence").run(timeout=30)
    assert not app.exception
    app.selectbox[0].set_value("Compton").run(timeout=30)
    assert not app.exception
    assert app.dataframe[0].value.district.eq("Compton").all()
    assert app.dataframe[1].value.calendar_year_awards.iloc[-1]==1019
