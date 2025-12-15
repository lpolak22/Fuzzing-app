# 🛡️ Izvještaj o Testiranju Sigurnosti: Analiza Fuzzinga

## 1. 🎯 Uvod i Ciljevi Fuzzinga

### 1.1 Cilj Testiranja
Definiranje glavnog cilja primjene *Fuzzing* metodologije na softver [Naziv Vaše Aplikacije].
* **Primarni cilj:** Identificirati *crashove* i *hangove* (zamrzavanja) uzrokovane neočekivanim, malicioznim ili *malformiranim* korisničkim ulazom.
* **Sekundarni cilj:** Mjeriti otpornost ciljane komponente te poboljšati *code coverage* (pokrivenost koda) sigurnosnim testovima unutar CI/CD cjevovoda.

### 1.2 Ciljana Komponenta (Target)
* **Komponenta:** [Npr. Modul za obradu slika, parser JSON zahtjeva, CLI ulazni vektor].
* **Jezik:** [Npr. C, C++, Python].
* **Alat:** [Npr. AFL++, LibFuzzer, Honggfuzz].

---

## 2. ⚙️ Metodologija Fuzzinga

### 2.1 Konfiguracija Fuzzera
Detaljan opis postavljanja alata za fuziranje unutar okruženja.
* **Fuzzer Tip:** [Npr. *Coverage-guided* fuzzer]
* **Okruženje:** Izvršeno u izoliranom Docker kontejneru ([Detalji Docker slike]).
* **Sjeme (Seed Corpus):** Korišteni set početnih ulaznih datoteka za fuzer. [Npr. 50 validnih, ali raznolikih JSON datoteka].

### 2.2 Integracija u CI/CD Cjevovod
Kako je *Fuzzing* faza integrirana u Jenkins pipeline. 
* **Pipeline Faza:** Fuzzing se izvodi kao *post-build* faza nakon Unit Testova.
* **Trajanje:** Svako izvođenje je ograničeno na [Npr. 15 minuta] zbog performansi CI/CD-a.

---

## 3. 📊 Rezultati i Analiza Učinkovitosti

### 3.1 Ključni Metrički Podaci
Prikaz ključnih mjernih podataka nakon izvršavanja Fuzzinga.

| Metrika | Vrijednost | Napomena |
| :--- | :--- | :--- |
| **Ukupno testirano ulaza** | [Npr. 5,432,109] | Broj generiranih i testiranih ulaza. |
| **Postignuti Code Coverage** | [Npr. 78.5%] | Postotak koda koji je Fuzzer uspio dosegnuti. |
| **Pronađeni *Crash* događaji** | **[Broj]** | *Uncontrolled Memory Access*, *Assertion Failure*, itd. |
| **Pronađeni *Hang* događaji** | [Broj] | Potencijalni *Denial of Service* (DoS). |

### 3.2 Analiza Kritičnih Ranijivosti
Opis najozbiljnijih pronađenih problema.

* **[Naziv Greške / Bug ID]:** [Npr. Heap Buffer Overflow u parseru datoteka]
    * **Komponenta:** [Npr. `parser.c`]
    * **Posljedica:** Potencijalno daljinsko izvršavanje koda (RCE).
    * **Status:** **Riješeno** (Patchiran kod u commitu [Hash]).

* **[Naziv Greške 2]:** [Opis]

---

## 4. 📝 Zaključak i Ukupni Dojam

### 4.1 Učinkovitost Fuzzing Metodologije
Kratka procjena uspješnosti.
* Fuzzing se pokazao **iznimno učinkovitim** u pronalasku grešaka koje su *Unit* i *Integration* testovi propustili, posebno u neobrađenim graničnim slučajevima.

### 4.2 Budući Smjerovi za Sigurnosno Testiranje
Prijedlozi za proširenje.
* **Poboljšanje Sjemena (Corpus):** Redovita obnova sjemena novim, relevantnim ulazima.
* **Duže izvršavanje:** Pokretanje dugotrajnog, noćnog Fuzzinga (izvan CI/CD cjevovoda) s većim resursima.
* **Dodatni Alati:** Integracija alata za statičku analizu koda (SAST) u Pipeline.