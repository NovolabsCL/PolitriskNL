# dashboard/app.py — PolitRisk Pro v2
# streamlit run dashboard/app.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import io, contextlib, sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from connectors.orchestrator import fetch_automatic_data
from engine.scoring          import ScoringEngine
from engine.financial        import calculate_efa, calculate_rar, format_usd
from engine.recommendations  import generate, conditions_by_category
from data.all_countries      import ALL_COUNTRIES, ISO3_TO_NAME
from config                  import SECTORS, ASSET_TYPES

st.set_page_config(page_title="PolitRisk Pro", page_icon="🌐",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&family=DM+Mono:wght@400;500&display=swap');
:root{--navy:#0F1E35;--navy-mid:#1B2F4E;--blue:#2451A0;--gold:#B8891A;--gold-lt:#D4A843;
      --silver:#8395A7;--g100:#F3F5F8;--g200:#E4E9F0;--g400:#98A6B5;
      --white:#FFFFFF;--green:#1A6B4A;--red:#8C1F1F;}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;color:var(--navy)!important;}
.stApp{background:var(--navy)!important;}

/* ── SIDEBAR VISIBLE ── */
[data-testid="stSidebar"]{background:var(--navy-mid)!important;border-right:1px solid #2A4060!important;}
[data-testid="stSidebar"] *{color:var(--g200)!important;}
[data-testid="stSidebar"] label{color:var(--g400)!important;font-size:.67rem!important;
  text-transform:uppercase!important;letter-spacing:.09em!important;font-weight:500!important;}
[data-testid="stSidebar"] .stSelectbox>div>div{background:#0F1E35!important;
  border:1px solid #2A4060!important;border-radius:3px!important;}
[data-testid="stSidebar"] hr{border-color:#2A4060!important;margin:.8rem 0!important;}
[data-testid="stSidebar"] .stButton>button{background:var(--gold)!important;
  color:var(--navy)!important;border:none!important;font-weight:600!important;
  font-size:.78rem!important;letter-spacing:.07em!important;text-transform:uppercase!important;
  padding:.6rem 1rem!important;border-radius:3px!important;width:100%!important;}
/* Botón de toggle del sidebar — hacerlo visible */
button[kind="header"]{background:rgba(184,137,26,0.2)!important;border:1px solid var(--gold)!important;}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"]{background:#1B2F4E!important;border-radius:4px 4px 0 0!important;gap:2px!important;padding:4px 4px 0!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--g400)!important;border:none!important;border-radius:3px 3px 0 0!important;font-size:.70rem!important;font-weight:500!important;letter-spacing:.06em!important;text-transform:uppercase!important;padding:.5rem .85rem!important;}
.stTabs [aria-selected="true"]{background:var(--white)!important;color:var(--navy)!important;font-weight:600!important;}
.stTabs [data-baseweb="tab-panel"]{background:var(--white)!important;border:1px solid var(--g200)!important;border-top:none!important;border-radius:0 0 4px 4px!important;padding:1.2rem!important;}

/* ── COMPONENTES ── */
.app-hdr{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;padding:.8rem 1.5rem;background:var(--navy);border-bottom:1px solid #2A4060;margin-bottom:0;}
@media (max-width: 768px) {
    .app-hdr { flex-direction: column; align-items: flex-start; }
    .app-meta { line-height: 1.4; }
    .map-legend { flex-wrap: wrap; text-align: center; }
}.app-brand{font-family:'DM Serif Display',serif;font-size:1.1rem;color:var(--white);margin:0;}
.app-brand span{color:var(--gold);}
.app-meta{font-size:.63rem;color:var(--silver);font-family:'DM Mono',monospace;letter-spacing:.06em;}
.kpi{background:var(--white);border:1px solid var(--g200);border-top:3px solid var(--navy);padding:.9rem 1.1rem;border-radius:2px;}
.kpi.g{border-top-color:var(--green);}.kpi.y{border-top-color:var(--gold);}.kpi.r{border-top-color:var(--red);}
.kpi-lbl{font-size:.58rem;text-transform:uppercase;letter-spacing:.11em;color:var(--silver);font-weight:600;margin-bottom:.25rem;}
.kpi-val{font-family:'DM Serif Display',serif;font-size:1.7rem;color:var(--navy);line-height:1;margin-bottom:.12rem;}
.kpi-sub{font-size:.62rem;color:var(--silver);font-family:'DM Mono',monospace;}
.vbadge{display:inline-block;padding:.2rem .6rem;border-radius:2px;font-size:.65rem;font-weight:600;letter-spacing:.09em;text-transform:uppercase;}
.vb-v{background:#E8F5EE;color:var(--green);border:1px solid #A8D5BC;}
.vb-c{background:#FDF8EC;color:#8C6010;border:1px solid #E8C97A;}
.vb-n{background:#FAEAEA;color:var(--red);border:1px solid #D4A0A0;}
.map-legend{display:flex;gap:1.2rem;align-items:center;justify-content:center;padding:.5rem 0;}
.li{display:flex;align-items:center;gap:.4rem;font-size:.63rem;color:var(--silver);font-family:'DM Mono',monospace;}
.ld{width:10px;height:10px;border-radius:50%;flex-shrink:0;}
.click-hint{text-align:center;font-size:.72rem;color:var(--silver);padding:.3rem 0 .1rem;font-family:'DM Mono',monospace;letter-spacing:.05em;}
.country-selected{background:#1B2F4E;border:1px solid var(--gold);border-radius:4px;padding:.8rem 1.2rem;margin-bottom:.8rem;display:flex;justify-content:space-between;align-items:center;}
.cs-name{font-family:'DM Serif Display',serif;font-size:1.1rem;color:var(--white);}
.cs-meta{font-size:.65rem;color:var(--silver);font-family:'DM Mono',monospace;}
.ind-row{display:flex;align-items:center;padding:.35rem 0;border-bottom:1px solid var(--g100);gap:.45rem;}
.ind-code{font-family:'DM Mono',monospace;font-size:.61rem;color:var(--silver);width:46px;flex-shrink:0;}
.ind-name{font-size:.72rem;color:var(--navy);flex:1;line-height:1.3;}
.ind-ya{font-family:'DM Mono',monospace;font-size:.61rem;color:#8C6010;width:34px;text-align:center;flex-shrink:0;background:#FDF8EC;border-radius:2px;padding:1px 3px;}
.ind-ym{font-family:'DM Mono',monospace;font-size:.61rem;color:var(--g400);width:34px;text-align:center;flex-shrink:0;}
.ind-sc{font-family:'DM Mono',monospace;font-size:.72rem;font-weight:500;width:32px;text-align:right;flex-shrink:0;}
.ind-bb{width:60px;height:3px;background:var(--g200);border-radius:2px;flex-shrink:0;overflow:hidden;}
.ind-bf{height:100%;border-radius:2px;}
.ind-na{font-family:'DM Mono',monospace;font-size:.61rem;color:var(--g400);}
.rec-text{font-size:.80rem;line-height:1.75;color:#1B2F4E;margin:0;}
.cond-cat{font-size:.58rem;text-transform:uppercase;letter-spacing:.14em;color:var(--silver);font-weight:600;margin:.9rem 0 .35rem;}
.ci{padding:.5rem .75rem;margin-bottom:.28rem;border-radius:2px;}
.ci.ob{background:#FDF8EC;border-left:3px solid var(--gold);}
.ci.re{background:var(--g100);border-left:3px solid var(--g400);}
.ci-main{font-size:.78rem;color:var(--navy);font-weight:500;line-height:1.3;}
.ci-rat{font-size:.70rem;color:var(--silver);margin-top:.2rem;line-height:1.4;font-style:italic;}
.ci-prio{font-size:.58rem;text-transform:uppercase;letter-spacing:.08em;font-weight:600;}
.ob-lbl{color:var(--gold);}.re-lbl{color:var(--silver);}
.efa-box{background:#F3F5F8;border-left:3px solid var(--blue);padding:.7rem .9rem;border-radius:2px;margin:.7rem 0;font-size:.76rem;color:#1B2F4E;line-height:1.65;}
.sb-s{font-size:.58rem!important;text-transform:uppercase!important;letter-spacing:.15em!important;color:var(--gold)!important;font-weight:600!important;margin-bottom:.35rem!important;}
footer{display:none!important;}#MainMenu{display:none!important;}header{display:none!important;}.stDeployButton{display:none!important;}

/* ── BOTÓN TOGGLE SIDEBAR — todas las versiones de Streamlit ── */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"],
button[aria-label="Close sidebar"],
button[aria-label="Open sidebar"],
button[aria-label="Collapse sidebar"],
button[aria-label="Expand sidebar"],
.css-1rs6os, .css-17ziqus, .css-fblp2m {
    background: var(--gold) !important;
    border-radius: 0 6px 6px 0 !important;
    width: 2rem !important;
    height: 2.5rem !important;
    border: none !important;
    cursor: pointer !important;
    position: fixed !important;
    top: 50% !important;
    left: 0 !important;
    z-index: 9999 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 2px 0 8px rgba(0,0,0,0.4) !important;
}
[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] svg,
button[aria-label="Open sidebar"] svg,
button[aria-label="Expand sidebar"] svg {
    fill: var(--navy) !important;
    color: var(--navy) !important;
    width: 16px !important;
    height: 16px !important;
}
/* Cuando el sidebar está expandido, mover el botón */
[data-testid="stSidebar"][aria-expanded="true"] ~ * [data-testid="collapsedControl"] {
    left: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── ESTADO ───────────────────────────────────────────────────────
if "analyses"       not in st.session_state: st.session_state.analyses       = {}
if "analyst_notes"  not in st.session_state: st.session_state.analyst_notes  = {}
if "clicked_country"not in st.session_state: st.session_state.clicked_country= None
engine = ScoringEngine()

# ── HELPERS ──────────────────────────────────────────────────────
def sc(s):
    if s is None: return "#98A6B5"
    if s>=70: return "#1A6B4A"
    if s>=55: return "#B8891A"
    if s>=40: return "#C05A1A"
    return "#8C1F1F"
def rl(lvl): return {"viable":"Viable","conditioned":"Condicionado","not_viable":"No Viable","insufficient_data":"Insuficiente"}.get(lvl,"—")
def rb(lvl): return {"viable":"vb-v","conditioned":"vb-c","not_viable":"vb-n"}.get(lvl,"vb-c")
def kc(lvl): return {"viable":"g","conditioned":"y","not_viable":"r"}.get(lvl,"")

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="padding:1.2rem 1rem .8rem;border-bottom:1px solid #2A4060;margin-bottom:1.2rem;"><p style="font-family:\'DM Serif Display\',serif;font-size:1.1rem;color:white;margin:0;">PolitRisk <span style=\'color:#B8891A\'>Pro</span></p><p style="font-size:.60rem;color:#8395A7;text-transform:uppercase;letter-spacing:.13em;margin-top:.15rem;">Configuración del Análisis</p></div>', unsafe_allow_html=True)

    st.markdown('<p class="sb-s">País y Sector</p>', unsafe_allow_html=True)

    # Si se hizo clic en el mapa, preseleccionar ese país
    default_country = st.session_state.clicked_country or "Chile"
    country_list = sorted(ALL_COUNTRIES.keys())
    default_idx  = country_list.index(default_country) if default_country in country_list else 0

    country    = st.selectbox("País de destino", country_list, index=default_idx)
    sector     = st.selectbox("Sector", list(SECTORS.keys()), format_func=lambda x: SECTORS[x])
    a_year     = st.selectbox("Año de referencia del informe",
                               [2026,2025,2024,2023,2022,2021,2020], index=0,
                               help="Los datos automáticos usan siempre el año más reciente disponible")
    asset_type = st.selectbox("Tipo de activo", list(ASSET_TYPES.keys()),
                               format_func=lambda x: ASSET_TYPES[x].split("(")[0].strip())
    st.markdown("---")

    st.markdown('<p class="sb-s">Dimensión Política</p>', unsafe_allow_html=True)
    p06=st.slider("V-Dem EDI (0–1)",0.0,1.0,0.79,0.01,help="vdem.net")
    p07=st.slider("Freedom House (0–100)",0.0,100.0,75.0,1.0,help="freedomhouse.org")
    p08=st.slider("Conflicto UCDP (0–10)",0.0,10.0,2.0,0.5,help="ucdp.uu.se")
    p09=st.slider("GPR Index",50.0,500.0,130.0,5.0,help="matteoiacoviello.com")
    p10=st.slider("Riesgo expropiación (0–10)",0.0,10.0,3.0,0.5)
    st.markdown("---")

    st.markdown('<p class="sb-s">Dimensión Económica</p>', unsafe_allow_html=True)
    e05=st.selectbox("Rating soberano",["AAA","AA+","AA","AA-","A+","A","A-","BBB+","BBB","BBB-","BB+","BB","BB-","B+","B","B-","CCC","D"],index=5)
    e06=st.slider("CDS spread (puntos base)",0.0,2000.0,120.0,5.0,help="worldgovernmentbonds.com")
    e01=st.number_input("Inflación (%)",value=5.0,step=0.1,help="imf.org WEO")
    e02=st.number_input("Crecimiento PIB (%)",value=2.5,step=0.1)
    e03=st.number_input("Deuda / PIB (%)",value=50.0,step=0.5)
    e08=st.number_input("Cuenta corriente / PIB (%)",value=-2.0,step=0.5)
    st.markdown("---")

    st.markdown('<p class="sb-s">Ambiente de Negocios</p>', unsafe_allow_html=True)
    b07=st.slider("TRACE Bribery (0–100)",0.0,100.0,45.0,1.0,help="traceinternational.org")
    b08=st.slider("Cobertura TBIs (0–10)",0.0,10.0,5.0,0.5,help="unctad.org")
    st.markdown("---")

    st.markdown('<p class="sb-s">Dimensión Social</p>', unsafe_allow_html=True)
    s01=st.slider("CPI (0–100)",0.0,100.0,50.0,1.0,help="transparency.org")
    s03=st.slider("GPI (1–5)",1.0,5.0,2.0,0.01,help="visionofhumanity.org")
    s04=st.slider("RSF Prensa (0–100)",0.0,100.0,40.0,1.0,help="rsf.org")
    s05=st.slider("ND-GAIN (0–100)",0.0,100.0,50.0,0.5,help="gain.nd.edu")
    s06=st.slider("Yale EPI (0–100)",0.0,100.0,45.0,0.5,help="epi.yale.edu")
    s07=st.slider("Riesgo ESG (0–10)",0.0,10.0,5.0,0.5)
    s08=st.slider("Presión comunitaria (0–10)",0.0,10.0,5.0,0.5)
    st.markdown("---")

    st.markdown('<p class="sb-s">Oportunidad Estratégica</p>', unsafe_allow_html=True)
    o02=st.number_input("Crecimiento sector (%)",value=4.0,step=0.5)
    o03=st.number_input("Tamaño mercado (USD M)",value=20000.0,step=1000.0)
    o04=st.slider("Incentivos IED (0–10)",0.0,10.0,5.0,0.5)
    o05=st.slider("Afinidad cultural (0–10)",0.0,10.0,5.0,0.5)
    o06=st.slider("Multilateral (0–10)",0.0,10.0,5.0,0.5)
    st.markdown("---")

    st.markdown('<p class="sb-s">Análisis Financiero (Opcional)</p>', unsafe_allow_html=True)
    inv=st.number_input("Inversión total (USD)",value=10_000_000,step=500_000)
    ret=st.number_input("Retorno esperado (USD/año)",value=1_500_000,step=100_000)
    st.markdown("---")
    run_btn=st.button("Ejecutar Análisis")

# ── EJECUCIÓN ────────────────────────────────────────────────────
if run_btn:
    with st.spinner(f"Descargando datos para {country}..."):
        try:
            buf=io.StringIO()
            with contextlib.redirect_stdout(buf):
                auto_data=fetch_automatic_data(country)
            manual_data={
                "POL_06":p06,"POL_07":p07,"POL_08":p08,"POL_09":p09,"POL_10":p10,
                "ECO_01":e01,"ECO_02":e02,"ECO_03":e03,"ECO_05":e05,"ECO_06":e06,"ECO_08":e08,
                "BIZ_07":b07,"BIZ_08":b08,
                "SOC_01":s01,"SOC_03":s03,"SOC_04":s04,"SOC_05":s05,"SOC_06":s06,"SOC_07":s07,"SOC_08":s08,
                "OPP_02":o02,"OPP_03":o03,"OPP_04":o04,"OPP_05":o05,"OPP_06":o06,
            }
            irp=engine.compute(country,sector,a_year,auto_data,manual_data)
            efa=None
            if inv>0:
                eco07=auto_data.get("ECO_07")
                fxv=eco07.get("value") if isinstance(eco07,dict) else eco07
                efa=calculate_efa(investment_usd=inv,irp_score=irp.irp_score or 50,fx_volatility=fxv,fx_data=auto_data)
                if ret>0: efa=calculate_rar(efa,ret)
            rec=generate(irp,asset_type,efa)
            st.session_state.analyses[f"{country}_{sector}"]=(irp,efa,rec)
            st.success(f"✓ Análisis de {country} completado — IRP: {irp.irp_score:.1f}")
        except Exception as e:
            st.error(f"Error: {e}")
            import traceback; st.code(traceback.format_exc())

# ── HEADER ───────────────────────────────────────────────────────
n=len(st.session_state.analyses)
st.markdown(f'<div class="app-hdr"><p class="app-brand">PolitRisk <span>Pro</span></p><p class="app-meta">Political Risk & Market Entry Intelligence &nbsp;|&nbsp; {n} análisis en cartera &nbsp;|&nbsp; {datetime.now().strftime("%d %b %Y")}</p></div>', unsafe_allow_html=True)
st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

# ── MAPA MUNDIAL ─────────────────────────────────────────────────
analyzed_rows, available_rows = [], []
analyzed_names = set()

for key,(a_irp,_,_) in st.session_state.analyses.items():
    iso3 = ALL_COUNTRIES.get(a_irp.country,{}).get("iso3")
    if iso3:
        analyzed_rows.append({
            "iso3":iso3,"country":a_irp.country,"irp":a_irp.irp_score or 0,
            "text":f"<b>{a_irp.country}</b><br>IRP: {a_irp.irp_score:.1f} — {rl(a_irp.risk_level)}<br>{SECTORS.get(a_irp.sector,'')}<br><i>Haz clic para ver el análisis</i>",
        })
        analyzed_names.add(a_irp.country)

for cname,cdata in ALL_COUNTRIES.items():
    if cname not in analyzed_names:
        iso3=cdata.get("iso3")
        if iso3:
            available_rows.append({
                "iso3":iso3,"country":cname,
                "text":f"<b>{cname}</b><br>Sin análisis<br><i>Selecciona en el panel izquierdo para analizar</i>",
            })

fig_map=go.Figure()

if available_rows:
    df_av=pd.DataFrame(available_rows)
    fig_map.add_trace(go.Choropleth(
        locations=df_av["iso3"], z=[0.5]*len(df_av),
        colorscale=[[0,"#1B2F4E"],[1,"#1B2F4E"]],
        showscale=False, marker_line_color="#2A4060", marker_line_width=0.5,
        hovertext=df_av["text"], hoverinfo="text", name="Sin análisis",
        customdata=df_av["country"],
    ))

if analyzed_rows:
    df_an=pd.DataFrame(analyzed_rows)
    fig_map.add_trace(go.Choropleth(
        locations=df_an["iso3"], z=df_an["irp"], zmin=0, zmax=100,
        colorscale=[
            [0.0,"#8C1F1F"],[0.4,"#8C1F1F"],
            [0.4,"#B85C1A"],[0.55,"#B85C1A"],
            [0.55,"#B8891A"],[0.70,"#B8891A"],
            [0.70,"#1A6B4A"],[1.0,"#1A6B4A"],
        ],
        showscale=True,
        colorbar=dict(
            title=dict(text="IRP",font=dict(size=10,family="DM Mono",color="#8395A7")),
            tickfont=dict(size=9,family="DM Mono",color="#8395A7"),
            thickness=10,len=0.5,x=1.01,bgcolor="rgba(0,0,0,0)",bordercolor="#2A4060"),
        marker_line_color="#0F1E35", marker_line_width=1.5,
        hovertext=df_an["text"], hoverinfo="text", name="Analizados",
        customdata=df_an["country"],
    ))

fig_map.update_layout(
    geo=dict(showframe=False,showcoastlines=True,coastlinecolor="#2A4060",
             showland=True,landcolor="#1B2F4E",showocean=True,oceancolor="#0F1E35",
             showcountries=True,countrycolor="#2A4060",bgcolor="#0F1E35",
             projection_type="natural earth"),
    paper_bgcolor="#0F1E35",plot_bgcolor="#0F1E35",
margin=dict(l=0,r=0,t=20,b=20),height=350,autosize=True,showlegend=False,    dragmode="pan",
)

# Capturar clic en el mapa
event=st.plotly_chart(
    fig_map, use_container_width=True,
    config={"displayModeBar":True,"scrollZoom":True,
            "modeBarButtonsToRemove":["select2d","lasso2d","autoScale2d"],
            "displaylogo":False},
    on_select="rerun",
    key="world_map",
)

# Procesar clic
if event and hasattr(event,"selection") and event.selection:
    pts=event.selection.get("points",[])
    if pts:
        loc=pts[0].get("location") or pts[0].get("customdata")
        if loc:
            # Si es ISO3, convertir a nombre
            if loc in ISO3_TO_NAME:
                clicked=ISO3_TO_NAME[loc]
            elif loc in ALL_COUNTRIES:
                clicked=loc
            else:
                clicked=None
            if clicked and clicked!=st.session_state.clicked_country:
                st.session_state.clicked_country=clicked
                st.rerun()

# Leyenda + hint
st.markdown("""
<div class="map-legend">
    <div class="li"><div class="ld" style="background:#1A6B4A"></div>Viable (≥70)</div>
    <div class="li"><div class="ld" style="background:#B8891A"></div>Medio-bajo (55–69)</div>
    <div class="li"><div class="ld" style="background:#B85C1A"></div>Medio-alto (40–54)</div>
    <div class="li"><div class="ld" style="background:#8C1F1F"></div>No viable (&lt;40)</div>
    <div class="li"><div class="ld" style="background:#1B2F4E;border:1px solid #2A4060"></div>Sin análisis</div>
</div>
<p class="click-hint">Haz clic en un país analizado para ver su resultado · Haz clic en cualquier país para seleccionarlo en el panel lateral</p>
""", unsafe_allow_html=True)

st.markdown("<div style='height:.6rem'></div>", unsafe_allow_html=True)

# ── PANEL DE ANÁLISIS ─────────────────────────────────────────────
if not st.session_state.analyses:
    st.markdown("""
    <div style="text-align:center;padding:2rem;background:#1B2F4E;border-radius:4px;border:1px solid #2A4060;">
        <p style="font-family:'DM Serif Display',serif;font-size:1.3rem;color:white;margin-bottom:.4rem;">
            Ningún país analizado aún
        </p>
        <p style="font-size:.80rem;color:#8395A7;margin:0;">
            Configura el análisis en el panel izquierdo y haz clic en <strong style="color:#B8891A">Ejecutar Análisis</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    DK=["political","economic","business","social","opportunity"]
    DL=["Político","Económico","Negocios","Social","Oportunidad"]

    # Selector
    keys=list(st.session_state.analyses.keys())
    labels=[f"{st.session_state.analyses[k][0].country} — {SECTORS.get(st.session_state.analyses[k][0].sector,'')}" for k in keys]

    # Si se hizo clic en el mapa en un país analizado, seleccionarlo
    default_sel=len(labels)-1
    if st.session_state.clicked_country:
        for i,k in enumerate(keys):
            if st.session_state.analyses[k][0].country==st.session_state.clicked_country:
                default_sel=i; break

    if len(st.session_state.analyses)>1:
        sel_lbl=st.selectbox("Ver análisis:",labels,index=default_sel,label_visibility="collapsed")
        sel_key=keys[labels.index(sel_lbl)]
    else:
        sel_key=keys[0]

    irp,efa,rec=st.session_state.analyses[sel_key]

    # Banner país seleccionado
    st.markdown(f"""
    <div class="country-selected">
        <div>
            <div class="cs-name">{irp.country}</div>
            <div class="cs-meta">{SECTORS.get(irp.sector,'')} &nbsp;|&nbsp; Año de referencia: {irp.analysis_year} &nbsp;|&nbsp; Cobertura: {irp.data_coverage_pct:.0f}%</div>
        </div>
        <span class="vbadge {rb(irp.risk_level)}">{rl(irp.risk_level)}</span>
    </div>
    """, unsafe_allow_html=True)

    # KPIs
    c1,c2,c3,c4=st.columns(4)
    irp_s=f"{irp.irp_score:.1f}" if irp.irp_score else "N/D"
    with c1: st.markdown(f'<div class="kpi {kc(irp.risk_level)}"><div class="kpi-lbl">IRP — Índice de Riesgo Político</div><div class="kpi-val">{irp_s}</div><div class="kpi-sub">Escala 0–100</div></div>',unsafe_allow_html=True)
    with c2:
        ev=format_usd(efa.efa_usd) if efa else "—"
        es=f"{efa.efa_pct:.1f}% de la inversión" if efa else "Sin datos financieros"
        st.markdown(f'<div class="kpi"><div class="kpi-lbl">EFA — Exposición Financiera Ajustada</div><div class="kpi-val">{ev}</div><div class="kpi-sub">{es}</div></div>',unsafe_allow_html=True)
    with c3:
        rv=f"{efa.rar:.2f}x" if (efa and efa.rar) else "—"
        st.markdown(f'<div class="kpi"><div class="kpi-lbl">RAR — Retorno Ajustado por Riesgo</div><div class="kpi-val">{rv}</div><div class="kpi-sub">Retorno / Exposición</div></div>',unsafe_allow_html=True)
    with c4:
        fx=f"{efa.fx_volatility*100:.1f}%" if (efa and efa.fx_volatility) else "—"
        st.markdown(f'<div class="kpi"><div class="kpi-lbl">Volatilidad Cambiaria (12 meses)</div><div class="kpi-val">{fx}</div><div class="kpi-sub">Yahoo Finance — dato de hoy</div></div>',unsafe_allow_html=True)

    st.markdown("<div style='height:.5rem'></div>",unsafe_allow_html=True)

    # TABS
    t1,t2,t3,t4=st.tabs(["Radar & Scores","Recomendación Estratégica","Indicadores Detallados","Comparador"])

    with t1:
        cr,cb=st.columns([1,1],gap="medium")
        COLORS=["#2451A0","#B8891A","#1A6B4A","#8C1F1F","#5A3A9A"]
        with cr:
            traces=[]
            for i,(k,(a,_,_)) in enumerate(st.session_state.analyses.items()):
                vals=[a.dimensions[dk].dimension_score or 0 for dk in DK]
                traces.append(go.Scatterpolar(r=vals+[vals[0]],theta=DL+[DL[0]],fill="toself",
                    name=a.country,line=dict(color=COLORS[i%5],width=2),fillcolor=COLORS[i%5],opacity=0.15))
            fig_r=go.Figure(data=traces)
            fig_r.update_layout(polar=dict(bgcolor="#F3F5F8",
                radialaxis=dict(visible=True,range=[0,100],tickfont=dict(size=9,family="DM Mono",color="#98A6B5"),gridcolor="#E4E9F0",linecolor="#E4E9F0"),
                angularaxis=dict(tickfont=dict(size=10,family="DM Sans",color="#0F1E35"),gridcolor="#E4E9F0",linecolor="#E4E9F0")),
                showlegend=len(st.session_state.analyses)>1,
                legend=dict(font=dict(size=10,family="DM Sans"),bgcolor="rgba(255,255,255,0.8)"),
                height=300,margin=dict(l=35,r=35,t=10,b=10),
                paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_r,use_container_width=True,config={"displayModeBar":False})
        with cb:
            bl=[irp.dimensions[k].name for k in DK]
            bs=[irp.dimensions[k].dimension_score or 0 for k in DK]
            fig_b=go.Figure(go.Bar(x=bs,y=bl,orientation="h",marker_color=[sc(s) for s in bs],
                text=[f"{s:.1f}" for s in bs],textposition="outside",textfont=dict(size=11,family="DM Mono",color="#0F1E35")))
            fig_b.update_layout(xaxis=dict(range=[0,115],showgrid=True,gridcolor="#E4E9F0",tickfont=dict(size=9,family="DM Mono",color="#98A6B5"),zeroline=False),
                yaxis=dict(tickfont=dict(size=10,family="DM Sans",color="#0F1E35"),autorange="reversed"),
                height=280,margin=dict(l=10,r=50,t=10,b=10),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",bargap=0.45)
            fig_b.add_vline(x=70,line_dash="dot",line_color="#1A6B4A",line_width=1,opacity=0.5,annotation_text="Viable",annotation_font=dict(size=9,color="#1A6B4A"))
            st.plotly_chart(fig_b,use_container_width=True,config={"displayModeBar":False})

    with t2:
        col_rec,col_n=st.columns([2,1],gap="medium")
        with col_rec:
            st.markdown(f'<div style="margin-bottom:.9rem;"><span class="vbadge {rb(irp.risk_level)}">{rl(irp.risk_level)}</span></div>',unsafe_allow_html=True)
            st.markdown(f'<p class="rec-text">{rec.executive_summary}</p>',unsafe_allow_html=True)
            if efa and rec.efa_summary: st.markdown(f'<div class="efa-box">{rec.efa_summary}</div>',unsafe_allow_html=True)
            for label,attr in [("Análisis Político e Institucional","political_analysis"),
                                ("Análisis Económico y Financiero","economic_analysis"),
                                ("Análisis del Ambiente de Negocios","business_analysis"),
                                ("Análisis Social y Reputacional","social_analysis"),
                                ("Análisis de Oportunidad Estratégica","opportunity_analysis")]:
                with st.expander(label): st.markdown(f'<p class="rec-text">{getattr(rec,attr)}</p>',unsafe_allow_html=True)
            grouped=conditions_by_category(rec)
            for cat,name in [("contractual","Condiciones Contractuales"),("financial","Condiciones Financieras"),("operational","Condiciones Operacionales")]:
                conds=grouped.get(cat,[])
                if conds:
                    st.markdown(f'<div class="cond-cat">{name}</div>',unsafe_allow_html=True)
                    for c in conds:
                        cls="ob" if c.priority=="obligatoria" else "re"
                        pl="Obligatoria" if c.priority=="obligatoria" else "Recomendada"
                        lc="ob-lbl" if c.priority=="obligatoria" else "re-lbl"
                        st.markdown(f'<div class="ci {cls}"><div><span class="ci-prio {lc}">{pl}</span> <span class="ci-main">{c.text}</span></div><div class="ci-rat">{c.rationale}</div></div>',unsafe_allow_html=True)
        with col_n:
            st.markdown('<p style="font-size:.60rem;text-transform:uppercase;letter-spacing:.12em;color:#98A6B5;font-weight:600;margin-bottom:.4rem;">Notas del Analista</p>',unsafe_allow_html=True)
            kn=f"{irp.country}_{irp.sector}"
            notes=st.text_area("Notas",value=st.session_state.analyst_notes.get(kn,""),height=220,placeholder="Contexto cualitativo, ajustes, supuestos...",label_visibility="collapsed")
            st.session_state.analyst_notes[kn]=notes
            st.markdown(f'<div style="margin-top:.8rem;padding:.7rem;background:#F3F5F8;border-radius:2px;font-size:.68rem;color:#98A6B5;line-height:1.55;"><strong style="color:#0F1E35;display:block;margin-bottom:.2rem;">Plazo de revisión</strong>{rec.review_schedule}</div>',unsafe_allow_html=True)

    with t3:
        dtabs=st.tabs([irp.dimensions[k].name for k in DK])
        for dt,dk in zip(dtabs,DK):
            with dt:
                dim=irp.dimensions[dk]
                rows=""
                for code,ind in dim.indicators.items():
                    yr=f'<span class="ind-ya">{ind.data_year}</span>' if (ind.input_type=="api" and ind.data_year) else '<span class="ind-ym">Manual</span>'
                    if ind.score is not None:
                        shtml=f'<span class="ind-sc" style="color:{sc(ind.score)}">{ind.score:.1f}</span>'
                        bhtml=f'<div class="ind-bb"><div class="ind-bf" style="width:{int(ind.score)}%;background:{sc(ind.score)}"></div></div>'
                    else: shtml='<span class="ind-na">N/D</span>';bhtml='<div class="ind-bb"></div>'
                    rows+=f'<div class="ind-row"><span class="ind-code">{code}</span><span class="ind-name">{ind.name}</span>{yr}{shtml}{bhtml}</div>'
                ds=f"{dim.dimension_score:.1f}" if dim.dimension_score else "N/D"
                st.markdown(f'<div style="display:flex;justify-content:space-between;margin-bottom:.6rem;padding-bottom:.4rem;border-bottom:1px solid #E4E9F0;"><span style="font-size:.66rem;color:#98A6B5;">Cobertura: <strong style="color:{sc(dim.coverage_pct)}">{dim.coverage_pct:.0f}%</strong></span><span style="font-size:.66rem;color:#98A6B5;">Score: <strong style="color:{sc(dim.dimension_score)};font-family:\'DM Mono\'">{ds}</strong></span></div>{rows}',unsafe_allow_html=True)

    with t4:
        if len(st.session_state.analyses)<2:
            st.markdown('<p style="font-size:.80rem;color:#98A6B5;text-align:center;padding:2rem;">Ejecuta análisis de al menos 2 países para activar el comparador.</p>',unsafe_allow_html=True)
        else:
            comp=[]
            for k2,(ai,ae,_) in st.session_state.analyses.items():
                row={"País":ai.country,"Sector":SECTORS.get(ai.sector,""),"IRP":f"{ai.irp_score:.1f}" if ai.irp_score else "N/D","Viabilidad":rl(ai.risk_level)}
                for dk in DK:
                    d=ai.dimensions.get(dk)
                    row[ai.dimensions[dk].name.split(" ")[0]]=f"{d.dimension_score:.1f}" if d and d.dimension_score else "N/D"
                if ae: row["EFA"]=format_usd(ae.efa_usd); row["RAR"]=f"{ae.rar:.2f}x" if ae.rar else "—"
                comp.append(row)
            st.dataframe(pd.DataFrame(comp).set_index("País"),use_container_width=True)
        if st.button("Limpiar todos los análisis"):
            st.session_state.analyses={}; st.session_state.clicked_country=None; st.rerun()

st.markdown(f'<div style="text-align:center;padding:1rem 0 .3rem;font-size:.58rem;color:#2A4060;letter-spacing:.09em;text-transform:uppercase;">PolitRisk Pro &nbsp;·&nbsp; Political Risk & Market Entry Intelligence &nbsp;·&nbsp; {datetime.now().strftime("%B %Y")}</div>',unsafe_allow_html=True)
