import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# Mapping disease keywords to WHO indicator codes
DISEASE_MAP = {
    "anemia": {
        "prevalence": "WHS9_90",   # Anaemia prevalence in women (15–49 years)
        "mortality": None,
        "dalys": None
    },
    "malaria": {
        "prevalence": "MALARIA1",          # Reported malaria cases
        "mortality": "MALARIA_DEATHS",     # Malaria deaths
        "dalys": "DALY_MALARIA"            # DALYs due to malaria
    },
    "diabetes": {
        "prevalence": "NCD_DIABETES_PREV", # Diabetes prevalence (age 18+)
        "mortality": "NCD_DIABETES_MORT",  # Diabetes deaths
        "dalys": "DALY_DIABETES"           # DALYs due to diabetes
    },
    "tuberculosis": {
        "prevalence": "TB_cases",          # TB incidence
        "mortality": "TB_mortality",       # TB mortality
        "dalys": "DALY_TUBERCULOSIS"       # DALYs due to TB
    },
    "hiv": {
        "prevalence": "HIV_prevalence",    # HIV prevalence
        "mortality": "HIV_mortality",      # HIV deaths
        "dalys": "DALY_HIV"                # DALYs due to HIV/AIDS
    },
    "hypertension": {
        "prevalence": "NCD_HYPERTENSION",  # Hypertension prevalence (adults)
        "mortality": "NCD_HYPERT_MORT",    # Hypertension-related deaths
        "dalys": "DALY_HYPERTENSION"       # DALYs due to hypertension
    },
    "cancer": {
        "prevalence": "CANCER_INCIDENCE",  # Cancer incidence
        "mortality": "CANCER_MORTALITY",   # Cancer mortality
        "dalys": "DALY_CANCER"             # DALYs due to cancer
    }
}


@app.get("/")
def root():
    """Root endpoint for quick check."""
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

    # Check if disease is mapped
    indicator = DISEASE_MAP.get(name.lower(), {})

    # Prevalence
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

    # Mortality
    if indicator.get("mortality"):
        try:
            mort_res = requests.get(f"{WHO_BASE}/{indicator['mortality']}?$format=json")
            if mort_res.ok:
                vals = mort_res.json().get("value", [])[:10]
                results["statistics"]["mortality_trend"] = [
                    {"year": int(v.get("TimeDim", 0)), "deaths": float(v.get("NumericValue", 0))}
                    for v in vals if v.get("TimeDim") and v.get("NumericValue")
                ]
        except Exception as e:
            results["statistics"]["mortality_trend"] = [{"year": 0, "deaths": 0, "error": str(e)}]

    # DALYs
    if indicator.get("dalys"):
        try:
            daly_res = requests.get(f"{WHO_BASE}/{indicator['dalys']}?$format=json")
            if daly_res.ok:
                vals = daly_res.json().get("value", [])[:10]
                results["statistics"]["dalys_trend"] = [
                    {"year": int(v.get("TimeDim", 0)), "dalys": float(v.get("NumericValue", 0))}
                    for v in vals if v.get("TimeDim") and v.get("NumericValue")
                ]
        except Exception as e:
            results["statistics"]["dalys_trend"] = [{"year": 0, "dalys": 0, "error": str(e)}]

    # WHO Regional Breakdown (generic attempt)
    try:
        reg_res = requests.get(f"{WHO_BASE}/GHO?$filter=contains(IndicatorName,'{name}')&$format=json")
        if reg_res.ok:
            vals = reg_res.json().get("value", [])[:20]
            results["statistics"]["region_data"] = [
                {
                    "region": REGION_MAP.get(v.get("SpatialDim", "Unknown"), v.get("SpatialDim")),
                    "value": float(v.get("NumericValue", 0))
                }
                for v in vals if v.get("SpatialDim") and v.get("NumericValue")
            ]
    except Exception as e:
        results["statistics"]["region_data"] = [{"region": "Error", "value": 0, "error": str(e)}]

    # WHO Age & Sex Breakdown (generic attempt)
    try:
        age_res = requests.get(f"{WHO_BASE}/GHO?$filter=contains(IndicatorName,'{name}')&$format=json")
        if age_res.ok:
            vals = age_res.json().get("value", [])[:30]
            results["statistics"]["age_sex_data"] = [
                {
                    "age_group": v.get("Dim1", "All ages"),   # WHO: Dim1 = Age group
                    "sex": v.get("Dim2", "Both sexes"),       # WHO: Dim2 = Sex
                    "value": float(v.get("NumericValue", 0))
                }
                for v in vals if v.get("NumericValue")
            ]
    except Exception as e:
        results["statistics"]["age_sex_data"] = [
            {"age_group": "Error", "sex": "Error", "value": 0, "error": str(e)}
        ]

    return results
