import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSCORSMiddleware

app = FastAPI()

# Enable CORS for GitHub Pages frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WHO_BASE = "https://ghoapi.azureedge.net/api"

# WHO Region Mapping
REGION_MAP = {
    "AFR": "Africa",
    "AMR": "Americas",
    "SEARO": "South-East Asia",
    "EURO": "Europe",
    "WPRO": "Western Pacific",
    "EMRO": "Eastern Mediterranean",
    "WORLD": "Global"
}

# Starter disease map (now malaria incidence uses real WHO ID)
DISEASE_MAP = {
    "malaria": {
        "prevalence": "4670",    # Malaria incidence (per 1,000 at risk)
        "mortality": None,       # To be added
        "dalys": None            # To be added
    }
}


@app.get("/")
def root():
    return {
        "message": "✅ Backend is running! Use /api/disease?name=malaria to fetch data."
    }


@app.get("/api/disease")
def get_disease(name: str):
    """Fetch disease data from WHO, PubMed, DHARA, CTRI."""
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

    # Lookup WHO indicators for this disease
    indicator = DISEASE_MAP.get(name.lower(), {})

    # Prevalence (Malaria incidence)
    if indicator.get("prevalence"):
        try:
            prev_res = requests.get(f"{WHO_BASE}/{indicator['prevalence']}?$format=json")
            if prev_res.ok:
                vals = prev_res.json().get("value", [])[:10]
                results["statistics"]["prevalence_trend"] = [
                    {"year": int(v.get("TimeDim", 0)), "cases": float(v.get("NumericValue", 0))}
                    for v in vals if v.get("TimeDim") and v.get("NumericValue")
                ]
        except Exception as e:
            results["statistics"]["prevalence_trend"] = [{"year": 0, "cases": 0, "error": str(e)}]

    return results
