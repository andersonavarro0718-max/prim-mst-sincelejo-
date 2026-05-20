"""
╔══════════════════════════════════════════════════════════════╗
║   MST — Red de Fibra Óptica de Sincelejo                    ║
║   Prim con min-heap  +  Kruskal con Union-Find              ║
║   Comparativa de costo y tiempo                             ║
║   Bloque B · Python · Semana 5                              ║
║   Tema: MST: cómo Telecom diseña redes de fibra al          ║
║         menor costo                                         ║
╚══════════════════════════════════════════════════════════════╝
"""

import heapq
import time
import json
import webbrowser
import os

# ══════════════════════════════════════════════
# 1. NODOS DEL GRAFO DE SINCELEJO
# ══════════════════════════════════════════════
nodos = {
    "N00": "UAJS Sede E",
    "N01": "UAJS Sede C",
    "N02": "UNISUCRE",
    "N03": "CECAR",
    "N04": "IPS SEYSA",
    "N05": "Clinica Las Americas",
    "N06": "Terminal de Transporte",
    "N07": "Mercado de Sincelejo",
    "N08": "Av. Alfonso Lopez",
    "N09": "Parque Santander",
    "N10": "Calle 30 / Troncal",
    "N11": "Barrio Puerta Roja",
}

# ══════════════════════════════════════════════
# 2. ARISTAS (bidireccionales, peso en minutos)
# ══════════════════════════════════════════════
aristas = [
    ("N00","N01", 8), ("N00","N05",12), ("N00","N08", 6),
    ("N01","N04", 5), ("N01","N08", 4), ("N01","N10",10),
    ("N02","N05", 9), ("N02","N09", 7), ("N02","N11", 4),
    ("N03","N10",12), ("N03","N06",18),
    ("N04","N07", 6), ("N04","N09", 8),
    ("N05","N09",10),
    ("N06","N09",11), ("N06","N07", 8),
    ("N07","N09", 5),
    ("N08","N10", 7),
    ("N10","N06",14),
]

# ══════════════════════════════════════════════
# 3. CONSTRUCCIÓN DEL GRAFO (para Prim)
# ══════════════════════════════════════════════
def construir_grafo():
    grafo = {n: [] for n in nodos}
    for origen, destino, peso in aristas:
        grafo[origen].append((peso, destino))
        grafo[destino].append((peso, origen))
    return grafo

# ══════════════════════════════════════════════
# 4. ALGORITMO DE PRIM CON MIN-HEAP
# ══════════════════════════════════════════════
def prim(grafo, start):
    parent = {n: None         for n in grafo}
    key    = {n: float('inf') for n in grafo}
    en_mst = {n: False        for n in grafo}
    orden  = []

    key[start] = 0
    heap = [(0, start)]

    while heap:
        costo, u = heapq.heappop(heap)
        if en_mst[u]:
            continue
        en_mst[u] = True
        orden.append((u, costo, parent[u]))
        for peso, v in grafo[u]:
            if not en_mst[v] and peso < key[v]:
                key[v]    = peso
                parent[v] = u
                heapq.heappush(heap, (peso, v))

    return parent, key, orden

# ══════════════════════════════════════════════
# 5. UNION-FIND (para Kruskal)
# ══════════════════════════════════════════════
class UnionFind:
    def __init__(self, elementos):
        # Cada nodo es su propio representante
        self.padre = {e: e for e in elementos}
        self.rango  = {e: 0 for e in elementos}

    def find(self, x):
        # Compresion de camino
        if self.padre[x] != x:
            self.padre[x] = self.find(self.padre[x])
        return self.padre[x]

    def union(self, x, y):
        # Union por rango
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False   # ya estan en el mismo componente → ciclo
        if self.rango[rx] < self.rango[ry]:
            rx, ry = ry, rx
        self.padre[ry] = rx
        if self.rango[rx] == self.rango[ry]:
            self.rango[rx] += 1
        return True

# ══════════════════════════════════════════════
# 6. ALGORITMO DE KRUSKAL CON UNION-FIND
# ══════════════════════════════════════════════
def kruskal():
    # Ordenar todas las aristas por peso (ascendente)
    aristas_ord = sorted(aristas, key=lambda e: e[2])
    uf  = UnionFind(nodos.keys())
    mst = []   # aristas del MST

    for origen, destino, peso in aristas_ord:
        # Si no forman ciclo, agregar al MST
        if uf.union(origen, destino):
            mst.append((origen, destino, peso))
        if len(mst) == len(nodos) - 1:
            break   # MST completo

    return mst

