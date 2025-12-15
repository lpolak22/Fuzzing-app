# Definirani testni scenariji

Tijekom fuzzing testiranja identificirani su sljedeći testni scenariji:

1. Ispravna struktura zahtjeva s neispravnim vjerodajnicama  
2. Nedostajući obavezni parametri  
3. Neispravan format ulaznih podataka  
4. Zlonamjerni i specijalni znakovi u inputu  
5. Prekoračenje duljine ulaznih polja  
6. Manipulacija reCAPTCHA tokenom  

Svaki scenarij testiran je pomoću velikog broja mutiranih ulaza generiranih fuzzing alatom.

## Test Caseovi – Prijava korisnika
| Test Case ID | Testni Scenarij | Steps to Reproduce | Expected Behavior | Actual Behavior |
|-------------|----------------|--------------------|-------------------|-----------------|
| TC-LOGIN-01 | Neispravni OIB i lozinka | 1. Poslati POST zahtjev na `/login` <br> 2. U tijelu zahtjeva poslati ispravan JSON <br> 3. Unijeti nepostojeći OIB i proizvoljnu lozinku | Sustav treba odbiti prijavu i vratiti HTTP 401 bez dodatnih informacija | Sustav vraća HTTP 401 i poruku o neispravnim podacima |
| TC-LOGIN-02 | Nedostaje OIB | 1. Poslati POST zahtjev <br> 2. Izostaviti parametar `oib` iz JSON-a | Sustav treba vratiti HTTP 400 s porukom o nedostajućim podacima | Sustav vraća HTTP 400 s odgovarajućom porukom |
| TC-LOGIN-03 | Nedostaje lozinka | 1. Poslati POST zahtjev <br> 2. Izostaviti parametar `password` | Sustav treba prekinuti obradu i vratiti HTTP 400 | Sustav ispravno vraća HTTP 400 |
| TC-LOGIN-04 | Prazni stringovi | 1. Poslati POST zahtjev <br> 2. Postaviti `oib` i `password` kao prazne stringove | Sustav treba odbiti zahtjev kao neispravan | Sustav vraća HTTP 400 |
| TC-LOGIN-05 | Specijalni znakovi u OIB-u | 1. Poslati POST zahtjev <br> 2. U `oib` unijeti znakove poput `'";--<>` | Sustav treba validirati ulaz i odbiti zahtjev | Sustav vraća HTTP 400 bez rušenja |
| TC-LOGIN-06 | Predugačak OIB | 1. Poslati POST zahtjev <br> 2. U `oib` unijeti niz od >11 znakova | Sustav treba sigurno odbiti zahtjev | Sustav odbija zahtjev, bez greške ili zastoja |
| TC-LOGIN-07 | SQL-like payload | 1. Poslati POST zahtjev <br> 2. Unijeti `oib: "' OR 1=1 --"` | Sustav mora spriječiti SQL injection | Sustav ispravno odbija zahtjev |
| TC-LOGIN-08 | Neispravan reCAPTCHA token | 1. Poslati POST zahtjev <br> 2. Postaviti `recaptchaToken` na slučajni string | Sustav treba odbiti zahtjev s HTTP 400 | Sustav ispravno vraća HTTP 400 |
| TC-LOGIN-09 | Nedostaje reCAPTCHA token | 1. Poslati POST zahtjev bez `recaptchaToken` | Sustav treba odbiti zahtjev | Sustav odbija zahtjev |


### Analiza ponašanja sustava

Rezultati fuzzing testiranja pokazali su da se sustav ponaša stabilno i predvidivo u svim testiranim scenarijima. Nijedan testni slučaj nije rezultirao rušenjem aplikacije, HTTP 500 greškom ili gubitkom dostupnosti servisa.

Ocekivano ponasanje
- Odbijanje neispravnih i nepotpunih zahtjeva
- Ispravna validacija ulaznih podataka
- Aktivacija mehanizma zaključavanja nakon više neuspješnih pokušaja
- Zaštita od SQL injection napada

