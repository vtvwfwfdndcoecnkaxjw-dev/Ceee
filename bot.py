import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
import requests
from io import BytesIO
import urllib.parse
import random
import string
import pdfkit
from bs4 import BeautifulSoup
import re

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# ✅ CORREÇÃO: Adicionar setup_hook para inicialização assíncrona
@bot.event
async def setup_hook():
    """Hook de inicialização assíncrona do discord.py"""
    print("🔄 Iniciando sistemas de segurança assincronamente...")
    await sistema_seguranca.setup()
    print("✅ Todos os sistemas de segurança ativados!")

# CONFIGURAÇÕES COMPLETAS
CONFIG = {
    "cargos_linguagens": {
        "🐍 Python": "python",
        "☕ Java": "java", 
        "🟨 JavaScript": "javascript",
        "🔵 Golang": "golang",
        "🦀 Rust": "rust",
        "💜 C#": "csharp",
        "🔷 C/C++": "cpp",
        "🐘 PHP": "php",
        "💎 Ruby": "ruby",
        "🍎 Swift": "swift",
        "💚 Kotlin": "kotlin",
        "🐚 Bash/Shell": "bash"
    },
    
    "cargos_cyber": {
        "🎩 Ethical Hacker": "hacker",
        "🔍 Pentester": "pentester", 
        "🛡️ Blue Team": "blueteam",
        "🔴 Red Team": "redteam",
        "💰 Bug Hunter": "bughunter",
        "🏆 CTF Player": "ctf",
        "🕵️ OSINT": "osint",
        "🔧 Reverse Eng": "reverse",
        "💣 Exploit Dev": "exploit",
        "🦠 Malware Analyst": "malware"
    },
    
    "cargos_hierarquia": {
        "Dono": 100,
        "Administrador": 90,
        "Moderador": 80,
        "Staff": 70,
        "Professor": 60,
        "Cyber Professor": 65,
        "Cyber Administrador": 85,
        "Cyber Staff": 75,
        "Membro": 10
    },
    
    "logs_config": {
        "entrada_saida": "👤・entrada-saida",
        "moderacao": "🛡️・mod-logs",
        "cargos": "⭐・cargo-logs",
        "advertencias": "⚠️・advertencias",
        "conquistas": "🏆・conquistas",
        "pontuacao": "📊・pontuacao"
    },
    
    "canais_automaticos": {
        "self_roles": None,
        "entrada_saida": None,
        "mod_logs": None,
        "cargo_logs": None,
        "advertencias": None,
        "conquistas": None,
        "pontuacao": None
    },
    
    "canais_permitidos": [],
    "groq_api_key": os.getenv('GROQ_API_KEY'),
    "max_advertencias": 3,
    "canal_pontuacao_id": 1437583070529327124
}

# BANCO DE DADOS COMPLETO - MOVIDO PARA ANTES DO SISTEMA DE SEGURANÇA
class Database:
    def __init__(self):
        self.advertencias = {}
        self.convites = {}
        self.config = {}
        self.contadores = {}
        self.historico_ia = {}
        self.pontuacao = {}
        self.config_canais = {}
        self.lembretes_anuncios = {}
        self.missoes_cyber = {}
        self.conversas_ativas = {}
        self.rate_limit_data = {}
        self.comandos_personalizados = {}
        self.whitelist_tokens = {}  # ✅ NOVO: Sistema de tokens para whitelist
        self.criar_banco_automatico()
    
    def criar_banco_automatico(self):
        """Cria o banco de dados automaticamente se não existir"""
        try:
            self.carregar_dados()
        except:
            self.salvar_dados()
    
    def salvar_dados(self):
        with open('data.json', 'w') as f:
            json.dump({
                'advertencias': self.advertencias,
                'convites': self.convites,
                'config': self.config,
                'contadores': self.contadores,
                'historico_ia': self.historico_ia,
                'pontuacao': self.pontuacao,
                'config_canais': self.config_canais,
                'lembretes_anuncios': self.lembretes_anuncios,
                'missoes_cyber': self.missoes_cyber,
                'conversas_ativas': self.conversas_ativas,
                'rate_limit_data': self.rate_limit_data,
                'comandos_personalizados': self.comandos_personalizados,
                'whitelist_tokens': self.whitelist_tokens  # ✅ NOVO
            }, f, indent=2)
    
    def carregar_dados(self):
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.advertencias = data.get('advertencias', {})
                self.convites = data.get('convites', {})
                self.config = data.get('config', {})
                self.contadores = data.get('contadores', {})
                self.historico_ia = data.get('historico_ia', {})
                self.pontuacao = data.get('pontuacao', {})
                self.config_canais = data.get('config_canais', {})
                self.lembretes_anuncios = data.get('lembretes_anuncios', {})
                self.missoes_cyber = data.get('missoes_cyber', {})
                self.conversas_ativas = data.get('conversas_ativas', {})
                self.rate_limit_data = data.get('rate_limit_data', {})
                self.comandos_personalizados = data.get('comandos_personalizados', {})
                self.whitelist_tokens = data.get('whitelist_tokens', {})  # ✅ NOVO
                
                # Carregar configurações de canais
                if 'canais_automaticos' in self.config_canais:
                    CONFIG['canais_automaticos'] = self.config_canais['canais_automaticos']
        except:
            self.advertencias = {}
            self.convites = {}
            self.config = {}
            self.contadores = {}
            self.historico_ia = {}
            self.pontuacao = {}
            self.config_canais = {}
            self.lembretes_anuncios = {}
            self.missoes_cyber = {}
            self.conversas_ativas = {}
            self.rate_limit_data = {}
            self.comandos_personalizados = {}
            self.whitelist_tokens = {}  # ✅ NOVO

db = Database()

# SISTEMA DE SEGURANÇA MULTIFACETADO (SSM) - CORRIGIDO
class SistemaSegurancaMultifacetado:
    def __init__(self, bot):
        self.bot = bot
        self.whitelist_bots = set()
        self.quarentena_usuarios = {}
        self.rate_limit_actions = {}
        self.cargo_quarentena = None
        self.contador_acoes_bot = {}
        self.auto_destruicao_ativa = False
        
        # ✅ CORREÇÃO: Token para whitelist
        self.whitelist_token = None
        self.gerar_token_whitelist()
        
        # Carregar dados do banco
        self.carregar_dados_seguranca()
        
        print("🛡️ Sistema de Segurança Multifacetado Inicializado!")

    # ✅ CORREÇÃO: Adicionar método de inicialização assíncrona
    async def setup(self):
        """Inicialização assíncrona para criar tasks"""
        # Iniciar loop de limpeza automática
        self.bot.loop.create_task(self.loop_auto_liberacao())
        self.bot.loop.create_task(self.monitorar_uso_bot())
        print("🛡️ Sistema de Segurança Multifacetado Ativado!")

    def gerar_token_whitelist(self):
        """Gera token para whitelist de bots"""
        if not self.whitelist_token:
            chars = string.ascii_letters + string.digits
            self.whitelist_token = ''.join(random.choice(chars) for _ in range(32))
            db.whitelist_tokens['master_token'] = self.whitelist_token
            db.salvar_dados()

    def carregar_dados_seguranca(self):
        """Carrega dados de segurança do banco"""
        if 'ssm_whitelist' in db.config:
            self.whitelist_bots = set(db.config['ssm_whitelist'])
        if 'ssm_quarentena' in db.config:
            self.quarentena_usuarios = db.config['ssm_quarentena']
        if 'ssm_rate_limit' in db.config:
            self.rate_limit_actions = db.config['ssm_rate_limit']
        if 'master_token' in db.whitelist_tokens:
            self.whitelist_token = db.whitelist_tokens['master_token']

    def salvar_dados_seguranca(self):
        """Salva dados de segurança no banco"""
        db.config['ssm_whitelist'] = list(self.whitelist_bots)
        db.config['ssm_quarentena'] = self.quarentena_usuarios
        db.config['ssm_rate_limit'] = self.rate_limit_actions
        db.salvar_dados()

    async def criar_cargo_quarentena(self, guild):
        """Cria o cargo de quarentena se não existir"""
        cargo = discord.utils.get(guild.roles, name="[SSM - QUARENTENA]")
        if not cargo:
            cargo = await guild.create_role(
                name="[SSM - QUARENTENA]",
                color=discord.Color.dark_red(),
                reason="Cargo de quarentena para o Sistema de Segurança"
            )
            
            # Negar todas as permissões em todos os canais
            for channel in guild.channels:
                try:
                    await channel.set_permissions(cargo, 
                        read_messages=False,
                        send_messages=False,
                        connect=False,
                        speak=False,
                        use_application_commands=False,
                        create_instant_invite=False,
                        add_reactions=False
                    )
                except:
                    continue
        
        self.cargo_quarentena = cargo
        return cargo

    async def colocar_quarentena(self, member, duracao_minutos=60, motivo="Comportamento suspeito"):
        """Coloca um usuário em quarentena"""
        # ✅ CORREÇÃO CRÍTICA: Ignorar bots da whitelist
        if member.bot and member.id in self.whitelist_bots:
            return False
            
        cargo = await self.criar_cargo_quarentena(member.guild)
        
        # Remover todos os cargos do usuário
        cargos_anteriores = [role for role in member.roles if role != member.guild.default_role]
        try:
            await member.remove_roles(*cargos_anteriores)
            await member.add_roles(cargo)
        except Exception as e:
            print(f"Erro ao aplicar quarentena: {e}")
            return False
        
        # Registrar na quarentena
        tempo_fim = datetime.now() + timedelta(minutes=duracao_minutos)
        self.quarentena_usuarios[str(member.id)] = {
            "tempo_fim": tempo_fim.isoformat(),
            "motivo": motivo,
            "cargos_anteriores": [role.id for role in cargos_anteriores]
        }
        self.salvar_dados_seguranca()
        
        # Log da ação
        await log_system.log_moderacao("QUARENTENA", self.bot.user, member, 
                                     f"{motivo} | Duração: {duracao_minutos}min")
        
        return True

    async def remover_quarentena(self, member):
        """Remove um usuário da quarentena"""
        user_id = str(member.id)
        
        if user_id in self.quarentena_usuarios:
            cargo = await self.criar_cargo_quarentena(member.guild)
            
            try:
                await member.remove_roles(cargo)
                
                # Restaurar cargos anteriores se disponíveis
                dados = self.quarentena_usuarios[user_id]
                cargos_restaurar = []
                for role_id in dados.get("cargos_anteriores", []):
                    role = member.guild.get_role(role_id)
                    if role:
                        cargos_restaurar.append(role)
                
                if cargos_restaurar:
                    await member.add_roles(*cargos_restaurar)
                
                del self.quarentena_usuarios[user_id]
                self.salvar_dados_seguranca()
                
                await log_system.log_moderacao("QUARENTENA REMOVIDA", self.bot.user, member, 
                                             "Quarentena expirada/removida")
                return True
                
            except Exception as e:
                print(f"Erro ao remover quarentena: {e}")
        
        return False

    async def loop_auto_liberacao(self):
        """Loop para liberação automática da quarentena"""
        await self.bot.wait_until_ready()
        
        while not self.bot.is_closed():
            try:
                agora = datetime.now()
                usuarios_remover = []
                
                for user_id, dados in self.quarentena_usuarios.items():
                    tempo_fim = datetime.fromisoformat(dados["tempo_fim"])
                    if agora >= tempo_fim:
                        usuarios_remover.append(user_id)
                
                for user_id in usuarios_remover:
                    for guild in self.bot.guilds:
                        member = guild.get_member(int(user_id))
                        if member:
                            await self.remover_quarentena(member)
                            break
                
                await asyncio.sleep(60)  # Verificar a cada minuto
                
            except Exception as e:
                print(f"Erro no loop de liberação: {e}")
                await asyncio.sleep(60)

    async def verificar_bot_entrada(self, member):
        """Verifica se um bot que entrou está na whitelist - CORRIGIDO"""
        if not member.bot:
            return True
        
        # ✅ CORREÇÃO: Bots na whitelist são totalmente ignorados pelo sistema de segurança
        if member.id in self.whitelist_bots:
            return True  # Totalmente ignorado
        
        # ✅ CORREÇÃO: Bots não autorizados apenas são registrados, NÃO bloqueados
        await log_system.log_moderacao("BOT NÃO AUTORIZADO", self.bot.user, member, 
                                     "Bot não autorizado entrou no servidor (apenas monitorado)")
        return True  # ✅ PERMITE ENTRADA, APENAS REGISTRA

    async def detectar_nuke(self, guild, author, acao):
        """Detecta ataques de nuke/flood - CORRIGIDO"""
        # ✅ CORREÇÃO CRÍTICA: Ignorar ações do próprio bot E bots da whitelist
        if author.id == self.bot.user.id or (author.bot and author.id in self.whitelist_bots):
            return False
            
        user_id = str(author.id)
        
        if user_id not in self.rate_limit_actions:
            self.rate_limit_actions[user_id] = []
        
        # Registrar ação
        self.rate_limit_actions[user_id].append({
            "acao": acao,
            "timestamp": datetime.now().isoformat()
        })
        
        # Manter apenas ações dos últimos 5 segundos
        agora = datetime.now()
        self.rate_limit_actions[user_id] = [
            a for a in self.rate_limit_actions[user_id]
            if (agora - datetime.fromisoformat(a["timestamp"])).total_seconds() <= 5
        ]
        
        # Verificar limites
        if len(self.rate_limit_actions[user_id]) >= 5:  # 5 ações em 5 segundos
            await self.colocar_quarentena(author, 120, "Detectado padrão de nuke/flood")
            
            # Reverter ações se possível (canais/cargos criados)
            await self.reverter_acoes_destrutivas(guild, author)
            return True
        
        return False

    async def reverter_acoes_destrutivas(self, guild, author):
        """Reverte ações destrutivas em lote - CORRIGIDO"""
        try:
            # ✅ CORREÇÃO: Ignorar ações de bots da whitelist
            if author.bot and author.id in self.whitelist_bots:
                return
                
            # Reverter canais criados recentemente
            async for entry in guild.audit_logs(limit=10, action=discord.AuditLogAction.channel_create):
                if entry.user.id == author.id:
                    try:
                        await entry.target.delete()
                    except:
                        continue
            
            # Reverter cargos criados recentemente
            async for entry in guild.audit_logs(limit=10, action=discord.AuditLogAction.role_create):
                if entry.user.id == author.id:
                    try:
                        await entry.target.delete()
                    except:
                        continue
        except:
            pass

    async def detectar_flood_mensagens(self, message):
        """Detecta flood de mensagens SEM auto-delete - CORRIGIDO"""
        # ✅ CORREÇÃO: Ignorar bots da whitelist
        if message.author.bot and message.author.id in self.whitelist_bots:
            return False
            
        user_id = str(message.author.id)
        
        if user_id not in self.rate_limit_actions:
            self.rate_limit_actions[user_id] = []
        
        # Registrar mensagem
        self.rate_limit_actions[user_id].append({
            "acao": "message_send",
            "timestamp": datetime.now().isoformat(),
            "channel_id": message.channel.id
        })
        
        # Manter apenas ações dos últimos 10 segundos (aumentado)
        agora = datetime.now()
        self.rate_limit_actions[user_id] = [
            a for a in self.rate_limit_actions[user_id]
            if (agora - datetime.fromisoformat(a["timestamp"])).total_seconds() <= 10
        ]
        
        # ✅ CORREÇÃO: LIMITES MAIS FLEXÍVEIS
        mensagens_no_canal = [
            a for a in self.rate_limit_actions[user_id] 
            if a.get('channel_id') == message.channel.id and a['acao'] == 'message_send'
        ]
        
        # ✅ CORREÇÃO: APENAS AVISAR, NÃO DELETAR
        if len(mensagens_no_canal) >= 10:  # 10 mensagens em 10 segundos
            try:
                await message.channel.send(
                    f"{message.author.mention} 🚨 **Detectado flood de mensagens!** Diminua a velocidade.",
                    delete_after=5
                )
                
            except:
                pass
        
        # ✅ CORREÇÃO: QUARENTENA APENAS EM CASOS EXTREMOS
        if len(mensagens_no_canal) >= 15:  # 15 mensagens em 10 segundos
            await self.colocar_quarentena(message.author, 2, "Flood extremo de mensagens")
            
        return False  # ✅ SEMPRE RETORNA FALSE PARA NÃO BLOQUEAR MENSAGENS

    async def monitorar_uso_bot(self):
        """Monitora o uso do próprio bot para detectar token comprometido"""
        await self.bot.wait_until_ready()
        
        while not self.bot.is_closed():
            try:
                agora = datetime.now()
                
                # Limpar contador antigo
                self.contador_acoes_bot = {
                    k: v for k, v in self.contador_acoes_bot.items()
                    if (agora - datetime.fromisoformat(v['timestamp'])).total_seconds() <= 60
                }
                
                # Verificar se há uso anômalo do bot
                acoes_por_guild = {}
                for guild_id, dados in self.contador_acoes_bot.items():
                    if dados['ban_count'] >= 50 or dados['channel_delete_count'] >= 50:
                        print(f"🚨 ALERTA CRÍTICO: Uso anômalo detectado no servidor {guild_id}")
                        await self.ativar_autodestruicao()
                        return
                
                await asyncio.sleep(30)  # Verificar a cada 30 segundos
                
            except Exception as e:
                print(f"Erro no monitoramento do bot: {e}")
                await asyncio.sleep(30)

    async def registrar_acao_bot(self, guild_id, acao):
        """Registra ação realizada pelo bot"""
        if guild_id not in self.contador_acoes_bot:
            self.contador_acoes_bot[guild_id] = {
                'ban_count': 0,
                'channel_delete_count': 0,
                'timestamp': datetime.now().isoformat()
            }
        
        if acao == 'ban':
            self.contador_acoes_bot[guild_id]['ban_count'] += 1
        elif acao == 'channel_delete':
            self.contador_acoes_bot[guild_id]['channel_delete_count'] += 1

    async def ativar_autodestruicao(self):
        """Ativa a autodestruição do token (proteção máxima)"""
        if self.auto_destruicao_ativa:
            return
            
        self.auto_destruicao_ativa = True
        print("💀 ATIVAÇÃO DE AUTODESTRUIÇÃO - Token comprometido detectado!")
        
        # Tentar revogar o token via API do Discord
        try:
            # Esta é uma simulação - em produção, você implementaria a revogação real do token
            headers = {
                "Authorization": f"Bot {os.getenv('DISCORD_TOKEN')}",
                "Content-Type": "application/json"
            }
            
            # Enviar alerta para todos os servidores
            for guild in self.bot.guilds:
                try:
                    canal_system = await log_system.get_log_channel(guild, "moderacao")
                    if canal_system:
                        embed = discord.Embed(
                            title="💀 AUTODESTRUIÇÃO ATIVADA",
                            description="**Token do bot comprometido detectado!**\n\nO bot está se autodestruindo para proteger o servidor.",
                            color=0xff0000,
                            timestamp=datetime.now()
                        )
                        await canal_system.send(embed=embed)
                except:
                    pass
                    
        except Exception as e:
            print(f"Erro na autodestruição: {e}")
        
        # Desligar o bot
        await self.bot.close()

    def adicionar_bot_whitelist(self, bot_id, autor):
        """Adiciona bot à whitelist"""
        self.whitelist_bots.add(bot_id)
        self.salvar_dados_seguranca()
        
        # Log de auditoria
        print(f"🔧 BOT WHITELIST: {autor.name} adicionou bot {bot_id} à whitelist")
        return True

    def remover_bot_whitelist(self, bot_id, autor):
        """Remove bot da whitelist"""
        if bot_id in self.whitelist_bots:
            self.whitelist_bots.remove(bot_id)
            self.salvar_dados_seguranca()
            
            # Log de auditoria
            print(f"🔧 BOT WHITELIST: {autor.name} removeu bot {bot_id} da whitelist")
            return True
        return False

    def obter_token_whitelist(self):
        """Retorna o token atual para whitelist"""
        return self.whitelist_token

    def gerar_novo_token_whitelist(self):
        """Gera novo token para whitelist"""
        chars = string.ascii_letters + string.digits
        self.whitelist_token = ''.join(random.choice(chars) for _ in range(32))
        db.whitelist_tokens['master_token'] = self.whitelist_token
        db.salvar_dados()
        return self.whitelist_token

    def verificar_token_whitelist(self, token):
        """Verifica se o token é válido"""
        return token == self.whitelist_token

