document.getElementById('imagen_usuario').addEventListener('change', function () {
  const file = this.files[0];
  const preview = document.getElementById('preview-imagen');
  const errorDiv = document.getElementById('error-imagen');
  errorDiv.textContent = '';

  if (file) {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/jpg'];
    if (!allowedTypes.includes(file.type)) {
      errorDiv.textContent = 'Solo se permiten imágenes JPG, PNG, GIF o WEBP.';
      this.value = '';
      preview.src = "https://acortar.link/xrxnFa";
      return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
      preview.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});