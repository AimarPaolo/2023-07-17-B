import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []
        self._choiceProd = None

    def fillDD(self):
        for i in range(2015, 2019):
            self._view.ddyear.options.append(ft.dropdown.Option(f"{i}"))
        for p in self._model.getBrand():
            self._view.ddbrand.options.append(ft.dropdown.Option(f"{p}"))

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        brand = self._view.ddbrand.value
        year = self._view.ddyear.value
        if brand is None or year is None:
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un brand!"))
            self._view.update_page()
            return
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato!"))
        self._model.buildGraph(brand, year)
        nNodes, nEdges = self._model.getCaratteristiche()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nNodes} nodi"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo creato ha {nEdges} archi"))
        migliori3 = self._model.getMigliori3()
        dizionario=dict()
        for m in range(3):
            self._view.txt_result.controls.append(ft.Text(f"Arco da {migliori3[m][0].Product_number} a {migliori3[m][1].Product_number} con peso {migliori3[m][2]}"))
            if migliori3[m][0].Product_number not in dizionario:
                dizionario[migliori3[m][0].Product_number] = 1
            else:
                dizionario[migliori3[m][0].Product_number] += 1
            if migliori3[m][1].Product_number not in dizionario:
                dizionario[migliori3[m][1].Product_number] = 1
            else:
                dizionario[migliori3[m][1].Product_number] += 1
        n_repeated = [k for (k, v) in dizionario.items() if v > 1]
        self._view.txt_result.controls.append(
            ft.Text(f"I nodi ripetuti sono: {n_repeated}"))
        self.fillProd()
        self._view.update_page()

    def handle_path(self, e):
        if self._choiceProd is None:
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un prodotto"))
            self._view.update_page()
            return
        soluzione = self._model.getBestPath(self._choiceProd)
        for s in range(len(soluzione)-1):
            self._view.txt_result.controls.append(ft.Text(f"Da {soluzione[s].Product} a {soluzione[s+1].Product} peso = {self._model._grafo[soluzione[s]][soluzione[s+1]]['weight']}"))
        self._view.update_page()

    def fillProd(self):
        self._view.ddProdotto.options.clear()
        for prod in self._model._grafo.nodes:
            self._view.ddProdotto.options.append(ft.dropdown.Option(text=prod.Product, data=prod, on_click=self.readProd))

    def readProd(self, e):
        if e.control.data is None:
            self._choiceProd = None
        else:
            self._choiceProd = e.control.data
        print("read data")
