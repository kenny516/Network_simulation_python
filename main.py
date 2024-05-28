import tkinter as tk
from tkinter import simpledialog, ttk, messagebox

from Model.Dns import Dns
from Model.Network import Network
from Model.Server import Server


class GraphEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.network = Network()

        self.title("Graph Editor")

        self.canvas = tk.Canvas(self, bg="white", width=600, height=400)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.node_positions = {}
        self.selected_node = None
        self.selected_node_tag = None
        self.offset_x = 0
        self.offset_y = 0

        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_motion)
        self.canvas.bind("<ButtonRelease-1>", self.handle_release)
        self.canvas.bind("<Button-3>", self.handle_right_click_canvas)  # Clic droit sur le terrain

    def add_node(self, x, y, ip):
        node_id = len(self.node_positions)
        node_tag = f"node_{node_id}"
        self.node_positions[node_tag] = (x, y)
        self.canvas.create_rectangle(x - 20, y - 20, x + 20, y + 20, fill="skyblue", tags=(node_tag, "node"))
        self.canvas.tag_bind(node_tag, "<Button-3>",
                             lambda event, node=node_tag: self.handle_right_click_node(event, node))
        self.canvas.tag_bind(node_tag, "<Enter>", self.show_node_details)

        return node_tag

    def show_node_details(self, event):
        x, y = event.x, event.y
        closest_item = self.canvas.find_closest(x, y)
        if closest_item:
            item = closest_item[0]
            tags = self.canvas.gettags(item)
            if "node" in tags:
                node_tag = tags[0]  # Le premier tag correspond au tag du nœud

                dns = self.network.dns_by_node_tag(node_tag)
                detail = (f"IP: {dns.server.address_ip}\n"
                          f"Liste des sites:\n"
                          + "\n".join([f"- {site}" for site in dns.list_domain_name]))

                # Ajoutez d'autres détails si nécessaire, par exemple :
                # node_details += f"Position: {self.node_positions[node_tag]}\n"
                # node_details += f"Autre détail: {quelque_chose}\n"

                # Obtenez les coordonnées de l'icône du nœud
                node_coords = self.canvas.coords(item)
                node_center_x = (node_coords[0] + node_coords[2]) / 2  # Coordonnée x du centre
                node_center_y = (node_coords[1] + node_coords[3]) / 2  # Coordonnée y du centre

                # Affichez les détails dans un label de texte au centre de l'icône du nœud
                self.canvas.create_text(node_center_x + 100, node_center_y, text=detail, anchor=tk.CENTER,
                                        fill="black", font=("Helvetica", 10), tags="node_details")

                # Liez l'événement de sortie de la souris à une fonction pour supprimer les détails
                self.canvas.tag_bind(item, "<Leave>", lambda event, tag="node_details": self.canvas.delete(tag))

    def draw_line(self):
        dns_list = self.network.list_dns
        self.canvas.delete("connexion")
        self.canvas.delete("path")
        self.canvas.delete("server")
        for dns in dns_list:
            server = dns.server
            for voisin, path in zip(server.voisin, server.path):
                location_voisin = voisin.location
                if server.status is False or voisin.status is False:
                    self.canvas.create_line(server.location[0], server.location[1],
                                            location_voisin[0], location_voisin[1], fill='red', width=2,
                                            tags="connexion")
                else:
                    self.canvas.create_line(server.location[0], server.location[1],
                                            location_voisin[0], location_voisin[1], fill='blue', width=2,
                                            tags="connexion")
                # Assuming path is a string representing some information about the connection
                self.canvas.create_text((server.location[0] + location_voisin[0]) / 2,
                                        (server.location[1] + location_voisin[1]) / 2, text=path, tags="path")

    def draw_line_search(self, path, color):
        self.canvas.delete("connexion")
        self.draw_line()
        self.canvas.create_oval(path[0].location[0] - 10, path[0].location[1] - 10,
                                path[0].location[0] + 10, path[0].location[1] + 10,
                                fill=color, tags="server")

        self.canvas.create_oval(path[len(path) - 1].location[0] - 10, path[len(path) - 1].location[1] - 10,
                                path[len(path) - 1].location[0] + 10, path[len(path) - 1].location[1] + 10,
                                fill=color, tags="server")

        for i in range(len(path) - 1):
            self.canvas.create_line(path[i].location[0], path[i].location[1],
                                    path[i + 1].location[0], path[i
                                                                  + 1].location[1],
                                    fill=color, width=2, tags="connexion")

    def draw_line_search2(self, path1, path2, color1, color2):
        self.canvas.delete("connexion")
        self.draw_line()
        self.canvas.create_oval(path1[0].location[0] - 10, path1[0].location[1] - 10,
                                path1[0].location[0] + 10, path1[0].location[1] + 10,
                                fill=color1, tags="server")

        self.canvas.create_oval(path1[len(path1) - 1].location[0] - 10, path1[len(path1) - 1].location[1] - 10,
                                path1[len(path1) - 1].location[0] + 10, path1[len(path1) - 1].location[1] + 10,
                                fill=color1, tags="server")

        for i in range(len(path1) - 1):
            self.canvas.create_line(path1[i].location[0], path1[i].location[1],
                                    path1[i + 1].location[0], path1[i
                                                                    + 1].location[1],
                                    fill=color1, width=2, tags="connexion")
            ########################################
        self.canvas.create_oval(path2[0].location[0] - 10, path2[0].location[1] - 10,
                                path2[0].location[0] + 10, path2[0].location[1] + 10,
                                fill=color2, tags="server")

        self.canvas.create_oval(path2[len(path2) - 1].location[0] - 10, path2[len(path2) - 1].location[1] - 10,
                                path2[len(path2) - 1].location[0] + 10, path2[len(path2) - 1].location[1] + 10,
                                fill=color2, tags="server")

        for i in range(len(path2) - 1):
            self.canvas.create_line(path2[i].location[0], path2[i].location[1],
                                    path2[i + 1].location[0], path2[i
                                                                    + 1].location[1],
                                    fill=color2, width=2, tags="connexion")

    def handle_click(self, event):
        x, y = event.x, event.y
        closest_item = self.canvas.find_closest(x, y)
        if closest_item:
            item = closest_item[0]
            tags = self.canvas.gettags(item)
            if "node" in tags:
                node_x, node_y = self.canvas.coords(item)[:2]
                node_center_x = (node_x + node_x + 20) / 2
                node_center_y = (node_y + node_y + 20) / 2
                distance = ((node_center_x - x) ** 2 + (node_center_y - y) ** 2) ** 0.5
                if distance <= 20:
                    self.selected_node = item
                    self.selected_node_tag = tags[0]
                    self.offset_x = x
                    self.offset_y = y

    def handle_motion(self, event):
        if self.selected_node is not None:
            x, y = event.x, event.y
            dx = x - self.offset_x
            dy = y - self.offset_y
            self.canvas.move(self.selected_node, dx, dy)
            self.offset_x = x
            self.offset_y = y

            server_tag = self.selected_node_tag

            # Vérifiez si le tag du nœud sélectionné est correctement obtenu
            if server_tag:
                server = self.network.server_by_node_tag(server_tag)
                if server:
                    server.location = [x, y]
                    self.draw_line()

    def handle_release(self, event):
        if self.selected_node is not None:
            x, y = event.x, event.y
            self.node_positions[self.selected_node] = (x, y)
        self.draw_line()
        self.selected_node = None

    def handle_right_click_canvas(self, event):
        x, y = event.x, event.y
        self.canvas_context_menu = tk.Menu(self, tearoff=0)
        # Utilisation d'une fonction lambda pour passer des arguments à menu_server_build
        self.canvas_context_menu.add_command(label="Cree un Server",
                                             command=lambda: self.menu_server_build(x, y))
        self.canvas_context_menu.post(event.x_root, event.y_root)

    def handle_right_click_node(self, event, node):
        self.node_context_menu = tk.Menu(self, tearoff=0, font=("Helvetica", 10, "bold"))

        self.node_context_menu.add_command(label="Link Other Server",
                                           command=lambda: self.link_another_server(node, event))
        self.node_context_menu.add_command(label="Stop",
                                           command=lambda: self.change_status(node))
        self.node_context_menu.add_separator()
        self.node_context_menu.add_command(label="Add Site",
                                           command=lambda: self.create_domain_dialog(node, "add"))
        self.node_context_menu.add_command(label="List Site",
                                           command=lambda: self.show_site_server(node))
        self.node_context_menu.add_separator()
        self.node_context_menu.add_command(label="Start Find",
                                           command=lambda: self.create_domain_dialog(node, ""))

        self.node_context_menu.config(bg="lightgray")
        self.node_context_menu.post(event.x_root, event.y_root)

    def search_site(self, domain_dialog, domainsearch, node):
        domain_dialog.destroy()
        if domainsearch is not None:
            if len(domainsearch) > 0:
                dns = self.network.dns_by_node_tag(node)
                if domainsearch not in dns.list_domain_name:
                    server_dom = self.network.get_server_by_domain(domainsearch)
                    chemin = self.network.min_chemin(dns.server, server_dom)
                    cheminParcour = self.network.trouverChemin(dns.server, domainsearch)
                    if chemin is not None and cheminParcour is not None:
                        self.draw_line_search2(chemin, cheminParcour, 'green', 'red')
                    else:
                        messagebox.showinfo("Domain not found", "aucun chemin trouver parcour")

                else:
                    self.canvas.create_oval(dns.server.location[0] - 10, dns.server.location[1] - 10,
                                            dns.server.location[0] + 10, dns.server.location[1] + 10,
                                            fill="green", tags="server")
            else:
                messagebox.showinfo("Domain empty", "Enter a name of domain valid")

    def add_site(self, domain_dialog, domain_site, node):
        domain_dialog.destroy()
        if domain_site is not None:
            if len(domain_site) > 0:
                dns = self.network.dns_by_node_tag(node)
                dns.list_domain_name.append(domain_site)
                print("Site ajouté dans le serveur DNS")
            else:
                print("Aucun nom de domaine saisi.")

    def create_domain_dialog(self, node, type):
        domain_dialog = tk.Toplevel(self)
        domain_dialog.title("Add Site")

        domain_label = tk.Label(domain_dialog, text="Nom de domaine:")
        domain_label.pack()

        domain_entry = tk.Entry(domain_dialog)
        domain_entry.pack()

        domain_entry.focus_set()
        if type == "add":
            ok_button = tk.Button(domain_dialog, text="Add",
                                  command=lambda: self.add_site(domain_dialog, domain_entry.get(), node))
            ok_button.pack()
        else:
            ok_button = tk.Button(domain_dialog, text="search",
                                  command=lambda: self.search_site(domain_dialog, domain_entry.get(), node))
            ok_button.pack()

    def show_site_server(self, node):
        site_server_window = tk.Toplevel(self)
        site_server_window.title("Sélectionner un serveur")

        # Changer la taille de la fenêtre
        site_server_window.geometry("300x200")  # Par exemple, une taille de 300x200 pixels

        dns_selected = self.network.dns_by_node_tag(node)
        for domain in dns_selected.list_domain_name:
            label = tk.Label(site_server_window, text=domain)
            label.pack()

    def menu_server_build(self, x, y):
        server_ip = simpledialog.askstring("Create server", "Enter IP Address:")

        location = [x, y]
        new_server = Server(server_ip, location)

        if self.network.verify_ip_free(server_ip):
            if len(server_ip) > 0:
                node_tag = self.add_node(x, y, server_ip)
                self.selected_node = node_tag
                self.offset_x = x
                self.offset_y = y

                new_server.node_tag = node_tag
                new_dns = Dns(new_server)
                self.network.add_dns(new_dns)
                print(f"Server created with address IP : {new_server.node_tag}")
                print(f"node tagging {node_tag}")
            else:
                self.menu_server_build(x, y)
        else:
            messagebox.showinfo("ERROR", f"IP already used by another server : {server_ip}")

    def link_another_server(self, node, event):
        server_selected = self.network.server_by_node_tag(node)
        tab_server = self.network.server_other(server_selected)

        # Créer une nouvelle fenêtre avec Toplevel
        node_context_window = tk.Toplevel(self)
        node_context_window.title("Menu Contextuel")

        # Créer une frame pour contenir les boutons
        button_frame = tk.Frame(node_context_window)
        button_frame.pack(padx=10, pady=10)

        # Ajouter des boutons pour chaque serveur dans tab_server
        for idx, link in enumerate(tab_server):
            if not Server.is_voisin(server_selected, link):
                button = tk.Button(button_frame, text=f"IP : {link.address_ip} et {link.location}",
                                   command=lambda current_link=link: self.create_path(server_selected, current_link,
                                                                                      node_context_window))
                button.grid(row=idx, column=0, pady=5)

        # Placez la fenêtre à l'emplacement du clic de la souris
        node_context_window.geometry(f"+{event.x_root}+{event.y_root}")

    def create_path(self, server_main: Server, server_link: Server, liste):
        liste.destroy()
        path = simpledialog.askfloat("path", "Enter Path :")
        if path > 0:
            server_main.voisin.append(server_link)
            server_link.voisin.append(server_main)

            server_main.path.append(path)
            server_link.path.append(path)
            print(f"path enregistre pour {server_link.location}")
            print(f"path enregistre pour {server_link.address_ip}")
            self.draw_line()
        else:
            print(f"path negative or empty => {path}")

    def change_status(self, node):
        server_selected = self.network.server_by_node_tag(node)
        print(f"status current : {server_selected.status}")
        server_selected.status = not server_selected.status
        print(f"status after :  {server_selected.status}")
        self.draw_line()


if __name__ == "__main__":
    app = GraphEditor()
    app.mainloop()
