import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WHO_BASE = "https://ghoapi.azureedge.net/api"

@app.get("/")
def root():
    return {"message": "Backend is running! Use /api/disease?name=malaria"}

@app.get("/api/disease")
def get_disease(name: str):
    results = {
        "overview": f"{name.capitalize()} data dashboard",
        "pubmed": [f"https://pubmed.ncbi.nlm.nih.gov/?term={name}"],
        "ayurveda_research": [f"https://dharaonline.org/Search.aspx?query={name}"],
        "clinical_trials": [f"https://ctri.nic.in/Clinicaltrials/advsearch.php?trial={name}"],
        "statistics": {
            "prevalence_trend": [],
            "mortality_trend": [],
            "dalys_trend": [],
            "region_data": [],
            "age_sex_data": []
        }
    }

    # WHO Prevalence trend
    try:
        prev_res = requests.get(f"{WHO_BASE}/WHOSIS_000001?$filter=contains(IndicatorName,'{name}')&$format=json")
        if prev_res.ok:
            vals = prev_res.json().get("value", [])[:10]
            results["statistics"]["prevalence_trend"] = [
                {"year": int(v.get("TimePeriod", 0)), "cases": float(v.get("NumericValue", 0))}
                for v in vals if v.get("TimePeriod") and v.get("NumericValue")
            ]
    except Exception as e:
        results["statistics"]["prevalence_trend"] = [{"year": 0, "cases": 0, "error": str(e)}]

    # WHO Mortality trend
    try:
        mort_res = requests.get(f"{WHO_BASE}/WHOSIS_000018?$filter=contains(IndicatorName,'{name}')&$format=json")
        if mort_res.ok:
            vals = mort_res.json().get("value", [])[:10]
            results["statistics"]["mortality_trend"] = [
                {"year": int(v.get("TimePeriod", 0)), "deaths": float(v.get("NumericValue", 0))}
                for v in vals if v.get("TimePeriod") and v.get("NumericValue")
            ]
    except Exception as e:
        results["statistics"]["mortality_trend"] = [{"year": 0, "deaths": 0, "error": str(e)}]

    # WHO DALYs
    try:
        daly_res = requests.get(f"{WHO_BASE}/DALY?$filter=contains(IndicatorName,'{name}')&$format=json")
        if daly_res.ok:
            vals = daly_res.json().get("value", [])[:10]
            results["statistics"]["dalys_trend"] = [
                {"year": int(v.get("TimePeriod", 0)), "dalys": float(v.get("NumericValue", 0))}
                for v in vals if v.get("TimePeriod") and v.get("NumericValue")
            ]
    except Exception as e:
        results["statistics"]["dalys_trend"] = [{"year": 0, "dalys": 0, "error": str(e)}]

    # WHO Regional Breakdown
    try:
        reg_res = requests.get(f"{WHO_BASE}/GHO?$filter=contains(IndicatorName,'{name}')&$format=json")
        if reg_res.ok:
            vals = reg_res.json().get("value", [])[:10]
            results["statistics"]["region_data"] = [
                {
                    "region": v.get("SpatialDim", "Unknown"),
                    "value": float(v.get("NumericValue", 0))
                }
                for v in vals if v.get("SpatialDim") and v.get("NumericValue")
            ]
    except Exception as e:
        results["statistics"]["region_data"] = [{"region": "Error", "value": 0, "error": str(e)}]

    # WHO Age & Sex Breakdown
    try:
        age_res = requests.get(f"{WHO_BASE}/GHO?$filter=contains(IndicatorName,'{name}')&$format=json")
        if age_res.ok:
            vals = age_res.json().get("value", [])[:20]
            results["statistics"]["age_sex_data"] = [
                {
                    "age_group": v.get("Dim1", "All ages"),  # WHO uses Dim1 for age group
                    "sex": v.get("Dim2", "Both sexes"),      # WHO uses Dim2 for sex
                    "value": float(v.get("NumericValue", 0))
                }
                for v in vals if v.get("NumericValue")
            ]
    except Exception as e:
        results["statistics"]["age_sex_data"] = [{"age_group": "Error", "sex": "Error", "value": 0, "error": str(e)}]

    return results
