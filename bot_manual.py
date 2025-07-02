from config import APOSTA, META_LUCRO, STOP_LOSS
import time

def calcular_probabilidade(cliques):
    probabilidade = 1.0
    casas_seguras = 22
    casas_totais = 25
    for i in range(cliques):
        probabilidade *= casas_seguras / casas_totais
        casas_seguras -= 1
        casas_totais -= 1
    return probabilidade * 100

banca = 10.0  # valor inicial da banca
lucro_total = 0
vitorias = 0
derrotas = 0

print("🎮 Bot Manual com Probabilidade (1Win Mines)")
print("Clique manualmente no jogo e informe ao bot os resultados.\n")

while True:
    if lucro_total >= META_LUCRO:
        print("🎯 Meta de lucro atingida!")
        break
    if lucro_total <= -STOP_LOSS:
        print("🛑 Stop Loss atingido!")
        break

    input("➡️ Pressione ENTER para iniciar uma nova rodada.")
    cliques = 0
    while True:
        cliques += 1
        prob = calcular_probabilidade(cliques)
        print(f"🧠 Probabilidade de {cliques} acerto(s) seguidos: {prob:.2f}%")

        if prob < 95:
            continuar = input("⚠️ Probabilidade abaixo de 95%. Deseja CONTINUAR? (s/n): ").strip().lower()
            if continuar != "s":
                cliques -= 1
                break

        acertou = input("👉 Você acertou o clique? (s/n): ").strip().lower()
        if acertou == "s":
            continuar = input("👉 Deseja CONTINUAR ou SACAR? (c/s): ").strip().lower()
            if continuar == "s":
                ganho = APOSTA * (0.09 * cliques)
                banca += ganho
                lucro_total += ganho
                vitorias += 1
                print(f"✅ Vitória com {cliques} cliques! Lucro: R${ganho:.2f}")
                with open("log.csv", "a") as f:
                    f.write(f"VITORIA,{cliques},{prob:.2f}%,{ganho:.2f},{banca:.2f}\n")
                break
        else:
            banca -= APOSTA
            lucro_total -= APOSTA
            cliques -= 1
            derrotas += 1
            print(f"❌ Derrota. Perdeu R${APOSTA:.2f}")
            with open("log.csv", "a") as f:
                f.write(f"DERROTA,{cliques},{prob:.2f}%,{-APOSTA:.2f},{banca:.2f}\n")
            break

    print(f"💰 Banca atual: R${banca:.2f}\n")
    time.sleep(1)
