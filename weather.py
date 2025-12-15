import json
import aiohttp

class WeatherMod:
    name = "Weather"
    description = "Ob-havo ma'lumotlari"
    version = "1.0.0"
    author = "System"
    commands = ["weather", "obhavo", "temp"]
    
    def __init__(self, client, db):
        self.client = client
        self.db = db
        self.api_key = None
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "commands": self.commands
        }
    
    async def weathercmd(self, message):
        """Ob-havo ma'lumotlari"""
        args = message.text.split()
        
        if len(args) < 2:
            await message.edit("🌤️ **Foydalanish:** `.weather Toshkent`")
            return
        
        city = " ".join(args[1:])
        await self.get_weather(message, city)
    
    async def obhavocmd(self, message):
        """Ob-havo (o'zbekcha)"""
        args = message.text.split()
        
        if len(args) < 2:
            await message.edit("🌤️ **Foydalanish:** `.obhavo Toshkent`")
            return
        
        city = " ".join(args[1:])
        await self.get_weather(message, city, lang="uz")
    
    async def tempcmd(self, message):
        """Haroratni ko'rish"""
        args = message.text.split()
        
        if len(args) < 2:
            await message.edit("🌡️ **Foydalanish:** `.temp Toshkent`")
            return
        
        city = " ".join(args[1:])
        await self.get_temperature(message, city)
    
    async def get_weather(self, message, city, lang="en"):
        """Ob-havo ma'lumotlarini olish"""
        try:
            # OpenWeatherMap API (bepul versiya)
            api_key = "your_api_key_here"  # Bu yerga o'z API key ingizni qo'ying
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang={lang}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Ma'lumotlarni olish
                        temp = data["main"]["temp"]
                        feels_like = data["main"]["feels_like"]
                        humidity = data["main"]["humidity"]
                        description = data["weather"][0]["description"]
                        wind_speed = data["wind"]["speed"]
                        city_name = data["name"]
                        country = data["sys"]["country"]
                        
                        # Havo holati belgisi
                        weather_emoji = self.get_weather_emoji(data["weather"][0]["id"])
                        
                        # Xabarni tayyorlash
                        if lang == "uz":
                            text = f"{weather_emoji} **{city_name}, {country} ob-havosi**\n\n"
                            text += f"🌡️ **Harorat:** {temp}°C\n"
                            text += f"🤏 **Hissiyot:** {feels_like}°C\n"
                            text += f"💧 **Namlik:** {humidity}%\n"
                            text += f"💨 **Shamol:** {wind_speed} m/s\n"
                            text += f"📝 **Tavsif:** {description.capitalize()}"
                        else:
                            text = f"{weather_emoji} **Weather in {city_name}, {country}**\n\n"
                            text += f"🌡️ **Temperature:** {temp}°C\n"
                            text += f"🤏 **Feels like:** {feels_like}°C\n"
                            text += f"💧 **Humidity:** {humidity}%\n"
                            text += f"💨 **Wind:** {wind_speed} m/s\n"
                            text += f"📝 **Description:** {description.capitalize()}"
                        
                        await message.edit(text)
                    else:
                        if lang == "uz":
                            await message.edit(f"❌ Shahar topilmadi: {city}")
                        else:
                            await message.edit(f"❌ City not found: {city}")
        
        except Exception as e:
            await message.edit(f"❌ Xato: {str(e)}")
    
    async def get_temperature(self, message, city):
        """Faqat haroratni olish"""
        try:
            api_key = "your_api_key_here"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        temp = data["main"]["temp"]
                        city_name = data["name"]
                        country = data["sys"]["country"]
                        
                        # Haroratga qarab rang
                        if temp < 0:
                            emoji = "❄️"
                            feeling = "Muzday"
                        elif temp < 10:
                            emoji = "🥶"
                            feeling = "Sovuq"
                        elif temp < 20:
                            emoji = "😊"
                            feeling = "Salqin"
                        elif temp < 30:
                            emoji = "🌤️"
                            feeling = "Issiq"
                        else:
                            emoji = "🔥"
                            feeling = "Juda issiq"
                        
                        text = f"{emoji} **{city_name}, {country}**\n\n"
                        text += f"🌡️ **Harorat:** {temp}°C\n"
                        text += f"📊 **Hissiyot:** {feeling}\n\n"
                        text += f"_{self.get_temperature_tip(temp)}_"
                        
                        await message.edit(text)
                    else:
                        await message.edit(f"❌ Shahar topilmadi: {city}")
        
        except Exception as e:
            await message.edit(f"❌ Xato: {str(e)}")
    
    def get_weather_emoji(self, weather_id):
        """Havo holati uchun emoji"""
        if weather_id == 800:
            return "☀️"  # Ochiq osmon
        elif 800 < weather_id < 805:
            return "☁️"  # Bulutli
        elif 300 <= weather_id < 600:
            return "🌧️"  # Yomg'ir
        elif 600 <= weather_id < 700:
            return "❄️"  # Qor
        elif 700 <= weather_id < 800:
            return "🌫️"  # Tuman
        elif 200 <= weather_id < 300:
            return "⛈️"  # Momaqaldiroq
        else:
            return "🌤️"
    
    def get_temperature_tip(self, temp):
        """Harorat bo'yicha maslahat"""
        if temp < -10:
            return "Uydan chiqmang, juda sovuq!"
        elif temp < 0:
            return "Issiq kiyining!"
        elif temp < 10:
            return "Kurtka kiyishni unutmang"
        elif temp < 20:
            return "Eng yaxshi ob-havo"
        elif temp < 30:
            return "Suyak oling"
        elif temp < 35:
            return "Ko'p suv iching"
        else:
            return "Issiqdan saqlaning!"