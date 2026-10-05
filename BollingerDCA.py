import backtrader as bt

class BollingerMeanReversion(bt.Strategy):
    params = (
        ('p_bband', 20),
        ('p_dev', 2.0),
        ('p_rsi', 14),
        ('dias_espera_reentrada', 10),
        ('max_entradas', 4),
        ('p_sma_visual', 100)
    )

    def __init__(self):
        # Mapeo de lineas de precios de la primera data
        self.dataclose = self.datas[0].close
        self.datalow = self.datas[0].low
        self.order = None

        # Indicadores
        self.bband = bt.indicators.BollingerBands(
            self.data, period=self.params.p_bband, devfactor=self.params.p_dev
        )
        self.rsi = bt.indicators.RSI(self.data, period=self.params.p_rsi)
        self.sma_visual = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.p_sma_visual, plotname='SMA 100'
        )

        # Estado DCA
        self.num_entradas = 0
        self.dias_desde_ultima_compra = 0
        self.precio_ultima_compra = 0.0

    def next(self):
        if self.order:
            return

        if self.position:
            self.dias_desde_ultima_compra += 1

        # 1. PRIMERA ENTRADA (25% del capital con filtro de Cash Real)
        if not self.position:
            # Corrección: Se evalúa si el MÍNIMO de la vela anterior perforó la banda
            salio_abajo = self.datalow[-1] < self.bband.lines.bot[-1]
            reingreso = self.dataclose[0] > self.bband.lines.bot[0]
            rsi_valido = self.rsi[-1] < 50

            if salio_abajo and reingreso and rsi_valido:
                # Mejora: Validación estricta de Cash disponible
                cash_disponible = self.broker.getcash()
                capital_destino = min(self.broker.getvalue() * 0.24, cash_disponible)
                tamano_lote = int(capital_destino / self.dataclose[0])

                if tamano_lote > 0:
                    self.order = self.buy(size=tamano_lote)
                    self.num_entradas = 1
                    self.dias_desde_ultima_compra = 0
                    self.precio_ultima_compra = self.dataclose[0]

        # 2. RECOMPRAS ESCALONADAS (DCA)
        elif self.num_entradas < self.params.max_entradas:
            hizo_espera = self.dias_desde_ultima_compra >= self.params.dias_espera_reentrada
            precio_mas_bajo = self.dataclose[0] < self.precio_ultima_compra

            if hizo_espera and precio_mas_bajo:
                cash_disponible = self.broker.getcash()
                capital_destino = min(self.broker.getvalue() * 0.24, cash_disponible)
                tamano_lote = int(capital_destino / self.dataclose[0])

                if tamano_lote > 0:
                    self.order = self.buy(size=tamano_lote)
                    self.num_entradas += 1
                    self.dias_desde_ultima_compra = 0
                    self.precio_ultima_compra = self.dataclose[0]

        # 3. SALIDA EN GANANCIA
        if self.position:
            precio_promedio = self.position.price
            esta_en_positivo = self.dataclose[0] > precio_promedio
            alcanzo_banda_top = self.dataclose[0] >= self.bband.lines.top[0]
            rsi_sobrecompra = self.rsi[0] >= 60

            if esta_en_positivo and (alcanzo_banda_top or rsi_sobrecompra):
                self.order = self.close()

    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Margin, order.Rejected]:
            self.order = None