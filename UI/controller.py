import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model



    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()




        """        if self._model.getNumNodi() == 0:
            self._view._txt_result.controls.append(
                ft.Text("Nessun artista ha venduto brani di questo genere in questi anni."))
            self._view.update_page()
            return"""

        # 4. stampo
        self._model.buildGraph()
        self._view._txt_result.controls.append(ft.Text("Grafo creato correttamente!", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))
        self._view._ddArtista.options.clear()
        self._view._ddArtista.value = None
        for a in self._model.getNodiOrdinati():
            self._view._ddArtista.options.append(ft.dropdown.Option(key=str(a.id), text=str(a)))

        self._view.update_page()

    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        res = self._view._txt_result.controls

        # artista con grado maggiore
        artista, grado = self._model.getGradoMax()
        res.append(ft.Text(f"Artista con grado maggiore: {artista} (grado {grado})"))

        # artista con somma dei pesi incidenti massima
        artista, peso = self._model.getIncidenti()
        res.append(ft.Text(f"Artista con somma dei pesi incidenti massima: {artista} (peso {peso})"))
        # 10 archi di peso maggiore
        res.append(ft.Text("I 10 archi di peso maggiore:"))
        for i,(n1, n2, p) in enumerate(self._model.get10(), start=1):
            res.append(ft.Text(f" {i}) {n1} – {n2}: (peso: {p})"))

        self._view.update_page()

    def handleSelezione(self, e):
        self._view._txt_result.controls.clear()

        # 1. grafo creato?
        if self._model.getNumNodi() == 0:
            self._view._txt_result.controls.append(ft.Text("Crea prima il grafo!", color="red"))
            self._view.update_page()
            return

        # 2. artista di partenza
        if self._view._ddArtista.value is None:
            self._view._txt_result.controls.append(ft.Text("Seleziona un artista di partenza!", color="red"))
            self._view.update_page()
            return
        partenza = self._model.getArtista(int(self._view._ddArtista.value))
        if partenza is None:
            self._view._txt_result.controls.append(ft.Text("Artista non presente nel grafo!", color="red"))
            self._view.update_page()
            return

        # 3. N
        try:
            N = int(self._view._txtInN.value)
        except (ValueError, TypeError):
            self._view._txt_result.controls.append(ft.Text("N deve essere un numero intero!", color="red"))
            self._view.update_page()
            return
        if N < 1:
            self._view._txt_result.controls.append(ft.Text("N deve essere un intero positivo!", color="red"))
            self._view.update_page()
            return

        # 4. ricorsione
        gruppo, totBrani = self._model.getGruppo(partenza, N)

        if len(gruppo) == 0:
            self._view._txt_result.controls.append(
                ft.Text(f"Nessun gruppo di {N} artisti a partire da {partenza}."))
            self._view.update_page()
            return

        # 5. stampo
        res = self._view._txt_result.controls
        res.append(ft.Text(f"Gruppo a partire da {partenza}:", color="green"))
        for a in sorted(gruppo, key=lambda x: x.nome):
            res.append(ft.Text(f"     {a} – {len(a.brani)} brani – {len(a.playlist)} playlist"))
        res.append(ft.Text(f"Numero totale di artisti: {len(gruppo)}"))
        res.append(ft.Text(f"Numero complessivo di brani: {totBrani}"))

        self._view.update_page()