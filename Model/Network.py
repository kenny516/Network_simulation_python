import heapq
from collections import deque


class Network:
    def __init__(self):
        self.list_dns = []

    @property
    def list_dns(self):
        return self._list_dns

    @list_dns.setter
    def list_dns(self, list_dns):
        self._list_dns = list_dns

    def add_dns(self, dns):
        self._list_dns.append(dns)

    def server_by_node_tag(self, node_tag):
        for dns in self._list_dns:
            if dns.server.node_tag == node_tag:
                return dns.server

    def dns_by_node_tag(self, node_tag):
        for dns in self._list_dns:
            if dns.server.node_tag == node_tag:
                return dns

    def dns_by_node_server(self, server):
        for dns in self._list_dns:
            if dns.server.address_ip == server.address_ip:
                return dns

    def server_other(self, server_exclude):
        new_server_tab = []
        for dns in self._list_dns:
            if not dns.server.address_ip == server_exclude.address_ip:
                new_server_tab.append(dns.server)
        return new_server_tab

    def verify_ip_free(self, address_ip):
        for dns in self._list_dns:
            if dns.server.address_ip == address_ip:
                return False
        return True

    def get_server_by_domain(self, domain_name):
        new_server_tab = []
        for dns in self._list_dns:
            if domain_name in dns.list_domain_name:
                new_server_tab.append(dns.server)
        return new_server_tab

    def dijkstra(self, start_node, end_node):
        # Initialisation des distances à l'infini pour tous les nœuds sauf le nœud de départ
        distances = {node.server.address_ip: float('inf') for node in self._list_dns}
        distances[start_node.address_ip] = 0

        # File de priorité pour stocker les nœuds à explorer, basée sur les distances estimées
        priority_queue = [(0, start_node)]  # (distance estimée, nœud)

        # Dictionnaire pour suivre les prédécesseurs sur le chemin le plus court
        predecessors = {}
        current_node = None
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            # Si on a atteint le nœud de destination, terminer
            curr = self.dns_by_node_server(current_node)
            if current_node == end_node:
                print("break")
                break

            # Parcourir les voisins du nœud actuel
            for neighbor, path_cost in zip(current_node.voisin, current_node.path):
                if neighbor.status:
                    neighbor_distance = current_distance + path_cost

                    # Si le chemin actuel vers ce voisin est plus court que celui précédemment enregistré
                    if neighbor_distance < distances[neighbor.address_ip]:
                        distances[neighbor.address_ip] = neighbor_distance
                        predecessors[neighbor] = current_node
                        heapq.heappush(priority_queue, (neighbor_distance, neighbor))

        # Reconstruction du chemin le plus court
        if current_node != end_node:
            return [None, 0]

        path = []
        while current_node in predecessors:
            path.append(current_node)
            current_node = predecessors[current_node]
        path.append(start_node)
        # Inversion du chemin car il a été construit à l'envers
        path.reverse()

        return [path, distances[end_node.address_ip]]

    def min_chemin(self, server_start, server_end_tab):
        distance = float('inf')
        chemin = None
        for server_domain in server_end_tab:
            dijkstra = self.dijkstra(server_start, server_domain)
            if dijkstra[1] < distance:
                distance = dijkstra[1]
                chemin = dijkstra[0]
        return chemin

    def trouverChemin(self, start_node, domain):
        fileAttente = deque([[start_node]])
        dejaVisites = set()

        cheminsTrouves = None
        # Parcours en largeur
        while fileAttente:
            cheminCourant = fileAttente.popleft()
            sommetCourant = cheminCourant[-1]

            curr = self.dns_by_node_server(sommetCourant)

            if domain in curr.list_domain_name:
                if cheminsTrouves is None or len(cheminCourant) < len(cheminsTrouves):
                    cheminsTrouves = cheminCourant
                continue

            dejaVisites.add(sommetCourant)

            for voisin in sommetCourant.voisin:
                if voisin not in dejaVisites:
                    nouveauChemin = cheminCourant + [voisin]
                    fileAttente.append(nouveauChemin)

        return cheminsTrouves
