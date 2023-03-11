import { Directive } from "vue";
import { Tooltip } from "bootstrap";

export const vBsTooltip: Directive<HTMLElement, string> = {
  mounted: (el, binding) => {
    el.setAttribute("data-bs-toggle", "tooltip");
    el.setAttribute("title", binding.value);
    if (binding.modifiers.html) el.setAttribute("data-bs-html", "true");
    ["top", "bottom", "right", "left"].forEach((modifier) => {
      if (binding.modifiers[modifier])
        el.setAttribute("data-bs-placement", modifier);
    });
    new Tooltip(el, {
      boundary: document.body,
    });
  },
};
