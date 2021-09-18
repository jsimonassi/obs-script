import socket
import threading
import time
import obspython as obs


class Server:

    def __init__(self):
        try:
            self.host = socket.gethostbyname(socket.gethostname())
            self.port = 5001
            self.buffer = 1024
            self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.is_live = True
            self.client_list = []
            orig = (self.host, self.port)
            self.udp.bind(orig)
            print("Socket iniciado no IP: " + self.host + " e na porta: " + str(self.port))
            thread = threading.Thread(target=self.listen, args=())
            thread.start()
        except Exception as e:
            print("Erro no bind do servidor: " + str(e))

    def listen(self):
        try:
            while self.is_live:
                msg, client = self.udp.recvfrom(self.buffer)
                decoded_msg = str(msg.decode())
                print(client, str(msg))

                if "add" in decoded_msg:
                    self.client_list.append(client)
                    print("Cliente adicionado: " + str(client))
                    current_scene_names = obs.obs_frontend_get_scene_names()
                    self.udp.sendto((str(current_scene_names)).encode(), client)
                elif "remove" in decoded_msg:
                    self.client_list.remove(client)
                    print("Cliente removido: " + str(client))


        except Exception as e:
            print("Erro ao receber informação do cliente: " + str(e))

    def send_broadcast(self, msg):
        print("Enviando broadcast com: " + str(msg))
        try:
            for client in self.client_list:
                print("Enviando para: " + str(client))
                self.udp.sendto(msg.encode(), client)

        except Exception as e:
            print("Erro ao enviar broadcast: " + str(e))


def init_scene_listener(server_instance):
    time.sleep(5) # Espera para montar as cenas
    last_scene = ""
    while server_instance.is_live:
        scenes = obs.obs_frontend_get_scenes()
        current_scene = obs.obs_frontend_get_current_scene()
        current_scene_index = 0
        for i in range(len(scenes)):
            if scenes[i] == current_scene:
                current_scene_index = i

        scenes_names = obs.obs_frontend_get_scene_names()
        current_scene_str = str(scenes_names[current_scene_index])
        if current_scene_str != last_scene:
            last_scene = current_scene_str
            server_instance.send_broadcast(current_scene_str)

        time.sleep(1) #Testa a cada 1 segundo


## OBS METHODS
def script_load(settings):
    # Todo: Enviar mudanças do obs
    print("executando script")
    global server_instance
    server_instance = Server()
    thread = threading.Thread(target=init_scene_listener, args=(server_instance,))
    thread.start()


def script_description():
    return f"<h1>OBS Current Scene</h1>\
            <p>Este script cria um servidor que envia continuamente informações via rede local sobre a cena atual.</p>\
            <p>O cliente pode se conectar com as seguintes informações: </p>\
            <h2>IP: {socket.gethostbyname(socket.gethostname())}</h2>\
            <h2>PORTA: 5001</h2><br/>\
            <small>Desenvolvido por: João Victor Simonassi </small><br/>\
            <small>Em caso de bugs, entrar contato via email: jsimonassi@id.uff.br </small><br/>\
            <small>PASCOM - Paróquia São Pedro Apóstolo | Venda das Pedras - Itaboraí, RJ </small><br/>"


def script_unload():
    server_instance.is_live = False
    server_instance.udp.close()

