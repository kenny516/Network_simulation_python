class Dns:
    def __init__(self, server):
        self.server = server
        self.list_domain_name = []

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, server):
        self._server = server

    @property
    def list_domain_name(self):
        return self._list_domain_name

    @list_domain_name.setter
    def list_domain_name(self, list_domain_name):
        self._list_domain_name = list_domain_name

    @staticmethod
    def find_server_by_domain(dns, domain):
        server_match = []
        for domain_self in dns.list_domain_name:
            if domain_self == domain:
                server_match.append(dns.server)
        return server_match
