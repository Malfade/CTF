#!/bin/bash
#
# Setup script for CTF Tools on Kali Linux
# Установка и настройка CTF инструментов для Kali Linux
#

echo "╔═══════════════════════════════════════════════════════╗"
echo "║        🐉 KALI LINUX CTF TOOLS SETUP 🐉              ║"
echo "║                    Version 2.0                        ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Проверка что мы в Kali Linux
if ! grep -q "Kali" /etc/os-release 2>/dev/null; then
    echo "⚠️  ВНИМАНИЕ: Этот скрипт предназначен для Kali Linux!"
    echo "   Продолжить установку? (y/n)"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Установка отменена."
        exit 1
    fi
fi

echo "🐉 Обнаружена Kali Linux - отлично!"
echo ""

# Проверка Python
echo "[*] Проверка Python..."
if ! command -v python3 &> /dev/null; then
    echo "[-] Python 3 не найден! Установка..."
    sudo apt update && sudo apt install -y python3 python3-pip
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "[+] Python $PYTHON_VERSION найден"

# Обновление системы
echo ""
echo "[*] Обновление системы Kali Linux..."
sudo apt update

# Установка дополнительных пакетов Kali
echo ""
echo "[*] Установка дополнительных пакетов..."
sudo apt install -y \
    python3-requests \
    python3-bs4 \
    python3-colorama \
    python3-scapy \
    python3-nmap \
    python3-paramiko \
    python3-cryptography \
    python3-pil \
    python3-psutil \
    python3-dnspython \
    python3-whois \
    python3-shodan \
    python3-magic \
    python3-venv \
    python3-full

# Установка популярных Kali инструментов если их нет
echo ""
echo "[*] Проверка популярных Kali инструментов..."

kali_tools=(
    "nmap" "masscan" "nikto" "sqlmap" "john" "hashcat" 
    "hydra" "dirb" "gobuster" "wfuzz" "burpsuite" "metasploit-framework"
    "aircrack-ng" "reaver" "wifite" "wireshark" "tshark"
    "volatility" "binwalk" "foremost" "steghide" "exiftool"
    "theharvester" "dnsrecon" "fierce" "recon-ng"
)

for tool in "${kali_tools[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        echo "[!] $tool не найден - установка..."
        sudo apt install -y "$tool" 2>/dev/null || echo "    Не удалось установить $tool"
    else
        echo "[+] $tool найден"
    fi
done

# Создание виртуального окружения (опционально)
echo ""
read -p "[?] Создать виртуальное окружение? (рекомендуется) (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "[*] Создание виртуального окружения..."
    python3 -m venv ctf_env
    source ctf_env/bin/activate
    echo "[+] Виртуальное окружение создано и активировано"
    echo "[!] Для активации в будущем используйте: source ctf_env/bin/activate"
fi

# Установка Python зависимостей
echo ""
echo "[*] Установка Python зависимостей..."
if [[ -f "requirements_kali.txt" ]]; then
    pip3 install -r requirements_kali.txt
else
    pip3 install -r requirements.txt
fi

# Создание директорий
echo ""
echo "[*] Создание рабочих директорий..."
mkdir -p ctf_results
mkdir -p ctf_logs
mkdir -p wordlists
mkdir -p payloads
mkdir -p screenshots
echo "[+] Директории созданы"

# Установка прав на выполнение
echo ""
echo "[*] Установка прав на выполнение..."
chmod +x *.py
chmod +x *.sh
echo "[+] Права установлены"

# Создание алиасов
echo ""
read -p "[?] Создать алиасы для быстрого доступа? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "[*] Создание алиасов..."
    
    # Добавляем алиасы в .bashrc
    cat >> ~/.bashrc << 'EOF'

# CTF Tools Aliases
alias ctf='cd /home/malfade/Worl/cybersecurity/CTF && python3 kali_launcher.py'
alias ctf-tools='cd /home/malfade/Worl/cybersecurity/CTF'
alias ctf-kali='cd /home/malfade/Worl/cybersecurity/CTF && python3 kali_integration.py --list-tools'
alias ctf-network='cd /home/malfade/Worl/cybersecurity/CTF && python3 network_tools.py'
alias ctf-web='cd /home/malfade/Worl/cybersecurity/CTF && python3 web_exploit.py'
alias ctf-crypto='cd /home/malfade/Worl/cybersecurity/CTF && python3 crypto_tools.py'
alias ctf-osint='cd /home/malfade/Worl/cybersecurity/CTF && python3 osint_tools.py'
alias ctf-tor='cd /home/malfade/Worl/cybersecurity/CTF && python3 tor_integration.py'

EOF
    
    echo "[+] Алиасы добавлены в ~/.bashrc"
    echo "[!] Перезапустите терминал или выполните: source ~/.bashrc"
fi

# Создание конфигурационных файлов
echo ""
echo "[*] Создание конфигурационных файлов..."

# Создаем .ctf_config
cat > .ctf_config << 'EOF'
# CTF Tools Configuration
DEFAULT_TIMEOUT=30
DEFAULT_THREADS=50
SAVE_RESULTS=true
LOG_LEVEL=INFO
TOR_PROXY=127.0.0.1:9050
SHODAN_API_KEY=
CENSYS_API_ID=
CENSYS_API_SECRET=
EOF

echo "[+] Конфигурационный файл создан"

# Проверка установки
echo ""
echo "[*] Проверка установки..."
echo ""

# Тестируем основные инструменты
echo "Тестирование инструментов:"
python3 -c "import requests; print('✓ requests')" 2>/dev/null || echo "✗ requests"
python3 -c "import colorama; print('✓ colorama')" 2>/dev/null || echo "✗ colorama"
python3 -c "import nmap; print('✓ python-nmap')" 2>/dev/null || echo "✗ python-nmap"

# Проверяем Kali инструменты
echo ""
echo "Проверка Kali инструментов:"
command -v nmap >/dev/null && echo "✓ nmap" || echo "✗ nmap"
command -v nikto >/dev/null && echo "✓ nikto" || echo "✗ nikto"
command -v sqlmap >/dev/null && echo "✓ sqlmap" || echo "✗ sqlmap"
command -v john >/dev/null && echo "✓ john" || echo "✗ john"
command -v hashcat >/dev/null && echo "✓ hashcat" || echo "✗ hashcat"

# Завершение
echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║            🐉 SETUP COMPLETE! 🐉                      ║"
echo "║         CTF Tools готовы к использованию!             ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "🚀 Для запуска используйте:"
echo "    python3 kali_launcher.py"
echo "    или просто: ctf (если создали алиас)"
echo ""
echo "📚 Полезные команды:"
echo "    ctf-kali          - Список Kali инструментов"
echo "    ctf-network       - Сетевые инструменты"
echo "    ctf-web           - Веб-эксплуатация"
echo "    ctf-crypto        - Криптография"
echo "    ctf-osint         - OSINT разведка"
echo "    ctf-tor           - Tor интеграция"
echo ""
echo "🎯 Быстрые команды:"
echo "    python3 kali_integration.py --list-tools"
echo "    python3 kali_integration.py --nmap 192.168.1.1 --scan-type aggressive"
echo "    python3 kali_integration.py --nikto http://target.com"
echo ""
echo "📁 Рабочие директории:"
echo "    ctf_results/      - Результаты сканирования"
echo "    ctf_logs/         - Логи"
echo "    wordlists/        - Словари"
echo "    payloads/         - Пейлоады"
echo ""
echo "🐉 Удачи на CTF с Kali Linux!"
echo ""

