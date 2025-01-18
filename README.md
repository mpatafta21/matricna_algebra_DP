Prije pokretanja projekta, osigurajte sljedeće:
- **Operacijski sustav**: Ubuntu (ili kompatibilni Linux sustavi) na virtualnoj mašini.
- **Preglednik**: Google Chrome (ili kompatibilni preglednik).
- **Python**: Verzija 3.10 ili novija.
- **Prolog**: Instaliran XSB Prolog.
- **Virtualno okruženje (venv)**: Za izolaciju Python ovisnosti.
- **Instaliran Flask**

- ## Postavljanje

Slijedite ove korake kako biste pokrenuli aplikaciju:

### 1. Preuzimanje projekta
Preuzmite projekt s GitHub repozitorija

### 2. Kreirajte i aktivirajte Python virtualno okruženje (ako se nalazite na virtualnoj mašini)
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Promjena putanje do XSB datoteke
Osigurajte da putanja do XSB Prologa u Python datoteci (app.py) odgovara stvarnoj putanji na vašem sustavu.

Provjerite ovu liniju u app.py:

```python
process = subprocess.Popen(
    ["/putanja/do/xsb/bin/xsb", "--noprompt"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
```
### 4. U terminalu navigirajte do mape projekta i pokrenite Flask aplikaciju upisom sljedeće naredbe:
```bash
python app.py
```
Aplikacija će biti dostupna na adresi: http://127.0.0.1:5000.

### 5. Pokrenite preglednik i otvorite adresu http://127.0.0.1:5000

### 6.  odgovarajuća polja unesite matrice u sljedećem formatu:
Svaki red unosi se u novi redak.

Elementi u jednom retku odvajaju se razmakom.

Svi redovi moraju imati isti broj elemenata.

### 7. Kliknite na odgovarajući gumb za operaciju


   