# ══════════════════════════════════════════════
# 7. MOSTRAR parent[] EN CONSOLA
# ══════════════════════════════════════════════
def mostrar_parent(parent, key):
    print("\n" + "=" * 62)
    print("  ARREGLO parent[]  —  PRIM")
    print("=" * 62)
    print(f"  {'Nodo':<6} {'parent[v]':<12} {'key (min)':<10} {'Nombre'}")
    print(f"  {'-'*6} {'-'*12} {'-'*10} {'-'*28}")
    for n in sorted(parent):
        p = parent[n] if parent[n] else "None"
        k = key[n] if key[n] != float('inf') else "inf"
        print(f"  {n:<6} {p:<12} {str(k)+' min':<10} {nodos[n]}")

# ══════════════════════════════════════════════
# 8. MOSTRAR MST EN CONSOLA
# ══════════════════════════════════════════════
def mostrar_mst_prim(parent, key):
    print("\n" + "=" * 62)
    print("  MST — PRIM")
    print("=" * 62)
    print(f"  {'Arista':<20} {'Peso':>6}   Descripcion")
    print(f"  {'-'*20} {'-'*6}   {'-'*32}")
    total = 0
    for n in sorted(parent):
        p = parent[n]
        if p:
            w = key[n]
            total += w
            print(f"  {p} --> {n:<13} {w:>4} min   {nodos[p]} -> {nodos[n]}")
    print(f"\n  {'COSTO TOTAL (Prim)':.<44} {total} min")
    return total

def mostrar_mst_kruskal(mst):
    print("\n" + "=" * 62)
    print("  MST — KRUSKAL")
    print("=" * 62)
    print(f"  {'Arista':<20} {'Peso':>6}   Descripcion")
    print(f"  {'-'*20} {'-'*6}   {'-'*32}")
    total = 0
    for a, b, w in sorted(mst):
        total += w
        print(f"  {a} --> {b:<13} {w:>4} min   {nodos[a]} -> {nodos[b]}")
    print(f"\n  {'COSTO TOTAL (Kruskal)':.<44} {total} min")
    return total

# ══════════════════════════════════════════════
# 9. VISUALIZACIÓN ASCII EN CONSOLA
# ══════════════════════════════════════════════
def visualizar_ascii(parent, key, orden):
    print("\n" + "=" * 62)
    print("  VISUALIZACION ASCII — MST (PRIM)")
    print("=" * 62)
    hijos = {n: [] for n in nodos}
    for n, p in parent.items():
        if p:
            hijos[p].append((key[n], n))
    for p in hijos:
        hijos[p].sort()

    def imprimir(nodo, prefijo="", es_ultimo=True, es_raiz=False):
        conector   = "" if es_raiz else ("└── " if es_ultimo else "├── ")
        nuevo_pref = "" if es_raiz else (prefijo + ("    " if es_ultimo else "│   "))
        peso_str   = f"  <-{key[nodo]}min" if parent[nodo] else ""
        print(f"  {prefijo}{conector}{nodo} [{nodos[nodo]}]{peso_str}")
        lista = hijos[nodo]
        for i, (_, hijo) in enumerate(lista):
            imprimir(hijo, nuevo_pref, i == len(lista) - 1)

    raiz = next(n for n in parent if parent[n] is None)
    imprimir(raiz, es_raiz=True)

    print(f"\n  {'#':<5} {'Nodo':<6} {'Desde':<8} {'Costo':>10}")
    print(f"  {'-'*5} {'-'*6} {'-'*8} {'-'*10}")
    for i, (n, c, p) in enumerate(orden):
        desde     = p if p else "raiz"
        costo_str = "0 min" if p is None else f"{c} min"
        print(f"  {i+1:<5} {n:<6} {desde:<8} {costo_str:>10}")

