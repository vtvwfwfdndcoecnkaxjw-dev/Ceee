#!/usr/bin/env python3
"""
🐱 CAT BOT - Sistema de Segurança Completo para Discord
Versão: 3.0 Premium | Nível: Wick/SecurityBot
Autor: Sistema Automatizado
Descrição: Bot de segurança completo com todas as funcionalidades premium
"""

import discord
from discord.ext import commands, tasks
from discord.ui import Button, View, Modal, TextInput, Select
import os
import json
import asyncio
import aiofiles
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set
import traceback
import pickle
import hashlib
from collections import defaultdict, deque
import random
import string
from enum import Enum
import logging
from logging.handlers import RotatingFileHandler
import sys

# ==============================================
# CONFIGURAÇÃO INICIAL E VARIÁVEIS DE AMBIENTE
# ==============================================

# Carregar variáveis de ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv não instalado. Instale com: pip install python-dotenv")
    sys.exit(1)

# Variáveis obrigatórias
REQUIRED_ENV = ['TOKEN', 'OWNER_ID']
missing = [var for var in REQUIRED_ENV if not os.getenv(var)]
if missing:
    print(f"❌ Variáveis de ambiente faltando: {', '.join(missing)}")
    print("Crie um arquivo .env com:")
    print("TOKEN=seu_token_aqui")
    print("OWNER_ID=seu_id_aqui")
    print("VOICE_CHANNEL_ID=opcional_id_canal_voz")
    sys.exit(1)

