# Uvod
Fuzzing, koji je još nazivan i "fuzz testing" je zapravo "automatizirana tehnika za testiranje softvera koja detektira sigurnosne ranjivosti tako što šalje nasumične ili neočekivane ulaze aplikacijama kako bi se identificirali padovi i pogreške". [1]

Za testiranje softvera koristeći navedenu tehniku,  koristi se tzv. fuzzer. Fuzzer pomaže u pronalasku mogućih uzorka pada sustava na način da pokaže na ranjivi dio koda. Fuzzeri su naročito korisni pri otkrivanju propusta koje napadači mogu iskoristiti u napadima poput ubacivanja zlonamjernih upita u bazu podataka (engl. SQL injection) ili unošenja štetnog koda u web stranice (engl. cross-site scripting), čime je moguće ukrasti podatke ili onesposobiti sustav.

# Vrste fuzzinga

Prema [1], postoje dvije glavne vrste fuzzinga, a to su:
* Fuzzing vođen pokrićem
* Bihevioralni fuzzing

**Fuzzing vođen pokrićem** (engl. coverage-guided fuzzing) usmjeren je na izvorni kod programa koji se izvodi. Program se isprobava nasumičnim ulaznim podacima kako bi se otkrile moguće greške. Cilj je izazvati prekid rada programa te se u tu svrhu stalno stvaraju novi testovi. Prekid programa upućuje na mogući problem. Sve podatke koji su prikupljeni tijekom rada programa koriste testeri kako bi ponovili situaciju u kojoj je sustav pao i kako bi se preciznije utvrdili rizični dijelovi koda.

**Bihevioralni fuzzing** koristi specifikacije sustava kako bi usporedili kako aplikacija radi kada se unose nasumični ulazi u odnosu kako aplikacija zapravo treba raditi. Rezultat razlike se može gledati kao mjesto na kojem je moguće pronaći potencijalni sigurnosni rizik.

Prema [2], fuzzing je moguće podijeliti na više različitih vrsta, a njih je moguće vidjeti na sljedećoj slici:

<img width="947" height="775" alt="image" src="https://github.com/user-attachments/assets/65cdb626-c61a-44ad-803a-1e8ec73e412e" />


