import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.modules.orders.model import Comanda, ComandaLumanare
from app.modules.catalog.model import Lumanare
from app.modules.erp_production.model import Material
from app.modules.analytics.schema import (
    DashboardAnalyticsResponse,
    KPISummary,
    ProductSalesPerformance,
    MaterialConsumptionReport,
)


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def calculeaza_statistici_dashboard(self) -> DashboardAnalyticsResponse:
        # --- 1. PROCESARE KPI FINANCIARI (COMENZI) ---
        comenzi_stmt = select(Comanda)
        comenzi_lista = self.db.execute(comenzi_stmt).scalars().all()

        if not comenzi_lista:
            kpis = KPISummary(
                venit_total=0.0,
                numar_comenzi=0,
                valoare_medie_comanda=0.0,
                total_lumanari_vandute=0,
            )
            return DashboardAnalyticsResponse(
                kpis=kpis, top_produse=[], consum_materiale=[]
            )

        df_comenzi = pd.DataFrame(
            [
                {"id_comanda": c.id_comanda, "total": float(c.total)}
                for c in comenzi_lista
            ]
        )

        linii_stmt = select(ComandaLumanare)
        linii_lista = self.db.execute(linii_stmt).scalars().all()
        df_linii = (
            pd.DataFrame(
                [
                    {
                        "id_lumanare": linie.id_lumanare,
                        "cantitate": linie.cantitate,
                        "pret_unitar": float(linie.pret_unitar),
                    }
                    for linie in linii_lista
                ]
            )
            if linii_lista
            else pd.DataFrame(columns=["id_lumanare", "cantitate", "pret_unitar"])
        )

        venit_total = float(df_comenzi["total"].sum())
        numar_comenzi = int(len(df_comenzi))
        valoare_medie_comanda = (
            float(df_comenzi["total"].mean()) if numar_comenzi > 0 else 0.0
        )
        total_lumanari_vandute = (
            int(df_linii["cantitate"].sum()) if not df_linii.empty else 0
        )

        kpis = KPISummary(
            venit_total=np.round(venit_total, 2),
            numar_comenzi=numar_comenzi,
            valoare_medie_comanda=np.round(valoare_medie_comanda, 2),
            total_lumanari_vandute=total_lumanari_vandute,
        )

        # --- 2. ANALIZÄ‚ PERFORMANÈšÄ‚ PRODUSE ---
        top_produse_raport = []
        if not df_linii.empty:
            df_linii["venit_linie"] = df_linii["cantitate"] * df_linii["pret_unitar"]
            df_agregat_prod = (
                df_linii.groupby("id_lumanare")
                .agg({"cantitate": "sum", "venit_linie": "sum"})
                .reset_index()
            )

            for _, row in df_agregat_prod.iterrows():
                id_lum = int(row["id_lumanare"])
                lumanare_obj = self.db.get(Lumanare, id_lum)
                if lumanare_obj:
                    top_produse_raport.append(
                        ProductSalesPerformance(
                            id_lumanare=id_lum,
                            nume_lumanare=lumanare_obj.nume,
                            sku=lumanare_obj.sku,
                            cantitate_vanduta=int(row["cantitate"]),
                            venit_generat=float(np.round(row["venit_linie"], 2)),
                        )
                    )
            top_produse_raport.sort(key=lambda x: x.venit_generat, reverse=True)

        # --- 3. RAPORT CONSUM MATERII PRIME ---
        consum_report = []
        materiale_stmt = select(Material)
        materiale_lista = self.db.execute(materiale_stmt).scalars().all()

        # Evitam utilizarea modelului inexistent si folosim o structura curata
        df_consumuri = pd.DataFrame(columns=["id_material", "cantitate_consumata"])

        for mat in materiale_lista:
            total_consumat = 0.0
            if not df_consumuri.empty:
                total_consumat = float(
                    df_consumuri[df_consumuri["id_material"] == mat.id_material][
                        "cantitate_consumata"
                    ].sum()
                )

            # Folosim atributele standard din modelul de productie detectat
            consum_report.append(
                MaterialConsumptionReport(
                    id_material=mat.id_material,
                    nume_material=getattr(
                        mat, "nume_material", getattr(mat, "nume", "Nespecificat")
                    ),
                    unitate=getattr(mat, "unitate", "g"),
                    total_consumat=float(np.round(total_consumat, 2)),
                    stoc_ramas_actual=float(
                        getattr(mat, "stoc_curent", getattr(mat, "stoc_actual", 0.0))
                    ),
                )
            )

        return DashboardAnalyticsResponse(
            kpis=kpis, top_produse=top_produse_raport, consum_materiale=consum_report
        )

