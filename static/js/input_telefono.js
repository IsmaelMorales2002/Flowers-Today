const telefono = document.getElementById('telefono');

telefono.addEventListener('input', function () {
  this.value = this.value.replace(/[^0-9]/g, '');
});

telefono.addEventListener('keypress', function (e) {
  if (!/[0-9]/.test(e.key)) {
    e.preventDefault();
  }
});