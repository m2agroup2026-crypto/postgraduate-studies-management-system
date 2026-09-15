import { localizedField } from "./labels";

export function localized(record, field, language = "ar", fallback = "—") {
  return localizedField(record, field, language, fallback);
}

export function localizedFlat(record, field, language = "ar", fallback = "—") {
  return localized(record, field, language, fallback);
}