TOKEN = os.getenv('TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))
VOICE_CHANNEL_ID = os.getenv('VOICE_CHANNEL_ID')
if VOICE_CHANNEL_ID:
    VOICE_CHANNEL_ID = int(VOICE_CHANNEL_ID)

# ==============================================
# CONFIGURAÇÃO DO LOGGING PROFISSIONAL
# ==============================================

class ProfessionalLogger:
    """Sistema de logging profissional com múltiplos arquivos"""
    
    def __init__(self):
        self.setup_logging()
        self.message_cache = deque(maxlen=5000)  # Cache de últimas mensagens
        self.deleted_messages = deque(maxlen=1000)  # Mensagens deletadas
        self.edit_history = defaultdict(list)  # Histórico de edições
        
    def setup_logging(self):
        """Configura sistema de logging multi-arquivo"""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # Configurar formato
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Arquivos de log específicos
        log_files = {
            'nuke': 'logs/nuke_protection.log',
            'raid': 'logs/raid_protection.log',
            'whitelist': 'logs/whitelist.log',
            'backup': 'logs/backup.log',
            'actions': 'logs/actions.log',
            'security': 'logs/security_warnings.log',
            'permissions': 'logs/permission_changes.log',
            'messages': 'logs/message_logs.log',
            'system': 'logs/system.log'
        }
        
        self.loggers = {}
        for name, filepath in log_files.items():
            logger = logging.getLogger(name)
            logger.setLevel(logging.INFO)
            
            # Handler para arquivo
            file_handler = RotatingFileHandler(
                filepath, maxBytes=10*1024*1024, backupCount=5
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            # Handler para console (apenas para system)
            if name == 'system':
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)
            
            self.loggers[name] = logger
    
    def log_nuke(self, message: str, user: Optional[discord.User] = None):
        """Log de proteção anti-nuke"""
        if user:
            message = f"[{user.id}] {user.name}: {message}"
        self.loggers['nuke'].warning(message)
    
    def log_raid(self, message: str, user: Optional[discord.User] = None):
        """Log de proteção anti-raid"""
        if user:
            message = f"[{user.id}] {user.name}: {message}"
        self.loggers['raid'].warning(message)
    
    def log_whitelist(self, message: str, user: Optional[discord.User] = None):
        """Log de alterações na whitelist"""
        if user:
            message = f"[{user.id}] {user.name}: {message}"
        self.loggers['whitelist'].info(message)
    
    def log_backup(self, message: str):
        """Log de operações de backup"""
        self.loggers['backup'].info(message)
    
    def log_action(self, action: str, user: discord.User, target: Any = None, reason: str = ""):
        """Log de ações realizadas"""
        msg = f"Action: {action} | User: {user.name} ({user.id})"
        if target:
            if hasattr(target, 'id'):
                msg += f" | Target: {target.id}"
            else:
                msg += f" | Target: {target}"
        if reason:
            msg += f" | Reason: {reason}"
        self.loggers['actions'].info(msg)
    
    def log_security(self, level: str, message: str, user: Optional[discord.User] = None):
        """Log de avisos de segurança"""
        if user:
            message = f"[{level}] [{user.id}] {user.name}: {message}"
        else:
            message = f"[{level}] {message}"
        self.loggers['security'].warning(message)
    
    def log_permission(self, change_type: str, user: discord.User, target: Any, before: Any, after: Any):
        """Log de alterações de permissão"""
        msg = f"{change_type} | By: {user.name} ({user.id}) | Target: {target}"
        msg += f" | Before: {before} | After: {after}"
        self.loggers['permissions'].info(msg)
    
    def log_message(self, message: discord.Message, action: str = "sent"):
        """Log de mensagens"""
        msg = f"[{message.created_at}] #{message.channel.name} | {message.author.name} ({message.author.id}): {action}"
        msg += f" | Content: {message.content[:200]}"
        
        if message.attachments:
            msg += f" | Attachments: {len(message.attachments)}"
        
        self.loggers['messages'].info(msg)
        
        # Cache da mensagem
        self.message_cache.append({
            'id': message.id,
            'author': f"{message.author.name} ({message.author.id})",
            'channel': message.channel.name,
            'content': message.content,
            'timestamp': message.created_at.isoformat(),
            'attachments': len(message.attachments)
        })
    
    def log_deleted_message(self, message: discord.Message, deleter: Optional[discord.User] = None):
        """Log de mensagens deletadas"""
        self.deleted_messages.append({
            'id': message.id,
            'author': f"{message.author.name} ({message.author.id})",
            'deleter': f"{deleter.name} ({deleter.id})" if deleter else "Unknown",
            'channel': message.channel.name,
            'content': message.content,
            'timestamp': datetime.utcnow().isoformat(),
            'deleted_at': datetime.utcnow().isoformat()
        })
        
        msg = f"[DELETED] #{message.channel.name} | Original author: {message.author.name} ({message.author.id})"
        if deleter:
            msg += f" | Deleted by: {deleter.name} ({deleter.id})"
        msg += f" | Content: {message.content[:200]}"
        
        self.loggers['messages'].warning(msg)
    
    def log_system(self, message: str, level: str = "INFO"):
        """Log do sistema"""
        if level == "ERROR":
            self.loggers['system'].error(message)
        elif level == "WARNING":
            self.loggers['system'].warning(message)
        else:
            self.loggers['system'].info(message)

logger = ProfessionalLogger()

# ==============================================
# CONFIGURAÇÃO DO BOT
# ==============================================

# Definir intents
intents = discord.Intents.all()
intents.message_content = True
intents.presences = True
intents.members = True

# Criar bot
bot = commands.Bot(
    command_prefix='#',
    intents=intents,
    help_command=None,
    case_insensitive=True
)

# ==============================================
# SISTEMA DE WHITELIST MASTER
# ==============================================

class WhitelistMaster:
    """Sistema de Whitelist nível Wick/Security"""
    
    PERMISSIONS_PERIGOSAS = [
        'administrator',
        'manage_guild',
        'manage_roles',
        'manage_channels',
        'manage_messages',
        'manage_webhooks',
        'manage_emojis',
        'manage_events',
        'ban_members',
        'kick_members',
        'mention_everyone',
        'move_members',
        'mute_members',
        'deafen_members',
        'priority_speaker',
        'view_audit_log',
        'manage_nicknames',
        'create_instant_invite'
    ]
    
    def __init__(self):
        self.whitelist_file = 'whitelist_data.json'
        self.backup_whitelist_file = 'whitelist_backup.json'
        self.whitelist = self.carregar_whitelist()
        self.fingerprints = self.carregar_fingerprints()
        
    def carregar_whitelist(self) -> List[int]:
        """Carrega a whitelist do arquivo"""
        try:
            if os.path.exists(self.whitelist_file):
                with open(self.whitelist_file, 'r') as f:
                    data = json.load(f)
                    lista = data.get('whitelist', [OWNER_ID])
                    # Garantir que o owner sempre está
                    if OWNER_ID not in lista:
                        lista.append(OWNER_ID)
                    return lista
            else:
                # Inicializar com o dono
                lista = [OWNER_ID]
                self.salvar_whitelist(lista)
                return lista
        except Exception as e:
            logger.log_system(f"Erro ao carregar whitelist: {e}", "ERROR")
            return [OWNER_ID]
    
    def carregar_fingerprints(self) -> Dict[int, Dict[str, Any]]:
        """Carrega fingerprints dos usuários"""
        try:
            if os.path.exists('fingerprints.json'):
                with open('fingerprints.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def salvar_fingerprints(self):
        """Salva fingerprints"""
        try:
            with open('fingerprints.json', 'w') as f:
                json.dump(self.fingerprints, f, indent=4)
        except:
            pass
    
    def salvar_whitelist(self, lista: Optional[List[int]] = None):
        """Salva a whitelist no arquivo"""
        if lista is None:
            lista = self.whitelist
        
        # Fazer backup primeiro
        if os.path.exists(self.whitelist_file):
            try:
                with open(self.whitelist_file, 'r') as f:
                    backup_data = json.load(f)
                with open(self.backup_whitelist_file, 'w') as f:
                    json.dump(backup_data, f, indent=4)
            except:
                pass
        
        # Salvar nova whitelist
        data = {
            'whitelist': lista,
            'last_updated': datetime.utcnow().isoformat(),
            'total_users': len(lista)
        }
        
        try:
            with open(self.whitelist_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.log_system(f"Erro ao salvar whitelist: {e}", "ERROR")
    
    def is_whitelisted(self, user_id: int) -> bool:
        """Verifica se um usuário está na whitelist"""
        return user_id in self.whitelist
    
    def adicionar_whitelist(self, user_id: int) -> bool:
        """Adiciona um usuário à whitelist"""
        if user_id not in self.whitelist:
            self.whitelist.append(user_id)
            self.salvar_whitelist()
            logger.log_whitelist(f"Usuário {user_id} adicionado à whitelist")
            return True
        return False
    
    def remover_whitelist(self, user_id: int) -> bool:
        """Remove um usuário da whitelist (exceto owner)"""
        if user_id in self.whitelist and user_id != OWNER_ID:
            self.whitelist.remove(user_id)
            self.salvar_whitelist()
            logger.log_whitelist(f"Usuário {user_id} removido da whitelist")
            return True
        return False
    
    def tem_permissao_perigosa(self, permissions: discord.Permissions) -> bool:
        """Verifica se as permissões contêm permissões perigosas"""
        for perm in self.PERMISSIONS_PERIGOSAS:
            if getattr(permissions, perm):
                return True
        return False
    
    def criar_fingerprint(self, user: discord.User) -> str:
        """Cria um fingerprint único para o usuário"""
        data = f"{user.id}{user.name}{user.created_at}{user.discriminator}"
        fingerprint = hashlib.sha256(data.encode()).hexdigest()
        
        self.fingerprints[user.id] = {
            'fingerprint': fingerprint,
            'username': user.name,
            'created_at': user.created_at.isoformat(),
            'last_seen': datetime.utcnow().isoformat()
        }
        self.salvar_fingerprints()
        
        return fingerprint
    
    def verificar_fingerprint(self, user: discord.User) -> bool:
        """Verifica se o fingerprint do usuário mudou (possível conta hackeada)"""
        if user.id not in self.fingerprints:
            self.criar_fingerprint(user)
            return True
        
        old_data = self.fingerprints[user.id]
        new_fingerprint = self.criar_fingerprint(user)
        
        if old_data['fingerprint'] != new_fingerprint:
            logger.log_security("HIGH", f"Fingerprint mudou para usuário {user.name} ({user.id}) - Possível conta comprometida")
            return False
        
        return True

whitelist_master = WhitelistMaster()

# ==============================================
# SISTEMA ANTI-NUKE PROFISSIONAL
# ==============================================

class AntiNukeProfessional:
    """Sistema Anti-Nuke nível empresarial"""
    
    def __init__(self):
        self.cooldowns = {}
        self.suspicious_actions = defaultdict(list)
        self.auto_restore_queue = []
        self.lockdown_mode = False
        self.siege_mode = False
        
    async def monitorar_criacao_cargo(self, role: discord.Role):
        """Monitora criação de cargos"""
        guild = role.guild
        
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.role_create):
            if entry.target.id == role.id:
                user = entry.user
                
                # Verificar se quem criou está na whitelist
                if not whitelist_master.is_whitelisted(user.id) and user.id != bot.user.id:
                    
                    # Verificar se o cargo tem permissões perigosas
                    if whitelist_master.tem_permissao_perigosa(role.permissions):
                        # AÇÃO: Deletar cargo e punir criador
                        try:
                            await role.delete(reason=f"Anti-Nuke: Cargo perigoso criado por não autorizado - {user.name}")
                            
                            # Punição automática
                            if user != guild.owner and user != bot.user:
                                try:
                                    await user.kick(reason="Tentativa de escalar privilégios")
                                    logger.log_action("KICK", user, role, "Criação de cargo perigoso")
                                except:
                                    pass
                            
                            # Log detalhado
                            logger.log_nuke(f"Cargo perigoso criado e removido: {role.name} por {user.name}", user)
                            logger.log_security("CRITICAL", f"Tentativa de criar cargo admin: {role.name}", user)
                            
                            # Notificar owner
                            await self.notificar_owner(
                                guild,
                                f"🚨 **TENTATIVA DE NUKE DETECTADA**\n"
                                f"**Usuário:** {user.mention} ({user.id})\n"
                                f"**Ação:** Criou cargo perigoso `{role.name}`\n"
                                f"**Status:** Bloqueado e usuário expulso\n"
                                f"**Permissões:** {role.permissions.value}"
                            )
                            
                        except Exception as e:
                            logger.log_system(f"Erro ao deletar cargo perigoso: {e}", "ERROR")
                
                break
    
    async def monitorar_delecao_cargo(self, role: discord.Role):
        """Monitora deleção de cargos"""
        guild = role.guild
        
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.role_delete):
            if entry.target.id == role.id:
                user = entry.user
                
                # Se o cargo deletado é importante (staff ou bot)
                if role.name.lower() in ['staff', 'admin', 'administrator', 'mod', 'moderator', bot.user.name.lower()]:
                    if not whitelist_master.is_whitelisted(user.id) and user != guild.owner:
                        
                        # AUTO-RESTORE: Recriar cargo
                        try:
                            restored_role = await guild.create_role(
                                name=role.name,
                                color=role.color,
                                hoist=role.hoist,
                                mentionable=role.mentionable,
                                permissions=role.permissions,
                                reason="Auto-Restore: Cargo importante deletado"
                            )
                            
                            # Restaurar posição se possível
                            try:
                                await restored_role.edit(position=role.position)
                            except:
                                pass
                            
                            # Punição automática
                            if user != guild.owner and user != bot.user:
                                try:
                                    await user.kick(reason="Tentativa de deletar cargo importante")
                                    logger.log_action("KICK", user, role, "Deleção de cargo importante")
                                except:
                                    pass
                            
                            # Log
                            logger.log_nuke(f"Cargo importante restaurado: {role.name} (deletado por {user.name})", user)
                            
                            # Notificar
                            await self.notificar_owner(
                                guild,
                                f"🛡️ **CARGO RESTAURADO AUTOMATICAMENTE**\n"
                                f"**Usuário:** {user.mention} ({user.id})\n"
                                f"**Ação:** Deletou cargo importante `{role.name}`\n"
                                f"**Status:** Cargo restaurado, usuário punido"
                            )
                            
                        except Exception as e:
                            logger.log_system(f"Erro ao restaurar cargo: {e}", "ERROR")
                
                break
    
    async def monitorar_delecao_canal(self, channel: discord.abc.GuildChannel):
        """Monitora deleção de canais"""
        guild = channel.guild
        
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_delete):
            if entry.target.id == channel.id:
                user = entry.user
                
                if not whitelist_master.is_whitelisted(user.id) and user != guild.owner and user != bot.user:
                    
                    # Verificar se é deleção em massa
                    user_id = user.id
                    agora = datetime.utcnow()
                    
                    if user_id not in self.cooldowns:
                        self.cooldowns[user_id] = []
                    
                    self.cooldowns[user_id].append(agora)
                    
                    # Limpar timestamps antigos
                    self.cooldowns[user_id] = [t for t in self.cooldowns[user_id] if agora - t < timedelta(seconds=10)]
                    
                    # Se deletou mais de 2 canais em 10 segundos
                    if len(self.cooldowns[user_id]) > 2:
                        # MODO EMERGENCIAL: Banir usuário
                        try:
                            await user.ban(reason="Deleção em massa de canais (Anti-Nuke)", delete_message_days=1)
                            logger.log_nuke(f"BAN por deleção em massa: {user.name} deletou {len(self.cooldowns[user_id])} canais", user)
                            
                            # Notificar modo de emergência
                            await self.notificar_owner(
                                guild,
                                f"🚨🚨 **EMERGÊNCIA: DELETOR EM MASSA**\n"
                                f"**Usuário:** {user.mention} ({user.id})\n"
                                f"**Ação:** Deletou {len(self.cooldowns[user_id])} canais em 10 segundos\n"
                                f"**Status:** BANIDO AUTOMATICAMENTE\n"
                                f"**Hora:** {agora.strftime('%H:%M:%S')}"
                            )
                            
                        except Exception as e:
                            logger.log_system(f"Erro ao banir deletor em massa: {e}", "ERROR")
                    
                    else:
                        # AUTO-RESTORE: Recriar canal
                        try:
                            if isinstance(channel, discord.TextChannel):
                                novo_canal = await channel.category.create_text_channel(
                                    name=channel.name,
                                    topic=channel.topic,
                                    nsfw=channel.nsfw,
                                    slowmode_delay=channel.slowmode_delay,
                                    position=channel.position,
                                    overwrites=channel.overwrites,
                                    reason="Auto-Restore: Canal deletado"
                                ) if channel.category else await guild.create_text_channel(
                                    name=channel.name,
                                    topic=channel.topic,
                                    nsfw=channel.nsfw,
                                    slowmode_delay=channel.slowmode_delay,
                                    position=channel.position,
                                    overwrites=channel.overwrites,
                                    reason="Auto-Restore: Canal deletado"
                                )
                            elif isinstance(channel, discord.VoiceChannel):
                                novo_canal = await channel.category.create_voice_channel(
                                    name=channel.name,
                                    bitrate=channel.bitrate,
                                    user_limit=channel.user_limit,
                                    position=channel.position,
                                    overwrites=channel.overwrites,
                                    reason="Auto-Restore: Canal deletado"
                                ) if channel.category else await guild.create_voice_channel(
                                    name=channel.name,
                                    bitrate=channel.bitrate,
                                    user_limit=channel.user_limit,
                                    position=channel.position,
                                    overwrites=channel.overwrites,
                                    reason="Auto-Restore: Canal deletado"
                                )
                            
                            # Punição para deletor
                            try:
                                await user.kick(reason="Tentativa de deletar canal")
                                logger.log_action("KICK", user, channel, "Deleção de canal")
                            except:
                                pass
                            
                            logger.log_nuke(f"Canal restaurado: #{channel.name} (deletado por {user.name})", user)
                            
                            # Notificar
                            await self.notificar_owner(
                                guild,
                                f"🛡️ **CANAL RESTAURADO AUTOMATICAMENTE**\n"
                                f"**Usuário:** {user.mention} ({user.id})\n"
                                f"**Ação:** Deletou canal `#{channel.name}`\n"
                                f"**Status:** Canal restaurado, usuário expulso"
                            )
                            
                        except Exception as e:
                            logger.log_system(f"Erro ao restaurar canal: {e}", "ERROR")
                
                break
    
    async def monitorar_alteracao_cargo(self, before: discord.Role, after: discord.Role):
        """Monitora alterações em cargos"""
        guild = after.guild
        
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.role_update):
            if entry.target.id == after.id:
                user = entry.user
                
                # Verificar se alguém não autorizado deu permissões perigosas
                if not whitelist_master.is_whitelisted(user.id) and user != guild.owner:
                    
                    # Verificar se foram adicionadas permissões perigosas
                    perms_antes = before.permissions
                    perms_depois = after.permissions
                    
                    perigosas_adicionadas = []
                    for perm in whitelist_master.PERMISSIONS_PERIGOSAS:
                        if not getattr(perms_antes, perm) and getattr(perms_depois, perm):
                            perigosas_adicionadas.append(perm)
                    
                    if perigosas_adicionadas:
                        # REVERTER: Remover permissões perigosas
                        try:
                            # Criar novas permissões (removendo as perigosas)
                            novas_perms = after.permissions
                            for perm in perigosas_adicionadas:
                                setattr(novas_perms, perm, False)
                            
                            await after.edit(permissions=novas_perms, reason="Anti-Nuke: Permissões perigosas removidas")
                            
                            # Punição automática
                            if user != guild.owner and user != bot.user:
                                try:
                                    await user.kick(reason="Tentativa de escalar permissões de cargo")
                                    logger.log_action("KICK", user, after, "Alteração de permissões perigosas")
                                except:
                                    pass
                            
                            logger.log_nuke(f"Permissões perigosas revertidas no cargo: {after.name} (alterado por {user.name})", user)
                            logger.log_security("HIGH", f"Tentativa de escalar cargo {after.name}", user)
                            
                            # Log detalhado de permissões
                            logger.log_permission("ROLE_UPDATE", user, after.name, perms_antes.value, perms_depois.value)
                            
                            # Notificar
                            await self.notificar_owner(
                                guild,
                                f"⚠️ **TENTATIVA DE ESCALAR PERMISSÕES**\n"
                                f"**Usuário:** {user.mention} ({user.id})\n"
                                f"**Cargo:** @{after.name}\n"
                                f"**Permissões adicionadas:** {', '.join(perigosas_adicionadas)}\n"
                                f"**Status:** Revertido automaticamente"
                            )
                            
                        except Exception as e:
                            logger.log_system(f"Erro ao reverter permissões: {e}", "ERROR")
                
                break
    
    async def monitorar_membro_update(self, before: discord.Member, after: discord.Member):
        """Monitora atualização de membros (cargos)"""
        if before.roles != after.roles:
            # Verificar cargos adicionados
            cargos_adicionados = [role for role in after.roles if role not in before.roles]
            
            for cargo in cargos_adicionados:
                if whitelist_master.tem_permissao_perigosa(cargo.permissions):
                    # Verificar quem adicionou
                    guild = after.guild
                    
                    async for entry in guild.audit_logs(limit=10, action=discord.AuditLogAction.member_role_update):
                        if entry.target.id == after.id:
                            user = entry.user
                            
                            # Se quem deu o cargo não está na whitelist
                            if not whitelist_master.is_whitelisted(user.id) and user != guild.owner:
                                
                                # REMOVER CARGO PERIGOSO
                                try:
                                    await after.remove_roles(cargo, reason=f"Anti-Nuke: Cargo perigoso dado por não autorizado - {user.name}")
                                    
                                    # Punição automática para quem deu o cargo
                                    if user != guild.owner and user != bot.user:
                                        try:
                                            await user.kick(reason="Tentativa de dar cargo perigoso")
                                            logger.log_action("KICK", user, after, "Dar cargo perigoso")
                                        except:
                                            pass
                                    
                                    # Se o membro que recebeu também não está na whitelist, punir também
                                    if not whitelist_master.is_whitelisted(after.id) and after != guild.owner:
                                        try:
                                            await after.kick(reason="Tentativa de receber cargo perigoso")
                                            logger.log_action("KICK", after, cargo, "Receber cargo perigoso")
                                        except:
                                            pass
                                    
                                    logger.log_nuke(f"Cargo perigoso removido: {cargo.name} de {after.name} (dado por {user.name})", user)
                                    logger.log_security("HIGH", f"Tentativa de dar cargo admin {cargo.name} para {after.name}", user)
                                    
                                    # Notificar
                                    await self.notificar_owner(
                                        guild,
                                        f"🛡️ **CARGO PERIGOSO BLOQUEADO**\n"
                                        f"**Quem deu:** {user.mention} ({user.id})\n"
                                        f"**Quem recebeu:** {after.mention} ({after.id})\n"
                                        f"**Cargo:** @{cargo.name}\n"
                                        f"**Status:** Cargo removido, ambos punidos"
                                    )
                                    
                                except Exception as e:
                                    logger.log_system(f"Erro ao remover cargo perigoso: {e}", "ERROR")
                            
                            break
    
    async def monitorar_ban(self, guild: discord.Guild, user: discord.User):
        """Monitora banimentos"""
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.ban):
            if entry.target.id == user.id:
                banner = entry.user
                
                if not whitelist_master.is_whitelisted(banner.id) and banner != guild.owner:
                    
                    # DESBANIR automaticamente
                    try:
                        await guild.unban(user, reason="Anti-Nuke: Banimento por não autorizado")
                        
                        # Punir quem baniu
                        if banner != guild.owner and banner != bot.user:
                            try:
                                await banner.kick(reason="Tentativa de banir membro")
                                logger.log_action("KICK", banner, user, "Banimento não autorizado")
                            except:
                                pass
                        
                        logger.log_nuke(f"Banimento revertido: {user.name} (banido por {banner.name})", banner)
                        
                        # Notificar
                        await self.notificar_owner(
                            guild,
                            f"🛡️ **BANIMENTO REVERTIDO**\n"
                            f"**Quem baniu:** {banner.mention} ({banner.id})\n"
                            f"**Quem foi banido:** {user.name} ({user.id})\n"
                            f"**Status:** Desbanido automaticamente"
                        )
                        
                    except Exception as e:
                        logger.log_system(f"Erro ao reverter ban: {e}", "ERROR")
                
                break
    
    async def monitorar_kick(self, member: discord.Member):
        """Monitora expulsões"""
        async for entry in member.guild.audit_logs(limit=5, action=discord.AuditLogAction.kick):
            if entry.target.id == member.id:
                kicker = entry.user
                
                if not whitelist_master.is_whitelisted(kicker.id) and kicker != member.guild.owner:
                    
                    # Tentar readicionar o membro (se possível via convite)
                    # Como não podemos forçar reentrada, apenas punimos quem expulsou
                    
                    try:
                        await kicker.kick(reason="Tentativa de expulsar membro")
                        logger.log_action("KICK", kicker, member, "Expulsão não autorizada")
                        
                        logger.log_nuke(f"Kicker punido: {kicker.name} (expulsou {member.name})", kicker)
                        
                        # Notificar
                        await self.notificar_owner(
                            member.guild,
                            f"🛡️ **EXPULSÃO BLOQUEADA**\n"
                            f"**Quem expulsou:** {kicker.mention} ({kicker.id})\n"
                            f"**Quem foi expulso:** {member.name} ({member.id})\n"
                            f"**Status:** Expulsor punido"
                        )
                        
                    except Exception as e:
                        logger.log_system(f"Erro ao punir kicker: {e}", "ERROR")
                
                break
    
    async def monitorar_criacao_invite(self, invite: discord.Invite):
        """Monitora criação de convites"""
        guild = invite.guild
        
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.invite_create):
            if entry.target.code == invite.code:
                user = entry.user
                
                if not whitelist_master.is_whitelisted(user.id) and user != guild.owner:
                    
                    # DELETAR convite
                    try:
                        await invite.delete(reason="Anti-Nuke: Convite criado por não autorizado")
                        
                        # Punir criador
                        if user != guild.owner and user != bot.user:
                            try:
                                await user.kick(reason="Criação de convite não autorizada")
                                logger.log_action("KICK", user, invite, "Criação de convite")
                            except:
                                pass
                        
                        logger.log_nuke(f"Convite deletado: criado por {user.name}", user)
                        
                    except Exception as e:
                        logger.log_system(f"Erro ao deletar convite: {e}", "ERROR")
                
                break
    
    async def monitorar_criacao_webhook(self, webhook: discord.Webhook):
        """Monitora criação de webhooks"""
        guild = webhook.guild
        
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.webhook_create):
            if entry.target.id == webhook.id:
                user = entry.user
                
                if not whitelist_master.is_whitelisted(user.id) and user != guild.owner:
                    
                    # DELETAR webhook
                    try:
                        await webhook.delete(reason="Anti-Nuke: Webhook criado por não autorizado")
                        
                        # Punir criador
                        if user != guild.owner and user != bot.user:
                            try:
                                await user.kick(reason="Criação de webhook não autorizada")
                                logger.log_action("KICK", user, webhook, "Criação de webhook")
                            except:
                                pass
                        
                        logger.log_nuke(f"Webhook deletado: criado por {user.name}", user)
                        logger.log_security("MEDIUM", f"Webhook malicioso deletado", user)
                        
                    except Exception as e:
                        logger.log_system(f"Erro ao deletar webhook: {e}", "ERROR")
                
                break
    
    async def monitorar_movimento_cargo(self, role: discord.Role, before_pos: int, after_pos: int):
        """Monitora movimentação de cargos na hierarquia"""
        guild = role.guild
        
        async for entry in guild.audit_logs(limit=5):
            if entry.action == discord.AuditLogAction.role_update:
                if entry.target.id == role.id:
                    user = entry.user
                    
                    # Se alguém tentou mover cargo acima do bot ou de staff
                    bot_role = guild.me.top_role
                    if after_pos > bot_role.position and not whitelist_master.is_whitelisted(user.id):
                        
                        # REVERTER posição
                        try:
                            await role.edit(position=before_pos, reason="Anti-Nuke: Tentativa de mover cargo acima do bot")
                            
                            # Punir
                            if user != guild.owner and user != bot.user:
                                try:
                                    await user.kick(reason="Tentativa de mover cargo acima do bot")
                                    logger.log_action("KICK", user, role, "Movimentação de cargo")
                                except:
                                    pass
                            
                            logger.log_nuke(f"Posição de cargo revertida: {role.name} (movido por {user.name})", user)
                            
                        except Exception as e:
                            logger.log_system(f"Erro ao reverter posição de cargo: {e}", "ERROR")
                    
                    break
    
    async def notificar_owner(self, guild: discord.Guild, message: str):
        """Notifica o owner sobre eventos críticos"""
        try:
            owner = guild.owner
            if owner:
                embed = discord.Embed(
                    title="🔔 Notificação de Segurança",
                    description=message,
                    color=discord.Color.red(),
                    timestamp=datetime.utcnow()
                )
                
                # Tentar enviar DM
                try:
                    await owner.send(embed=embed)
                except:
                    # Se não conseguir DM, tentar canal de logs
                    log_channel = await self.get_log_channel(guild)
                    if log_channel:
                        await log_channel.send(f"{owner.mention}", embed=embed)
        except Exception as e:
            logger.log_system(f"Erro ao notificar owner: {e}", "ERROR")
    
    async def get_log_channel(self, guild: discord.Guild) -> Optional[discord.TextChannel]:
        """Obtém ou cria canal de logs"""
        # Procurar canal existente
        for channel in guild.text_channels:
            if 'logs' in channel.name.lower() or 'log' in channel.name.lower() or 'audit' in channel.name.lower():
                return channel
        
        # Criar novo canal
        try:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
            }
            
            # Adicionar permissão para whitelist
            for user_id in whitelist_master.whitelist:
                member = guild.get_member(user_id)
                if member:
                    overwrites[member] = discord.PermissionOverwrite(read_messages=True)
            
            channel = await guild.create_text_channel(
                '🚨-security-logs',
                overwrites=overwrites,
                reason="Canal de logs de segurança criado automaticamente"
            )
            
            return channel
        except Exception as e:
            logger.log_system(f"Erro ao criar canal de logs: {e}", "ERROR")
            return None

