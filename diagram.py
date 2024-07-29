from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.compute import Server
from diagrams.generic.network import Router
from diagrams.onprem.network import Internet
from diagrams.custom import Custom

# Custom styles for clusters
network_cluster_attr = {
    "bgcolor": "#f0f8ff",  # AliceBlue background for networks
    "fontsize": "20",
    "pencolor": "#4682b4",  # SteelBlue color for cluster borders
    "penwidth": "2",
    "style": "rounded",  # Rounded corners
    "fillcolor": "#e6f2ff"  # Very light blue
}

subnetwork_cluster_attr = {
    "bgcolor": "#e0f8f8 ",  # AliceBlue background for networks
    "fontsize": "18",
    "pencolor": "#4682b4",  # SteelBlue color for cluster borders
    "penwidth": "2",
    "style": "rounded",  # Rounded corners
    "fillcolor": "#e6f2ff"  # Very light blue
}

container_cluster_attr = {
    "bgcolor": "#ffffff",  # White background for containers
    "fontsize": "18",
    "pencolor": "#32cd32",  # LimeGreen color for cluster borders
    "penwidth": "2",
    "style": "solid",  # Solid borders
    "fillcolor": "#f2f9f2"  # Very light green
}

with Diagram("Home Network", outformat="png", show=False):
    router = Router("Router")
    internet = Internet("Internet")

    pi = Server("Raspberry Pi")

    with Cluster("Docker Containers", graph_attr=network_cluster_attr):
        with Cluster("Portainer", graph_attr=container_cluster_attr):
            portainer = Custom(":9000", "./resources/portainer.png")
        
        with Cluster("RPI Monitor", graph_attr=container_cluster_attr):
            rpimonitor = Custom(":8888", "./resources/rpimonitor.png")

        with Cluster("Watchtower", graph_attr=container_cluster_attr):
            watchtower = Custom(":8080", "./resources/watchtower.png")

        with Cluster("Subnet 172.18.0.1", graph_attr=subnetwork_cluster_attr):
            with Cluster("Pi-hole", graph_attr=container_cluster_attr):
                pihole = Custom(":80", "./resources/pihole.png")
            with Cluster("Unbound", graph_attr=container_cluster_attr):
                unbound = Custom(":53", "./resources/unbound.png")
            pihole << Edge(xlabel="Port 53", color="#ff4500") >> unbound

        with Cluster("Subnet 172.22.0.1", graph_attr=subnetwork_cluster_attr):
            with Cluster("Docker Proxy", graph_attr=container_cluster_attr):
                dockerproxy = Custom("127.0.0.1:2375", "./resources/dockerproxy.png")
            with Cluster("Nginx", graph_attr=container_cluster_attr):
                nginx = Custom(":9000", "./resources/nginx.png")

            # Services behind Nginx proxy
            with Cluster("Homepage", graph_attr=container_cluster_attr):
                homepage = Custom(":3000", "./resources/homepage.png")
            with Cluster("Glances", graph_attr=container_cluster_attr):
                glances = Custom(":61208", "./resources/glances.png")
            with Cluster("Kopia", graph_attr=container_cluster_attr):
                kopia = Custom(":51515", "./resources/kopia.png")

            # Connect services to Nginx
            nginx >> Edge(xlabel="/", style="dotted", color="#4682b4") >> homepage

        # Connection from Pi to Nginx
        pi >> Edge(color="#32cd32", style="solid") >> nginx

        # Docker Socket Proxy connections
        homepage << Edge(xlabel="Socket", color="#ff6347", style="dotted") >> dockerproxy

        # Homepage widgets redirecting to other container web UIs
        homepage >> Edge(style="solid", color="#1e90ff") >> portainer
        homepage >> Edge(style="solid", color="#1e90ff") >> rpimonitor
        homepage >> Edge(style="solid", color="#1e90ff") >> pihole
        homepage >> Edge(style="solid", xlabel="/glances/", color="#1e90ff") >> glances
        homepage >> Edge(style="solid", xlabel="/kopia/", color="#1e90ff") >> kopia

    # External internet connection
    internet - Edge(color="#4682b4") - router - Edge(color="#4682b4") - pi

    laptop = Custom("Laptop", "./resources/laptop.png")  # https://www.flaticon.com/free-icons/computer

    laptop - router
    laptop - Edge(xlabel="DNS", style="dotted", color="#4682b4") - pihole
