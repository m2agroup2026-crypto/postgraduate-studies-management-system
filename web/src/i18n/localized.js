export function localized(item, field, language = "ar") {
  if (!item) return "—";

  const arabic = item[`${field}_ar`];
  const english = item[`${field}_en`];

  if (language === "en") {
    return english || arabic || "—";
  }

  return arabic || english || "—";
}

export function localizedFlat(item, field, language = "ar") {
  if (!item) return "—";

  const arabic = item[`${field}_ar`];
  const english = item[`${field}_en`];

  if (language === "en") {
    return english || arabic || "—";
  }

  return arabic || english || "—";
}
