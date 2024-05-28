class Server:
    def __init__(self, address_ip, location):
        self.address_ip = address_ip
        self.status = True
        self.location = location
        self.voisin = []
        self.path = []
        self.node_tag = None

    @property
    def address_ip(self):
        return self._address_ip

    @address_ip.setter
    def address_ip(self, value):
        self._address_ip = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def voisin(self):
        return self._voisin

    @voisin.setter
    def voisin(self, value):
        self._voisin = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def node_tag(self):
        return self._node_tag

    @node_tag.setter
    def node_tag(self, value):
        self._node_tag = value

    def voisin_server_path(self, server):
        server_and_path = []
        for i in range(len(self.voisin)):
            if self.voisin[i].address_ip == server.address_ip:
                server_and_path.append(self.voisin[i])
                server_and_path.append(self.path[i])
                return server_and_path
        return server_and_path

    def remove_voisin(self, server):
        self.voisin.remove(server)

    @staticmethod
    def is_voisin(server, new_voisin):
        for i in range(len(server.voisin)):
            if server.voisin[i].address_ip == new_voisin.address_ip:
                return True
        return False
