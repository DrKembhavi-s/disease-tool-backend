import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSCORSMiddleware

app = FastAPI()

# Enable CORS so frontend (GitHub Pages) can call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Backend is running! Use /api/disease?name=malaria"}

@app.get("/api/disease")
def get_disease(name: str):
    results = {
        "overview": f"{name.capitalize()} data dashboard",
        "pubmed": [
            f"https://pubmed.ncbi.nlm.nih.gov/?term={name}"
        ],
        "ayurveda_research": [
            f"https://dharaonline.org/Search.aspx?query={name}"
        ],
        "clinical_trials": [
            f"https://ctri.nic.in/Clinicaltrials/advsearch.php?trial={name}"
        ],
        "statistics": {
            "prevalence_trend": [],
            "mortality_trend": [],
            "dalys_trend": []
        }
    }

    # WHO API base
    WHO_BASE = "https://ghoapi.azureedge.net/api"

    # Prevalence data
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

    # Mortality data
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

    # DALYs data
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

    return results
