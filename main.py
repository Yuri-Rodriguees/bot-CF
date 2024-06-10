import asyncio
import sys
import ctypes
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image
from pyppeteer import launch
from pyppeteer.errors import PageError
from twitchio.ext import commands


# By: Yuuri_dev

# Função para executar o script de scraping
async def run_script(nick_to_search):
    # Configurar o navegador e a página
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    try:
        # Acessar a página inicial
        await page.goto("https://br.crossfire.z8games.com/competitiveranking.html", {"waitUntil": "networkidle0"})

        # Inserir o nick na barra de pesquisa
        await page.type("#desk_search_text", nick_to_search)
        await page.keyboard.press("Enter")
        
        # Esperar pelos resultados da pesquisa
        await page.waitForXPath("//ul[@class='cfr-rank col-4b']", {"timeout": 10000})
        
        # Encontrar o elemento que contém o nick desejado na tabela de resultados
        result_elements = await page.xpath(f"//ul[@class='cfr-rank col-4b']//li[@class='cfr-rank-name']/a[contains(text(), '{nick_to_search}')]")
        
        if result_elements:
            profile_link_handle = await result_elements[0].getProperty("href")
            profile_link = await profile_link_handle.jsonValue()

            # Acessar a página de perfil
            await page.goto(profile_link, {"waitUntil": "networkidle0"})
            await page.waitForXPath("(//div[@class='pastseason_tierText__3j7pS'])[4]", {"timeout": 10000})
            
            # Extrair o rank
            rank_elements = await page.xpath("(//div[@class='pastseason_tierText__3j7pS'])[4]")
            if rank_elements:
                h5_text = await page.evaluate('(element) => element.querySelector("h5").innerText', rank_elements[0])
                h3_text = await page.evaluate('(element) => element.querySelector("h3").innerText', rank_elements[0])

                result = f'\nRANK: {h5_text} - {h3_text}'
                return result
            else:
                return "Erro: Elemento de rank não encontrado"
        else:
            return "Erro: Jogador não encontrado"

    except PageError as e:
        return f"Erro ao carregar a página: {e}"

    finally:
        await browser.close()

# Bot
class Bot(commands.Bot):
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        super().__init__(token='TOKEN', client_id='FXS', nick='rank', prefix='!', initial_channels=['yuuri_dev', 'zaipzin'], loop=self.loop)

    async def event_ready(self):
        print(f'\nOnline | {self.nick}\n')

    @commands.command(name='rank')
    async def elorank(self, ctx, *args):
        if not args:
            await ctx.send('Por favor, forneça o nome do jogador após o comando. Exemplo: !rank jogador1')
        else:
            nick_to_search = ' '.join(args)
            result = await run_script(nick_to_search)
            await ctx.send(result)

def on_quit(icon, item):
    icon.stop()
    sys.exit(0)

def run_bot(loop):
    bot = Bot(loop=loop)
    bot.run()

# Ícone do sistema
def setup_icon():
    image = Image.open("assets/k.png")
    menu = (item('Sair', on_quit),)
    icon = pystray.Icon("name", image, "ZAIP BOT", menu)
    icon.run()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    threading.Thread(target=setup_icon).start()
    loop.create_task(run_bot(loop))
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    loop.run_forever()
