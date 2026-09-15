import React from "react";
import {
  ArrowUpLeft,
  BookOpenCheck,
  Building2,
  GraduationCap,
  Settings2,
  ShieldCheck,
  UsersRound,
} from "lucide-react";
import AnimatedNumber from "../../components/ui/AnimatedNumber";
import { localized } from "../../i18n";

const ICONS = {
  students: UsersRound,
  theses: BookOpenCheck,
  committees: GraduationCap,
  settings: Settings2,
};

const COPY = {
  students: { ar: "ملفات الطلاب", en: "Student records" },
  theses: { ar: "الرسائل العلمية", en: "Theses" },
  committees: { ar: "اللجان والمناقشات", en: "Committees & defenses" },
  settings: { ar: "حوكمة المنصة", en: "Platform governance" },
};

function ProgramDirectorDeck({ data, language, onNavigate }) {
  const ar = language === "ar";
  const navigation = data.ui?.navigation || [];
  const permitted = new Map(navigation.map((item) => [item.key, item]));
  const destinations = ["students", "theses", "committees", "settings"].filter((key) => permitted.has(key));

  return (
    <section className="roleCommandDeck programCommandDeck" aria-labelledby="program-command-title">
      <div className="roleCommandIntro">
        <span className="commandKicker"><ShieldCheck size={15} />{ar ? "إدارة البرنامج والمنصة" : "Program & platform control"}</span>
        <h3 id="program-command-title">{ar ? "غرفة العمليات الرقمية" : "Digital operations room"}</h3>
        <p>{ar ? "وصول مباشر للوحدات المصرح بها، مع فصل كامل بين تشغيل البرنامج وحوكمة المنصة." : "Direct access to authorized modules, with clear separation between program operations and platform governance."}</p>
      </div>
      <div className="commandDestinations">
        {destinations.map((key, index) => {
          const Icon = ICONS[key];
          const item = permitted.get(key);
          return (
            <button key={key} type="button" onClick={() => onNavigate?.(key)} style={{ "--deck-delay": `${index * 70}ms` }}>
              <span><Icon size={20} /></span>
              <div><small>{key === "settings" ? (ar ? "إدارة محمية" : "Protected control") : (ar ? "تشغيل أكاديمي" : "Academic operations")}</small><strong>{localized(item, "label", language, ar ? COPY[key].ar : COPY[key].en)}</strong></div>
              <ArrowUpLeft size={17} aria-hidden="true" />
            </button>
          );
        })}
      </div>
    </section>
  );
}

function ViceDeanDeck({ data, language, onNavigate }) {
  const ar = language === "ar";
  const decisions = data.pending_decisions || [];
  const thesisTotal = (data.research_analytics?.workflow || []).reduce((sum, item) => sum + (Number(item.count) || 0), 0);

  return (
    <section className="roleCommandDeck viceDeanCommandDeck" aria-labelledby="vice-dean-command-title">
      <div className="roleCommandIntro">
        <span className="commandKicker"><Building2 size={15} />{ar ? "موجز القرار الأكاديمي" : "Academic decision briefing"}</span>
        <h3 id="vice-dean-command-title">{ar ? "مسار القرارات ذات الأولوية" : "Priority decision runway"}</h3>
        <p>{ar ? "المعروض هنا مستخرج من مرحلة وكيل الكلية في سير العمل الفعلي." : "Every item shown here comes from the vice dean stage in the live workflow."}</p>
      </div>
      <div className="decisionRunway">
        <div className="decisionRunwayStat"><span>{ar ? "بانتظار القرار" : "Awaiting decision"}</span><strong><AnimatedNumber value={decisions.length} language={language} /></strong></div>
        <div className="decisionRunwayLine" aria-hidden="true"><i style={{ "--runway-load": `${thesisTotal ? Math.min((decisions.length / thesisTotal) * 100, 100) : 0}%` }} /></div>
        <button type="button" onClick={() => onNavigate?.("theses")}><BookOpenCheck size={18} />{ar ? "فتح الرسائل محل القرار" : "Open theses requiring decisions"}<ArrowUpLeft size={16} /></button>
      </div>
    </section>
  );
}

export default function RoleCommandDeck({ data, user, language, onNavigate }) {
  const roles = new Set(user?.roles || data.roles || []);
  const platformDirector = Boolean(user?.can_manage_dashboard || roles.has("PLATFORM_ADMIN"));
  if (platformDirector) return <ProgramDirectorDeck data={data} language={language} onNavigate={onNavigate} />;
  if (roles.has("VICE_DEAN_POSTGRADUATE") || roles.has("VICE_DEAN")) return <ViceDeanDeck data={data} language={language} onNavigate={onNavigate} />;
  return null;
}
