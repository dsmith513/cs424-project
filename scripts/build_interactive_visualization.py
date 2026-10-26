#!/usr/bin/env python3
"""Build a self-contained interactive HTML explorer from processed CSV files."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
OUTPUT = ROOT / "visualizations" / "passenger-explorer.html"

PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Metra Passenger Data Explorer</title>
<style>
:root{--ink:#183247;--muted:#5d7181;--line:#dbe4ea;--blue:#2878a8;--orange:#df853e;--green:#478469;--paper:#f4f7f9}
*{box-sizing:border-box}body{margin:0;background:var(--paper);font:15px/1.45 "Segoe UI",Arial,sans-serif;color:var(--ink)}
header{padding:28px max(22px,calc((100vw - 1320px)/2));background:#183247;color:white}header h1{margin:0 0 5px;font-size:26px}header p{margin:0;color:#d6e1e8}
main{max-width:1320px;margin:22px auto;padding:0 18px 40px}.controls{display:flex;gap:14px;align-items:end;flex-wrap:wrap;background:white;border:1px solid var(--line);padding:16px;border-radius:10px;margin-bottom:16px;box-shadow:0 2px 8px #1832470a}
label{display:grid;gap:5px;font-size:12px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.05em}select,button{font:inherit;padding:8px 10px;border:1px solid #b8c7d1;border-radius:6px;background:white;color:var(--ink);min-width:155px}button{cursor:pointer;min-width:auto;background:#eaf1f5}button:hover{background:#dce8ef}.hint{color:var(--muted);font-size:13px;margin-left:auto;max-width:430px}
.grid{display:grid;grid-template-columns:1.15fr .85fr;gap:16px}.card{background:white;border:1px solid var(--line);border-radius:10px;padding:16px;box-shadow:0 2px 8px #1832470a;min-width:0}.card h2{font-size:17px;margin:0}.card .desc{font-size:13px;color:var(--muted);margin:3px 0 12px}.card svg{display:block;width:100%;height:auto;overflow:visible}.full{grid-column:1/-1}.subcontrols{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin:0 0 8px;color:var(--muted);font-size:13px}.subcontrols select{min-width:190px;padding:5px 8px}.subcontrols label{display:flex;align-items:center;gap:6px;text-transform:none;letter-spacing:0;font-weight:500;font-size:13px}.subcontrols input{accent-color:var(--blue)}.foot{color:var(--muted);font-size:12px;margin:14px 2px 0}
svg text{font-family:"Segoe UI",Arial,sans-serif;fill:var(--ink)}.axis{stroke:#8599a7;stroke-width:1}.gridline{stroke:#e4ebef;stroke-width:1}.muted{fill:var(--muted)}.bar-on{fill:var(--blue)}.bar-off{fill:var(--orange)}.individual{fill:none;stroke:#5d9aba;stroke-opacity:.24;stroke-width:1.7}.median{fill:none;stroke:#183247;stroke-width:3.7}.dot{cursor:pointer}.dot:hover{stroke:#e38235;stroke-width:3}.selected-ring{fill:none;stroke:#df853e;stroke-width:3;pointer-events:none}
@media(max-width:850px){.grid{grid-template-columns:1fr}.full{grid-column:auto}.hint{margin:4px 0 0;max-width:none}header{padding:22px}}
</style>
</head>
<body>
<header><h1>Passenger Data Explorer</h1><p>Observed passenger movement in one train car on the Cary–Chicago OTC segment.</p></header>
<main>
  <section class="controls" aria-label="Trip selection">
    <label>Direction<select id="direction"><option>Inbound</option><option>Outbound</option></select></label>
    <label>Train<select id="train"></select></label>
    <label>Date<select id="date"></select></label>
    <button id="reset" type="button">Reset selection</button>
    <div class="hint">The selected trip updates the station bars and exit-share view. The load profile shows other trips on the selected train. Select a dot below to inspect that trip.</div>
  </section>
  <section class="grid">
    <article class="card"><h2>Boarding and exiting by station</h2><p class="desc" id="bar-caption"></p><svg id="bar-chart" viewBox="0 0 820 470" role="img" aria-label="Paired horizontal bars of station boardings and exits"></svg></article>
    <article class="card"><h2>Exit distribution</h2><p class="desc" id="pie-caption"></p><svg id="pie-chart" viewBox="0 0 560 430" role="img" aria-label="Pie chart showing exits by stop and remaining passengers"></svg></article>
    <article class="card full"><h2>Passenger load along the route</h2><p class="desc" id="line-caption"></p><div class="subcontrols"><label><input id="show-individual" type="checkbox" checked> Show individual trips</label><span>Dark line shows the median at each observed stop.</span></div><svg id="line-chart" viewBox="0 0 1180 520" role="img" aria-label="Passenger count along observed stops"></svg></article>
    <article class="card full"><h2>Peak passenger load by weekday</h2><p class="desc">One dot per trip. Filled circles are inbound; hollow circles are outbound. Click a point to select that trip above.</p><div class="subcontrols"><label>Y variable<select id="scatter-metric"><option value="peak_passengers">Peak passengers</option><option value="total_boardings">Total boardings</option></select></label></div><svg id="scatter-chart" viewBox="0 0 1180 470" role="img" aria-label="Weekday scatterplot of trips"></svg></article>
  </section>
  <p class="foot">Blank station entries mean the train skipped that stop. A zero means the train stopped and nobody boarded or exited in the observed car. Comparisons are descriptive: each service was observed on a fixed subset of weekdays and at a fixed departure time.</p>
</main>
<script>
const trips = __TRIPS__;
const stopRows = __STOPS__;
const weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday"];
const directionEl = document.getElementById("direction");
const trainEl = document.getElementById("train");
const dateEl = document.getElementById("date");
let selectedId = null;

function node(tag, attrs={}, text=null){const n=document.createElementNS("http://www.w3.org/2000/svg",tag);for(const [k,v] of Object.entries(attrs))n.setAttribute(k,v);if(text!==null)n.textContent=text;return n}
function resetSvg(id){const s=document.getElementById(id);s.replaceChildren();return s}
function text(svg,x,y,value,attrs={}){svg.appendChild(node("text",{x,y,...attrs},value))}
function addLine(svg,x1,y1,x2,y2,cls="axis"){svg.appendChild(node("line",{x1,y1,x2,y2,class:cls}))}
function fmtDate(d){return d}
function idFor(t){return t.observation_id}
function median(values){const a=[...values].sort((x,y)=>x-y),m=Math.floor(a.length/2);return a.length%2?a[m]:(a[m-1]+a[m])/2}
function chosenTrip(){return trips.find(t=>idFor(t)===selectedId)||trips[0]}
function tripStops(t){return stopRows.filter(r=>r.observation_id===idFor(t))}
function rebuildTrains(preferred){const d=directionEl.value;const trains=[...new Set(trips.filter(t=>t.direction===d).map(t=>t.train_number))].sort();trainEl.replaceChildren(...trains.map(n=>new Option(n,n)));trainEl.value=trains.includes(preferred)?preferred:trains[0]}
function rebuildDates(preferred){const matches=trips.filter(t=>t.direction===directionEl.value&&t.train_number===trainEl.value).sort((a,b)=>a.date.localeCompare(b.date));dateEl.replaceChildren(...matches.map(t=>new Option(`${t.date} · ${t.day_of_week}`,t.date)));dateEl.value=matches.some(t=>t.date===preferred)?preferred:matches[0].date;const t=matches.find(r=>r.date===dateEl.value);selectedId=idFor(t)}
function selectTrip(t){selectedId=idFor(t);directionEl.value=t.direction;rebuildTrains(t.train_number);rebuildDates(t.date);render()}

function drawBars(t){const svg=resetSvg("bar-chart"),rows=tripStops(t).filter(r=>r.stop_status==="observed_stop").sort((a,b)=>+a.stop_order- +b.stop_order);document.getElementById("bar-caption").textContent=`${t.date} · ${t.direction} · Train ${t.train_number} · ${t.departure_time}`;const W=820,H=470,L=155,R=24,T=22,B=38,rowH=(H-T-B)/rows.length,max=Math.max(1,...rows.flatMap(r=>[+r.boardings,+r.exits])),scale=(W-L-R)/max*0.9;
 const ticks=5;for(let i=0;i<=ticks;i++){const v=Math.ceil(max*i/ticks),x=L+v*scale;addLine(svg,x,T,x,H-B,"gridline");text(svg,x,H-12,String(v),{"text-anchor":"middle",class:"muted","font-size":12})}addLine(svg,L,T,L,H-B);text(svg,L,H-2,"Passengers",{"text-anchor":"start","font-size":11,class:"muted"});
 rows.forEach((r,i)=>{const y=T+i*rowH+rowH/2;const bh=Math.min(12,rowH*.32);text(svg,L-10,y+4,r.stop_name,{"text-anchor":"end","font-size":12});const on=+r.boardings,off=+r.exits;const onBar=node("rect",{x:L,y:y-bh-1,width:Math.max(on?1:0,on*scale),height:bh,rx:2,class:"bar-on"});onBar.appendChild(node("title",{},`${r.stop_name}: ${on} boarded`));svg.appendChild(onBar);const offBar=node("rect",{x:L,y:y+1,width:Math.max(off?1:0,off*scale),height:bh,rx:2,class:"bar-off"});offBar.appendChild(node("title",{},`${r.stop_name}: ${off} exited`));svg.appendChild(offBar);if(on===0&&off===0)text(svg,L+4,y+4,"0",{"font-size":10,class:"muted"})});
 const ly=H-B+3;svg.appendChild(node("rect",{x:L,y:ly,width:12,height:12,rx:2,class:"bar-on"}));text(svg,L+17,ly+10,"Boarded",{"font-size":11});svg.appendChild(node("rect",{x:L+90,y:ly,width:12,height:12,rx:2,class:"bar-off"}));text(svg,L+107,ly+10,"Exited",{"font-size":11});}

function arcPath(cx,cy,r,a0,a1){const x0=cx+r*Math.cos(a0),y0=cy+r*Math.sin(a0),x1=cx+r*Math.cos(a1),y1=cy+r*Math.sin(a1),large=(a1-a0)>Math.PI?1:0;return `M ${cx} ${cy} L ${x0} ${y0} A ${r} ${r} 0 ${large} 1 ${x1} ${y1} Z`}
function drawPie(t){const svg=resetSvg("pie-chart"),caption=document.getElementById("pie-caption");if(t.direction!=="Outbound"){caption.textContent="Choose an outbound trip to inspect its exit distribution.";text(svg,280,210,"Exit-share view is for outbound trips",{"text-anchor":"middle",class:"muted","font-size":16});return}
 const rows=tripStops(t).filter(r=>r.stop_status==="observed_stop"),slices=rows.filter(r=>+r.exits>0).map(r=>({name:r.stop_name,value:+r.exits}));const summary=trips.find(q=>idFor(q)===idFor(t));slices.push({name:"Remaining after Cary",value:+summary.segment_end_passengers});const total=slices.reduce((s,d)=>s+d.value,0);caption.textContent=`${t.date} · Train ${t.train_number} · ${total} passengers exited within or remained after the observed segment.`;
 const colors=["#2878a8","#478469","#e0a044","#d46e55","#849daf","#9276a8","#62a4a9"];let angle=-Math.PI/2;const cx=170,cy=215,r=135;slices.forEach((d,i)=>{const next=angle+2*Math.PI*d.value/total;const path=node("path",{d:arcPath(cx,cy,r,angle,next),fill:colors[i%colors.length],stroke:"white","stroke-width":2});path.appendChild(node("title",{},`${d.name}: ${d.value} (${(100*d.value/total).toFixed(1)}%)`));svg.appendChild(path);const y=132+i*35;svg.appendChild(node("rect",{x:340,y:y-13,width:15,height:15,rx:2,fill:colors[i%colors.length]}));text(svg,364,y,`${d.name}: ${d.value}`,{"font-size":13});angle=next});text(svg,cx,cy+4,String(total),{"text-anchor":"middle","font-size":24,"font-weight":700});text(svg,cx,cy+24,"passengers",{"text-anchor":"middle","font-size":11,class:"muted"})}

function drawLine(t){const svg=resetSvg("line-chart"),show=document.getElementById("show-individual").checked,rows=stopRows.filter(r=>r.direction===t.direction&&r.train_number===t.train_number);const ids=[...new Set(rows.map(r=>r.observation_id))];const groups=ids.map(id=>rows.filter(r=>r.observation_id===id).sort((a,b)=>+a.stop_order- +b.stop_order));const base=groups.find(g=>g[0]?.observation_id===idFor(t))||groups[0]||[];const stations=base.map(r=>r.stop_name);document.getElementById("line-caption").textContent=`${t.direction} · Train ${t.train_number} · ${groups.length} observed trips · stop order follows this service's route.`;const W=1180,H=520,L=68,R=24,T=26,B=132,all=groups.flatMap(g=>g.map(r=>+r.passengers_after_stop)),max=Math.ceil(Math.max(1,...all)/10)*10,scaleX=(W-L-R)/Math.max(1,stations.length-1),scaleY=(H-T-B)/max;
 for(let v=0;v<=max;v+=10){const y=H-B-v*scaleY;addLine(svg,L,y,W-R,y,"gridline");text(svg,L-9,y+4,String(v),{"text-anchor":"end","font-size":11,class:"muted"})}addLine(svg,L,T,L,H-B);addLine(svg,L,H-B,W-R,H-B);stations.forEach((name,i)=>{const x=L+i*scaleX;text(svg,x,H-B+17,name,{"text-anchor":"end","font-size":10,class:"muted",transform:`rotate(-42 ${x} ${H-B+17})`})});
 if(show){groups.forEach(g=>{const points=g.map((r,i)=>`${L+i*scaleX},${H-B-(+r.passengers_after_stop)*scaleY}`).join(" ");const pl=node("polyline",{points,class:"individual"});pl.appendChild(node("title",{},g[0].date));svg.appendChild(pl)})}
 const medians=stations.map((_,i)=>{const vals=groups.map(g=>+g[i]?.passengers_after_stop).filter(Number.isFinite);return vals.length?median(vals):0});const medianPoints=medians.map((v,i)=>`${L+i*scaleX},${H-B-v*scaleY}`).join(" ");svg.appendChild(node("polyline",{points:medianPoints,class:"median"}));medians.forEach((v,i)=>{const c=node("circle",{cx:L+i*scaleX,cy:H-B-v*scaleY,r:4,fill:"#183247"});c.appendChild(node("title",{},`${stations[i]} median: ${v}`));svg.appendChild(c)});}

function drawScatter(){const svg=resetSvg("scatter-chart"),metric=document.getElementById("scatter-metric").value,W=1180,H=470,L=70,R=25,T=28,B=58,max=Math.ceil(Math.max(...trips.map(t=>+t[metric]))/10)*10,scaleY=(H-T-B)/max,step=(W-L-R)/4;for(let v=0;v<=max;v+=10){const y=H-B-v*scaleY;addLine(svg,L,y,W-R,y,"gridline");text(svg,L-9,y+4,String(v),{"text-anchor":"end","font-size":11,class:"muted"})}addLine(svg,L,T,L,H-B);weekdays.forEach((d,i)=>text(svg,L+i*step,H-22,d,{"text-anchor":"middle","font-size":12}));text(svg,14,18,metric==="peak_passengers"?"Peak passengers":"Total boardings",{"font-size":11,class:"muted"});const occurrence={};trips.forEach(t=>{const day=weekdays.indexOf(t.day_of_week);const k=t.day_of_week+t.direction;const n=occurrence[k]||0;occurrence[k]=n+1;const jitter=((n%5)-2)*5;const directionOffset=t.direction==="Inbound"?-7:7;const x=L+day*step+directionOffset+jitter,y=H-B-(+t[metric])*scaleY,selected=idFor(t)===selectedId;const c=node("circle",{cx:x,cy:y,r:selected?6:4.8,fill:t.direction==="Inbound"?"#2878a8":"white",stroke:"#2878a8","stroke-width":selected?2.5:1.7,class:"dot",tabindex:0});c.appendChild(node("title",{},`${t.date} · ${t.direction} · Train ${t.train_number} · ${metric.replaceAll("_"," ")}: ${t[metric]}. Click to select.`));c.addEventListener("click",()=>selectTrip(t));c.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" ")selectTrip(t)});svg.appendChild(c);if(selected)svg.appendChild(node("circle",{cx:x,cy:y,r:10,class:"selected-ring"}))})}

function render(){const t=chosenTrip();drawBars(t);drawPie(t);drawLine(t);drawScatter()}
directionEl.addEventListener("change",()=>{rebuildTrains();rebuildDates();render()});trainEl.addEventListener("change",()=>{rebuildDates();render()});dateEl.addEventListener("change",()=>{const t=trips.find(q=>q.direction===directionEl.value&&q.train_number===trainEl.value&&q.date===dateEl.value);if(t)selectedId=idFor(t);render()});document.getElementById("show-individual").addEventListener("change",()=>drawLine(chosenTrip()));document.getElementById("scatter-metric").addEventListener("change",drawScatter);document.getElementById("reset").addEventListener("click",()=>{directionEl.value="Inbound";rebuildTrains("640");rebuildDates("2026-09-21");render()});
directionEl.value="Inbound";rebuildTrains("640");rebuildDates("2026-09-21");render();
</script>
</body></html>'''


def main() -> None:
    with (DATA / "passenger-stops.csv").open(newline="", encoding="utf-8") as handle:
        stops = list(csv.DictReader(handle))
    with (DATA / "trip-summary.csv").open(newline="", encoding="utf-8") as handle:
        trips = list(csv.DictReader(handle))
    page = PAGE.replace("__STOPS__", json.dumps(stops, ensure_ascii=False))
    page = page.replace("__TRIPS__", json.dumps(trips, ensure_ascii=False))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(page, encoding="utf-8")
    print(f"Wrote interactive explorer to {OUTPUT}")


if __name__ == "__main__":
    main()
