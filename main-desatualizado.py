import asyncio
import requests
from twitchio.ext import commands

def consultar_rank_cf(nickname):
    if not nickname:
        return "❌ Nickname não fornecido."

    url = "https://br.crossfire.z8games.com/rest/eloranking.json"
    params = {
        "startrow": 0,
        "endrow": 30,
        "name": nickname,
        "rankType": "user",
        "period": "all"
    }

    headers = {
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,es;q=0.7",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://br.crossfire.z8games.com/competitiveranking.html",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    cookies = {
        "dontaskregion": "1"
    }

    try:
        response = requests.get(url, headers=headers, cookies=cookies, params=params, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            resultados = dados.get("ds_WEB_USER_ALLTIME_TM_Result")
            if resultados and len(resultados) > 0:
                jogador = resultados[0]
                ign = jogador.get("ign")
                patente = jogador.get("tier_group_name")
                pts = jogador.get("rank_score")
                rank = jogador.get("rank")
                wins = jogador.get("win_cnt")
                losses = jogador.get("lose_cnt")
                kd = jogador.get("kd")
                winrate = jogador.get("vit")

                return (f"📛 Nick: {ign} | 🏅 {patente} ({pts} pts) | 🔢 Rank: {rank}º | "
                        f"📈 Win Rate: {winrate} | ⚔️ K/D: {kd} | ✅ V: {wins} ❌ D: {losses}")
            else:
                return "❌ Jogador não encontrado ou sem ranking."
        else:
            return f"❌ Erro {response.status_code}: Não foi possível obter os dados."
    except requests.RequestException as e:
        return f"⚠️ Erro de conexão: {e}"

class Bot(commands.Bot):
    def __init__(self):
        # Store channels separately since we can't access initial_channels later
        self.target_channels = ['yuriinerd', 'paozin9', 'kiweyfps', 'v1nniofc', 'dgzinsz', 'prtxis', 'zaipzin']
        super().__init__(
            token='d7q8nrmgmpmyp8nq4ei9xh5rvg97un',
            client_id='gp762nuuoqcoxypju8c569th9wz7q5',
            nick='cfal_rank',
            prefix='!',
            initial_channels=self.target_channels
        )

    async def event_ready(self):
        print(f'✅ Bot conectado como {self.nick}')
        print(f'✅ Conectado aos canais: {", ".join(self.target_channels)}')

    async def event_message(self, message):
        if message.echo:
            return

        print(f'Mensagem recebida de {message.author.name}: {message.content}')
        await self.handle_commands(message)

    @commands.command(name='rank')
    async def rank_command(self, ctx, *, nickname: str = None):
        if not nickname:
            await ctx.send("❌ Por favor, forneça um nickname após o comando !rank")
            return

        resultado = consultar_rank_cf(nickname)
        await ctx.send(resultado[:450])

if __name__ == "__main__":
    bot = Bot()
    bot.run()