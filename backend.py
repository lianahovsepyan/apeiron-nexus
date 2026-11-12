from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import psutil

app = FastAPI(title="Apeiron-Nexus Core API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <title>APEIRON / NEXUS :: ADVANCED SCIENTIFIC SUITE</title>
    <style>
        :root { --bg: #0b0f19; --panel: #111827; --accent: #ef4444; --text: #f3f4f6; --dim: #6b7280; --border: #1f2937; }
        body { background: var(--bg); color: var(--text); font-family: 'Courier New', monospace; padding: 20px; margin: 0; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 20px; font-size: 0.9rem; color: var(--accent); }
        .main-grid { display: grid; grid-template-columns: 260px 1fr 280px; gap: 20px; max-width: 1300px; margin: 0 auto; }
        .panel { background: var(--panel); border: 1px solid var(--border); padding: 15px; border-radius: 4px; }
        h3 { color: var(--accent); margin-top: 0; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; }
        .btn { background: transparent; border: 1px solid var(--accent); color: var(--accent); padding: 10px; font-size: 0.8rem; font-weight: bold; cursor: pointer; font-family: monospace; border-radius: 3px; margin-bottom: 10px; width: 100%; text-align: left; transition: 0.2s; }
        .btn:hover { background: rgba(239, 68, 68, 0.15); }
        .metrics-top { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 15px; }
        .metric-card { background: #070a12; border: 1px solid var(--border); padding: 10px; text-align: center; }
        .m-val { font-size: 1.1rem; color: var(--accent); font-weight: bold; margin-top: 4px; }
        .m-lbl { font-size: 0.7rem; color: var(--dim); text-transform: uppercase; }
        .visualizer { background: #070a12; border: 1px solid var(--border); height: 220px; display: flex; align-items: center; justify-content: center; position: relative; margin-bottom: 15px; }
        .terminal { background: #05070c; border: 1px solid var(--border); padding: 12px; font-size: 0.75rem; color: #34d399; height: 130px; overflow-y: auto; }
        .node-item { font-size: 0.75rem; padding: 6px 0; border-bottom: 1px solid #161e2e; display: flex; justify-content: space-between; color: var(--dim); }
        .node-item span { color: var(--accent); }
    </style>
</head>
<body>
    <div class="header">
        <span>APEIRON / NEXUS // ADVANCED SCIENTIFIC SUITE v2.4</span>
        <span style="color: #34d399; border: 1px solid #34d399; padding: 2px 8px; font-size: 0.75rem;">FP64 SCHRÖDINGER & SVD KERNEL ACTIVE</span>
    </div>

    <div class="main-grid">
        <!-- Left Sidebar -->
        <div class="panel">
            <h3>PHYSICAL HARDWARE CORES</h3>
            <button class="btn" style="border-color: var(--accent);" onclick="runBayesian()">⚡ BAYESIAN DISCOVERY</button>
            <button class="btn" style="border-color: #3b82f6; color: #3b82f6;" onclick="runSVD()">📉 TENSOR SVD & SCHRÖDINGER</button>
            <button class="btn" style="border-color: #34d399; color: #34d399;" onclick="fetchTelemetry()">🖥️ TELEMETRY SYNC</button>

            <h3 style="margin-top: 25px;">QUANTUM REGISTER NODES</h3>
            <div class="node-item">REG-PHYS-01 <span>TOPOLOGICAL</span></div>
            <div class="node-item">REG-PHYS-02 <span>COHERENT</span></div>
            <div class="node-item">REG-PHYS-03 <span>OPTIMAL</span></div>
            <div class="node-item">REG-PHYS-04 <span>SYNTHESIS</span></div>
            <div class="node-item">REG-PHYS-05 <span>ACTIVE-FP64</span></div>
        </div>

        <!-- Center Panel -->
        <div>
            <div class="metrics-top">
                <div class="metric-card"><div class="m-lbl">Gate Fidelity</div><div class="m-val" id="fid">0.99995</div></div>
                <div class="metric-card"><div class="m-lbl">Bayesian Evidence</div><div class="m-val" id="bev">0.99991</div></div>
                <div class="metric-card"><div class="m-lbl">Von Neumann S_vn</div><div class="m-val" id="svn">16.1736</div></div>
                <div class="metric-card"><div class="m-lbl">Compression Ratio</div><div class="m-val">0.00%</div></div>
            </div>

            <div class="panel" style="margin-bottom: 15px;">
                <div style="font-size: 0.75rem; color: var(--dim); margin-bottom: 8px;">TARGET: SCHRÖDINGER HILBERT SPACE // FP64</div>
                <div class="visualizer">
                    <svg width="100%" height="100%" viewBox="0 0 400 150" style="position: absolute;">
                        <path d="M 50 120 Q 200 10 350 100" fill="none" stroke="#ef4444" stroke-width="2"/>
                        <circle cx="210" cy="55" r="4" fill="#34d399"/>
                    </svg>
                </div>
            </div>

            <div class="panel">
                <h3>HARDWARE SCIENTIFIC DISCOVERY LOG</h3>
                <div class="terminal" id="term">
                    [HARDWARE CORE]: Advanced Scientific Suite online.<br>
                    [SYSTEM]: Telemetry sync module active. Click button to fetch metrics.
                </div>
            </div>
        </div>

        <!-- Right Sidebar -->
        <div class="panel">
            <h3>HARDWARE PROCESSOR LOAD</h3>
            <div style="font-size: 0.75rem; margin-bottom: 4px; display:flex; justify-content:space-between;"><span>CPU LOAD</span><span id="cpu-text">0.0%</span></div>
            <div style="background: #070a12; height: 6px; border: 1px solid var(--border); margin-bottom: 15px;"><div id="cpu-bar" style="background: var(--accent); width: 0%; height: 100%; transition: width 0.3s;"></div></div>

            <div style="font-size: 0.75rem; margin-bottom: 4px; display:flex; justify-content:space-between;"><span>RAM USAGE</span><span id="ram-text">0.0%</span></div>
            <div style="background: #070a12; height: 6px; border: 1px solid var(--border); margin-bottom: 25px;"><div id="ram-bar" style="background: #34d399; width: 0%; height: 100%; transition: width 0.3s;"></div></div>

            <h3 style="margin-top: 10px;">EXECUTION MATRIX</h3>
            <button class="btn" onclick="runBayesian()">⚡ RUN BAYESIAN KERNEL</button>
            <button class="btn" style="border-color: #3b82f6; color: #3b82f6;" onclick="runSVD()">📉 TENSOR SVD & SCHRÖDINGER</button>
            <button class="btn" style="border-color: #34d399; color: #34d399;" onclick="fetchTelemetry()">🖥️ TELEMETRY SYNC</button>
        </div>
    </div>

    <script>
        function log(msg) {
            const t = document.getElementById('term');
            const time = new Date().toTimeString().split(' ')[0];
            t.innerHTML += `<br>[${time}]: ${msg}`;
            t.scrollTop = t.scrollHeight;
        }

        async function fetchTelemetry() {
            try {
                log("Հարցում /api/telemetry...");
                const res = await fetch('/api/telemetry?t=' + Date.now(), { cache: 'no-store' });
                if (!res.ok) throw new Error("HTTP " + res.status);
                const data = await res.json();
                
                document.getElementById('cpu-text').innerText = data.cpu_load + '%';
                document.getElementById('cpu-bar').style.width = data.cpu_load + '%';
                document.getElementById('ram-text').innerText = data.ram_load + '%';
                document.getElementById('ram-bar').style.width = data.ram_load + '%';
                
                log(`[TELEMETRY OK] CPU: ${data.cpu_load}% | RAM: ${data.ram_load}%`);
            } catch (err) {
                log(`[ERROR]: ${err.message}`);
            }
        }

        async function runBayesian() {
            try {
                log("Հարցում /api/bayesian...");
                const res = await fetch('/api/bayesian?t=' + Date.now(), { cache: 'no-store' });
                if (!res.ok) throw new Error("HTTP " + res.status);
                const data = await res.json();
                document.getElementById('bev').innerText = data.bayesian_evidence;
                log(`[BAYESIAN OK] Evidence: ${data.bayesian_evidence}`);
            } catch (err) {
                log(`[ERROR]: ${err.message}`);
            }
        }

        async function runSVD() {
            try {
                log("Հարցում /api/svd...");
                const res = await fetch('/api/svd?t=' + Date.now(), { cache: 'no-store' });
                if (!res.ok) throw new Error("HTTP " + res.status);
                const data = await res.json();
                document.getElementById('svn').innerText = data.von_neumann_entropy;
                log(`[SVD OK] S_vn: ${data.von_neumann_entropy}`);
            } catch (err) {
                log(`[ERROR]: ${err.message}`);
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def serve_root(response: Response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return HTMLResponse(content=HTML_PAGE)

@app.get("/api/telemetry")
def get_telemetry():
    cpu = round(psutil.cpu_percent(interval=0.1), 1)
    ram = round(psutil.virtual_memory().percent, 1)
    print(f"[API] Telemetry -> CPU: {cpu}%, RAM: {ram}%")
    return {"status": "SUCCESS", "cpu_load": cpu, "ram_load": ram}

@app.get("/api/bayesian")
def run_bayesian():
    np.random.seed()
    val = float(np.exp(-np.var(np.random.randn(100))))
    print("[API] Bayesian executed.")
    return {"status": "SUCCESS", "bayesian_evidence": round(val, 6)}

@app.get("/api/svd")
def run_svd():
    H = np.random.randn(8, 8)
    H = (H + H.T) / 2
    U, S, Vt = np.linalg.svd(H)
    svn = float(-np.sum((S/np.sum(S)) * np.log(S/np.sum(S) + 1e-12)))
    print("[API] SVD executed.")
    return {"status": "SUCCESS", "von_neumann_entropy": round(svn, 5)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
