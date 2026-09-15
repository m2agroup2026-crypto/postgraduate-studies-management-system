import React from "react";
import MetricCard from "../../components/ui/MetricCard";
import {
  BookOpen,
  CalendarDays,
  GraduationCap,
  Users,
} from "lucide-react";
import { localized } from "../../i18n";

const iconMap = {
  Users,
  BookOpen,
  CalendarDays,
  GraduationCap,
};

export default function MetricsCards({ metrics, config = [], language = "ar" }) {
  const cards = config;
  const ar = language === "ar";

  return (
    <div className="metrics">
      {cards.map((card) => {
        const Icon = iconMap[card.icon] || GraduationCap;
        const label = localized(card, "label", language);
        return (
          <MetricCard
            key={card.key}
            icon={Icon}
            label={label}
            value={metrics?.[card.key] ?? 0}
            description={
              ar ? "بيانات مباشرة" : "Live system data"
            }
            language={language}
          />
        );
      })}
    </div>
  );
}
