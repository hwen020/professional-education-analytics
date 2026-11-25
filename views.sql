CREATE VIEW market_evidence AS
SELECT candidate, soc, occupation, bls_growth_pct, bls_annual_openings, bls_median_usd,
       edd_growth_pct, edd_decade_openings, edd_median_hourly_usd, benchmark, benchmark_usd
FROM public_market;
