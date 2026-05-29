// dashboard.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('pipelineForm');
  const resultContainer = document.getElementById('resultContainer');
  const traceOutput = document.getElementById('traceOutput');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const guestName = document.getElementById('guestName').value.trim();
    const guestNiche = document.getElementById('guestNiche').value.trim();
    const guestCompany = document.getElementById('guestCompany').value.trim();

    const payload = {
      guest_name: guestName,
      guest_niche: guestNiche || undefined,
      guest_company: guestCompany || undefined,
    };

    try {
      const response = await fetch('/research/full-pipeline', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();

      // Display the step‑by‑step trace
      resultContainer.classList.remove('hidden');
      const steps = data.steps ?? [];
      let pretty = '';
      steps.forEach((step, idx) => {
        pretty += `Step ${idx + 1} – ${step.stage}\n`;
        pretty += `Model: ${step.model}\n`;
        pretty += `Output (truncated): ${JSON.stringify(step.output).slice(0, 500)}${JSON.stringify(step.output).length > 500 ? '…' : ''}\n`;
        pretty += '\n';
      });
      traceOutput.textContent = pretty;
    } catch (err) {
      resultContainer.classList.remove('hidden');
      traceOutput.textContent = 'Error running pipeline: ' + err;
    }
  });
});
