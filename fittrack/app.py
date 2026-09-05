import os, json, datetime
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static')
DATA_FILE='data.json'

def load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f: return json.load(f)
    return {}

def save(d):
    with open(DATA_FILE,'w') as f: json.dump(d,f,indent=2)

@app.get('/')
def home(): return send_from_directory('static','index.html')

@app.get('/api/data')
def get_data(): return jsonify(load())

@app.post('/api/data')
def post_data():
    payload=request.get_json(force=True)
    d=load(); day=payload.get('date') or datetime.date.today().isoformat()
    d[day]=payload
    save(d); return jsonify(payload)

@app.post('/api/summary')
def summary():
    payload=request.get_json(force=True)
    key=os.getenv('OPENAI_API_KEY')
    if not key:
        return jsonify({'error':'OPENAI_API_KEY is not configured on the server.'}), 503
    try:
        from openai import OpenAI
        client=OpenAI(api_key=key)
        prompt=f"""You are a concise personal fitness coach. Analyze this day's workout and food log. Give: 1) training summary, 2) nutrition summary with protein/calorie caveats, 3) wins, 4) gaps, 5) one practical recommendation for tomorrow. Never present estimated nutrition as exact. Data:\n{json.dumps(payload, indent=2)}"""
        r=client.responses.create(model=os.getenv('OPENAI_MODEL','gpt-5.6-luna'), input=prompt)
        return jsonify({'summary':r.output_text})
    except Exception as e:
        return jsonify({'error':str(e)}),500

if __name__=='__main__':
    app.run(host='127.0.0.1', port=int(os.getenv('PORT','5000')), debug=True)
