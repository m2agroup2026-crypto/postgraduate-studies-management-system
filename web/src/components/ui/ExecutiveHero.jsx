import React from "react";
import { Clock3, Landmark, ShieldCheck } from "lucide-react";

export default function ExecutiveHero({ data, user, language = "ar", mode = "academicLeader" }) {
  const ar = language === "ar";
  const isPlatformDirector = mode === "platformDirector";

  const pendingMetric = data.ui?.metrics?.find(
    (item) => item.key === "pending"
  );

  return (
    <section className="executiveHero">
      <div className="executiveHeroCopy">
        <span className="executiveEyebrow">
          <Landmark size={16} />
          {ar
            ? isPlatformDirector ? "مركز قيادة البرنامج والمنصة" : "مركز القيادة الأكاديمي التنفيذي"
            : isPlatformDirector ? "Program & Platform Command Center" : "Executive Academic Command Center"}
        </span>

        <h2>
          {user?.name || data.identity?.name || (ar ? "المستخدم" : "User")}
        </h2>

        <p>
          {user?.title || data.identity?.title || (ar ? "الدراسات العليا" : "Postgraduate Studies")}
        </p>

        <div className="executiveTrust">
          <ShieldCheck size={17} />
          <span>
            {ar
              ? "بيانات مباشرة وفق صلاحيات الحساب"
              : "Live, permission-scoped data"}
          </span>
        </div>
      </div>

      <div
        className="decisionBrief"
        aria-label={
          ar
            ? "ملخص القرار الحالي"
            : "Current decision brief"
        }
      >
        <Clock3 size={22} />

        <span>
          {pendingMetric?.label_ar ||
            (ar
              ? "طلبات تنتظر قرارك"
              : "Awaiting your decision")}
        </span>

        <strong>
          {data.metrics?.pending ?? 0}
        </strong>

        <small>
          {ar
            ? "من سير العمل الفعلي"
            : "From the live workflow"}
        </small>
      </div>
    </section>
  );
}
