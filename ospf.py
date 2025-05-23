"""
module qui sert à générer les commandes pour ospf sur les routeurs
"""
from BGP import get_as_for_router


def config_ospf(router_id,router_name, process_id, graphe,numAs, cost=0):
    """
    Args:
        str: l'id du routeur
        int: l'id du process
        graphe: le graphe du réseau
        int: la métrique du lien (0 si valeur pas défaut)

    Returns:
        list: liste des commandes pour configurer OSPF sur les routeurs
    """
    commands = ["conf t"]
    # Generate the router OSPF configuration commands
    commands.append(f"router ospf {process_id}")
    commands.append("mpls ldp autoconfig")
    commands.append(f"router-id {router_id}")
    commands.append("exit")

    # Generate interface-specific OSPF commands for neighbor_list
    dico_voisins = graphe[numAs]["routeurs"][router_name]
    
    for interface in dico_voisins.keys():
        voisin=dico_voisins[interface][0]
        as_voisin=get_as_for_router(voisin,graphe)
        if as_voisin!=int(numAs):
            continue #on ne config pas OSPF si le lien est inter AS

         #on peut récupérer directement le nom de l'interface dans le dictionnaire
        commands.append(f"interface {interface}")
        commands.append(f"ip ospf {process_id} area 0")
        if cost:
            commands.append(f"ip ospf cost {cost}")
        commands.append("exit")
        
    interface="Loopback0" #on configure aussi la loopback pour l'IGP
    commands.append(f"interface {interface}")
    commands.append(f"ip ospf {process_id} area 0")
    if cost:
        commands.append(f"ip ospf cost {cost}")
    commands.append("exit")
    
    commands.append("exit")
    return commands

