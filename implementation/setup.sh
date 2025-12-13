#!/bin/bash
# Skripta: setup.sh
# Mjesto: implementation/

# ==========================================================
# KONSTANTE
# ==========================================================
VENV_DIR="venv"
PYTHON_DEPS="boofuzz scapy"

# Targeti za kompilaciju
declare -A C_TARGETS
C_TARGETS["targets/target_CGF/parser_config.c"]="targets/target_CGF/parser_config"
C_TARGETS["targets/target_Mutation/cli_string_processor.c"]="targets/target_Mutation/cli_string_processor"
C_TARGETS["targets/target_Grammar/simple_protocol_server.c"]="targets/target_Grammar/simple_protocol_server"

# Provjera da li se skripta izvršava iz root direktorija projekta
if [ ! -d "implementation" ]; then
    echo "ERROR: Pokrenite ovu skriptu iz root direktorija projekta (gdje se nalazi implementation/)."
    exit 1
fi

echo "--- 🛠️ PODEŠAVANJE FUZZING PROJEKTA ---"

# ==========================================================
# 1. POSTAVLJANJE PYTHON VIRTUALNOG OKRUŽENJA
# ==========================================================
echo -e "\n[1/3] Postavljanje Python venv-a i instalacija ovisnosti..."

if [ -d "$VENV_DIR" ]; then
    echo "  > Direktorij '$VENV_DIR' već postoji. Preskačem kreiranje."
else
    python3 -m venv $VENV_DIR
    echo "  > Virtualno okruženje kreirano."
fi

# Instalacija paketa unutar venv
source $VENV_DIR/bin/activate
pip install $PYTHON_DEPS
deactivate

echo "  > Python ovisnosti instalirane: $PYTHON_DEPS"

# ==========================================================
# 2. KOMPILACIJA C TARGET APLIKACIJA
# ==========================================================
echo -e "\n[2/3] Kompilacija C target aplikacija..."

# **ISPRAVNA LOGIKA ZA AFL++**
if command -v afl-gcc-fast &> /dev/null; then
    AFL_CC="afl-gcc-fast"
    echo "  > Korištenje naprednog AFL++ kompajlera ($AFL_CC) za CGF target."
elif command -v afl-clang-fast &> /dev/null; then
    AFL_CC="afl-clang-fast"
    echo "  > Korištenje naprednog AFL++ kompajlera ($AFL_CC) za CGF target."
else
    AFL_CC="gcc"
    echo "  > UPOZORENJE: Nije pronađen ispravan AFL++ kompajler (fast varijanta). Koristim 'gcc'. CGF neće imati pokrivenost!"
fi


for SRC_PATH in "${!C_TARGETS[@]}"; do
    TARGET_PATH=${C_TARGETS[$SRC_PATH]}
    
    # Odlučivanje o kompajleru
    COMPILER="gcc"
    if [[ "$SRC_PATH" == *"target_CGF"* ]]; then
        COMPILER="$AFL_CC"
    fi

    # Kompilacija
    echo "  > Kompajliranje $TARGET_PATH..."
    $COMPILER -o "implementation/$TARGET_PATH" "implementation/$SRC_PATH"

    if [ $? -eq 0 ]; then
        echo "    ✅ Uspješno kompajlirano."
    else
        echo "    ❌ GREŠKA pri kompajliranju $SRC_PATH"
    fi
done

# ==========================================================
# 3. KREIRANJE INPUT/OUTPUT STRUKTURE
# ==========================================================
echo -e "\n[3/3] Kreiranje I/O strukture za AFL++..."

CGF_IN_DIR="implementation/targets/target_CGF/in"
CGF_OUT_DIR="implementation/targets/target_CGF/out"

mkdir -p $CGF_IN_DIR
mkdir -p $CGF_OUT_DIR

# Kreiranje seed inputa
if [ ! -f "$CGF_IN_DIR/seed.txt" ]; then
    echo "test" > "$CGF_IN_DIR/seed.txt"
    echo "  > Kreiran seed input: $CGF_IN_DIR/seed.txt"
fi

echo -e "\n--- 🎉 PODEŠAVANJE GOTOVO! ---"
echo "Zapamtite: AFL++ i Radamsa moraju se instalirati ručno (pogledajte setup.md sekciju 3)."