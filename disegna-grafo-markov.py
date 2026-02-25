import collections
import networkx as nx
import matplotlib.pyplot as plt

# 1. Testo super-ridotto per creare bivi perfetti (2/3 da una parte, 1/3 dall'altra)
testo = """
il gatto mangia il pesce
il gatto mangia la carne
il gatto dorme sul divano
"""

parole = testo.split()

# Calcolo del Modello a Trigrammi
modello = collections.defaultdict(collections.Counter)
for i in range(len(parole) - 2):
    contesto = f"{parole[i]} {parole[i+1]}"
    modello[contesto][parole[i+2]] += 1

# 2. Costruzione dell'Albero (partendo da una frase iniziale)
G = nx.DiGraph()
contesto_iniziale = "il gatto"

# Aggiungiamo la radice dell'albero al "livello 0"
G.add_node("radice", layer=0, label=contesto_iniziale)

# Funzione per espandere i rami dell'albero livello per livello
def espandi_albero(contesto_attuale, id_padre, livello, max_livelli=2):
    if livello >= max_livelli:
        return
        
    conteggi = modello.get(contesto_attuale, {})
    if not conteggi: 
        return
    
    totale = sum(conteggi.values())
    seconda_parola_contesto = contesto_attuale.split()[1]
    
    for parola_successiva, conteggio in conteggi.items():
        probabilita = (conteggio / totale) * 100
        
        # Creiamo un ID univoco per il nodo (es. "1_mangia") per non far incrociare i rami
        id_figlio = f"L{livello}_{parola_successiva}"
        
        # Aggiungiamo il nodo specificando a quale "colonna" (layer) appartiene
        G.add_node(id_figlio, layer=livello + 1, label=parola_successiva)
        
        # Disegniamo il ramo dal padre al figlio con la probabilità
        G.add_edge(id_padre, id_figlio, label=f"{probabilita:.0f}%")
        
        # Calcoliamo il nuovo contesto e andiamo avanti al livello successivo
        nuovo_contesto = f"{seconda_parola_contesto} {parola_successiva}"
        espandi_albero(nuovo_contesto, id_figlio, livello + 1, max_livelli)

# Facciamo crescere l'albero per 2 livelli successivi
espandi_albero(contesto_iniziale, "radice", 0)

# 3. Disegno dell'Albero Gerarchico (da sinistra a destra)
plt.figure(figsize=(12, 6))

# multipartite_layout forza i nodi a mettersi in colonne separate in base al "layer"
pos = nx.multipartite_layout(G, subset_key="layer")

# Estraiamo le etichette pulite per i nodi
etichette_nodi = nx.get_node_attributes(G, 'label')

# Disegniamo i rettangoli/nodi
nx.draw(G, pos, labels=etichette_nodi, with_labels=True, 
        node_color='lightyellow', node_size=4000, edgecolors='orange',
        font_size=12, font_weight='bold', arrows=True, arrowsize=20, width=2)

# Disegniamo le percentuali sulle frecce
etichette_frecce = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=etichette_frecce, 
                             font_color='black', font_size=10, font_weight='bold',
                             bbox=dict(facecolor='white', edgecolor='lightgray', boxstyle='round,pad=0.2'))

plt.title("Albero Decisionale dell'LLM (Partendo da: 'il gatto')", fontsize=16, pad=20)
plt.margins(0.15)

# Salviamo l'immagine
plt.savefig("albero_decisionale.png", format="PNG", dpi=300, bbox_inches='tight')
print("Immagine 'albero_decisionale.png' creata con successo!")