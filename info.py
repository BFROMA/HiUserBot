# modules/info.py
# Foydalanuvchi ma'lumotlari moduli

from telethon import events
from telethon.tl.types import User, Channel, Chat
import datetime

class InfoModule:
    """Foydalanuvchi va chat haqida ma'lumot beruvchi modul"""
    
    # Modul ma'lumotlari
    name = "info"
    description = "Foydalanuvchi yoki chat haqida ma'lumot olish"
    version = "1.0"
    
    # Faol/faol emas holati
    enabled = True
    
    def __init__(self, client, db):
        """
        Modulni ishga tushirish
        
        Args:
            client: Telethon client obyekti
            db: Ma'lumotlar bazasi
        """
        self.client = client
        self.db = db
        self.register_handlers()
    
    def register_handlers(self):
        """Buyruqlarni ro'yxatdan o'tkazish"""
        
        @self.client.on(events.NewMessage(pattern=r'^\.info$', outgoing=True))
        async def info_handler(event):
            """Joriy foydalanuvchi haqida ma'lumot"""
            if not self.enabled:
                return
                
            # O'zimiz haqida ma'lumot
            me = await self.client.get_me()
            info_text = await self.get_user_info(me)
            await event.edit(info_text)
        
        @self.client.on(events.NewMessage(pattern=r'^\.info @?(\w+)$', outgoing=True))
        async def user_info_handler(event):
            """Berilgan foydalanuvchi haqida ma'lumot"""
            if not self.enabled:
                return
                
            username = event.pattern_match.group(1)
            
            try:
                # Username bo'yicha foydalanuvchini topish
                user = await self.client.get_entity(username)
                info_text = await self.get_user_info(user)
                await event.edit(info_text)
            except Exception as e:
                await event.edit(f"❌ **Xatolik:** {str(e)}")
    
    async def get_user_info(self, user):
        """Foydalanuvchi ma'lumotlarini formatlash"""
        
        # Asosiy ma'lumotlar
        user_id = user.id
        first_name = user.first_name or ""
        last_name = user.last_name or ""
        username = f"@{user.username}" if user.username else "Yo'q"
        
        # Qo'shimcha ma'lumotlar
        phone = user.phone or "Noma'lum"
        
        # Premium tekshirish
        premium = "✅" if getattr(user, 'premium', False) else "❌"
        
        # Bot tekshirish
        is_bot = "✅" if user.bot else "❌"
        
        # Online holat
        status = "Noma'lum"
        if hasattr(user, 'status'):
            if user.status:
                if hasattr(user.status, 'was_online'):
                    last_seen = user.status.was_online
                    status = last_seen.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    status = "Online"
        
        info_text = f"""
👤 **Foydalanuvchi Ma'lumotlari**

**ID:** `{user_id}`
**Ism:** {first_name} {last_name}
**Username:** {username}
**Telefon:** `{phone}`
**Bot:** {is_bot}
**Premium:** {premium}

**Oxirgi ko'rinish:** {status}
**Do'stlar soni:** {getattr(user, 'mutual_contact_count', 'Noma\'lum')}
"""
        return info_text
    
    def get_commands(self):
        """Modul buyruqlarini qaytarish"""
        return {
            '.info': 'O'zingiz haqida ma\'lumot olish',
            '.info <username>': 'Boshqa foydalanuvchi haqida ma\'lumot'
        }
    
    def enable(self):
        """Modulni yoqish"""
        self.enabled = True
        return f"{self.name} moduli yoqildi"
    
    def disable(self):
        """Modulni o'chirish"""
        self.enabled = False
        return f"{self.name} moduli o'chirildi"
    
    def get_info(self):
        """Modul haqida ma'lumot"""
        return {
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'enabled': self.enabled,
            'commands': self.get_commands()
        }