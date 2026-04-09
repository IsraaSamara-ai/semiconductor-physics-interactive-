# ═══════════════════════════════════════════════════════════════════════
#  فيزياء أشباه الموصلات التفاعلية — Israa Samara
#  Interactive Semiconductor Physics
# ═══════════════════════════════════════════════════════════════════════

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import numpy as np

# ─── إعدادات الصفحة ─────────────────────────────────────────────────
st.set_page_config(
    page_title="فيزياء أشباه الموصلات التفاعلية | Israa Samara",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── تنسيقات CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
*{font-family:'Cairo',sans-serif;direction:rtl;}
.stApp{background:linear-gradient(180deg,#060612 0%,#0c0c24 50%,#0a0a1a 100%);color:#e0e0e0;}
.stSidebar{background:linear-gradient(180deg,#0d0d2b,#12123a);border-left:1px solid #00e5ff22;}
.stSidebar [data-testid="stSidebarNav"]{gap:2px;}
.section-card{background:linear-gradient(135deg,#111133 0%,#0a0a22 100%);
  border:1px solid #00e5ff18;border-radius:16px;padding:28px;margin:12px 0;
  box-shadow:0 0 30px #00e5ff08;}
.info-box{background:linear-gradient(135deg,#1a1a40,#0f0f2a);
  border-right:4px solid #00e5ff;border-radius:10px;padding:18px;margin:14px 0;}
.warn-box{background:linear-gradient(135deg,#2a1a10,#1a0f0a);
  border-right:4px solid #ff9800;border-radius:10px;padding:18px;margin:14px 0;}
.success-box{background:linear-gradient(135deg,#0a2a1a,#0a1a0f);
  border-right:4px solid #4caf50;border-radius:10px;padding:18px;margin:14px 0;}
h1,h2,h3{color:#00e5ff !important;text-shadow:0 0 20px #00e5ff33;}
.stSelectbox label,.stSlider label,.stRadio label{color:#b0b0d0 !important;font-weight:600;}
.stSelectbox>div>div{background:#1a1a3a !important;border-color:#00e5ff33 !important;color:#e0e0e0 !important;}
.stSlider>div>div>div{background:#1a1a3a !important;}
.css-1d391kg{background:#00e5ff !important;}
div[data-testid="stSidebar"]::-webkit-scrollbar{width:4px;}
div[data-testid="stSidebar"]::-webkit-scrollbar-thumb{background:#00e5ff44;border-radius:4px;}
</style>
""", unsafe_allow_html=True)

# ─── لوحة الاسم ─────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:22px 30px;
  background:linear-gradient(135deg,#0a0a1a 0%,#14143a 50%,#0a0a1a 100%);
  border-radius:18px;margin-bottom:18px;border:1px solid #00e5ff22;
  box-shadow:0 4px 40px #00e5ff10;">
  <h1 style="color:#00e5ff;font-size:2rem;margin:0;letter-spacing:1px;">
    ⚡ فيزياء أشباه الموصلات التفاعلية</h1>
  <p style="color:#8888bb;font-size:0.95rem;margin:6px 0 0;">
    تعلّم المفاهيم الأساسية للإلكترونيات بشكل مرئي وتفاعلي خطوة بخطوة</p>
  <p style="color:#ff6baa;font-size:1.15rem;margin:12px 0 0;font-weight:800;">
    ✦ Israa Samara ✦</p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
#  دوال الرسوم المتحركة (HTML/Canvas)
# ═══════════════════════════════════════════════════════════════════════

def html_lattice(temperature, material):
    """رسوم متحركة لبلورة السليكون مع تأثير الحرارة"""
    n_pairs = min(int(temperature / 8), 12)
    return f"""
    <div style="direction:rtl;text-align:center;font-family:Cairo,sans-serif;">
    <canvas id="lc" width="780" height="380"
      style="border-radius:12px;background:#08081a;border:1px solid #00e5ff15;display:block;margin:0 auto;"></canvas>
    <script>
    const cv=document.getElementById('lc'),cx=cv.getContext('2d');
    const np={n_pairs},mat="{material}";
    const atoms=[];
    for(let r=0;r<4;r++)for(let c=0;c<7;c++)
      atoms.push({x:65+c*105,y:55+r*90,vx:0,vy:0});
    const bonds=[];
    for(let r=0;r<4;r++)for(let c=0;c<7;c++){{
      const i=r*7+c;
      if(c<6)bonds.push([i,i+1]);
      if(r<3)bonds.push([i,i+7]);
    }}
    const broken=new Set();
    while(broken.size<np&&broken.size<bonds.length)
      broken.add(Math.floor(Math.random()*bonds.length));
    const elec=[],holes=[];
    broken.forEach(bi=>{{
      const b=bonds[bi];
      const mx=(atoms[b[0]].x+atoms[b[1]].x)/2;
      const my=(atoms[b[0]].y+atoms[b[1]].y)/2;
      elec.push({{x:mx+Math.random()*20-10,y:my+Math.random()*20-10,
        vx:(Math.random()-0.5)*2,vy:(Math.random()-0.5)*2}});
      holes.push({{x:mx-Math.random()*20+10,y:my-Math.random()*20+10,
        vx:(Math.random()-0.5)*0.5,vy:(Math.random()-0.5)*0.5}});
    }});
    function draw(){{
      cx.clearRect(0,0,780,380);
      bonds.forEach((b,i)=>{{
        const ok=!broken.has(i);
        cx.beginPath();cx.moveTo(atoms[b[0]].x,atoms[b[0]].y);
        cx.lineTo(atoms[b[1]].x,atoms[b[1]].y);
        cx.strokeStyle=ok?'#335577':'#552222';cx.lineWidth=ok?2:1;
        cx.setLineDash(ok?[]:[4,4]);cx.stroke();cx.setLineDash([]);
      }});
      atoms.forEach(a=>{{
        cx.beginPath();cx.arc(a.x,a.y,22,0,Math.PI*2);
        cx.fillStyle='#1a2a4a';cx.fill();
        cx.strokeStyle='#4488aa';cx.lineWidth=1.5;cx.stroke();
        cx.fillStyle='#6699bb';cx.font='bold 13px Cairo';
        cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(mat,a.x,a.y);
      }});
      elec.forEach(e=>{{
        e.x+=e.vx;e.y+=e.vy;
        if(e.x<10||e.x>770)e.vx*=-1;
        if(e.y<10||e.y>370)e.vy*=-1;
        cx.beginPath();cx.arc(e.x,e.y,5,0,Math.PI*2);
        cx.fillStyle='#00bbff';cx.fill();
        cx.shadowColor='#00bbff';cx.shadowBlur=8;
        cx.beginPath();cx.arc(e.x,e.y,5,0,Math.PI*2);cx.fill();
        cx.shadowBlur=0;
        cx.fillStyle='#ffffff';cx.font='9px Cairo';
        cx.fillText('e⁻',e.x,e.y-10);
      }});
      holes.forEach(h=>{{
        h.x+=h.vx;h.y+=h.vy;
        if(h.x<20||h.x>760)h.vx*=-1;
        if(h.y<20||h.y>360)h.vy*=-1;
        cx.beginPath();cx.arc(h.x,h.y,6,0,Math.PI*2);
        cx.strokeStyle='#ff4466';cx.lineWidth=2;cx.stroke();
        cx.fillStyle='#ff446622';cx.fill();
        cx.fillStyle='#ff6688';cx.font='bold 10px Cairo';
        cx.fillText('+',h.x,h.y+1);
        cx.fillStyle='#ff6688';cx.font='9px Cairo';
        cx.fillText('فجوة',h.x,h.y-11);
      }});
      cx.fillStyle='#667799';cx.font='12px Cairo';
      cx.textAlign='right';
      cx.fillText('إلكترون حر (أزرق) ←→ فجوة (أحمر)',760,370);
      if(np===0){{cx.fillStyle='#44aa66';cx.font='14px Cairo';cx.textAlign='center';
        cx.fillText('جميع الروابط التساهمية سليمة — لا توجد إلكترونات حرة',390,370);}}
    }}
    setInterval(draw,33);
    </script></div>"""


def html_doping(dtype, dopant):
    """رسوم متحركة للإشابة — النوع N أو P"""
    is_n = dtype == "n"
    dop_color = "#44cc44" if is_n else "#cc8800"
    dop_sym = dopant
    carrier_label = "إلكترون حر" if is_n else "فجوة"
    carrier_color = "#00bbff" if is_n else "#ff4466"
    majority = "الإلكترونات الحرة" if is_n else "الفجوات"
    minority = "الفجوات" if is_n else "الإلكترونات"
    n_majority = 8 if is_n else 8
    n_minority = 2 if is_n else 2

    carriers_js = ""
    for i in range(n_majority):
        sx = 100 + (i % 4) * 160
        sy = 80 + (i // 4) * 180
        if is_n:
            carriers_js += f"""
            elec.push({{x:{sx},y:{sy},vx:(Math.random()-0.5)*2.5,vy:(Math.random()-0.5)*2.5}});"""
        else:
            carriers_js += f"""
            holes.push({{x:{sx},y:{sy},vx:(Math.random()-0.5)*0.7,vy:(Math.random()-0.5)*0.7}});"""
    for i in range(n_minority):
        sx = 300 + i * 120
        sy = 130
        if is_n:
            carriers_js += f"""
            holes.push({{x:{sx},y:{sy},vx:(Math.random()-0.5)*0.5,vy:(Math.random()-0.5)*0.5}});"""
        else:
            carriers_js += f"""
            elec.push({{x:{sx},y:{sy},vx:(Math.random()-0.5)*2,vy:(Math.random()-0.5)*2}});"""

    return f"""
    <div style="direction:rtl;text-align:center;font-family:Cairo,sans-serif;">
    <canvas id="dc" width="780" height="380"
      style="border-radius:12px;background:#08081a;border:1px solid #00e5ff15;display:block;margin:0 auto;"></canvas>
    <script>
    const cv=document.getElementById('dc'),cx=cv.getContext('2d');
    const atoms=[];
    const dopPositions=[{{x:260,y:145}},{{x:470,y:145}},{{x:365,y:250}}];
    for(let r=0;r<4;r++)for(let c=0;c<7;c++){{
      let isDop=false;
      dopPositions.forEach(d=>{{if(Math.abs(d.x-(65+c*105))<30&&Math.abs(d.y-(55+r*90))<30)isDop=true;}});
      atoms.push({{x:65+c*105,y:55+r*90,dop:isDop}});
    }}
    const elec=[],holes=[];
    {carriers_js}
    function draw(){{
      cx.clearRect(0,0,780,380);
      cx.fillStyle='{"#0a1030" if is_n else "#1a0a00"}';
      cx.fillRect(0,0,780,380);
      cx.fillStyle='{"#00113366" if is_n else "#33110066"}';
      cx.font='bold 28px Cairo';cx.textAlign='center';
      cx.fillText('{"نوع N (سالبة)" if is_n else "نوع P (موجبة)"}',390,35);
      for(let r=0;r<4;r++)for(let c=0;c<7;c++){{
        const i=r*7+c,a=atoms[i];
        cx.beginPath();cx.arc(a.x,a.y,22,0,Math.PI*2);
        if(a.dop){{cx.fillStyle='#1a3a1a';cx.strokeStyle='{dop_color}';}}
        else{{cx.fillStyle='#1a2a4a';cx.strokeStyle='#4488aa';}}
        cx.fill();cx.lineWidth=1.5;cx.stroke();
        cx.fillStyle=a.dop?'{dop_color}':'#6699bb';
        cx.font='bold 12px Cairo';cx.textAlign='center';cx.textBaseline='middle';
        cx.fillText(a.dop?'{dop_sym}':'Si',a.x,a.y);
      }}
      elec.forEach(e=>{{
        e.x+=e.vx;e.y+=e.vy;
        if(e.x<10||e.x>770)e.vx*=-1;if(e.y<10||e.y>370)e.vy*=-1;
        cx.beginPath();cx.arc(e.x,e.y,5,0,Math.PI*2);
        cx.fillStyle='#00bbff';cx.fill();
        cx.shadowColor='#00bbff';cx.shadowBlur=6;
        cx.beginPath();cx.arc(e.x,e.y,5,0,Math.PI*2);cx.fill();
        cx.shadowBlur=0;
      }});
      holes.forEach(h=>{{
        h.x+=h.vx;h.y+=h.vy;
        if(h.x<20||h.x>760)h.vx*=-1;if(h.y<20||h.y>360)h.vy*=-1;
        cx.beginPath();cx.arc(h.x,h.y,6,0,Math.PI*2);
        cx.strokeStyle='#ff4466';cx.lineWidth=2;cx.stroke();
        cx.fillStyle='#ff446622';cx.fill();
        cx.fillStyle='#ff6688';cx.font='bold 10px Cairo';
        cx.textAlign='center';cx.textBaseline='middle';cx.fillText('+',h.x,h.y+1);
      }});
      cx.fillStyle='#8899aa';cx.font='11px Cairo';cx.textAlign='right';
      cx.fillText('🔵 إلكترون حر    🔴 فجوة    🟢 ذرة مشابة',770,372);
      cx.fillStyle='{carrier_color}';cx.font='bold 13px Cairo';cx.textAlign='left';
      cx.fillText('الناقلات الأغلبية: {majority}',15,372);
      cx.fillStyle='#888';cx.font='11px Cairo';
      cx.fillText('الناقلات الأقلية: {minority}',15,355);
    }}
    setInterval(draw,33);
    </script></div>"""


def html_pn_junction():
    """رسوم متحركة لوصلة PN ومنطقة الاستنزاف"""
    return """
    <div style="direction:rtl;text-align:center;font-family:Cairo,sans-serif;">
    <canvas id="pn" width="780" height="400"
      style="border-radius:12px;background:#08081a;border:1px solid #00e5ff15;display:block;margin:0 auto;"></canvas>
    <script>
    const cv=document.getElementById('pn'),cx=cv.getContext('2d');
    let t=0;
    const fixedElec=[],fixedHoles=[];
    for(let i=0;i<5;i++)fixedElec.push({x:310+i*18,y:120+Math.random()*160});
    for(let i=0;i<5;i++)fixedHoles.push({x:450-i*18,y:120+Math.random()*160});
    const moveElec=[],moveHoles=[];
    function spawnCarrier(){{
      if(moveElec.length<4)moveElec.push({x:680,y:100+Math.random()*200,vx:-1.2,vy:0,alpha:1});
      if(moveHoles.length<4)moveHoles.push({x:100,y:100+Math.random()*200,vx:1.0,vy:0,alpha:1});
    }}
    function draw(){{
      t+=0.02;
      cx.clearRect(0,0,780,400);
      // P region
      cx.fillStyle='#1a0a0a';cx.fillRect(0,50,370,300);
      cx.fillStyle='#ff446622';cx.fillRect(0,50,370,300);
      // N region
      cx.fillStyle='#0a0a1a';cx.fillRect(410,50,370,300);
      cx.fillStyle='#00bbff15';cx.fillRect(410,50,370,300);
      // Depletion
      const dw=50+10*Math.sin(t*0.5);
      cx.fillStyle='#0a0a0a';
      cx.fillRect(390-dw/2,50,dw,300);
      cx.fillStyle='#33221188';
      for(let i=0;i<fixedElec.length;i++){{
        const ex=380-dw/2+10+i*8;
        cx.fillStyle='#00bbff';cx.font='bold 14px Cairo';
        cx.textAlign='center';cx.fillText('-',ex,fixedElec[i].y);
      }}
      for(let i=0;i<fixedHoles.length;i++){{
        const hx=400+dw/2-10-i*8;
        cx.fillStyle='#ff4466';cx.font='bold 14px Cairo';
        cx.textAlign='center';cx.fillText('+',hx,fixedHoles[i].y);
      }}
      // Labels
      cx.font='bold 20px Cairo';cx.textAlign='center';
      cx.fillStyle='#ff6688';cx.fillText('نوع P (موجبة)',185,85);
      cx.fillStyle='#66bbff';cx.fillText('نوع N (سالبة)',595,85);
      cx.fillStyle='#aa8855';cx.fillText('منطقة الاستنزاف',390,85);
      // Anode / Cathode
      cx.fillStyle='#ff8888';cx.font='14px Cairo';
      cx.textAlign='right';cx.fillText('المصعد (Anode) →',360,375);
      cx.fillStyle='#88bbff';cx.textAlign='left';
      cx.fillText('← المهبط (Cathode)',420,375);
      // Moving carriers
      if(Math.random()<0.03)spawnCarrier();
      moveElec.forEach((e,i)=>{{
        e.x+=e.vx;
        if(e.x<390-dw/2){{e.alpha-=0.05;}}
        if(e.alpha<=0||e.x<360)moveElec.splice(i,1);
        else{{cx.globalAlpha=e.alpha;cx.beginPath();cx.arc(e.x,e.y,4,0,Math.PI*2);
        cx.fillStyle='#00bbff';cx.fill();cx.shadowColor='#00bbff';cx.shadowBlur=6;
        cx.beginPath();cx.arc(e.x,e.y,4,0,Math.PI*2);cx.fill();cx.shadowBlur=0;cx.globalAlpha=1;}}
      }});
      moveHoles.forEach((h,i)=>{{
        h.x+=h.vx;
        if(h.x>390+dw/2){{h.alpha-=0.05;}}
        if(h.alpha<=0||h.x>420)moveHoles.splice(i,1);
        else{{cx.globalAlpha=h.alpha;cx.beginPath();cx.arc(h.x,h.y,5,0,Math.PI*2);
        cx.strokeStyle='#ff4466';cx.lineWidth=2;cx.stroke();cx.globalAlpha=1;}}
      }});
      // Electric field arrow
      cx.strokeStyle='#ffaa33';cx.lineWidth=2;cx.setLineDash([4,3]);
      cx.beginPath();cx.moveTo(390-dw/2+5,200);cx.lineTo(390+dw/2-5,200);cx.stroke();
      cx.setLineDash([]);
      cx.fillStyle='#ffaa33';cx.font='11px Cairo';cx.textAlign='center';
      cx.fillText('E⃗ (مجال كهربائي داخلي)',390,220);
      // Legend
      cx.fillStyle='#778899';cx.font='11px Cairo';cx.textAlign='right';
      cx.fillText('تنتشر الإلكترونات من N→P وتتوقف عند منطقة الاستنزاف',770,395);
    }}
    setInterval(draw,33);
    </script></div>"""


def html_bias_circuit(bias_type, voltage, material):
    """رسوم متحركة لدارة الانحياز مع حركة التيار"""
    barrier = 0.7 if material == "Si" else 0.3
    is_forward = bias_type == "forward"
    is_conducting = is_forward and voltage > barrier

    speed = 0
    if is_forward:
        if voltage > barrier:
            speed = min((voltage - barrier) * 3, 5)
        else:
            speed = 0.05
    else:
        speed = 0

    depletion_w = 60
    if is_forward:
        depletion_w = max(10, 60 - (voltage / barrier) * 50) if voltage <= barrier else 8
    else:
        depletion_w = min(60 + voltage * 5, 130)

    color_main = "#00e5ff" if is_conducting else "#555577"
    bulb_glow = 1.0 if is_conducting else 0.0

    return f"""
    <div style="direction:rtl;text-align:center;font-family:Cairo,sans-serif;">
    <canvas id="bc" width="780" height="480"
      style="border-radius:12px;background:#08081a;border:1px solid #00e5ff15;display:block;margin:0 auto;"></canvas>
    <script>
    const cv=document.getElementById('bc'),cx=cv.getContext('2d');
    let t=0;const spd={speed};const dw={depletion_w};const glow={bulb_glow};
    const isF={str(is_forward).lower()};const v={voltage};const bar={barrier};
    // Circuit path points (clockwise from battery +)
    const path=[{{x:120,y:100}},{{x:120,y:240}},{{x:300,y:240}},
      {{x:480,y:240}},{{x:660,y:240}},{{x:660,y:100}},{{x:390,y:100}},{{x:120,y:100}}];
    const dots=[];
    for(let i=0;i<20;i++){{
      dots.push({{pos:i/20,speed:spd*0.004+Math.random()*0.001}});
    }}
    function draw(){{
      t+=0.02;cx.clearRect(0,0,780,480);
      // Title
      cx.fillStyle=isF?'#00e5ff':'#ff6644';
      cx.font='bold 18px Cairo';cx.textAlign='center';
      cx.fillText(isF?'انحياز أمامي (Forward Bias)':'انحياز عكسي (Reverse Bias)',390,35);
      // Wires
      cx.strokeStyle=spd>0.1?'#00e5ff66':'#333355';
      cx.lineWidth=3;cx.beginPath();
      cx.moveTo(120,100);cx.lineTo(120,240);cx.lineTo(300,240);
      cx.moveTo(480,240);cx.lineTo(660,240);cx.lineTo(660,100);cx.lineTo(390,100);
      cx.stroke();
      // Battery
      cx.strokeStyle='#ffaa33';cx.lineWidth=2;
      cx.beginPath();cx.moveTo(120,105);cx.lineTo(120,155);cx.stroke();
      cx.beginPath();cx.moveTo(108,115);cx.lineTo(132,115);cx.stroke();
      cx.beginPath();cx.moveTo(113,125);cx.lineTo(127,125);cx.stroke();
      cx.beginPath();cx.moveTo(108,140);cx.lineTo(132,140);cx.stroke();
      cx.fillStyle='#ff4444';cx.font='bold 16px Cairo';cx.textAlign='center';
      cx.fillText('+',120,108);
      cx.fillStyle='#4444ff';cx.fillText('−',120,165);
      cx.fillStyle='#ccaa44';cx.font='12px Cairo';cx.fillText(v+' V',90,135);
      // Resistor
      cx.strokeStyle='#aa8844';cx.lineWidth=2;
      cx.beginPath();cx.moveTo(300,240);
      for(let i=0;i<6;i++){{cx.lineTo(310+i*20,240+(i%2===0?-12:12));}}
      cx.lineTo(420,240);cx.stroke();
      cx.fillStyle='#aa8844';cx.font='11px Cairo';cx.fillText('R',360,265);
      // Diode symbol
      const dx=390,dy=240;
      cx.fillStyle='#1a1a3a';cx.fillRect(dx-50,dy-25,100,50);
      cx.strokeStyle='#00e5ff55';cx.strokeRect(dx-50,dy-25,100,50);
      // Triangle
      cx.beginPath();
      if(isF){{cx.moveTo(dx-20,dy-15);cx.lineTo(dx+15,dy);cx.lineTo(dx-20,dy+15);cx.closePath();}}
      else{{cx.moveTo(dx+20,dy-15);cx.lineTo(dx-15,dy);cx.lineTo(dx+20,dy+15);cx.closePath();}}
      cx.fillStyle=spd>0.1?'#00e5ff44':'#333344';cx.fill();
      cx.strokeStyle='#00e5ff';cx.lineWidth=2;cx.stroke();
      // Line at cathode
      cx.beginPath();cx.moveTo(isF?dx+15:dx-15,dy-15);cx.lineTo(isF?dx+15:dx-15,dy+15);
      cx.strokeStyle='#00e5ff';cx.lineWidth=2.5;cx.stroke();
      cx.fillStyle='#778899';cx.font='10px Cairo';
      cx.fillText('ثنائي بلوري',dx,dy+40);
      // Depletion region indicator
      cx.fillStyle='#332211';cx.globalAlpha=0.6;
      cx.fillRect(dx-dw/2,dy-22,dw,44);cx.globalAlpha=1;
      cx.fillStyle='#886633';cx.font='9px Cairo';
      if(dw>20)cx.fillText('استنزاف',dx,dy+3);
      // Light bulb
      const bx=390,by=100;
      cx.beginPath();cx.arc(bx,by,18,0,Math.PI*2);
      if(glow>0.5){{cx.fillStyle='rgba(255,230,100,'+(0.3+0.4*Math.sin(t*5))+')';cx.fill();
        cx.shadowColor='#ffdd44';cx.shadowBlur=30;}}
      cx.beginPath();cx.arc(bx,by,18,0,Math.PI*2);
      cx.strokeStyle='#aa8844';cx.lineWidth=2;cx.stroke();cx.shadowBlur=0;
      cx.fillStyle=glow>0.5?'#ffee88':'#444444';cx.font='14px Cairo';cx.textAlign='center';
      cx.fillText('💡',bx,by+5);
      // Ammeter
      cx.beginPath();cx.arc(540,240,18,0,Math.PI*2);
      cx.fillStyle='#1a1a3a';cx.fill();cx.strokeStyle='#44aa44';cx.lineWidth=2;cx.stroke();
      cx.fillStyle='#44aa44';cx.font='bold 14px Cairo';cx.fillText('A',540,245);
      // Current dots
      if(spd>0.05){{
        dots.forEach(d=>{{
          d.pos+=d.speed;if(d.pos>1)d.pos-=1;
          const totalLen=path.reduce((s,p,i)=>{{
            if(i===0)return 0;const prev=path[i-1];
            return s+Math.sqrt((p.x-prev.x)**2+(p.y-prev.y)**2);
          }},0);
          let target=d.pos*totalLen,accum=0,px=path[0].x,py=path[0].y;
          for(let i=1;i<path.length;i++){{
            const prev=path[i-1],cur=path[i];
            const seg=Math.sqrt((cur.x-prev.x)**2+(cur.y-prev.y)**2);
            if(accum+seg>=target){{
              const frac=(target-accum)/seg;
              px=prev.x+frac*(cur.x-prev.x);py=prev.y+frac*(cur.y-prev.y);break;
            }}accum+=seg;
          }}
          cx.beginPath();cx.arc(px,py,4,0,Math.PI*2);
          cx.fillStyle='#00e5ff';cx.fill();
          cx.shadowColor='#00e5ff';cx.shadowBlur=8;
          cx.beginPath();cx.arc(px,py,4,0,Math.PI*2);cx.fill();cx.shadowBlur=0;
        }});
      }}
      // Status
      cx.fillStyle='#888';cx.font='12px Cairo';cx.textAlign='center';
      if(isF){{
        if(v>bar)cx.fillText('✅ التيار يسري — المصباح يضيء',390,460);
        else cx.fillText('⚠️ الجهد أقل من حاجز الجهد ('+bar+' V) — تيار ضعيف جداً',390,460);
      }}else{{
        cx.fillText('❌ الثنائي يحظر مرور التيار — المصباح مطفأ',390,460);
      }}
    }}
    setInterval(draw,33);
    </script></div>"""


def html_rectifier(voltage, frequency):
    """رسوم متحركة لمقوّم نصف الموجة مع الإشارة الداخلة والخارجة"""
    return f"""
    <div style="direction:rtl;text-align:center;font-family:Cairo,sans-serif;">
    <canvas id="rc" width="780" height="520"
      style="border-radius:12px;background:#08081a;border:1px solid #00e5ff15;display:block;margin:0 auto;"></canvas>
    <script>
    const cv=document.getElementById('rc'),cx=cv.getContext('2d');
    let t=0;const vmax={voltage};const freq={frequency};
    const omega=2*Math.PI*freq;
    const dots=[];
    for(let i=0;i<12;i++)dots.push({{pos:i/12}});
    function draw(){{
      t+=0.016;cx.clearRect(0,0,780,520);
      // Title
      cx.fillStyle='#00e5ff';cx.font='bold 16px Cairo';cx.textAlign='center';
      cx.fillText('الثنائي البلوري مقوّماً للتيار المتردد (نصف موجة)',390,25);
      // === Input waveform ===
      cx.strokeStyle='#335577';cx.lineWidth=1;cx.strokeRect(40,50,340,120);
      cx.fillStyle='#8899aa';cx.font='11px Cairo';cx.textAlign='center';
      cx.fillText('الإشارة الداخلة (تيار متردد)',210,45);
      // Axes
      cx.strokeStyle='#445566';cx.lineWidth=1;
      cx.beginPath();cx.moveTo(40,110);cx.lineTo(380,110);cx.stroke();
      cx.beginPath();cx.moveTo(210,50);cx.lineTo(210,170);cx.stroke();
      cx.fillStyle='#667788';cx.font='9px Cairo';cx.textAlign='right';
      cx.fillText('+V',38,75);cx.fillText('−V',38,155);cx.fillText('0',38,113);
      cx.fillText('t',382,113);
      // Sine wave
      cx.beginPath();cx.strokeStyle='#44aaff';cx.lineWidth=2;
      for(let px=0;px<340;px++){{
        const tt=t+px/340*2/freq;
        const v=vmax*Math.sin(omega*tt);
        const sy=110-v/vmax*50;
        if(px===0)cx.moveTo(40+px,sy);else cx.lineTo(40+px,sy);
      }}cx.stroke();
      // Scanning line
      const scanX=((t*freq*0.5)%1)*340;
      cx.strokeStyle='#ffffff33';cx.lineWidth=1;
      cx.beginPath();cx.moveTo(40+scanX,50);cx.lineTo(40+scanX,170);cx.stroke();
      const scanT=t+scanX/340*2/freq;
      const scanV=vmax*Math.sin(omega*scanT);
      // === Circuit in middle ===
      cx.strokeStyle='#335577';cx.strokeRect(40,185,700,80);
      cx.fillStyle='#8899aa';cx.font='11px Cairo';cx.textAlign='center';
      cx.fillText('الدارة: مصدر متردد → ثنائي بلوري → مقاومة (حمل)',390,200);
      // Simple circuit
      const cy=235;
      cx.strokeStyle=scanV>0?'#00e5ff66':'#333355';cx.lineWidth=2;
      cx.beginPath();cx.moveTo(100,cy);cx.lineTo(250,cy);cx.stroke();
      cx.beginPath();cx.moveTo(350,cy);cx.lineTo(500,cy);cx.stroke();
      // AC source
      cx.beginPath();cx.arc(100,cy,20,0,Math.PI*2);
      cx.strokeStyle='#ffaa33';cx.lineWidth=2;cx.stroke();
      cx.fillStyle='#ffaa33';cx.font='14px Cairo';cx.fillText('∼',100,cy+5);
      // Diode
      cx.beginPath();cx.moveTo(260,cy-12);cx.lineTo(285,cy);cx.lineTo(260,cy+12);cx.closePath();
      cx.fillStyle=scanV>0?'#00e5ff44':'#333344';cx.fill();
      cx.strokeStyle=scanV>0?'#00e5ff':'#555577';cx.lineWidth=2;cx.stroke();
      cx.beginPath();cx.moveTo(285,cy-12);cx.lineTo(285,cy+12);
      cx.strokeStyle=scanV>0?'#00e5ff':'#555577';cx.stroke();
      cx.fillStyle='#778899';cx.font='10px Cairo';cx.fillText('ثنائي',272,cy-20);
      // Resistor
      cx.strokeStyle='#aa8844';cx.lineWidth=2;
      cx.beginPath();cx.moveTo(500,cy);
      for(let i=0;i<6;i++)cx.lineTo(510+i*12,cy+(i%2===0?-8:8));
      cx.lineTo(580,cy);cx.stroke();
      cx.fillStyle='#aa8844';cx.font='10px Cairo';cx.fillText('R',540,cy-15);
      // Status
      if(scanV>0){{
        cx.fillStyle='#44ff88';cx.font='bold 12px Cairo';cx.fillText('انحياز أمامي ✅ التيار يمر',390,cy+30);
        // Moving dots
        dots.forEach(d=>{{
          d.pos+=0.008;if(d.pos>1)d.pos-=1;
          const dx=120+d.pos*440;cx.beginPath();cx.arc(dx,cy,3,0,Math.PI*2);
          cx.fillStyle='#00e5ff';cx.fill();
        }});
      }}else{{
        cx.fillStyle='#ff4444';cx.font='bold 12px Cairo';cx.fillText('انحياز عكسي ❌ التيار محظور',390,cy+30);
      }}
      // === Output waveform ===
      cx.strokeStyle='#335577';cx.lineWidth=1;cx.strokeRect(40,280,340,120);
      cx.fillStyle='#8899aa';cx.font='11px Cairo';cx.textAlign='center';
      cx.fillText('الإشارة الخارجة (نصف موجية)',210,275);
      cx.strokeStyle='#445566';cx.lineWidth=1;
      cx.beginPath();cx.moveTo(40,340);cx.lineTo(380,340);cx.stroke();
      cx.beginPath();cx.moveTo(210,280);cx.lineTo(210,400);cx.stroke();
      cx.fillStyle='#667788';cx.font='9px Cairo';cx.textAlign='right';
      cx.fillText('+V',38,305);cx.fillText('0',38,343);
      // Half wave
      cx.beginPath();cx.strokeStyle='#44ff88';cx.lineWidth=2;
      for(let px=0;px<340;px++){{
        const tt=t+px/340*2/freq;
        const v=vmax*Math.sin(omega*tt);
        const sy=v>0?340-v/vmax*50:340;
        if(px===0)cx.moveTo(40+px,sy);else cx.lineTo(40+px,sy);
      }}cx.stroke();
      // Scan line on output
      cx.strokeStyle='#ffffff33';cx.lineWidth=1;
      cx.beginPath();cx.moveTo(40+scanX,280);cx.lineTo(40+scanX,400);cx.stroke();
      // === Explanation panel ===
      cx.fillStyle='#111133';cx.strokeStyle='#00e5ff22';cx.lineWidth=1;
      cx.beginPath();cx.roundRect(410,280,340,120,10);cx.fill();cx.stroke();
      cx.fillStyle='#aabbcc';cx.font='11px Cairo';cx.textAlign='right';
      const halfV=(vmax/1.414).toFixed(1);
      cx.fillText('النصف الموجب (جهد > 0):',740,300);
      cx.fillStyle='#44ff88';cx.fillText('→ انحياز أمامي، التيار يمر',740,318);
      cx.fillStyle='#aabbcc';cx.fillText('النصف السالب (جهد < 0):',740,340);
      cx.fillStyle='#ff4444';cx.fillText('→ انحياز عكسي، التيار محظور',740,358);
      cx.fillStyle='#ffaa44';cx.fillText('القيمة الفعّالة ≈ '+halfV+' V',740,385);
      // Bottom note
      cx.fillStyle='#667788';cx.font='11px Cairo';cx.textAlign='center';
      cx.fillText('النتيجة: تيار متردد يتحول إلى تيار pulsating في اتجاه واحد فقط',390,500);
    }}
    setInterval(draw,16);
    </script></div>"""


# ═══════════════════════════════════════════════════════════════════════
#  دوال الرسوم البيانية (Plotly)
# ═══════════════════════════════════════════════════════════════════════

def plot_band_gap(material):
    """مخطط نطاقات الطاقة يوضح الفجوة"""
    if material == "Si":
        eg, ev, ec = 1.12, 0, 1.12
        color_fill = "rgba(0,180,255,0.15)"
        color_line = "#00b4ff"
    else:
        eg, ev, ec = 0.67, 0, 0.67
        color_fill = "rgba(255,150,0,0.15)"
        color_line = "#ff9600"

    fig = go.Figure()
    # Valence band
    fig.add_trace(go.Scatter(
        x=[-1, 0, 1, 2, 3, 4, 5], y=[-0.3, -0.1, 0, 0, 0, -0.1, -0.3],
        fill='tozeroy', fillcolor='rgba(255,70,100,0.2)',
        line=dict(color='#ff4466', width=2), name='نطاق التكافؤ'
    ))
    # Conduction band
    fig.add_trace(go.Scatter(
        x=[-1, 0, 1, 2, 3, 4, 5],
        y=[ec + 0.3, ec + 0.1, ec, ec, ec, ec + 0.1, ec + 0.3],
        fill='tozeroy', fillcolor=color_fill,
        line=dict(color=color_line, width=2), name='نطاق التوصيل'
    ))
    # Gap arrow
    fig.add_annotation(x=2.5, y=ec / 2, text=f'الفجوة = {eg} eV',
                       font=dict(size=16, color='#ffcc00', family='Cairo'),
                       showarrow=True, arrowhead=2, ax=60, ay=0)
    # Labels
    fig.add_annotation(x=0.5, y=-0.2, text='نطاق التكافؤ<br>(فجوات)',
                       font=dict(size=13, color='#ff6688', family='Cairo'), showarrow=False)
    fig.add_annotation(x=0.5, y=ec + 0.2, text='نطاق التوصيل<br>(إلكترونات حرة)',
                       font=dict(size=13, color=color_line, family='Cairo'), showarrow=False)
    # Electron dot
    fig.add_trace(go.Scatter(
        x=[3], y=[ec + 0.05], mode='markers+text',
        marker=dict(size=14, color='#00e5ff', symbol='circle'),
        text=['e⁻'], textposition='top center',
        textfont=dict(size=12, color='#00e5ff'), showlegend=False
    ))
    # Hole dot
    fig.add_trace(go.Scatter(
        x=[3.5], y=[-0.05], mode='markers+text',
        marker=dict(size=14, color='#ff4466', symbol='circle-open', line=dict(width=2)),
        text=['فجوة'], textposition='bottom center',
        textfont=dict(size=11, color='#ff4466'), showlegend=False
    ))

    mat_name = "السليكون (Si)" if material == "Si" else "الجرمانيوم (Ge)"
    fig.update_layout(
        title=dict(text=f'مخطط نطاقات الطاقة — {mat_name}', font=dict(size=18, color='#00e5ff', family='Cairo')),
        plot_bgcolor='#0a0a1a', paper_bgcolor='#0a0a1a',
        xaxis=dict(showgrid=False, visible=False, range=[-0.5, 5.5]),
        yaxis=dict(showgrid=False, visible=False, range=[-0.5, ec + 0.5]),
        height=350, margin=dict(t=60, b=30, l=30, r=30),
        font=dict(family='Cairo', color='#aaa')
    )
    return fig


def plot_iv_curve(material, v_point=0):
    """منحنى العلاقة بين التيار والجهد للثنائي البلوري"""
    barrier = 0.7 if material == "Si" else 0.3
    Is = 1e-9  # Saturated reverse current
    Vt = 0.026  # Thermal voltage at room temp

    # Forward
    vf = np.linspace(0, 1.2, 300)
    If = Is * (np.exp(vf / Vt) - 1)
    If_ma = If * 1000  # Convert to mA
    If_ma = np.clip(If_ma, 0, 100)

    # Reverse
    vr = np.linspace(0, -20, 200)
    Ir = Is * (np.exp(vr / Vt) - 1)
    Ir_ua = Ir * 1e6  # Convert to µA
    Ir_ua = np.clip(Ir_ua, -5, 0)

    mat_name = "السليكون (Si)" if material == "Si" else "الجرمانيوم (Ge)"
    color_f = '#00e5ff' if material == 'Si' else '#ff9600'

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=vf, y=If_ma, mode='lines',
        line=dict(color=color_f, width=2.5),
        name=f'انحياز أمامي ({mat_name})'
    ))
    fig.add_trace(go.Scatter(
        x=vr, y=Ir_ua, mode='lines',
        line=dict(color='#ff4466', width=2, dash='dash'),
        name='انحياز عكسي'
    ))

    # Barrier voltage marker
    fig.add_vline(x=barrier, line_dash='dot', line_color='#ffcc00', line_width=1.5)
    fig.add_annotation(x=barrier, y=max(If_ma) * 0.5,
                       text=f'حاجز الجهد = {barrier} V',
                       font=dict(size=13, color='#ffcc00', family='Cairo'),
                       showarrow=True, arrowhead=1, ax=-80, ay=0)

    # Interactive point
    if v_point >= 0:
        i_at_v = Is * (np.exp(min(v_point, 1.2) / Vt) - 1) * 1000
        i_at_v = min(i_at_v, 100)
        fig.add_trace(go.Scatter(
            x=[v_point], y=[i_at_v], mode='markers+text',
            marker=dict(size=12, color='#ffffff', symbol='diamond'),
            text=[f'({v_point:.1f}V, {i_at_v:.1f}mA)'],
            textposition='top left', textfont=dict(size=11, color='#ffffff', family='Cairo'),
            showlegend=False
        ))
    elif v_point < 0:
        i_at_v = Is * (np.exp(max(v_point, -20) / Vt) - 1) * 1e6
        fig.add_trace(go.Scatter(
            x=[v_point], y=[i_at_v], mode='markers+text',
            marker=dict(size=12, color='#ffffff', symbol='diamond'),
            text=[f'({v_point:.1f}V, {i_at_v:.2f}µA)'],
            textposition='bottom left', textfont=dict(size=11, color='#ffffff', family='Cairo'),
            showlegend=False
        ))

    fig.update_layout(
        title=dict(text=f'منحنى (I-V) للثنائي البلوري — {mat_name}', font=dict(size=18, color='#00e5ff', family='Cairo')),
        plot_bgcolor='#0a0a1a', paper_bgcolor='#0a0a1a',
        xaxis=dict(title=dict(text='فرق الجهد (V)', font=dict(size=13, color='#aaa', family='Cairo')),
                   gridcolor='#1a1a3a', zerolinecolor='#333355', range=[-15, 1.5],
                   titlefont=dict(family='Cairo')),
        yaxis=dict(title=dict(text='التيار', font=dict(size=13, color='#aaa', family='Cairo')),
                   gridcolor='#1a1a3a', zerolinecolor='#333355',
                   titlefont=dict(family='Cairo')),
        height=420, margin=dict(t=60, b=60, l=60, r=40),
        legend=dict(font=dict(size=12, family='Cairo', color='#aaa'), bgcolor='#0a0a1a88'),
        font=dict(family='Cairo', color='#aaa')
    )
    return fig


def plot_ac_rectified(vmax, freq):
    """مخطط التيار المتردد قبل وبعد التقويم"""
    t = np.linspace(0, 3 / freq, 1000)
    v_in = vmax * np.sin(2 * np.pi * freq * t)
    v_out = np.where(v_in > 0, v_in, 0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t * 1000, y=v_in, mode='lines',
        line=dict(color='#4488ff', width=2),
        name='الإشارة الداخلة (متردد)'
    ))
    fig.add_trace(go.Scatter(
        x=t * 1000, y=v_out, mode='lines',
        line=dict(color='#44ff88', width=2.5),
        name='الإشارة الخارجة (نصف موجية)'
    ))
    # Fill the blocked part
    fig.add_trace(go.Scatter(
        x=t * 1000, y=np.where(v_in < 0, v_in, 0), mode='lines',
        line=dict(color='#ff446644', width=1.5, dash='dot'),
        fill='tozeroy', fillcolor='rgba(255,68,100,0.1)',
        name='الجزء المحظور'
    ))
    # Barrier line
    fig.add_hline(y=0, line_dash='dot', line_color='#555577', line_width=1)

    v_rms = vmax / np.sqrt(2)
    fig.update_layout(
        title=dict(text=f'مقوّم نصف موجة — Vmax={vmax}V, f={freq}Hz, Vrms≈{v_rms:.1f}V',
                   font=dict(size=16, color='#00e5ff', family='Cairo')),
        plot_bgcolor='#0a0a1a', paper_bgcolor='#0a0a1a',
        xaxis=dict(title=dict(text='الزمن (ms)', font=dict(size=13, color='#aaa', family='Cairo')),
                   gridcolor='#1a1a3a', zerolinecolor='#333355', titlefont=dict(family='Cairo')),
        yaxis=dict(title=dict(text='الجهد (V)', font=dict(size=13, color='#aaa', family='Cairo')),
                   gridcolor='#1a1a3a', zerolinecolor='#333355',
                   range=[-vmax * 1.2, vmax * 1.2], titlefont=dict(family='Cairo')),
        height=380, margin=dict(t=60, b=50, l=60, r=40),
        legend=dict(font=dict(size=12, family='Cairo', color='#aaa'), bgcolor='#0a0a1a88'),
        font=dict(family='Cairo', color='#aaa')
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════
#  شريط جانبي للتنقل
# ═══════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:15px;margin-bottom:10px;
      background:linear-gradient(135deg,#1a1a4a,#0a0a2a);border-radius:12px;border:1px solid #00e5ff22;">
      <p style="color:#ff6baa;font-weight:800;font-size:1rem;margin:0;">Israa Samara</p>
      <p style="color:#556;font-size:0.8rem;margin:4px 0 0;">فيزياء أشباه الموصلات</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    page = st.radio("📚 اختر الموضوع:", [
        "🏠 المقدمة",
        "🔬 المواد وشبه الموصلات",
        "🕳️ الفجوة الطاقية (Band Gap)",
        "➕ النوع N والنوع P",
        "⚡ الثنائي البلوري (PN Junction)",
        "🔋 الانحياز الأمامي",
        "🔄 الانحياز العكسي",
        "📏 مقاومة الثنائي البلوري",
        "🔌 الثنائي مقوّم للتيار المتردد",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.caption("💡 حرّك الأدوات التفاعلية في كل قسم لمشاهدة التغييرات بصرياً")


# ═══════════════════════════════════════════════════════════════════════
#  محتوى الأقسام
# ═══════════════════════════════════════════════════════════════════════

# ─── 1. المقدمة ─────────────────────────────────────────────────────
if page == "🏠 المقدمة":
    st.markdown("""
    <div class="section-card">
    <h2>مرحباً بك في عالم أشباه الموصلات! 🌟</h2>
    <p style="font-size:1.05rem;line-height:2;color:#bbc;">
    هل تساءلت يوماً كيف يعمل هاتفك المحمول؟ أو كيف يُحوَّل التيار المتردد من المقابس الجدارية
    إلى تيار مستمر يشغّل حاسوبك؟ الجواب يكمن في <strong style="color:#00e5ff;">أشباه الموصلات</strong> —
    المواد التي غيّرت وجه التكنولوجيا الحديثة.
    </p>
    <br>
    <p style="font-size:1rem;line-height:2;color:#99a;">
    في هذا التطبيق التفاعلي، سنتعلّم معاً خطوة بخطوة:</p>
    <ul style="font-size:1rem;line-height:2.2;color:#8899bb;list-style:none;padding:0;">
      <li>🔬 ما هي المواد الموصلة والعازلة وشبه الموصلة؟</li>
      <li>🕳️ ما المقصود بالفجوة الطاقية؟</li>
      <li>➕ كيف نصنع النوع N والنوع P بالإشابة؟</li>
      <li>⚡ ما هو الثنائي البلوري (وصلة PN)؟</li>
      <li>🔋 ما الفرق بين الانحياز الأمامي والعكسي؟</li>
      <li>📏 كيف نحسب مقاومة الثنائي البلوري؟</li>
      <li>🔌 كيف نستخدم الثنائي كمقوّم للتيار المتردد؟</li>
    </ul>
    <br>
    <div class="info-box">
      <strong style="color:#00e5ff;">📌 كيف تستخدم هذا التطبيق؟</strong><br>
      اختر الموضوع من القائمة الجانبية، ثم استخدم الأدوات التفاعلية (المنزلقات، أزرار الاختيار)
      لتغيير المادة والقيم وشاهد ما يحدث بصرياً من خلال الرسوم المتحركة والمنحنيات البيانية.
    </div>
    </div>
    """, unsafe_allow_html=True)


# ─── 2. المواد وشبه الموصلات ────────────────────────────────────────
elif page == "🔬 المواد وشبه الموصلات":
    st.markdown('<div class="section-card"><h2>المواد الموصلة والعازلة وشبه الموصلة</h2>', unsafe_allow_html=True)

    st.markdown("""
    <p style="line-height:2.2;color:#bbc;">كل مادة حولنا تتكوّن من ذرات، ولكل ذرة إلكترونات تدور حول نواتها.
    الإلكترونات الموجودة في <strong style="color:#ffcc00;">المستوى الأخير</strong> تُسمّى
    <strong style="color:#00e5ff;">إلكترونات التكافؤ</strong>، وهي التي تحدد إذا كانت المادة توصل الكهرباء أم لا.</p>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        <div class="warn-box">
        <h3 style="color:#ff9800;margin:0 0 8px;">🔌 مواد موصلة (Conductors)</h3>
        <p style="margin:0;line-height:2;color:#ccb;">إلكترونات التكافؤ <strong>&lt; 4</strong><br>
        ارتباط ضعيف بالذرة → إلكترونات حرة كثيرة<br>
        <strong>أمثلة:</strong> النحاس، الحديد، الفضة</p>
        </div>
        <div class="warn-box" style="border-color:#ff4444;">
        <h3 style="color:#ff4444;margin:0 0 8px;">🚫 مواد عازلة (Insulators)</h3>
        <p style="margin:0;line-height:2;color:#ccb;">إلكترونات التكافؤ <strong>&gt; 4</strong><br>
        ارتباط قوي بالذرة → لا إلكترونات حرة تقريباً<br>
        <strong>أمثلة:</strong> المطاط، الزجاج، المايكا</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="success-box">
        <h3 style="color:#4caf50;margin:0 0 8px;">⚛️ مواد شبه موصلة (Semiconductors)</h3>
        <p style="margin:0;line-height:2;color:#ccb;">إلكترونات التكافؤ <strong>= 4</strong><br>
        توصيل متوسط ← يمكن التحكم به!<br>
        <strong>أمثلة:</strong> السليكون (Si)، الجرمانيوم (Ge)</p>
        </div>
        <div class="info-box">
        <h3 style="color:#00e5ff;margin:0 0 8px;">💡 لماذا مهمة؟</h3>
        <p style="margin:0;line-height:2;color:#ccb;">بإضافة شوائب (إشابة) نتحكم بقدرتها على التوصيل،
        وبذلك نصنع الثنائي البلوري والترانزستور وكل الأجهزة الإلكترونية!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<h3 style="margin-top:20px;">🔬 جرّب بنفسك: تأثير الحرارة على بلورة السليكون</h3>', unsafe_allow_html=True)
    mat = st.selectbox("اختر المادة:", ["Si — السليكون", "Ge — الجرمانيوم"], key="lat_mat")
    mat_code = "Si" if "Si" in mat else "Ge"
    temp = st.slider("درجة الحرارة (K):", 0, 600, 0, 10, key="lat_temp",
                     help="عند الصفر المطلق (0K) لا توجد إلكترونات حرة. مع زيادة الحرارة تتهدم بعض الروابط.")

    if temp == 0:
        st.markdown("""
        <div class="info-box">
        <strong>🔬 عند الصفر المطلق (0 K):</strong><br>
        جميع إلكترونات التكافؤ مقيدة في الروابط التساهمية. لا توجد إلكترونات حرة ولا فجوات.
        البلورة تتصرف كعازل تام.
        </div>
        """, unsafe_allow_html=True)
    elif temp < 200:
        st.markdown(f"""
        <div class="info-box">
        <strong>🌡️ عند {temp} K — حرارة منخفضة:</strong><br>
        عدد قليل جداً من الروابط تتهدم. تتكون أزواج إلكترون-فجوة قليلة.
        التوصيل ضعيف جداً.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="success-box">
        <strong>🌡️ عند {temp} K — حرارة مرتفعة:</strong><br>
        عدد كبير من الروابط تتهدم! تتكون أزواج إلكترون-فجوة كثيرة.
        <strong style="color:#00e5ff;">الإلكترونات الحرة</strong> (النقاط الزرقاء) تتحرك عشوائياً<br>
        <strong style="color:#ff4466;">الفجوات</strong> (الدوائر الحمراء) تبدو كشحنات موجبة تتحرك بعكس الإلكترونات
        </div>
        """, unsafe_allow_html=True)

    components.html(html_lattice(temp, mat_code), width=820, height=420)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── 3. الفجوة الطاقية ─────────────────────────────────────────────
elif page == "🕳️ الفجوة الطاقية (Band Gap)":
    st.markdown('<div class="section-card"><h2>الفجوة الطاقية (Band Gap)</h2>', unsafe_allow_html=True)

    st.markdown("""
    <p style="line-height:2.2;color:#bbc;">
    في أي مادة، توجد إلكترونات في مستويات طاقة مختلفة. عند تجمّع الذرات في بلورة،
    تتشكّل <strong style="color:#ff6688;">نطاقات الطاقة</strong> بدلاً من المستويات المنفصلة:</p>
    <ul style="line-height:2.2;color:#99aabb;">
      <li><strong style="color:#ff6688;">نطاق التكافؤ (Valence Band):</strong> يحتوي إلكترونات التكافؤ المقيدة بالذرة</li>
      <li><strong style="color:#00e5ff;">نطاق التوصيل (Conduction Band):</strong> الإلكترونات هنا حرة وتسهم في التوصيل</li>
      <li><strong style="color:#ffcc00;">الفجوة الطاقية (Band Gap - Eg):</strong> الفرق في الطاقة بين النطاقين</li>
    </ul>
    """, unsafe_allow_html=True)

    mat = st.selectbox("اختر المادة لمشاهدة فجوتها الطاقية:", [
        "Si — السليكون (Eg = 1.12 eV)",
        "Ge — الجرمانيوم (Eg = 0.67 eV)"
    ], key="bg_mat")
    mat_code = "Si" if "Si" in mat else "Ge"

    st.plotly_chart(plot_band_gap(mat_code), use_container_width=True)

    st.markdown("""
    <div class="info-box">
    <strong>📌 ماذا يعني هذا عملياً؟</strong><br><br>
    • <strong style="color:#ff9800;">العوازل:</strong> فجوة كبيرة جداً (> 5 eV) → لا يمكن للإلكترونات القفز → لا توصيل<br>
    • <strong style="color:#4caf50;">أشباه الموصلات:</strong> فجوة متوسطة (0.1 - 3 eV) → بالحرارة أو الإشابة يمكن للإلكترونات القفز<br>
    • <strong style="color:#00e5ff;">الموصلات:</strong> النطاقان متداخلان → الإلكترونات حرة دائماً
    </div>
    <div class="warn-box">
    <strong>⚡ لاحظ الفرق:</strong> فجوة السليكون (1.12 eV) أكبر من الجرمانيوم (0.67 eV)،
    لذلك السليكون أقل تأثراً بالحرارة وأكثر استقراراً في التطبيقات الإلكترونية.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── 4. النوع N والنوع P ───────────────────────────────────────────
elif page == "➕ النوع N والنوع P":
    st.markdown('<div class="section-card"><h2>أشباه الموصلات من النوع N والنوع P</h2>', unsafe_allow_html=True)

    st.markdown("""
    <p style="line-height:2.2;color:#bbc;">
    أشباه الموصلات النقية لا توصل الكهرباء جيداً. لكن بعملية تُسمّى
    <strong style="color:#ffcc00;">الإشابة (Doping)</strong>، نضيف شوائب منتقاة لزيادة التوصيل:</p>
    """, unsafe_allow_html=True)

    dtype = st.radio("اختر نوع الإشابة:", ["نوع N (سالبة) — إضافة شوائب خماسية التكافؤ",
                                               "نوع P (موجبة) — إضافة شوائب ثلاثية التكافؤ"], key="dop_type")
    is_n = "N" in dtype

    if is_n:
        dopant = st.selectbox("اختر عنصر الإشابة (خماسي التكافؤ — 5 إلكترونات تكافؤ):",
                              ["Sb — الأنتيمون", "P — الفسفور", "As — الزرنيخ"], key="dop_n")
        dop_sym = dopant.split("—")[0].strip()
        st.markdown(f"""
        <div class="info-box">
        <strong style="color:#44cc44;">🟢 الإشابة من النوع N:</strong><br><br>
        ذرة <strong>{dop_sym}</strong> تحتوي <strong>5</strong> إلكترونات تكافؤ (واحد زائد!).<br>
        عند حلولها محل ذرة سليكون: 4 إلكترونات تكوّن روابط تساهمية ← <strong style="color:#00e5ff;">الإلكترون الخامس يصبح حراً!</strong><br><br>
        ✅ <strong>الناقلات الأغلبية:</strong> الإلكترونات الحرة (لأن عددها أكبر بكثير)<br>
        ⬜ <strong>الناقلات الأقلية:</strong> الفجوات (عدد قليل من الحرارة)<br><br>
        <strong>لماذا تُسمّى "سالبة"؟</strong> لأن الشحنة الحرة السائدة سالبة (الإلكترونات).
        </div>
        """, unsafe_allow_html=True)
    else:
        dopant = st.selectbox("اختر عنصر الإشابة (ثلاثي التكافؤ — 3 إلكترونات تكافؤ):",
                              ["B — البورون", "Ga — الغاليوم"], key="dop_p")
        dop_sym = dopant.split("—")[0].strip()
        st.markdown(f"""
        <div class="warn-box" style="border-color:#ff9800;">
        <strong style="color:#ff9800;">🟠 الإشابة من النوع P:</strong><br><br>
        ذرة <strong>{dop_sym}</strong> تحتوي <strong>3</strong> إلكترونات تكافؤ فقط (ناقص واحد!).<br>
        عند حلولها محل ذرة سليكون: 3 روابط تساهمية ← <strong style="color:#ff4466;">الرابطة الرابعة مفقودة → فجوة!</strong><br><br>
        ✅ <strong>الناقلات الأغلبية:</strong> الفجوات (لأن عددها أكبر بكثير)<br>
        ⬜ <strong>الناقلات الأقلية:</strong> الإلكترونات الحرة (عدد قليل من الحرارة)<br><br>
        <strong>لماذا تُسمّى "موجبة"؟</strong> لأن الفجوة تبدو كشحنة موجبة متحركة.
        </div>
        """, unsafe_allow_html=True)

    components.html(html_doping("n" if is_n else "p", dop_sym), width=820, height=420)

    st.markdown("""
    <div class="success-box">
    <strong>💡 ملاحظة مهمة:</strong> رغم أننا نسمّيها "سالبة" أو "موجبة"، إلا أن البلورة ككل متعادلة كهربائياً!
    التسمية تشير إلى <strong>نوع الناقلات الأغلبية</strong> وليس إلى شحنة البلورة.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── 5. الثنائي البلوري ────────────────────────────────────────────
elif page == "⚡ الثنائي البلوري (PN Junction)":
    st.markdown('<div class="section-card"><h2>الثنائي البلوري (وصلة PN)</h2>', unsafe_allow_html=True)

    st.markdown("""
    <p style="line-height:2.2;color:#bbc;">
    <strong style="color:#00e5ff;">الثنائي البلوري (Diode)</strong> يتكوّن من بلورة واحدة:
    نصفها من النوع <strong style="color:#ff6688;">P</strong> والنصف الآخر من النوع
    <strong style="color:#66bbff;">N</strong>. عند اتصالهما يتكوّن شيء سحري!</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <strong>🔍 ماذا يحدث عند اتصال P مع N؟</strong><br><br>
    <strong>الخطوة 1 — الانتشار:</strong> الإلكترونات من N تنتشر نحو P (لأنها أكثر هناك)،
    والفجوات من P تنتشر نحو N.<br><br>
    <strong>الخطوة 2 — إعادة التركيب:</strong> كل إلكترون يلتقي بفجوة يُعاد تركيبهما → يختفيان.<br><br>
    <strong>الخطوة 3 — منطقة الاستنزاف:</strong> نتيجة اختفاء الناقلات، تتكوّن منطقة وسطى
    <strong style="color:#ffaa33;">خالية من الناقلات</strong> تُسمّى "منطقة الاستنزاف".<br><br>
    <strong>الخطوة 4 — المجال الكهربائي الداخلي:</strong> الشحنات المتبقية في منطقة الاستنزاف
    (+ في طرف N، − في طرف P) تُنشئ مجالاً كهربائياً يُعيق المزيد من الانتشار.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="warn-box">
    <strong>⚡ رمز الثنائي في الدارات:</strong><br>
    المثلث يشير لاتجاه مرور التيار (من المصعد Anode إلى المهبط Cathode).<br>
    <strong style="color:#ff6688;">المصعد (A)</strong> = طرف النوع P ← <strong style="color:#66bbff;">المهبط (K)</strong> = طرف النوع N
    </div>
    """, unsafe_allow_html=True)

    components.html(html_pn_junction(), width=820, height=440)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── 6. الانحياز الأمامي ───────────────────────────────────────────
elif page == "🔋 الانحياز الأمامي":
    st.markdown('<div class="section-card"><h2>الانحياز الأمامي (Forward Bias)</h2>', unsafe_allow_html=True)

    st.markdown("""
    <p style="line-height:2.2;color:#bbc;">
    في الانحياز الأمامي، نوصل <strong style="color:#ff4444;">القطب الموجب للبطارية بالمصعد (P)</strong>
    و<strong style="color:#4444ff;">القطب السالب بالمهبط (N)</strong>.</p>
    """, unsafe_allow_html=True)

    mat = st.selectbox("اختر مادة الثنائي:", ["Si — السليكون (حاجز الجهد = 0.7 V)",
                                                 "Ge — الجرمانيوم (حاجز الجهد = 0.3 V)"], key="fb_mat")
    mat_code = "Si" if "Si" in mat else "Ge"
    barrier = 0.7 if mat_code == "Si" else 0.3

    voltage = st.slider("فرق الجهد المطبق (V):", 0.0, 2.0, 0.0, 0.05, key="fb_v",
                        help="زيادة الجهد تدريجياً ولاحظ ما يحدث عند تجاوز حاجز الجهد")

    if voltage < barrier * 0.8:
        st.markdown(f"""
        <div class="warn-box">
        <strong>⚠️ الجهد ({voltage:.2f} V) أقل بكثير من حاجز الجهد ({barrier} V)</strong><br><br>
        المجال الكهربائي الخارجي ضعيف ولا يستطيع التغلب على المجال الداخلي لمنطقة الاستنزاف.<br>
        <strong>التيار شبه معدوم</strong> — المصباح لا يضيء.
        </div>
        """, unsafe_allow_html=True)
    elif voltage < barrier:
        st.markdown(f"""
        <div class="warn-box" style="border-color:#ffcc00;">
        <strong>⚡ نقترب من حاجز الجهد! ({voltage:.2f} V من {barrier} V)</strong><br><br>
        المجال الخارجي يبدأ بضغط منطقة الاستنزاف التي تضيق تدريجياً.<br>
        <strong>تيار صغير جداً يبدأ بالظهور</strong>.
        </div>
        """, unsafe_allow_html=True)
    else:
        current_approx = (voltage - barrier) * 10
        st.markdown(f"""
        <div class="success-box">
        <strong>✅ تجاوزنا حاجز الجهد! ({voltage:.2f} V > {barrier} V)</strong><br><br>
        المجال الخارجي قوي كفاية لتضييق منطقة الاستنزاف كلياً تقريباً.<br>
        <strong style="color:#00e5ff;">الإلكترونات تتدفق بحرية!</strong> التيار يزداد بسرعة كبيرة.<br>
        <strong>المصباح يضيء</strong> {('بشدة 🔆' if current_approx > 8 else 'بإضاءة متوسطة 💡' if current_approx > 3 else 'بإضاءة خافتة 🔅')}
        </div>
        """, unsafe_allow_html=True)

    components.html(html_bias_circuit("forward", voltage, mat_code), width=820, height=520)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── 7. الانحياز العكسي ───────────────────────────────────────────
elif page == "🔄 الانحياز العكسي":
    st.markdown('<div class="section-card"><h2>الانحياز العكسي (Reverse Bias)</h2>', unsafe_allow_html=True)

    st.markdown("""
    <p style="line-height:2.2;color:#bbc;">
    في الانحياز العكسي، نعكس الاتصال: <strong style="color:#ff4444;">القطب الموجب بالمهبط (N)</strong>
    و<strong style="color:#4444ff;">القطب السالب بالمصعد (P)</strong>.</p>
    """, unsafe_allow_html=True)

    mat = st.selectbox("اختر مادة الثنائي:", ["Si — السليكون", "Ge — الجرمانيوم"], key="rb_mat")
    mat_code = "Si" if "Si" in mat else "Ge"
    barrier = 0.7 if mat_code == "Si" else 0.3

    voltage = st.slider("فرق الجهد العكسي (V):", 0, 30, 5, 1, key="rb_v",
                        help="زيادة الجهد العكسي ولاحظ اتساع منطقة الاستنزاف")

    st.markdown(f"""
    <div class="warn-box">
    <strong>❌ الانحياز العكسي — التيار محظور!</strong><br><br>
    المجال الكهربائي الخارجي <strong>يعزز</strong> المجال الداخلي لمنطقة الاستنزاف بدلاً من إلغائه.<br>
    منطقة الاستنزاف <strong style="color:#ffaa33;">تتسع</strong> مع زيادة الجهد العكسي (الآن عرضها ≈ {min(60 + voltage * 5, 130):.0f} وحدة).<br>
    <strong>التيار شبه معدوم</strong> (تيار تسرب ضعيف جداً بالميكرو أمبير فقط).<br>
    <strong>المصباح مطفأ تماماً.</strong>
    </div>
    <div style="background:#2a0a0a;border:1px solid #ff000033;border-radius:10px;padding:15px;margin:10px 0;">
    <strong style="color:#ff3333;">⚠️ تحذير: جهد الانهيار!</strong><br>
    <span style="color:#cc8888;">إذا زاد الجهد العكسي عن قيمة معينة تُسمّى "جهد الانهيار" (Breakdown Voltage)،
    تنهار مقاومة الثنائي ويسري تيار كبير يؤدي إلى <strong>تلف الثنائي!</strong></span>
    </div>
    """, unsafe_allow_html=True)

    components.html(html_bias_circuit("reverse", voltage, mat_code), width=820, height=520)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── 8. مقاومة الثنائي البلوري ────────────────────────────────────
elif page == "📏 مقاومة الثنائي البلوري":
    st.markdown('<div class="section-card"><h2>مقاومة الثنائي البلوري</h2>', unsafe_allow_html=True)

    st.markdown("""
    <p style="line-height:2.2;color:#bbc;">
    مقاومة الثنائي البلوري <strong style="color:#ffcc00;">ليست ثابتة!</strong> إنها تعتمد على طريقة التوصيل
    وفرق الجهد المطبق. لذلك نسمّيها <strong style="color:#00e5ff;">مقاومة لا أومية</strong>.</p>
    """, unsafe_allow_html=True)

    mat = st.selectbox("اختر مادة الثنائي:", ["Si — السليكون (حاجز 0.7 V)",
                                                 "Ge — الجرمانيوم (حاجز 0.3 V)"], key="res_mat")
    mat_code = "Si" if "Si" in mat else "Ge"
    barrier = 0.7 if mat_code == "Si" else 0.3
    Is = 1e-9
    Vt = 0.026

    v_point = st.slider("اختر فرق الجهد لقراءة المقاومة عند هذه النقطة (V):", -10.0, 1.2, 0.8, 0.05, key="res_v")

    # Calculate resistance at this point
    if v_point > 0.01:
        i_at_v = Is * (np.exp(min(v_point, 1.2) / Vt) - 1)
        r_forward = v_point / i_at_v if i_at_v > 1e-12 else float('inf')
        r_display = f"{r_forward:.1f} Ω" if r_forward < 1e6 else f"{r_forward / 1e3:.1f} kΩ" if r_forward < 1e9 else f"{r_forward / 1e6:.1f} MΩ"
    else:
        r_forward = float('inf')
        r_display = "∞ (شبه لا نهائية)"

    if v_point < 0:
        i_at_v = abs(Is * (np.exp(max(v_point, -20) / Vt) - 1))
        r_reverse = abs(v_point) / i_at_v if i_at_v > 1e-15 else float('inf')
        r_rev_display = f"{r_reverse / 1e6:.1f} MΩ" if r_reverse < 1e12 else f"{r_reverse / 1e9:.1f} GΩ"
    else:
        r_reverse = float('inf')
        r_rev_display = "∞"

    st.plotly_chart(plot_iv_curve(mat_code, v_point), use_container_width=True)

    if v_point >= 0:
        st.markdown(f"""
        <div class="info-box">
        <strong>📊 عند الجهد {v_point:.2f} V (انحياز أمامي):</strong><br><br>
        {'⚠️ الجهد أقل من حاجز الجهد ({barrier} V) ← تيار شبه معدوم ← مقاومة كبيرة جداً' if v_point < barrier else
        f'✅ الجهد أكبر من حاجز الجهد ({barrier} V) ← تيار يسري ← مقاومة صغيرة<br>'
        f'<strong style="color:#00e5ff;">المقاومة ≈ {r_display}</strong>'}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="warn-box">
        <strong>📊 عند الجهد {v_point:.1f} V (انحياز عكسي):</strong><br><br>
        ❌ تيار التسرب ضعيف جداً (بالميكرو أمبير)<br>
        <strong style="color:#ff6644;">المقاومة ≈ {r_rev_display}</strong> — مقاومة كبيرة جداً!
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="success-box">
    <strong>💡 الخلاصة:</strong><br>
    • <strong>الانحياز الأمامي</strong> (بعد حاجز الجهد): مقاومة <strong style="color:#00e5ff;">صغيرة</strong> (بضع عشرات من الأوم)<br>
    • <strong>الانحياز العكسي:</strong> مقاومة <strong style="color:#ff4444;">كبيرة جداً</strong> (ميغا أوم أو أكثر)<br>
    • هذا الاختلاف الكبير في المقاومة هو ما يجعل الثنائي يسمح بالتيار في اتجاه واحد فقط!
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── 9. الثنائي مقوّم للتيار المتردد ──────────────────────────────
elif page == "🔌 الثنائي مقوّم للتيار المتردد":
    st.markdown('<div class="section-card"><h2>الثنائي البلوري مقوّماً للتيار المتردد</h2>', unsafe_allow_html=True)

    st.markdown("""
    <p style="line-height:2.2;color:#bbc;">
    المنازل تزوّدنا بتيار <strong style="color:#4488ff;">متردد</strong> (يتغير مقداره واتجاهه)،
    لكن الأجهزة الإلكترونية تحتاج تيار <strong style="color:#44ff88;">مستمر</strong> (ثابت الاتجاه).<br>
    <strong style="color:#00e5ff;">الثنائي البلوري يحل هذه المشكلة!</strong></p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    <strong>🔌 مبدأ العمل — مقوّم نصف موجة:</strong><br><br>
    <strong style="color:#44ff88;">النصف الموجب (V > 0):</strong> الثنائي في انحياز أمامي → يمرّر التيار → يظهر في الخرج<br>
    <strong style="color:#ff4466;">النصف السالب (V < 0):</strong> الثنائي في انحياز عكسي → يحظر التيار → الخرج = صفر<br><br>
    النتيجة: <strong style="color:#ffcc00;">موجة نصف جيبية في اتجاه واحد فقط</strong> (تيار pulsating وليس مستمر تماماً)
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        vmax = st.slider("القيمة العظمى للجهد (V):", 1, 50, 10, 1, key="rec_v")
    with col2:
        freq = st.slider("التردد (Hz):", 10, 200, 50, 10, key="rec_f")

    v_rms = vmax / np.sqrt(2)
    st.markdown(f"""
    <div class="warn-box">
    <strong>📊 معلومات حسابية:</strong><br>
    القيمة العظمى: <strong>{vmax} V</strong> &nbsp;|&nbsp;
    التردد: <strong>{freq} Hz</strong> &nbsp;|&nbsp;
    الزمن الدوري: <strong>{1000/freq:.1f} ms</strong><br>
    القيمة الفعّالة للإشارة الخارجة (نصف موجة): ≈ <strong style="color:#ffcc00;">{vmax/2:.1f} V</strong>
    (نلاحظ أنها نصف القيمة الفعّالة للإشارة الكاملة {v_rms:.1f} V)
    </div>
    """, unsafe_allow_html=True)

    components.html(html_rectifier(vmax, freq), width=820, height=560)

    st.plotly_chart(plot_ac_rectified(vmax, freq), use_container_width=True)

    st.markdown("""
    <div class="success-box">
    <strong>💡 تطبيقات عملية:</strong><br>
    • <strong>شواحن الهاتف والحاسوب:</strong> تحوّل التيار المتردد من المقتبس إلى تيار مستمر يشغّل الجهاز<br>
    • <strong>محولات الطاقة (Adapters):</strong> تستخدم مقوّمات لتحويل 220V متردد إلى 5V أو 12V مستمر<br>
    • ملاحظة: مقوّم نصف الموجة يفقد نصف الطاقة! في التطبيقات العملية يُستخدم <strong>مقوّم كامل الموجة</strong> لأفضل كفاءة.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── تذييل الصفحة ──────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:20px;margin-top:20px;
  border-top:1px solid #00e5ff11;">
  <p style="color:#556;font-size:0.85rem;">
    تطبيق فيزياء أشباه الموصلات التفاعلية — based on فيزياء الثاني عشر، الوحدة السادسة</p>
  <p style="color:#ff6baa;font-size:0.95rem;font-weight:700;margin-top:4px;">
    Israa Samara ✦</p>
</div>
""", unsafe_allow_html=True)