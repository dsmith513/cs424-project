"""Build the static and interactive Assignment 3 passenger-load views."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
OUTPUT = ROOT / "visualizations"

PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{color-scheme:light;--ink:#183247;--muted:#5b7180;--line:#d9e3e8;--paper:#f4f7f8;--card:#fff;--blue:#86b7c8;--blue-dark:#276b89;--orange:#c7672e;--gray:#9daab2}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.55 "Segoe UI",Arial,sans-serif}header{background:#e6f0f3;padding:28px max(22px,calc((100vw - 1440px)/2));border-bottom:1px solid var(--line)}header .eyebrow{margin:0 0 6px;color:var(--blue-dark);font-size:12px;text-transform:uppercase;letter-spacing:.12em;font-weight:700}h1{margin:0;font-size:clamp(26px,3vw,38px);line-height:1.2}header p{max-width:900px;margin:10px 0 0;color:var(--muted)}main{max-width:1440px;margin:24px auto;padding:0 22px 40px}.intro,.card,.controls{background:var(--card);border:1px solid var(--line);border-radius:12px;box-shadow:0 2px 8px #1832470a}.intro{padding:18px 22px;margin-bottom:18px}.intro p{margin:0}.intro p+p{margin-top:8px}.controls{padding:15px 18px;margin-bottom:18px;display:flex;align-items:end;gap:14px;flex-wrap:wrap}.controls label{display:flex;flex-direction:column;gap:5px;font-size:13px;font-weight:650}.controls select{min-width:145px;padding:9px 11px;border:1px solid #aebfc8;border-radius:7px;background:white;color:var(--ink);font:inherit}.controls select:focus-visible,input:focus-visible{outline:3px solid #76adc3;outline-offset:2px}.controls .hint{flex:1 1 340px;color:var(--muted);font-size:13px;max-width:660px}.check{display:flex!important;flex-direction:row!important;align-items:center;gap:8px!important;padding:9px 0}.check input{width:18px;height:18px;accent-color:var(--blue-dark)}.card{padding:18px 18px 14px;margin-bottom:18px;min-width:0}.card h2{margin:0;font-size:19px}.caption{margin:3px 0 12px;color:var(--muted);font-size:13px}.chart-wrap{width:100%;overflow-x:auto}svg{display:block;width:100%;height:auto;min-width:740px}svg text{font-family:"Segoe UI",Arial,sans-serif;fill:var(--ink)}.gridline{stroke:#e8eef1;stroke-width:1}.axis{stroke:#8297a4;stroke-width:1}.muted{fill:var(--muted)}.trip-line{fill:none;stroke:#8f9ca5;stroke-opacity:.42;stroke-width:1.6}.selected-line{fill:none;stroke:var(--orange);stroke-width:3.4}.median-line{fill:none;stroke:#19394d;stroke-width:3}.reference-line{fill:none;stroke:#7e8c94;stroke-width:2;stroke-dasharray:7 5}.iqr-band{fill:#8fbccd;fill-opacity:.34;stroke:none}.trip-dot{fill:#8f9ca5;fill-opacity:.6}.selected-dot{fill:var(--orange);stroke:white;stroke-width:1.5}.median-dot{fill:#19394d}.peak-ring{fill:none;stroke:var(--orange);stroke-width:2.5}.legend{display:flex;flex-wrap:wrap;gap:12px 22px;align-items:center;color:var(--muted);font-size:13px;margin:7px 4px 2px}.legend span{display:inline-flex;align-items:center;gap:7px}.swatch{width:23px;height:0;border-top:3px solid #19394d}.swatch.band{height:12px;border:0;background:#8fbccd80}.swatch.selected{border-color:var(--orange)}.swatch.reference{border-top:2px dashed #7e8c94}.swatch.individual{border-top:2px solid #8f9ca5}.callout{margin-top:10px;background:#f4f8f9;border-left:3px solid var(--blue-dark);padding:10px 13px;color:var(--muted);font-size:13px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}.grid .card{margin:0}.table-wrap{overflow:auto;margin-top:14px}table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);white-space:nowrap}th{background:#f3f7f8;color:#385365;position:sticky;top:0}tbody tr:hover{background:#f7fafb}.foot{font-size:12px;color:var(--muted);margin:16px 2px 0}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
@media(max-width:820px){main{padding:0 12px 28px;margin-top:14px}.grid{grid-template-columns:1fr}.controls{align-items:stretch}.controls label{flex:1 1 145px}.controls select{width:100%}header{padding:22px 16px}.card{padding:14px 12px}}
@media print{body{background:white}header{padding:16px 0}.intro,.card,.controls{box-shadow:none;break-inside:avoid}.card{padding:10px}.grid{gap:8px}main{max-width:none;padding:0}.table-wrap{overflow:visible}table{font-size:10px}svg{min-width:0}}
</style>
</head>
<body>
<header><p class="eyebrow">Assignment 3 · Task 1</p><h1>__HEADING__</h1><p>Passenger counts in one observed train car on the Cary–Chicago OTC segment. Counts are recorded at stops and terminal checkpoints; lines guide the eye along route order.</p></header>
<main>
<section class="intro"><p>__INTRO__</p><p>All views use the same processed passenger-stop records. Skipped stops have no row; a recorded zero means nobody boarded or exited at that observed stop. These data describe the sampled trips, not the full train.</p></section>
__BODY__
<p class="foot">Comparisons are descriptive. Each train is paired with a fixed set of weekdays and a fixed departure time, so a difference cannot be attributed to weekday or express status alone.</p>
</main>
<script>
const trips=__TRIPS__;
const stopRows=__STOPS__;
const days=["Monday","Tuesday","Wednesday","Thursday","Friday"];
const colors={Inbound:"#276b89",Outbound:"#a65436"};
function svgNode(tag,attrs={},value=null){const e=document.createElementNS("http://www.w3.org/2000/svg",tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);if(value!==null)e.textContent=value;return e}
function line(svg,x1,y1,x2,y2,cls="axis"){svg.appendChild(svgNode("line",{x1,y1,x2,y2,class:cls}))}
function label(svg,x,y,value,attrs={}){svg.appendChild(svgNode("text",{x,y,...attrs},value))}
function quantile(values,p){const a=[...values].sort((x,y)=>x-y),pos=(a.length-1)*p,lo=Math.floor(pos),hi=Math.ceil(pos);return a[lo]+(a[hi]-a[lo])*(pos-lo)}
function median(values){return quantile(values,.5)}
function rowsForTrip(t){return stopRows.filter(r=>r.observation_id===t.observation_id).sort((a,b)=>+a.stop_order- +b.stop_order)}
function panelTrips(direction,train){return trips.filter(t=>t.direction===direction&&t.train_number===train).sort((a,b)=>a.date.localeCompare(b.date))}
function summaryFor(t){return `${t.date} · ${t.day_of_week} · Train ${t.train_number}`}
function drawProfile(svg,profiles,{width=570,height=395,maxY=100,showTrips=true,selectedId=null,reference=null,title="",subtitle="",compact=false,tooltips=false}={}){
  svg.replaceChildren();svg.setAttribute("viewBox",`0 0 ${width} ${height}`);
  const L=compact?48:70,R=18,T=compact?35:36,B=compact?112:154;
  const base=profiles.find(p=>p.trip)||profiles[0];if(!base)return;
  const stations=base.rows.map(r=>r.stop_name),n=stations.length,plotW=width-L-R,plotH=height-T-B;
  const x=i=>L+(n<=1?plotW/2:i*plotW/(n-1)),y=v=>T+plotH-(+v)*plotH/maxY;
  const tick=Math.max(10,Math.ceil(maxY/5/10)*10);
  for(let v=0;v<=maxY;v+=tick){line(svg,L,y(v),width-R,y(v),"gridline");label(svg,L-8,y(v)+4,String(v),{"text-anchor":"end","font-size":11,class:"muted"})}
  line(svg,L,T,L,T+plotH);line(svg,L,T+plotH,width-R,T+plotH);
  label(svg,L,T-14,title,{"font-size":compact?14:16,"font-weight":700});
  if(subtitle)label(svg,L,T+4,subtitle,{"font-size":10,class:"muted"});
  stations.forEach((s,i)=>label(svg,x(i),T+plotH+14,s,{"font-size":compact?9:10,class:"muted","text-anchor":"end",transform:`rotate(-48 ${x(i)} ${T+plotH+14})`}));
  function valuesAt(index,source){return source.map(p=>+p.rows[index]?.passengers_after_stop).filter(Number.isFinite)}
  if(reference&&reference.length){const refMed=stations.map((_,i)=>median(valuesAt(i,reference)));const pts=refMed.map((v,i)=>`${x(i)},${y(v)}`).join(" ");svg.appendChild(svgNode("polyline",{points:pts,class:"reference-line"}))}
  const q1=stations.map((_,i)=>quantile(valuesAt(i,profiles),.25)),q3=stations.map((_,i)=>quantile(valuesAt(i,profiles),.75));
  const band=q3.map((v,i)=>`${x(i)},${y(v)}`).concat(q1.map((v,j)=>`${x(q1.length-1-j)},${y(q1[q1.length-1-j])}`)).join(" ");svg.appendChild(svgNode("polygon",{points:band,class:"iqr-band"}));
  if(showTrips)profiles.forEach(p=>{if(p.trip.observation_id===selectedId)return;const pts=p.rows.map((r,i)=>`${x(i)},${y(r.passengers_after_stop)}`).join(" ");const path=svgNode("polyline",{points:pts,class:"trip-line"});if(tooltips)path.appendChild(svgNode("title",{},summaryFor(p.trip)));svg.appendChild(path);p.rows.forEach((r,i)=>{const c=svgNode("circle",{cx:x(i),cy:y(r.passengers_after_stop),r:2.2,class:"trip-dot"});if(tooltips)c.appendChild(svgNode("title",{},`${summaryFor(p.trip)} · ${r.stop_name}: ${r.passengers_after_stop} passengers`));svg.appendChild(c)})});
  const med=stations.map((_,i)=>median(valuesAt(i,profiles))),medPts=med.map((v,i)=>`${x(i)},${y(v)}`).join(" ");svg.appendChild(svgNode("polyline",{points:medPts,class:"median-line"}));med.forEach((v,i)=>svg.appendChild(svgNode("circle",{cx:x(i),cy:y(v),r:2.8,class:"median-dot"})));
  const chosen=profiles.find(p=>p.trip.observation_id===selectedId);
  if(chosen){const pts=chosen.rows.map((r,i)=>`${x(i)},${y(r.passengers_after_stop)}`).join(" ");svg.appendChild(svgNode("polyline",{points:pts,class:"selected-line"}));chosen.rows.forEach((r,i)=>{const c=svgNode("circle",{cx:x(i),cy:y(r.passengers_after_stop),r:4,class:"selected-dot"});if(tooltips)c.appendChild(svgNode("title",{},`${summaryFor(chosen.trip)} · ${r.stop_name}: ${r.passengers_after_stop} passengers`));svg.appendChild(c)});const peak=chosen.rows.reduce((best,r)=>+r.passengers_after_stop>+best.passengers_after_stop?r:best,chosen.rows[0]),i=chosen.rows.indexOf(peak);svg.appendChild(svgNode("circle",{cx:x(i),cy:y(peak.passengers_after_stop),r:7,class:"peak-ring"}));if(!compact)label(svg,Math.max(L+4,Math.min(width-R-4,x(i))),Math.max(T+18,y(peak.passengers_after_stop)-12),`Peak ${peak.passengers_after_stop} · ${peak.stop_name}`,{"font-size":12,"font-weight":700,fill:"#a34f23","text-anchor":i>n-3?"end":"start"})}
}

function setupStatic(){
  const groups=[...new Map(trips.map(t=>[`${t.direction}|${t.train_number}`,{direction:t.direction,train:t.train_number,service:t.service_type}])).values()].sort((a,b)=>a.direction.localeCompare(b.direction)||a.train.localeCompare(b.train));
  const maxY=Math.ceil(Math.max(...stopRows.map(r=>+r.passengers_after_stop))/10)*10;
  const grid=document.getElementById("static-grid");
  groups.forEach(g=>{const ts=panelTrips(g.direction,g.train),profiles=ts.map(trip=>({trip,rows:rowsForTrip(trip)}));const card=document.createElement("article");card.className="card";const h=document.createElement("h2");h.textContent=`${g.direction} · Train ${g.train} (${g.service})`;card.appendChild(h);const p=document.createElement("p");p.className="caption";p.textContent=`${profiles.length} trips · all dates shown · same passenger-count scale in every panel`;card.appendChild(p);const wrap=document.createElement("div");wrap.className="chart-wrap";const svg=svgNode("svg",{role:"img","aria-label":`${g.direction} train ${g.train} passenger profiles, interquartile range, and median`});wrap.appendChild(svg);card.appendChild(wrap);drawProfile(svg,profiles,{width:680,height:420,maxY,showTrips:true,compact:true,title:"Passengers after each observed stop"});grid.appendChild(card)});
  const tbody=document.querySelector("#peak-table tbody");[...trips].sort((a,b)=>a.date.localeCompare(b.date)||a.direction.localeCompare(b.direction)).forEach(t=>{const tr=document.createElement("tr");[t.date,t.day_of_week,t.direction,`${t.train_number} (${t.service_type})`,t.peak_passengers,t.peak_at_stop].forEach(v=>{const td=document.createElement("td");td.textContent=v;tr.appendChild(td)});tbody.appendChild(tr)});
}

function setupInteractive(){
  const direction=document.getElementById("direction"),train=document.getElementById("train"),weekday=document.getElementById("weekday"),date=document.getElementById("date"),show=document.getElementById("show-trips"),svg=document.getElementById("interactive-chart");
  const profiles=trips.map(trip=>({trip,rows:rowsForTrip(trip)}));
  const unique=(xs)=>[...new Set(xs)];
  function fillTrains(preferred){const ts=unique(trips.filter(t=>t.direction===direction.value).map(t=>t.train_number)).sort();train.replaceChildren(...ts.map(v=>new Option(`${v} · ${trips.find(t=>t.train_number===v&&t.direction===direction.value).service_type}`,v)));train.value=ts.includes(preferred)?preferred:ts[0]}
  function matchedTrips(){return trips.filter(t=>t.direction===direction.value&&t.train_number===train.value&&(weekday.value==="All weekdays"||t.day_of_week===weekday.value)).sort((a,b)=>a.date.localeCompare(b.date))}
  function fillDates(preferred){const ts=matchedTrips();date.replaceChildren(...ts.map(t=>new Option(`${t.date} · ${t.day_of_week}`,t.observation_id)));date.value=ts.some(t=>t.observation_id===preferred)?preferred:(ts[0]?.observation_id||"")}
  function render(){const subset=matchedTrips(),base=panelTrips(direction.value,train.value),selected=profiles.find(p=>p.trip.observation_id===date.value),selectedId=selected?.trip.observation_id||null;const filtered=subset.map(t=>profiles.find(p=>p.trip.observation_id===t.observation_id)).filter(Boolean),context=base.map(t=>profiles.find(p=>p.trip.observation_id===t.observation_id)).filter(Boolean);const maxY=Math.ceil(Math.max(...stopRows.map(r=>+r.passengers_after_stop))/10)*10;const reference=weekday.value==="All weekdays"?null:context;drawProfile(svg,filtered,{width:1180,height:590,maxY,showTrips:show.checked,selectedId,reference,title:`${direction.value} · Train ${train.value} · ${weekday.value}`,subtitle:`${filtered.length} sampled trip${filtered.length===1?"":"s"} in this profile`,tooltips:true});
    const t=selected?.trip,peak=t?`${t.peak_passengers} passengers at ${t.peak_at_stop}`:"No trip selected";document.getElementById("summary").textContent=`${filtered.length} of ${context.length} trips · ${t?summaryFor(t):"No trip selected"} · selected-trip peak: ${peak}.`;
    document.getElementById("weekday-note").textContent=weekday.value==="All weekdays"?"The band summarizes all sampled trips on this train in this direction.":`The blue band and dark median use ${filtered.length} ${weekday.value} trip${filtered.length===1?"":"s"}; the dashed line is the all-weekday median for this train. Small samples and paired schedules limit weekday interpretation.`;
  }
  direction.addEventListener("change",()=>{fillTrains();fillDates();render()});train.addEventListener("change",()=>{fillDates();render()});weekday.addEventListener("change",()=>{fillDates();render()});date.addEventListener("change",render);show.addEventListener("change",render);
  direction.value="Inbound";fillTrains("640");weekday.value="All weekdays";fillDates("2026-09-21_inbound_640");render();
}
if(document.body.dataset.mode==="static")setupStatic();else setupInteractive();
</script>
</body>
</html>'''

STATIC_BODY = r'''<section class="card"><h2>Static overview: every direction and train</h2><p class="caption">Four service panels show every observed trip, with a median profile and interquartile band. Gray lines are individual trips. The shared vertical scale supports comparison across panels.</p><div id="static-grid" class="grid" aria-label="Small multiples of passenger load by direction and train"></div><div class="legend"><span><i class="swatch individual"></i>Individual trip</span><span><i class="swatch band"></i>Interquartile range (25th–75th percentile)</span><span><i class="swatch"></i>Median</span></div></section>
<section class="card"><h2>Peak load by trip</h2><p class="caption">The table makes the date and peak location of each static trip profile available without filtering.</p><div class="table-wrap"><table id="peak-table"><thead><tr><th>Date</th><th>Weekday</th><th>Direction</th><th>Train / service</th><th>Peak passengers</th><th>Peak stop</th></tr></thead><tbody></tbody></table></div></section>'''

INTERACTIVE_BODY = r'''<section class="controls" aria-label="Filter passenger-load profiles"><label for="direction">Direction<select id="direction"><option>Inbound</option><option>Outbound</option></select></label><label for="train">Train<select id="train"></select></label><label for="weekday">Weekday subset<select id="weekday"><option>All weekdays</option><option>Monday</option><option>Tuesday</option><option>Wednesday</option><option>Thursday</option><option>Friday</option></select></label><label for="date">Highlight trip<select id="date"></select></label><label class="check" for="show-trips"><input id="show-trips" type="checkbox">Show other individual trips</label><p class="hint">Filter the service profile to a weekday subset, then highlight a trip to compare its route and peak with the observed distribution.</p></section>
<section class="card"><h2>Passenger load along the observed segment</h2><p id="summary" class="caption" aria-live="polite"></p><p id="weekday-note" class="caption"></p><div class="chart-wrap"><svg id="interactive-chart" viewBox="0 0 1180 590" role="img" aria-label="Passenger load at observed stops, with median, interquartile range, and selected trip"></svg></div><div class="legend"><span><i class="swatch band"></i>Interquartile range for filtered trips</span><span><i class="swatch"></i>Median for filtered trips</span><span><i class="swatch selected"></i>Highlighted trip</span><span><i class="swatch reference"></i>All-weekday median reference</span><span><i class="swatch individual"></i>Other trip profiles</span></div><div class="callout">A selected trip is emphasized in orange and its highest observed passenger count is marked. With a weekday selected, the dashed line keeps the full train profile visible for context. Weekday is paired with train and departure time in this sample, so the comparison does not isolate a weekday effect.</div></section>'''


def main() -> None:
    with (DATA / "passenger-stops.csv").open(newline="", encoding="utf-8") as handle:
        stops = list(csv.DictReader(handle))
    with (DATA / "trip-summary.csv").open(newline="", encoding="utf-8") as handle:
        trips = list(csv.DictReader(handle))
    OUTPUT.mkdir(parents=True, exist_ok=True)
    data = {"__TRIPS__": json.dumps(trips, ensure_ascii=False), "__STOPS__": json.dumps(stops, ensure_ascii=False)}
    pages = [
        ("assignment3-static.html", "Static passenger-load overview", "Static alternative · all services at once", "Static overview", "A non-interactive set of small multiples shows every observed trip and distribution across the four direction/train groups. The trip table reports each date's peak count and stop. This exposes the full overview at once, so users can compare service profiles and peak locations without operating filters.", STATIC_BODY, "static"),
        ("assignment3-interactive.html", "Interactive passenger-load explorer", "Interactive view · filter and highlight", "Interactive passenger-load explorer", "This view selects the passenger-load line visualization from Assignment 2. Direction, train, and weekday controls filter the trips summarized by the median and interquartile range; a trip selector overlays one date and marks its peak. Filtering by weekday places that subset beside the all-weekday train median, supporting comparison of sampled weekday-service patterns.", INTERACTIVE_BODY, "interactive"),
    ]
    for filename, title, heading, short_title, intro, body, mode in pages:
        page = PAGE.replace("__TITLE__", title).replace("__HEADING__", heading).replace("__INTRO__", intro).replace("__BODY__", body)
        page = page.replace("__TRIPS__", data["__TRIPS__"]).replace("__STOPS__", data["__STOPS__"])
        if mode == "static":
            page = page.replace("tbody tr:hover{background:#f7fafb}", "")
        # Put the mode on the body so the shared script builds only the chosen version.
        page = page.replace("<body>", f'<body data-mode="{mode}">')
        path = OUTPUT / filename
        path.write_text(page, encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
