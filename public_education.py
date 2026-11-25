"""Analyze public education aggregates independently of the market models."""
import pandas as pd

from analytics import load

SOURCE = "Public observations"
STATE = "California statewide"


def observations():
    cdcp = load("public_cdcp").melt(id_vars="district", var_name="fiscal_year",value_name="ftes")
    cdcp = cdcp.sort_values(["district","fiscal_year"]).reset_index(drop=True)
    prior = cdcp.groupby("district").ftes.shift()
    cdcp["change_ftes"] = (cdcp.ftes-prior).round(2)
    cdcp["yoy_rate"] = cdcp.ftes.div(prior.where(prior.gt(0)))-1
    cdcp["source_type"] = SOURCE
    cdcp["source_id"] = "CDCP-2025"
    calbright = load("public_calbright").sort_values("year")
    for metric in ("june_30_enrollment","calendar_year_awards"):
        calbright[f"{metric}_yoy"] = calbright[metric].pct_change()
    calbright["source_type"] = SOURCE
    calbright["source_id"] = "LAO-5150"
    return cdcp, calbright


def public_findings(cdcp, calbright):
    state = cdcp[cdcp.district.eq(STATE)]
    latest = state.iloc[-1]
    row = calbright.iloc[-1]
    return {
        "state": f"California reported {latest.ftes:,.2f} noncredit CDCP FTES in {latest.fiscal_year}, "
                 f"up {latest.yoy_rate:.1%} from the prior fiscal year.",
        "provider": f"Calbright reported {int(row.june_30_enrollment):,} students enrolled on June 30, {int(row.year)} "
                    f"and {int(row.calendar_year_awards):,} awards during calendar year {int(row.year)}. "
                    f"The respective counts grew {row.june_30_enrollment_yoy:.1%} and {row.calendar_year_awards_yoy:.1%}.",
    }
