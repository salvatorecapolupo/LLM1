# 🤖 Generatore di Testo Didattico (Mini-LLM)

Questo progetto è un semplice script in Python progettato per spiegare, nel modo più intuitivo possibile, il principio fondamentale alla base dei Large Language Models (LLM) come ChatGPT o dei suggeritori di testo degli smartphone: **prevedere la parola successiva basandosi sulla statistica e sul contesto**.

## 🧠 Come funziona? L'uso delle Catene di Markov

Per rendere il codice leggero e comprensibile senza l'uso di reti neurali complesse, questo script utilizza un approccio probabilistico basato sulle **Catene di Markov** (specificamente, un modello a N-grammi, o *Trigrammi*).

Il principio di base di una Catena di Markov applicata al testo è che **la probabilità della parola successiva dipende interamente dallo stato attuale** (le parole immediatamente precedenti).

Ecco i passaggi che esegue lo script:
1. **Lettura (Addestramento):** Il programma legge un testo di esempio e lo divide in parole.
2. **Mappatura del Contesto:** Scorre il testo a gruppi di tre parole alla volta. Salva le prime due parole come "contesto" e registra la terza parola come "conseguenza", contando quante volte si ripete.
3. **Calcolo delle Probabilità:** Se dopo le parole "Il" e "re" il testo originale prosegue con "amava" nell'80% dei casi e con "decise" nel 20% dei casi, il programma memorizza questi "pesi".
4. **Generazione:** Quando chiediamo al programma di generare un testo partendo da due parole, lui cerca nel suo dizionario, guarda le probabilità e lancia un "dado truccato" (`random.choices`) per scegliere la parola successiva. Poi fa scorrere la finestra: usa le nuove due parole finali per indovinare quella dopo ancora, creando un ciclo continuo.

## 🚀 Come usarlo

Non sono necessarie librerie esterne. È sufficiente avere Python 3 installato.

1. Clona questo repository.
2. Esegui lo script dal terminale:
   ```bash
   python generatore.py
