# ==========================================================
# KONFIGURACIJA
# ==========================================================

# Apsolutna putanja do Node.js server repozitorija
SERVER_DIR="/home/marin/repozitoriji/cro-vote-webapp"

# ==========================================================
# POKRETANJE SERVERA
# ==========================================================

echo "--- 🚀 POKRETANJE NODE.JS SERVERA ---"
echo "Pokušavam se prebaciti u direktorij: $SERVER_DIR"

# Prelazak u direktorij
cd "$SERVER_DIR"

# Provjera je li prelazak bio uspješan
if [ $? -eq 0 ]; then
    echo "Uspješno sam se prebacio u $SERVER_DIR."
    echo "Pokrećem 'npm run start'..."
    
    # Izvršavanje komande
    npm run start

    # Napomena: Nakon što se server pokrene, skripta će se ovdje 'zamrznuti'
    # dok server ne bude zaustavljen (Ctrl+C).
else
    echo "❌ GREŠKA: Direktorij '$SERVER_DIR' ne postoji ili nemate dozvolu za pristup."
    echo "Provjerite putanju i pokušajte ponovo."
    exit 1
fi