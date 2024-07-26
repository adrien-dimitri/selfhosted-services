from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.compute import Server
from diagrams.generic.network import Router
from diagrams.onprem.network import Internet
from diagrams.custom import Custom

common_cluster ={
"bgcolor":"white",
"fontsize" : "20",
"pencolor" : "brown",
"penwidth" : "1",
"orientation" : "portrait"
}

temp_cluster = {
"pencolor" : "brown",
"penwidth" : "0",
"bgcolor" : "white",
}

main_cluster ={
"labelloc" : "t",
"fontsize" : "22",
"splines" : "spline"
}

with Diagram("Home Network", outformat="png", show=False):
    router = Router("Router")
    internet = Internet("Internet")

    
    pi = Server("Raspberry Pi")
    
    with Cluster("Docker Containers", graph_attr=main_cluster):
        portainer = Custom("Portainer", "./resources/portainer.png")
        rpimonitor = Custom("RPI Monitor", "./resources/rpimonitor.png")
        
        with Cluster("172.18.0.1", graph_attr=main_cluster):
            pihole = Custom("Pi-hole", "./resources/pihole.png")
            unbound = Custom("Unbound", "./resources/unbound.png")
            pihole << Edge(label="Port 53") >> unbound
        
        with Cluster("172.22.0.1", graph_attr=main_cluster):
            nginx = Custom("Nginx", "./resources/nginx.png")
            homepage = Custom("Homepage", "./resources/homepage.png")
            nginx << Edge(label="Proxy") >> homepage

        # Connections to Raspberry Pi
        pi - [portainer, rpimonitor]
        pi - nginx
        pi - pihole

    # External internet connection
    internet - Edge() - router - Edge() - pi
        
    laptop = Custom("Laptop", "./resources/laptop.png") # https://www.flaticon.com/free-icons/computer"

    laptop - router
    laptop >> Edge(label="DNS") >> pihole

    
