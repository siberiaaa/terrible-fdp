import networkx as nx #para manejo de grafos
import matplotlib.pyplot as plt # para graficar

# Prim
def prim(G, start_node):
    visitados = [] # El orden de los vertices
    resultado = nx.Graph() # crea grafo

    visitados.append(start_node) # Se le agrega a la lista de visitados el nodo inicial

    while len(visitados) < len(G): # Mientras los vértices visitados sea menor a los vértices del grafo que es 15 que es igual al número de vértices
        min_peso = float('inf') # Un número infinito wao
        min_edge = ""           # Aún ninguno es el menor


        # Basicamente esta es la parte de elegir al menor
        for node in visitados: # Itera en toodos los ya visitados para elegir el menor
            for nodovecino, datos in G[node].items(): # Es casi lo mismo a G.neighbors(current_node), solo que este te trae el nodo y los datos, o sea weight
                if (nodovecino not in visitados and datos['weight'] < min_peso): # Si el nodo vecino no ha sido visitado y si su peso es el menor 
                    min_peso = datos['weight']
                    min_edge = (node, nodovecino)

        if (min_edge != ""): # Si tiene un valor minimo
            node = min_edge[0]
            nodovecino = min_edge[1] # equivalente     node, nodovecino = min_edge
            
            resultado.add_edge(node, nodovecino, weight=min_peso) # Misma sintaxis para añadirle 
            visitados.append(nodovecino) # Se añadie a la lista de visitados 

    # Imprimir los vértices en el orden que se agregaron
    print("Vértices en el orden que se agregaron:")
    for node in resultado.nodes():
        print(node)

    return resultado


# Kruskal
def kruskal(G):
    resultado = nx.Graph()

    aristas = [] # Donde se guardan todos los aristas que se van a iterar
    for u, v, datos in G.edges(data=True): # Se llena la lista con una tupla de los datos de los vertices y el peso
        aristas.append((u, v, datos))
    
    aristasordenadas = []
    # Básicamente ordenar en orden de peso los aristas
    for i in range (len(aristas)): 
        minweight = float('inf')
        minindex = -1
        index = -1
        for arista in aristas:
            index += 1
            if (arista[2]['weight'] < minweight):
                minweight = arista[2]['weight'] 
                minindex = index
        aristasordenadas.append(aristas.pop(minindex))
    
    conjuntos = {nodo: [nodo] for nodo in G.nodes()}  # Diccionario para guardar los conjuntos de nodos que vendría a ser como los "visitados". Le crearía un diccionario a cada nodo. Basicamente un diccionario de conjuntos
    aristas_added = []  # Aquí se almacena en que orden fueron agregadas las aristas

    # Para más información de esta parte buscar en Wikipedia Estructura de datos para conjuntos disjuntos
    # Lo que sigue es el unir y buscar subconjuntos
    for u, v, datos in aristasordenadas: #Accede al nodo inicial y nodo final y datos que tiene weight
        if conjuntos[u] != conjuntos[v]:  # Verificar si los nodos están en conjuntos diferentes
            resultado.add_edge(u, v, weight=datos['weight']) #Añade la arista al grafo
            aristas_added.append((u, v))  # Agregar la arista al registro
            conjunto_u = conjuntos[u] #  Asignar los conjuntos a estas variables para posterior manipulacion                                                            
            conjunto_v = conjuntos[v]
            
            # Unir los conjuntos de nodos
            for nodo in conjunto_v: # Para cada nodo en el conjunto v 
                conjunto_u.append(nodo) # Añadirle al conjunto u los nodos del conjunto v
                conjuntos[nodo] = conjunto_u # En el diccionario de cada nodo que esta en el conjunto v se va a igualar al conjunto u (justo en ese estado)

    # Imprimir el orden de las aristas agregadas
    print("Orden en que fueron agregadas las aristas:")
    for edge in aristas_added:
        print(edge)

    return resultado


#Algoritmo Búsqueda por Anchura ABA (breadth first search)
def aba(G, StartNode):
    nodosvisitados = {node: False for node in G.nodes} # Se crea diccionario con valores iniciales en false todos los nodos de G
    fila = [StartNode] # Una fila ("cola") donde primer elemento sera el nodo inicial (como una fila al revés?)
    nodosvisitados[StartNode] = True # nodo inicial se coloca como visitado
    result = [] # Donde se guardaria el grafo resultante
    diccionario = {node: [] for node in G.nodes} # Diccionario para guardar los nodos recorridos
 
    while len(fila) >= 1: # Mientras haya elementos en la fila       while fila
        current_node = fila.pop(0) # pop el primer elemento de la fila
        result.append(current_node) # Agrega el nodo actual al resultado

        for node in G.neighbors(current_node):  # Por cada nodo vecino del vértice actual
            if (not nodosvisitados[node]): # Si el nodo no ha sido visitado
                fila.append(node) # Se agrega a la fila
                nodosvisitados[node] = True # Y se marca como visitado para que no vaya a agregarse con otro vértice y por ende hacer un ciclo
                diccionario[current_node].append(node) # Para efectos del grafo indicamos que estos nodos se "derivan" del nodo actual

    print("Resultado del recorrido ABA: ", result)
    return diccionario # Devuelve el diccionario con los nodos recorridos


