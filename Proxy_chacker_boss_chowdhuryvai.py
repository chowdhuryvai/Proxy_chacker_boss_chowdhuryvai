import socket
import threading
import time
import os
import sys
import struct
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

class AdvancedProxyChecker:
    def __init__(self):
        self.working_http = []
        self.working_socks4 = []
        self.working_socks5 = []
        self.total_proxies = 0
        self.current_proxy = 0
        self.timeout = 10
        self.test_url = "http://www.google.com"
        self.test_host = "www.google.com"
        self.test_port = 80
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        banner = r"""
  ██████  ██░ ██  ▄▄▄       ██▓███   ██▀███   ▒█████    ██████ 
▒██    ▒ ▓██░ ██▒▒████▄    ▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒▒██    ▒ 
░ ▓██▄   ▒██▀▀██░▒██  ▀█▄  ▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒░ ▓██▄   
  ▒   ██▒░▓█ ░██ ░██▄▄▄▄██ ▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░  ▒   ██▒
▒██████▒▒░▓█▒░██▓ ▓█   ▓██▒▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░▒██████▒▒
▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒ ▒▒   ▓▒█░▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░
░ ░▒  ░ ░ ▒ ░▒░ ░  ▒   ▒▒ ░░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░ ░ ░▒  ░ ░
░  ░  ░   ░  ░░ ░  ░   ▒   ░░         ░░   ░ ░ ░ ░ ▒  ░  ░  ░  
      ░   ░  ░  ░      ░  ░            ░         ░ ░        ░  
                                                               
        ╔═══════════════════════════════════════════╗
        ║       ADVANCED PROXY CHECKER TOOL         ║
        ║              by chowdhuryvai              ║
        ║    HTTP • SOCKS4 • SOCKS5 Supported       ║
        ╚═══════════════════════════════════════════╝
        """
        print("\033[1;32m" + banner + "\033[0m")
        print("\033[1;36m" + "=" * 65 + "\033[0m")
        print("\033[1;33mTelegram ID:\033[0m \033[1;37mhttps://t.me/darkvaiadmin\033[0m")
        print("\033[1;33mTelegram Channel:\033[0m \033[1;37mhttps://t.me/windowspremiumkey\033[0m")
        print("\033[1;33mWebsite:\033[0m \033[1;37mhttps://crackyworld.com/\033[0m")
        print("\033[1;36m" + "=" * 65 + "\033[0m")
        print()
    
    def print_colored(self, text, color_code):
        print(f"\033[{color_code}m{text}\033[0m")
    
    def validate_ip_port(self, proxy):
        """Validate IP:PORT format"""
        try:
            ip, port = proxy.split(':')
            # Validate IP
            socket.inet_aton(ip)
            # Validate port
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                return False
            return True
        except:
            return False
    
    def check_http_proxy(self, proxy):
        """Check HTTP proxy"""
        try:
            proxy_handler = urllib.request.ProxyHandler({
                'http': f'http://{proxy}', 
                'https': f'https://{proxy}'
            })
            opener = urllib.request.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            response = urllib.request.urlopen(self.test_url, timeout=self.timeout)
            if response.getcode() == 200:
                return True
            return False
        except:
            return False
    
    def check_socks4_proxy(self, proxy):
        """Check SOCKS4 proxy"""
        try:
            ip, port = proxy.split(':')
            port = int(port)
            
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((ip, port))
            
            # SOCKS4 connection request
            request = struct.pack('>BBH', 0x04, 0x01, port)  # Version 4, Connect command, port
            request += socket.inet_aton(socket.gethostbyname(self.test_host))  # IP address
            request += struct.pack('B', 0x00)  # User ID (empty)
            
            sock.send(request)
            response = sock.recv(8)
            
            sock.close()
            
            # Check response (should be 0x5A for success)
            if len(response) >= 2 and response[1] == 0x5A:
                return True
            return False
        except:
            return False
    
    def check_socks5_proxy(self, proxy):
        """Check SOCKS5 proxy"""
        try:
            ip, port = proxy.split(':')
            port = int(port)
            
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((ip, port))
            
            # SOCKS5 greeting - no authentication
            greeting = struct.pack('BBB', 0x05, 0x01, 0x00)  # Version 5, 1 method, no auth
            sock.send(greeting)
            response = sock.recv(2)
            
            if response[1] != 0x00:  # No acceptable authentication method
                sock.close()
                return False
            
            # SOCKS5 connection request
            request = struct.pack('>BBBB', 0x05, 0x01, 0x00, 0x03)  # Version 5, connect, reserved, domain
            request += struct.pack('B', len(self.test_host))  # Domain length
            request += self.test_host.encode()  # Domain name
            request += struct.pack('>H', self.test_port)  # Port
            
            sock.send(request)
            response = sock.recv(10)
            
            sock.close()
            
            # Check response (should be 0x00 for success)
            if len(response) >= 2 and response[1] == 0x00:
                return True
            return False
        except:
            return False
    
    def check_proxy_all_protocols(self, proxy):
        """Check proxy for all protocols (HTTP, SOCKS4, SOCKS5)"""
        self.current_proxy += 1
        progress = (self.current_proxy / self.total_proxies) * 100
        
        # Remove any whitespace and validate format
        proxy = proxy.strip()
        
        if not proxy or not self.validate_ip_port(proxy):
            self.print_colored(f"[{self.current_proxy}/{self.total_proxies}] {proxy} - INVALID FORMAT", "1;31")
            return None
        
        working_protocols = []
        
        # Check HTTP
        http_working = self.check_http_proxy(proxy)
        if http_working:
            working_protocols.append("HTTP")
            self.print_colored(f"[{self.current_proxy}/{self.total_proxies}] {proxy} - HTTP ✓", "1;32")
        
        # Check SOCKS4
        socks4_working = self.check_socks4_proxy(proxy)
        if socks4_working:
            working_protocols.append("SOCKS4")
            self.print_colored(f"[{self.current_proxy}/{self.total_proxies}] {proxy} - SOCKS4 ✓", "1;33")
        
        # Check SOCKS5
        socks5_working = self.check_socks5_proxy(proxy)
        if socks5_working:
            working_protocols.append("SOCKS5")
            self.print_colored(f"[{self.current_proxy}/{self.total_proxies}] {proxy} - SOCKS5 ✓", "1;36")
        
        if not working_protocols:
            self.print_colored(f"[{self.current_proxy}/{self.total_proxies}] {proxy} - DEAD", "1;31")
            return None
        
        return (proxy, working_protocols)
    
    def load_proxies_from_file(self, filename):
        """Load proxies from text file"""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                proxies = f.readlines()
            return [proxy.strip() for proxy in proxies if proxy.strip()]
        except FileNotFoundError:
            self.print_colored(f"File {filename} not found!", "1;31")
            return []
        except Exception as e:
            self.print_colored(f"Error reading file: {e}", "1;31")
            return []
    
    def save_working_proxies(self, filename_prefix="working_proxies"):
        """Save working proxies to separate files for each protocol"""
        try:
            # Save HTTP proxies
            if self.working_http:
                http_file = f"{filename_prefix}_http.txt"
                with open(http_file, 'w') as f:
                    for proxy in self.working_http:
                        f.write(f"{proxy}\n")
                self.print_colored(f"HTTP proxies saved to: {http_file}", "1;32")
            
            # Save SOCKS4 proxies
            if self.working_socks4:
                socks4_file = f"{filename_prefix}_socks4.txt"
                with open(socks4_file, 'w') as f:
                    for proxy in self.working_socks4:
                        f.write(f"{proxy}\n")
                self.print_colored(f"SOCKS4 proxies saved to: {socks4_file}", "1;33")
            
            # Save SOCKS5 proxies
            if self.working_socks5:
                socks5_file = f"{filename_prefix}_socks5.txt"
                with open(socks5_file, 'w') as f:
                    for proxy in self.working_socks5:
                        f.write(f"{proxy}\n")
                self.print_colored(f"SOCKS5 proxies saved to: {socks5_file}", "1;36")
            
            # Save all working proxies
            if self.working_http or self.working_socks4 or self.working_socks5:
                all_file = f"{filename_prefix}_all.txt"
                with open(all_file, 'w') as f:
                    f.write("=== HTTP PROXIES ===\n")
                    for proxy in self.working_http:
                        f.write(f"{proxy}\n")
                    f.write("\n=== SOCKS4 PROXIES ===\n")
                    for proxy in self.working_socks4:
                        f.write(f"{proxy}\n")
                    f.write("\n=== SOCKS5 PROXIES ===\n")
                    for proxy in self.working_socks5:
                        f.write(f"{proxy}\n")
                self.print_colored(f"All proxies saved to: {all_file}", "1;35")
                
        except Exception as e:
            self.print_colored(f"Error saving files: {e}", "1;31")
    
    def print_detailed_stats(self):
        """Print detailed statistics"""
        self.print_colored("\n" + "=" * 65, "1;36")
        self.print_colored("PROXY CHECKING COMPLETED - DETAILED RESULTS", "1;35")
        self.print_colored("=" * 65, "1;36")
        
        self.print_colored(f"TOTAL PROXIES CHECKED: {self.total_proxies}", "1;33")
        self.print_colored(f"WORKING HTTP PROXIES:  {len(self.working_http)}", "1;32")
        self.print_colored(f"WORKING SOCKS4 PROXIES: {len(self.working_socks4)}", "1;33")
        self.print_colored(f"WORKING SOCKS5 PROXIES: {len(self.working_socks5)}", "1;36")
        
        total_working = len(self.working_http) + len(self.working_socks4) + len(self.working_socks5)
        success_rate = (total_working / self.total_proxies) * 100 if self.total_proxies > 0 else 0
        
        self.print_colored(f"TOTAL WORKING PROXIES:  {total_working}", "1;32")
        self.print_colored(f"OVERALL SUCCESS RATE:   {success_rate:.2f}%", "1;35")
        self.print_colored("=" * 65, "1;36")
    
    def show_working_proxies(self):
        """Display all working proxies by protocol"""
        if self.working_http:
            self.print_colored("\n=== WORKING HTTP PROXIES ===", "1;32")
            for i, proxy in enumerate(self.working_http, 1):
                self.print_colored(f"{i}. {proxy}", "1;37")
        
        if self.working_socks4:
            self.print_colored("\n=== WORKING SOCKS4 PROXIES ===", "1;33")
            for i, proxy in enumerate(self.working_socks4, 1):
                self.print_colored(f"{i}. {proxy}", "1;37")
        
        if self.working_socks5:
            self.print_colored("\n=== WORKING SOCKS5 PROXIES ===", "1;36")
            for i, proxy in enumerate(self.working_socks5, 1):
                self.print_colored(f"{i}. {proxy}", "1;37")
    
    def run_checker(self):
        """Main checker function"""
        self.clear_screen()
        self.print_banner()
        
        # Reset counters
        self.working_http = []
        self.working_socks4 = []
        self.working_socks5 = []
        self.current_proxy = 0
        
        # Get proxy file
        proxy_file = input("\033[1;37mEnter proxy file path: \033[0m")
        
        if not os.path.exists(proxy_file):
            self.print_colored("File not found! Please check the path.", "1;31")
            time.sleep(2)
            return
        
        # Load proxies
        proxies = self.load_proxies_from_file(proxy_file)
        self.total_proxies = len(proxies)
        
        if self.total_proxies == 0:
            self.print_colored("No valid proxies found in the file!", "1;31")
            time.sleep(2)
            return
        
        self.print_colored(f"Loaded {self.total_proxies} proxies from file", "1;33")
        
        # Get threads count
        try:
            threads = int(input("\033[1;37mEnter number of threads (default 50): \033[0m") or "50")
            threads = max(1, min(threads, 500))  # Limit between 1-500
        except:
            threads = 50
        
        # Get timeout
        try:
            timeout = int(input("\033[1;37mEnter timeout in seconds (default 10): \033[0m") or "10")
            self.timeout = max(1, min(timeout, 60))  # Limit between 1-60
        except:
            self.timeout = 10
        
        # Start checking
        self.print_colored(f"\nStarting proxy check with {threads} threads, timeout {self.timeout}s...", "1;33")
        self.print_colored("=" * 65, "1;36")
        self.print_colored("LEGEND: HTTP ✓ | SOCKS4 ✓ | SOCKS5 ✓ | DEAD", "1;37")
        self.print_colored("=" * 65, "1;36")
        
        start_time = time.time()
        
        # Process proxies with threading
        with ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_proxy = {executor.submit(self.check_proxy_all_protocols, proxy): proxy for proxy in proxies}
            
            for future in as_completed(future_to_proxy):
                result = future.result()
                if result:
                    proxy, protocols = result
                    if "HTTP" in protocols:
                        self.working_http.append(proxy)
                    if "SOCKS4" in protocols:
                        self.working_socks4.append(proxy)
                    if "SOCKS5" in protocols:
                        self.working_socks5.append(proxy)
        
        end_time = time.time()
        
        # Print results
        self.print_detailed_stats()
        self.print_colored(f"Time taken: {end_time - start_time:.2f} seconds", "1;33")
        
        # Show working proxies
        self.show_working_proxies()
        
        # Save results
        if self.working_http or self.working_socks4 or self.working_socks5:
            save_option = input("\n\033[1;37mSave working proxies to files? (y/n): \033[0m").lower()
            if save_option == 'y':
                output_prefix = input("\033[1;37mEnter output filename prefix (default: working_proxies): \033[0m") or "working_proxies"
                self.save_working_proxies(output_prefix)

def main():
    checker = AdvancedProxyChecker()
    
    while True:
        checker.run_checker()
        
        again = input("\n\033[1;37mCheck another file? (y/n): \033[0m").lower()
        if again != 'y':
            checker.print_colored("\nThank you for using chowdhuryvai Advanced Proxy Checker!", "1;32")
            checker.print_colored("Visit: https://crackyworld.com/ for more tools!", "1;33")
            checker.print_colored("Telegram: https://t.me/darkvaiadmin", "1;36")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;31mProgram interrupted by user. Exiting...\033[0m")
    except Exception as e:
        print(f"\n\033[1;31mAn unexpected error occurred: {e}\033[0m")