Neočekivana zapažanja
- Nije bilo neočekivanih zapažanja u Fuzz testu


Sigurnosna procjena
- Na temelju provedenih fuzzing testova može se zaključiti da login funkcionalnost posjeduje visoku razinu otpornosti na neispravne i zlonamjerne ulazne podatke. Sustav nije pokazao znakove ranjivosti koje bi omogućile neovlašteni pristup ili uskraćivanje usluge (DoS).

Preporuka za poboljšanje
- Uvesti strogu validaciju ulaza pomoću shema (npr. JSON Schema)
- Izbjegavati reflektiranje korisničkog inputa u porukama o greškama
- Centralizirati obradu grešaka
- Proširiti fuzzing testove na TOTP i promjenu lozinke



## Test Caseovi – Registracija korisnika

| ID | Endpoint | Polje | Payload | Očekivano ponašanje | Stvarni rezultat | Status | Napomena |
|----|----------|-------|---------|---------------------|------------------|--------|----------|
| R1 | /api/register | oib | 88721173004 | Sustav treba prihvatiti ispravan OIB | HTTP 201 Created | PASS | Ispravan OIB |
| R2 | /api/register | phone | 88721173004 | Sustav treba validirati broj telefona | HTTP 400 Bad Request | PASS | Neispravan format |
| R3 | /api/register | password | lucija123 | Lozinka treba biti hashirana i prihvaćena | HTTP 201 Created | PASS | bcrypt ispravno radi |
| R4 | /api/register | name | lucija123 | Ime s brojkama treba biti odbijeno | HTTP 400 Bad Request | PASS | Validacija imena |
| R5 | /api/register | oib | (prazno) | Sustav mora odbiti prazan OIB | HTTP 400 Bad Request | PASS | Obavezno polje |
| R6 | /api/register | name | \n | Sustav mora odbiti kontrolne znakove | HTTP 400 Bad Request | PASS | Nevažeći znak |
| R7 | /api/register | address | \n | Sustav mora odbiti kontrolne znakove | HTTP 400 Bad Request | PASS | Nevažeći unos |
| R8 | /api/register | name | \t | Sustav mora odbiti kontrolne znakove | HTTP 400 Bad Request | PASS | Nevažeći unos |
| R9 | /api/register | address | \t | Sustav mora odbiti kontrolne znakove | HTTP 400 Bad Request | PASS | Nevažeći unos |
| R10 | /api/register | name | ' | Sustav mora odbiti specijalne znakove | HTTP 400 Bad Request | PASS | SQL/XSS zaštita |
| R11 | /api/register | surname | ' | Sustav mora odbiti specijalne znakove | HTTP 400 Bad Request | PASS | SQL/XSS zaštita |
| R12 | /api/register | address | ' | Sustav mora odbiti specijalne znakove | HTTP 400 Bad Request | PASS | Sigurnosna validacija |
| R13 | /api/register | email | ' | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | Validacija emaila |
| R14 | /api/register | password | ' | Sustav mora odbiti lozinku | HTTP 400 Bad Request | PASS | Sigurnosna validacija |
| R15 | /api/register | confirm-password | ' | Sustav mora odbiti potvrdu lozinke | HTTP 400 Bad Request | PASS | Neispravan unos |
| R16 | /api/register | name | " | Sustav mora odbiti specijalne znakove | HTTP 400 Bad Request | PASS | Validacija |
| R17 | /api/register | surname | " | Sustav mora odbiti specijalne znakove | HTTP 400 Bad Request | PASS | Validacija |
| R18 | /api/register | address | " | Sustav mora odbiti specijalne znakove | HTTP 400 Bad Request | PASS | Validacija |
| R19 | /api/register | email | " | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | Validacija |
| R20 | /api/register | password | " | Sustav mora odbiti lozinku | HTTP 400 Bad Request | PASS | Sigurnost |
| R21 | /api/register | confirm-password | " | Sustav mora odbiti potvrdu lozinke | HTTP 400 Bad Request | PASS | Neispravno |
| R22 | /api/register | address | \ | Sustav mora odbiti escape znak | HTTP 400 Bad Request | PASS | Sigurnost |
| R23 | /api/register | name | \ | Sustav mora odbiti escape znak | HTTP 400 Bad Request | PASS | Sigurnost |
| R24 | /api/register | surname | \ | Sustav mora odbiti escape znak | HTTP 400 Bad Request | PASS | Sigurnost |
| R25 | /api/register | email | / | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | Validacija |
| R26 | /api/register | address | / | Sustav mora odbiti neispravan format | HTTP 400 Bad Request | PASS | Validacija |
| R27 | /api/register | address | // | Sustav mora odbiti path-like input | HTTP 400 Bad Request | PASS | Path traversal zaštita |
| R28 | /api/register | address | .. | Sustav mora odbiti path-like input | HTTP 400 Bad Request | PASS | Sigurnost |
| R29 | /api/register | address | ../ | Sustav mora odbiti path traversal | HTTP 400 Bad Request | PASS | Sigurnost |
| R30 | /api/register | oib | ; | Sustav mora odbiti nevažeći OIB | HTTP 400 Bad Request | PASS | Validacija |
| R31 | /api/register | email | ; | Sustav mora odbiti nevažeći email | HTTP 400 Bad Request | PASS | Validacija |
| R32 | /api/register | name | \| | Sustav mora odbiti specijalni znak | HTTP 400 Bad Request | PASS | Sigurnost |
| R33 | /api/register | address | \| | Sustav mora odbiti specijalni znak | HTTP 400 Bad Request | PASS | Sigurnost |
| R34 | /api/register | password | $( | Sustav mora odbiti command-like input | HTTP 400 Bad Request | PASS | Command injection spriječena |
| R35 | /api/register | name | $( | Sustav mora odbiti command-like input | HTTP 400 Bad Request | PASS | Sigurnost |
| R36 | /api/register | name | ` | Sustav mora odbiti command-like input | HTTP 400 Bad Request | PASS | Sigurnost |
| R37 | /api/register | password | ` | Sustav mora odbiti command-like input | HTTP 400 Bad Request | PASS | Sigurnost |
| R38 | /api/register | email | # | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | Validacija |
| R39 | /api/register | name | A | Sustav treba prihvatiti jedno slovo | HTTP 201 Created | PASS | Minimalna duljina |
| R40 | /api/register | surname | A | Sustav treba prihvatiti jedno slovo | HTTP 201 Created | PASS | Minimalna duljina |
| R41 | /api/register | name | A' | Sustav mora odbiti specijalni znak | HTTP 400 Bad Request | PASS | Sigurnost |
| R42 | /api/register | surname | A' | Sustav mora odbiti specijalni znak | HTTP 400 Bad Request | PASS | Sigurnost |
| R43 | /api/register | name | A" | Sustav mora odbiti specijalni znak | HTTP 400 Bad Request | PASS | Sigurnost |
| R44 | /api/register | surname | A" | Sustav mora odbiti specijalni znak | HTTP 400 Bad Request | PASS | Sigurnost |
| R45 | /api/register | name | A( | Sustav mora odbiti nevažeći znak | HTTP 400 Bad Request | PASS | Validacija |
| R46 | /api/register | surname | A( | Sustav mora odbiti nevažeći znak | HTTP 400 Bad Request | PASS | Validacija |
| R47 | /api/register | password | AAAAA' | Sustav mora odbiti lozinku | HTTP 400 Bad Request | PASS | Sigurnost |
| R48 | /api/register | confirm-password | AAAAA' | Sustav mora odbiti potvrdu | HTTP 400 Bad Request | PASS | Sigurnost |
| R49 | /api/register | password | A'*1000 | Sustav mora odbiti predugu lozinku | HTTP 400 Bad Request | PASS | Boundary test |
| R50 | /api/register | password | A"*1000 | Sustav mora odbiti predugu lozinku | HTTP 400 Bad Request | PASS | Boundary test |
| R51–R62 | /api/register | SQLi payloadi | razni | Sustav mora spriječiti SQL injection | HTTP 400 Bad Request | PASS | Parametrizirani upiti |
| R63–R75 | /api/register | XSS payloadi | razni | Sustav ne smije izvršiti skriptu | HTTP 400 Bad Request | PASS | XSS spriječena |
| R76–R79 | /api/register | template/command | razni | Sustav mora odbiti unos | HTTP 400 Bad Request | PASS | Sigurnost |
| R80–R84 | /api/register | Unicode | razni | Sustav mora ostati stabilan | HTTP 400 | PASS | UTF-8 stabilnost |
| R85–R95 | /api/register | numeric edge | razni | Sustav mora odbiti nevažeće vrijednosti | HTTP 400 | PASS | Granice podataka |
| R51 | /api/register | oib | 1 OR 1=1 -- | Sustav mora spriječiti SQL injection | HTTP 400 Bad Request | PASS | Parametrizirani upiti |
| R52 | /api/register | email | 1 OR 1=1 -- | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | Validacija emaila |
| R53 | /api/register | oib | 1' OR 1=1 -- | Sustav mora spriječiti SQL injection | HTTP 400 Bad Request | PASS | SQLi spriječena |
| R54 | /api/register | email | 1' OR 1=1 -- | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | SQLi payload |
| R55 | /api/register | oib | ' OR '1'='1 | Sustav mora spriječiti SQL injection | HTTP 400 Bad Request | PASS | Sigurnosna validacija |
| R56 | /api/register | email | ' OR '1'='1 | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | SQLi payload |
| R57 | /api/register | email | " OR "1"="1" | Sustav mora odbiti SQL injection pokušaj | HTTP 400 Bad Request | PASS | SQLi spriječena |
| R58 | /api/register | email | ' OR 1=1-- | Sustav mora odbiti SQL injection | HTTP 400 Bad Request | PASS | Sigurnosna provjera |
| R59 | /api/register | password | admin'-- | Sustav mora odbiti neispravnu lozinku | HTTP 400 Bad Request | PASS | SQLi u lozinci |
| R60 | /api/register | email | admin'-- | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | Validacija |
| R61 | /api/register | password | '; DROP TABLE users;-- | Sustav mora spriječiti destruktivne SQL naredbe | HTTP 400 Bad Request | PASS | SQL injection spriječena |
| R62 | /api/register | email | '; DROP TABLE users;-- | Sustav mora odbiti zlonamjerni unos | HTTP 400 Bad Request | PASS | Baza nije ugrožena |
| R63 | /api/register | name | <script>alert(1)</script> | Sustav ne smije izvršiti skriptu | HTTP 400 Bad Request | PASS | XSS spriječena |
| R64 | /api/register | surname | <script>alert(1)</script> | Sustav ne smije izvršiti skriptu | HTTP 400 Bad Request | PASS | XSS spriječena |
| R65 | /api/register | address | <script>alert(1)</script> | Sustav mora odbiti XSS payload | HTTP 400 Bad Request | PASS | Sigurnosna validacija |
| R66 | /api/register | email | <script>alert(1)</script> | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | XSS payload |
| R67 | /api/register | password | <script>alert(1)</script> | Sustav mora odbiti zlonamjernu lozinku | HTTP 400 Bad Request | PASS | XSS spriječena |
| R68 | /api/register | confirm-password | <script>alert(1)</script> | Sustav mora odbiti zlonamjerni unos | HTTP 400 Bad Request | PASS | Sigurnosna validacija |
| R69 | /api/register | name | <img src=x onerror=alert(1)> | Sustav ne smije izvršiti HTML event | HTTP 400 Bad Request | PASS | XSS spriječena |
| R70 | /api/register | address | <img src=x onerror=alert(1)> | Sustav mora odbiti HTML payload | HTTP 400 Bad Request | PASS | XSS spriječena |
| R71 | /api/register | email | <img src=x onerror=alert(1)> | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | XSS payload |
| R72 | /api/register | name | <svg/onload=alert(1)> | Sustav ne smije izvršiti SVG | HTTP 400 Bad Request | PASS | XSS spriječena |
| R73 | /api/register | email | <svg/onload=alert(1)> | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | XSS payload |
| R74 | /api/register | name | "><script>alert(1)</script> | Sustav mora odbiti XSS kombinaciju | HTTP 400 Bad Request | PASS | XSS spriječena |
| R75 | /api/register | email | "><script>alert(1)</script> | Sustav mora odbiti zlonamjerni email | HTTP 400 Bad Request | PASS | XSS payload |
| R76 | /api/register | name | ${7*7} | Sustav mora odbiti template injection | HTTP 400 Bad Request | PASS | Template injection spriječena |
| R77 | /api/register | email | ${7*7} | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | Template payload |
| R78 | /api/register | name | ls -la | Sustav mora odbiti command-like input | HTTP 400 Bad Request | PASS | Command injection spriječena |
| R79 | /api/register | email | ls -la | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | Command payload |
| R80 | /api/register | name | čćžšđ | Sustav mora ispravno obraditi UTF-8 | HTTP 400 Bad Request | PASS | UTF-8 stabilnost |
| R81 | /api/register | surname | čćžšđ | Sustav mora ispravno obraditi UTF-8 | HTTP 400 Bad Request | PASS | UTF-8 stabilnost |
| R82 | /api/register | address | čćžšđ | Sustav mora ostati stabilan | HTTP 400 Bad Request | PASS | UTF-8 stabilnost |
| R83 | /api/register | name | 𝓐𝓑𝓒 | Sustav mora odbiti nevažeće Unicode znakove | HTTP 400 Bad Request | PASS | Unicode edge case |
| R84 | /api/register | email | 𝓐𝓑𝓒 | Sustav mora odbiti neispravan email | HTTP 400 Bad Request | PASS | Unicode edge case |
| R85 | /api/register | oib | 00000000000 | Sustav mora odbiti nevažeći OIB | HTTP 400 Bad Request | PASS | Logička validacija |
| R86 | /api/register | phone | 00000000000 | Sustav mora odbiti nevažeći broj | HTTP 400 Bad Request | PASS | Validacija |
| R87 | /api/register | oib | 123 | Sustav mora odbiti prekratak OIB | HTTP 400 Bad Request | PASS | Boundary test |
| R88 | /api/register | phone | 123 | Sustav mora odbiti prekratak broj | HTTP 400 Bad Request | PASS | Boundary test |
| R89 | /api/register | oib | 999999999999999 | Sustav mora odbiti predug OIB | HTTP 400 Bad Request | PASS | Boundary test |
| R90 | /api/register | phone | 999999999999999 | Sustav mora odbiti predug broj | HTTP 400 Bad Request | PASS | Boundary test |
| R91 | /api/register | oib | 1234567890abc | Sustav mora odbiti alfanumerički OIB | HTTP 400 Bad Request | PASS | Tip podataka |
| R92 | /api/register | phone | 1234567890abc | Sustav mora odbiti alfanumerički broj | HTTP 400 Bad Request | PASS | Tip podataka |
| R93 | /api/register | oib | -1 | Sustav mora odbiti negativan OIB | HTTP 400 Bad Request | PASS | Logička validacija |
| R94 | /api/register | oib | 2147483647 | Sustav mora odbiti graničnu vrijednost | HTTP 400 Bad Request | PASS | Integer overflow test |
| R95 | /api/register | oib | 2147483648 | Sustav mora odbiti overflow vrijednost | HTTP 400 Bad Request | PASS | Integer overflow test |



























