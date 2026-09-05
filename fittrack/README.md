# FitTrack

A mobile-friendly daily fitness + nutrition journal.

## Run locally

```bash
cd fittrack
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
python app.py
```

Then open http://127.0.0.1:5000

The app stores daily logs in `data.json` and keeps the OpenAI key server-side.
