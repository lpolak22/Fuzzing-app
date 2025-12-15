# Plan rada – Praktični dio projekta (Fuzzing)

Praktični dio projekta obuhvaća pripremu okruženja, implementaciju ciljnog programa, provođenje fuzzing testiranja nad datotekama i web aplikacijom te analizu dobivenih rezultata.

---

## FAZA 1 – Postavljanje virtualnog okruženja

U prvoj fazi postavljeno je izolirano testno okruženje kako bi se osigurala sigurna i kontrolirana provedba fuzzing testiranja.

Aktivnosti:
- instalacija alata **VirtualBox**
- kreiranje virtualne mašine s operativnim sustavom **Ubuntu**
- osnovna konfiguracija virtualnog sustava
- instalacija razvojnih alata (GCC/Clang, make, Git, Python)

Cilj faze:
- osigurati stabilno i ponovljivo okruženje za sigurnosno testiranje

---

## FAZA 2 – Instalacija i konfiguracija fuzzing alata

U ovoj fazi instalirani su alati potrebni za različite vrste fuzzing testiranja.

### Alati:
- **AFL++** – mutation-based fuzzing nad binarnim programima
- **Radamsa** – generiranje mutiranih ulaza
- **Python (custom skripte)** – generacijski fuzzing za web API

Aktivnosti:
- instalacija potrebnih ovisnosti
- preuzimanje i kompilacija AFL++ alata
- instalacija Radamsa alata
- provjera ispravnosti instalacije alata testnim izvršavanjem

Cilj faze:
- pripremiti alate za fuzzing nad različitim tipovima ciljeva

---

## FAZA 3 – Izrada ciljnog programa (file-based fuzzing)

U ovoj fazi izrađen je ciljni program koji obrađuje ulazne datoteke te je pogodan za fuzzing testiranje.

### Metoda fuzzinga:
- **Mutation-based fuzzing**

### Alati:
- AFL++
- Radamsa

Aktivnosti:
- implementacija jednostavnog C programa za obradu ulaznih datoteka
- namjerno uvođenje ranjivih konstrukcija (npr. buffer overflow, nedostatna provjera ulaza)
- kompilacija programa korištenjem AFL++ wrappera (`afl-gcc` / `afl-clang`)
- testiranje ciljnog programa s mutiranim ulazima

Cilj faze:
- demonstrirati kako fuzzing može otkriti greške u programima koji obrađuju datoteke

---

## FAZA 4 – Priprema testnih inputa (seed files)

Prije pokretanja file-based fuzzinga pripremljeni su početni ulazni podaci.

Aktivnosti:
- izrada minimalnih ispravnih ulaznih datoteka
- definiranje početnih seed inputa
- uključivanje edge case primjera (prazni inputi, ekstremne duljine)

Cilj faze:
- omogućiti fuzzing alatu kvalitetnu bazu za generiranje mutiranih testnih slučajeva

---

## FAZA 5 – File-based fuzzing testiranje

U ovoj fazi provedeno je fuzzing testiranje nad ciljnim programom koji obrađuje datoteke.

Aktivnosti:
- pokretanje AFL++ fuzzing procesa
- praćenje generiranih inputa i pokrivenosti koda
- detekcija i bilježenje crash slučajeva
- analiza uzroka rušenja ciljnog programa

Cilj faze:
- identificirati greške i potencijalne sigurnosne ranjivosti u programu

---

## FAZA 6 – Web fuzzing (REST API fuzzing)

U ovoj fazi provedeno je fuzzing testiranje web aplikacije kroz REST API sučelje.

### Metode fuzzinga:
- **Mutation-based fuzzing**
- **Generation-based fuzzing**

### Alati:
- **Radamsa** – mutacija payloadova
- **Custom Python skripte** – generiranje HTTP zahtjeva
- **curl / fetch** – slanje REST zahtjeva

Aktivnosti:
- identifikacija kritičnih REST endpointa (login, registracija)
- fuzzing JSON payloadova (OIB, email, lozinka, tokeni)
- testiranje neispravnih, zlonamjernih i rubnih ulaza
- testiranje zaštitnih mehanizama (reCAPTCHA, rate limiting)

Cilj faze:
- provjeriti otpornost web aplikacije na zlonamjerne i neispravne ulazne podatke

---

## FAZA 7 – Analiza rezultata fuzzing testiranja

U završnoj fazi analizirani su rezultati file-based i web fuzzing testiranja.

Aktivnosti:
- analiza crash inputa i neispravnih odgovora
- identifikacija uzroka grešaka u aplikaciji
- procjena sigurnosnog utjecaja pronađenih problema
- usporedba očekivanog i stvarnog ponašanja sustava

Cilj faze:
- razumjeti sigurnosne implikacije pronađenih grešaka i procijeniti razinu sigurnosti sustava

