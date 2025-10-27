document.addEventListener('DOMContentLoaded', () => {
  // === Ventas por mes ===
  const ctxMes = document.getElementById('graficoVentasTotales');
  if (ctxMes) {
    new Chart(ctxMes, {
      type: 'line',
      data: {
        labels: mesesLabels,
        datasets: [
          {
            label: 'Ventas de productos ($)',
            data: ventasProductosDatos,
            borderColor: '#FFC107',
            backgroundColor: 'rgba(255,193,7,0.2)',
            fill: true,
            tension: 0.4,
            borderWidth: 2,
            pointRadius: 4
          },
          {
            label: 'Servicios (cantidad)',
            data: ventasServiciosDatos,
            borderColor: '#20C997',
            backgroundColor: 'rgba(32,201,151,0.25)',
            fill: true,
            tension: 0.4,
            borderWidth: 2,
            pointRadius: 4
          }
        ]
      },
      options: {
        plugins: { legend: { labels: { color: '#fff' } } },
        scales: {
          x: { ticks: { color: '#fff' }, grid: { color: '#444' } },
          y: { ticks: { color: '#fff' }, grid: { color: '#444' } }
        }
      }
    });
  }

  // (Se eliminó el gráfico de pastel de comprobantes)

  // === Top productos por CANTIDAD (más vendidos) ===
  const ctxTopCant = document.getElementById('graficoTopProductosCantidad');
  if (ctxTopCant) {
    new Chart(ctxTopCant, {
      type: 'bar',
      data: {
        labels: productosLabels,
        datasets: [{
          label: 'Unidades vendidas',
          data: productosCantidades,
          backgroundColor: 'rgba(13,110,253,0.6)', // azul bootstrap
          borderColor: '#0D6EFD',
          borderWidth: 1,
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y', // barras horizontales
        plugins: {
          legend: { labels: { color: '#fff' } },
          tooltip: { callbacks: { label: (ctx) => ` ${ctx.raw} uds` } }
        },
        scales: {
          x: { ticks: { color: '#fff' }, grid: { color: '#444' } },
          y: { ticks: { color: '#fff' }, grid: { color: '#444' } }
        }
      }
    });
  }
});
