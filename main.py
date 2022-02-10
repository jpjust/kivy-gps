from plyer import gps
from kivy.app import App
from kivy.uix.label import Label
from kivy.utils import platform

# Classe principal
class MyApp(App):

    # Label para exibição das informações
    lbCoordenadas = Label(text="Aguarde...")

    # Inicialização do app
    def build(self):

        # Se a plataforma for Android, solicita as permissões de localização
        if platform == "android":
            self.request_android_permissions()

        # Configura os callbacks e inicia o módulo gps
        try:
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            gps.start(1000, 0)
        except NotImplementedError:
            self.lbCoordenadas.text = "GPS não suportado nesta plataforma."

        # Retorna o Label para exibição das coordenadas
        return self.lbCoordenadas

    # Call back de localização
    def on_location(self, **kwargs):
        self.lbCoordenadas.text = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

    # Callback de informação de status
    def on_status(self, stype, status):
        print(stype, status)

    # Solicitação de permissões
    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            if all([res for res in results]):
                print("Todas as permissões foram concedidas.")
            else:
                print("Algumas permissões não foram concedidas.")

        request_permissions(
            [Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION],
            callback
        )

# Início do programa
if __name__ == "__main__":
    MyApp().run()
