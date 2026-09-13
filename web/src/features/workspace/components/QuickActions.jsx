import React from "react";

export default function QuickActions({
  language,
  onNavigate,
}) {
  const ar = language === "ar";

  const actions = [
    {
      key: "students",
      label_ar: "إدارة الطلاب",
      label_en: "Student Registry",
    },
    {
      key: "theses",
      label_ar: "الرسائل العلمية",
      label_en: "Thesis Management",
    },
    {
      key: "committees",
      label_ar: "اللجان والمناقشات",
      label_en: "Committees & Defenses",
    },
    {
      key: "reports",
      label_ar: "التقارير",
      label_en: "Reports",
    },
  ];


  return (
    <section className="quickActions">
      <header>
        <h3>
          {ar ? "إجراءات سريعة" : "Quick Actions"}
        </h3>

        <p>
          {ar
            ? "الوصول المباشر إلى وحدات التشغيل"
            : "Quick access to operational modules"}
        </p>
      </header>


      <div className="quickActionsGrid">
        {actions.map((action) => (
          <button
            key={action.key}
            type="button"
            onClick={() => onNavigate(action.key)}
          >
            {ar
              ? action.label_ar
              : action.label_en}
          </button>
        ))}
      </div>
    </section>
  );
}
