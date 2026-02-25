import collections
import random

# 1. Il nostro testo di addestramento (Corpus)
testo = """
C'era una volta un re che viveva in un grande castello. 
Il re amava molto passeggiare nel bosco vicino al castello. 
Nel bosco vicino c'era anche una piccola casa dove viveva un mago. 
Un giorno il re decise di andare a trovare il mago. 
Il mago era famoso perché sapeva leggere le stelle e prevedere il futuro. 
Quando il re arrivò alla piccola casa, vide che il mago stava leggendo un grosso libro. 
Il mago alzò gli occhi e disse: benvenuto mio re, sapevo che saresti venuto. 
Il re domandò: come facevi a saperlo? 
Il mago rispose: ho letto le stelle, e le stelle non mentono mai. 
Così il re e il mago parlarono per ore del futuro del regno. 
Il re amava molto ascoltare le storie del mago saggio.
"""

# Pulizia e tokenizzazione (divisione in parole)
testo_pulito = testo.lower().replace('.', ' .').replace(',', ' ,').replace(':', ' :').replace('?', ' ?')
parole = testo_pulito.split()

# 2. Addestramento del Modello (Catena di Markov del secondo ordine / Trigrammi)
modello = collections.defaultdict(collections.Counter)

for i in range(len(parole) - 2):
    contesto = (parole[i], parole[i+1])
    parola_successiva = parole[i+2]
    modello[contesto][parola_successiva] += 1

# 3. La funzione di generazione
def genera_paragrafo(parola1, parola2, lunghezza_massima=30):
    frase_generata = [parola1.lower(), parola2.lower()]
    
    for _ in range(lunghezza_massima):
        contesto_attuale = (frase_generata[-2], frase_generata[-1])
        
        if contesto_attuale in modello:
            # Estraiamo le opzioni e le loro frequenze (pesi)
            opzioni = list(modello[contesto_attuale].keys())
            pesi = list(modello[contesto_attuale].values())
            
            # Scegliamo la parola successiva rispettando le probabilità statistiche
            parola_scelta = random.choices(opzioni, weights=pesi)[0]
            frase_generata.append(parola_scelta)
        else:
            break # Fine della generazione se il contesto è sconosciuto
            
    # Formattazione finale per rendere la frase leggibile
    testo_finale = " ".join(frase_generata)
    testo_finale = testo_finale.replace(" .", ".").replace(" ,", ",").replace(" :", ":").replace(" ?", "?")
    return testo_finale

# --- Esecuzione del codice ---
if __name__ == "__main__":
    print("--- Generatore di Testo Basato su Markov ---")
    print("Inizio: 'Il re'")
    print("Risultato:", genera_paragrafo("il", "re"))
    print("-" * 40)
    print("Inizio: 'Nel bosco'")
    print("Risultato:", genera_paragrafo("nel", "bosco"))