anti_nuke = AntiNukeProfessional()

# ==============================================
# SISTEMA ANTI-RAID PROFISSIONAL
# ==============================================

class AntiRaidProfessional:
    """Sistema Anti-Raid completo"""
    
    def __init__(self):
        self.join_timestamps = defaultdict(list)
        self.suspicious_joins = defaultdict(list)
        self.raid_mode = False
        self.siege_mode = False
        self.invite_usage = defaultdict(int)
        
    async def monitorar_entrada(self, member: discord.Member):
        """Monitora entrada de membros"""
        agora = datetime.utcnow()
        guild_id = member.guild.id
        
        # Adicionar timestamp
        self.join_timestamps[guild_id].append(agora)
        
        # Limpar timestamps antigos (últimos 10 segundos)
        self.join_timestamps[guild_id] = [
            t for t in self.join_timestamps[guild_id]
            if agora - t < timedelta(seconds=10)
        ]
        
        # Verificar se é conta suspeita
        is_suspicious = await self.verificar_conta_suspeita(member)
        
        if is_suspicious:
            self.suspicious_joins[guild_id].append({
                'member': member,
                'timestamp': agora,
                'reason': is_suspicious
            })
            
            logger.log_raid(f"Conta suspeita detectada: {member.name} - {is_suspicious}", member)
        
        # Verificar se há raid (muitas entradas em pouco tempo)
        if len(self.join_timestamps[guild_id]) > 7:  # Mais de 7 entradas em 10 segundos
            if not self.raid_mode:
                await self.ativar_modo_raid(member.guild)
        
        # Se há muitas contas suspeitas
        if len(self.suspicious_joins[guild_id]) > 3:
            await self.lidar_com_contas_suspeitas(member.guild)
    
    async def verificar_conta_suspeita(self, member: discord.Member) -> Optional[str]:
        """Verifica se uma conta é suspeita"""
        agora = datetime.utcnow()
        idade_conta = agora - member.created_at
        
        # Conta muito nova (menos de 1 dia)
        if idade_conta < timedelta(days=1):
            return f"Conta muito nova ({idade_conta.days} dias)"
        
        # Conta com nome genérico
        generic_names = ['user', 'discord', 'admin', 'test', 'hello', 'hi', 'new']
        if any(name in member.name.lower() for name in generic_names):
            return "Nome genérico/suspeito"
        
        # Sem avatar
        if not member.avatar:
            return "Sem avatar (conta padrão)"
        
        # Verificar fingerprint
        if not whitelist_master.verificar_fingerprint(member):
            return "Fingerprint alterado (conta possivelmente hackeada)"
        
        return None
    
    async def ativar_modo_raid(self, guild: discord.Guild):
        """Ativa modo de proteção contra raid"""
        self.raid_mode = True
        logger.log_raid(f"MODO RAID ATIVADO no servidor {guild.name}", None)
        
        # Fechar servidor (revogar todos convites)
        await self.fechar_servidor(guild)
        
        # Banir contas suspeitas
        await self.banir_contas_suspeitas(guild)
        
        # Notificar owner
        try:
            owner = guild.owner
            if owner:
                embed = discord.Embed(
                    title="🚨 MODO RAID ATIVADO",
                    description=(
                        "**Detectada entrada em massa de contas suspeitas!**\n\n"
                        "✅ Todos convites foram revogados\n"
                        "✅ Contas suspeitas banidas\n"
                        "✅ Servidor fechado temporariamente\n\n"
                        "O modo será desativado automaticamente em 30 minutos."
                    ),
                    color=discord.Color.dark_red(),
                    timestamp=datetime.utcnow()
                )
                
                await owner.send(embed=embed)
        except:
            pass
        
        # Agendar desativação
        asyncio.create_task(self.desativar_modo_raid(guild))
    
    async def fechar_servidor(self, guild: discord.Guild):
        """Fecha o servidor (revoga todos convites)"""
        try:
            invites = await guild.invites()
            for invite in invites:
                try:
                    await invite.delete(reason="Modo raid ativado")
                except:
                    pass
            
            logger.log_raid(f"Todos convites revogados no servidor {guild.name}", None)
        except Exception as e:
            logger.log_system(f"Erro ao revogar convites: {e}", "ERROR")
    
    async def banir_contas_suspeitas(self, guild: discord.Guild):
        """Banir contas suspeitas recentes"""
        guild_id = guild.id
        
        if guild_id in self.suspicious_joins:
            for entry in self.suspicious_joins[guild_id]:
                member = entry['member']
                reason = entry['reason']
                
                try:
                    await member.ban(reason=f"Anti-Raid: {reason}", delete_message_days=1)
                    logger.log_action("BAN", bot.user, member, f"Anti-Raid: {reason}")
                except:
                    pass
        
        # Limpar lista após banir
        self.suspicious_joins[guild_id] = []
    
    async def lidar_com_contas_suspeitas(self, guild: discord.Guild):
        """Lida com múltiplas contas suspeitas"""
        guild_id = guild.id
        
        if len(self.suspicious_joins[guild_id]) > 5:
            await self.ativar_modo_raid(guild)
        elif len(self.suspicious_joins[guild_id]) > 2:
            # Apenas banir as suspeitas
            await self.banir_contas_suspeitas(guild)
    
    async def desativar_modo_raid(self, guild: discord.Guild):
        """Desativa modo raid após 30 minutos"""
        await asyncio.sleep(1800)  # 30 minutos
        
        self.raid_mode = False
        logger.log_raid(f"MODO RAID DESATIVADO no servidor {guild.name}", None)
        
        # Notificar owner
        try:
            owner = guild.owner
            if owner:
                embed = discord.Embed(
                    title="🟢 MODO RAID DESATIVADO",
                    description="O modo raid foi desativado automaticamente após 30 minutos.",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
                
                await owner.send(embed=embed)
        except:
            pass
    
    async def monitorar_spam(self, message: discord.Message):
        """Monitora spam de mensagens"""
        author_id = message.author.id
        agora = datetime.utcnow()
        
        if author_id not in self.join_timestamps:
            self.join_timestamps[author_id] = []
        
        self.join_timestamps[author_id].append(agora)
        
        # Manter apenas últimos 10 segundos
        self.join_timestamps[author_id] = [
            t for t in self.join_timestamps[author_id]
            if agora - t < timedelta(seconds=10)
        ]
        
        # Se enviou mais de 10 mensagens em 10 segundos
        if len(self.join_timestamps[author_id]) > 10:
            await self.lidar_com_spammer(message.author, message.guild)
    
    async def lidar_com_spammer(self, member: discord.Member, guild: discord.Guild):
        """Lida com spammers"""
        try:
            # Banir spammer
            await member.ban(reason="Anti-Raid: Spam em massa", delete_message_days=1)
            
            logger.log_raid(f"Spammer banido: {member.name} ({len(self.join_timestamps[member.id])} mensagens em 10s)", member)
            logger.log_action("BAN", bot.user, member, "Spam em massa")
            
            # Limpar cache
            if member.id in self.join_timestamps:
                del self.join_timestamps[member.id]
        except Exception as e:
            logger.log_system(f"Erro ao banir spammer: {e}", "ERROR")

anti_raid = AntiRaidProfessional()

# ==============================================
# SISTEMA DE VOICE PERMANENTE
# ==============================================

class VoicePermanente:
    """Sistema de presença permanente em voice"""
    
    def __init__(self):
        self.voice_channel_id = VOICE_CHANNEL_ID
        self.voice_client = None
        self.permanent_voice = None
        
    async def conectar_voice(self, guild: discord.Guild):
        """Conecta ao canal de voz configurado"""
        if not self.voice_channel_id:
            return
        
        try:
            channel = guild.get_channel(self.voice_channel_id)
            if channel and isinstance(channel, discord.VoiceChannel):
                
                # Se já está conectado, desconectar
                if self.voice_client and self.voice_client.is_connected():
                    await self.voice_client.disconnect()
                
                # Conectar
                self.voice_client = await channel.connect()
                
                # Configurar permissões para bloquear entrada
                await self.configurar_permissões_voice(channel)
                
                logger.log_system(f"✅ Conectado permanentemente ao canal de voz: {channel.name}")
                
                # Iniciar verificação periódica
                if not verificar_conexao_voice.is_running():
                    verificar_conexao_voice.start()
                    
        except Exception as e:
            logger.log_system(f"❌ Erro ao conectar ao voice: {e}", "ERROR")
    
    async def configurar_permissões_voice(self, channel: discord.VoiceChannel):
        """Configura permissões para bloquear entrada no canal"""
        try:
            # Permitir apenas visualização para todos
            overwrites = {
                channel.guild.default_role: discord.PermissionOverwrite(
                    connect=False,  # Ninguém pode conectar
                    view_channel=True  # Todos podem ver
                ),
                channel.guild.me: discord.PermissionOverwrite(
                    connect=True,
                    speak=False,
                    stream=False
                )
            }
            
            # Permitir conexão apenas para whitelist
            for user_id in whitelist_master.whitelist:
                member = channel.guild.get_member(user_id)
                if member:
                    overwrites[member] = discord.PermissionOverwrite(connect=True)
            
            await channel.edit(overwrites=overwrites, reason="Proteção de canal permanente")
            
        except Exception as e:
            logger.log_system(f"Erro ao configurar permissões do voice: {e}", "ERROR")
    
    async def recriar_canal(self, guild: discord.Guild):
        """Recria o canal de voz se foi deletado"""
        try:
            # Verificar se canal ainda existe
            channel = guild.get_channel(self.voice_channel_id)
            
            if not channel:
                # Criar novo canal
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(
                        connect=False,
                        view_channel=True
                    ),
                    guild.me: discord.PermissionOverwrite(
                        connect=True,
                        speak=False,
                        stream=False
                    )
                }
                
                new_channel = await guild.create_voice_channel(
                    "🔒 Voice Secure",
                    overwrites=overwrites,
                    reason="Canal de voz permanente recriado"
                )
                
                self.voice_channel_id = new_channel.id
                
                # Reconectar
                await self.conectar_voice(guild)
                
                logger.log_system(f"✅ Canal de voz recriado: {new_channel.name}")
                
        except Exception as e:
            logger.log_system(f"❌ Erro ao recriar canal de voz: {e}", "ERROR")
    
    async def mover_intruso(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """Move intrusos que tentarem entrar no canal"""
        if after.channel and after.channel.id == self.voice_channel_id:
            if member.id != bot.user.id and not whitelist_master.is_whitelisted(member.id):
                
                # Mover para outro canal de voz
                outros_canais = [c for c in member.guild.voice_channels if c.id != self.voice_channel_id]
                
                if outros_canais:
                    try:
                        await member.move_to(random.choice(outros_canais))
                        
                        # Avisar
                        try:
                            await member.send("❌ Você não tem permissão para entrar no canal seguro!")
                        except:
                            pass
                        
                        logger.log_action("VOICE_MOVE", member, after.channel, "Tentativa de entrar no canal seguro")
                        
                    except Exception as e:
                        logger.log_system(f"Erro ao mover intruso do voice: {e}", "ERROR")

voice_permanente = VoicePermanente()

# ==============================================
# SISTEMA DE BACKUP/RESTORE ABSOLUTO
# ==============================================

class BackupRestoreMaster:
    """Sistema completo de backup e restore"""
    
    def __init__(self):
        self.backup_file = 'backup_completo.json'
        self.backup_cache = {}
        
    async def criar_backup_completo(self, guild: discord.Guild) -> Dict[str, Any]:
        """Cria backup absoluto de tudo"""
        logger.log_backup(f"Iniciando backup completo do servidor: {guild.name}")
        
        backup = {
            'metadata': {
                'guild_id': str(guild.id),
                'guild_name': guild.name,
                'owner_id': str(guild.owner_id),
                'icon_url': str(guild.icon.url) if guild.icon else None,
                'banner_url': str(guild.banner.url) if guild.banner else None,
                'description': guild.description,
                'created_at': guild.created_at.isoformat(),
                'backup_date': datetime.utcnow().isoformat(),
                'backup_version': '3.0',
                'total_members': guild.member_count
            },
            'settings': await self._backup_settings(guild),
            'roles': await self._backup_roles(guild),
            'categories': await self._backup_categories(guild),
            'channels': await self._backup_channels(guild),
            'emoji': await self._backup_emoji(guild),
            'whitelist': whitelist_master.whitelist,
            'voice_config': {
                'voice_channel_id': voice_permanente.voice_channel_id
            }
        }
        
        logger.log_backup(f"Backup concluído: {len(backup['roles'])} cargos, {len(backup['channels'])} canais")
        
        return backup
    
    async def _backup_settings(self, guild: discord.Guild) -> Dict[str, Any]:
        """Backup das configurações do servidor"""
        return {
            'system_channel_id': str(guild.system_channel.id) if guild.system_channel else None,
            'rules_channel_id': str(guild.rules_channel.id) if guild.rules_channel else None,
            'public_updates_channel_id': str(guild.public_updates_channel.id) if guild.public_updates_channel else None,
            'afk_channel_id': str(guild.afk_channel.id) if guild.afk_channel else None,
            'afk_timeout': guild.afk_timeout,
            'verification_level': str(guild.verification_level),
            'default_notifications': str(guild.default_notifications),
            'explicit_content_filter': str(guild.explicit_content_filter),
            'mfa_level': str(guild.mfa_level),
            'premium_tier': guild.premium_tier,
            'premium_subscription_count': guild.premium_subscription_count,
            'preferred_locale': str(guild.preferred_locale),
            'features': guild.features
        }
    
    async def _backup_roles(self, guild: discord.Guild) -> List[Dict[str, Any]]:
        """Backup de todos os cargos"""
        roles_data = []
        
        for role in guild.roles:
            if role.name == "@everyone":
                continue
                
            role_data = {
                'id': str(role.id),
                'name': role.name,
                'color': role.color.value,
                'hoist': role.hoist,
                'position': role.position,
                'permissions': role.permissions.value,
                'mentionable': role.mentionable,
                'display_icon': str(role.display_icon.url) if role.display_icon else None,
                'managed': role.managed,
                'tags': {
                    'bot_id': str(role.tags.bot_id) if role.tags and role.tags.bot_id else None,
                    'premium_subscriber': role.tags.premium_subscriber if role.tags else None
                } if role.tags else {}
            }
            roles_data.append(role_data)
        
        return sorted(roles_data, key=lambda x: x['position'], reverse=True)
    
    async def _backup_categories(self, guild: discord.Guild) -> List[Dict[str, Any]]:
        """Backup de todas as categorias"""
        categories_data = []
        
        for category in guild.categories:
            cat_data = {
                'id': str(category.id),
                'name': category.name,
                'position': category.position,
                'nsfw': category.nsfw,
                'overwrites': self._serialize_overwrites(category.overwrites)
            }
            categories_data.append(cat_data)
        
        return sorted(categories_data, key=lambda x: x['position'])
    
    async def _backup_channels(self, guild: discord.Guild) -> Dict[str, List[Dict[str, Any]]]:
        """Backup de todos os canais"""
        channels_data = {
            'text': [],
            'voice': [],
            'stage': [],
            'forum': []
        }
        
        for channel in guild.channels:
            channel_data = {
                'id': str(channel.id),
                'name': channel.name,
                'category_id': str(channel.category_id) if channel.category else None,
                'position': channel.position,
                'overwrites': self._serialize_overwrites(channel.overwrites),
                'nsfw': getattr(channel, 'nsfw', False)
            }
            
            if isinstance(channel, discord.TextChannel):
                channel_data.update({
                    'topic': channel.topic,
                    'slowmode_delay': channel.slowmode_delay,
                    'default_auto_archive_duration': channel.default_auto_archive_duration,
                    'type': 'text'
                })
                channels_data['text'].append(channel_data)
                
            elif isinstance(channel, discord.VoiceChannel):
                channel_data.update({
                    'bitrate': channel.bitrate,
                    'user_limit': channel.user_limit,
                    'video_quality_mode': str(channel.video_quality_mode),
                    'type': 'voice'
                })
                channels_data['voice'].append(channel_data)
                
            elif isinstance(channel, discord.StageChannel):
                channel_data.update({
                    'bitrate': channel.bitrate,
                    'user_limit': channel.user_limit,
                    'topic': channel.topic,
                    'type': 'stage'
                })
                channels_data['stage'].append(channel_data)
                
            elif isinstance(channel, discord.ForumChannel):
                channel_data.update({
                    'topic': channel.topic,
                    'default_auto_archive_duration': channel.default_auto_archive_duration,
                    'available_tags': [tag.to_dict() for tag in channel.available_tags] if hasattr(channel, 'available_tags') else [],
                    'type': 'forum'
                })
                channels_data['forum'].append(channel_data)
        
        # Ordenar por posição
        for channel_type in channels_data:
            channels_data[channel_type] = sorted(channels_data[channel_type], key=lambda x: x['position'])
        
        return channels_data
    
    async def _backup_emoji(self, guild: discord.Guild) -> List[Dict[str, Any]]:
        """Backup de todos os emojis"""
        emoji_data = []
        
        for emoji in guild.emojis:
            emoji_data.append({
                'id': str(emoji.id),
                'name': emoji.name,
                'url': str(emoji.url),
                'animated': emoji.animated,
                'managed': emoji.managed,
                'available': emoji.available,
                'roles': [str(role.id) for role in emoji.roles]
            })
        
        return emoji_data
    
    def _serialize_overwrites(self, overwrites):
        """Serializa permissões de overwrite"""
        serialized = {}
        for target, overwrite in overwrites.items():
            if target:
                key = f"role_{target.id}" if isinstance(target, discord.Role) else f"member_{target.id}"
                serialized[key] = {
                    'allow': overwrite.pair()[0].value,
                    'deny': overwrite.pair()[1].value
                }
        return serialized
    
    def salvar_backup(self, backup_data: Dict[str, Any]):
        """Salva backup em arquivo"""
        try:
            with open(self.backup_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=4, ensure_ascii=False)
            
            logger.log_backup(f"Backup salvo em {self.backup_file}")
            return True
        except Exception as e:
            logger.log_system(f"Erro ao salvar backup: {e}", "ERROR")
            return False
    
    def carregar_backup(self) -> Optional[Dict[str, Any]]:
        """Carrega backup do arquivo"""
        try:
            if os.path.exists(self.backup_file):
                with open(self.backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.log_backup(f"Backup carregado: {data['metadata']['guild_name']}")
                    return data
        except Exception as e:
            logger.log_system(f"Erro ao carregar backup: {e}", "ERROR")
        
        return None
    
    async def restaurar_backup_completo(self, guild: discord.Guild, backup_data: Dict[str, Any]):
        """RESTAURAÇÃO COMPLETA - Apaga tudo e recria"""
        logger.log_backup(f"Iniciando restauração completa do servidor: {guild.name}")
        
        # CONFIRMAÇÃO DE SEGURANÇA (deve ser feita via UI)
        
        try:
            # 1. SALVAR CONFIGURAÇÕES ATUAIS (backup de emergência)
            backup_emergencia = await self.criar_backup_completo(guild)
            with open('backup_emergencia.json', 'w', encoding='utf-8') as f:
                json.dump(backup_emergencia, f, indent=4)
            
            logger.log_backup("Backup de emergência criado")
            
            # 2. APAGAR TUDO (exceto @everyone e cargos do bot)
            await self._limpar_servidor(guild)
            
            # 3. RESTAURAR CARGOS
            await self._restaurar_cargos(guild, backup_data['roles'])
            
            # 4. RESTAURAR CATEGORIAS
            categories_map = await self._restaurar_categorias(guild, backup_data['categories'])
            
            # 5. RESTAURAR CANAIS
            await self._restaurar_canais(guild, backup_data['channels'], categories_map)
            
            # 6. RESTAURAR CONFIGURAÇÕES
            await self._restaurar_settings(guild, backup_data['settings'])
            
            # 7. RESTAURAR WHITELIST
            if 'whitelist' in backup_data:
                whitelist_master.whitelist = backup_data['whitelist']
                whitelist_master.salvar_whitelist()
            
            # 8. RESTAURAR CONFIG VOICE
            if 'voice_config' in backup_data:
                voice_permanente.voice_channel_id = backup_data['voice_config'].get('voice_channel_id')
            
            logger.log_backup(f"✅ Restauração completa concluída: {guild.name}")
            
            return True
            
        except Exception as e:
            logger.log_system(f"❌ Erro na restauração: {e}", "ERROR")
            logger.log_backup(f"❌ Restauração falhou: {str(e)}")
            return False
    
    async def _limpar_servidor(self, guild: discord.Guild):
        """Limpa o servidor (canais e cargos)"""
        
        # Apagar todos os canais
        for channel in guild.channels:
            try:
                await channel.delete(reason="Restauração completa")
            except:
                pass
        
        # Apagar todos os cargos (exceto @everyone e cargos gerenciados)
        for role in guild.roles:
            if role.name != "@everyone" and not role.managed and role != guild.me.top_role:
                try:
                    await role.delete(reason="Restauração completa")
                except:
                    pass
        
        await asyncio.sleep(2)  # Pausa para evitar rate limit
    
    async def _restaurar_cargos(self, guild: discord.Guild, roles_data: List[Dict[str, Any]]):
        """Restaura todos os cargos"""
        roles_map = {}
        
        for role_data in roles_data:
            try:
                role = await guild.create_role(
                    name=role_data['name'],
                    color=discord.Color(role_data['color']),
                    hoist=role_data['hoist'],
                    permissions=discord.Permissions(role_data['permissions']),
                    mentionable=role_data['mentionable'],
                    reason="Restauração de backup"
                )
                
                roles_map[role_data['id']] = role
                
                # Posição será ajustada depois
                
            except Exception as e:
                logger.log_system(f"Erro ao criar cargo {role_data['name']}: {e}", "ERROR")
        
        # Ajustar posições (do menos importante para o mais importante)
        for role_data in sorted(roles_data, key=lambda x: x['position']):
            if role_data['id'] in roles_map:
                try:
                    await roles_map[role_data['id']].edit(position=role_data['position'])
                except:
                    pass
        
        return roles_map
    
    async def _restaurar_categorias(self, guild: discord.Guild, categories_data: List[Dict[str, Any]]):
        """Restaura todas as categorias"""
        categories_map = {}
        
        for cat_data in categories_data:
            try:
                # Desserializar overwrites
                overwrites = self._deserialize_overwrites(cat_data['overwrites'], guild)
                
                category = await guild.create_category(
                    name=cat_data['name'],
                    position=cat_data['position'],
                    overwrites=overwrites,
                    reason="Restauração de backup"
                )
                
                categories_map[cat_data['id']] = category
                
            except Exception as e:
                logger.log_system(f"Erro ao criar categoria {cat_data['name']}: {e}", "ERROR")
        
        return categories_map
    
    async def _restaurar_canais(self, guild: discord.Guild, channels_data: Dict[str, List[Dict[str, Any]]], categories_map: Dict[str, discord.CategoryChannel]):
        """Restaura todos os canais"""
        
        # Função para criar overwrites
        def criar_overwrites(overwrites_data):
            overwrites = {}
            for key, perm_data in overwrites_data.items():
                try:
                    if key.startswith('role_'):
                        role_id = int(key.split('_')[1])
                        role = guild.get_role(role_id)
                        if role:
                            overwrites[role] = discord.PermissionOverwrite(
                                allow=discord.Permissions(perm_data['allow']),
                                deny=discord.Permissions(perm_data['deny'])
                            )
                except:
                    pass
            return overwrites
        
        # Restaurar canais de texto
        for channel_data in channels_data.get('text', []):
            try:
                category = categories_map.get(channel_data['category_id']) if channel_data.get('category_id') else None
                overwrites = criar_overwrites(channel_data['overwrites'])
                
                channel = await guild.create_text_channel(
                    name=channel_data['name'],
                    category=category,
                    position=channel_data['position'],
                    topic=channel_data.get('topic'),
                    slowmode_delay=channel_data.get('slowmode_delay', 0),
                    nsfw=channel_data.get('nsfw', False),
                    overwrites=overwrites,
                    reason="Restauração de backup"
                )
                
            except Exception as e:
                logger.log_system(f"Erro ao criar canal de texto {channel_data['name']}: {e}", "ERROR")
        
        # Restaurar canais de voz
        for channel_data in channels_data.get('voice', []):
            try:
                category = categories_map.get(channel_data['category_id']) if channel_data.get('category_id') else None
                overwrites = criar_overwrites(channel_data['overwrites'])
                
                channel = await guild.create_voice_channel(
                    name=channel_data['name'],
                    category=category,
                    position=channel_data['position'],
                    bitrate=min(channel_data.get('bitrate', 64000), guild.bitrate_limit),
                    user_limit=channel_data.get('user_limit', 0),
                    overwrites=overwrites,
                    reason="Restauração de backup"
                )
                
            except Exception as e:
                logger.log_system(f"Erro ao criar canal de voz {channel_data['name']}: {e}", "ERROR")
    
    async def _restaurar_settings(self, guild: discord.Guild, settings_data: Dict[str, Any]):
        """Restaura configurações do servidor"""
        try:
            update_data = {}
            
            # Canal de sistema
            if settings_data.get('system_channel_id'):
                channel = guild.get_channel(int(settings_data['system_channel_id']))
                if channel:
                    update_data['system_channel'] = channel
            
            # Canal de regras
            if settings_data.get('rules_channel_id'):
                channel = guild.get_channel(int(settings_data['rules_channel_id']))
                if channel:
                    update_data['rules_channel'] = channel
            
            # Canal de atualizações
            if settings_data.get('public_updates_channel_id'):
                channel = guild.get_channel(int(settings_data['public_updates_channel_id']))
                if channel:
                    update_data['public_updates_channel'] = channel
            
            # AFK
            if settings_data.get('afk_channel_id'):
                channel = guild.get_channel(int(settings_data['afk_channel_id']))
                if channel:
                    update_data['afk_channel'] = channel
            
            if settings_data.get('afk_timeout'):
                update_data['afk_timeout'] = settings_data['afk_timeout']
            
            # Nível de verificação
            if settings_data.get('verification_level'):
                try:
                    update_data['verification_level'] = discord.VerificationLevel[settings_data['verification_level']]
                except:
                    pass
            
            # Filtro de conteúdo
            if settings_data.get('explicit_content_filter'):
                try:
                    update_data['explicit_content_filter'] = discord.ContentFilter[settings_data['explicit_content_filter']]
                except:
                    pass
            
            if update_data:
                await guild.edit(**update_data, reason="Restauração de backup")
                
        except Exception as e:
            logger.log_system(f"Erro ao restaurar settings: {e}", "ERROR")
    
    def _deserialize_overwrites(self, overwrites_data: Dict[str, Any], guild: discord.Guild):
        """Desserializa overwrites"""
        overwrites = {}
        
        for key, perm_data in overwrites_data.items():
            try:
                if key.startswith('role_'):
                    role_id = int(key.split('_')[1])
                    role = guild.get_role(role_id)
                    if role:
                        overwrites[role] = discord.PermissionOverwrite(
                            allow=discord.Permissions(perm_data['allow']),
                            deny=discord.Permissions(perm_data['deny'])
                        )
            except:
                pass
        
        return overwrites

backup_master = BackupRestoreMaster()

# ==============================================
# PAINEL PROFISSIONAL COM BOTÕES
# ==============================================

class CatBotUI:
    """Sistema de UI profissional do Cat Bot"""
    
    @staticmethod
    def create_main_panel() -> discord.Embed:
        """Cria o painel principal"""
        embed = discord.Embed(
            title="🐱 **CAT BOT - PAINEL DE CONTROLE** 🛡️",
            description="Sistema de segurança completo nível empresarial\n"
                       "─────────────────────────────",
            color=discord.Color.from_rgb(47, 49, 54),
            timestamp=datetime.utcnow()
        )
        
        # Status do sistema
        status_fields = [
            ("🛡️ **WHITELIST**", f"`{len(whitelist_master.whitelist)}` administradores", True),
            ("🚨 **ANTI-NUKE**", "✅ **ATIVADO**", True),
            ("⚔️ **ANTI-RAID**", "✅ **ATIVADO**", True),
            ("🎙️ **VOICE**", f"`{'✅ CONECTADO' if voice_permanente.voice_client else '❌ DESCONECTADO'}`", True),
            ("📦 **BACKUP**", f"`{'✅ DISPONÍVEL' if backup_master.carregar_backup() else '❌ NÃO DISPONÍVEL'}`", True),
            ("👥 **MEMBROS**", f"`{sum(g.member_count for g in bot.guilds)}` total", True)
        ]
        
        for name, value, inline in status_fields:
            embed.add_field(name=name, value=value, inline=inline)
        
        embed.add_field(
            name="📊 **ESTATÍSTICAS**",
            value=f"```Servidores: {len(bot.guilds)}\n"
                  f"Canais: {sum(len(g.channels) for g in bot.guilds)}\n"
                  f"Latência: {round(bot.latency * 1000, 2)}ms```",
            inline=False
        )
        
        embed.set_footer(
            text="Cat Bot v3.0 | Sistema Premium",
            icon_url="https://cdn.discordapp.com/emojis/1234567890123456.png"
        )
        
        return embed
    
    @staticmethod
    def create_whitelist_panel() -> discord.Embed:
        """Cria painel da whitelist"""
        embed = discord.Embed(
            title="🛡️ **GERENCIADOR DE WHITELIST**",
            description="Controle total sobre administradores autorizados\n"
                       "─────────────────────────────",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        # Listar whitelist
        if whitelist_master.whitelist:
            lista_formatada = []
            for i, user_id in enumerate(whitelist_master.whitelist[:10], 1):
                user = bot.get_user(user_id)
                nome = user.mention if user else f"`{user_id}`"
                lista_formatada.append(f"**{i}.** {nome}")
            
            embed.add_field(
                name=f"👑 ADMINISTRADORES ({len(whitelist_master.whitelist)})",
                value="\n".join(lista_formatada),
                inline=False
            )
            
            if len(whitelist_master.whitelist) > 10:
                embed.add_field(
                    name="📄 MAIS...",
                    value=f"`+{len(whitelist_master.whitelist) - 10} administradores não exibidos`",
                    inline=False
                )
        else:
            embed.add_field(
                name="📭 WHITELIST VAZIA",
                value="Adicione administradores usando os botões abaixo.",
                inline=False
            )
        
        embed.set_footer(text="Apenas o dono pode gerenciar a whitelist")
        
        return embed
    
    @staticmethod
    def create_backup_panel() -> discord.Embed:
        """Cria painel de backup"""
        backup_data = backup_master.carregar_backup()
        
        embed = discord.Embed(
            title="📦 **SISTEMA DE BACKUP**",
            description="Backup e restauração completa do servidor\n"
                       "─────────────────────────────",
            color=discord.Color.green() if backup_data else discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        
        if backup_data:
            metadata = backup_data['metadata']
            backup_date = datetime.fromisoformat(metadata['backup_date'])
            idade = datetime.utcnow() - backup_date
            
            embed.add_field(
                name="✅ **BACKUP DISPONÍVEL**",
                value=f"**Servidor:** {metadata['guild_name']}\n"
                      f"**Data:** {backup_date.strftime('%d/%m/%Y %H:%M')}\n"
                      f"**Idade:** {idade.days} dias, {idade.seconds // 3600} horas\n"
                      f"**Versão:** {metadata.get('backup_version', '1.0')}",
                inline=False
            )
            
            embed.add_field(
                name="📊 **CONTEÚDO DO BACKUP**",
                value=f"```Cargos: {len(backup_data['roles'])}\n"
                      f"Categorias: {len(backup_data['categories'])}\n"
                      f"Canais: {len(backup_data['channels'].get('text', [])) + len(backup_data['channels'].get('voice', []))}\n"
                      f"Emojis: {len(backup_data.get('emoji', []))}```",
                inline=False
            )
        else:
            embed.add_field(
                name="❌ **NENHUM BACKUP**",
                value="Nenhum backup foi criado ainda.\n"
                      "Clique em **Criar Backup** para fazer o primeiro backup.",
                inline=False
            )
        
        embed.set_footer(text="⚠️ Restauração apaga tudo e recria do backup")
        
        return embed
    
    @staticmethod
    def create_security_panel() -> discord.Embed:
        """Cria painel de segurança"""
        embed = discord.Embed(
            title="🚨 **PAINEL DE SEGURANÇA**",
            description="Configurações avançadas de proteção\n"
                       "─────────────────────────────",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        status_anti_nuke = "✅ **ATIVADO**"
        status_anti_raid = "✅ **ATIVADO**" if not anti_raid.raid_mode else "🚨 **MODO RAID ATIVO**"
        status_lockdown = "✅ **DESATIVADO**" if not anti_nuke.lockdown_mode else "🔒 **LOCKDOWN ATIVO**"
        
        embed.add_field(
            name="🛡️ **PROTEÇÕES**",
            value=f"**Anti-Nuke:** {status_anti_nuke}\n"
                  f"**Anti-Raid:** {status_anti_raid}\n"
                  f"**Lockdown:** {status_lockdown}\n"
                  f"**Auto-Restore:** ✅ **ATIVADO**",
            inline=False
        )
        
        embed.add_field(
            name="⚙️ **CONFIGURAÇÕES**",
            value="```Modo Fantasma: ✅ ATIVADO\n"
                  "Logs Protegidos: ✅ ATIVADO\n"
                  "Auto-Ban Spam: ✅ ATIVADO\n"
                  "Detecção Webhook: ✅ ATIVADO```",
            inline=False
        )
        
        embed.add_field(
            name="📈 **ESTATÍSTICAS**",
            value=f"```Tentativas bloqueadas: {len(anti_nuke.suspicious_actions)}\n"
                  f"Contas banidas: {sum(len(v) for v in anti_raid.suspicious_joins.values())}\n"
                  f"Restaurações: {len(anti_nuke.auto_restore_queue)}```",
            inline=False
        )
        
        embed.set_footer(text="Configurações em tempo real")
        
        return embed

# Componentes UI
class WhitelistModal(Modal, title="🛡️ Adicionar à Whitelist"):
    user_id = TextInput(
        label="ID do Usuário",
        placeholder="123456789012345678",
        style=discord.TextStyle.short,
        required=True,
        max_length=20
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id.value)
            
            if interaction.user.id != OWNER_ID:
                await interaction.response.send_message("❌ Apenas o dono pode adicionar à whitelist!", ephemeral=True)
                return
            
            user = interaction.guild.get_member(user_id)
            if not user:
                await interaction.response.send_message("❌ Usuário não encontrado no servidor!", ephemeral=True)
                return
            
            if whitelist_master.adicionar_whitelist(user_id):
                embed = discord.Embed(
                    title="✅ WHITELIST ATUALIZADA",
                    description=f"**Usuário adicionado:** {user.mention} (`{user_id}`)\n"
                               f"**Total de admins:** {len(whitelist_master.whitelist)}",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message("❌ Usuário já está na whitelist!", ephemeral=True)
                
        except ValueError:
            await interaction.response.send_message("❌ ID inválido! Digite apenas números.", ephemeral=True)

class RemoveWhitelistModal(Modal, title="🛡️ Remover da Whitelist"):
    user_id = TextInput(
        label="ID do Usuário",
        placeholder="123456789012345678",
        style=discord.TextStyle.short,
        required=True,
        max_length=20
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            user_id = int(self.user_id.value)
            
            if interaction.user.id != OWNER_ID:
                await interaction.response.send_message("❌ Apenas o dono pode remover da whitelist!", ephemeral=True)
                return
            
            if user_id == OWNER_ID:
                await interaction.response.send_message("❌ Não pode remover o dono da whitelist!", ephemeral=True)
                return
            
            if whitelist_master.remover_whitelist(user_id):
                user = bot.get_user(user_id) or interaction.guild.get_member(user_id)
                user_mention = user.mention if user else f"`{user_id}`"
                
                embed = discord.Embed(
                    title="✅ WHITELIST ATUALIZADA",
                    description=f"**Usuário removido:** {user_mention}\n"
                               f"**Total de admins:** {len(whitelist_master.whitelist)}",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message("❌ Usuário não está na whitelist!", ephemeral=True)
                
        except ValueError:
            await interaction.response.send_message("❌ ID inválido! Digite apenas números.", ephemeral=True)

class VoiceChannelModal(Modal, title="🎙️ Configurar Canal de Voz"):
    channel_id = TextInput(
        label="ID do Canal de Voz",
        placeholder="123456789012345678",
        style=discord.TextStyle.short,
        required=True,
        max_length=20
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            channel_id = int(self.channel_id.value)
            
            if interaction.user.id != OWNER_ID:
                await interaction.response.send_message("❌ Apenas o dono pode configurar o canal de voz!", ephemeral=True)
                return
            
            channel = interaction.guild.get_channel(channel_id)
            if not channel or not isinstance(channel, discord.VoiceChannel):
                await interaction.response.send_message("❌ Canal de voz não encontrado!", ephemeral=True)
                return
            
            voice_permanente.voice_channel_id = channel_id
            await voice_permanente.conectar_voice(interaction.guild)
            
            embed = discord.Embed(
                title="✅ CANAL DE VOZ CONFIGURADO",
                description=f"**Canal definido:** {channel.mention}\n"
                           f"**Status:** Conectado permanentemente\n"
                           f"**Proteção:** Ativada (apenas whitelist pode entrar)",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except ValueError:
            await interaction.response.send_message("❌ ID inválido! Digite apenas números.", ephemeral=True)

# Views (Botões)
class MainPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🛡️ Whitelist", style=discord.ButtonStyle.primary, emoji="🛡️", row=0)
    async def whitelist_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Apenas o dono pode acessar!", ephemeral=True)
            return
        
        embed = CatBotUI.create_whitelist_panel()
        view = WhitelistManagementView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="📦 Backup", style=discord.ButtonStyle.green, emoji="📦", row=0)
    async def backup_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Apenas o dono pode acessar!", ephemeral=True)
            return
        
        embed = CatBotUI.create_backup_panel()
        view = BackupManagementView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="🚨 Segurança", style=discord.ButtonStyle.red, emoji="🚨", row=0)
    async def security_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Apenas o dono pode acessar!", ephemeral=True)
            return
        
        embed = CatBotUI.create_security_panel()
        view = SecurityManagementView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="🎙️ Voice", style=discord.ButtonStyle.secondary, emoji="🎙️", row=1)
    async def voice_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Apenas o dono pode acessar!", ephemeral=True)
            return
        
        modal = VoiceChannelModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="📊 Estatísticas", style=discord.ButtonStyle.blurple, emoji="📊", row=1)
    async def stats_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Apenas o dono pode acessar!", ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        embed = discord.Embed(
            title="📊 ESTATÍSTICAS DO SISTEMA",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        # Estatísticas gerais
        total_members = sum(g.member_count for g in bot.guilds)
        total_channels = sum(len(g.channels) for g in bot.guilds)
        total_roles = sum(len(g.roles) for g in bot.guilds)
        
        embed.add_field(
            name="🌐 SERVIDORES",
            value=f"```Total: {len(bot.guilds)}\n"
                  f"Membros: {total_members}\n"
                  f"Canais: {total_channels}\n"
                  f"Cargos: {total_roles}```",
            inline=False
        )
        
        # Estatísticas de proteção
        embed.add_field(
            name="🛡️ PROTEÇÃO",
            value=f"```Whitelist: {len(whitelist_master.whitelist)} admins\n"
                  f"Backups: {'✅' if backup_master.carregar_backup() else '❌'}\n"
                  f"Voice: {'✅' if voice_permanente.voice_client else '❌'}\n"
                  f"Latência: {round(bot.latency * 1000, 2)}ms```",
            inline=False
        )
        
        # Uptime
        if hasattr(bot, 'start_time'):
            uptime = datetime.utcnow() - bot.start_time
            embed.add_field(
                name="⏰ UPTIME",
                value=f"```{uptime.days}d {uptime.seconds // 3600}h {(uptime.seconds % 3600) // 60}m```",
                inline=False
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="⚙️ Configurações", style=discord.ButtonStyle.gray, emoji="⚙️", row=1)
    async def config_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != OWNER_ID:
            await interaction.response.send_message("❌ Apenas o dono pode acessar!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="⚙️ CONFIGURAÇÕES AVANÇADAS",
            description="Configurações do sistema Cat Bot",
            color=discord.Color.dark_gray(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="🛠️ SISTEMA",
            value="```Versão: 3.0 Premium\n"
                  f"Owner: {OWNER_ID}\n"
                  f"Prefixo: #\n"
                  f"Modo: Profissional```",
            inline=False
        )
        
        embed.add_field(
            name="📁 ARQUIVOS",
            value="```whitelist_data.json\n"
                  "backup_completo.json\n"
                  "fingerprints.json\n"
                  "logs/ (pasta)```",
            inline=False
        )
        
        view = ConfigView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class WhitelistManagementView(View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label="➕ Adicionar", style=discord.ButtonStyle.green, row=0)
    async def add_button(self, interaction: discord.Interaction, button: Button):
        modal = WhitelistModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="➖ Remover", style=discord.ButtonStyle.red, row=0)
    async def remove_button(self, interaction: discord.Interaction, button: Button):
        modal = RemoveWhitelistModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="📋 Listar", style=discord.ButtonStyle.blurple, row=0)
    async def list_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        
        embed = discord.Embed(
            title="📋 LISTA COMPLETA DA WHITELIST",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        if whitelist_master.whitelist:
            for i, user_id in enumerate(whitelist_master.whitelist, 1):
                user = bot.get_user(user_id) or interaction.guild.get_member(user_id)
                status = "✅ ONLINE" if user and user.status != discord.Status.offline else "⚫ OFFLINE"
                created = user.created_at.strftime("%d/%m/%Y") if user else "Desconhecido"
                
                user_info = f"`{user_id}`"
                if user:
                    user_info = f"{user.mention}\n`{user_id}`"
                
                embed.add_field(
                    name=f"{i}. {user.name if user else f'ID: {user_id}'} {status}",
                    value=f"{user_info}\nCriado: {created}",
                    inline=False
                )
        else:
            embed.description = "Nenhum usuário na whitelist."
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🔙 Voltar", style=discord.ButtonStyle.gray, row=1)
    async def back_button(self, interaction: discord.Interaction, button: Button):
        embed = CatBotUI.create_main_panel()
        view = MainPanelView()
        await interaction.response.edit_message(embed=embed, view=view)

class BackupManagementView(View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label="💾 Criar Backup", style=discord.ButtonStyle.green, row=0)
    async def create_backup(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        
        try:
            backup_data = await backup_master.criar_backup_completo(interaction.guild)
            success = backup_master.salvar_backup(backup_data)
            
            if success:
                embed = discord.Embed(
                    title="✅ BACKUP CRIADO COM SUCESSO",
                    description=f"Backup completo do servidor salvo.\n"
                               f"**Itens salvos:**",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
                
                embed.add_field(name="Cargos", value=str(len(backup_data['roles'])), inline=True)
                embed.add_field(name="Categorias", value=str(len(backup_data['categories'])), inline=True)
                embed.add_field(name="Canais", value=str(len(backup_data['channels']['text']) + len(backup_data['channels']['voice'])), inline=True)
                embed.add_field(name="Emojis", value=str(len(backup_data.get('emoji', []))), inline=True)
                embed.add_field(name="Configurações", value="Todas", inline=True)
                embed.add_field(name="Whitelist", value=str(len(backup_data['whitelist'])), inline=True)
                
                embed.set_footer(text="Backup salvo em backup_completo.json")
                
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send("❌ Erro ao salvar backup!", ephemeral=True)
                
        except Exception as e:
            await interaction.followup.send(f"❌ Erro ao criar backup: {str(e)}", ephemeral=True)
            logger.log_system(f"Erro no backup: {traceback.format_exc()}", "ERROR")
    
    @discord.ui.button(label="🔄 Restaurar", style=discord.ButtonStyle.red, row=0)
    async def restore_backup(self, interaction: discord.Interaction, button: Button):
        backup_data = backup_master.carregar_backup()
        
        if not backup_data:
            await interaction.response.send_message("❌ Nenhum backup disponível para restaurar!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="⚠️ CONFIRMAÇÃO DE RESTAURAÇÃO",
            description="**ATENÇÃO:** Esta ação é IRREVERSÍVEL!\n\n"
                       "**O que será feito:**\n"
                       "1. ❌ Todos os cargos serão DELETADOS\n"
                       "2. ❌ Todos os canais serão DELETADOS\n"
                       "3. ❌ Todas as categorias serão DELETADAS\n"
                       "4. ✅ Tudo será recriado do backup\n\n"
                       f"**Backup:** {backup_data['metadata']['guild_name']}\n"
                       f"**Data:** {datetime.fromisoformat(backup_data['metadata']['backup_date']).strftime('%d/%m/%Y %H:%M')}\n\n"
                       "**Tem certeza absoluta?**",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        view = ConfirmRestoreView()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="📄 Info Backup", style=discord.ButtonStyle.blurple, row=0)
    async def info_backup(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        
        backup_data = backup_master.carregar_backup()
        
        if backup_data:
            metadata = backup_data['metadata']
            backup_date = datetime.fromisoformat(metadata['backup_date'])
            idade = datetime.utcnow() - backup_date
            
            embed = discord.Embed(
                title="📄 INFORMAÇÕES DO BACKUP",
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(
                name="📋 METADADOS",
                value=f"**Servidor:** {metadata['guild_name']}\n"
                      f"**ID:** {metadata['guild_id']}\n"
                      f"**Owner:** <@{metadata['owner_id']}>\n"
                      f"**Data:** {backup_date.strftime('%d/%m/%Y %H:%M:%S')}\n"
                      f"**Idade:** {idade.days} dias",
                inline=False
            )
            
            embed.add_field(
                name="📊 CONTEÚDO",
                value=f"```Cargos: {len(backup_data['roles'])}\n"
                      f"Categorias: {len(backup_data['categories'])}\n"
                      f"Canais Texto: {len(backup_data['channels'].get('text', []))}\n"
                      f"Canais Voz: {len(backup_data['channels'].get('voice', []))}\n"
                      f"Emojis: {len(backup_data.get('emoji', []))}```",
                inline=False
            )
            
            if 'whitelist' in backup_data:
                embed.add_field(
                    name="🛡️ WHITELIST",
                    value=f"`{len(backup_data['whitelist'])}` administradores",
                    inline=True
                )
            
            embed.set_footer(text=f"Versão: {metadata.get('backup_version', '1.0')}")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.followup.send("❌ Nenhum backup encontrado!", ephemeral=True)
    
    @discord.ui.button(label="🔙 Voltar", style=discord.ButtonStyle.gray, row=1)
    async def back_button(self, interaction: discord.Interaction, button: Button):
        embed = CatBotUI.create_main_panel()
        view = MainPanelView()
        await interaction.response.edit_message(embed=embed, view=view)

class ConfirmRestoreView(View):
    def __init__(self):
        super().__init__(timeout=60)
    
    @discord.ui.button(label="✅ SIM, RESTAURAR", style=discord.ButtonStyle.danger, row=0)
    async def confirm_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        
        backup_data = backup_master.carregar_backup()
        
        if not backup_data:
            await interaction.followup.send("❌ Backup não encontrado!", ephemeral=True)
            return
        
        # Enviar mensagem de processo
        embed = discord.Embed(
            title="🔄 RESTAURAÇÃO EM ANDAMENTO",
            description="**A restauração pode levar alguns minutos...**\n"
                       "Não desligue o bot durante este processo.\n\n"
                       f"Progresso: `[▰▱▱▱▱▱▱▱▱] 10%`",
            color=discord.Color.orange(),
            timestamp=datetime.utcnow()
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        
        # Iniciar restauração
        try:
            success = await backup_master.restaurar_backup_completo(interaction.guild, backup_data)
            
            if success:
                embed = discord.Embed(
                    title="✅ RESTAURAÇÃO CONCLUÍDA",
                    description=f"Servidor **{backup_data['metadata']['guild_name']}** restaurado com sucesso!\n\n"
                               "**O que foi restaurado:**\n"
                               f"• {len(backup_data['roles'])} cargos\n"
                               f"• {len(backup_data['categories'])} categorias\n"
                               f"• {len(backup_data['channels']['text']) + len(backup_data['channels']['voice'])} canais\n"
                               f"• {len(backup_data.get('emoji', []))} emojis\n"
                               f"• {len(backup_data['whitelist'])} administradores na whitelist\n\n"
                               "✅ **Sistema completo restaurado**",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
                
                await interaction.edit_original_response(embed=embed)
                
                # Reconectar ao voice
                if voice_permanente.voice_channel_id:
                    await asyncio.sleep(5)
                    await voice_permanente.conectar_voice(interaction.guild)
                    
            else:
                embed = discord.Embed(
                    title="❌ ERRO NA RESTAURAÇÃO",
                    description="Ocorreu um erro durante a restauração.\n"
                               "Verifique os logs para mais informações.\n\n"
                               "⚠️ **Backup de emergência foi criado:** `backup_emergencia.json`",
                    color=discord.Color.red(),
                    timestamp=datetime.utcnow()
                )
                
                await interaction.edit_original_response(embed=embed)
                
        except Exception as e:
            embed = discord.Embed(
                title="❌ ERRO CRÍTICO",
                description=f"Erro durante a restauração:\n```{str(e)[:500]}```\n\n"
                           "Verifique os logs para detalhes.",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            
            await interaction.edit_original_response(embed=embed)
            logger.log_system(f"Erro crítico na restauração: {traceback.format_exc()}", "ERROR")
    
    @discord.ui.button(label="❌ CANCELAR", style=discord.ButtonStyle.gray, row=0)
    async def cancel_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(
            content="✅ Restauração cancelada.",
            embed=None,
            view=None
        )

class SecurityManagementView(View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label="🔒 Lockdown", style=discord.ButtonStyle.red, row=0)
    async def lockdown_button(self, interaction: discord.Interaction, button: Button):
        if not anti_nuke.lockdown_mode:
            anti_nuke.lockdown_mode = True
            
            embed = discord.Embed(
                title="🔒 LOCKDOWN ATIVADO",
                description="**O servidor está agora em modo lockdown.**\n\n"
                           "**O que acontece:**\n"
                           "• Ninguém pode criar/editar/deletar cargos\n"
                           "• Ninguém pode criar/editar/deletar canais\n"
                           "• Ninguém pode banir/expulsar membros\n"
                           "• Nenhum convite pode ser criado\n"
                           "• Webhooks bloqueados\n"
                           "• Entrada de novos membros monitorada\n\n"
                           "Apenas a whitelist tem acesso total.",
                color=discord.Color.red(),
                timestamp=datetime.utcnow()
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            anti_nuke.lockdown_mode = False
            
            embed = discord.Embed(
                title="🔓 LOCKDOWN DESATIVADO",
                description="**Modo lockdown desativado.**\n"
                           "Operações normais restauradas.",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🛡️ Siege Mode", style=discord.ButtonStyle.red, row=0)
    async def siege_button(self, interaction: discord.Interaction, button: Button):
        if not anti_raid.siege_mode:
            anti_raid.siege_mode = True
            
            embed = discord.Embed(
                title="🛡️ SIEGE MODE ATIVADO",
                description="**Modo de cerco ativado.**\n\n"
                           "**Proteções extras:**\n"
                           "• Todas as entradas são bloqueadas\n"
                           "• Todos os convites revogados\n"
                           "• Canais fechados para não-membros\n"
                           "• Auto-ban para contas suspeitas\n"
                           "• Monitoramento total ativado\n\n"
                           "Este modo é para emergências graves.",
                color=discord.Color.dark_red(),
                timestamp=datetime.utcnow()
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            anti_raid.siege_mode = False
            
            embed = discord.Embed(
                title="🟢 SIEGE MODE DESATIVADO",
                description="**Modo de cerco desativado.**\n"
                           "Operações normais restauradas.",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="📜 Ver Logs", style=discord.ButtonStyle.blurple, row=0)
    async def logs_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        
        embed = discord.Embed(
            title="📜 SISTEMA DE LOGS",
            description="Logs disponíveis:",
            color=discord.Color.dark_gray(),
            timestamp=datetime.utcnow()
        )
        
        log_files = [
            ("🚨 Anti-Nuke", "nuke_protection.log"),
            ("⚔️ Anti-Raid", "raid_protection.log"),
            ("🛡️ Whitelist", "whitelist.log"),
            ("📦 Backup", "backup.log"),
            ("📝 Ações", "actions.log"),
            ("⚠️ Segurança", "security_warnings.log"),
            ("🔐 Permissões", "permission_changes.log"),
            ("💬 Mensagens", "message_logs.log")
        ]
        
        logs_info = []
        for name, filename in log_files:
            path = f"logs/{filename}"
            if os.path.exists(path):
                size = os.path.getsize(path)
                logs_info.append(f"✅ **{name}** - `{size/1024:.1f} KB`")
            else:
                logs_info.append(f"❌ **{name}** - `NÃO CRIADO`")
        
        embed.add_field(
            name="📁 ARQUIVOS DE LOG",
            value="\n".join(logs_info),
            inline=False
        )
        
        embed.add_field(
            name="📊 ESTATÍSTICAS",
            value=f"```Mensagens cacheadas: {len(logger.message_cache)}\n"
                  f"Mensagens deletadas: {len(logger.deleted_messages)}\n"
                  f"Edições monitoradas: {sum(len(v) for v in logger.edit_history.values())}```",
            inline=False
        )
        
        view = LogsView()
        await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="🔙 Voltar", style=discord.ButtonStyle.gray, row=1)
    async def back_button(self, interaction: discord.Interaction, button: Button):
        embed = CatBotUI.create_main_panel()
        view = MainPanelView()
        await interaction.response.edit_message(embed=embed, view=view)

class LogsView(View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label="📨 Mensagens", style=discord.ButtonStyle.blurple, row=0)
    async def messages_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        
        if not logger.message_cache:
            await interaction.followup.send("❌ Nenhuma mensagem no cache!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="📨 ÚLTIMAS MENSAGENS",
            description=f"Últimas {len(logger.message_cache)} mensagens monitoradas:",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        # Mostrar últimas 5 mensagens
        for i, msg in enumerate(list(logger.message_cache)[-5:], 1):
            embed.add_field(
                name=f"#{i} - {msg['channel']}",
                value=f"**{msg['author']}**: {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}\n"
                      f"`{msg['timestamp'][11:19]}`",
                inline=False
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🗑️ Deletadas", style=discord.ButtonStyle.red, row=0)
    async def deleted_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        
        if not logger.deleted_messages:
            await interaction.followup.send("❌ Nenhuma mensagem deletada registrada!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🗑️ MENSAGENS DELETADAS",
            description=f"Últimas {len(logger.deleted_messages)} mensagens deletadas:",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )
        
        # Mostrar últimas 5 deletadas
        for i, msg in enumerate(list(logger.deleted_messages)[-5:], 1):
            embed.add_field(
                name=f"#{i} - {msg['channel']}",
                value=f"**Autor:** {msg['author']}\n"
                      f"**Deletada por:** {msg['deleter']}\n"
                      f"**Conteúdo:** {msg['content'][:100]}{'...' if len(msg['content']) > 100 else ''}",
                inline=False
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)

class ConfigView(View):
    def __init__(self):
        super().__init__(timeout=300)
    
    @discord.ui.button(label="🔄 Recarregar", style=discord.ButtonStyle.green, row=0)
    async def reload_button(self, interaction: discord.Interaction, button: Button):
        # Recarregar whitelist
        whitelist_master.whitelist = whitelist_master.carregar_whitelist()
        
        embed = discord.Embed(
            title="🔄 CONFIGURAÇÕES RECARREGADAS",
            description="**Configurações recarregadas com sucesso:**\n\n"
                       f"• Whitelist: `{len(whitelist_master.whitelist)}` admins\n"
                       f"• Fingerprints: `{len(whitelist_master.fingerprints)}` usuários\n"
                       f"• Backup: `{'✅' if backup_master.carregar_backup() else '❌'}`",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🧹 Limpar Cache", style=discord.ButtonStyle.red, row=0)
    async def clear_button(self, interaction: discord.Interaction, button: Button):
        # Limpar caches
        anti_raid.join_timestamps.clear()
        anti_raid.suspicious_joins.clear()
        anti_nuke.cooldowns.clear()
        anti_nuke.suspicious_actions.clear()
        
        logger.message_cache.clear()
        logger.deleted_messages.clear()
        logger.edit_history.clear()
        
        embed = discord.Embed(
            title="🧹 CACHE LIMPO",
            description="**Todos os caches foram limpos:**\n\n"
                       "• Cache de mensagens\n"
                       "• Cache de entradas\n"
                       "• Cache de ações suspeitas\n"
                       "• Histórico de edições\n"
                       "• Mensagens deletadas",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @discord.ui.button(label="🔙 Voltar", style=discord.ButtonStyle.gray, row=1)
    async def back_button(self, interaction: discord.Interaction, button: Button):
        embed = CatBotUI.create_main_panel()
        view = MainPanelView()
        await interaction.response.edit_message(embed=embed, view=view)

# ==============================================
# SISTEMA DE LIMPEZA DE LOGS (a cada 100 mensagens)
# ==============================================

class LogCleaner:
    """Sistema de limpeza automática de logs"""
    
    def __init__(self):
        self.message_count = 0
        self.cleanup_threshold = 100
    
    async def check_and_clean(self):
        """Verifica e limpa logs antigos"""
        self.message_count += 1
        
        if self.message_count >= self.cleanup_threshold:
            await self.cleanup_old_logs()
            self.message_count = 0
    
    async def cleanup_old_logs(self):
        """Limpa logs antigos (mantém apenas últimos 1000 registros)"""
        try:
            # Para o cache de mensagens
            if len(logger.message_cache) > 1000:
                # Manter apenas últimos 1000
                while len(logger.message_cache) > 1000:
                    logger.message_cache.popleft()
            
            # Para mensagens deletadas
            if len(logger.deleted_messages) > 500:
                while len(logger.deleted_messages) > 500:
                    logger.deleted_messages.popleft()
            
            # Limpar arquivos de log muito grandes
            log_files = [
                'logs/message_logs.log',
                'logs/actions.log',
                'logs/permission_changes.log'
            ]
            
            for log_file in log_files:
                if os.path.exists(log_file):
                    size_mb = os.path.getsize(log_file) / (1024 * 1024)
                    
                    # Se maior que 50MB, truncar
                    if size_mb > 50:
                        with open(log_file, 'w') as f:
                            f.write(f"⚠️ Log truncado automaticamente em {datetime.utcnow()}\n")
                        
                        logger.log_system(f"Log truncado: {log_file} ({size_mb:.1f} MB)")
            
            logger.log_system("✅ Limpeza de logs concluída")
            
        except Exception as e:
            logger.log_system(f"❌ Erro ao limpar logs: {e}", "ERROR")

log_cleaner = LogCleaner()

# ==============================================
# EVENTOS DO BOT
# ==============================================

@bot.event
async def on_ready():
    """Evento quando o bot está pronto"""
    bot.start_time = datetime.utcnow()
    
    print(f"\n{'='*60}")
    print(f"🐱 CAT BOT v3.0 - SISTEMA PREMIUM")
    print(f"{'='*60}")
    print(f"✅ Conectado como: {bot.user.name} ({bot.user.id})")
    print(f"👑 Owner: {OWNER_ID}")
    print(f"🛡️ Whitelist: {len(whitelist_master.whitelist)} administradores")
    print(f"🌐 Servidores: {len(bot.guilds)}")
    print(f"📊 Total membros: {sum(g.member_count for g in bot.guilds)}")
    print(f"{'='*60}\n")
    
    logger.log_system(f"Bot iniciado: {bot.user.name} ({bot.user.id})")
    logger.log_system(f"Servidores: {len(bot.guilds)}")
    
    # Definir status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} servidores | #painel"
        ),
        status=discord.Status.online
    )
    
    # Conectar ao voice channel
    for guild in bot.guilds:
        if voice_permanente.voice_channel_id:
            await voice_permanente.conectar_voice(guild)
    
    # Iniciar tarefas periódicas
    if not verificar_conexao_voice.is_running():
        verificar_conexao_voice.start()
    
    if not limpar_logs_periodico.is_running():
        limpar_logs_periodico.start()

# ==============================================
# EVENTOS DE MONITORAMENTO
# ==============================================

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    """Monitora atualizações de membros"""
    await anti_nuke.monitorar_membro_update(before, after)
    
    # Log da ação
    if before.roles != after.roles:
        logger.log_action("MEMBER_ROLE_UPDATE", after, f"{len(after.roles)} cargos", "")

@bot.event
async def on_guild_channel_delete(channel: discord.abc.GuildChannel):
    """Monitora deleção de canais"""
    await anti_nuke.monitorar_delecao_canal(channel)
    logger.log_action("CHANNEL_DELETE", bot.user, channel.name, "Monitorado")

@bot.event
async def on_guild_channel_create(channel: discord.abc.GuildChannel):
    """Monitora criação de canais"""
    guild = channel.guild
    
    async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_create):
        if entry.target.id == channel.id:
            user = entry.user
            
            if not whitelist_master.is_whitelisted(user.id) and user != guild.owner and user != bot.user:
                # Se não autorizado criou canal, deletar
                try:
                    await channel.delete(reason="Canal criado por não autorizado")
                    await user.kick(reason="Criação de canal não autorizada")
                    logger.log_nuke(f"Canal deletado: criado por {user.name}", user)
                except:
                    pass
            
            break
    
    logger.log_action("CHANNEL_CREATE", channel.guild.me, channel.name, "")

@bot.event
async def on_guild_role_create(role: discord.Role):
    """Monitora criação de cargos"""
    await anti_nuke.monitorar_criacao_cargo(role)
    logger.log_action("ROLE_CREATE", role.guild.me, role.name, "")

@bot.event
async def on_guild_role_delete(role: discord.Role):
    """Monitora deleção de cargos"""
    await anti_nuke.monitorar_delecao_cargo(role)
    logger.log_action("ROLE_DELETE", role.guild.me, role.name, "")

@bot.event
async def on_guild_role_update(before: discord.Role, after: discord.Role):
    """Monitora atualização de cargos"""
    await anti_nuke.monitorar_alteracao_cargo(before, after)
    
    if before.position != after.position:
        await anti_nuke.monitorar_movimento_cargo(after, before.position, after.position)
    
    logger.log_action("ROLE_UPDATE", after.guild.me, after.name, "")

@bot.event
async def on_member_ban(guild: discord.Guild, user: discord.User):
    """Monitora banimentos"""
    await anti_nuke.monitorar_ban(guild, user)
    logger.log_action("MEMBER_BAN", guild.me, user.name, "")

@bot.event
async def on_member_remove(member: discord.Member):
    """Monitora remoção de membros (kick)"""
    await anti_nuke.monitorar_kick(member)
    logger.log_action("MEMBER_KICK", member.guild.me, member.name, "")

@bot.event
async def on_invite_create(invite: discord.Invite):
    """Monitora criação de convites"""
    await anti_nuke.monitorar_criacao_invite(invite)
    logger.log_action("INVITE_CREATE", invite.guild.me, invite.code, "")

@bot.event
async def on_webhooks_update(channel: discord.TextChannel):
    """Monitora atualização de webhooks"""
    try:
        webhooks = await channel.webhooks()
        for webhook in webhooks:
            # Verificar se é novo
            await anti_nuke.monitorar_criacao_webhook(webhook)
    except:
        pass
    
    logger.log_action("WEBHOOKS_UPDATE", channel.guild.me, channel.name, "")

@bot.event
async def on_member_join(member: discord.Member):
    """Monitora entrada de membros"""
    await anti_raid.monitorar_entrada(member)
    logger.log_action("MEMBER_JOIN", member.guild.me, member.name, "")

@bot.event
async def on_message(message: discord.Message):
    """Monitora todas as mensagens"""
    if message.author.bot:
        return
    
    # Log da mensagem
    logger.log_message(message)
    
    # Verificar spam
    await anti_raid.monitorar_spam(message)
    
    # Verificar limpeza de logs
    await log_cleaner.check_and_clean()
    
    # Processar comandos
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message: discord.Message):
    """Monitora mensagens deletadas"""
    if message.author.bot:
        return
    
    # Tentar identificar quem deletou
    deleter = None
    try:
        async for entry in message.guild.audit_logs(limit=5, action=discord.AuditLogAction.message_delete):
            if entry.target.id == message.author.id:
                deleter = entry.user
                break
    except:
        pass
    
    logger.log_deleted_message(message, deleter)

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    """Monitora edição de mensagens"""
    if before.author.bot or before.content == after.content:
        return
    
    # Adicionar ao histórico de edições
    if before.author.id not in logger.edit_history:
        logger.edit_history[before.author.id] = []
    
    logger.edit_history[before.author.id].append({
        'before': before.content,
        'after': after.content,
        'timestamp': datetime.utcnow().isoformat(),
        'channel': before.channel.name
    })
    
    # Manter apenas últimas 10 edições por usuário
    if len(logger.edit_history[before.author.id]) > 10:
        logger.edit_history[before.author.id] = logger.edit_history[before.author.id][-10:]
    
    logger.log_system(f"Mensagem editada por {before.author.name} em #{before.channel.name}")

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    """Monitora atualizações de voice"""
    await voice_permanente.mover_intruso(member, before, after)
    
    # Log de entrada/saída do voice
    if not before.channel and after.channel:
        logger.log_action("VOICE_JOIN", member, after.channel.name, "")
    elif before.channel and not after.channel:
        logger.log_action("VOICE_LEAVE", member, before.channel.name, "")

# ==============================================
# TAREFAS PERIÓDICAS
# ==============================================

@tasks.loop(minutes=1)
async def verificar_conexao_voice():
    """Verifica e reconecta ao voice channel periodicamente"""
    for guild in bot.guilds:
        if voice_permanente.voice_channel_id:
            # Verificar se canal ainda existe
            channel = guild.get_channel(voice_permanente.voice_channel_id)
            
            if not channel:
                # Recriar canal
                await voice_permanente.recriar_canal(guild)
            elif not voice_permanente.voice_client or not voice_permanente.voice_client.is_connected():
                # Reconectar
                await voice_permanente.conectar_voice(guild)

@tasks.loop(hours=1)
async def limpar_logs_periodico():
    """Limpeza periódica de logs"""
    await log_cleaner.cleanup_old_logs()

# ==============================================
# COMANDOS DO BOT
# ==============================================

@bot.command(name='painel')
async def comando_painel(ctx: commands.Context):
    """Comando principal do painel"""
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Apenas o dono pode usar este comando!")
        return
    
    embed = CatBotUI.create_main_panel()
    view = MainPanelView()
    
    await ctx.send(embed=embed, view=view)

@bot.command(name='backup')
async def comando_backup(ctx: commands.Context):
    """Cria backup rápido"""
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Apenas o dono pode fazer backup!")
        return
    
    await ctx.send("🔄 Criando backup...")
    
    try:
        backup_data = await backup_master.criar_backup_completo(ctx.guild)
        success = backup_master.salvar_backup(backup_data)
        
        if success:
            embed = discord.Embed(
                title="✅ BACKUP CRIADO",
                description=f"Backup do servidor **{ctx.guild.name}** criado com sucesso!",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name="Cargos", value=str(len(backup_data['roles'])), inline=True)
            embed.add_field(name="Canais", value=str(len(backup_data['channels']['text']) + len(backup_data['channels']['voice'])), inline=True)
            embed.add_field(name="Categorias", value=str(len(backup_data['categories'])), inline=True)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Erro ao salvar backup!")
            
    except Exception as e:
        await ctx.send(f"❌ Erro ao criar backup: {str(e)[:100]}")

@bot.command(name='whitelist')
async def comando_whitelist(ctx: commands.Context):
    """Mostra a whitelist"""
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Apenas o dono pode ver a whitelist!")
        return
    
    embed = CatBotUI.create_whitelist_panel()
    view = WhitelistManagementView()
    
    await ctx.send(embed=embed, view=view)

@bot.command(name='logs')
async def comando_logs(ctx: commands.Context):
    """Mostra informações dos logs"""
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Apenas o dono pode ver os logs!")
        return
    
    embed = discord.Embed(
        title="📜 SISTEMA DE LOGS",
        color=discord.Color.dark_gray(),
        timestamp=datetime.utcnow()
    )
    
    embed.add_field(
        name="📊 ESTATÍSTICAS",
        value=f"```Mensagens cacheadas: {len(logger.message_cache)}\n"
              f"Mensagens deletadas: {len(logger.deleted_messages)}\n"
              f"Edições monitoradas: {sum(len(v) for v in logger.edit_history.values())}```",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='status')
async def comando_status(ctx: commands.Context):
    """Mostra status completo do sistema"""
    if ctx.author.id != OWNER_ID:
        await ctx.send("❌ Apenas o dono pode ver o status!")
        return
    
    embed = discord.Embed(
        title="📊 STATUS DO SISTEMA CAT BOT",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    # Informações gerais
    uptime = datetime.utcnow() - bot.start_time
    latency = round(bot.latency * 1000, 2)
    
    embed.add_field(
        name="🌐 GERAL",
        value=f"```Uptime: {uptime.days}d {uptime.seconds // 3600}h\n"
              f"Servidores: {len(bot.guilds)}\n"
              f"Latência: {latency}ms\n"
              f"Versão: 3.0 Premium```",
        inline=False
    )
    
    # Proteções
    embed.add_field(
        name="🛡️ PROTEÇÕES",
        value=f"```Anti-Nuke: {'✅ ATIVO' if not anti_nuke.lockdown_mode else '🚨 LOCKDOWN'}\n"
              f"Anti-Raid: {'✅ ATIVO' if not anti_raid.raid_mode else '🚨 RAID MODE'}\n"
              f"Whitelist: {len(whitelist_master.whitelist)} admins\n"
              f"Voice: {'✅ CONECTADO' if voice_permanente.voice_client else '❌ DESCONECTADO'}```",
        inline=False
    )
    
    # Estatísticas
    embed.add_field(
        name="📈 ESTATÍSTICAS",
        value=f"```Tentativas bloqueadas: {len(anti_nuke.suspicious_actions)}\n"
              f"Contas suspeitas: {sum(len(v) for v in anti_raid.suspicious_joins.values())}\n"
              f"Restaurações: {len(anti_nuke.auto_restore_queue)}```",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='ajuda')
async def comando_ajuda(ctx: commands.Context):
    """Mostra ajuda"""
    embed = discord.Embed(
        title="🐱 CAT BOT - COMANDOS",
        description="Sistema de segurança completo\n"
                   "─────────────────────────────",
        color=discord.Color.blue()
    )
    
    commands_list = [
        ("#painel", "Abre o painel de controle principal"),
        ("#backup", "Cria um backup rápido do servidor"),
        ("#whitelist", "Mostra e gerencia a whitelist"),
        ("#logs", "Mostra estatísticas dos logs"),
        ("#status", "Mostra status completo do sistema"),
        ("#ajuda", "Mostra esta mensagem")
    ]
    
    for cmd, desc in commands_list:
        embed.add_field(name=cmd, value=desc, inline=False)
    
    embed.set_footer(text="Apenas o dono pode usar estes comandos")
    
    await ctx.send(embed=embed)

# ==============================================
# FUNÇÃO PRINCIPAL
# ==============================================

async def main():
    """Função principal"""
    try:
        print("🚀 Iniciando Cat Bot v3.0...")
        logger.log_system("Iniciando sistema Cat Bot v3.0")
        
        await bot.start(TOKEN)
    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado pelo usuário")
        logger.log_system("Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        logger.log_system(f"Erro crítico: {traceback.format_exc()}", "ERROR")
    finally:
        if not bot.is_closed():
            await bot.close()

# ==============================================
# EXECUÇÃO
# ==============================================

if __name__ == "__main__":
    # Criar diretório de logs se não existir
    os.makedirs("logs", exist_ok=True)
    
    # Executar bot
    asyncio.run(main())
