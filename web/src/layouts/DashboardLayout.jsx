import React from "react";

export default function DashboardLayout({
  children,
  user,
  language,
  onLanguageChange,
  onLogout,
}) {
  const ar = language === "ar";

  return (
    <main dir={ar ? "rtl" : "ltr"}>
      <aside>
        <div className="brand">
          <span>PG</span>
          <div>
            الدراسات العليا
            <small>كلية الطب</small>
          </div>
        </div>

        <nav>
          {[
            "نظرة عامة",
            "الطلاب",
            "الرسائل العلمية",
            "اللجان والمناقشات",
            "التقارير",
            "الإعدادات",
          ].map((item, index) => (
            <button
              className={index === 0 ? "active" : ""}
              key={item}
            >
              {item}
            </button>
          ))}
        </nav>
      </aside>

      <section className="workspace">
        {children}
      </section>
    </main>
  );
}