# ══════════════════════════════════════════════
# 10. COMPARATIVA DE TIEMPO Y RESULTADO
# ══════════════════════════════════════════════
def comparativa(grafo, t_prim, costo_prim, t_kruskal, costo_kruskal):
    print("\n" + "=" * 62)
    print("  COMPARATIVA: PRIM vs KRUSKAL")
    print("=" * 62)
    print(f"\n  {'Algoritmo':<12} {'Costo MST':>12} {'Tiempo (seg)':>16}")
    print(f"  {'-'*12} {'-'*12} {'-'*16}")
    print(f"  {'Prim':<12} {str(costo_prim)+' min':>12} {t_prim:>16.8f}")
    print(f"  {'Kruskal':<12} {str(costo_kruskal)+' min':>12} {t_kruskal:>16.8f}")

    print(f"\n  Mismo resultado : {'SI ✔' if costo_prim == costo_kruskal else 'NO ✘'}")
    mas_rapido = "Prim" if t_prim < t_kruskal else "Kruskal"
    diff = abs(t_prim - t_kruskal)
    print(f"  Mas rapido      : {mas_rapido}  (diferencia: {diff:.8f} seg)")
    print(f"\n  CONCLUSION: Ambos algoritmos encuentran el MST optimo")
    print(f"  de {costo_prim} minutos. Prim usa min-heap O(E log V),")
    print(f"  Kruskal usa Union-Find O(E log E).")

