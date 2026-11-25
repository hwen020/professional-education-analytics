from analytics import load, scenario
from market import demand_score


def test_source_evidence():
    evidence = load("public_market")
    assert evidence.soc.tolist() == ["15-2051","15-1212","13-1082"]
    assert evidence.edd_decade_openings.tolist() == [2710,590,5200]
    assert evidence.bls_annual_openings.tolist() == [24800,14100,76500]
    assert evidence.notna().all().all()
    assert load("sources").url.str.startswith("https://").all()


def test_evidence_ranking():
    scores = demand_score()
    assert scores.iloc[0].candidate == "Data Analytics"
    assert scores.score.between(0,1).all()


def test_scenario_at_published_tuition():
    price = load("public_market").benchmark_usd.iloc[0]
    assert scenario(price,price,0,0)["break_even"] is None
    assert scenario(price,0,price,1) == {"contribution":0,"break_even":1}
