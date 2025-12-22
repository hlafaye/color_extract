document.addEventListener("DOMContentLoaded", () => {
    // ---------- Elements ----------
    const fileInput = document.getElementById("file-input");
    const btnImporter = document.getElementById("btn-importer");
    const btnCalculer = document.getElementById("btn-calculer");
  
    // ---------- Import button -> open file picker ----------
    if (btnImporter && fileInput) {
      btnImporter.addEventListener("click", () => fileInput.click());
    }
  
    // ---------- Enable/disable "Calculer" ----------
    if (fileInput && btnCalculer) {
      const toggleCalc = () => {
        btnCalculer.disabled = !(fileInput.files && fileInput.files.length > 0);
      };
      fileInput.addEventListener("change", toggleCalc);
      toggleCalc(); // état initial
    }
  
    // ---------- Click-to-copy (event delegation) ----------
    document.addEventListener("click", async (e) => {
      const card = e.target.closest(".color-card");
      if (!card) return;
  
      const hex = card.dataset.hex;
      if (!hex) return;
  
      // debug rapide (tu peux enlever après)
      console.log("COPY:", hex);
  
      try {
        // clipboard API (souvent KO en http)
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(hex);
        } else {
          // fallback fiable
          const ta = document.createElement("textarea");
          ta.value = hex;
          ta.style.position = "fixed";
          ta.style.left = "-9999px";
          document.body.appendChild(ta);
          ta.focus();
          ta.select();
          const ok = document.execCommand("copy");
          ta.remove();
          if (!ok) throw new Error("execCommand copy failed");
        }
  
        card.classList.add("copied");
        setTimeout(() => card.classList.remove("copied"), 600);
  
      } catch (err) {
        console.error("Clipboard failed:", err);
        alert("Copie manuelle: " + hex);
      }
    });
  });
  