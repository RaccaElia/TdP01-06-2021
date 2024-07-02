import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def handle_graph(self, e):
        nodi = self._model.creaGrafo()
        self._view._ddgenes.options = list(map(lambda x: ft.dropdown.Option(x.GeneID), nodi))
        self._view.txtOut.controls.append(ft.Text(f"nodi: {self._model.grafoDetails()[0]}, archi: {self._model.grafoDetails()[1]}"))
        self._view.update_page()

    def handle_dettagli(self, e):
        geni = self._model.getAdiacenti(self._view._ddgenes.value)
        self._view.txtOut.controls.append(ft.Text(f"Geni adiacenti a {self._view._ddgenes.value}"))
        for gene in geni:
            self._view.txtOut.controls.append(ft.Text(f"{gene[0]} - {gene[1]}"))
        self._view.update_page()

    def handle_search(self, e):
        geni = self._model.simulazia(self._view._ddgenes.value, int(self._view._txtSoglia.value))
        print(geni)
        for gene in geni.keys():
            self._view.txtOut.controls.append(ft.Text(f"{gene} studiato da {geni[gene]} ingegneri"))
        self._view.update_page()
