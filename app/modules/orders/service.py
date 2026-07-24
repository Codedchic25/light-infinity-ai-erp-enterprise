"""
Serviciul de business pentru gestionarea comenzilor si a stocurilor.
Implementeaza logica tranzactionala de checkout cu decrementare automata de stoc.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.modules.orders.model import Comanda, ComandaLumanare
from app.modules.orders.schema import CheckoutInput
from app.modules.catalog.model import Lumanare


class OrdersService:
    """
    Clasa centralizata pentru gestionarea checkout-ului si a stocurilor corelate.
    """

    def __init__(self, db: Session):
        self.db = db

    def plaseaza_comanda(self, checkout_in: CheckoutInput, id_user: int) -> Comanda:
        """
        Proceseaza cosul de cumparaturi, valideaza stocurile, le scade si salveaza comanda.
        Ruleaza intr-o singura tranzactie SQL atomica (ACID).
        """
        total_comanda = 0.0
        produse_de_salvat = []

        # Parcurgem fiecare produs din cosul trimis de client
        for item in checkout_in.produse:
            # Cautam produsul direct in tabela de lumÃ¢nari
            lumanare = (
                self.db.query(Lumanare)
                .filter(Lumanare.id_lumanare == item.id_lumanare)
                .first()
            )

            if not lumanare:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"LumÃ¢narea cu ID-ul {item.id_lumanare} nu mai exista in catalog.",
                )

            # BARIERÄ‚ DE STOC: Verificam daca avem suficiente bucati in depozit
            if lumanare.stoc < item.cantitate:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stoc insuficient pentru '{lumanare.nume}'. Disponibil: {lumanare.stoc} buc, Solicitat: {item.cantitate} buc.",
                )

            # AUTOMATIZARE STOC: Scadem fizic cantitatea din inventarul cloud Neon
            lumanare.stoc -= item.cantitate

            # Calculam pretul partial si acumulam in totalul comenzii
            pret_articol = lumanare.pret * item.cantitate
            total_comanda += pret_articol

            # Pregatim rÃ¢ndul pentru tabela de legatura (istoric comanda)
            produse_de_salvat.append(
                {
                    "id_lumanare": lumanare.id_lumanare,
                    "cantitate": item.cantitate,
                    "pret_salvat": lumanare.pret,
                }
            )

        # Cream antetul comenzii generale
        db_comanda = Comanda(
            id_user=id_user, status="in_asteptare", total=round(total_comanda, 2)
        )
        self.db.add(db_comanda)
        self.db.flush()  # Generam ID-ul comenzii fara a inchide tranzactia inca

        # Salvam detaliile fiecarui produs in tabela de legatura
        for prod in produse_de_salvat:
            db_detaliu = ComandaLumanare(
                id_comanda=db_comanda.id_comanda,
                id_lumanare=prod["id_lumanare"],
                cantitate=prod["cantitate"],
                pret_salvat=prod["pret_salvat"],
            )
            self.db.add(db_detaliu)

        # Salvam permanent toate modificarile in cloud (commit atomic)
        self.db.commit()
        self.db.refresh(db_comanda)

        return db_comanda

    def get_comenzi_utilizator(self, id_user: int) -> list[Comanda]:
        """Returneaza istoricul de comenzi ale unui anumit client."""
        return self.db.query(Comanda).filter(Comanda.id_user == id_user).all()

    def get_toate_comenzile_erp(self) -> list[Comanda]:
        """Metoda administrativa: returneaza absolut toate comenzile pentru panoul ERP."""
        return self.db.query(Comanda).all()

