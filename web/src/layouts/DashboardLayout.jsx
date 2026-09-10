import React from "react";
import logo from "../assets/logo.webp";
import {
  BarChart3,
  BookOpen,
  CalendarDays,
  LayoutDashboard,
  Settings as SettingsIcon,
  Users,
} from "lucide-react";

const iconMap = {
  LayoutDashboard,
  Users,
  BookOpen,
  CalendarDays,
  BarChart3,
  Settings: SettingsIcon,
};

export default function DashboardLayout({
  children,
  language,
  navigation = [],
  activeSection = "overview",
  onNavigate,
}) {
  const ar = language === "ar";

  return (
    <main dir={ar ? "rtl" : "ltr"}>
      <aside>
        <div className="brand">
          <img src={logo} alt="Faculty of Medicine - Assiut University" />
          <div>
            {ar ? "كلية الطب" : "Faculty of Medicine"}
            <small>{ar ? "جامعة أسيوط" : "Assiut University"}</small>
            <small>{ar ? "إدارة الدراسات العليا والبحوث" : "Postgraduate Studies & Research"}</small>
          </div>
        </div>

        <nav>
          {navigation.map((item) => {
            const Icon = iconMap[item.icon] || LayoutDashboard;
            const label = ar ? item.label_ar : (item.label_en || item.label_ar);
            return (
              <button
                className={activeSection === item.key ? "active" : ""}
                key={item.key}
                onClick={() => onNavigate?.(item.key)}
                type="button"
                aria-current={activeSection === item.key ? "page" : undefined}
              >
                <Icon size={18} />
                <span>{label}</span>
              </button>
            );
          })}
        </nav>
      </aside>

      <section className="workspace">
        {children}
      </section>
    </main>
  );
}
