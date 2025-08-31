# Dr Kembhavi’s Disease/Vyadhi Data Tool  

**Developed by Astanga Wellness Pvt Ltd, Hubli, Karnataka, India**  
*Integrating Ayurveda & Modern Science for Complete Health Insights*  

---

## 🌍 Overview  
This is a **web-based disease information dashboard** that integrates data from multiple global and Ayurvedic sources.  
It allows users to **search for a disease**, and instantly see:  

- ✅ Overview (from Wikipedia & other sources)  
- ✅ Ayurveda Research (DHARA database)  
- ✅ Clinical Trials (CTRI registry)  
- ✅ PubMed Research (top scientific publications)  
- ✅ WHO Statistics (prevalence, mortality, DALYs)  
- ✅ Regional Breakdown & Age/Sex Distribution  
- ✅ Interactive Charts (via Chart.js)  
- ✅ Export as PDF Report  
- ✅ Disclaimer section  

Frontend is deployed via **GitHub Pages**, Backend via **FastAPI on Render**.  

---

## 🔧 Tech Stack  
- **Frontend**: HTML, CSS, JavaScript, Chart.js  
- **Backend**: Python, FastAPI, Uvicorn, Requests, BeautifulSoup4  
- **Deployment**:  
  - Backend → Render (Free Tier)  
  - Frontend → GitHub Pages  

---

## 🚀 Live Demo  
🔗 **Frontend (GitHub Pages)**: [https://your-username.github.io/disease-tool-frontend/](https://your-username.github.io/disease-tool-frontend/)  
🔗 **Backend (Render API)**: [https://your-service.onrender.com/api/disease?name=malaria](https://your-service.onrender.com/api/disease?name=malaria)  

---

## 📖 Usage  
1. Open the [Frontend Page](https://your-username.github.io/disease-tool-frontend/).  
2. Enter a **disease name** (e.g. `malaria`, `diabetes`, `covid-19`).  
3. The tool will fetch data from:  
   - Wikipedia (Overview)  
   - PubMed (Scientific Articles)  
   - DHARA (Ayurveda Research Links)  
   - CTRI (Clinical Trial Registry of India)  
   - WHO GHO API (Global Health Data)  
4. View charts, research links, and download as PDF.  

---

## ⚠️ Disclaimer  
This tool is designed for **educational and research purposes only**.  
It is **not intended as medical advice**.  
Always consult a qualified healthcare professional before making health-related decisions.  

---

## 🛠️ Development Setup (For Contributors)  

### Backend (FastAPI)  
Clone the backend repo and run locally:  
```bash
git clone https://github.com/your-username/disease-tool-backend.git
cd disease-tool-backend
pip install -r requirements.txt
uvicorn api:app --reload
