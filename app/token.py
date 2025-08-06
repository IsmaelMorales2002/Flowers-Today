from django.contrib.auth.tokens import PasswordResetTokenGenerator

class GenerarToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, usuario, timestamp):
        return f"{usuario.id_usuario}{timestamp}{usuario.usuario_activo}"

token_generator = GenerarToken()