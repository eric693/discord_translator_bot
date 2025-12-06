import discord
from discord.ext import commands
from googletrans import Translator
import asyncio
import logging
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設置日誌
logging.basicConfig(level=logging.INFO)

# 初始化翻譯器
translator = Translator()

# 創建機器人實例
intents = discord.Intents.default()
intents.message_content = True  # 啟用訊息內容權限，自動翻譯需要此權限
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} 已經上線！')
    print(f'機器人ID: {bot.user.id}')
    print('---準備開始翻譯服務---')

@bot.event
async def on_message(message):
    # 調試信息
    print(f"收到訊息: '{message.content}' 來自: {message.author}")
    
    # 防止機器人回應自己的訊息
    if message.author == bot.user:
        print("忽略機器人自己的訊息")
        return
    
    # 防止機器人回應其他機器人的訊息
    if message.author.bot:
        print("忽略其他機器人的訊息")
        return
    
    # 檢查是否為指令，如果是指令就不自動翻譯
    if message.content.startswith('!'):
        print("這是指令，處理指令...")
        await bot.process_commands(message)
        return
    
    # 自動翻譯功能：檢測中文並自動翻譯
    try:
        # 過濾太短的訊息（避免翻譯單個字符或表情符號）
        if len(message.content.strip()) < 2:
            print("訊息太短，跳過翻譯")
            return
            
        print(f"開始檢測語言: '{message.content}'")
        # 檢測語言
        detected_lang = detect_language(message.content)
        print(f"檢測到的語言: {detected_lang}")
        
        # 雙向自動翻譯：中文翻英文，英文翻中文
        if detected_lang in ['zh-tw', 'zh-TW', 'zh-cn', 'zh-CN', 'zh']:
            print("檢測到中文，翻譯成英文...")
            translated = translate_text(message.content, 'en')
            print(f"翻譯結果: {translated}")
            
            # 直接發送翻譯結果
            await message.channel.send(translated)
            print("翻譯結果已發送！")
        elif detected_lang == 'en':
            print("檢測到英文，翻譯成中文...")
            translated = translate_text(message.content, 'zh-tw')
            print(f"翻譯結果: {translated}")
            
            # 直接發送翻譯結果
            await message.channel.send(translated)
            print("翻譯結果已發送！")
        else:
            print(f"檢測到其他語言({detected_lang})，跳過自動翻譯")
            
    except Exception as e:
        # 如果自動翻譯失敗，靜默處理（不發送錯誤訊息）
        print(f"自動翻譯錯誤: {e}")
        import traceback
        traceback.print_exc()
    
    # 繼續處理其他指令
    await bot.process_commands(message)

def detect_language(text):
    """檢測文字語言"""
    try:
        detected = translator.detect(text)
        return detected.lang
    except Exception as e:
        print(f"語言檢測錯誤: {e}")
        return None

def translate_text(text, target_lang='en'):
    """翻譯文字"""
    try:
        if target_lang == 'auto':
            # 自動檢測並翻譯
            detected_lang = detect_language(text)
            if detected_lang == 'zh-tw' or detected_lang == 'zh':
                target_lang = 'en'
            else:
                target_lang = 'zh-tw'
        
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception as e:
        print(f"翻譯錯誤: {e}")
        return "翻譯失敗，請稍後再試。"

