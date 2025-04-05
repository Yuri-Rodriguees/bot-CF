import requests
from twitchio.ext import commands

def consultar_rank_cf(nickname):
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

                return (f"📛 Nick: {ign}\n"
                        f"🏅 Patente: {patente} ({pts} pts)\n"
                        f"🔢 Rank Global: {rank}º\n"
                        f"📈 Win Rate: {winrate}\n"
                        f"⚔️ K/D: {kd}\n"
                        f"✅ Vitórias: {wins} ❌ Derrotas: {losses}")
            else:
                return "❌ Jogador não encontrado ou sem ranking."
        else:
            return f"❌ Erro {response.status_code}: Não foi possível obter os dados."
    except requests.RequestException as e:
        return f"⚠️ Erro de conexão: {e}"

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token='ghqdbysz6d2vutnoeff9xbsfnyc1ze',
            client_id='7bfw2re4ipw0ing4grpodex1novufz',
            nick='yuri_de_saogonsalo',
            prefix='!',
            initial_channels=['yuri_de_saogonsalo', 'paozin9']
        )

    async def event_ready(self):
        print(f'\n✅ Bot online como {self.nick}\n')

    @commands.command(name='rank')
    async def elorank(self, ctx, *args):
        if not args:
            await ctx.send('❗ Use: !rank <nick>')
        else:
            nickname = ' '.join(args)
            resultado = consultar_rank_cf(nickname)
            await ctx.send(resultado[:450])

if __name__ == "__main__":
    bot = Bot()
    bot.run()