#Algoritmo Búsqueda en Profundidad ABP (depth first search)
def abp(G, StartNode):
    nodosvisitados = {node: False for node in G.nodes} # Se crea diccionario con valores iniciales en false todos los nodos de G
    fila = [StartNode] # Una fila ("cola") donde primer elemento sera el nodo inicial
    resultado = [] # Donde se guardaria el orden en el que han sido agregado los vertices
    diccionario = {node: [] for node in G.nodes} #Donde se guardaria el grafo resultante. En esta inicialización basicamente agrega todos los grafos con su lista (de relaciones) vacia

    while len(fila) >= 1: #Mientras haya elementos en la fila  TODO: while fila
        current_node = fila[-1]  #Se ubica en el próximo nodo sin sacarlo de la pila               #El problema antes era que lo sacaba y no podía retroceder si hacía falta.
        if not nodosvisitados[current_node]:
            resultado.append(current_node)
            nodosvisitados[current_node] = True #Si no ha sido visitado ese nodo, se coloca el visitado en true y se agrega a el vértice a resultados.

        #Carga una lista de nodos vecinos con los nodos vecinos del vértice actual que NO hayan sido visitados
        nodosvecinos = [] 
        for node in G.neighbors(current_node):
            if (not nodosvisitados[node]):
                nodosvecinos.append(node)
        #neighbors = [node for node in G.neighbors(current_node) if not nodosvisitados[node]] TODO:
        
        if (len(nodosvecinos) >= 1): #Si nodosvecinos no visitados tiene elementos
            siguientenodo = nodosvecinos[0] #El siguiente nodo para aplicar el algoritmo será el que está en primera posición de los nodosvecinos no visitados
            diccionario[current_node].append(siguientenodo) #Para efectos del grafo indicamos que este siguiente nodo se "deriva" del nodo actual
            fila.append(siguientenodo) #Se termina de establecer el siguiente vértice a ubicarse agregando en la fila este siguiente nodo
        else:
            fila.pop()  # Si no hay vecinos no visitados, "retrocede un vértice", sacando el último elemento en la fila

    print("Resultado del recorrido ABP: ", resultado)
    return diccionario


#printing
def printgraph(graph):
    print("Cierra la ventana para continuar...")
    pos=nx.spring_layout(graph, seed=4)
    nx.draw_networkx(graph,pos)
    labels = nx.get_edge_attributes(graph,'weight')
    nx.draw_networkx_edge_labels(graph,pos,edge_labels=labels)
    plt.show()


if __name__ == "__main__":
    graph = nx.Graph() #crea grafo
    listadevertices = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "P"]
    graph.add_nodes_from(listadevertices)
    listadeponderaciones = [("A", "B", 8), ("A", "E", 4), ("A", "D", 5), ("D", "H", 6),
                        ("D", "E", 9), ("E", "B", 12), ("E", "F", 3), ("E", "J", 5),
                        ("E", "I", 8), ("H", "I", 2), ("H", "M", 7), ("I", "M", 6),
                        ("I", "J", 10), ("M", "N", 2), ("N", "J", 9), ("J", "K", 6),
                        ("N", "P", 12), ("P", "K", 7), ("P", "L", 6), ("L", "G", 7),
                        ("L", "K", 5), ("K", "G", 8), ("K", "F", 8), ("F", "G", 1),
                        ("F", "C", 9), ("F", "B", 4), ("B", "C", 3), ("C", "G", 11)]
    graph.add_weighted_edges_from(listadeponderaciones)

    respuesta = 0
    while respuesta != "6":
        respuesta = input("Selecciona una opción\n[1]ABP\n[2]ABA\n[3]Kruskal\n[4]Prim\n[5]Visualizar grafo cargado\n[6]Salir\n\n")
        if respuesta == "1":
            printgraph(nx.Graph(abp(graph, "A")))
        elif respuesta == "2":
            printgraph(nx.Graph(aba(graph, "A")))
        elif respuesta == "3":
            printgraph(kruskal(graph))
        elif respuesta == "4":
            printgraph(prim(graph, "A"))
        elif respuesta == "5":
            printgraph(graph)
        elif respuesta == "6":
            print("Saliendo...")
        else:
            print("Opcion incorrecta")

            print("Saliendo...")
        else:
            print("Opcion incorrecta")
