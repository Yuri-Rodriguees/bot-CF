import requests

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

    response = requests.get(url, headers=headers, cookies=cookies, params=params)

    if response.status_code == 200:
        dados = response.json()

        resultados = dados.get("ds_WEB_USER_ALLTIME_TM_Result")
        if resultados and len(resultados) > 0:
            jogador = resultados[0]
            print(f"📇 Nome: {jogador.get('ign')}")
            print(f"🏅 Rank: {jogador.get('tier_group_name')}")
            print(f" TOP RANK: {jogador.get('rank')}")
            print(f"⭐ Pontos: {jogador.get('rank_score')}")
            print(f"📊 Win: {jogador.get('win_cnt')} - ❌ Derrotas: {jogador.get('lose_cnt')}")
            print(f"⚔️ K/D: {jogador.get('kd')}")
            print(f"📈 Win Rate: {jogador.get('vit')}")
        else:
            print("❌ Jogador não encontrado ou sem ranking.")
    else:
        print(f"Erro {response.status_code}: Não foi possível obter os dados.")

if __name__ == "__main__":
    nick = input("Digite o nickname do jogador: ")
    consultar_rank_cf(nick)