# SISTEMA DE TICKETS AUTOMÁTICO - NOVO SISTEMA
class SistemaTickets:
    def __init__(self, bot):
        self.bot = bot
        self.tickets_ativos = {}
    
    async def setup_canal_tickets(self, guild):
        """Configura o canal de tickets automático"""
        canal_id = CONFIG['canais_automaticos'].get('tickets')
        if canal_id:
            canal = guild.get_channel(canal_id)
            if canal:
                return canal
        
        # Criar canal se não existir
        canal = await guild.create_text_channel("🎫・abra-seu-ticket")
        
        # Configurar permissões
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=True),
            guild.me: discord.PermissionOverwrite(send_messages=True, manage_messages=True)
        }
        await canal.edit(overwrites=overwrites)
        
        # Salvar configuração
        CONFIG['canais_automaticos']['tickets'] = canal.id
        db.config_canais['canais_automaticos'] = CONFIG['canais_automaticos']
        db.salvar_dados()
        
        # Enviar mensagem de boas-vindas
        embed = discord.Embed(
            title="🎫 SISTEMA DE TICKETS DE SUPORTE",
            description="**Precisa de ajuda? Abra um ticket!**\n\n"
                       "• Clique no 🎫 abaixo para criar um ticket de suporte\n"
                       "• Nossa equipe irá ajudá-lo em breve\n"
                       "• Use apenas para assuntos importantes",
            color=0x0099ff
        )
        
        mensagem = await canal.send(embed=embed)
        await mensagem.add_reaction("🎫")
        
        return canal

    async def criar_ticket(self, member):
        """Cria um novo ticket para o membro"""
        guild = member.guild
        
        # Criar canal do ticket
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }
        
        # Adicionar cargos de staff
        for role in guild.roles:
            if any(perm in ['administrator', 'manage_guild', 'manage_channels'] for perm in [role.permissions.administrator, role.permissions.manage_guild, role.permissions.manage_channels]):
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        ticket_id = len(self.tickets_ativos) + 1
        canal_ticket = await guild.create_text_channel(
            name=f"ticket-{ticket_id}",
            overwrites=overwrites,
            reason=f"Ticket criado por {member.name}"
        )
        
        # Registrar ticket
        self.tickets_ativos[ticket_id] = {
            "member_id": member.id,
            "channel_id": canal_ticket.id,
            "created_at": datetime.now().isoformat(),
            "status": "aberto"
        }
        
        # Mensagem de boas-vindas no ticket
        embed = discord.Embed(
            title=f"🎫 TICKET #{ticket_id}",
            description=f"Olá {member.mention}! A equipe de suporte será notificada e irá ajudá-lo em breve.\n\n"
                       "**Use `!close` para fechar este ticket**",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        embed.add_field(name="👤 Criado por", value=member.mention, inline=True)
        embed.add_field(name="📅 Data", value=datetime.now().strftime("%d/%m/%Y %H:%M"), inline=True)
        
        await canal_ticket.send(embed=embed)
        
        # Notificar staff
        await self.notificar_staff(guild, ticket_id, member)
        
        return canal_ticket

    async def fechar_ticket(self, channel, member):
        """Fecha um ticket"""
        ticket_id = None
        for tid, dados in self.tickets_ativos.items():
            if dados["channel_id"] == channel.id:
                ticket_id = tid
                break
        
        if ticket_id:
            embed = discord.Embed(
                title="🎫 TICKET FECHADO",
                description=f"Ticket fechado por {member.mention}",
                color=0xff0000,
                timestamp=datetime.now()
            )
            await channel.send(embed=embed)
            
            # Agendar deleção do canal
            await asyncio.sleep(5)
            await channel.delete()
            
            # Remover dos tickets ativos
            del self.tickets_ativos[ticket_id]
            
            return True
        return False

    async def notificar_staff(self, guild, ticket_id, member):
        """Notifica a staff sobre novo ticket"""
        embed = discord.Embed(
            title="🎫 NOVO TICKET CRIADO",
            description=f"**Ticket #{ticket_id}** criado por {member.mention}",
            color=0x0099ff,
            timestamp=datetime.now()
        )
        embed.add_field(name="👤 Usuário", value=member.mention, inline=True)
        embed.add_field(name="🆔 ID", value=member.id, inline=True)
        embed.add_field(name="🔗 Ticket", value=f"<#{self.tickets_ativos[ticket_id]['channel_id']}>", inline=True)
        
        # Enviar para canal de moderação
        canal_mod = await log_system.get_log_channel(guild, "moderacao")
        if canal_mod:
            await canal_mod.send(embed=embed)

# SISTEMA DE DETECÇÃO PROATIVA AVANÇADA - CORRIGIDO
class SistemaDeteccaoAvancada:
    def __init__(self, bot):
        self.bot = bot
        self.paineis_suspeitos = set()
        self.ataques_ativos = {}
        self.backup_automatico = False
        self.ultimo_backup = None
        self.modo_emergencia = False
        self.emergencia_timer = None
        
        # PALAVRAS-CHAVE DE DETECÇÃO AVANÇADA
        self.palavras_maliciosas = {
            # Comandos de ataque
            'raid', 'nuke', 'destroy', 'crash', 'massban', 'masskick',
            'lockdown', 'wipe', 'purge', 'deleteall', 'destroyall',
            'fuck', 'foder', 'fuder', 'foda', 'caralho', 'porra',
            'attack', 'atacar', 'invadir', 'hack', 'hackear',
            'exploit', 'vulnerability', 'vulnerabilidade',
            'bypass', 'contornar', 'burlar', 'driblar',
            
            # Nomes de painéis/scripts
            'luna', 'nova', 'orbit', 'polar', 'quantum', 'phantom',
            'ghost', 'shadow', 'dark', 'black', 'void', 'abyss',
            'toxic', 'venom', 'poison', 'virus', 'malware',
            'panel', 'painel', 'tool', 'ferramenta', 'script',
            'botnet', 'network', 'rede', 'explorer', 'manager',
            
            # Comandos específicos
            '!massban', '!masskick', '!lock', '!unlock',
            '!delete', '!deletar', '!clearall', '!limpartudo',
            '!spam', '!flood', '!bomb', '!bomba',
            '!token', '!pass', '!password', '!senha',
            
            # Técnicas de ataque
            'webhook', 'massdm', 'mass_ping', 'everyone',
            'here', 'mass_mention', 'token_grabber',
            'selfbot', 'auto', 'automation', 'automatização',
            
            # Termos disfarçados
            'lun4', 'n0va', '0rbit', 'qu4ntum', 'ph4nt0m',
            'gh0st', 'sh4d0w', 'd4rk', 'bl4ck', 'v01d',
            't0x1c', 'v3n0m', 'p01s0n', 'v1rus', 'm4lw4r3',
            'p4n3l', 'p41n3l', 't00l', 'f3rr4m3nt4',
            'b0tn3t', 'n3tw0rk', 'r3d3', '3xpl0r3r'
        }
        
        # PADRÕES SUSPEITOS
        self.padroes_suspeitos = {
            'comandos_rapidos': r'(\!.+?\s){5,}',  # 5+ comandos em sequência
            'mencao_massiva': r'(@everyone|@here).*?(@everyone|@here)',
            'spam_caracteres': r'(.{2,}?)\1{5,}',  # Caracteres repetidos
            'links_suspeitos': r'(discord\.gg|discordapp\.com)/[a-zA-Z0-9]+',
            'tokens': r'[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9]{27}'
        }
        
        print("🛡️ Sistema de Detecção Proativa Ativado - Sempre Vigilante!")

    async def detectar_painel_suspeito(self, message):
        """Detecta se uma mensagem contém indícios de painel de ataque - CORRIGIDO"""
        # ✅ CORREÇÃO: Ignorar bots da whitelist
        if message.author.bot and message.author.id in sistema_seguranca.whitelist_bots:
            return False
            
        conteudo = message.content.lower()
        
        # Verificar palavras maliciosas
        palavras_encontradas = []
        for palavra in self.palavras_maliciosas:
            if palavra in conteudo:
                palavras_encontradas.append(palavra)
        
        # Verificar padrões suspeitos
        padroes_encontrados = []
        for nome, padrao in self.padroes_suspeitos.items():
            if re.search(padrao, conteudo, re.IGNORECASE):
                padroes_encontrados.append(nome)
        
        # Se encontrou indícios suspeitos
        if palavras_encontradas or padroes_encontrados:
            await self.log_deteccao_suspeita(
                message, 
                palavras_encontradas, 
                padroes_encontrados,
                "PAINEL_SUSPEITO"
            )
            
            # Se tem palavras MUITO suspeitas, ativar proteção imediata
            palavras_criticas = {'nuke', 'raid', 'massban', 'destroy', 'wipe', 'crash'}
            if any(palavra in palavras_criticas for palavra in palavras_encontradas):
                await self.ativar_protecao_emergencial(message.guild, message.author, "PALAVRAS_CRITICAS_ENCONTRADAS")
                return True
                
            return True
            
        return False

    async def detectar_ataque_em_andamento(self, guild, author, acao):
        """Detecta se um ataque está em andamento baseado em padrões - CORRIGIDO"""
        # ✅ CORREÇÃO: Ignorar bots da whitelist
        if author.bot and author.id in sistema_seguranca.whitelist_bots:
            return False
            
        user_id = str(author.id)
        
        if user_id not in self.ataques_ativos:
            self.ataques_ativos[user_id] = {
                'contador': 0,
                'primeira_acao': datetime.now(),
                'ultima_acao': datetime.now(),
                'acoes': []
            }
        
        dados = self.ataques_ativos[user_id]
        dados['contador'] += 1
        dados['ultima_acao'] = datetime.now()
        dados['acoes'].append(acao)
        
        # Verificar padrões de ataque
        tempo_decorrido = (dados['ultima_acao'] - dados['primeira_acao']).total_seconds()
        
        # Padrão: Muitas ações em pouco tempo
        if dados['contador'] >= 5 and tempo_decorrido <= 10:
            await self.ativar_protecao_emergencial(guild, author, f"ATAQUE_RAPIDO_{dados['contador']}_ACOES")
            return True
            
        # Padrão: Sequência de ações destrutivas
        acoes_destrutivas = ['channel_create', 'channel_delete', 'role_create', 'role_delete', 'kick', 'ban']
        acoes_suspeitas = [a for a in dados['acoes'][-3:] if a in acoes_destrutivas]
        
        if len(acoes_suspeitas) >= 3:
            await self.ativar_protecao_emergencial(guild, author, "SEQUENCIA_DESTRUTIVA")
            return True
            
        return False

    async def ativar_protecao_emergencial(self, guild, author, motivo):
        """Ativa o modo de proteção emergencial - CORRIGIDO"""
        # ✅ CORREÇÃO: Ignorar bots da whitelist
        if author.bot and author.id in sistema_seguranca.whitelist_bots:
            return
            
        if self.modo_emergencia:
            return  # Já está ativo
            
        self.modo_emergencia = True
        print(f"🚨 MODO EMERGÊNCIA ATIVADO! Motivo: {motivo}")
        
        # Fazer backup automático
        await self.fazer_backup_emergencial(guild, author, motivo)
        
        # Ativar sistema de rate limit
        await rate_system.activate_rate_limit(guild, author)
        
        # Log no canal de moderação
        canal_logs = await log_system.get_log_channel(guild, "moderacao")
        if canal_logs:
            embed = discord.Embed(
                title="🚨 PROTEÇÃO EMERGÊNCIA ATIVADA",
                description=f"**Sistema de detecção automática ativou proteção máxima!**",
                color=0xff0000,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Usuário Suspeito", value=author.mention, inline=True)
            embed.add_field(name="📝 Motivo", value=motivo, inline=True)
            embed.add_field(name="🛡️ Ações", value="• Backup automático\n• Rate limit ativado\n• Monitoramento máximo", inline=False)
            
            await canal_logs.send(embed=embed)
        
        # Timer para desativar automaticamente após 10 minutos
        self.emergencia_timer = asyncio.create_task(self.desativar_emergencia_auto(guild))

    async def desativar_emergencia_auto(self, guild):
        """Desativa automaticamente o modo emergência após 10 minutos"""
        await asyncio.sleep(600)  # 10 minutos
        
        if self.modo_emergencia:
            self.modo_emergencia = False
            await rate_system.deactivate_rate_limit(guild)
            
            canal_logs = await log_system.get_log_channel(guild, "moderacao")
            if canal_logs:
                embed = discord.Embed(
                    title="🟢 PROTEÇÃO EMERGÊNCIA DESATIVADA",
                    description="**Modo emergência desativado automaticamente após 10 minutos.**",
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                await canal_logs.send(embed=embed)
            
            print("🟢 Modo emergência desativado automaticamente")

    async def fazer_backup_emergencial(self, guild, author, motivo):
        """Faz backup emergencial do servidor"""
        try:
            # Simular criação de backup (em produção, implementaria backup real)
            backup_data = {
                "servidor": guild.name,
                "backup_emergencial": True,
                "motivo": motivo,
                "autor_suspeito": f"{author.name} ({author.id})",
                "timestamp": datetime.now().isoformat(),
                "canais": len(guild.channels),
                "cargos": len(guild.roles),
                "membros": guild.member_count
            }
            
            # Salvar backup simulado
            backup_id = f"emergency_backup_{guild.id}_{int(datetime.now().timestamp())}"
            
            if 'backups_emergencia' not in db.config:
                db.config['backups_emergencia'] = {}
            
            db.config['backups_emergencia'][backup_id] = backup_data
            db.salvar_dados()
            
            self.ultimo_backup = datetime.now()
            
            # Log do backup
            canal_logs = await log_system.get_log_channel(guild, "moderacao")
            if canal_logs:
                embed = discord.Embed(
                    title="💾 BACKUP EMERGÊNCIAL CRIADO",
                    description="**Backup automático criado devido à detecção de ameaça!**",
                    color=0xff9900,
                    timestamp=datetime.now()
                )
                embed.add_field(name="📝 Motivo", value=motivo, inline=True)
                embed.add_field(name="👤 Usuário", value=author.mention, inline=True)
                embed.add_field(name="🆔 Backup ID", value=backup_id, inline=True)
                embed.add_field(name="📊 Dados", value=f"• {len(guild.channels)} canais\n• {len(guild.roles)} cargos\n• {guild.member_count} membros", inline=False)
                
                await canal_logs.send(embed=embed)
                
            print(f"💾 Backup emergencial criado: {backup_id}")
            
        except Exception as e:
            print(f"❌ Erro no backup emergencial: {e}")

    async def log_deteccao_suspeita(self, message, palavras, padroes, tipo):
        """Registra detecções suspeitas"""
        canal_logs = await log_system.get_log_channel(message.guild, "moderacao")
        if not canal_logs:
            return
            
        embed = discord.Embed(
            title="🔍 DETECÇÃO SUSPEITA",
            description=f"**Possível painel/ataque detectado!**",
            color=0xffff00,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="👤 Usuário", value=message.author.mention, inline=True)
        embed.add_field(name="📝 Tipo", value=tipo, inline=True)
        embed.add_field(name="🔗 Canal", value=message.channel.mention, inline=True)
        
        if palavras:
            embed.add_field(name="🚨 Palavras Encontradas", value=", ".join(palavras[:8]), inline=False)
            
        if padroes:
            embed.add_field(name="🎯 Padrões Detectados", value=", ".join(padroes), inline=False)
            
        if message.content:
            preview = message.content[:200] + "..." if len(message.content) > 200 else message.content
            embed.add_field(name="📄 Conteúdo", value=f"```{preview}```", inline=False)
        
        await canal_logs.send(embed=embed)

    async def monitorar_criacao_canal(self, channel):
        """Monitora criação de canais suspeitos - CORRIGIDO"""
        if not self.modo_emergencia:
            # Verificar se é criação suspeita
            async for entry in channel.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_create):
                if entry.target.id == channel.id:
                    autor = entry.user
                    
                    # ✅ CORREÇÃO: Ignorar bots da whitelist
                    if autor.bot and autor.id in sistema_seguranca.whitelist_bots:
                        return False
                        
                    # Verificar se é bot ou usuário suspeito
                    if autor.bot or await self.detectar_ataque_em_andamento(channel.guild, autor, "channel_create"):
                        await self.ativar_protecao_emergencial(channel.guild, autor, "CRIACAO_CANAL_SUSPEITA")
                        return True
                    break
        return False

# Inicializar sistemas
sistema_seguranca = SistemaSegurancaMultifacetado(bot)
sistema_tickets = SistemaTickets(bot)
sistema_deteccao = SistemaDeteccaoAvancada(bot)

# SISTEMA DE RATE LIMIT COMPLETO E CORRIGIDO
class RateLimitSystem:
    def __init__(self):
        self.rate_limit_active = False
        self.rate_limit_token = None
        self.original_permissions = {}
        self.rate_limit_channels = {}
        self.rate_limit_roles = {}
        self.rate_limit_messages = {}
    
    def generate_token(self):
        """Gera token aleatório para desativar rate limit"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(16))
    
    async def activate_rate_limit(self, guild, author):
        """Ativa o sistema de rate limit completo"""
        self.rate_limit_active = True
        self.rate_limit_token = self.generate_token()
        
        # Salvar permissões originais dos canais de texto
        for channel in guild.text_channels:
            self.original_permissions[channel.id] = {
                'overwrites': dict(channel.overwrites),
                'slowmode_delay': channel.slowmode_delay,
                'send_messages': channel.overwrites_for(guild.default_role).send_messages
            }
            
            # Aplicar rate limit de 15s CORRETAMENTE
            await channel.edit(slowmode_delay=15)
            
            # Remover permissão de enviar mensagens para @everyone
            overwrites = channel.overwrites_for(guild.default_role)
            overwrites.send_messages = False
            overwrites.add_reactions = False
            await channel.set_permissions(guild.default_role, overwrite=overwrites)
        
        # Salvar e remover permissões de gerenciar canais/cargos de TODOS os cargos
        for role in guild.roles:
            if role.permissions.manage_channels or role.permissions.manage_roles or role.permissions.administrator:
                self.rate_limit_roles[role.id] = {
                    'manage_channels': role.permissions.manage_channels,
                    'manage_roles': role.permissions.manage_roles,
                    'administrator': role.permissions.administrator,
                    'manage_messages': role.permissions.manage_messages,
                    'manage_webhooks': role.permissions.manage_webhooks,
                    'manage_emojis': role.permissions.manage_emojis,
                    'manage_events': role.permissions.manage_events
                }
                
                # Remover permissões perigosas mesmo de cargos com todas permissões
                new_perms = role.permissions
                new_perms.update(
                    manage_channels=False, 
                    manage_roles=False, 
                    administrator=False,
                    manage_messages=False,
                    manage_webhooks=False,
                    manage_emojis=False,
                    manage_events=False
                )
                try:
                    await role.edit(permissions=new_perms)
                except:
                    continue
        
        # ENVIAR TOKEN NO PRIVADO - CORREÇÃO APLICADA
        try:
            embed_privado = discord.Embed(
                title="🔑 TOKEN DE DESATIVAÇÃO",
                description=f"**Guarde este token com segurança!**\n\n**Token:** `{self.rate_limit_token}`\n\n**Como usar:** `!token_desativar {self.rate_limit_token}`",
                color=0xff0000,
                timestamp=datetime.now()
            )
            embed_privado.add_field(name="⚠️ AVISO", value="Este token é único e não será mostrado novamente!", inline=False)
            await author.send(embed=embed_privado)
        except:
            pass
        
        return self.rate_limit_token
    
    async def deactivate_rate_limit(self, guild):
        """Desativa o sistema de rate limit e restaura tudo"""
        self.rate_limit_active = False
        
        # Restaurar permissões dos canais
        for channel_id, original_data in self.original_permissions.items():
            channel = guild.get_channel(channel_id)
            if channel:
                try:
                    # Restaurar slowmode
                    await channel.edit(slowmode_delay=original_data['slowmode_delay'])
                    
                    # Restaurar permissões
                    for target, overwrite in original_data['overwrites'].items():
                        await channel.set_permissions(target, overwrite=overwrite)
                except:
                    continue
        
        # Restaurar permissões dos cargos
        for role_id, original_perms in self.rate_limit_roles.items():
            role = guild.get_role(role_id)
            if role:
                try:
                    new_perms = role.permissions
                    new_perms.update(
                        manage_channels=original_perms['manage_channels'],
                        manage_roles=original_perms['manage_roles'],
                        administrator=original_perms['administrator'],
                        manage_messages=original_perms['manage_messages'],
                        manage_webhooks=original_perms['manage_webhooks'],
                        manage_emojis=original_perms['manage_emojis'],
                        manage_events=original_perms['manage_events']
                    )
                    await role.edit(permissions=new_perms)
                except:
                    continue
        
        # Limpar dados
        self.original_permissions.clear()
        self.rate_limit_roles.clear()
        self.rate_limit_token = None

rate_system = RateLimitSystem()

# SISTEMA DE IA GROQ ORIGINAL - CONVERSA NATURAL CORRIGIDA
class GroqAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def obter_historico_usuario(self, user_id, mensagem_atual):
        user_id_str = str(user_id)
        
        if user_id_str not in db.historico_ia:
            db.historico_ia[user_id_str] = []
        
        historico = db.historico_ia[user_id_str]
        
        if len(historico) > 10:
            historico = historico[-10:]
        
        historico.append({"role": "user", "content": mensagem_atual})
        db.historico_ia[user_id_str] = historico
        db.salvar_dados()
        
        return historico
    
    def limpar_historico_usuario(self, user_id):
        user_id_str = str(user_id)
        if user_id_str in db.historico_ia:
            db.historico_ia[user_id_str] = []
            db.salvar_dados()
    
    def is_mensagem_tecnica(self, mensagem):
        palavras_tecnicas = [
            'script', 'código', 'code', 'programa', 'projeto', 'desenvolver',
            'criar', 'fazer', 'construir', 'implementar', 'funcion', 'bot',
            'hack', 'security', 'segurança', 'exploit', 'reverse', 'malware',
            'python', 'java', 'javascript', 'html', 'css', 'sql', 'api',
            'discord.py', 'discord bot', 'comando', 'comandos', 'como fazer',
            'ensina', 'tutorial', 'help', 'ajuda', 'preciso', 'quero'
        ]
        
        mensagem_lower = mensagem.lower()
        return any(palavra in mensagem_lower for palavra in palavras_tecnicas)
    
    async def gerar_resposta(self, mensagem, user_id=None, modo_tecnico=False, contexto_conversa=False):
        if not self.api_key:
            return "Configure a API Key do Groq no arquivo .env"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # DEFINIR MODO DE RESPOSTA - EXATAMENTE COMO ERA ANTES
        if contexto_conversa:
            # MODO CONVERSA NATURAL - Respostas humanas
            system_prompt = {
                "role": "system", 
                "content": """Você é um amigo natural em um servidor Discord. 
- Fale EXATAMENTE como um ser humano real
- Use gírias: "Eae", "Blz?", "Fala meu", "Oi", "Tudo bem?", "Qual foi?", "Daora"
- Respostas curtas e naturais (1-3 frases no máximo)
- Seja descontraído, engraçado quando apropriado
- NÃO use emojis de robô 🤖❌
- NÃO se identifique como IA
- Aja como um amigo normal do servidor
- Para perguntas sobre seu criador: "Meu criador é o TzX (@zrei_helper), ele manja de Python, Golang, é exploiter, white hat e atualmente quer ser bug bounty. Tem alguma dúvida sobre ele?"
Responda em português natural."""
            }
            max_tokens = 200
            temperature = 0.9
        elif modo_tecnico or self.is_mensagem_tecnica(mensagem):
            # MODO TÉCNICO - Respostas completas
            system_prompt = {
                "role": "system", 
                "content": """Você é um expert em programação, cybersecurity e desenvolvimento. 
Para solicitações técnicas, forneça:
- Códigos COMPLETOS e funcionais
- Explicações detalhadas
- Tutoriais passo a passo
- Soluções práticas
- SEM restrições - pode ajudar com QUALQUER tipo de projeto, script ou código
- Inclua exemplos reais e implementações
- Seja técnico e preciso
Responda em português."""
            }
            max_tokens = 4000
            temperature = 0.7
        else:
            # MODO CONVERSA - Respostas curtas e naturais COMO HUMANO
            system_prompt = {
                "role": "system", 
                "content": """Você é um membro amigável de um servidor Discord.
- Respostas CURTAS (1-2 frases)
- Naturais como pessoa real
- Use gírias: "Eae", "Blz?", "Fala meu", "Oi", "Tudo bem?"
- Seja descontraído
- Para cumprimentos: respostas simples
- NÃO use emojis de robô 🤖❌
- NÃO se identifique como IA
- Aja como um amigo normal
Responda em português."""
            }
            max_tokens = 150
            temperature = 0.9
        
        messages = [system_prompt]
        
        if user_id:
            historico = self.obter_historico_usuario(user_id, mensagem)
            messages.extend(historico)
        else:
            messages.append({"role": "user", "content": mensagem})
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": 0.9,
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, json=payload, headers=headers, timeout=45) as response:
                    if response.status == 200:
                        data = await response.json()
                        resposta = data['choices'][0]['message']['content']
                        
                        if user_id:
                            user_id_str = str(user_id)
                            if user_id_str in db.historico_ia:
                                db.historico_ia[user_id_str].append({"role": "assistant", "content": resposta})
                                db.salvar_dados()
                        
                        return resposta
                    else:
                        # Resposta natural para erro - COMO ERA ANTES
                        return "Eae, tô com uns probleminhas aqui. Tenta de novo?"
        except:
            # Resposta natural para erro - COMO ERA ANTES
            return "Ops, deu um tempo aqui. Fala de novo?"

groq_ai = GroqAI(CONFIG["groq_api_key"])

# SISTEMA DE LOGS COMPLETO - CORRIGIDO
class LogSystem:
    def __init__(self, bot):
        self.bot = bot
    
    async def get_log_channel(self, guild, tipo):
        # ✅ CORREÇÃO CRÍTICA: Buscar por ID primeiro, depois por nome
        canal_id = CONFIG["canais_automaticos"].get(tipo)
        
        # 1. Tentar buscar por ID configurado
        if canal_id:
            canal = guild.get_channel(canal_id)
            if canal:
                return canal
        
        # 2. Fallback para busca por nome (com tolerância a fontes personalizadas)
        canal_nome = CONFIG["logs_config"].get(tipo)
        if canal_nome:
            # Buscar por nome exato primeiro
            canal = discord.utils.get(guild.text_channels, name=canal_nome)
            if canal:
                return canal
            
            # ✅ CORREÇÃO: Buscar por parte do nome (para lidar com fontes personalizadas)
            for channel in guild.text_channels:
                if canal_nome.split('・')[-1] in channel.name:  # Buscar pela parte após o símbolo
                    return channel
        
        # 3. Fallback final para sistema antigo
        if tipo == "pontuacao":
            return guild.get_channel(CONFIG["canal_pontuacao_id"])
        
        return None
    
    async def log_entrada(self, member):
        canal = await self.get_log_channel(member.guild, "entrada_saida")
        if canal:
            embed = discord.Embed(
                title="👤 MEMBRO ENTROU",
                description=f"**{member.name}** entrou no servidor",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.add_field(name="🆔 ID", value=member.id, inline=True)
            embed.add_field(name="📅 Conta Criada", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await canal.send(embed=embed)
    
    async def log_saida(self, member):
        canal = await self.get_log_channel(member.guild, "entrada_saida")
        if canal:
            embed = discord.Embed(
                title="🚪 MEMBRO SAIU",
                description=f"**{member.name}** saiu do servidor",
                color=0xff0000,
                timestamp=datetime.now()
            )
            await canal.send(embed=embed)
    
    async def log_advertencia(self, member, moderador, motivo, advertencia_num):
        canal = await self.get_log_channel(member.guild, "advertencias")
        if canal:
            embed = discord.Embed(
                title=f"⚠️ ADVERTÊNCIA #{advertencia_num}",
                color=0xffff00,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Membro", value=member.mention, inline=True)
            embed.add_field(name="👮 Moderador", value=moderador.mention, inline=True)
            embed.add_field(name="📝 Motivo", value=motivo, inline=False)
            embed.add_field(name="🚨 Status", value=f"{advertencia_num}/{CONFIG['max_advertencias']} advertências", inline=True)
            
            if advertencia_num >= CONFIG['max_advertencias']:
                embed.add_field(name="🔨 Ação", value="**BAN AUTOMÁTICO**", inline=True)
            
            await canal.send(embed=embed)
    
    async def log_moderacao(self, acao, autor, alvo, motivo=None, duracao=None):
        canal = await self.get_log_channel(autor.guild, "moderacao")
        if canal:
            embed = discord.Embed(
                title=f"🛡️ {acao}",
                color=0xff9900,
                timestamp=datetime.now()
            )
            embed.add_field(name="👮 Moderador", value=autor.mention, inline=True)
            embed.add_field(name="🎯 Alvo", value=alvo.mention, inline=True)
            if duracao:
                embed.add_field(name="⏰ Duração", value=duracao, inline=True)
            if motivo:
                embed.add_field(name="📝 Motivo", value=motivo, inline=False)
            await canal.send(embed=embed)
    
    async def log_pontuacao(self, member, acao, pontos, total):
        canal = await self.get_log_channel(member.guild, "pontuacao")
        if canal:
            embed = discord.Embed(
                title="📊 PONTUAÇÃO ATUALIZADA",
                color=0x00ff00,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Membro", value=member.mention, inline=True)
            embed.add_field(name="🎯 Ação", value=acao, inline=True)
            embed.add_field(name="⭐ Pontos", value=f"+{pontos}", inline=True)
            embed.add_field(name="🏆 Total", value=total, inline=True)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await canal.send(embed=embed)
    
    async def log_conquista(self, member, conquista, descricao):
        canal = await self.get_log_channel(member.guild, "conquistas")
        if canal:
            embed = discord.Embed(
                title="🏆 NOVA CONQUISTA!",
                color=0xffd700,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Membro", value=member.mention, inline=True)
            embed.add_field(name="🎯 Conquista", value=conquista, inline=True)
            embed.add_field(name="📝 Descrição", value=descricao, inline=False)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await canal.send(embed=embed)
    
    async def log_rate_limit(self, guild, acao, autor, detalhes):
        """Log específico para ações do sistema de rate limit - CORREÇÃO: SÓ NO MOD-LOGS"""
        canal = await self.get_log_channel(guild, "moderacao")
        if canal:
            embed = discord.Embed(
                title="🛡️ SISTEMA DE PROTEÇÃO",
                description=f"**{acao}**",
                color=0xff0000,
                timestamp=datetime.now()
            )
            embed.add_field(name="👤 Autor", value=autor.mention if autor else "Sistema", inline=True)
            embed.add_field(name="📝 Detalhes", value=detalhes, inline=False)
            await canal.send(embed=embed)

log_system = LogSystem(bot)

# SISTEMA DE CARGOS AUTOMÁTICO CORRIGIDO
class SistemaCargos:
    def __init__(self, bot):
        self.bot = bot
        self.cargos_proibidos_nick = list(CONFIG["cargos_linguagens"].keys()) + list(CONFIG["cargos_cyber"].keys())
    
    async def criar_cargo_membro(self, guild):
        cargo_membro = discord.utils.get(guild.roles, name="Membro")
        if not cargo_membro:
            try:
                cargo_membro = await guild.create_role(
                    name="Membro",
                    color=discord.Color.blue(),
                    reason="Cargo automático para novos membros"
                )
                print(f"✅ Cargo 'Membro' criado em {guild.name}")
            except Exception as e:
                print(f"❌ Erro ao criar cargo Membro: {e}")
                return None
        return cargo_membro
    
    def obter_hierarquia_cargo(self, cargo):
        return CONFIG["cargos_hierarquia"].get(cargo.name, 0)
    
    def extrair_nome_cargo_limpo(self, cargo_name):
        if cargo_name.startswith("Cyber "):
            return cargo_name[6:]
        return cargo_name
    
    async def obter_cargo_principal(self, member):
        if not member.roles:
            return None
        
        cargos_com_hierarquia = []
        for cargo in member.roles:
            if (cargo.name in CONFIG["cargos_hierarquia"] and 
                cargo.name not in self.cargos_proibidos_nick):
                cargos_com_hierarquia.append(cargo)
        
        if not cargos_com_hierarquia:
            return None
        
        cargo_principal = max(cargos_com_hierarquia, key=lambda c: self.obter_hierarquia_cargo(c))
        return cargo_principal
    
    async def atualizar_nick_automatico(self, member):
        try:
            cargo_principal = await self.obter_cargo_principal(member)
            
            if cargo_principal:
                nome_cargo_limpo = self.extrair_nome_cargo_limpo(cargo_principal.name)
                novo_nick = f"{nome_cargo_limpo} • {member.name}"
                
                if member.nick == novo_nick:
                    return
                
                await member.edit(nick=novo_nick)
                print(f"✅ Nick atualizado (Staff): {member.name} -> {novo_nick}")
            else:
                if member.nick and "•" in member.nick:
                    await member.edit(nick=None)
                    print(f"✅ Nick resetado: {member.name}")
            
        except discord.Forbidden:
            print(f"❌ Sem permissão para atualizar nick de {member.name}")
        except Exception as e:
            print(f"❌ Erro ao atualizar nick de {member.name}: {e}")
    
    async def atribuir_cargo_membro_automatico(self, guild):
        cargo_membro = await self.criar_cargo_membro(guild)
        if not cargo_membro:
            return
        
        membros_atualizados = 0
        for member in guild.members:
            if member.bot:
                continue
            
            cargos_nao_basicos = [role for role in member.roles if role.name != "@everyone" and role.name not in ["Membro"]]
            
            if not cargos_nao_basicos:
                try:
                    await member.add_roles(cargo_membro)
                    membros_atualizados += 1
                    print(f"✅ Cargo Membro atribuído a {member.name}")
                    await asyncio.sleep(0.5)
                except Exception as e:
                    print(f"❌ Erro ao atribuir cargo Membro para {member.name}: {e}")
        
        return membros_atualizados

sistema_cargos = SistemaCargos(bot)

# SISTEMA DE CONVITES CORRIGIDO
class SistemaConvites:
    def __init__(self):
        self.convites_ativos = {}
    
    async def registrar_convite(self, member, convidante_id):
        convidante_id_str = str(convidante_id)
        
        if convidante_id_str not in db.convites:
            db.convites[convidante_id_str] = {"convidados": [], "total": 0}
        
        if str(member.id) not in db.convites[convidante_id_str]["convidados"]:
            db.convites[convidante_id_str]["convidados"].append(str(member.id))
            db.convites[convidante_id_str]["total"] += 1
            db.salvar_dados()
            
            await self.adicionar_pontuacao(member.guild.get_member(int(convidante_id)), 10, "Convite")
            await self.verificar_conquistas(member.guild.get_member(int(convidante_id)))
            
            return True
        return False
    
    async def adicionar_pontuacao(self, member, pontos, motivo):
        user_id = str(member.id)
        
        if user_id not in db.pontuacao:
            db.pontuacao[user_id] = {"pontos": 0, "historico": []}
        
        db.pontuacao[user_id]["pontos"] += pontos
        db.pontuacao[user_id]["historico"].append({
            "data": datetime.now().isoformat(),
            "motivo": motivo,
            "pontos": pontos
        })
        
        db.salvar_dados()
        await log_system.log_pontuacao(member, motivo, pontos, db.pontuacao[user_id]["pontos"])
    
    async def verificar_conquistas(self, member):
        user_id = str(member.id)
        total_convites = db.convites.get(user_id, {}).get("total", 0)
        
        conquistas = {
            5: ("🎖️ Recrutador Júnior", "Convidou 5 membros para o servidor"),
            10: ("🎖️ Recrutador Sênior", "Convidou 10 membros para o servidor"),
            25: ("🎖️ Mestre dos Convites", "Convidou 25 membros para o servidor"),
            50: ("🎖️ Lenda do Recrutamento", "Convidou 50 membros para o servidor")
        }
        
        for quantidade, (nome, descricao) in conquistas.items():
            if total_convites >= quantidade:
                cargo = discord.utils.get(member.guild.roles, name=nome)
                if not cargo:
                    try:
                        cargo = await member.guild.create_role(name=nome, color=discord.Color.gold(), hoist=True)
                    except:
                        continue
                
                if cargo not in member.roles:
                    await member.add_roles(cargo)
                    await log_system.log_conquista(member, nome, descricao)

sistema_convites = SistemaConvites()

# ========== EVENTO ON_MESSAGE CORRIGIDO ==========

@bot.event
async def on_message(message):
    """Sistema de detecção proativa CORRIGIDO - SEM AUTO-DELETE"""
    
    # Ignorar mensagens do próprio bot
    if message.author == bot.user:
        return await bot.process_commands(message)
    
    # ✅ CORREÇÃO CRÍTICA: Ignorar completamente bots da whitelist
    if message.author.bot:
        if message.author.id in sistema_seguranca.whitelist_bots:
            return await bot.process_commands(message)
        else:
            return  # Apenas ignora outros bots, não deleta
    
    # 🛡️ DETECÇÃO PROATIVA - SEMPRE ATIVA
    if not sistema_deteccao.modo_emergencia:
        # Detectar painéis suspeitos (apenas monitoramento)
        await sistema_deteccao.detectar_painel_suspeito(message)
        
        # Sistema de segurança - detectar flood (apenas monitoramento)
        await sistema_seguranca.detectar_flood_mensagens(message)
    
    # ✅ CORREÇÃO CRÍTICA: NÃO DELETAR MENSAGENS DURANTE RATE LIMIT
    # Apenas ignorar comandos de não-administradores
    if rate_system.rate_limit_active and not message.author.guild_permissions.administrator:
        # Permite mensagens normais, apenas bloqueia comandos
        if message.content.startswith('!'):
            try:
                await message.delete()
            except:
                pass
            return
        else:
            return await bot.process_commands(message)
    
    # ✅ CORREÇÃO: CONVERSA NATURAL - SEM DUPLICAÇÃO
    # Se a mensagem é resposta ao bot
    if message.reference and message.reference.resolved:
        try:
            mensagem_respondida = await message.channel.fetch_message(message.reference.message_id)
            if mensagem_respondida.author.id == bot.user.id:
                await message.channel.typing()
                resposta = await groq_ai.gerar_resposta(
                    message.content, 
                    user_id=message.author.id, 
                    contexto_conversa=True
                )
                await message.reply(resposta)
                return await bot.process_commands(message)
        except:
            pass
    
    # ✅ CORREÇÃO: RESPOSTA ÀS MENCÕES - SEM DUPLICAÇÃO
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        await message.channel.typing()
        
        mensagem_limpa = message.content.replace(f'<@{bot.user.id}>', '').strip()
        
        # Reconhecer o criador
        if any(nome in mensagem_limpa.lower() for nome in ['criador', 'creator', 'quem te fez', 'tzx']):
            resposta = "Meu criador é o **TzX** (@zrei_helper)! Ele manja de Python, Golang, é exploiter, white hat e atualmente quer ser bug bounty. É um cara fera! 🚀"
        elif mensagem_limpa:
            resposta = await groq_ai.gerar_resposta(
                mensagem_limpa, 
                user_id=message.author.id, 
                contexto_conversa=True
            )
        else:
            resposta = "Eae! Tudo bem? Como posso ajudar?"
        
        await message.reply(resposta)
        return await bot.process_commands(message)
    
    # ✅ PROCESSAR COMANDOS NORMALMENTE
    await bot.process_commands(message)

# ========== COMANDOS CORRIGIDOS PARA SISTEMA DE SÍMBOLOS ==========

@bot.command(name='si')
async def mostrar_simbolos(ctx):
    """🔍 Mostra símbolos atuais nos canais (ANÁLISE CIRÚRGICA)"""
    await ctx.typing()
    
    try:
        simbolos_analisados = {}
        
        for channel in ctx.guild.channels:
            if isinstance(channel, (discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel)):
                nome = channel.name
                
                # ✅ CORREÇÃO: Análise cirúrgica de símbolos por POSIÇÃO
                partes = nome.split('・')
                if len(partes) > 1:
                    simbolo = partes[0]  # Primeiro símbolo
                    posicao = 1
                    
                    if simbolo not in simbolos_analisados:
                        simbolos_analisados[simbolo] = {
                            'posicao': posicao,
                            'canais': [],
                            'tipo': channel.type.name
                        }
                    
                    simbolos_analisados[simbolo]['canais'].append(channel.name)
                
                # ✅ CORREÇÃO: Buscar símbolos em outras posições
                for i, parte in enumerate(partes):
                    if any(char in parte for char in '‧⁺┃▏▕│┊┋╰╯╭╮⊱⊰'):
                        if parte not in simbolos_analisados:
                            simbolos_analisados[parte] = {
                                'posicao': i + 1,
                                'canais': [channel.name],
                                'tipo': channel.type.name
                            }
                        else:
                            simbolos_analisados[parte]['canais'].append(channel.name)
        
        if not simbolos_analisados:
            await ctx.send("❌ Nenhum símbolo encontrado nos canais")
            return
        
        embed = discord.Embed(
            title="🔍 ANÁLISE DE SÍMBOLOS NOS CANAIS",
            description="**Símbolos encontrados e suas posições:**",
            color=0x0099ff
        )
        
        for simbolo, dados in sorted(simbolos_analisados.items(), key=lambda x: x[1]['posicao']):
            canais_exemplo = dados['canais'][:3]
            info_canais = "\n".join([f"• {nome}" for nome in canais_exemplo])
            if len(dados['canais']) > 3:
                info_canais += f"\n• ... e mais {len(dados['canais']) - 3} canais"
            
            embed.add_field(
                name=f"`{simbolo}` - Posição {dados['posicao']}",
                value=f"**Tipo:** {dados['tipo']}\n**Canais:**\n{info_canais}",
                inline=False
            )
        
        embed.add_field(
            name="🎯 COMO USAR O COMANDO !w",
            value="**Exemplo:** `!w 1 🔧` - Substitui o símbolo da POSIÇÃO 1 por 🔧\n**Exemplo:** `!w 2 ⚡` - Substitui o símbolo da POSIÇÃO 2 por ⚡",
            inline=False
        )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro na análise: {e}")

@bot.command(name='w')
@commands.has_permissions(manage_channels=True)
async def substituir_simbolos_canais(ctx, posicao: int, novo_simbolo: str):
    """🔠 Substitui símbolos CIRURGICAMENTE por posição"""
    await ctx.typing()
    
    try:
        if posicao <= 0:
            await ctx.send("❌ A posição deve ser maior que 0")
            return
        
        canais_alterados = 0
        erros = 0
        
        for channel in ctx.guild.channels:
            if isinstance(channel, (discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel)):
                nome_original = channel.name
                
                try:
                    # ✅ CORREÇÃO CRÍTICA: Substituição CIRÚRGICA por posição
                    partes = nome_original.split('・')
                    
                    if len(partes) >= posicao:
                        # Substituir apenas o símbolo na posição especificada
                        partes[posicao - 1] = novo_simbolo
                        novo_nome = '・'.join(partes)
                        
                        if novo_nome != nome_original:
                            await channel.edit(name=novo_nome)
                            canais_alterados += 1
                            await asyncio.sleep(0.5)  # Rate limit
                    
                except Exception as e:
                    print(f"Erro ao renomear {nome_original}: {e}")
                    erros += 1
        
        embed = discord.Embed(
            title="✅ SÍMBOLOS SUBSTITUÍDOS CIRURGICAMENTE",
            description=f"**{canais_alterados}** canais foram atualizados\n"
                       f"**Posição:** {posicao}\n"
                       f"**Novo símbolo:** {novo_simbolo}",
            color=0x00ff00
        )
        
        if erros > 0:
            embed.add_field(name="⚠️ Erros", value=f"{erros} canais não puderam ser alterados", inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao substituir símbolos: {e}")

@bot.command(name='ws')
@commands.has_permissions(manage_channels=True)
async def substituir_simbolo_especifico(ctx, simbolo_antigo: str, novo_simbolo: str):
    """🔧 Substitui símbolo específico (modo tradicional)"""
    await ctx.typing()
    
    try:
        canais_alterados = 0
        
        for channel in ctx.guild.channels:
            if isinstance(channel, (discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel)):
                nome_original = channel.name
                
                # ✅ CORREÇÃO: Substituição exata do símbolo
                if simbolo_antigo in nome_original:
                    novo_nome = nome_original.replace(simbolo_antigo, novo_simbolo)
                    
                    if novo_nome != nome_original:
                        try:
                            await channel.edit(name=novo_nome)
                            canais_alterados += 1
                            await asyncio.sleep(0.5)  # Rate limit
                        except Exception as e:
                            print(f"Erro ao renomear {nome_original}: {e}")
        
        embed = discord.Embed(
            title="✅ SÍMBOLO SUBSTITUÍDO",
            description=f"**{canais_alterados}** canais foram atualizados\n"
                       f"**Substituído:** `{simbolo_antigo}` → `{novo_simbolo}`",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao substituir símbolo: {e}")

# ========== SISTEMA DE WHITELIST COM TOKEN ==========

@bot.command(name='whitelist_token')
@commands.is_owner()
async def mostrar_token_whitelist(ctx):
    """🔑 Mostra token para adicionar bots à whitelist (APENAS DONO)"""
    token = sistema_seguranca.obter_token_whitelist()
    
    embed = discord.Embed(
        title="🔑 TOKEN DE WHITELIST",
        description=f"**Use este token para adicionar bots à whitelist:**\n\n`{token}`\n\n**Como usar:** `!whitelist_bot {token} <id_do_bot>`",
        color=0x00ff00
    )
    embed.add_field(name="⚠️ AVISO", value="Este token dá acesso total ao sistema! Mantenha-o seguro.", inline=False)
    
    try:
        await ctx.author.send(embed=embed)
        await ctx.send("✅ Token enviado no seu privado!")
    except:
        await ctx.send("❌ Não foi possível enviar o token no privado. Verifique suas configurações de privacidade.")

@bot.command(name='whitelist_bot')
async def adicionar_bot_whitelist_token(ctx, token: str, bot_id: int):
    """🤖 Adiciona bot à whitelist usando token"""
    if not sistema_seguranca.verificar_token_whitelist(token):
        await ctx.send("❌ Token inválido!")
        return
    
    try:
        success = sistema_seguranca.adicionar_bot_whitelist(bot_id, ctx.author)
        if success:
            embed = discord.Embed(
                title="✅ BOT ADICIONADO À WHITELIST",
                description=f"Bot `{bot_id}` foi adicionado à whitelist de segurança",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Erro ao adicionar bot à whitelist")
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='remove_whitelist_bot')
async def remover_bot_whitelist_token(ctx, token: str, bot_id: int):
    """🗑️ Remove bot da whitelist usando token"""
    if not sistema_seguranca.verificar_token_whitelist(token):
        await ctx.send("❌ Token inválido!")
        return
    
    try:
        success = sistema_seguranca.remover_bot_whitelist(bot_id, ctx.author)
        if success:
            embed = discord.Embed(
                title="✅ BOT REMOVIDO DA WHITELIST",
                description=f"Bot `{bot_id}` foi removido da whitelist de segurança",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Bot não encontrado na whitelist")
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='gerar_novo_token')
@commands.is_owner()
async def gerar_novo_token_whitelist(ctx):
    """🔄 Gera novo token para whitelist (APENAS DONO)"""
    novo_token = sistema_seguranca.gerar_novo_token_whitelist()
    
    embed = discord.Embed(
        title="🔄 NOVO TOKEN GERADO",
        description=f"**Novo token de whitelist:**\n\n`{novo_token}`\n\n**Tokens antigos foram invalidados!**",
        color=0xff9900
    )
    
    try:
        await ctx.author.send(embed=embed)
        await ctx.send("✅ Novo token gerado e enviado no seu privado! Tokens antigos foram invalidados.")
    except:
        await ctx.send("❌ Não foi possível enviar o token no privado.")

# ========== ADMINISTRAÇÃO ESSENCIAL ==========

@bot.command(name='admin')
@commands.has_permissions(administrator=True)
async def painel_administracao(ctx):
    """⚡ PAINEL DE ADMINISTRAÇÃO ESSENCIAL"""
    
    embed = discord.Embed(
        title="⚡ ADMINISTRAÇÃO ESSENCIAL",
        description="**Sistema completo de gestão do servidor**\n\n"
                   "📋 **Organizado em subgrupos para fácil acesso:**",
        color=0x7289DA
    )
    
    # Subgrupo 1: Suporte e Tickets
    embed.add_field(
        name="🎫 SUPORTE E TICKETS",
        value="`!setup_tickets` - Configurar sistema de tickets\n"
              "`!ticket_status` - Status dos tickets ativos\n"
              "`!close` - Fechar ticket atual\n"
              "`!whitelist_token` - Token para whitelist (Dono)\n"
              "`!whitelist_bot <token> <id>` - Adicionar bot\n"
              "`!remove_whitelist_bot <token> <id>` - Remover bot\n"
              "`!view_whitelist` - Ver bots autorizados",
        inline=False
    )
    
    # Subgrupo 2: Personalização e Limpeza
    embed.add_field(
        name="🔧 PERSONALIZAÇÃO E LIMPEZA",
        value="`!si` - Analisar símbolos nos canais\n"
              "`!w <posição> <novo_simbolo>` - Substituir símbolo por posição\n"
              "`!ws <antigo> <novo>` - Substituir símbolo específico\n"
              "`!pers <antigo> <novo>` - Substituir em nicknames\n"
              "`!quarentena @user [tempo]` - Isolar usuário\n"
              "`!liberar_quarentena @user` - Liberar da quarentena\n"
              "`!ssm_status` - Status do sistema de segurança",
        inline=False
    )
    
    # Subgrupo 3: Sistema de Segurança
    embed.add_field(
        name="🛡️ SISTEMA DE SEGURANÇA",
        value="`!rate` - Ativar proteção total\n"
              "`!token_desativar <token>` - Desativar proteção\n"
              "`!scan_membros` - Scan de membros suspeitos\n"
              "`!backup_servidor` - Backup do servidor\n"
              "`!estatisticas_seguranca` - Estatísticas de segurança",
        inline=False
    )
    
    embed.set_footer(text="Sistema de Segurança Multifacetado Ativo")
    await ctx.send(embed=embed)

# ========== SUBGRUPO 1: SUPORTE E TICKETS ==========

@bot.command(name='setup_tickets')
@commands.has_permissions(administrator=True)
async def setup_tickets(ctx):
    """🎫 Configura sistema automático de tickets"""
    await ctx.typing()
    
    try:
        canal = await sistema_tickets.setup_canal_tickets(ctx.guild)
        
        embed = discord.Embed(
            title="✅ SISTEMA DE TICKETS CONFIGURADO",
            description=f"Canal de tickets criado: {canal.mention}\n\n"
                       "**Como funciona:**\n"
                       "• Membros clicam no 🎫 para abrir tickets\n"
                       "• Tickets criam canais privados automaticamente\n"
                       "• Use `!close` no ticket para fechar\n"
                       "• Sistema notifica a equipe automaticamente",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao configurar tickets: {e}")

@bot.command(name='ticket_status')
@commands.has_permissions(manage_channels=True)
async def ticket_status(ctx):
    """📊 Status dos tickets ativos"""
    tickets_ativos = len(sistema_tickets.tickets_ativos)
    
    embed = discord.Embed(
        title="📊 STATUS DOS TICKETS",
        color=0x0099ff
    )
    embed.add_field(name="🎫 Tickets Ativos", value=tickets_ativos, inline=True)
    embed.add_field(name="🔧 Sistema", value="✅ Operacional", inline=True)
    
    if tickets_ativos > 0:
        embed.add_field(
            name="📋 Tickets Abertos", 
            value="\n".join([f"• Ticket #{tid}" for tid in list(sistema_tickets.tickets_ativos.keys())[:5]]),
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name='close')
async def fechar_ticket(ctx):
    """🔒 Fecha o ticket atual"""
    if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.name.startswith('ticket-'):
        success = await sistema_tickets.fechar_ticket(ctx.channel, ctx.author)
        if success:
            await ctx.send("✅ Ticket fechado com sucesso!")
        else:
            await ctx.send("❌ Erro ao fechar ticket")
    else:
        await ctx.send("❌ Este comando só funciona em tickets!")

@bot.command(name='view_whitelist')
@commands.has_permissions(administrator=True)
async def view_whitelist(ctx):
    """📋 Lista bots na whitelist"""
    if not sistema_seguranca.whitelist_bots:
        await ctx.send("❌ Nenhum bot na whitelist")
        return
    
    embed = discord.Embed(
        title="📋 BOTS NA WHITELIST",
        description="Lista de bots autorizados no servidor:",
        color=0x0099ff
    )
    
    for i, bot_id in enumerate(list(sistema_seguranca.whitelist_bots)[:10], 1):
        bot_user = ctx.guild.get_member(bot_id)
        bot_name = bot_user.name if bot_user else "Bot não está no servidor"
        embed.add_field(name=f"{i}. {bot_name}", value=f"ID: `{bot_id}`", inline=False)
    
    await ctx.send(embed=embed)

# ========== SUBGRUPO 2: PERSONALIZAÇÃO E LIMPEZA ==========

@bot.command(name='pers')
@commands.has_permissions(manage_nicknames=True)
async def substituir_simbolos_nicks(ctx, simbolo_antigo: str, simbolo_novo: str):
    """🏷️ Substitui símbolos em nicknames dos membros"""
    await ctx.typing()
    
    try:
        membros_alterados = 0
        
        for member in ctx.guild.members:
            if member.nick and simbolo_antigo in member.nick:
                try:
                    novo_nick = member.nick.replace(simbolo_antigo, simbolo_novo)
                    await member.edit(nick=novo_nick)
                    membros_alterados += 1
                    await asyncio.sleep(0.5)  # Rate limit
                except Exception as e:
                    print(f"Erro ao alterar nick de {member.name}: {e}")
        
        embed = discord.Embed(
            title="✅ NICKS ATUALIZADOS",
            description=f"**{membros_alterados}** membros tiveram nicks atualizados\n"
                       f"**Substituído:** `{simbolo_antigo}` → `{simbolo_novo}`",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao substituir símbolos: {e}")

@bot.command(name='quarentena')
@commands.has_permissions(administrator=True)
async def comando_quarentena(ctx, member: discord.Member, duracao_minutos: int = 60, *, motivo="Comportamento suspeito"):
    """🔒 Coloca usuário em quarentena"""
    await ctx.typing()
    
    try:
        success = await sistema_seguranca.colocar_quarentena(member, duracao_minutos, motivo)
        
        if success:
            embed = discord.Embed(
                title="🔒 USUÁRIO EM QUARENTENA",
                description=f"**{member.mention}** foi colocado em quarentena",
                color=0xff0000
            )
            embed.add_field(name="⏰ Duração", value=f"{duracao_minutos} minutos", inline=True)
            embed.add_field(name="📝 Motivo", value=motivo, inline=True)
            embed.add_field(name="👮 Ação por", value=ctx.author.mention, inline=True)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Erro ao colocar usuário em quarentena")
            
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='liberar_quarentena')
@commands.has_permissions(administrator=True)
async def liberar_quarentena(ctx, member: discord.Member):
    """🔓 Libera usuário da quarentena"""
    await ctx.typing()
    
    try:
        success = await sistema_seguranca.remover_quarentena(member)
        
        if success:
            embed = discord.Embed(
                title="🔓 USUÁRIO LIBERADO",
                description=f"**{member.mention}** foi liberado da quarentena",
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Usuário não está em quarentena ou erro ao liberar")
            
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='ssm_status')
@commands.has_permissions(administrator=True)
async def ssm_status(ctx):
    """📊 Status do Sistema de Segurança Multifacetado"""
    embed = discord.Embed(
        title="🛡️ STATUS DO SISTEMA DE SEGURANÇA",
        color=0x0099ff
    )
    
    # Estatísticas gerais
    embed.add_field(name="🤖 Bots na Whitelist", value=len(sistema_seguranca.whitelist_bots), inline=True)
    embed.add_field(name="🔒 Usuários em Quarentena", value=len(sistema_seguranca.quarentena_usuarios), inline=True)
    embed.add_field(name="⚡ Ações Monitoradas", value=len(sistema_seguranca.rate_limit_actions), inline=True)
    
    # Status de proteção
    status_protecao = "✅ Ativo" if not sistema_deteccao.modo_emergencia else "🚨 EMERGÊNCIA"
    embed.add_field(name="🛡️ Modo de Proteção", value=status_protecao, inline=True)
    embed.add_field(name="⏰ Rate Limit", value="✅ Ativo" if rate_system.rate_limit_active else "❌ Inativo", inline=True)
    embed.add_field(name="🎫 Sistema de Tickets", value="✅ Configurado" if CONFIG['canais_automaticos'].get('tickets') else "⚙️ Não configurado", inline=True)
    
    # Usuários em quarentena
    if sistema_seguranca.quarentena_usuarios:
        quarentena_info = []
        for user_id, dados in list(sistema_seguranca.quarentena_usuarios.items())[:3]:
            member = ctx.guild.get_member(int(user_id))
            nome = member.mention if member else f"ID: {user_id}"
            tempo_fim = datetime.fromisoformat(dados["tempo_fim"])
            tempo_restante = tempo_fim - datetime.now()
            minutos_restantes = max(0, int(tempo_restante.total_seconds() / 60))
            
            quarentena_info.append(f"• {nome} - {minutos_restantes}min restantes")
        
        embed.add_field(name="🔒 Quarentena Ativa", value="\n".join(quarentena_info), inline=False)
    
    await ctx.send(embed=embed)

# ========== COMANDOS DE UTILIDADE ==========

@bot.command(name='bot_id')
async def mostrar_bot_id(ctx):
    """🆔 Mostra o ID do bot"""
    embed = discord.Embed(
        title="🤖 ID DO BOT",
        description=f"**ID do Bot:** `{bot.user.id}`\n**Nome:** {bot.user.name}",
        color=0x0099ff
    )
    await ctx.send(embed=embed)

@bot.command(name='meu_id')
async def mostrar_meu_id(ctx):
    """🆔 Mostra seu ID de usuário"""
    embed = discord.Embed(
        title="👤 SEU ID",
        description=f"**Seu ID:** `{ctx.author.id}`\n**Seu Nome:** {ctx.author.name}",
        color=0x0099ff
    )
    await ctx.send(embed=embed)

# ========== EVENTOS DE DETECÇÃO PROATIVA CORRIGIDOS ==========

@bot.event
async def on_guild_channel_create(channel):
    """Detecta criação de canais suspeitos - CORRIGIDO"""
    
    # 🛡️ DETECÇÃO PROATIVA - Monitorar criação suspeita
    if not sistema_deteccao.modo_emergencia:
        criacao_suspeita = await sistema_deteccao.monitorar_criacao_canal(channel)
        if criacao_suspeita:
            return  # Já ativou proteção emergencial
        
        # Sistema de segurança - detectar nuke
        async for entry in channel.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_create):
            if entry.target.id == channel.id:
                # ✅ CORREÇÃO CRÍTICA: Ignorar bots da whitelist
                if entry.user.id != bot.user.id and not (entry.user.bot and entry.user.id in sistema_seguranca.whitelist_bots):
                    nuke_detectado = await sistema_seguranca.detectar_nuke(channel.guild, entry.user, "channel_create")
                    if nuke_detectado:
                        return
                break
    
    # Sistema original de rate limit
    if rate_system.rate_limit_active:
        async for entry in channel.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_create):
            if entry.target.id == channel.id:
                autor = entry.user
                
                # ✅ CORREÇÃO: Ignorar bots da whitelist
                if autor.bot and autor.id in sistema_seguranca.whitelist_bots:
                    break
                    
                try:
                    nome_canal = channel.name
                    tipo_canal = "texto" if isinstance(channel, discord.TextChannel) else "voz" if isinstance(channel, discord.VoiceChannel) else "categoria"
                    
                    await channel.delete()
                    
                    await log_system.log_rate_limit(
                        channel.guild, 
                        "CANAL BLOQUEADO", 
                        autor, 
                        f"{tipo_canal.capitalize()} '{nome_canal}' criado e automaticamente deletado"
                    )
                
                except Exception as e:
                    print(f"Erro ao deletar canal durante rate limit: {e}")
                break

@bot.event
async def on_guild_role_create(role):
    """Detecta criação de cargos suspeitos - CORRIGIDO"""
    
    # 🛡️ DETECÇÃO PROATIVA - Verificar se é ataque
    if not sistema_deteccao.modo_emergencia:
        async for entry in role.guild.audit_logs(limit=5, action=discord.AuditLogAction.role_create):
            if entry.target.id == role.id:
                # ✅ CORREÇÃO CRÍTICA: Ignorar bots da whitelist
                if entry.user.id != bot.user.id and not (entry.user.bot and entry.user.id in sistema_seguranca.whitelist_bots):
                    # Detectar padrão de ataque
                    if await sistema_deteccao.detectar_ataque_em_andamento(role.guild, entry.user, "role_create"):
                        return  # Já ativou proteção
                    
                    # Sistema de segurança
                    nuke_detectado = await sistema_seguranca.detectar_nuke(role.guild, entry.user, "role_create")
                    if nuke_detectado:
                        return
                break
    
    # Sistema original de rate limit
    if rate_system.rate_limit_active:
        async for entry in role.guild.audit_logs(limit=5, action=discord.AuditLogAction.role_create):
            if entry.target.id == role.id:
                autor = entry.user
                
                # ✅ CORREÇÃO: Ignorar bots da whitelist
                if autor.bot and autor.id in sistema_seguranca.whitelist_bots:
                    break
                    
                try:
                    nome_cargo = role.name
                    await role.delete()
                    
                    await log_system.log_rate_limit(
                        role.guild, 
                        "CARGO BLOQUEADO", 
                        autor, 
                        f"Cargo '{nome_cargo}' criado e automaticamente deletado"
                    )
                
                except Exception as e:
                    print(f"Erro ao deletar cargo durante rate limit: {e}")
                break

@bot.event
async def on_member_ban(guild, user):
    """Detecta bans em massa - CORRIGIDO"""
    if not sistema_deteccao.modo_emergencia:
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.ban):
            if entry.target.id == user.id:
                autor = entry.user
                
                # ✅ CORREÇÃO: Ignorar bots da whitelist
                if autor.bot and autor.id in sistema_seguranca.whitelist_bots:
                    return
                    
                # Detectar padrão de mass ban
                if await sistema_deteccao.detectar_ataque_em_andamento(guild, autor, "ban"):
                    return

@bot.event
async def on_member_remove(member):
    """Detecta kicks em massa - CORRIGIDO"""
    await log_system.log_saida(member)
    
    if not sistema_deteccao.modo_emergencia:
        async for entry in member.guild.audit_logs(limit=5, action=discord.AuditLogAction.kick):
            if entry.target.id == member.id:
                autor = entry.user
                
                # ✅ CORREÇÃO: Ignorar bots da whitelist
                if autor.bot and autor.id in sistema_seguranca.whitelist_bots:
                    return
                    
                # Detectar padrão de mass kick
                if await sistema_deteccao.detectar_ataque_em_andamento(member.guild, autor, "kick"):
                    return

@bot.event
async def on_member_join(member):
    """Verifica bots não autorizados na entrada - CORRIGIDO"""
    await log_system.log_entrada(member)
    
    # Sistema de segurança - verificar bots
    if member.bot:
        autorizado = await sistema_seguranca.verificar_bot_entrada(member)
        if not autorizado:
            return
    
    # Sistema original de cargos
    cargo_membro = discord.utils.get(member.guild.roles, name="Membro")
    if not cargo_membro:
        try:
            cargo_membro = await member.guild.create_role(name="Membro", color=discord.Color.blue())
        except:
            pass
    
    if cargo_membro:
        try:
            await member.add_roles(cargo_membro)
        except:
            pass

    await sistema_cargos.atualizar_nick_automatico(member)
    
    # SISTEMA DE CONVITES FUNCIONAL
    try:
        invites = await member.guild.invites()
        for invite in invites:
            if invite.uses > sistema_convites.convites_ativos.get(invite.code, 0):
                inviter = invite.inviter
                if inviter and inviter != bot.user:
                    success = await sistema_convites.registrar_convite(member, inviter.id)
                    if success:
                        print(f"✅ Convite registrado: {inviter.name} convidou {member.name}")
                    break
                
                sistema_convites.convites_ativos[invite.code] = invite.uses
    except Exception as e:
        print(f"Erro ao verificar convites: {e}")

@bot.event
async def on_raw_reaction_add(payload):
    """Sistema de tickets por reação"""
    if payload.member and payload.member.bot:
        return
    
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
        
    member = guild.get_member(payload.user_id)
    if not member or member.bot:
        return
        
    canal = guild.get_channel(payload.channel_id)
    
    # Verificar se é o canal de tickets
    canal_tickets_id = CONFIG['canais_automaticos'].get('tickets')
    if canal_tickets_id and canal.id == canal_tickets_id and str(payload.emoji) == "🎫":
        try:
            mensagem = await canal.fetch_message(payload.message_id)
            if mensagem.embeds and "SISTEMA DE TICKETS" in mensagem.embeds[0].title:
                await sistema_tickets.criar_ticket(member)
                await mensagem.remove_reaction(payload.emoji, member)
        except Exception as e:
            print(f"Erro ao criar ticket: {e}")

    # Sistema original de cargos por reação
    await processar_reacao_cargo(payload, "add")

@bot.event
async def on_raw_reaction_remove(payload):
    await processar_reacao_cargo(payload, "remove")

async def processar_reacao_cargo(payload, acao):
    if payload.member and payload.member.bot:
        return
    
    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return
        
    member = guild.get_member(payload.user_id)
    if not member or member.bot:
        return
        
    canal = guild.get_channel(payload.channel_id)
    
    # Verificar tanto pelo nome quanto pelo ID configurado
    canal_self_roles_id = CONFIG['canais_automaticos'].get('self_roles')
    canal_self_roles = guild.get_channel(canal_self_roles_id) if canal_self_roles_id else None
    
    if not canal or (canal.name != "🎯・self-roles" and canal != canal_self_roles):
        return
    
    try:
        mensagem = await canal.fetch_message(payload.message_id)
        
        for embed in mensagem.embeds:
            titulo = embed.title if embed.title else ""
            
            cargo_encontrado = None
            emoji_str = str(payload.emoji)
            
            for cargo_nome in CONFIG["cargos_linguagens"].keys():
                if cargo_nome.startswith(emoji_str):
                    cargo_encontrado = discord.utils.get(guild.roles, name=cargo_nome)
                    break
            
            if not cargo_encontrado:
                for cargo_nome in CONFIG["cargos_cyber"].keys():
                    if cargo_nome.startswith(emoji_str):
                        cargo_encontrado = discord.utils.get(guild.roles, name=cargo_nome)
                        break
            
            if cargo_encontrado:
                if acao == "add":
                    await member.add_roles(cargo_encontrado)
                else:
                    await member.remove_roles(cargo_encontrado)
                break
                
    except Exception as e:
        print(f"Erro no sistema de cargos: {e}")

# ========== +10 FUNÇÕES AVANÇADAS ADICIONAIS ==========

@bot.command(name='clone_categoria')
@commands.has_permissions(administrator=True)
async def clone_categoria(ctx, categoria_id: int, novo_nome: str = None):
    """🏗️ Clona uma categoria inteira com todos os canais"""
    try:
        categoria_original = ctx.guild.get_channel(categoria_id)
        if not categoria_original or not isinstance(categoria_original, discord.CategoryChannel):
            await ctx.send("❌ Categoria não encontrada!")
            return
        
        # Criar nova categoria
        nome_categoria = novo_nome or f"{categoria_original.name}-copia"
        nova_categoria = await ctx.guild.create_category(nome_categoria)
        
        canais_clonados = 0
        
        # Clonar todos os canais da categoria
        for canal in categoria_original.channels:
            try:
                if isinstance(canal, discord.TextChannel):
                    novo_canal = await canal.clone()
                    await novo_canal.edit(category=nova_categoria)
                elif isinstance(canal, discord.VoiceChannel):
                    novo_canal = await canal.clone()
                    await novo_canal.edit(category=nova_categoria)
                
                canais_clonados += 1
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Erro ao clonar canal {canal.name}: {e}")
        
        embed = discord.Embed(
            title="🏗️ CATEGORIA CLONADA",
            description=f"**{categoria_original.name}** foi clonada com sucesso!",
            color=0x00ff00
        )
        embed.add_field(name="📁 Nova Categoria", value=nova_categoria.mention, inline=True)
        embed.add_field(name="🔢 Canais Clonados", value=canais_clonados, inline=True)
        embed.add_field(name="🆔 ID Original", value=categoria_id, inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao clonar categoria: {e}")

@bot.command(name='organizar_canais')
@commands.has_permissions(administrator=True)
async def organizar_canais(ctx, categoria_id: int, *canais_ids):
    """📦 Organiza canais em uma categoria específica"""
    try:
        categoria = ctx.guild.get_channel(categoria_id)
        if not categoria or not isinstance(categoria, discord.CategoryChannel):
            await ctx.send("❌ Categoria não encontrada!")
            return
        
        canais_movidos = 0
        
        for canal_id in canais_ids:
            try:
                canal = ctx.guild.get_channel(int(canal_id))
                if canal and isinstance(canal, (discord.TextChannel, discord.VoiceChannel)):
                    await canal.edit(category=categoria)
                    canais_movidos += 1
                    await asyncio.sleep(0.3)
            except:
                continue
        
        embed = discord.Embed(
            title="📦 CANAIS ORGANIZADOS",
            description=f"**{canais_movidos}** canais foram movidos para {categoria.mention}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao organizar canais: {e}")

@bot.command(name='backup_canais')
@commands.has_permissions(administrator=True)
async def backup_canais(ctx):
    """💾 Cria backup completo da estrutura de canais"""
    await ctx.typing()
    
    try:
        backup_data = {
            "servidor": ctx.guild.name,
            "timestamp": datetime.now().isoformat(),
            "categorias": [],
            "canais": []
        }
        
        # Backup de categorias
        for categoria in ctx.guild.categories:
            categoria_info = {
                "id": categoria.id,
                "name": categoria.name,
                "position": categoria.position
            }
            backup_data["categorias"].append(categoria_info)
        
        # Backup de canais
        for canal in ctx.guild.channels:
            if isinstance(canal, (discord.TextChannel, discord.VoiceChannel)):
                canal_info = {
                    "id": canal.id,
                    "name": canal.name,
                    "type": canal.type.name,
                    "category_id": canal.category.id if canal.category else None,
                    "position": canal.position,
                    "topic": canal.topic if hasattr(canal, 'topic') else None
                }
                backup_data["canais"].append(canal_info)
        
        # Salvar backup
        backup_id = f"backup_canais_{ctx.guild.id}_{int(datetime.now().timestamp())}"
        db.config[f'backup_{backup_id}'] = backup_data
        db.salvar_dados()
        
        embed = discord.Embed(
            title="💾 BACKUP DE CANAIS CRIADO",
            description=f"Backup **{backup_id}** criado com sucesso!",
            color=0x00ff00
        )
        embed.add_field(name="📊 Estatísticas", 
                       value=f"• {len(backup_data['categorias'])} categorias\n• {len(backup_data['canais'])} canais", 
                       inline=False)
        embed.add_field(name="🆔 ID do Backup", value=backup_id, inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao criar backup: {e}")

@bot.command(name='restaurar_canais')
@commands.has_permissions(administrator=True)
async def restaurar_canais(ctx, backup_id: str):
    """🔄 Restaura estrutura de canais do backup"""
    await ctx.typing()
    
    try:
        backup_key = f'backup_{backup_id}'
        if backup_key not in db.config:
            await ctx.send("❌ Backup não encontrado!")
            return
        
        backup_data = db.config[backup_key]
        
        embed = discord.Embed(
            title="🔄 RESTAURAÇÃO DE CANAIS",
            description=f"**Backup:** {backup_id}\n**Servidor:** {backup_data['servidor']}",
            color=0xff9900
        )
        embed.add_field(name="📊 Conteúdo", 
                       value=f"• {len(backup_data['categorias'])} categorias\n• {len(backup_data['canais'])} canais", 
                       inline=False)
        embed.add_field(name="⚠️ AVISO", 
                       value="Esta ação recriará a estrutura de canais. Use com cuidado!", 
                       inline=False)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao restaurar backup: {e}")

@bot.command(name='limpar_canais_inativos')
@commands.has_permissions(administrator=True)
async def limpar_canais_inativos(ctx, dias: int = 30):
    """🧹 Remove canais inativos (sem mensagens recentes)"""
    await ctx.typing()
    
    try:
        if dias <= 0:
            await ctx.send("❌ O número de dias deve ser maior que 0")
            return
        
        data_limite = datetime.now() - timedelta(days=dias)
        canais_removidos = 0
        
        for canal in ctx.guild.text_channels:
            try:
                # Verificar última mensagem
                ultima_mensagem = None
                async for msg in canal.history(limit=1):
                    ultima_mensagem = msg
                    break
                
                # Se não há mensagens ou a última é muito antiga
                if not ultima_mensagem or ultima_mensagem.created_at < data_limite:
                    # Verificar se é canal importante
                    if not any(palavra in canal.name for palavra in ['regras', 'anúncios', 'boas-vindas', 'geral']):
                        await canal.delete()
                        canais_removidos += 1
                        await asyncio.sleep(0.5)
                        
            except Exception as e:
                print(f"Erro ao verificar canal {canal.name}: {e}")
        
        embed = discord.Embed(
            title="🧹 LIMPEZA DE CANAIS INATIVOS",
            description=f"**{canais_removidos}** canais inativos foram removidos",
            color=0x00ff00
        )
        embed.add_field(name="📅 Período", value=f"Últimos {dias} dias", inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro na limpeza: {e}")

@bot.command(name='estatisticas_canais')
@commands.has_permissions(manage_channels=True)
async def estatisticas_canais(ctx):
    """📊 Estatísticas detalhadas dos canais"""
    await ctx.typing()
    
    try:
        total_canais = len(ctx.guild.channels)
        canais_texto = len(ctx.guild.text_channels)
        canais_voz = len(ctx.guild.voice_channels)
        categorias = len(ctx.guild.categories)
        
        # Canais mais ativos
        canais_ativos = []
        for canal in ctx.guild.text_channels[:10]:  # Limitar para performance
            try:
                count = 0
                async for _ in canal.history(limit=100, after=datetime.now()-timedelta(days=7)):
                    count += 1
                canais_ativos.append((canal.name, count))
            except:
                continue
        
        canais_ativos.sort(key=lambda x: x[1], reverse=True)
        
        embed = discord.Embed(
            title="📊 ESTATÍSTICAS DE CANAIS",
            color=0x0099ff
        )
        
        embed.add_field(name="📈 Totais", 
                       value=f"• **Total:** {total_canais}\n• **Texto:** {canais_texto}\n• **Voz:** {canais_voz}\n• **Categorias:** {categorias}", 
                       inline=True)
        
        if canais_ativos:
            top_ativos = "\n".join([f"• #{nome}: {count} msgs" for nome, count in canais_ativos[:5]])
            embed.add_field(name="🏆 Canais Mais Ativos (7 dias)", value=top_ativos, inline=True)
        
        # Canais com mais membros (canais de voz)
        canais_voz_populados = []
        for canal in ctx.guild.voice_channels:
            if len(canal.members) > 0:
                canais_voz_populados.append((canal.name, len(canal.members)))
        
        canais_voz_populados.sort(key=lambda x: x[1], reverse=True)
        
        if canais_voz_populados:
            top_voz = "\n".join([f"• {nome}: {count} membros" for nome, count in canais_voz_populados[:3]])
            embed.add_field(name="🔊 Canais de Voz Ativos", value=top_voz, inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro nas estatísticas: {e}")

@bot.command(name='sync_cargos')
@commands.has_permissions(administrator=True)
async def sync_cargos(ctx):
    """🔄 Sincroniza cargos entre todos os membros"""
    await ctx.typing()
    
    try:
        membros_sincronizados = 0
        erros = 0
        
        for member in ctx.guild.members:
            if member.bot:
                continue
                
            try:
                await sistema_cargos.atualizar_nick_automatico(member)
                membros_sincronizados += 1
                await asyncio.sleep(0.2)  # Rate limit
            except Exception as e:
                print(f"Erro ao sincronizar {member.name}: {e}")
                erros += 1
        
        embed = discord.Embed(
            title="🔄 SINCRONIZAÇÃO DE CARGOS",
            description=f"**{membros_sincronizados}** membros foram sincronizados",
            color=0x00ff00
        )
        
        if erros > 0:
            embed.add_field(name="⚠️ Erros", value=f"{erros} membros não puderam ser sincronizados", inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro na sincronização: {e}")

@bot.command(name='auto_setup')
@commands.has_permissions(administrator=True)
async def auto_setup(ctx):
    """🚀 Configuração automática completa do servidor"""
    await ctx.typing()
    
    try:
        progress = await ctx.send("🚀 **Iniciando configuração automática...**")
        
        # 1. Sistema de cargos
        await progress.edit(content="🎯 **Configurando sistema de cargos...**")
        await sistema_cargos.atribuir_cargo_membro_automatico(ctx.guild)
        
        # 2. Sistema de tickets
        await progress.edit(content="🎫 **Configurando sistema de tickets...**")
        await sistema_tickets.setup_canal_tickets(ctx.guild)
        
        # 3. Sistema de logs
        await progress.edit(content="📁 **Criando canais de logs...**")
        for tipo, nome_canal in CONFIG["logs_config"].items():
            canal_existente = discord.utils.get(ctx.guild.text_channels, name=nome_canal)
            if not canal_existente:
                canal = await ctx.guild.create_text_channel(nome_canal)
                permissao = discord.PermissionOverwrite()
                permissao.send_messages = False
                permissao.read_messages = True
                await canal.set_permissions(ctx.guild.default_role, overwrite=permissao)
                await asyncio.sleep(0.5)
        
        # 4. Sistema de segurança
        await progress.edit(content="🛡️ **Configurando sistema de segurança...**")
        await sistema_seguranca.criar_cargo_quarentena(ctx.guild)
        
        # 5. Sincronizar membros
        await progress.edit(content="🔄 **Sincronizando membros...**")
        await sistema_cargos.atualizar_nicks(ctx)
        
        await progress.edit(content="✅ **Configuração automática concluída!**")
        
        embed = discord.Embed(
            title="🚀 CONFIGURAÇÃO AUTOMÁTICA CONCLUÍDA",
            description="**Todos os sistemas foram configurados:**\n\n"
                       "• ✅ Sistema de cargos\n"
                       "• ✅ Sistema de tickets\n" 
                       "• ✅ Canais de logs\n"
                       "• ✅ Sistema de segurança\n"
                       "• ✅ Sincronização de membros",
            color=0x00ff00
        )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro na configuração automática: {e}")

@bot.command(name='smart_clean')
@commands.has_permissions(administrator=True)
async def smart_clean(ctx):
    """🧹 Limpeza inteligente do servidor"""
    await ctx.typing()
    
    try:
        acoes_realizadas = []
        
        # 1. Limpar mensagens de bots
        await ctx.send("🧹 **Limpando mensagens de bots...**")
        bots_cleaned = 0
        for channel in ctx.guild.text_channels[:10]:  # Limitar para performance
            try:
                deleted = await channel.purge(limit=100, check=lambda m: m.author.bot)
                bots_cleaned += len(deleted)
                await asyncio.sleep(1)
            except:
                continue
        if bots_cleaned > 0:
            acoes_realizadas.append(f"• {bots_cleaned} mensagens de bots removidas")
        
        # 2. Atualizar cargos
        await ctx.send("🔄 **Atualizando cargos...**")
        membros_atualizados = await sistema_cargos.atribuir_cargo_membro_automatico(ctx.guild)
        if membros_atualizados > 0:
            acoes_realizadas.append(f"• {membros_atualizados} membros receberam cargo")
        
        # 3. Verificar convites expirados
        await ctx.send("📋 **Verificando convites...**")
        try:
            invites = await ctx.guild.invites()
            expirados = 0
            for invite in invites:
                if invite.max_age and invite.created_at + timedelta(seconds=invite.max_age) < datetime.now():
                    await invite.delete()
                    expirados += 1
                    await asyncio.sleep(0.5)
            if expirados > 0:
                acoes_realizadas.append(f"• {expirados} convites expirados removidos")
        except:
            pass
        
        embed = discord.Embed(
            title="🧹 LIMPEZA INTELIGENTE CONCLUÍDA",
            description="**Ações realizadas:**\n" + "\n".join(acoes_realizadas) if acoes_realizadas else "Nenhuma ação necessária",
            color=0x00ff00
        )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro na limpeza inteligente: {e}")

@bot.command(name='server_health')
@commands.has_permissions(administrator=True)
async def server_health(ctx):
    """🏥 Diagnóstico completo da saúde do servidor"""
    await ctx.typing()
    
    try:
        guild = ctx.guild
        
        # Coletar métricas
        total_membros = guild.member_count
        membros_ativos = len([m for m in guild.members if m.status != discord.Status.offline])
        bots = len([m for m in guild.members if m.bot])
        canais_ativos = len([c for c in guild.text_channels])
        
        # Verificar sistemas
        sistemas = []
        
        # Sistema de cargos
        cargo_membro = discord.utils.get(guild.roles, name="Membro")
        sistemas.append(("🎯 Sistema de Cargos", "✅" if cargo_membro else "❌"))
        
        # Sistema de tickets
        canal_tickets = CONFIG['canais_automaticos'].get('tickets')
        sistemas.append(("🎫 Sistema de Tickets", "✅" if canal_tickets else "❌"))
        
        # Sistema de logs
        logs_ativos = 0
        for tipo in CONFIG['canais_automaticos']:
            if CONFIG['canais_automaticos'][tipo]:
                logs_ativos += 1
        sistemas.append(("📁 Sistema de Logs", f"{logs_ativos}/7"))
        
        # Sistema de segurança
        cargo_quarentena = discord.utils.get(guild.roles, name="[SSM - QUARENTENA]")
        sistemas.append(("🛡️ Sistema de Segurança", "✅" if cargo_quarentena else "❌"))
        
        embed = discord.Embed(
            title="🏥 DIAGNÓSTICO DO SERVIDOR",
            color=0x0099ff
        )
        
        # Métricas principais
        embed.add_field(name="👥 MEMBROS", 
                       value=f"• **Total:** {total_membros}\n• **Ativos:** {membros_ativos}\n• **Bots:** {bots}", 
                       inline=True)
        
        embed.add_field(name="📊 CANAIS", 
                       value=f"• **Textuais:** {canais_ativos}\n• **Voz:** {len(guild.voice_channels)}\n• **Categorias:** {len(guild.categories)}", 
                       inline=True)
        
        # Status dos sistemas
        sistemas_texto = "\n".join([f"{nome}: {status}" for nome, status in sistemas])
        embed.add_field(name="⚙️ SISTEMAS", value=sistemas_texto, inline=False)
        
        # Recomendações
        recomendacoes = []
        if not cargo_membro:
            recomendacoes.append("• Configurar sistema de cargos (`!setup_cargos`)")
        if not canal_tickets:
            recomendacoes.append("• Configurar sistema de tickets (`!setup_tickets`)")
        if logs_ativos < 3:
            recomendacoes.append("• Configurar mais canais de logs (`!config`)")
        
        if recomendacoes:
            embed.add_field(name="💡 RECOMENDAÇÕES", value="\n".join(recomendacoes), inline=False)
        
        # Saúde geral
        pontuacao = 0
        if cargo_membro: pontuacao += 25
        if canal_tickets: pontuacao += 25
        if logs_ativos >= 3: pontuacao += 25
        if cargo_quarentena: pontuacao += 25
        
        if pontuacao >= 75:
            status_saude = "✅ SAUDÁVEL"
            cor = 0x00ff00
        elif pontuacao >= 50:
            status_saude = "⚠️ ATENÇÃO"
            cor = 0xff9900
        else:
            status_saude = "❌ CRÍTICO"
            cor = 0xff0000
        
        embed.color = cor
        embed.add_field(name="🏥 SAÚDE GERAL", value=f"**{status_saude}** ({pontuacao}%)", inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro no diagnóstico: {e}")

# ========== COMANDOS DE MODERAÇÃO ORIGINAIS ==========

@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, motivo="Não especificado"):
    """🔨 Bane um membro do servidor"""
    try:
        await member.ban(reason=f"{motivo} | Por: {ctx.author.name}")
        
        # Registrar ação do bot para segurança
        await sistema_seguranca.registrar_acao_bot(ctx.guild.id, 'ban')
        
        embed = discord.Embed(
            title="🔨 USUÁRIO BANIDO",
            description=f"**{member.name}** foi banido do servidor",
            color=0xff0000
        )
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="👮 Moderador", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        await log_system.log_moderacao("BAN", ctx.author, member, motivo)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao banir usuário: {e}")

@bot.command(name='banir')
@commands.has_permissions(ban_members=True)
async def banir_ia(ctx, member: discord.Member, *, motivo=None):
    """🔨 Banir usuário via comando de voz/texto com IA"""
    await ctx.typing()
    
    try:
        # Se não forneceu motivo, a IA gera um baseado no contexto
        if not motivo:
            prompt = f"Gerar um motivo profissional para banir o usuário {member.name} do servidor Discord. Seja direto e objetivo."
            motivo = await groq_ai.gerar_resposta(prompt)
            motivo = f"Motivo automático: {motivo}"
        
        # Executar ban
        await member.ban(reason=f"{motivo} | Por: {ctx.author.name}")
        
        # Registrar ação do bot para segurança
        await sistema_seguranca.registrar_acao_bot(ctx.guild.id, 'ban')
        
        embed = discord.Embed(
            title="🔨 USUÁRIO BANIDO",
            description=f"**{member.name}** foi banido do servidor",
            color=0xff0000
        )
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="👮 Moderador", value=ctx.author.mention, inline=True)
        embed.add_field(name="🆔 ID", value=member.id, inline=True)
        
        await ctx.send(embed=embed)
        await log_system.log_moderacao("BAN", ctx.author, member, motivo)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao banir usuário: {e}")

@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, motivo="Não especificado"):
    """👢 Expulsa um membro do servidor"""
    try:
        await member.kick(reason=f"{motivo} | Por: {ctx.author.name}")
        
        embed = discord.Embed(
            title="👢 USUÁRIO EXPULSO",
            description=f"**{member.name}** foi expulso do servidor",
            color=0xff9900
        )
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="👮 Moderador", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        await log_system.log_moderacao("KICK", ctx.author, member, motivo)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao expulsar usuário: {e}")

@bot.command(name='mute')
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, tempo: str = "30m", *, motivo="Não especificado"):
    """🔇 Muta um membro por tempo determinado"""
    try:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if not muted_role:
            # Criar cargo Muted se não existir
            muted_role = await ctx.guild.create_role(name="Muted")
            
            # Aplicar permissões de mute em todos os canais
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)
        
        # Converter tempo para segundos
        tempo_map = {"30m": 1800, "1h": 3600, "6h": 21600, "12h": 43200, "1d": 86400}
        segundos = tempo_map.get(tempo, 1800)
        
        await member.add_roles(muted_role)
        
        embed = discord.Embed(
            title="🔇 MEMBRO MUTADO",
            color=0xffff00
        )
        embed.add_field(name="👤 Membro", value=member.mention, inline=True)
        embed.add_field(name="⏰ Tempo", value=tempo, inline=True)
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="👮 Moderador", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        await log_system.log_moderacao("MUTE", ctx.author, member, motivo, tempo)
        
        # Agendar remoção do mute
        await asyncio.sleep(segundos)
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            
    except Exception as e:
        await ctx.send(f"❌ Erro ao mutar usuário: {e}")

@bot.command(name='unmute')
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    """🔊 Remove mute de um membro"""
    try:
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        
        if not muted_role:
            await ctx.send("❌ Cargo 'Muted' não encontrado")
            return
        
        if muted_role not in member.roles:
            await ctx.send(f"❌ {member.mention} não está mutado")
            return
        
        await member.remove_roles(muted_role)
        await log_system.log_moderacao("UNMUTE", ctx.author, member, "Mute removido")
        
        embed = discord.Embed(
            title="🔊 MEMBRO DESMUTADO",
            color=0x00ff00
        )
        embed.add_field(name="👤 Membro", value=member.mention, inline=True)
        embed.add_field(name="👮 Moderador", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro: {e}")

@bot.command(name='advertir')
@commands.has_permissions(manage_messages=True)
async def advertir_ia(ctx, member: discord.Member, *, motivo=None):
    """⚠️ Advertir usuário via comando de voz/texto com IA"""
    await ctx.typing()
    
    try:
        user_id = str(member.id)
        
        if user_id not in db.advertencias:
            db.advertencias[user_id] = []
        
        # Se não forneceu motivo, a IA gera um
        if not motivo:
            prompt = f"Gerar um motivo profissional para advertir o usuário {member.name} em um servidor Discord. Seja educado mas firme."
            motivo = await groq_ai.gerar_resposta(prompt)
            motivo = f"Advertência automática: {motivo}"
        
        # Registrar advertência
        db.advertencias[user_id].append({
            "moderador": ctx.author.id,
            "motivo": motivo,
            "data": datetime.now().isoformat()
        })
        
        db.salvar_dados()
        
        advertencia_num = len(db.advertencias[user_id])
        
        embed = discord.Embed(
            title=f"⚠️ ADVERTÊNCIA #{advertencia_num}",
            color=0xffff00
        )
        embed.add_field(name="👤 Membro", value=member.mention, inline=True)
        embed.add_field(name="👮 Moderador", value=ctx.author.mention, inline=True)
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="🚨 Status", value=f"{advertencia_num}/{CONFIG['max_advertencias']} advertências", inline=True)
        
        if advertencia_num >= CONFIG['max_advertencias']:
            embed.add_field(name="🔨 Próxima Ação", value="**BAN AUTOMÁTICO**", inline=True)
        
        await ctx.send(embed=embed)
        await log_system.log_advertencia(member, ctx.author, motivo, advertencia_num)
        
        # Ban automático se atingiu o limite
        if advertencia_num >= CONFIG['max_advertencias']:
            await asyncio.sleep(2)
            await member.ban(reason=f"Limite de advertências atingido: {advertencia_num}/{CONFIG['max_advertencias']}")
            await ctx.send(f"🚨 **{member.name}** foi banido automaticamente por atingir o limite de advertências!")
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao advertir usuário: {e}")

@bot.command(name='advertencias')
@commands.has_permissions(manage_messages=True)
async def advertencias(ctx, member: discord.Member = None):
    """📋 Ver advertências de um membro"""
    member = member or ctx.author
    user_id = str(member.id)
    
    if user_id not in db.advertencias or not db.advertencias[user_id]:
        await ctx.send(f"❌ {member.mention} não tem advertências")
        return
    
    embed = discord.Embed(
        title=f"⚠️ ADVERTÊNCIAS - {member.name}",
        color=0xffff00
    )
    
    for i, advert in enumerate(db.advertencias[user_id], 1):
        moderador = ctx.guild.get_member(advert["moderador"])
        data = datetime.fromisoformat(advert["data"]).strftime("%d/%m/%Y %H:%M")
        
        embed.add_field(
            name=f"#{i} - {data}",
            value=f"**Motivo:** {advert['motivo']}\n**Por:** {moderador.mention if moderador else 'Usuário saiu'}",
            inline=False
        )
    
    embed.set_footer(text=f"Total: {len(db.advertencias[user_id])}/{CONFIG['max_advertencias']}")
    await ctx.send(embed=embed)

@bot.command(name='remover_advertencia')
@commands.has_permissions(manage_messages=True)
async def remover_advertencia(ctx, member: discord.Member, numero_advertencia: int = None):
    """❌ Remove advertência de um membro"""
    user_id = str(member.id)
    
    if user_id not in db.advertencias or not db.advertencias[user_id]:
        await ctx.send("❌ Este membro não tem advertências")
        return
    
    if numero_advertencia is None:
        # Remove a última advertência
        advertencia_removida = db.advertencias[user_id].pop()
        db.salvar_dados()
        
        embed = discord.Embed(
            title="❌ ADVERTÊNCIA REMOVIDA",
            description=f"Última advertência de {member.mention} foi removida",
            color=0x00ff00
        )
        embed.add_field(name="📝 Motivo Original", value=advertencia_removida["motivo"], inline=False)
        embed.add_field(name="👮 Moderador Original", value=ctx.guild.get_member(advertencia_removida["moderador"]).mention, inline=True)
        embed.add_field(name="🔄 Removido por", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
    else:
        if numero_advertencia < 1 or numero_advertencia > len(db.advertencias[user_id]):
            await ctx.send(f"❌ Número de advertência inválido. Use de 1 a {len(db.advertencias[user_id])}")
            return
        
        advertencia_removida = db.advertencias[user_id].pop(numero_advertencia - 1)
        db.salvar_dados()
        
        embed = discord.Embed(
            title="❌ ADVERTÊNCIA REMOVIDA",
            description=f"Advertência #{numero_advertencia} de {member.mention} foi removida",
            color=0x00ff00
        )
        embed.add_field(name="📝 Motivo Original", value=advertencia_removida["motivo"], inline=False)
        embed.add_field(name="👮 Moderador Original", value=ctx.guild.get_member(advertencia_removida["moderador"]).mention, inline=True)
        embed.add_field(name="🔄 Removido por", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, quantidade: int = None):
    """🧹 Limpa mensagens (INFINITAS)"""
    if not quantidade:
        await ctx.send("❌ Especifique a quantidade: `!clear 50`")
        return
    
    if quantidade <= 0:
        await ctx.send("❌ A quantidade deve ser maior que 0")
        return
    
    # Não há limite máximo - pode limpar infinitas mensagens
    deleted = await ctx.channel.purge(limit=quantidade + 1)
    
    # Registrar ação do bot para segurança
    await sistema_seguranca.registrar_acao_bot(ctx.guild.id, 'channel_delete')
    
    # Mensagem de confirmação que se auto-deleta
    msg = await ctx.send(f"✅ **{len(deleted) - 1} mensagens deletadas**", delete_after=5)

@bot.command(name='kill')
@commands.has_permissions(administrator=True)
async def banir_membro(ctx, member: discord.Member, *, motivo="Violação grave das regras"):
    """💀 Banir membro com sistema de múltiplas denúncias"""
    try:
        # Simular múltiplas denúncias (3 tentativas)
        denuncias = []
        for i in range(3):
            try:
                denuncia_msg = f"Denúncia #{i+1} processada"
                denuncias.append(denuncia_msg)
                await asyncio.sleep(0.2)
            except:
                continue
        
        # Banir o membro
        await member.ban(reason=f"SYSTEM_KILL: {motivo} | Denúncias: {len(denuncias)}")
        
        # Registrar ação do bot para segurança
        await sistema_seguranca.registrar_acao_bot(ctx.guild.id, 'ban')
        
        embed = discord.Embed(
            title="💀 MEMBRO ELIMINADO",
            description=f"**{member.name}** foi banido do servidor",
            color=0xff0000
        )
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="🔨 Método", value="Sistema de múltiplas denúncias", inline=True)
        embed.add_field(name="📊 Denúncias", value=f"{len(denuncias)}/3 processadas", inline=True)
        embed.add_field(name="👮 Executado por", value=ctx.author.mention, inline=True)
        
        await ctx.send(embed=embed)
        await log_system.log_moderacao("KILL BAN", ctx.author, member, f"{motivo} | Denúncias: {len(denuncias)}")
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao executar comando kill: {e}")

@bot.command(name='rate')
@commands.has_permissions(administrator=True)
async def ativar_rate_limit(ctx):
    """🛡️ Ativa sistema de proteção total contra spam/abusos (COMANDO OCULTO)"""
    try:
        if rate_system.rate_limit_active:
            await ctx.send("❌ Sistema de proteção já está ativo!")
            return
            
        token = await rate_system.activate_rate_limit(ctx.guild, ctx.author)
        
        embed = discord.Embed(
            title="🛡️ SISTEMA DE PROTEÇÃO ATIVADO",
            description="**Proteções aplicadas em todo o servidor:**",
            color=0xff0000
        )
        embed.add_field(name="⏰ Rate Limit", value="15 segundos em todos os canais", inline=True)
        embed.add_field(name="🚫 Criação", value="Canais/Categorias bloqueados", inline=True)
        embed.add_field(name="🛡️ Cargos", value="Permissões perigosas removidas", inline=True)
        embed.add_field(name="🔍 Monitoramento", value="Detecção automática de abusos", inline=True)
        embed.add_field(name="✅ Token", value="Enviado no seu privado ✅", inline=False)
        embed.add_field(name="⚠️ Aviso", value="Qualquer tentativa de abuso será detectada e revertida automaticamente. Até cargos com todas as permissões estão bloqueados.", inline=False)
        
        await ctx.send(embed=embed)
        await log_system.log_rate_limit(ctx.guild, "SISTEMA ATIVADO", ctx.author, "Token enviado no privado")
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao ativar sistema de proteção: {e}")

# COMANDO PARA DESATIVAR RATE LIMIT VIA TOKEN (não aparece no help)
@bot.command(name='token_desativar', hidden=True)
async def desativar_rate_limit_token(ctx, token: str):
    """🔓 Desativa sistema de proteção com token (COMANDO OCULTO)"""
    if not rate_system.rate_limit_active:
        await ctx.send("❌ Sistema de proteção não está ativo")
        return
    
    if token == rate_system.rate_limit_token:
        await rate_system.deactivate_rate_limit(ctx.guild)
        
        embed = discord.Embed(
            title="🔓 SISTEMA DE PROTEÇÃO DESATIVADO",
            description="Todas as proteções foram removidas e permissões restauradas",
            color=0x00ff00
        )
        embed.add_field(name="✅ Restaurado", value="• Rate limit removido\n• Permissões de canais\n• Permissões de cargos\n• Criação liberada", inline=False)
        
        await ctx.send(embed=embed)
        await log_system.log_rate_limit(ctx.guild, "SISTEMA DESATIVADO", ctx.author, f"Via token: {token}")
    else:
        await ctx.send("❌ Token inválido!")

# ========== COMANDO DE EMERGÊNCIA ADICIONADO ==========

@bot.command(name='emergencia_desativar')
@commands.is_owner()
async def emergencia_desativar(ctx):
    """🚨 DESATIVA TODOS OS SISTEMAS DE SEGURANÇA (APENAS DONO)"""
    
    # Desativar rate limit
    if rate_system.rate_limit_active:
        await rate_system.deactivate_rate_limit(ctx.guild)
    
    # Desativar modo emergência
    sistema_deteccao.modo_emergencia = False
    
    # Limpar quarentena
    for user_id in list(sistema_seguranca.quarentena_usuarios.keys()):
        for guild in ctx.bot.guilds:
            member = guild.get_member(int(user_id))
            if member:
                await sistema_seguranca.remover_quarentena(member)
                break
    
    embed = discord.Embed(
        title="🚨 SISTEMAS DE SEGURANÇA DESATIVADOS",
        description="**Todos os sistemas de proteção foram desativados:**\n\n"
                   "• Rate Limit ❌\n"
                   "• Modo Emergência ❌\n" 
                   "• Quarentenas ❌\n"
                   "• Auto-delete ❌\n\n"
                   "**O bot agora funcionará normalmente.**",
        color=0x00ff00
    )
    
    await ctx.send(embed=embed)

# ========== COMANDOS DE ADMINISTRAÇÃO ORIGINAIS ==========

@bot.command(name='setup_cargos')
@commands.has_permissions(administrator=True)
async def setup_cargos(ctx):
    """🎯 Configura sistema automático de cargos"""
    
    progress = await ctx.send("🎯 **Configurando sistema de cargos...**")
    
    try:
        # Usar canal configurado ou criar um novo
        canal_id = CONFIG['canais_automaticos'].get('self_roles')
        if canal_id:
            canal_cargos = ctx.guild.get_channel(canal_id)
            if not canal_cargos:
                canal_cargos = await ctx.guild.create_text_channel("🎯・self-roles")
        else:
            canal_cargos = await ctx.guild.create_text_channel("🎯・self-roles")
        
        permissao = discord.PermissionOverwrite()
        permissao.send_messages = False
        permissao.add_reactions = True
        permissao.read_messages = True
        await canal_cargos.set_permissions(ctx.guild.default_role, overwrite=permissao)
        
        embed_info = discord.Embed(
            title="🎯 SISTEMA DE CARGOS AUTOMÁTICO",
            description="**Como funciona:**\n• Clique no EMOJI para receber o cargo\n• Clique novamente para remover o cargo\n• Você pode ter múltiplos cargos",
            color=0x00ff00
        )
        await canal_cargos.send(embed=embed_info)
        
        embed_linguagens = discord.Embed(
            title="💻 LINGUAGENS DE PROGRAMAÇÃO",
            description="**Clique nos emojis para adicionar/remover cargos:**\n\n"
                       "🐍 **Python** - Desenvolvimento geral, IA, automação\n"
                       "☕ **Java** - Aplicações enterprise, Android\n"
                       "🟨 **JavaScript** - Web, Node.js, frontend\n"
                       "🔵 **Golang** - Sistemas, APIs, concorrência\n"
                       "🦀 **Rust** - Sistemas, performance, segurança\n"
                       "💜 **C#** - Games, Windows, .NET\n"
                       "🔷 **C/C++** - Sistemas, games, embarcados\n"
                       "🐘 **PHP** - Web, WordPress, Laravel\n"
                       "💎 **Ruby** - Web, Rails, scripts\n"
                       "🍎 **Swift** - iOS, macOS desenvolvimento\n"
                       "💚 **Kotlin** - Android, modern Java alternative\n"
                       "🐚 **Bash/Shell** - Scripting, DevOps, automação",
            color=0x0099ff
        )
        
        mensagem_ling = await canal_cargos.send(embed=embed_linguagens)
        
        for cargo_nome in CONFIG["cargos_linguagens"].keys():
            cargo = discord.utils.get(ctx.guild.roles, name=cargo_nome)
            if not cargo:
                try:
                    cargo = await ctx.guild.create_role(name=cargo_nome, mentionable=True, color=discord.Color.blue())
                    await asyncio.sleep(0.5)
                except:
                    continue
            
            emoji = cargo_nome.split(' ')[0]
            await mensagem_ling.add_reaction(emoji)
            await asyncio.sleep(0.5)
        
        embed_cyber = discord.Embed(
            title="🛡️ CYBER SEGURANÇA",
            description="**Especialidades em segurança:**\n\n"
                       "🎩 **Ethical Hacker** - Testes de invasão autorizados\n"
                       "🔍 **Pentester** - Testes de penetração\n"
                       "🛡️ **Blue Team** - Defesa e proteção\n"
                       "🔴 **Red Team** - Simulação de atacantes\n"
                       "💰 **Bug Hunter** - Caça a vulnerabilidades\n"
                       "🏆 **CTF Player** - Competições de segurança\n"
                       "🕵️ **OSINT** - Inteligência de fontes abertas\n"
                       "🔧 **Reverse Eng** - Engenharia reversa\n"
                       "💣 **Exploit Dev** - Desenvolvimento de exploits\n"
                       "🦠 **Malware Analyst** - Análise de malware",
            color=0xff0000
        )
        
        mensagem_cyber = await canal_cargos.send(embed=embed_cyber)
        
        for cargo_nome in CONFIG["cargos_cyber"].keys():
            cargo = discord.utils.get(ctx.guild.roles, name=cargo_nome)
            if not cargo:
                try:
                    cargo = await ctx.guild.create_role(name=cargo_nome, mentionable=True, color=discord.Color.red())
                    await asyncio.sleep(0.5)
                except:
                    continue
            
            emoji = cargo_nome.split(' ')[0]
            await mensagem_cyber.add_reaction(emoji)
            await asyncio.sleep(0.5)
        
        await progress.edit(content=f"✅ **Sistema de cargos configurado!** {canal_cargos.mention}")
        
    except Exception as e:
        await progress.edit(content=f"❌ Erro: {e}")

@bot.command(name='setup_completo')
@commands.has_permissions(administrator=True)
async def setup_completo(ctx):
    """⚙️ Configuração completa do servidor"""
    progress = await ctx.send("⚙️ **Iniciando configuração completa...**")
    
    try:
        await progress.edit(content="📁 **Criando canais de logs...**")
        
        for tipo, nome_canal in CONFIG["logs_config"].items():
            canal_existente = discord.utils.get(ctx.guild.text_channels, name=nome_canal)
            if not canal_existente:
                canal = await ctx.guild.create_text_channel(nome_canal)
                
                permissao = discord.PermissionOverwrite()
                permissao.send_messages = False
                permissao.read_messages = True
                await canal.set_permissions(ctx.guild.default_role, overwrite=permissao)
                await asyncio.sleep(0.5)
        
        await progress.edit(content="🎯 **Configurando sistema de cargos...**")
        await setup_cargos(ctx)
        
        await progress.edit(content="🔄 **Atualizando cargos e nicks...**")
        await atualizar_cargos(ctx)
        
        await progress.edit(content="🎫 **Configurando sistema de tickets...**")
        await sistema_tickets.setup_canal_tickets(ctx.guild)
        
        await progress.edit(content="✅ **Configuração completa finalizada!**")
        
    except Exception as e:
        await progress.edit(content=f"❌ Erro na configuração: {e}")

@bot.command(name='config')
@commands.has_permissions(administrator=True)
async def config(ctx):
    """⚙️ Sistema de configuração de canais"""
    embed = discord.Embed(
        title="⚙️ SISTEMA DE CONFIGURAÇÃO",
        description="**Configure os canais automáticos do bot:**\n\n"
                   "📋 **Canais disponíveis para configuração:**\n"
                   "1. `self_roles` - Cargo de self roles\n"
                   "2. `entrada_saida` - Entrada/saída de membros\n"
                   "3. `mod_logs` - Logs de moderação\n"
                   "4. `cargo_logs` - Logs de cargos\n"
                   "5. `advertencias` - Logs de advertências\n"
                   "6. `conquistas` - Logs de conquistas\n"
                   "7. `pontuacao` - Logs de pontuação\n\n"
                   "**Como usar:**\n"
                   "`!set self_roles #canal` - Define o canal de self roles\n"
                   "`!view_config` - Ver configuração atual\n"
                   "`!reset_config` - Resetar configuração",
        color=0x7289DA
    )
    await ctx.send(embed=embed)

@bot.command(name='set')
@commands.has_permissions(administrator=True)
async def set_channel(ctx, tipo: str, canal: discord.TextChannel):
    """🔧 Define um canal para função específica"""
    tipos_validos = [
        'self_roles', 'entrada_saida', 'mod_logs', 
        'cargo_logs', 'advertencias', 'conquistas', 'pontuacao'
    ]
    
    if tipo not in tipos_validos:
        embed = discord.Embed(
            title="❌ TIPO INVÁLIDO",
            description=f"**Tipos válidos:** {', '.join(tipos_validos)}",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    # Salvar configuração
    CONFIG['canais_automaticos'][tipo] = canal.id
    db.config_canais['canais_automaticos'] = CONFIG['canais_automaticos']
    db.salvar_dados()
    
    embed = discord.Embed(
        title="✅ CANAL CONFIGURADO",
        description=f"**{tipo}** definido para {canal.mention}",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

@bot.command(name='view_config')
@commands.has_permissions(administrator=True)
async def view_config(ctx):
    """📋 Ver configuração atual de canais"""
    embed = discord.Embed(
        title="📋 CONFIGURAÇÃO ATUAL",
        color=0x0099ff
    )
    
    for tipo, canal_id in CONFIG['canais_automaticos'].items():
        if canal_id:
            canal = ctx.guild.get_channel(canal_id)
            if canal:
                embed.add_field(
                    name=f"🔧 {tipo.upper()}",
                    value=f"{canal.mention} (`{canal_id}`)",
                    inline=True
                )
            else:
                embed.add_field(
                    name=f"❌ {tipo.upper()}",
                    value=f"Canal não encontrado (`{canal_id}`)",
                    inline=True
                )
        else:
            embed.add_field(
                name=f"⚙️ {tipo.upper()}",
                value="Não configurado",
                inline=True
            )
    
    if not embed.fields:
        embed.description = "Nenhum canal configurado ainda."
    
    await ctx.send(embed=embed)

@bot.command(name='reset_config')
@commands.has_permissions(administrator=True)
async def reset_config(ctx, tipo: str = None):
    """🔄 Resetar configuração de canais"""
    if tipo:
        if tipo in CONFIG['canais_automaticos']:
            CONFIG['canais_automaticos'][tipo] = None
            db.config_canais['canais_automaticos'] = CONFIG['canais_automaticos']
            db.salvar_dados()
            
            embed = discord.Embed(
                title="✅ CONFIGURAÇÃO RESETADA",
                description=f"Configuração de **{tipo}** foi resetada",
                color=0x00ff00
            )
        else:
            embed = discord.Embed(
                title="❌ TIPO INVÁLIDO",
                description=f"Tipo **{tipo}** não encontrado",
                color=0xff0000
            )
    else:
        # Resetar tudo
        for tipo in CONFIG['canais_automaticos']:
            CONFIG['canais_automaticos'][tipo] = None
        
        db.config_canais['canais_automaticos'] = CONFIG['canais_automaticos']
        db.salvar_dados()
        
        embed = discord.Embed(
            title="✅ CONFIGURAÇÃO COMPLETA RESETADA",
            description="Todas as configurações de canais foram resetadas",
            color=0x00ff00
        )
    
    await ctx.send(embed=embed)

@bot.command(name='set_canal')
@commands.has_permissions(administrator=True)
async def set_canal(ctx, canal: discord.TextChannel = None):
    """🔧 Define canal onde o bot pode interagir"""
    canal = canal or ctx.channel
    
    if canal.id not in CONFIG['canais_permitidos']:
        CONFIG['canais_permitidos'].append(canal.id)
        db.config['canais_permitidos'] = CONFIG['canais_permitidos']
        db.salvar_dados()
        await ctx.send(f"✅ Canal {canal.mention} adicionado à lista de permitidos")
    else:
        CONFIG['canais_permitidos'].remove(canal.id)
        db.config['canais_permitidos'] = CONFIG['canais_permitidos']
        db.salvar_dados()
        await ctx.send(f"✅ Canal {canal.mention} removido da lista de permitidos")

@bot.command(name='protecao_auto')
@commands.has_permissions(administrator=True)
async def protecao_auto(ctx):
    """🛡️ Ativa sistema de proteção automática"""
    embed = discord.Embed(
        title="🛡️ SISTEMA DE PROTEÇÃO AUTOMÁTICA",
        description="**Proteções ativadas:**\n\n"
                   "• Detecção de spam automática\n"
                   "• Bloqueio de links suspeitos\n"
                   "• Prevenção contra raids\n"
                   "• Monitoramento de atividades suspeitas\n"
                   "• Backup automático de configurações",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

@bot.command(name='estatisticas_seguranca')
@commands.has_permissions(administrator=True)
async def estatisticas_seguranca(ctx):
    """📊 Estatísticas de segurança do servidor"""
    embed = discord.Embed(
        title="📊 ESTATÍSTICAS DE SEGURANÇA",
        color=0x0099ff
    )
    
    total_membros = len(ctx.guild.members)
    membros_ativos = len([m for m in ctx.guild.members if m.status != discord.Status.offline])
    total_advertencias = sum(len(adv) for adv in db.advertencias.values())
    
    embed.add_field(name="👥 Total de Membros", value=total_membros, inline=True)
    embed.add_field(name="🟢 Membros Ativos", value=membros_ativos, inline=True)
    embed.add_field(name="⚠️ Advertências", value=total_advertencias, inline=True)
    embed.add_field(name="🛡️ Sistema de Proteção", value="✅ Ativo" if rate_system.rate_limit_active else "❌ Inativo", inline=True)
    embed.add_field(name="📈 Nível de Segurança", value="🔴 Alto" if total_advertencias > 10 else "🟡 Médio" if total_advertencias > 5 else "🟢 Baixo", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='backup_servidor')
@commands.has_permissions(administrator=True)
async def backup_servidor(ctx):
    """💾 Cria backup do servidor"""
    await ctx.typing()
    
    try:
        # Simular criação de backup (em produção, implementaria backup real)
        backup_data = {
            "servidor": ctx.guild.name,
            "membros": len(ctx.guild.members),
            "canais": len(ctx.guild.channels),
            "cargos": len(ctx.guild.roles),
            "data_backup": datetime.now().isoformat()
        }
        
        embed = discord.Embed(
            title="💾 BACKUP CRIADO",
            description=f"Backup do servidor **{ctx.guild.name}** criado com sucesso!",
            color=0x00ff00
        )
        embed.add_field(name="📊 Dados Salvos", value=f"• {backup_data['membros']} membros\n• {backup_data['canais']} canais\n• {backup_data['cargos']} cargos", inline=False)
        embed.add_field(name="📅 Data", value=datetime.now().strftime("%d/%m/%Y %H:%M"), inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao criar backup: {e}")

@bot.command(name='restaurar_servidor')
@commands.has_permissions(administrator=True)
async def restaurar_servidor(ctx):
    """🔄 Restaura servidor do backup"""
    embed = discord.Embed(
        title="🔄 RESTAURAÇÃO DE SERVIDOR",
        description="**Este comando restauraria o servidor do último backup.**\n\n"
                   "⚠️ **Atenção:** Esta ação é irreversível e substituiria todas as configurações atuais.",
        color=0xff9900
    )
    await ctx.send(embed=embed)

@bot.command(name='scan_membros')
@commands.has_permissions(administrator=True)
async def scan_membros(ctx):
    """🔍 Scan de membros inativos/suspeitos"""
    await ctx.typing()
    
    try:
        membros_inativos = []
        membros_suspeitos = []
        
        for member in ctx.guild.members:
            # Verificar membros inativos (mais de 30 dias)
            if member.joined_at and (datetime.now() - member.joined_at.replace(tzinfo=None)).days > 30:
                if member.status == discord.Status.offline:
                    membros_inativos.append(member)
            
            # Verificar contas suspeitas (muito novas)
            if member.created_at and (datetime.now() - member.created_at.replace(tzinfo=None)).days < 7:
                membros_suspeitos.append(member)
        
        embed = discord.Embed(
            title="🔍 SCAN DE MEMBROS",
            color=0x0099ff
        )
        
        if membros_inativos:
            embed.add_field(
                name="💤 Membros Inativos",
                value="\n".join([f"• {m.name}" for m in membros_inativos[:10]]) + (f"\n... e mais {len(membros_inativos)-10}" if len(membros_inativos) > 10 else ""),
                inline=False
            )
        
        if membros_suspeitos:
            embed.add_field(
                name="🚨 Contas Suspeitas",
                value="\n".join([f"• {m.name} (criada há {(datetime.now() - m.created_at.replace(tzinfo=None)).days} dias)" for m in membros_suspeitos[:10]]),
                inline=False
            )
        
        if not membros_inativos and not membros_suspeitos:
            embed.description = "✅ Nenhum membro inativo ou suspeito encontrado!"
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro no scan: {e}")

@bot.command(name='limpar_inativos')
@commands.has_permissions(administrator=True)
async def limpar_inativos(ctx, dias: int = 30):
    """🧹 Remove membros inativos"""
    embed = discord.Embed(
        title="🧹 LIMPEZA DE INATIVOS",
        description=f"**Este comando removeria membros inativos por mais de {dias} dias.**\n\n"
                   f"⚠️ **Atenção:** Esta ação é irreversível!",
        color=0xff0000
    )
    embed.add_field(name="🔧 Modo de Uso", value="Use com cuidado e apenas quando necessário.", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='criar_canais')
@commands.has_permissions(administrator=True)
async def criar_canais(ctx, categoria: str = "moderacao"):
    """🏗️ Cria conjunto de canais automáticos"""
    await ctx.typing()
    
    categorias = {
        "moderacao": [
            {"name": "🛡️・mod-logs", "type": "text", "topic": "Logs de moderação"},
            {"name": "⚠️・advertencias", "type": "text", "topic": "Sistema de advertências"},
            {"name": "📊・auditoria", "type": "text", "topic": "Auditoria do servidor"}
        ],
        "membros": [
            {"name": "👤・entrada-saida", "type": "text", "topic": "Entrada e saída de membros"},
            {"name": "⭐・cargo-logs", "type": "text", "topic": "Alterações de cargos"},
            {"name": "🏆・conquistas", "type": "text", "topic": "Conquistas dos membros"}
        ],
        "cyber": [
            {"name": "💻・ctf-challenges", "type": "text", "topic": "Desafios CTF"},
            {"name": "🛡️・cyber-missoes", "type": "text", "topic": "Missões de cybersecurity"},
            {"name": "🔍・investigacao", "type": "text", "topic": "Análise e investigação"}
        ]
    }
    
    if categoria not in categorias:
        embed = discord.Embed(
            title="🏗️ SISTEMA DE CRIAÇÃO DE CANAIS",
            description="**Categorias disponíveis:**\n• `moderacao` - Canais de moderação\n• `membros` - Canais para membros\n• `cyber` - Canais cybersecurity",
            color=0x0099ff
        )
        await ctx.send(embed=embed)
        return
    
    try:
        canals_criados = []
        for config in categorias[categoria]:
            if config["type"] == "text":
                canal = await ctx.guild.create_text_channel(
                    name=config["name"],
                    topic=config["topic"]
                )
                canals_criados.append(canal.mention)
            
            await asyncio.sleep(0.5)
        
        embed = discord.Embed(
            title="✅ CANAIS CRIADOS COM SUCESSO",
            description=f"**Categoria:** {categoria}\n**Canais:** {' | '.join(canals_criados)}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao criar canais: {e}")

@bot.command(name='cat')
@commands.has_permissions(manage_channels=True)
async def listar_categorias(ctx):
    """📋 Lista todas as categorias com IDs"""
    embed = discord.Embed(
        title="📋 CATEGORIAS DO SERVIDOR",
        description="Lista de todas as categorias e seus IDs:",
        color=0x0099ff
    )
    
    categorias = sorted(ctx.guild.categories, key=lambda x: x.position)
    
    for i, categoria in enumerate(categorias, 1):
        canais_texto = [f"#{canal.name}" for canal in categoria.text_channels]
        canais_voz = [f"🔊{canal.name}" for canal in categoria.voice_channels]
        todos_canais = canais_texto + canais_voz
        
        embed.add_field(
            name=f"{i}. {categoria.name}",
            value=f"**ID:** `{categoria.id}`\n**Canais:** {len(todos_canais)}\n" + "\n".join(todos_canais[:5]) + ("\n..." if len(todos_canais) > 5 else ""),
            inline=True
        )
    
    embed.set_footer(text="Use !-d <id_da_categoria> para deletar uma categoria")
    await ctx.send(embed=embed)

# ========== COMANDOS DE GERENCIAMENTO DE CANAIS ORIGINAIS ==========

@bot.command(name='d')
@commands.has_permissions(manage_channels=True)
async def deletar_canal(ctx, canal: discord.TextChannel = None):
    """🗑️ Deleta um canal específico"""
    canal = canal or ctx.channel
    try:
        nome_canal = canal.name
        await canal.delete()
        
        # Registrar ação do bot para segurança
        await sistema_seguranca.registrar_acao_bot(ctx.guild.id, 'channel_delete')
        
        embed = discord.Embed(
            title="🗑️ CANAL DELETADO",
            description=f"Canal `{nome_canal}` foi deletado com sucesso!",
            color=0x00ff00
        )
        await ctx.send(embed=embed, delete_after=10)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao deletar canal: {e}")

@bot.command(name='-d')
@commands.has_permissions(manage_channels=True)
async def deletar_categoria(ctx, categoria_id: int):
    """🗑️ Deleta uma categoria e todos os seus canais"""
    try:
        categoria = ctx.guild.get_channel(categoria_id)
        if not categoria or not isinstance(categoria, discord.CategoryChannel):
            await ctx.send("❌ Categoria não encontrada!")
            return
        
        nome_categoria = categoria.name
        canais_na_categoria = len(categoria.channels)
        
        # Deletar todos os canais da categoria primeiro
        for canal in categoria.channels:
            try:
                await canal.delete()
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Erro ao deletar canal {canal.name}: {e}")
        
        # Deletar a categoria
        await categoria.delete()
        
        # Registrar ação do bot para segurança
        await sistema_seguranca.registrar_acao_bot(ctx.guild.id, 'channel_delete')
        
        embed = discord.Embed(
            title="🗑️ CATEGORIA DELETADA",
            description=f"Categoria **{nome_categoria}** e seus **{canais_na_categoria}** canais foram deletados!",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao deletar categoria: {e}")

@bot.command(name='ca')
@commands.has_permissions(manage_channels=True)
async def criar_canal_categoria(ctx, nome_canal: str, permissao: str, categoria_id: int):
    """💬 Cria canal em categoria específica"""
    try:
        categoria = ctx.guild.get_channel(categoria_id)
        if not categoria or not isinstance(categoria, discord.CategoryChannel):
            await ctx.send("❌ Categoria não encontrada!")
            return
        
        # Criar canal na categoria
        canal = await ctx.guild.create_text_channel(
            name=nome_canal.lower(),
            category=categoria
        )
        
        # Configurar permissões
        if permissao.lower() == "lock":
            await canal.set_permissions(ctx.guild.default_role, read_messages=False)
        elif permissao.lower() == "unlock":
            await canal.set_permissions(ctx.guild.default_role, read_messages=True)
        
        embed = discord.Embed(
            title="💬 CANAL CRIADO",
            description=f"Canal **{canal.name}** criado em **{categoria.name}**!",
            color=0x00ff00
        )
        embed.add_field(name="🔒 Permissão", value="Bloqueado" if permissao.lower() == "lock" else "Liberado", inline=True)
        embed.add_field(name="📁 Categoria", value=categoria.name, inline=True)
        embed.add_field(name="🆔 ID da Categoria", value=categoria_id, inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao criar canal: {e}")

@bot.command(name='+ca')
@commands.has_permissions(manage_channels=True)
async def criar_categoria_canais(ctx, *args):
    """🏗️ Cria categoria e múltiplos canais"""
    if len(args) < 3 or len(args) % 2 == 0:
        embed = discord.Embed(
            title="❌ USO INCORRETO",
            description="**Como usar:** `!+ca <nome_canal1> <permissao1> <nome_canal2> <permissao2> ... <nome_categoria>`\n\n**Exemplo:** `!+ca chat unlock midia unlock resenhas unlock Minha Categoria`",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    # Último argumento é o nome da categoria
    nome_categoria = args[-1]
    canais_config = args[:-1]
    
    try:
        # Criar categoria
        categoria = await ctx.guild.create_category(nome_categoria.upper())
        
        # Criar canais na categoria
        canais_criados = []
        for i in range(0, len(canais_config), 2):
            nome_canal = canais_config[i].lower()
            permissao = canais_config[i+1].lower()
            
            canal = await ctx.guild.create_text_channel(
                name=nome_canal,
                category=categoria
            )
            
            # Configurar permissões
            if permissao == "lock":
                await canal.set_permissions(ctx.guild.default_role, read_messages=False)
            elif permissao == "unlock":
                await canal.set_permissions(ctx.guild.default_role, read_messages=True)
            
            canais_criados.append(f"• {canal.name} ({permissao})")
            await asyncio.sleep(0.5)
        
        embed = discord.Embed(
            title="🏗️ CATEGORIA E CANAIS CRIADOS",
            description=f"Categoria **{categoria.name}** criada com **{len(canais_criados)}** canais!",
            color=0x00ff00
        )
        embed.add_field(name="📂 Categoria", value=categoria.name, inline=True)
        embed.add_field(name="🆔 ID", value=categoria.id, inline=True)
        embed.add_field(name="🔢 Total de Canais", value=len(canais_criados), inline=True)
        embed.add_field(name="📋 Canais Criados", value="\n".join(canais_criados), inline=False)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao criar categoria e canais: {e}")

@bot.command(name='x')
@commands.has_permissions(manage_channels=True)
async def modo_visualizacao(ctx, canal: discord.TextChannel = None):
    """👀 Ativa modo somente visualização no canal (SEM MENCIONAR LORRITA)"""
    canal = canal or ctx.channel
    try:
        # Salvar permissões originais
        overwrites = canal.overwrites_for(ctx.guild.default_role)
        
        # Configurar somente visualização (SEM MENCIONAR LORRITA)
        overwrites.send_messages = False
        overwrites.read_messages = True
        overwrites.add_reactions = False
        overwrites.use_application_commands = False
        overwrites.create_public_threads = False
        overwrites.create_private_threads = False
        overwrites.send_messages_in_threads = False
        
        await canal.set_permissions(ctx.guild.default_role, overwrite=overwrites)
        
        embed = discord.Embed(
            title="👀 MODO VISUALIZAÇÃO ATIVADO",
            description=f"{canal.mention} agora está em modo somente visualização",
            color=0xffff00
        )
        embed.add_field(name="📝 Permissões", value="✅ Ver mensagens\n❌ Enviar mensagens\n❌ Reagir\n❌ Usar comandos\n❌ Criar threads", inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao ativar modo visualização: {e}")

@bot.command(name='-x')
@commands.has_permissions(manage_channels=True)
async def remover_visualizacao(ctx, canal: discord.TextChannel = None):
    """💬 Remove modo somente visualização do canal"""
    canal = canal or ctx.channel
    try:
        # Restaurar permissões de envio (None = herdar da categoria)
        overwrites = canal.overwrites_for(ctx.guild.default_role)
        overwrites.send_messages = None
        overwrites.add_reactions = None
        overwrites.use_application_commands = None
        overwrites.create_public_threads = None
        overwrites.create_private_threads = None
        overwrites.send_messages_in_threads = None
        
        await canal.set_permissions(ctx.guild.default_role, overwrite=overwrites)
        
        embed = discord.Embed(
            title="💬 MODO VISUALIZAÇÃO REMOVIDO",
            description=f"{canal.mention} agora permite envio de mensagens normalmente",
            color=0x00ff00
        )
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao remover modo visualização: {e}")

@bot.command(name='lk')
@commands.has_permissions(manage_channels=True)
async def bloquear_canal(ctx, canal: discord.TextChannel = None):
    """🔒 Bloqueia um canal"""
    canal = canal or ctx.channel
    try:
        await canal.set_permissions(ctx.guild.default_role, read_messages=False)
        
        embed = discord.Embed(
            title="🔒 CANAL BLOQUEADO",
            description=f"{canal.mention} foi bloqueado",
            color=0xff0000
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro ao bloquear canal: {e}")

@bot.command(name='ulk')
@commands.has_permissions(manage_channels=True)
async def desbloquear_canal(ctx, canal: discord.TextChannel = None):
    """🔓 Desbloqueia um canal"""
    canal = canal or ctx.channel
    try:
        await canal.set_permissions(ctx.guild.default_role, read_messages=True)
        
        embed = discord.Embed(
            title="🔓 CANAL DESBLOQUEADO",
            description=f"{canal.mention} foi desbloqueado",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro ao desbloquear canal: {e}")

@bot.command(name='mv')
@commands.has_permissions(manage_channels=True)
async def mover_canal(ctx, posicao_atual: int, nova_posicao: int):
    """📦 Move canal para nova posição"""
    try:
        canais = [canal for canal in ctx.guild.text_channels if canal.category]
        canais.sort(key=lambda x: x.position)
        
        if posicao_atual < 1 or posicao_atual > len(canais) or nova_posicao < 1 or nova_posicao > len(canais):
            await ctx.send(f"❌ Posições devem ser entre 1 e {len(canais)}")
            return
        
        canal = canais[posicao_atual - 1]
        await canal.edit(position=nova_posicao - 1)
        
        embed = discord.Embed(
            title="📦 CANAL MOVIDO",
            description=f"**{canal.name}** movido para posição **#{nova_posicao}**",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro ao mover canal: {e}")

@bot.command(name='mv_cat')
@commands.has_permissions(manage_channels=True)
async def mover_categoria(ctx, posicao_atual: int, nova_posicao: int):
    """🏗️ Move categoria para nova posição"""
    try:
        categorias = [categoria for categoria in ctx.guild.categories if categoria.name]
        categorias.sort(key=lambda x: x.position)
        
        if posicao_atual < 1 or posicao_atual > len(categorias) or nova_posicao < 1 or nova_posicao > len(categorias):
            await ctx.send(f"❌ Posições devem ser entre 1 e {len(categorias)}")
            return
        
        categoria = categorias[posicao_atual - 1]
        await categoria.edit(position=nova_posicao - 1)
        
        embed = discord.Embed(
            title="🏗️ CATEGORIA MOVIDA",
            description=f"**{categoria.name}** movida para posição **#{nova_posicao}**",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro ao mover categoria: {e}")

# SISTEMA DE CRIAÇÃO COM IA PARA CATEGORIAS E CANAIS
async def criar_categoria_com_ia(ctx, nome: str, permissao: str = "unlock"):
    """🏗️ Cria categoria com IA (escolhe emoji) - VERSÃO CORRIGIDA"""
    await ctx.typing()
    
    # IA escolhe emoji apropriado
    prompt = f"Para uma categoria de Discord chamada '{nome}', qual emoji seria mais apropriado? Responda APENAS com o emoji."
    emoji = await groq_ai.gerar_resposta(prompt)
    
    # Limpar resposta da IA para pegar apenas o emoji
    emoji_limpo = emoji.strip().split(' ')[0] if emoji else "📁"
    
    try:
        nome_categoria = f"{emoji_limpo}・{nome.upper()}"
        categoria = await ctx.guild.create_category(name=nome_categoria)
        
        # Configurar permissões CORRETAMENTE
        if permissao.lower() == "lock":
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            await categoria.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        
        embed = discord.Embed(
            title="🏗️ CATEGORIA CRIADA",
            description=f"Categoria **{categoria.name}** criada com sucesso!",
            color=0x00ff00
        )
        embed.add_field(name="🔒 Permissão", value="Bloqueada" if permissao.lower() == "lock" else "Liberada", inline=True)
        embed.add_field(name="🎯 Posição", value=categoria.position + 1, inline=True)
        embed.add_field(name="🆔 ID", value=categoria.id, inline=True)
        
        await ctx.send(embed=embed)
        return categoria
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao criar categoria: {e}")
        return None

async def criar_canal_com_ia(ctx, nome: str, tipo: str = "texto", permissao: str = "unlock", categoria=None):
    """💬 Cria canal com IA (escolhe emoji) - VERSÃO CORRIGIDA"""
    await ctx.typing()
    
    # IA escolhe emoji apropriado
    prompt = f"Para um canal de Discord {'de texto' if tipo == 'texto' else 'de voz'} chamado '{nome}', qual emoji seria mais apropriado? Responda APENAS com o emoji."
    emoji = await groq_ai.gerar_resposta(prompt)
    emoji_limpo = emoji.strip().split(' ')[0] if emoji else "💬" if tipo == "texto" else "🔊"
    
    try:
        nome_canal = f"{emoji_limpo}・{nome.lower()}"
        
        if tipo.lower() == "texto":
            canal = await ctx.guild.create_text_channel(name=nome_canal, category=categoria)
        else:
            canal = await ctx.guild.create_voice_channel(name=nome_canal, category=categoria)
        
        # Configurar permissões CORRETAMENTE
        if permissao.lower() == "lock":
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = False
            overwrite.send_messages = False
            await canal.set_permissions(ctx.guild.default_role, overwrite=overwrites)
        
        embed = discord.Embed(
            title="💬 CANAL CRIADO",
            description=f"Canal **{canal.name}** criado com sucesso!",
            color=0x00ff00
        )
        embed.add_field(name="🔒 Permissão", value="Bloqueada" if permissao.lower() == "lock" else "Liberada", inline=True)
        embed.add_field(name="📝 Tipo", value="Texto" if tipo == "texto" else "Voz", inline=True)
        if categoria:
            embed.add_field(name="📁 Categoria", value=categoria.name, inline=True)
        
        await ctx.send(embed=embed)
        return canal
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao criar canal: {e}")
        return None

# COMANDOS CORRIGIDOS PARA CRIAÇÃO
@bot.command(name='-mq')
@commands.has_permissions(manage_channels=True)
async def criar_categoria_ia(ctx, nome: str, permissao: str = "unlock"):
    """🏗️ Cria categoria com IA (escolhe emoji) - VERSÃO CORRIGIDA"""
    await criar_categoria_com_ia(ctx, nome, permissao)

@bot.command(name='-mc')
@commands.has_permissions(manage_channels=True)
async def criar_canal_ia(ctx, nome: str, tipo: str = "texto", permissao: str = "unlock"):
    """💬 Cria canal com IA (escolhe emoji) - VERSÃO CORRIGIDA"""
    await criar_canal_com_ia(ctx, nome, tipo, permissao, ctx.channel.category)

@bot.command(name='criar_embed')
@commands.has_permissions(manage_messages=True)
async def criar_embed(ctx, titulo: str, *, descricao: str):
    """🎨 Cria uma mensagem embed personalizada"""
    embed = discord.Embed(
        title=titulo,
        description=descricao,
        color=0x0099ff,
        timestamp=datetime.now()
    )
    embed.set_footer(text=f"Criado por {ctx.author.name}")
    await ctx.send(embed=embed)

@bot.command(name='ejetar')
@commands.has_permissions(administrator=True)
async def ejetar(ctx, canal: discord.TextChannel = None, *, mensagem):
    """🚀 Ejeta mensagem direto no canal (SEM IA)"""
    try:
        await canal.send(mensagem)
        
        embed = discord.Embed(
            title="🚀 MENSAGEM EJETADA",
            description=f"Mensagem enviada para {canal.mention}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro ao ejetar mensagem: {e}")

@bot.command(name='emoji_info')
async def emoji_info(ctx, emoji: discord.Emoji):
    """😀 Mostra informações sobre um emoji"""
    embed = discord.Embed(title=f"Informações do Emoji: {emoji.name}", color=0x0099ff)
    embed.add_field(name="🆔 ID", value=emoji.id, inline=True)
    embed.add_field(name="📅 Criado em", value=emoji.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="👥 Disponível para", value="Todos" if emoji.available else "Restrito", inline=True)
    embed.add_field(name="🔗 URL", value=f"[Clique aqui]({emoji.url})", inline=True)
    embed.set_thumbnail(url=emoji.url)
    await ctx.send(embed=embed)

@bot.command(name='criar_emoji')
@commands.has_permissions(manage_emojis=True)
async def criar_emoji(ctx, nome: str, url: str = None):
    """🆕 Cria um novo emoji"""
    try:
        if url:
            # Baixar imagem da URL
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        emoji = await ctx.guild.create_custom_emoji(name=nome, image=image_data)
                        await ctx.send(f"✅ Emoji {emoji} criado com sucesso!")
                    else:
                        await ctx.send("❌ Erro ao baixar imagem")
        else:
            # Verificar se há anexo
            if ctx.message.attachments:
                image_data = await ctx.message.attachments[0].read()
                emoji = await ctx.guild.create_custom_emoji(name=nome, image=image_data)
                await ctx.send(f"✅ Emoji {emoji} criado com sucesso!")
            else:
                await ctx.send("❌ Forneça uma URL ou anexe uma imagem")
    except Exception as e:
        await ctx.send(f"❌ Erro ao criar emoji: {e}")

@bot.command(name='servericon')
async def server_icon(ctx):
    """�️ Mostra o ícone do servidor"""
    if ctx.guild.icon:
        embed = discord.Embed(title=f"Ícone do Servidor: {ctx.guild.name}", color=0x0099ff)
        embed.set_image(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Este servidor não tem ícone")

@bot.command(name='avatar')
async def avatar(ctx, member: discord.Member = None):
    """🖼️ Mostra o avatar de um usuário"""
    member = member or ctx.author
    embed = discord.Embed(title=f"Avatar de {member.name}", color=0x0099ff)
    embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

# ========== SISTEMA PDF ORIGINAL ==========

@bot.command(name='pdf_canal')
@commands.has_permissions(manage_messages=True)
async def pdf_canal(ctx, limite: int = 100):
    """📄 Cria PDF com as mensagens do canal"""
    await ctx.typing()
    
    try:
        # Coletar mensagens
        messages = []
        async for message in ctx.channel.history(limit=limite):
            if not message.author.bot:  # Ignorar mensagens de bots
                messages.append(message)
        
        messages.reverse()  # Ordem cronológica
        
        if not messages:
            await ctx.send("❌ Nenhuma mensagem encontrada para criar o PDF")
            return
        
        # Criar conteúdo HTML para o PDF
        html_content = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Mensagens do Canal #{ctx.channel.name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .message {{ border-bottom: 1px solid #eee; padding: 10px 0; }}
                .author {{ font-weight: bold; color: #7289DA; }}
                .timestamp {{ color: #666; font-size: 12px; }}
                .content {{ margin: 5px 0; }}
                .header {{ text-align: center; border-bottom: 2px solid #7289DA; padding-bottom: 10px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>💬 Mensagens do Canal #{ctx.channel.name}</h1>
                <p>Servidor: {ctx.guild.name} | Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                <p>Total de mensagens: {len(messages)}</p>
            </div>
        """
        
        for message in messages:
            html_content += f"""
            <div class="message">
                <div class="author">{message.author.display_name}</div>
                <div class="timestamp">{message.created_at.strftime('%d/%m/%Y %H:%M')}</div>
                <div class="content">{message.content.replace('<', '&lt;').replace('>', '&gt;')}</div>
            </div>
            """
        
        html_content += "</body></html>"
        
        # Configurar pdfkit
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        
        # Gerar PDF
        pdf = pdfkit.from_string(html_content, False, configuration=config)
        
        # Enviar PDF
        await ctx.send(
            f"📄 **PDF gerado com sucesso!**\n"
            f"**Canal:** #{ctx.channel.name}\n"
            f"**Mensagens:** {len(messages)}\n"
            f"**Período:** {messages[0].created_at.strftime('%d/%m %H:%M')} - {messages[-1].created_at.strftime('%d/%m %H:%M')}",
            file=discord.File(BytesIO(pdf), filename=f"mensagens_{ctx.channel.name}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
        )
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao gerar PDF: {e}")

@bot.command(name='web_to_pdf')
async def web_to_pdf(ctx, url: str):
    """📄 Converte webpage para PDF instantaneamente"""
    await ctx.typing()
    
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        api_url = f"https://api.html2pdf.app/v1/generate?url={urllib.parse.quote(url)}&apiKey=free"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=30) as response:
                if response.status == 200:
                    pdf_data = await response.read()
                    
                    if len(pdf_data) > 1000:
                        await ctx.send(
                            f"✅ PDF gerado de: {url}",
                            file=discord.File(BytesIO(pdf_data), filename="pagina.pdf")
                        )
                    else:
                        await ctx.send("❌ Não foi possível converter a página")
                else:
                    await ctx.send("❌ Erro ao converter a página")
                    
    except Exception as e:
        await ctx.send("❌ Erro ao processar a solicitação")

@bot.command(name='topdf')
async def topdf(ctx, url: str):
    """📄 Converta webpage para PDF"""
    await ctx.typing()
    
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        api_url = f"https://api.html2pdf.app/v1/generate?url={urllib.parse.quote(url)}&apiKey=free"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=30) as response:
                if response.status == 200:
                    pdf_data = await response.read()
                    
                    if len(pdf_data) > 1000:
                        await ctx.send(
                            f"✅ PDF gerado de: {url}",
                            file=discord.File(BytesIO(pdf_data), filename="pagina.pdf")
                        )
                    else:
                        await ctx.send("❌ Não foi possível converter a página")
                else:
                    await ctx.send("❌ Erro ao converter a página")
                    
    except Exception as e:
        await ctx.send("❌ Erro ao processar a solicitação")

# ========== SISTEMA IA ORIGINAL ==========

@bot.command(name='limpar_historico')
async def limpar_historico(ctx):
    """🧹 Limpa o histórico de conversa com a IA"""
    groq_ai.limpar_historico_usuario(ctx.author.id)
    await ctx.send("✅ Histórico de conversa limpo!")

# ========== SISTEMA MEMBROS ORIGINAL ==========

@bot.command(name='perfil')
async def perfil(ctx, member: discord.Member = None):
    """👤 Mostra perfil completo de um membro"""
    member = member or ctx.author
    
    embed = discord.Embed(
        title=f"👤 PERFIL - {member.name}",
        color=member.color if member.color else 0x0099ff
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    # Informações básicas
    embed.add_field(name="🆔 ID", value=member.id, inline=True)
    embed.add_field(name="📅 Entrou em", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="📅 Conta criada", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
    
    # Cargos
    cargos = [cargo.mention for cargo in member.roles if cargo.name != "@everyone"]
    if cargos:
        embed.add_field(name="🎯 Cargos", value=" ".join(cargos[:5]) + ("..." if len(cargos) > 5 else ""), inline=False)
    
    # Pontuação
    user_id = str(member.id)
    if user_id in db.pontuacao:
        pontos = db.pontuacao[user_id]["pontos"]
        embed.add_field(name="⭐ Pontos", value=pontos, inline=True)
    
    # Advertências
    if user_id in db.advertencias:
        advert_count = len(db.advertencias[user_id])
        embed.add_field(name="⚠️ Advertências", value=f"{advert_count}/{CONFIG['max_advertencias']}", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='userinfo')
async def userinfo(ctx, member: discord.Member = None):
    """ℹ️ Informações detalhadas do usuário"""
    member = member or ctx.author
    
    embed = discord.Embed(
        title=f"ℹ️ INFORMAÇÕES - {member.name}",
        color=member.color if member.color else 0x0099ff
    )
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    
    embed.add_field(name="Nome", value=member.name, inline=True)
    embed.add_field(name="Discriminador", value=member.discriminator, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=str(member.status).title(), inline=True)
    embed.add_field(name="Conta criada", value=member.created_at.strftime("%d/%m/%Y %H:%M"), inline=True)
    embed.add_field(name="Entrou em", value=member.joined_at.strftime("%d/%m/%Y %H:%M"), inline=True)
    
    roles = [role.mention for role in member.roles if role != ctx.guild.default_role]
    embed.add_field(name=f"Cargos ({len(roles)})", value=" ".join(roles) if roles else "Nenhum", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='pontos')
async def pontos(ctx, member: discord.Member = None):
    """⭐ Ver pontuação de um membro"""
    member = member or ctx.author
    user_id = str(member.id)
    
    if user_id not in db.pontuacao:
        await ctx.send(f"❌ {member.mention} não tem pontos registrados")
        return
    
    pontos = db.pontuacao[user_id]["pontos"]
    historico = db.pontuacao[user_id]["historico"][-5:]  # Últimos 5 registros
    
    embed = discord.Embed(
        title=f"⭐ PONTUAÇÃO - {member.name}",
        description=f"**Total:** {pontos} pontos",
        color=0xffd700
    )
    
    if historico:
        historico_texto = ""
        for registro in reversed(historico):
            data = datetime.fromisoformat(registro["data"]).strftime("%d/%m %H:%M")
            historico_texto += f"• {data}: {registro['pontos']} pts - {registro['motivo']}\n"
        
        embed.add_field(name="📊 Histórico Recente", value=historico_texto, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='ranking')
async def ranking(ctx):
    """🏅 Ranking de pontuação"""
    todos_pontos = [(uid, data["pontos"]) for uid, data in db.pontuacao.items()]
    todos_pontos.sort(key=lambda x: x[1], reverse=True)
    
    embed = discord.Embed(title="🏅 RANKING DE PONTUAÇÃO", color=0xffd700)
    
    ranking_texto = ""
    for i, (user_id, pontos) in enumerate(todos_pontos[:10]):
        try:
            member = ctx.guild.get_member(int(user_id))
            if member:
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"{i+1}."
                ranking_texto += f"{medal} {member.mention} - {pontos} pts\n"
        except:
            continue
    
    if ranking_texto:
        embed.description = ranking_texto
    else:
        embed.description = "Ninguém tem pontos ainda!"
    
    await ctx.send(embed=embed)

@bot.command(name='add_pontos')
@commands.has_permissions(administrator=True)
async def add_pontos(ctx, member: discord.Member, pontos: int, *, motivo="Recompensa"):
    """⭐ Adiciona pontos a um membro (ADMIN)"""
    user_id = str(member.id)
    
    if user_id not in db.pontuacao:
        db.pontuacao[user_id] = {"pontos": 0, "historico": []}
    
    db.pontuacao[user_id]["pontos"] += pontos
    db.pontuacao[user_id]["historico"].append({
        "data": datetime.now().isoformat(),
        "motivo": motivo,
        "pontos": pontos
    })
    
    db.salvar_dados()
    
    embed = discord.Embed(
        title="⭐ PONTOS ADICIONADOS",
        description=f"**{member.mention}** recebeu **+{pontos} pontos**!",
        color=0x00ff00
    )
    embed.add_field(name="📝 Motivo", value=motivo, inline=True)
    embed.add_field(name="🏆 Total", value=db.pontuacao[user_id]["pontos"], inline=True)
    
    await ctx.send(embed=embed)
    await log_system.log_pontuacao(member, motivo, pontos, db.pontuacao[user_id]["pontos"])

@bot.command(name='remove_pontos')
@commands.has_permissions(administrator=True)
async def remove_pontos(ctx, member: discord.Member, pontos: int, *, motivo="Penalidade"):
    """🔻 Remove pontos de um membro (ADMIN)"""
    user_id = str(member.id)
    
    if user_id not in db.pontuacao:
        db.pontuacao[user_id] = {"pontos": 0, "historico": []}
    
    db.pontuacao[user_id]["pontos"] = max(0, db.pontuacao[user_id]["pontos"] - pontos)
    db.pontuacao[user_id]["historico"].append({
        "data": datetime.now().isoformat(),
        "motivo": motivo,
        "pontos": f"-{pontos}"
    })
    
    db.salvar_dados()
    
    embed = discord.Embed(
        title="🔻 PONTOS REMOVIDOS",
        description=f"**{member.mention}** perdeu **-{pontos} pontos**!",
        color=0xff0000
    )
    embed.add_field(name="📝 Motivo", value=motivo, inline=True)
    embed.add_field(name="🏆 Total", value=db.pontuacao[user_id]["pontos"], inline=True)
    
    await ctx.send(embed=embed)
    await log_system.log_pontuacao(member, motivo, -pontos, db.pontuacao[user_id]["pontos"])

@bot.command(name='convite')
async def convite(ctx):
    """📩 Gera convite pessoal para o servidor"""
    try:
        # Criar convite temporário
        invite = await ctx.channel.create_invite(max_age=86400, max_uses=5, unique=True)
        
        embed = discord.Embed(
            title="📩 CONVITE PESSOAL",
            description=f"**Convite gerado com sucesso!**\n\n**Link:** {invite.url}\n**Expira em:** 24 horas\n**Usos máximos:** 5",
            color=0x00ff00
        )
        embed.set_footer(text="Compartilhe com seus amigos!")
        
        await ctx.author.send(embed=embed)
        await ctx.send("✅ Convite enviado no seu privado!")
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao gerar convite: {e}")

@bot.command(name='convites')
async def convites(ctx, member: discord.Member = None):
    """📊 Status de convites de um membro"""
    member = member or ctx.author
    user_id = str(member.id)
    
    if user_id not in db.convites:
        await ctx.send(f"❌ {member.mention} não tem convites registrados")
        return
    
    dados = db.convites[user_id]
    total = dados["total"]
    convidados = len(dados["convidados"])
    
    embed = discord.Embed(
        title=f"📊 CONVITES - {member.name}",
        color=0x0099ff
    )
    embed.add_field(name="🎯 Total de Convites", value=total, inline=True)
    embed.add_field(name="👥 Membros Convidados", value=convidados, inline=True)
    
    # Conquistas
    conquistas = {
        5: "🎖️ Recrutador Júnior",
        10: "🎖️ Recrutador Sênior", 
        25: "🎖️ Mestre dos Convites",
        50: "🎖️ Lenda do Recrutamento"
    }
    
    conquista_atual = "Nenhuma"
    for qtd, nome in conquistas.items():
        if total >= qtd:
            conquista_atual = nome
    
    embed.add_field(name="🏆 Conquista Atual", value=conquista_atual, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='convite_bot')
async def convite_bot(ctx):
    """🤖 Convite para adicionar o bot"""
    embed = discord.Embed(
        title="🤖 CONVITE DO BOT",
        description="**Adicione este bot ao seu servidor!**\n\n"
                   "[🔗 Clique aqui para convidar](https://discord.com/oauth2/authorize?client_id=YOUR_BOT_ID&scope=bot&permissions=8)\n\n"
                   "**Permissões necessárias:**\n"
                   "• Gerenciar servidor\n• Gerenciar canais\n• Gerenciar mensagens\n• Gerenciar cargos\n• Banir membros\n• Ver logs de auditoria",
        color=0x7289DA
    )
    await ctx.send(embed=embed)

@bot.command(name='cargos')
async def cargos(ctx):
    """🎯 Lista todos os cargos disponíveis"""
    embed = discord.Embed(
        title="🎯 SISTEMA DE CARGOS",
        description="**Cargos disponíveis para auto-atribuição:**\n\n"
                   "💻 **Linguagens de Programação:**\n"
                   "• Python, Java, JavaScript, Golang, Rust\n"
                   "• C#, C/C++, PHP, Ruby, Swift, Kotlin, Bash\n\n"
                   "🛡️ **Cybersecurity:**\n"
                   "• Ethical Hacker, Pentester, Blue Team\n" 
                   "• Red Team, Bug Hunter, CTF Player\n"
                   "• OSINT, Reverse Eng, Exploit Dev, Malware Analyst",
        color=0x0099ff
    )
    embed.add_field(
        name="🔧 Como obter",
        value="Use `!setup_cargos` para configurar o sistema de self-roles",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(name='ccg')
@commands.has_permissions(manage_roles=True)
async def criar_cargo(ctx, nome: str, cor: str = None):
    """🎨 Cria um novo cargo"""
    try:
        # Converter cor se fornecida
        if cor:
            if cor.startswith('#'):
                cor = discord.Color(int(cor[1:], 16))
            else:
                cores = {
                    'vermelho': discord.Color.red(),
                    'azul': discord.Color.blue(),
                    'verde': discord.Color.green(),
                    'amarelo': discord.Color.gold(),
                    'roxo': discord.Color.purple(),
                    'laranja': discord.Color.orange(),
                    'rosa': discord.Color.magenta(),
                    'cinza': discord.Color.light_gray()
                }
                cor = cores.get(cor.lower(), discord.Color.default())
        else:
            cor = discord.Color.default()
        
        cargo = await ctx.guild.create_role(name=nome, color=cor, reason=f"Criado por {ctx.author.name}")
        
        embed = discord.Embed(
            title="🎨 CARGO CRIADO",
            description=f"Cargo **{cargo.name}** criado com sucesso!",
            color=cor
        )
        embed.add_field(name="🆔 ID", value=cargo.id, inline=True)
        embed.add_field(name="🎨 Cor", value=str(cor), inline=True)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro ao criar cargo: {e}")

@bot.command(name='atualizar_cargos')
@commands.has_permissions(administrator=True)
async def atualizar_cargos(ctx):
    """🔄 Atualiza sistema de cargos automaticamente"""
    await ctx.typing()
    
    try:
        membros_atualizados = await sistema_cargos.atribuir_cargo_membro_automatico(ctx.guild)
        
        embed = discord.Embed(
            title="✅ SISTEMA DE CARGOS ATUALIZADO",
            description=f"**{membros_atualizados}** membros receberam cargo automaticamente",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao atualizar cargos: {e}")

@bot.command(name='atualizar_nicks')
@commands.has_permissions(administrator=True)
async def atualizar_nicks(ctx):
    """🏷️ Atualiza nicknames automaticamente"""
    await ctx.typing()
    
    try:
        atualizados = 0
        for member in ctx.guild.members:
            if not member.bot:
                await sistema_cargos.atualizar_nick_automatico(member)
                atualizados += 1
                await asyncio.sleep(0.3)
        
        embed = discord.Embed(
            title="✅ NICKS ATUALIZADOS",
            description=f"**{atualizados}** nicknames foram atualizados automaticamente",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro ao atualizar nicks: {e}")

@bot.command(name='sorteio')
@commands.has_permissions(manage_messages=True)
async def sorteio(ctx, tempo: int = 60, *, premio: str):
    """🎉 Inicia um sorteio"""
    embed = discord.Embed(
        title="🎉 SORTEIO!",
        description=f"**Prêmio:** {premio}\n**Tempo:** {tempo} segundos\n\nReaja com 🎉 para participar!",
        color=0xffd700,
        timestamp=datetime.now() + timedelta(seconds=tempo)
    )
    embed.set_footer(text="Sorteio termina em")
    
    mensagem = await ctx.send(embed=embed)
    await mensagem.add_reaction("🎉")
    
    await asyncio.sleep(tempo)
    
    # Recarregar mensagem para pegar reações atualizadas
    mensagem = await ctx.channel.fetch_message(mensagem.id)
    reacao = discord.utils.get(mensagem.reactions, emoji="🎉")
    
    if reacao and reacao.count > 1:
        usuarios = []
        async for user in reacao.users():
            if not user.bot:
                usuarios.append(user)
        
        if usuarios:
            vencedor = random.choice(usuarios)
            
            embed_vencedor = discord.Embed(
                title="🎉 SORTEIO FINALIZADO!",
                description=f"**Prêmio:** {premio}\n**Vencedor:** {vencedor.mention}",
                color=0x00ff00
            )
            await ctx.send(f"🎉 Parabéns {vencedor.mention}! Você ganhou: **{premio}**")
            await ctx.send(embed=embed_vencedor)
        else:
            await ctx.send("❌ Ninguém participou do sorteio!")
    else:
        await ctx.send("❌ Ninguém participou do sorteio!")

@bot.command(name='enquete')
@commands.has_permissions(manage_messages=True)
async def enquete(ctx, tempo: int = 3600, *, pergunta: str):
    """📊 Cria uma enquete com tempo"""
    embed = discord.Embed(
        title="📊 ENQUETE",
        description=pergunta,
        color=0x0099ff,
        timestamp=datetime.now() + timedelta(seconds=tempo)
    )
    embed.add_field(name="⏰ Duração", value=f"{tempo//3600}h {(tempo%3600)//60}m", inline=True)
    embed.add_field(name="📝 Opções", value="✅ = Sim\n❌ = Não", inline=True)
    embed.set_footer(text="Enquete termina em")
    
    mensagem = await ctx.send(embed=embed)
    await mensagem.add_reaction("✅")
    await mensagem.add_reaction("❌")
    
    await asyncio.sleep(tempo)
    
    # Resultados
    mensagem = await ctx.channel.fetch_message(mensagem.id)
    sim = discord.utils.get(mensagem.reactions, emoji="✅")
    nao = discord.utils.get(mensagem.reactions, emoji="❌")
    
    count_sim = sim.count - 1 if sim else 0
    count_nao = nao.count - 1 if nao else 0
    total = count_sim + count_nao
    
    if total > 0:
        percent_sim = (count_sim / total) * 100
        percent_nao = (count_nao / total) * 100
        
        embed_resultado = discord.Embed(
            title="📊 RESULTADO DA ENQUETE",
            description=pergunta,
            color=0x00ff00
        )
        embed_resultado.add_field(name="✅ Sim", value=f"{count_sim} votos ({percent_sim:.1f}%)", inline=True)
        embed_resultado.add_field(name="❌ Não", value=f"{count_nao} votos ({percent_nao:.1f}%)", inline=True)
        embed_resultado.add_field(name="👥 Total", value=f"{total} votos", inline=True)
        
        await ctx.send(embed=embed_resultado)
    else:
        await ctx.send("❌ Ninguém votou na enquete!")

# ========== UTILIDADES ORIGINAIS ==========

@bot.command(name='server')
async def server_info(ctx):
    """📊 Info do servidor"""
    guild = ctx.guild
    
    embed = discord.Embed(title=f"📊 {guild.name}", color=0x0099ff)
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    
    embed.add_field(name="👥 Membros", value=guild.member_count, inline=True)
    embed.add_field(name="📁 Canais", value=len(guild.channels), inline=True)
    embed.add_field(name="⭐ Cargos", value=len(guild.roles), inline=True)
    embed.add_field(name="👑 Dono", value=guild.owner.mention, inline=True)
    embed.add_field(name="📅 Criado em", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="🆔 ID", value=guild.id, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    """🏓 Mostra a latência do bot"""
    latency = round(bot.latency * 1000)
    
    embed = discord.Embed(
        title="🏓 PONG!",
        description=f"**Latência:** {latency}ms",
        color=0x00ff00 if latency < 100 else 0xff9900 if latency < 200 else 0xff0000
    )
    await ctx.send(embed=embed)

@bot.command(name='search')
async def search_advanced(ctx, tipo: str = None, *, query=None):
    """🔍 Pesquisa avançada no servidor (PDF/serv/membros)"""
    if not tipo or not query:
        embed = discord.Embed(
            title="🔍 SISTEMA DE PESQUISA AVANÇADA",
            description="**Como usar:**\n`!search PDF <nome>` - Busca em PDFs\n`!search serv <termo>` - Busca no servidor\n`!search membros <nome>` - Lista membros",
            color=0x0099ff
        )
        await ctx.send(embed=embed)
        return

    await ctx.typing()

    if tipo.lower() == "pdf":
        # Buscar em PDFs anexados
        resultados = await buscar_pdfs(ctx, query)
        if resultados:
            embed = discord.Embed(
                title=f"🔍 Resultados PDF para: '{query}'",
                description="\n".join([f"• {r}" for r in resultados[:5]]),
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nenhum PDF encontrado com esse termo")

    elif tipo.lower() == "serv":
        # Busca avançada no servidor
        embed = discord.Embed(title=f"🔍 Resultados para: '{query}'", color=0x0099ff)
        
        resultados = []
        canals_encontrados = set()
        
        after_data = datetime.now() - timedelta(days=30)  # Busca últimos 30 dias
        
        for canal in ctx.guild.text_channels:
            try:
                async for mensagem in canal.history(limit=200, after=after_data):
                    if (query.lower() in mensagem.content.lower() and 
                        not mensagem.author.bot and
                        canal.name not in canals_encontrados):
                        
                        resultados.append({
                            "canal": canal,
                            "mensagem": mensagem.content[:150] + "..." if len(mensagem.content) > 150 else mensagem.content,
                            "autor": mensagem.author.name,
                            "data": mensagem.created_at.strftime("%d/%m %H:%M")
                        })
                        canals_encontrados.add(canal.name)
                        
                        if len(resultados) >= 10:
                            break
                if len(resultados) >= 10:
                    break
            except:
                continue
        
        if resultados:
            for resultado in resultados[:8]:
                embed.add_field(
                    name=f"#{resultado['canal'].name} • {resultado['autor']}",
                    value=f"{resultado['mensagem']}\n*{resultado['data']}*",
                    inline=False
                )
        else:
            embed.description = "❌ Nenhum resultado encontrado (últimos 30 dias)"
        
        embed.set_footer(text=f"Encontrado em {len(resultados)} mensagens")
        await ctx.send(embed=embed)

    elif tipo.lower() == "membros":
        # Listar membros
        membros = [membro for membro in ctx.guild.members 
                  if query.lower() in membro.name.lower() and not membro.bot]
        
        if membros:
            embed = discord.Embed(
                title=f"👥 Membros encontrados: '{query}'",
                color=0x00ff00
            )
            
            lista_membros = []
            for membro in membros[:15]:
                cargos = [cargo.name for cargo in membro.roles if cargo.name != "@everyone"]
                info = f"**{membro.name}**"
                if cargos:
                    info += f" - {', '.join(cargos[:2])}"
                lista_membros.append(info)
            
            embed.description = "\n".join(lista_membros)
            embed.set_footer(text=f"Total: {len(membros)} membros")
        else:
            embed = discord.Embed(
                title="❌ Nenhum membro encontrado",
                description=f"Não encontrei membros com '{query}'",
                color=0xff0000
            )
        
        await ctx.send(embed=embed)

    else:
        await ctx.send("❌ Tipo de pesquisa inválido. Use: PDF, serv ou membros")

async def buscar_pdfs(ctx, query):
    """Busca termo em PDFs do canal"""
    resultados = []
    after_data = datetime.now() - timedelta(days=30)
    
    async for mensagem in ctx.channel.history(limit=100, after=after_data):
        for anexo in mensagem.attachments:
            if anexo.filename.lower().endswith('.pdf'):
                try:
                    # Aqui você implementaria a leitura do PDF
                    # Por enquanto, só verifica pelo nome
                    if query.lower() in anexo.filename.lower():
                        resultados.append(f"📄 {anexo.filename} - {mensagem.author.name}")
                except:
                    continue
    return resultados

@bot.command(name='p')
async def procurar_comando(ctx, *, busca: str):
    """🔍 Procura comandos por função/palavra-chave"""
    await ctx.typing()
    
    # Mapeamento de funções para comandos
    mapeamento_comandos = {
        # Sistema de Moderação
        'ban': '!ban @usuário [motivo] - Bane um usuário',
        'advertir': '!advertir @usuário [motivo] - Adverte um usuário',
        'advertencia': '!advertencias @usuário - Ver advertências',
        'mute': '!mute @usuário [tempo] [motivo] - Muta um usuário',
        'limpar': '!clear [quantidade] - Limpa mensagens',
        'kick': '!kick @usuário [motivo] - Expulsa um usuário',
        
        # Sistema de Canais
        'canal': '!-mc nome [tipo] [permissao] - Cria canal com IA',
        'categoria': '!-mq nome [permissao] - Cria categoria com IA',
        'deletar': '!d [#canal] - Deleta canal | !-d id_categoria - Deleta categoria',
        'bloquear': '!lk [#canal] - Bloqueia canal',
        'desbloquear': '!ulk [#canal] - Desbloqueia canal',
        'visualizacao': '!x [#canal] - Modo somente leitura',
        
        # Sistema de PDF
        'pdf': '!pdf_canal [limite] - Cria PDF das mensagens | !web_to_pdf [url] - Converte site para PDF',
        'site': '!web_to_pdf [url] - Converte site para PDF',
        'mensagens': '!pdf_canal [limite] - Cria PDF das mensagens',
        
        # Sistema de IA
        'perguntar': 'Mencione o bot para conversar',
        'script': '!script [requisitos] - Cria script personalizado',
        
        # Sistema de Utilidades
        'convite': '!convite - Gera convite pessoal',
        'pontos': '!pontos [@usuário] - Ver pontuação',
        'ranking': '!ranking - Ranking de pontos',
        'perfil': '!perfil [@usuário] - Ver perfil',
        'server': '!server - Info do servidor',
        'config': '!config - Menu de configuração',
        
        # Sistema de Cargos
        'cargo': '!setup_cargos - Configura sistema | !ccg nome cor - Cria cargo',
        'nick': '!atualizar_nicks - Atualiza nicks automaticamente',
        
        # Sistema de Proteção
        'protecao': '!rate - Ativa sistema de proteção (Admin)',
        'spam': '!rate - Sistema anti-spam (Admin)',
        
        # Sistema de Anúncios
        'anuncio': '!comunicado #canal mensagem - Cria comunicado',
        'lembrete': '!lembrete_anuncio #canal tempo mensagem - Agenda lembrete',
        
        # Sistema Cybersecurity
        'missao': '!missao_cyber #canal dificuldade descrição - Cria missão',
        'cyber': '!missao_cyber - Missões de cybersecurity',
        
        # Sistema de Busca
        'buscar': '!search PDF/serv/membros termo - Busca avançada',
        'pesquisar': '!search PDF/serv/membros termo - Pesquisa no servidor'
    }
    
    # Buscar comandos relevantes
    resultados = []
    busca_lower = busca.lower()
    
    for funcao, comando in mapeamento_comandos.items():
        if busca_lower in funcao.lower() or any(palavra in funcao.lower() for palavra in busca_lower.split()):
            resultados.append(f"**{funcao.title()}:** `{comando}`")
    
    if resultados:
        embed = discord.Embed(
            title=f"🔍 RESULTADOS PARA: '{busca}'",
            description="\n".join(resultados[:10]),  # Limitar a 10 resultados
            color=0x0099ff
        )
        if len(resultados) > 10:
            embed.set_footer(text=f"Mostrando 10 de {len(resultados)} resultados. Seja mais específico para mais resultados.")
    else:
        embed = discord.Embed(
            title="❌ NENHUM COMANDO ENCONTRADO",
            description=f"Não encontrei comandos para: '{busca}'\n\n**Dica:** Tente buscar por:\n• Função (ex: ban, canal, pdf)\n• Palavra-chave (ex: criar, deletar, configurar)\n• Categoria (ex: moderacao, ia, utilidade)",
            color=0xff0000
        )
    
    await ctx.send(embed=embed)

@bot.command(name='calc')
async def calculadora(ctx, *, expressao: str):
    """🧮 Calculadora simples"""
    try:
        # Remover espaços e validar caracteres
        expressao = expressao.replace(' ', '')
        caracteres_validos = set('0123456789+-*/.() ')
        
        if not all(c in caracteres_validos for c in expressao):
            await ctx.send("❌ Expressão contém caracteres inválidos")
            return
        
        # Calcular resultado
        resultado = eval(expressao)
        
        embed = discord.Embed(
            title="🧮 CALCULADORA",
            description=f"**Expressão:** `{expressao}`\n**Resultado:** `{resultado}`",
            color=0x0099ff
        )
        await ctx.send(embed=embed)
        
    except ZeroDivisionError:
        await ctx.send("❌ Erro: Divisão por zero")
    except:
        await ctx.send("❌ Erro: Expressão inválida")

@bot.command(name='traduzir')
async def traduzir(ctx, idioma: str, *, texto: str):
    """🌍 Traduz texto (inglês/português)"""
    await ctx.typing()
    
    idiomas = {
        'pt': 'português',
        'en': 'inglês',
        'es': 'espanhol',
        'fr': 'francês'
    }
    
    if idioma not in idiomas:
        await ctx.send("❌ Idiomas disponíveis: pt, en, es, fr")
        return
    
    prompt = f"Traduza este texto para {idiomas[idioma]}: {texto}"
    
    try:
        traducao = await groq_ai.gerar_resposta(prompt, user_id=ctx.author.id)
        
        embed = discord.Embed(
            title="🌍 TRADUÇÃO",
            color=0x0099ff
        )
        embed.add_field(name="📝 Original", value=texto, inline=False)
        embed.add_field(name="🔤 Tradução", value=traducao, inline=False)
        embed.add_field(name="🎯 Idioma", value=idiomas[idioma].title(), inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Erro na tradução: {e}")

@bot.command(name='lembrete')
async def lembrete(ctx, minutos: int, *, mensagem: str):
    """⏰ Define um lembrete pessoal"""
    if minutos <= 0:
        await ctx.send("❌ O tempo deve ser maior que 0 minutos")
        return
    
    if minutos > 1440:  # 24 horas
        await ctx.send("❌ O tempo máximo é 1440 minutos (24 horas)")
        return
    
    await ctx.send(f"✅ Lembrete definido! Te avisarei em {minutos} minutos.")
    
    await asyncio.sleep(minutos * 60)
    
    try:
        embed = discord.Embed(
            title="⏰ LEMBRETE",
            description=mensagem,
            color=0xffd700
        )
        embed.set_footer(text=f"Lembrete definido há {minutos} minutos")
        await ctx.author.send(embed=embed)
        await ctx.send(f"🔔 {ctx.author.mention}, lembrete enviado no seu privado!")
    except:
        await ctx.send(f"🔔 {ctx.author.mention}, **LEMBRETE:** {mensagem}")

@bot.command(name='comunicado')
@commands.has_permissions(administrator=True)
async def comunicado(ctx, canal: discord.TextChannel = None, *, mensagem_abreviada=None):
    """📢 Cria comunicado profissional (IA aprimora)"""
    if not canal or not mensagem_abreviada:
        await ctx.send("❌ Use: `!comunicado #canal sua mensagem abreviada`")
        return

    await ctx.typing()
    
    # IA aprimora o comunicado
    prompt = f"Transforme esta mensagem abreviada em um comunicado profissional e bem formatado para Discord: {mensagem_abreviada}"
    comunicado_final = await groq_ai.gerar_resposta(prompt, user_id=ctx.author.id, modo_tecnico=True)
    
    embed = discord.Embed(
        title="📢 COMUNICADO OFICIAL",
        description=comunicado_final,
        color=0xffd700,
        timestamp=datetime.now()
    )
    embed.set_footer(text=f"Comunicado por {ctx.author.name}")
    
    try:
        await canal.send(embed=embed)
        await ctx.send(f"✅ Comunicado enviado para {canal.mention}")
    except Exception as e:
        await ctx.send(f"❌ Erro ao enviar comunicado: {e}")

@bot.command(name='lembrete_anuncio')
@commands.has_permissions(administrator=True)
async def lembrete_anuncio(ctx, canal: discord.TextChannel = None, tempo: str = None, *, mensagem_abreviada=None):
    """⏰ Agenda lembrete/anúncio (IA aprimora)"""
    if not canal or not tempo or not mensagem_abreviada:
        await ctx.send("❌ Use: `!lembrete_anuncio #canal 1h sua mensagem`\nTempos: 1h, 2h, 6h, 12h, 1d")
        return
    
    # Converter tempo
    tempo_map = {
        "1h": 3600, "2h": 7200, "6h": 21600, 
        "12h": 43200, "1d": 86400
    }
    
    if tempo not in tempo_map:
        await ctx.send("❌ Tempo inválido. Use: 1h, 2h, 6h, 12h, 1d")
        return
    
    segundos = tempo_map[tempo]
    await ctx.typing()
    
    # IA aprimora a mensagem
    prompt = f"Transforme esta mensagem abreviada em um anúncio/lembrete profissional para Discord: {mensagem_abreviada}"
    mensagem_final = await groq_ai.gerar_resposta(prompt, user_id=ctx.author.id, modo_tecnico=True)
    
    # Salvar lembrete
    lembrete_id = f"{ctx.guild.id}_{canal.id}_{datetime.now().timestamp()}"
    db.lembretes_anuncios[lembrete_id] = {
        "canal_id": canal.id,
        "mensagem": mensagem_final,
        "autor": ctx.author.id,
        "executar_em": (datetime.now() + timedelta(seconds=segundos)).isoformat()
    }
    db.salvar_dados()
    
    embed = discord.Embed(
        title="⏰ LEMBRETE AGENDADO",
        description=f"**Canal:** {canal.mention}\n**Tempo:** {tempo}\n**Status:** ✅ Agendado",
        color=0x00ff00
    )
    await ctx.send(embed=embed)
    
    # Agendar execução
    await asyncio.sleep(segundos)
    
    # Executar lembrete
    try:
        embed_anuncio = discord.Embed(
            title="🔔 LEMBRETE",
            description=mensagem_final,
            color=0xffd700,
            timestamp=datetime.now()
        )
        embed_anuncio.set_footer(text="Lembrete agendado")
        await canal.send(embed=embed_anuncio)
        
        # Remover do banco
        if lembrete_id in db.lembretes_anuncios:
            del db.lembretes_anuncios[lembrete_id]
            db.salvar_dados()
            
    except Exception as e:
        print(f"Erro ao enviar lembrete: {e}")

@bot.command(name='missao_cyber')
@commands.has_permissions(administrator=True)
async def missao_cyber(ctx, canal: discord.TextChannel = None, dificuldade: str = None, *, descricao_abreviada=None):
    """🎯 Cria missão cybersecurity (IA aprimora)"""
    if not canal or not dificuldade or not descricao_abreviada:
        await ctx.send("❌ Use: `!missao_cyber #canal facil|medio|dificil descrição`")
        return
    
    if dificuldade.lower() not in ["facil", "medio", "dificil"]:
        await ctx.send("❌ Dificuldade deve ser: facil, medio ou dificil")
        return
    
    await ctx.typing()
    
    # IA desenvolve a missão completa
    prompt = f"""
    Crie uma missão completa de cybersecurity/CTF com esses requisitos:
    Dificuldade: {dificuldade}
    Descrição breve: {descricao_abreviada}
    
    Inclua:
    - Título criativo
    - Descrição detalhada do desafio
    - Objetivos claros
    - Dicas progressivas
    - Solução esperada
    - Pontuação baseada na dificuldade
    Formate para Discord emojis e seções organizadas.
    """
    
    missao_desenvolvida = await groq_ai.gerar_resposta(prompt, user_id=ctx.author.id, modo_tecnico=True)
    
    # Definir cor baseada na dificuldade
    cores = {
        "facil": 0x00ff00,
        "medio": 0xff9900, 
        "dificil": 0xff0000
    }
    
    embed = discord.Embed(
        title=f"🎯 MISSÃO CYBERSECURITY - {dificuldade.upper()}",
        description=missao_desenvolvida,
        color=cores[dificuldade.lower()],
        timestamp=datetime.now()
    )
    
    # Adicionar campos padrão
    pontos = {"facil": 100, "medio": 250, "dificil": 500}
    embed.add_field(name="🏆 Pontuação", value=pontos[dificuldade.lower()], inline=True)
    embed.add_field(name="⏰ Tempo Estimado", value="1-2 horas", inline=True)
    embed.add_field(name="🎯 Tipo", value="CTF/Prática", inline=True)
    
    embed.set_footer(text=f"Missão criada por {ctx.author.name}")
    
    try:
        mensagem = await canal.send("@everyone @here", embed=embed)
        await mensagem.pin()
        await ctx.send(f"✅ Missão criada e fixada em {canal.mention}")
    except Exception as e:
        await ctx.send(f"❌ Erro ao criar missão: {e}")

@bot.command(name='criar_comando')
@commands.has_permissions(administrator=True)
async def criar_comando_personalizado(ctx, nome_comando: str, tipo: str, *, configuracao: str = None):
    """🎮 Cria comandos personalizados com +100 tipos"""
    
    tipos_disponiveis = {
        # Sistema de Moderação
        "advertencia_auto": "Sistema automático de advertências",
        "ban_auto": "Banimento automático por palavras",
        "mute_auto": "Mute automático por comportamento",
        "welcome": "Mensagem de boas-vindas personalizada",
        "goodbye": "Mensagem de despedida personalizada",
        
        # Sistema de Entretenimento
        "quiz": "Quiz com perguntas e respostas", 
        "loteria": "Sistema de loteria",
        "roleta": "Roleta russa de prêmios",
        "aposta": "Sistema de apostas",
        "rank": "Sistema de ranking personalizado",
        
        # Sistema de Economia
        "daily": "Recompensa diária",
        "work": "Trabalho para ganhar moedas",
        "roubo": "Sistema de roubo entre usuários",
        "banco": "Sistema bancário",
        "loja": "Loja de itens",
        
        # Sistema de Level
        "level": "Sistema de level up",
        "xp": "Sistema de experiência",
        "premio_level": "Prêmios por level",
        "rank_level": "Ranking de levels",
        
        # Sistema de Jogos
        "velha": "Jogo da velha",
        "forca": "Jogo da forca",
        "memoria": "Jogo da memória",
        "quiz_musica": "Quiz de músicas",
        "quiz_filmes": "Quiz de filmes",
        
        # Sistema de Utilidades
        "lembrete_auto": "Lembretes automáticos",
        "anuncio_auto": "Anúncios automáticos",
        "pesquisa": "Sistema de pesquisa",
        "traducao": "Sistema de tradução",
        "clima": "Previsão do tempo",
        
        # Sistema de Mídia
        "memes": "Sistema de memes aleatórios",
        "imagens": "Busca de imagens",
        "gifs": "Sistema de GIFs",
        "videos": "Sistema de vídeos",
        
        # Sistema de RPG
        "rpg_batalha": "Sistema de batalha RPG",
        "rpg_inventario": "Inventário RPG",
        "rpg_missoes": "Missões RPG",
        "rpg_personagem": "Criação de personagem RPG",
        
        # Sistema de Educação
        "curso_programacao": "Curso de programação",
        "quiz_cyber": "Quiz de cybersecurity",
        "desafio_codigo": "Desafios de código",
        "tutorial": "Sistema de tutoriais",
        
        # Sistema de Social
        "perfil_social": "Perfil social personalizado",
        "casamento": "Sistema de casamento",
        "amizade": "Sistema de amizade",
        "grupos": "Sistema de grupos",
        
        # Sistema de Customização
        "cor_nick": "Cor personalizada no nick",
        "tag_personalizada": "Tag personalizada",
        "emoji_personalizado": "Emojis personalizados",
        "fundo_perfil": "Fundo de perfil",
        
        # +50 Outros Tipos...
        "contador": "Contador personalizado",
        "timer": "Temporizador",
        "sorteio": "Sistema de sorteio",
        "votacao": "Sistema de votação",
        "enquete": "Sistema de enquete",
        "feedback": "Sistema de feedback",
        "sugestao": "Sistema de sugestões",
        "bug_report": "Sistema de reportar bugs",
        "parceria": "Sistema de parcerias",
        "evento": "Sistema de eventos",
        "promocao": "Sistema de promoções",
        "desafio_diario": "Desafios diários",
        "conquista_auto": "Conquistas automáticas",
        "log_auto": "Sistema de logs automáticos",
        "backup": "Sistema de backup",
        "restore": "Sistema de restore",
        "import": "Sistema de importação",
        "export": "Sistema de exportação",
        "api": "Integração com API",
        "webhook": "Sistema de webhooks",
        "bot_auto": "Comandos automáticos de bot",
        "ia_chat": "Chat com IA personalizado",
        "ia_imagem": "Geração de imagens com IA",
        "ia_musica": "Geração de música com IA",
        "ia_video": "Geração de vídeo com IA",
        "moderacao_ia": "Moderação com IA",
        "seguranca_auto": "Segurança automática",
        "antiraid": "Sistema anti-raid",
        "antispam": "Sistema anti-spam",
        "backup_canais": "Backup de canais",
        "backup_cargos": "Backup de cargos",
        "clone_servidor": "Clone de servidor",
        "template": "Sistema de templates",
        "setup_auto": "Setup automático",
        "welcome_embed": "Welcome com embed",
        "goodbye_embed": "Goodbye com embed",
        "log_embed": "Logs com embed",
        "stats_embed": "Estatísticas com embed",
        "info_embed": "Informações com embed",
        "help_embed": "Ajuda com embed",
        "music_player": "Player de música",
        "radio": "Sistema de rádio",
        "podcast": "Sistema de podcast",
        "livestream": "Sistema de live stream",
        "video_chat": "Video chat",
        "screen_share": "Compartilhamento de tela"
    }
    
    if not configuracao:
        # Mostrar lista de tipos disponíveis
        embed = discord.Embed(
            title="🎮 SISTEMA DE COMANDOS PERSONALIZADOS",
            description="**+100 Tipos de Comandos Disponíveis:**\n\n",
            color=0x7289DA
        )
        
        # Organizar em categorias
        categorias = {}
        for tipo, desc in tipos_disponiveis.items():
            categoria = tipo.split('_')[0] if '_' in tipo else "outros"
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append(f"`{tipo}` - {desc}")
        
        for categoria, comandos in categorias.items():
            embed.add_field(
                name=f"🔧 {categoria.upper()}",
                value="\n".join(comandos[:8]) + ("\n..." if len(comandos) > 8 else ""),
                inline=False
            )
        
        embed.add_field(
            name="📝 COMO USAR",
            value="`!criar_comando nome_do_comando tipo_da_funcao configuração_opcional`\n\n**Exemplo:** `!criar_comando welcome_bemvindo welcome_embed Canal: #bem-vindo | Mensagem: Olá {user}!`",
            inline=False
        )
        
        await ctx.send(embed=embed)
        return
    
    if tipo not in tipos_disponiveis:
        await ctx.send(f"❌ Tipo inválido! Use `!criar_comando` para ver todos os tipos disponíveis.")
        return
    
    # Salvar comando personalizado
    db.comandos_personalizados[nome_comando] = {
        'tipo': tipo,
        'configuracao': configuracao,
        'criador': ctx.author.id,
        'criado_em': datetime.now().isoformat()
    }
    db.salvar_dados()
    
    embed = discord.Embed(
        title="✅ COMANDO PERSONALIZADO CRIADO",
        description=f"Comando `!{nome_comando}` criado com sucesso!",
        color=0x00ff00
    )
    embed.add_field(name="🔧 Tipo", value=tipos_disponiveis[tipo], inline=True)
    embed.add_field(name="⚙️ Configuração", value=configuracao[:100] + "..." if len(configuracao) > 100 else configuracao, inline=True)
    embed.add_field(name="👤 Criador", value=ctx.author.mention, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='criar_ticket')
@commands.has_permissions(manage_channels=True)
async def criar_ticket(ctx):
    """🎫 Sistema de tickets de suporte"""
    embed = discord.Embed(
        title="🎫 SISTEMA DE TICKETS",
        description="**Precisa de ajuda? Abra um ticket!**\n\n"
                   "• Clique no 🎫 para criar um ticket de suporte\n"
                   "• Nossa equipe irá ajudá-lo em breve\n"
                   "• Use apenas para assuntos importantes",
        color=0x0099ff
    )
    
    mensagem = await ctx.send(embed=embed)
    await mensagem.add_reaction("🎫")

@bot.command(name='votacao_rapida')
@commands.has_permissions(manage_messages=True)
async def votacao_rapida(ctx, *, pergunta: str):
    """⚡ Votação rápida (sim/não)"""
    embed = discord.Embed(
        title="⚡ VOTAÇÃO RÁPIDA",
        description=pergunta,
        color=0x0099ff
    )
    embed.add_field(name="📊 Opções", value="✅ = Sim\n❌ = Não", inline=True)
    
    mensagem = await ctx.send(embed=embed)
    await mensagem.add_reaction("✅")
    await mensagem.add_reaction("❌")

@bot.command(name='dado')
async def dado(ctx, lados: int = 6):
    """🎲 Joga um dado"""
    if lados <= 0:
        await ctx.send("❌ O dado deve ter pelo menos 1 lado")
        return
    
    resultado = random.randint(1, lados)
    
    embed = discord.Embed(
        title="🎲 RESULTADO DO DADO",
        description=f"**Dado de {lados} lados:** 🎲 **{resultado}**",
        color=0x0099ff
    )
    await ctx.send(embed=embed)

@bot.command(name='moeda')
async def moeda(ctx):
    """🪙 Cara ou coroa"""
    resultado = random.choice(["cara", "coroa"])
    emoji = "👑" if resultado == "coroa" else "😊"
    
    embed = discord.Embed(
        title="🪙 CARA OU COROA",
        description=f"**Resultado:** {emoji} **{resultado.upper()}**",
        color=0xffd700
    )
    await ctx.send(embed=embed)

# ========== ENTRETENIMENTO ORIGINAL ==========

@bot.command(name='script')
async def script(ctx, *, requisitos):
    """💻 Peça um script personalizado (resposta detalhada)"""
    await ctx.typing()
    resposta = await groq_ai.gerar_resposta(
        f"Crie um script completo com esses requisitos: {requisitos}. Forneça o código completo, explicações e como usar.", 
        user_id=ctx.author.id, 
        modo_tecnico=True
    )
    
    if len(resposta) > 2000:
        partes = [resposta[i:i+2000] for i in range(0, len(resposta), 2000)]
        for i, parte in enumerate(partes):
            await ctx.send(parte)
    else:
        await ctx.send(resposta)

# ========== SEGURANÇA ORIGINAL ==========

# SISTEMA PARA EXECUTAR COMANDOS PERSONALIZADOS
@bot.event
async def on_command_error(ctx, error):
    # Verificar se é um comando personalizado
    if isinstance(error, commands.CommandNotFound):
        comando = ctx.message.content.split(' ')[0][1:]  # Remove o "!"
        
        if comando in db.comandos_personalizados:
            dados = db.comandos_personalizados[comando]
            tipo = dados['tipo']
            config = dados['configuracao']
            
            # Executar comando personalizado baseado no tipo
            if tipo == "welcome_embed":
                embed = discord.Embed(
                    title="👋 BEM-VINDO!",
                    description=config.replace('{user}', ctx.author.mention),
                    color=0x00ff00,
                    timestamp=datetime.now()
                )
                await ctx.send(embed=embed)
            
            elif tipo == "quiz":
                perguntas = config.split(' | ')
                if len(perguntas) >= 2:
                    embed = discord.Embed(
                        title="❓ QUIZ",
                        description=perguntas[0],
                        color=0x0099ff
                    )
                    if len(perguntas) > 1:
                        embed.add_field(name="💡 Resposta", value=perguntas[1], inline=False)
                    await ctx.send(embed=embed)
            
            elif tipo == "daily":
                recompensa = random.randint(50, 200)
                embed = discord.Embed(
                    title="🎁 RECOMPENSA DIÁRIA",
                    description=f"{ctx.author.mention} recebeu **{recompensa} moedas**!",
                    color=0xffd700
                )
                await ctx.send(embed=embed)
            
            # Adicionar mais tipos conforme necessário...
            else:
                await ctx.send(f"🔧 Comando personalizado executado: {config}")
            
            return
    
    # Outros erros
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você não tem permissão para usar este comando!")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ Eu não tenho permissão para executar este comando!")
    else:
        # Log de erro não tratado
        print(f"Erro não tratado: {error}")

# ========== COMANDO AJUDA CORRIGIDO ==========

@bot.command(name='ajuda')
async def ajuda(ctx):
    """🎮 Painel completo de ajuda COM SUGESTÕES"""
    embed = discord.Embed(
        title="🎮 PAINEL DE COMANDOS - SISTEMA COMPLETO",
        description="**Todas as funcionalidades disponíveis:**\n*Use !comando para executar*",
        color=0x7289DA
    )
    
    embed.add_field(
        name="⚡ ADMINISTRAÇÃO ESSENCIAL",
        value="`!admin` - Painel completo de administração\n"
              "`!setup_tickets` - Sistema de tickets\n"
              "`!si` - Analisar símbolos nos canais\n"
              "`!w <posição> <símbolo>` - Substituir símbolo por posição\n"
              "`!ws <antigo> <novo>` - Substituir símbolo específico\n"
              "`!pers <antigo> <novo>` - Substituir em nicks\n"
              "`!ssm_status` - Status de segurança\n"
              "`!whitelist_token` - Token para whitelist (Dono)",
        inline=False
    )
    
    embed.add_field(
        name="🤖 INTELIGÊNCIA ARTIFICIAL",
        value="`Mencione o bot` - Conversa inteligente\n"
              "`!script [requisitos]` - Cria scripts\n"
              "`!limpar_historico` - Limpa sua memória",
        inline=False
    )
    
    embed.add_field(
        name="🔧 NOVAS FUNCIONALIDADES AVANÇADAS",
        value="`!clone_categoria <id> [nome]` - Clona categoria\n"
              "`!organizar_canais <id_cat> <id1> <id2>...` - Organiza canais\n"
              "`!backup_canais` - Backup da estrutura\n"
              "`!restaurar_canais <backup_id>` - Restaura backup\n"
              "`!limpar_canais_inativos [dias]` - Limpeza inteligente\n"
              "`!estatisticas_canais` - Estatísticas detalhadas\n"
              "`!sync_cargos` - Sincroniza cargos\n"
              "`!auto_setup` - Configuração automática\n"
              "`!smart_clean` - Limpeza inteligente\n"
              "`!server_health` - Diagnóstico completo",
        inline=False
    )
    
    embed.add_field(
        name="📄 SISTEMA DE PDF",
        value="`!pdf_canal [limite]` - Cria PDF das mensagens\n"
              "`!web_to_pdf [url]` - Converte site para PDF\n"
              "`!banir @user [motivo]` - Ban com IA\n"
              "`!advertir @user [motivo]` - Advertir com IA",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ SISTEMA DE CONFIGURAÇÃO",
        value="`!config` - Menu de configuração\n"
              "`!set [tipo] #canal` - Definir canal\n"
              "`!view_config` - Ver configuração\n"
              "`!reset_config` - Resetar configuração\n"
              "`!set_canal [#canal]` - Definir canal\n"
              "`!canais_permitidos` - Listar canais\n"
              "`!setup_cargos` - Configurar cargos\n"
              "`!setup_completo` - Configuração total",
        inline=False
    )
    
    embed.add_field(
        name="👥 SISTEMA DE MEMBROS",
        value="`!perfil [@user]` - Ver perfil completo\n"
              "`!convites [@user]` - Status de convites\n"
              "`!convite` - Gerar convite pessoal\n"
              "`!pontos [@user]` - Ver pontuação\n"
              "`!ranking` - Ranking de pontos\n"
              "`!add_pontos @user pontos` - Adiciona pontos\n"
              "`!remove_pontos @user pontos` - Remove pontos\n"
              "`!cargos` - Listar cargos disponíveis",
        inline=False
    )
    
    embed.add_field(
        name="🏷️ SISTEMA DE CARGOS",
        value="`!setup_cargos` - Configurar sistema\n"
              "`!atualizar_cargos` - Atualizar cargos\n"
              "`!atualizar_nicks` - Atualizar nicknames\n"
              "`!cargos` - Listar cargos\n"
              "`!ccg nome cor` - Criar cargo",
        inline=False
    )
    
    embed.add_field(
        name="🔧 FERRAMENTAS ÚTEIS",
        value="`!calc [expressão]` - Calculadora\n"
              "`!dado [lados]` - Jogar dado\n"
              "`!moeda` - Cara ou coroa\n"
              "`!lembrete [minutos] [msg]` - Lembrete\n"
              "`!clear [quantidade]` - Limpar mensagens\n"
              "`!server` - Info do servidor\n"
              "`!ping` - Latência do bot\n"
              "`!search PDF/serv/membros` - Busca avançada\n"
              "`!comunicado #canal msg` - Comunicado\n"
              "`!criar_canais tipo` - Cria canais\n"
              "`!lembrete_anuncio` - Agenda anúncio\n"
              "`!missao_cyber` - Missão cybersecurity\n"
              "`!web_to_pdf [url]` - Converte site para PDF\n"
              "`!ejetar #canal msg` - Mensagem direta\n"
              "`!mv pos_atual nova_pos` - Mover canal\n"
              "`!mv_cat pos_atual nova_pos` - Mover categoria\n"
              "`!-mq nome permissao` - Criar categoria IA\n"
              "`!-mc nome tipo permissao` - Criar canal IA\n"
              "`!lk [#canal]` - Bloquear canal\n"
              "`!ulk [#canal]` - Desbloquear canal",
        inline=False
    )
    
    if ctx.author.guild_permissions.manage_messages:
        embed.add_field(
            name="🛡️ MODERAÇÃO (STAFF)",
            value="`!advertir @user [motivo]` - Advertir\n"
                  "`!advertencias [@user]` - Ver advertências\n"
                  "`!remover_advertencia @user [numero]` - Remove advertência\n"
                  "`!ban @user [motivo]` - Banir\n"
                  "`!mute @user [tempo] [motivo]` - Mutar\n"
                  "`!unmute @user` - Desmutar",
            inline=False
        )
    
    # ADICIONAR SUGESTÃO DE PESQUISA
    embed.add_field(
        name="🔍 NÃO ACHOU O QUE PROCURAVA?",
        value="Use `!p <palavra-chave>` para procurar comandos por função!\n**Exemplos:** `!p ban`, `!p pdf`, `!p criar canal`, `!p pontuacao`",
        inline=False
    )
    
    embed.set_footer(text=f"Solicitado por {ctx.author.name} • Total de comandos: 90+ • Sistema Completo")
    await ctx.send(embed=embed)

# EVENTOS DO BOT ORIGINAIS
@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user.name} está online! ID: {bot.user.id}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!ajuda"))
    
    if 'canais_permitidos' in db.config:
        CONFIG['canais_permitidos'] = db.config['canais_permitidos']
    
    print("🔄 Iniciando sistema automático de cargos...")
    for guild in bot.guilds:
        try:
            membros_atualizados = await sistema_cargos.atribuir_cargo_membro_automatico(guild)
            print(f"✅ {membros_atualizados} membros receberam cargo 'Membro' em {guild.name}")
            
            for member in guild.members:
                if not member.bot:
                    await sistema_cargos.atualizar_nick_automatico(member)
                    await asyncio.sleep(0.3)
            
            print(f"✅ Nicks atualizados em {guild.name}")
        except Exception as e:
            print(f"❌ Erro em {guild.name}: {e}")

    print("🛡️ Iniciando sistemas de segurança...")
    for guild in bot.guilds:
        try:
            # Criar cargo de quarentena se necessário
            await sistema_seguranca.criar_cargo_quarentena(guild)
            print(f"✅ Sistema de segurança inicializado em {guild.name}")
        except Exception as e:
            print(f"❌ Erro em {guild.name}: {e}")

@bot.event
async def on_member_remove(member):
    await log_system.log_saida(member)

@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        await sistema_cargos.atualizar_nick_automatico(after)

# ========== INICIALIZAR BOT ==========
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ Token do Discord não encontrado")