@bot.command(name='translate', aliases=['翻譯', 't'])
async def translate_command(ctx, *, text=None):
    """
    翻譯指令
    用法: !translate [文字] 或 !翻譯 [文字] 或 !t [文字]
    """
    if not text:
        await ctx.send("請提供要翻譯的文字！\n用法: `!translate 你好世界` 或 `!翻譯 Hello World`")
        return
    
    # 顯示正在翻譯的訊息
    thinking_msg = await ctx.send("🔄 正在翻譯中...")
    
    try:
        # 檢測語言並翻譯
        detected_lang = detect_language(text)
        print(f"檢測到的語言: {detected_lang}")  # 調試信息
        
        if detected_lang in ['zh-tw', 'zh-TW', 'zh-cn', 'zh-CN', 'zh']:
            # 中文翻譯成英文
            translated = translate_text(text, 'en')
            source_lang = "中文"
            target_lang = "英文"
        else:
            # 其他語言翻譯成繁體中文
            translated = translate_text(text, 'zh-tw')
            source_lang = "英文"
            target_lang = "繁體中文"
        
        # 創建嵌入式訊息
        embed = discord.Embed(
            title="🌐 翻譯結果",
            color=0x00ff00,
            timestamp=ctx.message.created_at
        )
        
        embed.add_field(
            name=f"原文 ({source_lang})",
            value=f"```{text}```",
            inline=False
        )
        
        embed.add_field(
            name=f"譯文 ({target_lang})",
            value=f"```{translated}```",
            inline=False
        )
        
        embed.set_footer(text=f"由 {ctx.author.display_name} 請求", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        # 更新訊息
        await thinking_msg.edit(content=None, embed=embed)
        
    except Exception as e:
        await thinking_msg.edit(content=f"❌ 翻譯時發生錯誤: {str(e)}")
        print(f"翻譯錯誤詳情: {e}")  # 調試信息

@bot.command(name='to_english', aliases=['英文', 'en'])
async def to_english(ctx, *, text=None):
    """強制翻譯成英文"""
    if not text:
        await ctx.send("請提供要翻譯成英文的文字！")
        return
    
    thinking_msg = await ctx.send("🔄 正在翻譯成英文...")
    
    try:
        translated = translate_text(text, 'en')
        
        embed = discord.Embed(
            title="🇺🇸 翻譯成英文",
            color=0x0099ff,
            timestamp=ctx.message.created_at
        )
        
        embed.add_field(name="原文", value=f"```{text}```", inline=False)
        embed.add_field(name="英文", value=f"```{translated}```", inline=False)
        embed.set_footer(text=f"由 {ctx.author.display_name} 請求", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await thinking_msg.edit(content=None, embed=embed)
        
    except Exception as e:
        await thinking_msg.edit(content=f"❌ 翻譯時發生錯誤: {str(e)}")
        print(f"翻譯錯誤詳情: {e}")

@bot.command(name='to_chinese', aliases=['中文', 'zh'])
async def to_chinese(ctx, *, text=None):
    """強制翻譯成繁體中文"""
    if not text:
        await ctx.send("請提供要翻譯成中文的文字！")
        return
    
    thinking_msg = await ctx.send("🔄 正在翻譯成繁體中文...")
    
    try:
        translated = translate_text(text, 'zh-tw')
        
        embed = discord.Embed(
            title="🇹🇼 翻譯成繁體中文",
            color=0xff6600,
            timestamp=ctx.message.created_at
        )
        
        embed.add_field(name="原文", value=f"```{text}```", inline=False)
        embed.add_field(name="繁體中文", value=f"```{translated}```", inline=False)
        embed.set_footer(text=f"由 {ctx.author.display_name} 請求", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
        
        await thinking_msg.edit(content=None, embed=embed)
        
    except Exception as e:
        await thinking_msg.edit(content=f"❌ 翻譯時發生錯誤: {str(e)}")
        print(f"翻譯錯誤詳情: {e}")

@bot.command(name='auto_toggle', aliases=['自動翻譯', 'auto'])
async def auto_toggle(ctx):
    """開啟/關閉自動翻譯功能"""
    # 這裡可以添加每個服務器的設置，現在先顯示當前狀態
    embed = discord.Embed(
        title="🤖 自動翻譯設置",
        description="目前自動翻譯功能已啟用",
        color=0x00ff88
    )
    
    embed.add_field(
        name="📋 功能說明",
        value="• 檢測到中文時自動翻譯成英文\n• 不會翻譯以 `!` 開頭的指令\n• 過濾太短的訊息（少於2個字符）",
        inline=False
    )
    
    embed.add_field(
        name="💡 使用提示",
        value="• 直接輸入中文即可自動翻譯\n• 使用 `!translate` 指令進行手動翻譯\n• 使用 `!英文` 或 `!中文` 強制翻譯",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='help_translate', aliases=['翻譯幫助'])
async def help_translate(ctx):
    """顯示翻譯機器人的幫助訊息"""
    embed = discord.Embed(
        title="🤖 翻譯機器人使用指南",
        description="支援繁體中文和英文之間的無限次數雙向翻譯",
        color=0x9932cc
    )
    
    embed.add_field(
        name="🔄 自動雙向翻譯",
        value="• 輸入中文 → 自動翻譯成英文\n• 輸入英文 → 自動翻譯成中文\n• 其他語言不會自動翻譯",
        inline=False
    )
    
    embed.add_field(
        name="📝 手動翻譯指令",
        value="`!translate [文字]` 或 `!翻譯 [文字]` 或 `!t [文字]`\n自動檢測語言並翻譯",
        inline=False
    )
    
    embed.add_field(
        name="🇺🇸 強制翻譯成英文",
        value="`!to_english [文字]` 或 `!英文 [文字]` 或 `!en [文字]`",
        inline=False
    )
    
    embed.add_field(
        name="🇹🇼 強制翻譯成繁體中文",
        value="`!to_chinese [文字]` 或 `!中文 [文字]` 或 `!zh [文字]`",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ 設置指令",
        value="`!auto_toggle` 或 `!自動翻譯` - 查看自動翻譯設置",
        inline=False
    )
    
    embed.add_field(
        name="💡 使用範例",
        value="• 直接輸入：`你好世界` → 自動翻譯成 `Hello World`\n• 直接輸入：`Hello World` → 自動翻譯成 `你好世界`\n• `!translate Bonjour` → 手動翻譯法文成中文\n• `!英文 早安` → 強制翻譯成英文",
        inline=False
    )
    
    embed.add_field(
        name="✨ 特色功能",
        value="• 🔄 雙向自動翻譯\n• 🌐 無限次數翻譯\n• 🎯 智能語言檢測\n• 🎨 精美的嵌入式訊息\n• 📱 支援多種指令別名",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    """錯誤處理"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ 請提供要翻譯的文字！")
    elif isinstance(error, commands.CommandNotFound):
        pass  # 忽略未知指令
    else:
        await ctx.send(f"❌ 發生錯誤: {str(error)}")
        print(f"錯誤: {error}")

# 運行機器人
if __name__ == "__main__":
    print("🤖 Discord 翻譯機器人啟動中...")
    print("請確保已設置環境變數 DISCORD_BOT_TOKEN")
    
    # 從環境變數獲取 TOKEN
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    
    if not TOKEN:
        print("❌ 錯誤：未找到 DISCORD_BOT_TOKEN 環境變數！")
        print("\n📝 請在 Railway 中設置環境變數：")
        print("1. 進入你的服務 (Service)")
        print("2. 點擊 'Variables' 標籤")
        print("3. 添加變數名稱: DISCORD_BOT_TOKEN")
        print("4. 添加你的 Discord Bot Token 作為值")
        exit(1)
    
    try:
        print("🚀 正在連接到 Discord...")
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ TOKEN 無效！請檢查你的 TOKEN 是否正確。")
    except Exception as e:
        print(f"❌ 機器人啟動失敗: {e}")
        print("💡 常見問題：")
        print("- 檢查網路連接")
        print("- 確認 TOKEN 正確")
        print("- 確保已安裝所需套件")