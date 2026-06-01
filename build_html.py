import json

with open("cards_data.json", "r", encoding="utf-8") as f:
    cards = json.load(f)

for card in cards:
    keys_to_remove = [k for k, v in card.items() if v is None or v == "" or v == []]
    for k in keys_to_remove:
        del card[k]

cards_json = json.dumps(cards, ensure_ascii=False)

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blox Cards Database</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0a0e17;--card:#141b2d;--card-hover:#1a2340;--border:#1e2a45;--text:#c8d6e5;--text-bright:#fff;--accent:#4fc3f7;--blue:#4a90d9;--red:#e74c3c;--green:#27ae60;--yellow:#f1c40f;--colourless:#95a5a6}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;padding:20px 30px}

.controls{display:flex;flex-wrap:wrap;gap:10px;padding:15px 0;max-width:1400px;margin:0 auto}
.controls input,.controls select{background:#1a2235;border:1px solid var(--border);color:var(--text);padding:8px 12px;border-radius:6px;font-size:0.9em;outline:none;transition:border .2s}
.controls input:focus,.controls select:focus{border-color:var(--accent)}
.controls input{flex:1;min-width:200px}
.controls select{min-width:130px}
.btn{background:var(--accent);color:#000;border:none;padding:8px 16px;border-radius:6px;cursor:pointer;font-weight:600;font-size:0.85em;transition:all .2s}
.btn:hover{background:#81d4fa;transform:translateY(-1px)}
.btn.active{background:#fff;color:#000}
.view-toggle{display:flex;gap:4px}
.view-toggle .btn{padding:6px 12px}
.color-dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}
.color-Blue{background:var(--blue)}.color-Red{background:var(--red)}.color-Green{background:var(--green)}.color-Yellow{background:var(--yellow)}.color-Colourless{background:var(--colourless)}
.rarity-tag{display:inline-block;padding:2px 8px;border-radius:4px;font-size:0.75em;font-weight:600;text-transform:uppercase}
.rarity-Common{background:#2c3e50;color:#95a5a6}.rarity-Uncommon{background:#1a3a1a;color:#27ae60}
.rarity-Rare{background:#1a2a4a;color:#4a90d9}.rarity-Epic{background:#3a1a4a;color:#9b59b6}
.rarity-Legendary{background:#4a3a1a;color:#f39c12}.rarity-Token{background:#2a2a2a;color:#7f8c8d}
.rarity-Legacy{background:#3a2a1a;color:#e67e22}
.type-tag{display:inline-block;padding:2px 6px;border-radius:3px;font-size:0.7em;font-weight:600;text-transform:uppercase;margin-left:4px;background:#1a2a3a;color:#5dade2}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:12px;padding:15px 0;max-width:1400px;margin:0 auto}
.card-grid{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:16px;cursor:pointer;transition:all .2s;position:relative;overflow:hidden}
.card-grid:hover{background:var(--card-hover);border-color:var(--accent);transform:translateY(-2px);box-shadow:0 8px 25px rgba(0,0,0,.3)}
.card-grid .card-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px}
.card-grid .card-name{color:var(--text-bright);font-weight:700;font-size:1.05em;flex:1}
.card-grid .card-stats{display:flex;gap:12px;margin-bottom:10px;font-size:0.85em}
.card-grid .stat{display:flex;align-items:center;gap:4px}
.card-grid .stat-icon{font-size:1.1em}
.card-grid .stat-val{color:var(--text-bright);font-weight:600}
.card-grid .card-effect{font-size:0.82em;color:#8b9dc3;line-height:1.5;max-height:60px;overflow:hidden;text-overflow:ellipsis}
.card-grid .card-bio{font-size:0.75em;color:#556677;font-style:italic;margin-top:8px;max-height:36px;overflow:hidden;text-overflow:ellipsis}
.card-grid .card-meta{display:flex;gap:6px;margin-top:10px;flex-wrap:wrap;align-items:center}

.table-wrap{padding:15px 0;overflow-x:auto;max-width:1400px;margin:0 auto}
table{width:100%;border-collapse:collapse;font-size:0.85em}
th{background:#0f1520;color:var(--accent);padding:10px 12px;text-align:left;cursor:pointer;white-space:nowrap;user-select:none;border-bottom:2px solid var(--accent)}
th:hover{background:#1a2235}
th .sort-arrow{margin-left:4px;font-size:0.8em;opacity:0.4}
th.sorted .sort-arrow{opacity:1}
td{padding:8px 12px;border-bottom:1px solid var(--border);vertical-align:top}
tr:hover td{background:var(--card-hover)}
.effect-cell{max-width:400px;font-size:0.8em;color:#8b9dc3;line-height:1.4}
.bio-cell{max-width:250px;font-size:0.75em;color:#556677;font-style:italic}

.modal-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.7);z-index:200;justify-content:center;align-items:center;padding:20px}
.modal-overlay.active{display:flex}
.modal{background:var(--card);border:1px solid var(--border);border-radius:16px;max-width:600px;width:100%;max-height:90vh;overflow-y:auto;padding:30px;position:relative}
.modal .close{position:absolute;top:12px;right:16px;background:none;border:none;color:var(--text);font-size:1.5em;cursor:pointer}
.modal h2{color:var(--text-bright);font-size:1.5em;margin-bottom:16px}
.modal .detail-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px}
.modal .detail-item{background:#0f1520;padding:10px 14px;border-radius:8px}
.modal .detail-label{font-size:0.75em;color:#6b7c93;text-transform:uppercase;margin-bottom:4px}
.modal .detail-value{color:var(--text-bright);font-weight:600}
.modal .effect-box{background:#0f1520;padding:14px;border-radius:8px;margin-bottom:12px;line-height:1.6;font-size:0.9em}
.modal .bio-box{color:#6b7c93;font-style:italic;font-size:0.85em;padding:10px 14px;background:#0a0e17;border-radius:8px}

.result-count{padding:5px 0;font-size:0.85em;color:#6b7c93;max-width:1400px;margin:0 auto}
.hidden{display:none!important}
</style>
</head>
<body>

<div class="controls">
<input type="text" id="search" placeholder="Search cards by name, effect, bio..." autocomplete="off">
<select id="filterColor"><option value="">All Colors</option>
<option value="Blue">Blue</option><option value="Red">Red</option>
<option value="Green">Green</option><option value="Yellow">Yellow</option>
<option value="Colourless">Colourless</option></select>
<select id="filterRarity"><option value="">All Rarities</option>
<option value="Common">Common</option><option value="Uncommon">Uncommon</option>
<option value="Rare">Rare</option><option value="Epic">Epic</option>
<option value="Legendary">Legendary</option><option value="Token">Token</option></select>
<select id="filterType"><option value="">All Types</option>
<option value="Fighter">Fighter</option><option value="Action">Action</option>
<option value="Terrain">Terrain</option><option value="Gear">Gear</option></select>
<select id="sortBy"><option value="name">Sort: Name</option>
<option value="health">Sort: Health</option><option value="power">Sort: Power</option>
<option value="cost_total">Sort: Cost</option><option value="rarity">Sort: Rarity</option>
<option value="color">Sort: Color</option></select>
<div class="view-toggle">
<button class="btn active" onclick="setView('grid')">Grid</button>
<button class="btn" onclick="setView('table')">Table</button>
</div>
</div>

<div id="resultCount" class="result-count"></div>

<div id="gridView" class="grid"></div>

<div id="tableView" class="table-wrap hidden">
<table><thead><tr>
<th onclick="sortTable('name')">Name <span class="sort-arrow">↕</span></th>
<th onclick="sortTable('color')">Color <span class="sort-arrow">↕</span></th>
<th onclick="sortTable('rarity')">Rarity <span class="sort-arrow">↕</span></th>
<th onclick="sortTable('card_type')">Type <span class="sort-arrow">↕</span></th>
<th onclick="sortTable('health')">HP <span class="sort-arrow">↕</span></th>
<th onclick="sortTable('power')">Pow <span class="sort-arrow">↕</span></th>
<th onclick="sortTable('cost_text')">Cost <span class="sort-arrow">↕</span></th>
<th>Effect</th>
<th>Bio</th>
</tr></thead><tbody id="tableBody"></tbody></table>
</div>

<div class="modal-overlay" id="modal">
<div class="modal">
<button class="close" onclick="closeModal()">×</button>
<div id="modalContent"></div>
</div>
</div>

<script>
const CARDS = ''' + cards_json + r''';

const rarityOrder = {Common:0,Uncommon:1,Rare:2,Epic:3,Legendary:4,Token:5,Legacy:6};
let currentView = 'grid';
let tableSortKey = 'name';
let tableSortDir = 1;

function getTotalCost(card) {
    if (!card.cost) return 0;
    return Object.values(card.cost).reduce((a,b) => a+b, 0);
}

function getCostDisplay(card) {
    if (card.cost_text) return card.cost_text;
    if (!card.cost) return '-';
    return Object.entries(card.cost).map(([k,v]) => v+k[0]).join(' ');
}

function filterCards() {
    const search = document.getElementById('search').value.toLowerCase();
    const color = document.getElementById('filterColor').value;
    const rarity = document.getElementById('filterRarity').value;
    const type = document.getElementById('filterType').value;

    let filtered = CARDS.filter(c => {
        if (color && c.color !== color) return false;
        if (rarity && c.rarity !== rarity) return false;
        if (type && c.card_type !== type) return false;
        if (search) {
            const hay = [c.name, c.effect, c.bio, c.rarity_text, c.cost_text].filter(Boolean).join(' ').toLowerCase();
            return hay.includes(search);
        }
        return true;
    });

    const sortVal = document.getElementById('sortBy').value;
    filtered.sort((a, b) => {
        if (sortVal === 'name') return a.name.localeCompare(b.name);
        if (sortVal === 'health') return (b.health||0) - (a.health||0);
        if (sortVal === 'power') return (b.power||0) - (a.power||0);
        if (sortVal === 'cost_total') return getTotalCost(b) - getTotalCost(a);
        if (sortVal === 'rarity') return (rarityOrder[b.rarity]||0) - (rarityOrder[a.rarity]||0);
        if (sortVal === 'color') return (a.color||'').localeCompare(b.color||'');
        return 0;
    });

    document.getElementById('resultCount').textContent = filtered.length + ' cards';
    renderGrid(filtered);
    renderTable(filtered);
}

function renderGrid(cards) {
    const g = document.getElementById('gridView');
    g.innerHTML = cards.map((c, i) => {
        const idx = CARDS.indexOf(c);
        return `<div class="card-grid" onclick="showModal(${idx})">
            <div class="card-header">
                <div class="card-name">${esc(c.name)}</div>
                <span class="rarity-tag rarity-${c.rarity||''}">${c.rarity||''}</span>
            </div>
            <div class="card-stats">
                ${c.health != null ? `<div class="stat"><span class="stat-icon">&#10084;&#65039;</span><span class="stat-val">${c.health}</span></div>` : ''}
                ${c.power != null ? `<div class="stat"><span class="stat-icon">&#9876;&#65039;</span><span class="stat-val">${c.power}</span></div>` : ''}
                <div class="stat"><span class="stat-icon">&#128176;</span><span class="stat-val">${getCostDisplay(c)}</span></div>
            </div>
            ${c.effect ? `<div class="card-effect">${esc(c.effect)}</div>` : ''}
            ${c.bio ? `<div class="card-bio">${esc(c.bio)}</div>` : ''}
            <div class="card-meta">
                <span class="color-dot color-${c.color||''}"></span><span style="font-size:0.8em">${c.color||'?'}</span>
                <span class="type-tag">${c.card_type||''}</span>
            </div>
        </div>`;
    }).join('');
}

function renderTable(cards) {
    const tb = document.getElementById('tableBody');
    tb.innerHTML = cards.map(c => {
        const idx = CARDS.indexOf(c);
        return `<tr onclick="showModal(${idx})" style="cursor:pointer">
            <td><strong>${esc(c.name)}</strong></td>
            <td><span class="color-dot color-${c.color||''}"></span>${c.color||''}</td>
            <td><span class="rarity-tag rarity-${c.rarity||''}">${c.rarity||''}</span></td>
            <td><span class="type-tag">${c.card_type||''}</span></td>
            <td>${c.health!=null?c.health:'-'}</td>
            <td>${c.power!=null?c.power:'-'}</td>
            <td>${getCostDisplay(c)}</td>
            <td class="effect-cell">${c.effect?esc(c.effect):''}</td>
            <td class="bio-cell">${c.bio?esc(c.bio):''}</td>
        </tr>`;
    }).join('');
}

function sortTable(key) {
    if (tableSortKey === key) tableSortDir *= -1;
    else { tableSortKey = key; tableSortDir = 1; }

    const filtered = getFiltered();
    filtered.sort((a, b) => {
        let va = a[key], vb = b[key];
        if (key === 'health' || key === 'power') return ((vb||0) - (va||0)) * tableSortDir;
        if (key === 'rarity') return ((rarityOrder[vb]||0) - (rarityOrder[va]||0)) * tableSortDir;
        return String(va||'').localeCompare(String(vb||'')) * tableSortDir;
    });
    renderTable(filtered);
}

function getFiltered() {
    const search = document.getElementById('search').value.toLowerCase();
    const color = document.getElementById('filterColor').value;
    const rarity = document.getElementById('filterRarity').value;
    const type = document.getElementById('filterType').value;
    return CARDS.filter(c => {
        if (color && c.color !== color) return false;
        if (rarity && c.rarity !== rarity) return false;
        if (type && c.card_type !== type) return false;
        if (search) {
            const hay = [c.name, c.effect, c.bio, c.rarity_text, c.cost_text].filter(Boolean).join(' ').toLowerCase();
            return hay.includes(search);
        }
        return true;
    });
}

function showModal(idx) {
    const c = CARDS[idx];
    let html = `<h2>${esc(c.name)}</h2><div class="detail-grid">`;
    if (c.color) html += `<div class="detail-item"><div class="detail-label">Color</div><div class="detail-value"><span class="color-dot color-${c.color}"></span>${c.color}</div></div>`;
    if (c.rarity) html += `<div class="detail-item"><div class="detail-label">Rarity</div><div class="detail-value"><span class="rarity-tag rarity-${c.rarity}">${c.rarity}</span></div></div>`;
    if (c.card_type) html += `<div class="detail-item"><div class="detail-label">Type</div><div class="detail-value"><span class="type-tag">${c.card_type}</span></div></div>`;
    if (c.cost_text) html += `<div class="detail-item"><div class="detail-label">Cost</div><div class="detail-value">${esc(c.cost_text)}</div></div>`;
    if (c.health != null) html += `<div class="detail-item"><div class="detail-label">Health</div><div class="detail-value">${c.health}</div></div>`;
    if (c.power != null) html += `<div class="detail-item"><div class="detail-label">Power</div><div class="detail-value">${c.power}</div></div>`;
    html += `</div>`;
    if (c.effect) html += `<div style="margin-bottom:12px"><div class="detail-label" style="margin-bottom:6px">Effect</div><div class="effect-box">${esc(c.effect).replace(/\|/g, '<br>')}</div></div>`;
    if (c.bio) html += `<div><div class="detail-label" style="margin-bottom:6px">Bio</div><div class="bio-box">${esc(c.bio)}</div></div>`;
    html += `<div style="margin-top:14px"><a href="https://blox-cards.fandom.com/wiki/${encodeURIComponent(c.name)}" target="_blank" style="color:var(--accent)">View on Wiki</a></div>`;
    document.getElementById('modalContent').innerHTML = html;
    document.getElementById('modal').classList.add('active');
}

function closeModal() { document.getElementById('modal').classList.remove('active'); }
document.getElementById('modal').addEventListener('click', e => { if (e.target.id === 'modal') closeModal(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

function setView(v) {
    currentView = v;
    document.getElementById('gridView').classList.toggle('hidden', v !== 'grid');
    document.getElementById('tableView').classList.toggle('hidden', v !== 'table');
    document.querySelectorAll('.view-toggle .btn').forEach(b => b.classList.toggle('active', b.textContent.trim().toLowerCase() === v));
}

function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }

let debounce;
document.getElementById('search').addEventListener('input', () => { clearTimeout(debounce); debounce = setTimeout(filterCards, 200); });
document.getElementById('filterColor').addEventListener('change', filterCards);
document.getElementById('filterRarity').addEventListener('change', filterCards);
document.getElementById('filterType').addEventListener('change', filterCards);
document.getElementById('sortBy').addEventListener('change', filterCards);

filterCards();
</script>
</body>
</html>'''

with open("blox_cards.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Done: {len(cards)} cards, {len(html)} bytes")
