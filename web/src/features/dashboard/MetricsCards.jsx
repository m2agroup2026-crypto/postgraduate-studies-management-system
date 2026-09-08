import React from "react";
import {
  BookOpen,
  CalendarDays,
  GraduationCap,
  Users,
} from "lucide-react";

const iconMap = {
  Users,
  BookOpen,
  CalendarDays,
  GraduationCap,
};

const fallbackCards = [
  { key: "students", label_ar: "الطلاب النشطون", label_en: "Active students", icon: "Users" },
  { key: "theses", label_ar: "الرسائل المسجلة", label_en: "Registered theses", icon: "BookOpen" },
  { key: "defenses", label_ar: "المناقشات القادمة", label_en: "Upcoming defenses", icon: "CalendarDays" },
  { key: "pending", label_ar: "ملفات تحتاج متابعة", label_en: "Files requiring follow-up", icon: "GraduationCap" },
];

export default function MetricsCards({ metrics, config, language = "ar" }) {
  const cards = config?.length ? config : fallbackCards;
  const ar = language === "ar";

  return (
    <div className="metrics">
      {cards.map((card) => {
        const Icon = iconMap[card.icon] || GraduationCap;
        const label = ar ? card.label_ar : (card.label_en || card.label_ar);
        return (
          <article key={card.key}>
            <Icon />
            <span>{label}</span>
            <strong>{metrics?.[card.key] ?? 0}</strong>
            <small>{ar ? "من قاعدة البيانات" : "From live system data"}</small>
          </article>
        );
      })}
    </div>
  );
}
