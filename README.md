# Vigion.ai – AI Movie Maker | Neurosys Hackathon

**Vigion.ai** is an AI-powered movie creator designed for the Neurosys hackathon. It generates multi-scene videos from a simple prompt, leveraging Google's APIs and the Veo engine, all integrated using Python.

---

## 🚀 Quick Start

1. **Clone the Repo**
git clone (https://github.com/PrematureDroneOperator/Huxlers)
cd neurosys-hackathon-vigion-ai

2. **Install Dependencies**
Go to the `backend` folder and run:
pip install -r requirements.txt
pip install -r r2.txt


3. **Add API Credentials**
- Place your `service-account.json` (from Google Cloud Platform) and API keys in the required locations in:
  - `handleVideoGen.py`
  - `handleImageGen.py`
  - `handlePrompt.py`

4. **Run the Backend (ASGI App)**
- In the `backend` directory, start the server:
  ```
  uvicorn app:app --reload
  ```

---

## 🧠 How It Works

- Enter a simple text prompt.
- Vigion.ai generates a multi-scene video using advanced AI and Google APIs.
- Uses FastAPI for a fast, flexible backend.
- Includes modules for image generation, prompt processing, and video assembly.

---

## 📁 Repo Structure

- `backend/`: FastAPI app and core AI engine

---

## Support & Contact

- Email: [abdulhammaad@gmail.com](mailto:abdulhammaad@gmail.com)
- Phone: +91-70190-35321

---

*Hackathon Submission – Neurosys 2025*  
*AI Movie Generation. Powered by Google and Veo.*  
