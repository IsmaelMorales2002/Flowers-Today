    // Ventas últimos 6 meses
    const ctxMeses = document.getElementById('ventasMesesChart').getContext('2d');
    new Chart(ctxMeses, {
        type: 'line',
        data: {
            labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
            datasets: [{
                label: 'Ventas',
                data: [120, 150, 180, 130, 170, 200],
                borderColor: '#ffc107',
                backgroundColor: 'hsla(45, 100.00%, 51.40%, 0.20)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            plugins: { legend: { labels: { color: '#fff' } } },
            scales: {
                x: { ticks: { color: '#fff' }, grid: { color: '#444' } },
                y: { ticks: { color: '#fff' }, grid: { color: '#444' } }
            }
        }
    });

    // Ventas de la semana
    const ctxSemana = document.getElementById('ventasSemanaChart').getContext('2d');
    new Chart(ctxSemana, {
        type: 'bar',
        data: {
            labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
            datasets: [{
                label: 'Ventas',
                data: [20, 35, 40, 25, 50, 60, 30],
                backgroundColor: '#6C2DC7'
            }]
        },
        options: {
            plugins: { legend: { labels: { color: '#fff' } } },
            scales: {
                x: { ticks: { color: '#fff' }, grid: { color: '#444' } },
                y: { ticks: { color: '#fff' }, grid: { color: '#444' } }
            }
        }
    });

    // Productos más vendidos de la semana
    const ctxProductos = document.getElementById('productosVendidosChart').getContext('2d');
    new Chart(ctxProductos, {
        type: 'doughnut',
        data: {
            labels: ['Rosa Roja', 'Lirio Blanco', 'Orquídea', 'Ramo Primavera', 'Tulipán'],
            datasets: [{
                label: 'Cantidad vendida',
                data: [30, 25, 20, 15, 10],
                backgroundColor: [
                    '#ffc107', '#0d6efd', '#dc3545', '#198754', '#6f42c1'
                ]
            }]
        },
        options: {
            plugins: { legend: { labels: { color: '#fff' } } }
        }
    });

    // DataTable
    $(document).ready(function() {
        $('#tablaExistencias').DataTable({
            language: {
                url: 'https://cdn.datatables.net/plug-ins/2.3.2/i18n/es-ES.json',
            }
        });
    });