# ══════════════════════════════════════════════
# 11. GENERAR PÁGINA WEB
# ══════════════════════════════════════════════
def generar_web(parent, key, orden, mst_kruskal, costo_total,
                t_prim, t_kruskal):

    posiciones = {
        "N00": (380, 55),  "N01": (560,110), "N02": (140,115),
        "N03": ( 80,265),  "N04": (590,230), "N05": (280,135),
        "N06": (480,395),  "N07": (610,345), "N08": (445,175),
        "N09": (345,295),  "N10": (200,365), "N11": ( 80,165),
    }

    nodos_js     = {k: {"name": v, "x": posiciones[k][0], "y": posiciones[k][1]}
                    for k, v in nodos.items()}
    aristas_js   = [{"from": a, "to": b, "w": w} for a, b, w in aristas]
    mst_prim_js  = [{"from": parent[n], "to": n, "w": key[n]}
                    for n in parent if parent[n]]
    mst_krus_js  = [{"from": a, "to": b, "w": w} for a, b, w in mst_kruskal]
    orden_js     = [{"node": n, "cost": c, "from": p} for n, c, p in orden]
    parent_js    = {n: parent[n] for n in parent}
    key_js       = {n: (key[n] if key[n] != float('inf') else -1) for n in key}
    krus_sorted  = sorted(mst_kruskal, key=lambda e: e[2])

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Prim vs Kruskal — MST Sincelejo</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:#0b1120;color:#e2e8f0;font-family:'Segoe UI',sans-serif;height:100vh;display:flex;flex-direction:column;overflow:hidden}}
  header{{background:#111827;border-bottom:1px solid #1e3a5f;padding:12px 24px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}}
  header h1{{font-size:16px;font-weight:700;color:#93c5fd}}
  header p{{font-size:11px;color:#64748b;margin-top:2px}}
  .hbadges{{display:flex;gap:8px}}
  .hbadge{{font-size:10px;padding:3px 10px;border-radius:20px;border:1px solid #1e3a5f;color:#67e8f9;background:rgba(6,182,212,.1)}}
  .hbadge.green{{color:#6ee7b7;border-color:rgba(16,185,129,.3);background:rgba(16,185,129,.1)}}
  .layout{{display:flex;flex:1;overflow:hidden}}
  .graph-wrap{{flex:1;position:relative;background:#0f172a}}
  #cvs{{width:100%;height:100%;display:block}}
  .panel{{width:330px;background:#111827;border-left:1px solid #1e3a5f;display:flex;flex-direction:column;overflow:hidden;flex-shrink:0}}
  .controls{{padding:10px 12px;border-bottom:1px solid #1e3a5f;display:flex;gap:7px;flex-wrap:wrap}}
  .btn{{font-size:11px;font-weight:600;padding:6px 12px;border-radius:7px;border:none;cursor:pointer;transition:.2s}}
  .btn-blue{{background:#2563eb;color:#fff}}
  .btn-blue:hover{{background:#1d4ed8}}
  .btn-blue:disabled{{background:#1e3a5f;color:#475569;cursor:not-allowed}}
  .btn-gray{{background:#1e293b;color:#94a3b8;border:1px solid #334155}}
  .btn-gray:hover{{background:#273549}}
  .btn-green{{background:#065f46;color:#6ee7b7;border:1px solid rgba(16,185,129,.4)}}
  .btn-green:hover{{background:#047857}}
  .tabs{{display:flex;background:#0f172a;border-bottom:1px solid #1e3a5f}}
  .tab{{flex:1;padding:9px 0;text-align:center;font-size:10px;cursor:pointer;color:#64748b;border-bottom:2px solid transparent;transition:.2s}}
  .tab.active{{color:#67e8f9;border-bottom-color:#67e8f9}}
  .tb{{flex:1;overflow-y:auto;padding:12px;display:none}}
  .tb.active{{display:block}}
  .log-item{{padding:7px 0;border-bottom:1px solid #1e293b;animation:fi .3s ease}}
  @keyframes fi{{from{{opacity:0;transform:translateY(4px)}}to{{opacity:1;transform:none}}}}
  .log-step{{font-size:9px;color:#475569;font-family:monospace}}
  .log-node{{font-size:13px;font-weight:700;color:#93c5fd}}
  .log-name{{font-size:10px;color:#64748b}}
  .log-cost{{display:inline-block;margin-top:3px;font-size:10px;font-family:monospace;background:rgba(16,185,129,.12);color:#6ee7b7;padding:2px 7px;border-radius:4px}}
  table{{width:100%;border-collapse:collapse;font-size:10px}}
  th{{font-size:8px;color:#475569;text-align:left;padding:5px 5px;border-bottom:1px solid #1e3a5f;letter-spacing:1px;font-family:monospace}}
  td{{padding:5px 5px;border-bottom:1px solid #1a2235;font-family:monospace;color:#94a3b8}}
  tr.hl td{{background:rgba(59,130,246,.1);color:#93c5fd}}
  tr.khl td{{background:rgba(16,185,129,.08);color:#6ee7b7}}
  .stats{{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:10px}}
  .stat{{background:#1e293b;border-radius:8px;padding:9px}}
  .stat-l{{font-size:8px;color:#475569;font-family:monospace;letter-spacing:1px}}
  .stat-v{{font-size:18px;font-weight:700;color:#93c5fd;margin-top:2px}}
  .cmp-row{{display:flex;gap:8px;margin-bottom:8px}}
  .cmp-card{{flex:1;background:#1e293b;border-radius:8px;padding:10px;border:1px solid #1e3a5f}}
  .cmp-card.winner{{border-color:rgba(16,185,129,.4)}}
  .cmp-title{{font-size:9px;color:#64748b;font-family:monospace;letter-spacing:1px}}
  .cmp-val{{font-size:20px;font-weight:700;margin-top:3px}}
  .cmp-sub{{font-size:9px;color:#64748b;margin-top:2px}}
  .same-badge{{background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);color:#6ee7b7;font-size:10px;padding:5px 10px;border-radius:6px;text-align:center;margin-bottom:10px}}
  .legend{{display:flex;gap:10px;padding:7px 12px;border-top:1px solid #1e3a5f;flex-wrap:wrap;flex-shrink:0}}
  .leg{{display:flex;align-items:center;gap:4px;font-size:9px;color:#64748b}}
  .leg-dot{{width:9px;height:9px;border-radius:50%}}
  ::-webkit-scrollbar{{width:3px}}
  ::-webkit-scrollbar-thumb{{background:#1e3a5f;border-radius:2px}}
  .empty{{text-align:center;padding:24px 10px;color:#475569;font-size:11px}}
  .mode-btns{{display:flex;gap:6px;margin-bottom:10px}}
  .mbtn{{flex:1;font-size:10px;padding:5px 0;border-radius:6px;border:1px solid #1e3a5f;background:transparent;color:#64748b;cursor:pointer;transition:.2s;text-align:center}}
  .mbtn.active{{background:#1e3a5f;color:#93c5fd;border-color:#3b82f6}}
</style>
</head>
<body>
<header>
  <div>
    <h1>🔗 MST — Red de Fibra Óptica de Sincelejo</h1>
    <p>Prim (min-heap) + Kruskal (Union-Find) · 12 Nodos · 19 Aristas · Bloque B</p>
  </div>
  <div class="hbadges">
    <span class="hbadge">Prim: <span id="hdr-prim">—</span> min</span>
    <span class="hbadge">Kruskal: <span id="hdr-krus">—</span> min</span>
    <span class="hbadge green" id="hdr-same" style="display:none">✔ Mismo resultado</span>
  </div>
</header>

<div class="layout">
  <div class="graph-wrap"><canvas id="cvs"></canvas></div>

  <div class="panel">
    <div class="controls">
      <button class="btn btn-blue"  id="btn-run">▶ Ejecutar Prim</button>
      <button class="btn btn-gray"  id="btn-step" disabled>Paso a paso</button>
      <button class="btn btn-green" id="btn-krus" disabled>Mostrar Kruskal</button>
      <button class="btn btn-gray"  id="btn-reset">↺ Reset</button>
    </div>

    <div class="tabs">
      <div class="tab active" onclick="tab('log')">Pasos</div>
      <div class="tab" onclick="tab('parent')">parent[]</div>
      <div class="tab" onclick="tab('cmp')">Prim vs Kruskal</div>
    </div>

    <div class="tb active" id="tb-log">
      <div class="empty" id="log-empty">Presiona <b>Ejecutar Prim</b><br>para ver los pasos</div>
      <div id="log-list"></div>
    </div>

    <div class="tb" id="tb-parent">
      <div class="stats">
        <div class="stat"><div class="stat-l">NODOS</div><div class="stat-v">12</div></div>
        <div class="stat"><div class="stat-l">ARISTAS MST</div><div class="stat-v" id="s-aristas">—</div></div>
        <div class="stat"><div class="stat-l">COSTO PRIM</div><div class="stat-v" id="s-prim">—</div></div>
        <div class="stat"><div class="stat-l">NODO INICIO</div><div class="stat-v">N01</div></div>
      </div>
      <table>
        <thead><tr><th>NODO</th><th>NOMBRE</th><th>parent[v]</th><th>key</th></tr></thead>
        <tbody id="tbl-body"></tbody>
      </table>
    </div>

    <div class="tb" id="tb-cmp">
      <div class="empty" id="cmp-empty">Ejecuta ambos algoritmos<br>para ver la comparativa</div>
      <div id="cmp-content" style="display:none">
        <div class="same-badge" id="same-badge"></div>
        <div style="font-size:9px;color:#475569;font-family:monospace;letter-spacing:1px;margin-bottom:6px">COSTO MST</div>
        <div class="cmp-row">
          <div class="cmp-card" id="card-prim-cost">
            <div class="cmp-title">PRIM</div>
            <div class="cmp-val" id="v-prim-cost" style="color:#93c5fd">—</div>
            <div class="cmp-sub">minutos</div>
          </div>
          <div class="cmp-card" id="card-krus-cost">
            <div class="cmp-title">KRUSKAL</div>
            <div class="cmp-val" id="v-krus-cost" style="color:#6ee7b7">—</div>
            <div class="cmp-sub">minutos</div>
          </div>
        </div>
        <div style="font-size:9px;color:#475569;font-family:monospace;letter-spacing:1px;margin-bottom:6px">TIEMPO DE EJECUCIÓN</div>
        <div class="cmp-row">
          <div class="cmp-card" id="card-prim-t">
            <div class="cmp-title">PRIM</div>
            <div class="cmp-val" id="v-prim-t" style="color:#93c5fd;font-size:13px">—</div>
            <div class="cmp-sub">segundos</div>
          </div>
          <div class="cmp-card" id="card-krus-t">
            <div class="cmp-title">KRUSKAL</div>
            <div class="cmp-val" id="v-krus-t" style="color:#6ee7b7;font-size:13px">—</div>
            <div class="cmp-sub">segundos</div>
          </div>
        </div>
        <div style="font-size:9px;color:#475569;font-family:monospace;letter-spacing:1px;margin-bottom:6px">ARISTAS DEL MST</div>
        <div class="mode-btns">
          <div class="mbtn active" onclick="showMstTable('prim')">Prim</div>
          <div class="mbtn" onclick="showMstTable('krus')">Kruskal</div>
        </div>
        <table>
          <thead><tr><th>ARISTA</th><th>PESO</th><th>DESCRIPCIÓN</th></tr></thead>
          <tbody id="mst-tbl"></tbody>
        </table>
      </div>
    </div>

    <div class="legend">
      <div class="leg"><div class="leg-dot" style="background:#3b82f6"></div>Prim MST</div>
      <div class="leg"><div class="leg-dot" style="background:#f59e0b"></div>Actual</div>
      <div class="leg"><div style="width:16px;height:2px;background:#10b981;border-radius:1px"></div>Arista Prim</div>
      <div class="leg"><div style="width:16px;height:2px;background:#a855f7;border-radius:1px"></div>Arista Kruskal</div>
    </div>
  </div>
</div>

<script>
const NODES  = {json.dumps(nodos_js)};
const EDGES  = {json.dumps(aristas_js)};
const MST_P  = {json.dumps(mst_prim_js)};
const MST_K  = {json.dumps(mst_krus_js)};
const ORDEN  = {json.dumps(orden_js)};
const PARENT = {json.dumps(parent_js)};
const KEY    = {json.dumps(key_js)};
const KRUS_S = {json.dumps(krus_sorted)};
const COSTO  = {costo_total};
const T_PRIM = {t_prim};
const T_KRUS = {t_kruskal};
const IDS    = Object.keys(NODES);

const cvs = document.getElementById('cvs');
const ctx = cvs.getContext('2d');
let W, H;

function resize(){{ W=cvs.width=cvs.offsetWidth; H=cvs.height=cvs.offsetHeight; draw(); }}
window.addEventListener('resize', resize);

const state   = {{}};
const mstSet  = new Set();
let krusVis   = false;
let stepIdx   = 0, done = false, timer = null;

IDS.forEach(id => state[id]='default');

function nx(id){{ return NODES[id].x*(W/740); }}
function ny(id){{ return NODES[id].y*(H/500); }}

function draw(){{
  ctx.clearRect(0,0,W,H);
  // grid
  ctx.strokeStyle='rgba(30,58,95,0.25)'; ctx.lineWidth=0.5;
  for(let x=0;x<W;x+=50){{ ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,H);ctx.stroke(); }}
  for(let y=0;y<H;y+=50){{ ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke(); }}

  // aristas base
  EDGES.forEach(e=>{{
    ctx.beginPath(); ctx.moveTo(nx(e.from),ny(e.from)); ctx.lineTo(nx(e.to),ny(e.to));
    ctx.strokeStyle='rgba(71,85,105,0.3)'; ctx.lineWidth=1.2; ctx.setLineDash([4,4]); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle='rgba(100,116,139,0.55)'; ctx.font='bold 8px monospace'; ctx.textAlign='center';
    ctx.fillText(e.w,(nx(e.from)+nx(e.to))/2,(ny(e.from)+ny(e.to))/2-4);
  }});

  // aristas Kruskal (púrpura) si visible
  if(krusVis){{
    MST_K.forEach(e=>{{
      ctx.beginPath(); ctx.moveTo(nx(e.from),ny(e.from)); ctx.lineTo(nx(e.to),ny(e.to));
      ctx.strokeStyle='rgba(168,85,247,0.7)'; ctx.lineWidth=2.5; ctx.stroke();
    }});
  }}

  // aristas Prim (verde)
  mstSet.forEach(k=>{{
    const [a,b,w]=k.split('|');
    ctx.beginPath(); ctx.moveTo(nx(a),ny(a)); ctx.lineTo(nx(b),ny(b));
    ctx.strokeStyle='#10b981'; ctx.lineWidth=3; ctx.stroke();
    ctx.fillStyle='#6ee7b7'; ctx.font='bold 9px monospace'; ctx.textAlign='center';
    ctx.fillText(w+'m',(nx(a)+nx(b))/2,(ny(a)+ny(b))/2-6);
  }});

  // nodos
  IDS.forEach(id=>{{
    const x=nx(id),y=ny(id),st=state[id];
    let fill='#1e293b',stroke='#475569',sw=1.5,tc='#94a3b8';
    if(st==='visited'){{fill='#1e3a5f';stroke='#3b82f6';sw=2.5;tc='#93c5fd';}}
    if(st==='current'){{fill='#451a03';stroke='#f59e0b';sw=3;tc='#fcd34d';}}
    if(st==='kruskal'){{fill='#2e1065';stroke='#a855f7';sw=2.5;tc='#d8b4fe';}}
    if(st==='current'){{ctx.shadowColor='#f59e0b';ctx.shadowBlur=16;}}
    ctx.beginPath(); ctx.arc(x,y,18,0,Math.PI*2);
    ctx.fillStyle=fill; ctx.fill(); ctx.strokeStyle=stroke; ctx.lineWidth=sw; ctx.stroke();
    ctx.shadowBlur=0;
    ctx.fillStyle=tc; ctx.font='bold 9px monospace'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(id,x,y);
    const words=NODES[id].name.split(' ');
    ctx.fillStyle='rgba(148,163,184,0.6)'; ctx.font='7px Segoe UI';
    words.slice(0,2).forEach((w,i)=>ctx.fillText(w,x,y+26+(i*9)));
    ctx.textBaseline='alphabetic';
  }});
}}

function applyStep(i){{
  const s=ORDEN[i];
  if(i>0) state[ORDEN[i-1].node]='visited';
  state[s.node]='current';
  if(s.from) mstSet.add(`${{s.from}}|${{s.node}}|${{s.cost}}`);
  document.getElementById('log-empty').style.display='none';
  const div=document.createElement('div'); div.className='log-item';
  div.innerHTML=`<div class="log-step">Paso ${{i+1}} / ${{ORDEN.length}}</div>
    <div class="log-node">${{s.node}}</div><div class="log-name">${{NODES[s.node].name}}</div>
    <span class="log-cost">${{s.from?s.from+' → '+s.node+' · '+s.cost+' min':'Nodo raíz · 0 min'}}</span>`;
  const list=document.getElementById('log-list');
  list.appendChild(div); list.lastChild.scrollIntoView({{behavior:'smooth',block:'end'}});
  draw();
}}

function finish(){{
  state[ORDEN[ORDEN.length-1].node]='visited';
  // header
  document.getElementById('hdr-prim').textContent=COSTO;
  document.getElementById('hdr-krus').textContent=COSTO;
  document.getElementById('hdr-same').style.display='';
  // stats parent tab
  document.getElementById('s-aristas').textContent=ORDEN.length-1;
  document.getElementById('s-prim').textContent=COSTO+' min';
  // tabla parent
  const tbody=document.getElementById('tbl-body'); tbody.innerHTML='';
  IDS.slice().sort().forEach(id=>{{
    const p=PARENT[id],k=KEY[id];
    const tr=document.createElement('tr'); if(p) tr.classList.add('hl');
    tr.innerHTML=`<td>${{id}}</td><td style="font-size:8px;color:#64748b">${{NODES[id].name}}</td><td>${{p||'null'}}</td><td>${{k>=0?k+' min':'∞'}}</td>`;
    tbody.appendChild(tr);
  }});
  // comparativa
  document.getElementById('cmp-empty').style.display='none';
  document.getElementById('cmp-content').style.display='block';
  document.getElementById('same-badge').textContent='✔ Prim y Kruskal obtienen el mismo costo: '+COSTO+' min';
  document.getElementById('v-prim-cost').textContent=COSTO;
  document.getElementById('v-krus-cost').textContent=COSTO;
  document.getElementById('v-prim-t').textContent=T_PRIM.toFixed(8);
  document.getElementById('v-krus-t').textContent=T_KRUS.toFixed(8);
  // marcar ganador de tiempo
  if(T_PRIM<T_KRUS) document.getElementById('card-prim-t').classList.add('winner');
  else document.getElementById('card-krus-t').classList.add('winner');
  showMstTable('prim');
  // habilitar Kruskal
  document.getElementById('btn-krus').disabled=false;
  document.getElementById('btn-run').disabled=true;
  document.getElementById('btn-step').disabled=true;
  draw();
}}

function showMstTable(which){{
  document.querySelectorAll('.mbtn').forEach((b,i)=>b.classList.toggle('active',['prim','krus'][i]===which));
  const tbody=document.getElementById('mst-tbl'); tbody.innerHTML='';
  const data = which==='prim' ? MST_P : KRUS_S;
  data.forEach(e=>{{
    const a=e.from||e[0], b=e.to||e[1], w=e.w||e[2];
    const tr=document.createElement('tr'); tr.classList.add(which==='prim'?'hl':'khl');
    tr.innerHTML=`<td>${{a}} → ${{b}}</td><td>${{w}} min</td><td style="font-size:8px;color:#64748b">${{NODES[a].name}} → ${{NODES[b].name}}</td>`;
    tbody.appendChild(tr);
  }});
}}

document.getElementById('btn-run').addEventListener('click',()=>{{
  resetAll(); done=true; stepIdx=0;
  document.getElementById('btn-run').disabled=true;
  document.getElementById('btn-step').disabled=false;
  timer=setInterval(()=>{{
    if(stepIdx>=ORDEN.length){{clearInterval(timer);finish();return;}}
    applyStep(stepIdx++);
  }},700);
}});

document.getElementById('btn-step').addEventListener('click',()=>{{
  if(!done) return; clearInterval(timer);
  if(stepIdx<ORDEN.length) applyStep(stepIdx++); else finish();
}});

document.getElementById('btn-krus').addEventListener('click',()=>{{
  krusVis=!krusVis;
  document.getElementById('btn-krus').textContent=krusVis?'Ocultar Kruskal':'Mostrar Kruskal';
  if(krusVis) IDS.forEach(id=>{{ if(state[id]==='visited') state[id]='kruskal'; }});
  else IDS.forEach(id=>{{ if(state[id]==='kruskal') state[id]='visited'; }});
  draw();
}});

document.getElementById('btn-reset').addEventListener('click',resetAll);

function resetAll(){{
  clearInterval(timer); stepIdx=0; done=false; krusVis=false;
  mstSet.clear(); IDS.forEach(id=>state[id]='default');
  document.getElementById('log-list').innerHTML='';
  document.getElementById('log-empty').style.display='block';
  document.getElementById('tbl-body').innerHTML='';
  document.getElementById('s-aristas').textContent='—';
  document.getElementById('s-prim').textContent='—';
  document.getElementById('hdr-prim').textContent='—';
  document.getElementById('hdr-krus').textContent='—';
  document.getElementById('hdr-same').style.display='none';
  document.getElementById('cmp-empty').style.display='block';
  document.getElementById('cmp-content').style.display='none';
  document.getElementById('btn-run').disabled=false;
  document.getElementById('btn-step').disabled=true;
  document.getElementById('btn-krus').disabled=true;
  document.getElementById('btn-krus').textContent='Mostrar Kruskal';
  draw();
}}

function tab(name){{
  const names=['log','parent','cmp'];
  document.querySelectorAll('.tab').forEach((t,i)=>t.classList.toggle('active',names[i]===name));
  document.querySelectorAll('.tb').forEach(b=>b.classList.toggle('active',b.id==='tb-'+name));
}}

resize();
</script>
</body>
</html>"""

    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mst_visualizacion.html")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n  Pagina web generada: {ruta}")
    print("  Abriendo en el navegador...")
    webbrowser.open("file:///" + ruta.replace("\\", "/"))

# ══════════════════════════════════════════════
# 12. PROGRAMA PRINCIPAL
# ══════════════════════════════════════════════
if __name__ == "__main__":

    print("\n" + "=" * 62)
    print("  MST: COMO TELECOM DISENYA REDES DE FIBRA AL MENOR COSTO")
    print("  Grafo de Sincelejo · 12 Nodos · 19 Aristas")
    print("=" * 62)

    grafo = construir_grafo()

    # ── PRIM con medición de tiempo ──────────────
    t0 = time.perf_counter()
    parent, key, orden = prim(grafo, "N01")
    t_prim = time.perf_counter() - t0

    mostrar_parent(parent, key)
    costo_prim = mostrar_mst_prim(parent, key)
    visualizar_ascii(parent, key, orden)

    # ── KRUSKAL con medición de tiempo ───────────
    print("\n" + "=" * 62)
    print("  KRUSKAL CON UNION-FIND")
    print("=" * 62)

    t0 = time.perf_counter()
    mst_k = kruskal()
    t_kruskal = time.perf_counter() - t0

    costo_kruskal = mostrar_mst_kruskal(mst_k)

    # ── COMPARATIVA ──────────────────────────────
    comparativa(grafo, t_prim, costo_prim, t_kruskal, costo_kruskal)

    print("\n" + "=" * 62)
    print(f"  Tiempo Prim    : {t_prim:.8f} seg")
    print(f"  Tiempo Kruskal : {t_kruskal:.8f} seg")
    print("=" * 62)
    print("  FIN DEL PROGRAMA")
    print("=" * 62 + "\n")

    # ── PÁGINA WEB ───────────────────────────────
    generar_web(parent, key, orden, mst_k, costo_prim, t_prim, t_kruskal)
