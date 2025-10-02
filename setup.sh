#!/bin/bash
#
# Setup script for CTF Tools
# Установка всех зависимостей и подготовка окружения
#

echo "╔═══════════════════════════════════════════════════════╗"
echo "║        CTF TOOLS - Setup & Installation              ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

# Проверка Python
echo "[*] Проверка Python..."
if ! command -v python3 &> /dev/null; then
    echo "[-] Python 3 не найден! Установите Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "[+] Python $PYTHON_VERSION найден"

# Проверка pip
echo "[*] Проверка pip..."
if ! command -v pip3 &> /dev/null; then
    echo "[-] pip3 не найден! Установка pip..."
    python3 -m ensurepip --upgrade
fi
echo "[+] pip найден"

# Создание виртуального окружения (опционально)
read -p "[?] Создать виртуальное окружение? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "[*] Создание виртуального окружения..."
    python3 -m venv ctf_env
    source ctf_env/bin/activate
    echo "[+] Виртуальное окружение создано и активировано"
fi

# Установка зависимостей
echo "[*] Установка зависимостей..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "[+] Зависимости установлены успешно"
else
    echo "[-] Ошибка установки зависимостей"
    exit 1
fi

# Создание директорий для результатов
echo "[*] Создание директорий..."
mkdir -p ctf_results
mkdir -p ctf_logs
mkdir -p test_data
echo "[+] Директории созданы"

# Установка прав на выполнение
echo "[*] Установка прав на выполнение..."
chmod +x *.py
chmod +x *.sh
echo "[+] Права установлены"

# Проверка системных инструментов
echo ""
echo "[*] Проверка системных инструментов..."

check_tool() {
    if command -v $1 &> /dev/null; then
        echo "[+] $1 найден"
    else
        echo "[!] $1 не найден (опционально)"
    fi
}

check_tool nmap
check_tool netcat
check_tool tcpdump
check_tool wireshark

# Завершение
echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║            Setup Complete! / Установка завершена!     ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""
echo "[+] Для запуска используйте:"
echo "    python3 ctf_launcher.py"
echo ""
echo "[+] Или отдельные инструменты:"
echo "    python3 network_tools.py --help"
echo "    python3 web_exploit.py --help"
echo "    python3 crypto_tools.py --help"
echo ""

# Создание алиаса (опционально)
read -p "[?] Создать алиас 'ctf' для быстрого запуска? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ALIAS_CMD="alias ctf='cd $(pwd) && python3 ctf_launcher.py'"
    echo "$ALIAS_CMD" >> ~/.bashrc
    echo "[+] Алиас добавлен в ~/.bashrc"
    echo "[*] Используйте: source ~/.bashrc или перезапустите терминал"
    echo "[*] Затем просто введите: ctf"
fi

echo ""
echo "[+] Готово! Удачи на CTF соревнованиях!"







