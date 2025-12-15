# Sažetak fuzzing testiranja

## Opseg testiranja

Fuzzing testiranje provedeno je nad sljedećim funkcionalnostima sustava:
- **Prijava korisnika (login)**
- **Registracija korisnika**


Ukupno je definirano i izvršeno **104 testna slučaja**:
- **9 test caseova za login**
- **95 test caseova za registraciju**

---

## Rezultati testiranja


| Kategorija | Broj testova |
|------------|-------------|
| Ukupan broj testova | **104** |
| Testovi koji su prošli (PASS) | **104** |
| Testovi koji su pali (FAIL) | **0** |
| Neočekivani rezultati | **0** |
| Padovi sustava (crash / HTTP 500) | **0** |

---

### Očekivani vs. neočekivani slučajevi

- **Očekivani rezultati:** 104 / 104  
  Svi testovi ponašali su se u skladu s očekivanjima definiranima u testnim scenarijima.
- **Neočekivani rezultati:** 0 / 104  
  Nisu zabilježena odstupanja, nekonzistentni odgovori niti nepredvidivo ponašanje sustava.

---

## Stabilnost i sigurnost sustava

Tijekom fuzzing testiranja:
- nije došlo do rušenja aplikacije
- nije zabilježena nijedna HTTP 500 greška
- nije došlo do zastoja (DoS)
- baza podataka nije bila ugrožena
- zlonamjerni payloadovi nisu izvršeni

Sustav je dosljedno vraćao:
- **HTTP 400** za neispravne ili zlonamjerne ulaze
- **HTTP 401** za neuspješne pokušaje prijave
- **HTTP 201** isključivo za valjane i sigurne zahtjeve

---

## Sigurnosna procjena

Na temelju provedenih fuzzing testova može se zaključiti da sustav pokazuje **visoku razinu otpornosti** na:
- SQL injection napade
- XSS napade
- manipulaciju ulaznim podacima
- neispravne i ekstremne vrijednosti
- Unicode i encoding edge caseove

### Ocjena sigurnosti sustava

**Ocjena: 9 / 10**

**Obrazloženje:**
- Sustav se ponaša stabilno i predvidivo
- Ulazni podaci su pravilno validirani
- Ne postoje kritične ranjivosti otkrivene fuzzingom
- Nema padova niti curenja informacija

Ocjena nije 10/10 isključivo zbog mogućnosti dodatnog unaprjeđenja validacijskih i sigurnosnih mehanizama.

---

## Preporuke za poboljšanje

Iako nisu pronađene kritične ranjivosti, preporučuje se:
- uvođenje **centralizirane validacije ulaza** (npr. JSON Schema)
- dodatno ograničavanje duljine svih tekstualnih polja
- strože definiranje dozvoljenih znakova za ime, prezime i adresu
- proširenje fuzzing testova na:
  - TOTP verifikaciju
  - promjenu lozinke
  - reset lozinke
- periodično automatizirano fuzzing testiranje (CI/CD)

---

## Zaključak

Fuzzing testiranje potvrdilo je da aplikacija:
- pravilno rukuje zlonamjernim i neispravnim unosima
- ne pokazuje znakove sigurnosnih propusta
- spremna je za produkcijsko okruženje uz minimalna dodatna poboljšanja

Sustav se može smatrati **sigurnim, stabilnim i robusnim** u kontekstu testiranih funkcionalnosti.
