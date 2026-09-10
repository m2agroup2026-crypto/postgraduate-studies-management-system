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

export default function MetricsCards({ metrics, config = [], definitions = {}, language = "ar" }) {
  const cards = config;
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
            <small title={definitions[card.key]}>
              {ar ? "بيانات مباشرة" : "Live system data"}
            </small>
          </article>
        );
      })}
    </div>
  );
}
