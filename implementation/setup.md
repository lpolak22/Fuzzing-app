# ⚙️ Vodič za Postavljanje Projekta (SETUP.MD)

Ovaj dokument objašnjava kako brzo postaviti okruženje za fuzzing.
Preporučujemo korištenje priložene skripte `setup.sh` koja automatizira većinu koraka.

## 1. Preduvjeti

Osigurajte da imate instalirane Git, Python 3.10+, GCC (ili Clang) i 'make'.

## 2. Automatizirano Postavljanje

Pokrenite priloženu `setup.sh` skriptu koja će instalirati Python ovisnosti, kompajlirati C targete i kreirati virtualno okruženje (`venv`).

**Napomena:** Skripta NEĆE instalirati AFL++ i Radamsu jer to zahtijeva `sudo` privilegije. To morate učiniti ručno (pogledajte sekciju 3).

```bash
# Pokretanje skripte (iz root direktorija projekta)
# chmod +x implementation/setup.sh (ako skripta nije izvršna)
./implementation/setup.sh


Koraci prije pokretanja skripte su:

sudo apt update
sudo apt install build-essential clang llvm-dev libstdc++-14-dev python3-dev

# Postavljanje core_pattern: AFL zahtijeva da se core dumpovi šalju njemu
echo core | sudo tee /proc/sys/kernel/core_pattern
# Onemogućavanje limita za core dump
ulimit -c unlimited
# Ubrzavanje performansi I/O operacija
sudo sh -c 'echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor'

# Prelazak u direktorij za alate
cd implementation/tools/afl++

# Kompilacija i instalacija
# Kloniranje i kompilacija
git clone https://github.com/AFLplusplus/AFLplusplus
cd AFLplusplus
sudo make all
sudo make install
which afl-gcc-fast


# Instalacija preko package managera (Debian/Ubuntu)

cd radamsa
sudo apt install build-essential git
git clone https://gitlab.com/akihe/radamsa.git
cd radamsa
sudo apt install ocaml ocaml-findlib opam
make
sudo make install
which radamsa
radamsa --version



# Fuzzing parser_config

cd ~/Documents/SIS/projekt/Fuzzing-app  #treba se pozicionirati u root folder 
cd implementation/targets/target_CGF
afl-clang-fast parser_config.c -o parser_config
cd ~/Documents/SIS/projekt/Fuzzing-app 
afl-fuzz -i implementation/targets/target_CGF/in -o implementation/targets/target_CGF/out implementation/targets/target_CGF/parser_config



#Prije pokretanja, ne zaboravite dati skripti dozvolu za izvršavanje: 
chmod +x implementation/setup.sh
sudo apt install python3-venv  #ako nema instalirano vec prije
#Pokrenite setup.sh
./implementation/setup.sh 

# Aktivacija venv-a

source venv/bin/activate

# Pokretanje Scapy fuzzer-a
python3 implementation/targets/target_Generation/fuzz_target4_scapy.py


echo "test" | radamsa | implementation/targets/target_Mutation/cli_string_processor
