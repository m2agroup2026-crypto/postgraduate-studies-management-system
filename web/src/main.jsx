import React, {useState} from 'react';
import {createRoot} from 'react-dom/client';
import {BookOpen, Bot, CalendarDays, GraduationCap, Languages, Search, Users} from 'lucide-react';
import './styles.css';

const profiles={
  PROGRAM_DIRECTOR:{name:'مدير البرنامج',title:'مدير برنامج الدراسات العليا'},
  DEAN:{name:'الأستاذ الدكتور علاء عطية',title:'عميد كلية الطب'},
  VICE_DEAN:{name:'الأستاذ الدكتور محمد عبد الباسط خلاف',title:'وكيل الكلية لشؤون الدراسات العليا والبحوث'}
};
const metrics=[['الطلاب النشطون','1,284',Users],['الرسائل المسجلة','746',BookOpen],['المناقشات القادمة','38',CalendarDays],['ملفات تحتاج متابعة','64',GraduationCap]];

function App(){
 const [role,setRole]=useState('PROGRAM_DIRECTOR'); const [lang,setLang]=useState('ar');
 const [open,setOpen]=useState(false); const [messages,setMessages]=useState([{from:'bot',text:'مرحبًا، أنا مساعد الدراسات العليا. كيف أساعدك اليوم؟'}]); const [q,setQ]=useState('');
 const ar=lang==='ar', p=profiles[role];
 const send=()=>{if(!q.trim())return; setMessages([...messages,{from:'user',text:q},{from:'bot',text:'وجدت 64 ملفًا يحتاج متابعة، و12 مناقشة خلال الأسبوعين القادمين.'}]);setQ('')};
 return <main dir={ar?'rtl':'ltr'}>
  <aside><div className="brand"><span>PG</span><div>الدراسات العليا<small>كلية الطب</small></div></div>
   <nav>{['نظرة عامة','الطلاب','الرسائل العلمية','اللجان والمناقشات','التقارير','الإعدادات'].map((x,i)=><button className={i===0?'active':''} key={x}>{x}</button>)}</nav>
  </aside>
  <section className="workspace">
   <header><div><small>Postgraduate Studies Management System</small><h1>مركز قيادة الدراسات العليا</h1></div><div className="actions"><button onClick={()=>setLang(ar?'en':'ar')}><Languages size={18}/>{ar?'English':'العربية'}</button><div className="profile"><b>{p.name}</b><small>{p.title}</small></div></div></header>
   <div className="rolebar"><span>عرض لوحة:</span>{Object.keys(profiles).map(r=><button className={role===r?'selected':''} onClick={()=>setRole(r)} key={r}>{profiles[r].title}</button>)}</div>
   <div className="welcome"><div><small>لوحة المتابعة التنفيذية</small><h2>مرحبًا، {p.name}</h2><p>صورة موحدة لحركة التسجيل والرسائل واللجان والقرارات الأكاديمية.</p></div><div className="pulse"><span>حالة النظام</span><b>جميع الخدمات تعمل</b></div></div>
   <div className="metrics">{metrics.map(([label,value,Icon])=><article key={label}><Icon/><span>{label}</span><strong>{value}</strong><small>محدّث الآن</small></article>)}</div>
   <div className="grid"><article className="panel"><div className="paneltitle"><h3>أداء الأقسام</h3><button><Search size={16}/> التفاصيل</button></div>{[['الباطنة',92],['الأطفال',84],['الجراحة',76],['الصحة العامة',68]].map(([n,v])=><div className="progress" key={n}><span>{n}</span><i><em style={{width:v+'%'}}/></i><b>{v}%</b></div>)}</article><article className="panel"><h3>تنبيهات تتطلب إجراء</h3><ul><li><b>18</b><span>خطة بحث تجاوزت موعد المراجعة</span></li><li><b>12</b><span>لجنة مناقشة تنتظر الاعتماد</span></li><li><b>34</b><span>ملف طالب يحتاج استكمالًا</span></li></ul></article></div>
  </section>
  <button className="assistantFab" onClick={()=>setOpen(!open)}><Bot/></button>
  {open&&<div className="assistant"><header><Bot/><div><b>المساعد الذكي</b><small>متصل ببياناتك المصرح بها</small></div></header><div className="chat">{messages.map((m,i)=><p className={m.from} key={i}>{m.text}</p>)}</div><footer><input value={q} onChange={e=>setQ(e.target.value)} onKeyDown={e=>e.key==='Enter'&&send()} placeholder="اسأل عن الطلاب أو الرسائل..."/><button onClick={send}>إرسال</button></footer></div>}
 </main>
}
createRoot(document.getElementById('root')).render(<App/>);
