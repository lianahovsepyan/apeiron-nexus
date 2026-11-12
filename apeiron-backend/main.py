from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import os
from monte_carlo_qec import MonteCarloQECBenchmark

app = FastAPI(title="Apeiron v53.1 Verified QEC Backend")

@app.get("/", response_class=HTMLResponse)
def read_root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Apeiron v53.1 Backend is running. index.html not found.</h3>"

@app.get("/api/run-qec")
def run_quantum_simulation(gamma: float = Query(0.35, ge=0.01, le=0.99), trials: int = Query(500, ge=10, le=2000)):
    mc = MonteCarloQECBenchmark(num_trials=trials)
    report = mc.run_simulation(gamma=gamma)
    return report

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
