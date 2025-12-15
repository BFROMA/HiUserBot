import math
import json
from datetime import datetime

class CalculatorMod:
    name = "Calculator"
    description = "Matematik hisob-kitoblar"
    version = "2.0.0"
    author = "System"
    commands = ["calc", "calculate", "math", "eval", "pi", "prime"]
    
    def __init__(self, client, db):
        self.client = client
        self.db = db
        self.history = []
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "commands": self.commands,
            "history_count": len(self.history)
        }
    
    async def calccmd(self, message):
        """Kalkulyator"""
        args = message.text.split()
        
        if len(args) < 2:
            await self.show_calculator_help(message)
            return
        
        expression = " ".join(args[1:])
        await self.calculate(message, expression)
    
    async def calculatecmd(self, message):
        """Hisoblash (to'liq nom)"""
        await self.calccmd(message)
    
    async def mathcmd(self, message):
        """Matematik funksiyalar"""
        args = message.text.split()
        
        if len(args) < 2:
            await message.edit("🧮 **Matematik funksiyalar:**\n\n"
                             "`.math sin 45` - Sinus\n"
                             "`.math cos 45` - Kosinus\n"
                             "`.math sqrt 16` - Ildiz\n"
                             "`.math log 100` - Logarifm\n"
                             "`.math pow 2 3` - Daraja (2^3)")
            return
        
        func = args[1].lower()
        
        try:
            if func == "sin":
                if len(args) < 3:
                    await message.edit("❌ Burchak kiriting: `.math sin 45`")
                    return
                angle = float(args[2])
                result = math.sin(math.radians(angle))
                await message.edit(f"sin({angle}°) = {result:.6f}")
                
            elif func == "cos":
                if len(args) < 3:
                    await message.edit("❌ Burchak kiriting: `.math cos 45`")
                    return
                angle = float(args[2])
                result = math.cos(math.radians(angle))
                await message.edit(f"cos({angle}°) = {result:.6f}")
                
            elif func == "tan":
                if len(args) < 3:
                    await message.edit("❌ Burchak kiriting: `.math tan 45`")
                    return
                angle = float(args[2])
                result = math.tan(math.radians(angle))
                await message.edit(f"tan({angle}°) = {result:.6f}")
                
            elif func == "sqrt":
                if len(args) < 3:
                    await message.edit("❌ Son kiriting: `.math sqrt 16`")
                    return
                num = float(args[2])
                result = math.sqrt(num)
                await message.edit(f"√{num} = {result}")
                
            elif func == "log":
                if len(args) < 3:
                    await message.edit("❌ Son kiriting: `.math log 100`")
                    return
                num = float(args[2])
                result = math.log10(num)
                await message.edit(f"log₁₀({num}) = {result:.6f}")
                
            elif func == "ln":
                if len(args) < 3:
                    await message.edit("❌ Son kiriting: `.math ln 100`")
                    return
                num = float(args[2])
                result = math.log(num)
                await message.edit(f"ln({num}) = {result:.6f}")
                
            elif func == "pow" or func == "power":
                if len(args) < 4:
                    await message.edit("❌ Son va daraja kiriting: `.math pow 2 3`")
                    return
                base = float(args[2])
                exponent = float(args[3])
                result = math.pow(base, exponent)
                await message.edit(f"{base}^{exponent} = {result}")
                
            else:
                await message.edit(f"❌ Funksiya topilmadi: {func}")
                
        except Exception as e:
            await message.edit(f"❌ Xato: {str(e)}")
    
    async def evalcmd(self, message):
        """Ifodani hisoblash (xavfsiz)"""
        args = message.text.split()
        
        if len(args) < 2:
            await message.edit("🔢 **Foydalanish:** `.eval 2+2*3`")
            return
        
        expression = " ".join(args[1:])
        
        # Xavfli so'zlarni tekshirish
        dangerous = ["import", "open", "exec", "__", "os.", "sys.", "subprocess"]
        for word in dangerous:
            if word in expression:
                await message.edit(f"⚠️ Xavfli ifoda: {word}")
                return
        
        try:
            # Xavfsiz hisoblash
            result = self.safe_eval(expression)
            
            # Tarixga qo'shish
            self.history.append({
                "expression": expression,
                "result": str(result),
                "time": datetime.now().isoformat()
            })
            
            if len(self.history) > 10:
                self.history = self.history[-10:]
            
            await message.edit(f"**Hisoblash:** `{expression}`\n**Natija:** `{result}`")
            
        except Exception as e:
            await message.edit(f"❌ Xato: {str(e)}")
    
    async def picmd(self, message):
        """PI soni va matematik konstantalar"""
        text = "🧮 **MATEMATIK KONSTANTALAR**\n\n"
        
        text += f"π (PI) = {math.pi:.15f}\n"
        text += f"e (Euler soni) = {math.e:.15f}\n"
        text += f"φ (Oltin nisbat) = {(1 + math.sqrt(5)) / 2:.15f}\n\n"
        
        text += "📊 **Qo'shimcha:**\n"
        text += f"√2 = {math.sqrt(2):.10f}\n"
        text += f"√3 = {math.sqrt(3):.10f}\n"
        text += f"ln(2) = {math.log(2):.10f}\n"
        text += f"ln(10) = {math.log(10):.10f}"
        
        await message.edit(text)
    
    async def primecmd(self, message):
        """Tub sonlar"""
        args = message.text.split()
        
        if len(args) < 2:
            # Tub sonlar haqida ma'lumot
            text = "🔢 **TUB SONLAR**\n\n"
            text += "Tub son - faqat 1 ga va o'ziga bo'linadigan son\n\n"
            text += "**Foydalanish:**\n"
            text += "`.prime check 17` - 17 tub ekanligini tekshirish\n"
            text += "`.prime list 10` - Dastlabki 10 ta tub son\n"
            text += "`.prime factors 48` - 48 ning tub ko'paytuvchilari\n"
            text += "`.prime random` - Tasodifiy tub son"
            await message.edit(text)
            return
        
        subcommand = args[1].lower()
        
        try:
            if subcommand == "check":
                if len(args) < 3:
                    await message.edit("❌ Son kiriting: `.prime check 17`")
                    return
                
                num = int(args[2])
                if self.is_prime(num):
                    await message.edit(f"✅ {num} - TUB SON")
                else:
                    await message.edit(f"❌ {num} - TUB SON EMAS")
            
            elif subcommand == "list":
                if len(args) < 3:
                    count = 10
                else:
                    count = min(int(args[2]), 50)  # Maksimal 50 ta
                
                primes = self.generate_primes(count)
                text = f"🔢 **DASTLABKI {count} TA TUB SON:**\n\n"
                
                # 5 ta qatorda ko'rsatish
                for i in range(0, len(primes), 5):
                    row = primes[i:i+5]
                    text += " ".join([f"`{p:4}`" for p in row]) + "\n"
                
                await message.edit(text)
            
            elif subcommand == "factors":
                if len(args) < 3:
                    await message.edit("❌ Son kiriting: `.prime factors 48`")
                    return
                
                num = int(args[2])
                factors = self.prime_factors(num)
                
                if factors:
                    # Ko'paytma shaklida
                    factors_str = " × ".join([f"{base}^{exp}" if exp > 1 else str(base) 
                                            for base, exp in factors.items()])
                    text = f"🔢 **{num} ning tub ko'paytuvchilari:**\n\n"
                    text += f"`{num} = {factors_str}`\n\n"
                    
                    # Ro'yxat shaklida
                    text += "📋 **Ro'yxat:**\n"
                    for base, exp in factors.items():
                        text += f"• {base}" + (f" ({exp} marta)" if exp > 1 else "") + "\n"
                    
                    await message.edit(text)
                else:
                    await message.edit(f"❌ {num} soni uchun tub ko'paytuvchilar topilmadi")
            
            elif subcommand == "random":
                import random
                # 100-1000 oralig'ida tasodifiy tub son
                primes = [p for p in range(100, 1001) if self.is_prime(p)]
                random_prime = random.choice(primes)
                
                text = f"🎲 **TASODIFIY TUB SON:**\n\n"
                text += f"**`{random_prime}`**\n\n"
                text += f"📊 **Xususiyatlari:**\n"
                text += f"• 100-1000 oralig'ida\n"
                text += f"• Raqamlar yig'indisi: {sum(int(d) for d in str(random_prime))}\n"
                text += f"• Raqamlar soni: {len(str(random_prime))}"
                
                await message.edit(text)
            
            else:
                await message.edit(f"❌ Noma'lum buyruq: {subcommand}")
                
        except Exception as e:
            await message.edit(f"❌ Xato: {str(e)}")
    
    async def calculate(self, message, expression):
        """Ifodani hisoblash"""
        try:
            # Xavfsiz hisoblash uchun funksiya
            def safe_calc(expr):
                # Xavfli so'zlarni olib tashlash
                for word in ["import", "open", "exec", "__", "os", "sys", "subprocess"]:
                    if word in expr.lower():
                        raise ValueError(f"Xavfli ifoda: {word}")
                
                # Matematik funksiyalarni qo'llab-quvvatlash
                allowed_names = {
                    'abs': abs,
                    'round': round,
                    'min': min,
                    'max': max,
                    'sum': sum,
                    'pow': pow,
                    'sqrt': math.sqrt,
                    'sin': math.sin,
                    'cos': math.cos,
                    'tan': math.tan,
                    'log': math.log,
                    'log10': math.log10,
                    'pi': math.pi,
                    'e': math.e
                }
                
                # Hisoblash
                try:
                    result = eval(expr, {"__builtins__": {}}, allowed_names)
                    return result
                except:
                    # Oddiy hisoblash
                    return eval(expr)
            
            result = safe_calc(expression)
            
            # Tarixga qo'shish
            self.history.append({
                "expression": expression,
                "result": str(result),
                "time": datetime.now().isoformat()
            })
            
            # Javobni formatlash
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            text = f"🧮 **KALKULYATOR**\n\n"
            text += f"📝 **Ifoda:** `{expression}`\n"
            text += f"✅ **Natija:** `{result}`\n\n"
            
            # Tarixni ko'rsatish (agar bor bo'lsa)
            if self.history:
                text += "📚 **So'nggi hisoblar:**\n"
                for item in self.history[-3:]:
                    text += f"• {item['expression']} = {item['result']}\n"
            
            await message.edit(text)
            
        except Exception as e:
            await message.edit(f"❌ Xato: {str(e)}")
    
    def safe_eval(self, expression):
        """Xavfsiz hisoblash"""
        # Faqat matematik amallar va raqamlar
        import ast
        
        # AST daraxtini tahlil qilish
        tree = ast.parse(expression, mode='eval')
        
        # Ruxsat etilgan node'lar
        allowed_nodes = {
            ast.Expression,
            ast.BinOp,
            ast.UnaryOp,
            ast.Num,
            ast.Constant,
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.Mod,
            ast.Pow,
            ast.USub,
            ast.UAdd
        }
        
        # Node'larni tekshirish
        for node in ast.walk(tree):
            if type(node) not in allowed_nodes:
                raise ValueError(f"Ruxsat etilmagan amal: {type(node).__name__}")
        
        # Hisoblash
        return eval(compile(tree, filename='<ast>', mode='eval'))
    
    def is_prime(self, n):
        """Tub sonlikni tekshirish"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        limit = int(math.sqrt(n)) + 1
        for i in range(3, limit, 2):
            if n % i == 0:
                return False
        return True
    
    def generate_primes(self, count):
        """Tub sonlar yaratish"""
        primes = []
        num = 2
        
        while len(primes) < count:
            if self.is_prime(num):
                primes.append(num)
            num += 1
        
        return primes
    
    def prime_factors(self, n):
        """Tub ko'paytuvchilarga ajratish"""
        if n < 2:
            return {}
        
        factors = {}
        temp = n
        
        # 2 ga bo'lish
        while temp % 2 == 0:
            factors[2] = factors.get(2, 0) + 1
            temp //= 2
        
        # Toq sonlar
        i = 3
        while i * i <= temp:
            while temp % i == 0:
                factors[i] = factors.get(i, 0) + 1
                temp //= i
            i += 2
        
        # Qolgan son
        if temp > 1:
            factors[temp] = factors.get(temp, 0) + 1
        
        return factors
    
    async def show_calculator_help(self, message):
        """Kalkulyator yordami"""
        text = "🧮 **KALKULYATOR YORDAMI**\n\n"
        
        text += "**Asosiy buyruqlar:**\n"
        text += "• `.calc 2+2*3` - Matematik ifoda\n"
        text += "• `.math sin 45` - Matematik funksiyalar\n"
        text += "• `.eval 2^10` - Ifodani baholash\n"
        text += "• `.pi` - Matematik konstantalar\n"
        text += "• `.prime check 17` - Tub sonlik tekshiruvi\n\n"
        
        text += "**Amallar:**\n"
        text += "`+` Qo'shish, `-` Ayirish, `*` Ko'paytirish\n"
        text += "`/` Bo'lish, `%` Qoldiq, `**` Daraja\n\n"
        
        text += "**Funksiyalar:**\n"
        text += "`sqrt(x)`, `sin(x)`, `cos(x)`, `log(x)`\n"
        text += "`abs(x)`, `round(x)`, `min(a,b)`, `max(a,b)`"
        
        await message.edit(text)