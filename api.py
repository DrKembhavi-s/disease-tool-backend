from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is running! Use /api/disease?name=malaria"}

@app.get("/api/disease")
def get_disease(name: str):
    return {
        "overview": f"{name.capitalize()} is a sample disease overview from backend.",
        "pubmed": [
            "https://pubmed.ncbi.nlm.nih.gov/123456/",
            "https://pubmed.ncbi.nlm.nih.gov/789012/"
        ],
        "ayurveda_research": [
            "https://dharaonline.org/sample1",
            "https://dharaonline.org/sample2"
        ],
        "clinical_trials": [
            "https://ctri.nic.in/sample1",
            "https://ctri.nic.in/sample2"
        ],
        "statistics": {
            "prevalence_trend": [
                {"year": 2018, "cases": 100000},
                {"year": 2019, "cases": 120000},
                {"year": 2020, "cases": 90000},
                {"year": 2021, "cases": 110000}
            ],
            "mortality_trend": [
                {"year": 2018, "deaths": 2000},
                {"year": 2019, "deaths": 2500},
                {"year": 2020, "deaths": 1800},
                {"year": 2021, "deaths": 2100}
            ],
            "dalys_trend": [
                {"year": 2018, "dalys": 50000},
                {"year": 2019, "dalys": 52000},
                {"year": 2020, "dalys": 48000},
                {"year": 2021, "dalys": 53000}
            ]
        }
    }
