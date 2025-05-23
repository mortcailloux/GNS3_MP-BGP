import json


def links_in_AS(AS):
    routers = AS["routeurs"]
    links = []
    processed = set()  # Pour éviter de traiter deux fois le même lien

    for router_src, interfaces in routers.items(): # Parcours de chaque routeur source et de ses interfaces
        for intf_src, info_src in interfaces.items():
            router_dest, metric_src = info_src[0], info_src[1]
            if router_dest in routers: # Liens internes (destination dans la même AS)
                key = tuple(sorted([router_src, router_dest])) # Clé unique du lien pour éviter les doublons (sans tenir compte de l'ordre)
                if key not in processed:
                    # Recherche de l'interface sur le routeur destination qui pointe vers src
                    intf_dest, metric_dest = None, None
                    for intf_dest_temp, info_dest in routers[router_dest].items():
                        if info_dest[0] == router_src:
                            intf_dest, metric_dest = intf_dest_temp, info_dest[1]
                            break
                    if intf_dest is not None:
                        if metric_src != metric_dest:
                            print(f"Info : Les métriques sont différentes pour le lien {router_src} <-> {router_dest} : {metric_src} vs {metric_dest}")
                        if router_src < router_dest: # Routeur avec le nom "le plus petit" en premier
                            links.append([router_src, intf_src, router_dest, intf_dest, metric_src])
                        else:
                            links.append([router_dest, intf_dest, router_src, intf_src, metric_src])
                        processed.add(key)
    return links


if __name__=="__main__":
    with open('fichier_intention.json', 'r') as file:
        intent_data = json.load(file)
# Traitement de chaque AS
#for AS_number, AS_data in intent.items():
    #print("AS", AS_number, links_in_AS(AS_data))

# Résultat de la fonction links_in_AS(AS) avec intent_lite.json
# AS 1 [['R1', 'GigabitEthernet1/0', 'R2', 'FastEthernet0/0', 10], ['R1', 'GigabitEthernet2/0', 'R3', 'GigabitEthernet1/0', 0], ['R2', 'GigabitEthernet1/0', 'R3', 'GigabitEthernet2/0', 0]]
# AS 2 [['R4', 'FastEthernet0/0', 'R5', 'GigabitEthernet1/0', 0], ['R4', 'GigabitEthernet2/0', 'R6', 'GigabitEthernet2/0', 0], ['R5', 'GigabitEthernet2/0', 'R6', 'GigabitEthernet1/0', 0]]