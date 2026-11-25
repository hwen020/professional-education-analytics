"""Load the cited occupational and provider snapshot."""
from analytics import load


def market():
    return load("public_market")


def demand_score():
    evidence = market()
    growth = evidence.bls_growth_pct / evidence.bls_growth_pct.max()
    national = evidence.bls_annual_openings / evidence.bls_annual_openings.max()
    regional = evidence.edd_decade_openings / evidence.edd_decade_openings.max()
    return evidence[["candidate", "soc"]].assign(
        score=.50*growth + .25*national + .25*regional
    ).sort_values("score", ascending=False)
