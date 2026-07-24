# âš™ï¸ METODÄ‚: Automatizarea Productiei si Consumului de Retete (ERP)

## 1. Rezumat Executiv
Aceasta metoda automatizeaza complet fluxul industrial de productie pentru lumÃ¢nari de tip premium.
Ea elimina introducerea manuala a stocurilor de ingrediente prin calcularea automata a consumului de materii prime (ceara, parfum, fitil) la fiecare lot nou fabricat si actualizarea corelata a inventarului in cloud-ul Neon PostgreSQL.

## 2. Logica de Business si Transformare
Atunci cÃ¢nd administratorul raporteaza fabricarea unui lot de lumÃ¢nari:
1. **Validare Input:** Sistemul verifica identitatea administratorului (JWT) si disponibilitatea ID-ului lumÃ¢narii.
2. **Calcul Consum:** Sistemul citeste reteta standard asociata acelei lumÃ¢nari (ex: o lumÃ¢nare de 200g necesita 180g ceara de soia si 20ml parfum de lavanda).
3. **Control Stoc Materii Prime:** Sistemul verifica daca in depozit exista suficiente materii prime. Daca stocul este insuficient, operatiunea este respinsa (eroare 400).
4. **Tranzactie Atomica (ACID):**
   - Creste stocul de lumÃ¢nari finite cu cantitatea lotului.
   - Scade cantitatile exacte de materii prime din tabela `materiale`.
   - ÃŽnregistreaza o linie de istoric in tabela `stock_audit_logs`.

## 3. Specificatie Schema Output (Pydantic)
Metoda garanteaza returnarea unui obiect JSON structurat:
- `id_lot`: ID-ul unic al operatiunii de productie.
- `sku_produs`: Codul unic al lumÃ¢narii fabricate.
- `cantitate_fabricata`: Numarul de bucati finite intrate in stoc.
- `status`: ÃŽntotdeauna "succes_procesat".
- `consum_detaliat`: O lista cu ID-urile materialelor si gramajele totale scazute.

## 4. Exemple de Output Garantat

### Exemplu 1: Rulare cu Succes
```json
{
  "id_lot": 1024,
  "sku_produs": "LUM-SOIA-LAV-01",
  "cantitate_fabricata": 50,
  "status": "succes_procesat",
  "consum_detaliat": [
    {"material": "Ceara de Soia", "cantitate_scazuta_g": 9000.0},
    {"material": "Parfum Lavanda", "cantitate_scazuta_ml": 1000.0}
  ]
}
```

