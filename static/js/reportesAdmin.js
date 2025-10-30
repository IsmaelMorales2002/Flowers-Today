(function () {
  const modal = document.getElementById('modal-fechas');
  const inputEndpoint = document.getElementById('rp-endpoint');
  const inputDesde = document.getElementById('fecha_desde');
  const inputHasta = document.getElementById('fecha_hasta');
  const btnPreview = document.getElementById('btn-preview');
  const btnPdf = document.getElementById('btn-export-pdf');
  const btnXlsx = document.getElementById('btn-export-xlsx');

  function buildUrl(endpoint, params) {
    const base = `/reportes/export/${endpoint}/`;
    const usp = new URLSearchParams(params);
    return usp.toString() ? `${base}?${usp.toString()}` : base;
  }

  function getParamsOrAll() {
    const d = inputDesde.value;
    const h = inputHasta.value;

    // Si ambos vacíos -> todo
    if (!d && !h) return {};

    // Si uno vacío -> inválido
    if ((d && !h) || (!d && h)) {
      alert('Si defines una fecha, completa ambas: Desde y Hasta. O deja ambas vacías para exportar todo.');
      return null;
    }

    // Si ambos completos, validar orden
    if (h < d) {
      alert('La fecha "Hasta" no puede ser menor que "Desde".');
      return null;
    }
    return { desde: d, hasta: h };
  }

  if (modal) {
    modal.addEventListener('show.bs.modal', function (ev) {
      const btn = ev.relatedTarget;
      const endpoint = btn?.getAttribute('data-endpoint') || '';
      inputEndpoint.value = endpoint;
      inputDesde.value = '';
      inputHasta.value = '';
    });
  }

  if (btnPreview) {
    btnPreview.addEventListener('click', function () {
      const params = getParamsOrAll();
      if (params === null) return;
      params.format = 'html';
      const endpoint = inputEndpoint.value;
      const url = buildUrl(endpoint, params);
      window.open(url, '_blank');
    });
  }

  if (btnPdf) {
    btnPdf.addEventListener('click', function () {
      const params = getParamsOrAll();
      if (params === null) return;
      params.format = 'pdf';
      const endpoint = inputEndpoint.value;
      const url = buildUrl(endpoint, params);
      window.open(url, '_blank');
    });
  }

  if (btnXlsx) {
    btnXlsx.addEventListener('click', function () {
      const params = getParamsOrAll();
      if (params === null) return;
      params.format = 'xlsx';
      const endpoint = inputEndpoint.value;
      const url = buildUrl(endpoint, params);
      window.open(url, '_blank');
    });
  }

  document.querySelectorAll('[data-no-dates="1"]').forEach(btn => {
    btn.addEventListener('click', function () {
      const endpoint = btn.getAttribute('data-endpoint');
      const format = btn.getAttribute('data-format') || 'pdf';
      const url = buildUrl(endpoint, { format });
      window.open(url, '_blank');
    });
  });
})();
