import React, { useEffect, useRef, useState } from "react";

export default function AnimatedNumber({ value, language = "ar", duration = 700 }) {
  const numericValue = Number(value);
  const isNumeric = Number.isFinite(numericValue);
  const [display, setDisplay] = useState(isNumeric ? 0 : value ?? "—");
  const previous = useRef(0);

  useEffect(() => {
    if (!isNumeric) {
      setDisplay(value ?? "—");
      return undefined;
    }

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setDisplay(numericValue);
      previous.current = numericValue;
      return undefined;
    }

    const startValue = previous.current;
    const delta = numericValue - startValue;
    const startedAt = performance.now();
    let frame;

    const update = (now) => {
      const progress = Math.min((now - startedAt) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplay(Math.round(startValue + delta * eased));
      if (progress < 1) frame = requestAnimationFrame(update);
      else previous.current = numericValue;
    };

    frame = requestAnimationFrame(update);
    return () => cancelAnimationFrame(frame);
  }, [duration, isNumeric, numericValue, value]);

  return isNumeric
    ? new Intl.NumberFormat(language === "ar" ? "ar-EG" : "en-GB").format(display)
    : display;
}
