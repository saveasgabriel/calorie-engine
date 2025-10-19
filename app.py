import streamlit as st

# --- FUNÇÕES ---

def projetar_peso_dinamico(getd_inicial, tmb_inicial, peso_inicial, altura, idade, sexo, calorias_alvo, dias_projecao):
    peso_atual = peso_inicial
    gasto_adicional = (getd_inicial - tmb_inicial)

    for dia in range(1, dias_projecao + 1):
        if sexo == "Masculino":
            tmb_atual = 10 * peso_atual + 6.25 * altura - 5 * idade + 5
        else:
            tmb_atual = 10 * peso_atual + 6.25 * altura - 5 * idade - 161
        
        getd_atual = tmb_atual + gasto_adicional
        diferenca_calorica = calorias_alvo - getd_atual
        mudanca_kg = diferenca_calorica / 7700
        peso_atual += mudanca_kg
        
    return peso_atual

def resetar_campos_treino():
    st.session_state.duracao_input = None
    st.session_state.frequencia_input = None

st.set_page_config(page_title="Calculadora de Metas", layout="centered")
st.title("Calculadora de Calorias e Metas")
st.write("Siga os passos abaixo para descobrir seu gasto calórico e definir suas metas nutricionais.")
st.divider()

st.subheader("Passo 1: Insira seus dados")
st.write("Comece com suas informações básicas para calcularmos seu metabolismo em repouso.")

sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
idade = st.number_input("Idade (anos)", min_value=10, max_value=120, value=25)
peso = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=71.0)
altura = st.number_input("Altura (cm)", min_value=120.0, max_value=250.0, value=175.0)

if sexo == "Masculino":
    tmb = 10 * peso + 6.25 * altura - 5 * idade + 5
else:
    tmb = 10 * peso + 6.25 * altura - 5 * idade - 161

st.write("#### Resultado: Seu Metabolismo Basal (TMB)")
st.success(f"A energia mínima que seu corpo gasta em repouso é de **{tmb:.0f} kcal** por dia.")

with st.expander("O que isso significa?"):
    st.write(
        """
        A Taxa Metabólica Basal (TMB) é o número de calorias que seu corpo queima em repouso absoluto, 
        apenas para manter funções vitais. Utilizamos a fórmula de **Mifflin-St Jeor**, considerada 
        uma das mais precisas para a população geral.
        """
    )

st.divider()

st.subheader("Passo 2: Adicione seus treinos")
st.write("Registre as atividades físicas que você faz regularmente.")

if "atividades" not in st.session_state:
    st.session_state.atividades = {
        "Musculação (leve)": 3.0, "Musculação (moderada)": 4.5, "Musculação (intensa)": 6.0, "Crossfit": 6.0,
        "Funcional (intenso)": 7.0, "Caminhar (5,5km/h)": 3.5, "Caminhar (6,5km/h)": 5.0,
        "Corrida (9,5km/h)": 10.0, "Corrida (12km/h)": 12.5, "Corrida (15km/h)": 15.0,
        "Pedal (16-19km/h)": 6.0, "Pedal (22-25km/h)": 10.0, "Natação (moderado)": 7.0,
        "Futebol": 8.0, "Muay Thai (intenso)": 10.0, "Jiu-jitsu (Posição)": 3.0,
        "Jiu-jitsu (Rola)": 10.0, "Boxe": 6.0
    }

st.write("##### Registre uma sessão de treino")

def registrar_sessao():
    if not st.session_state.duracao_input or not st.session_state.frequencia_input:
        st.warning("Por favor, preencha a duração e a frequência para registrar a sessão.")
        return

    atividade_key = st.session_state.atividade_selecionada
    sessao = {
        "atividade": atividade_key,
        "met": st.session_state.atividades[atividade_key],
        "duracao_h": st.session_state.duracao_input / 60,
        "frequencia": st.session_state.frequencia_input
    }
    st.session_state.sessoes.append(sessao)
    
    st.session_state.duracao_input = None
    st.session_state.frequencia_input = None

if "sessoes" not in st.session_state:
    st.session_state.sessoes = []

atividade_escolhida = st.selectbox(
    "Atividade", 
    options=list(st.session_state.atividades.keys()), 
    on_change=resetar_campos_treino, 
    key="atividade_selecionada"
)
duracao_min = st.number_input(
    "Duração (minutos)", 
    min_value=1, 
    max_value=300, 
    placeholder="Ex: 60", 
    key="duracao_input"
)
frequencia = st.number_input(
    "Frequência (vezes por semana)", 
    min_value=1, 
    max_value=14, 
    placeholder="Ex: 3", 
    key="frequencia_input"
)

st.button("Registrar sessão de treino", on_click=registrar_sessao)

calorias_atividades = sum(s["met"] * peso * s["duracao_h"] * s["frequencia"] for s in st.session_state.sessoes)

st.write("#### Resultado: Gasto com Treinos")
st.info(f"O gasto calórico semanal com seus treinos é de **{calorias_atividades:.0f} kcal**.")

if st.session_state.sessoes:
    st.write("###### Sessões Registradas")
    for i, sessao in enumerate(st.session_state.sessoes):
        gasto_semanal = sessao['met'] * peso * sessao['duracao_h'] * sessao['frequencia']
        col1, col2 = st.columns([8, 1])
        with col1:
            st.markdown(f"**{sessao['atividade']}**: {sessao['frequencia']}x semana, {sessao['duracao_h']*60:.0f} min | Gasto: **{gasto_semanal:.0f} kcal**")
        with col2:
            if st.button("🗑️", key=f"delete_session_{i}", help="Excluir esta sessão"):
                st.session_state.sessoes.pop(i)
                st.rerun()

with st.expander("Adicionar uma nova atividade ou saber mais sobre METs"):
    st.write("Se sua atividade não está na lista, você pode adicioná-la abaixo.")
    col1, col2 = st.columns(2)
    with col1:
        nova_atividade = st.text_input("Nome da nova atividade")
    with col2:
        novo_met = st.number_input("Valor de MET", min_value=1.0, max_value=20.0, value=6.0)
    
    if st.button("Cadastrar nova atividade") and nova_atividade:
        st.session_state.atividades[nova_atividade] = novo_met
        st.rerun()
    
    st.divider()
    st.write(
        """
        **O que é MET?** É o Equivalente Metabólico da Tarefa. Ele mede quanta energia uma atividade consome em comparação com o repouso. 
        Um MET de 5, por exemplo, significa que você está queimando 5 vezes mais calorias do que se estivesse sentado quieto.
        """
    )
    st.markdown("Não sabe o valor de MET? [Pesquise aqui no Compêndio de Atividades Físicas](https://sites.google.com/site/compendiumofphysicalactivities/home).", unsafe_allow_html=True)

st.divider()

st.subheader("Passo 3: Atividades do dia a dia (NEAT)")
st.write(
    """
    **NEAT** é o gasto calórico com tudo o que você faz fora dos treinos, como caminhar ou tarefas domésticas. 
    A contagem de passos é uma ótima forma de estimá-lo.
    """
)
passos = st.number_input("Média de passos diários", min_value=0, max_value=50000, value=8000)
calorias_passos = passos * peso * 0.0005
st.info(f"Gasto diário estimado com seus passos: **{calorias_passos:.0f} kcal**.")
st.caption("Dica: Não inclua aqui os passos de treinos que você já registrou no Passo 2.")

st.divider()

st.subheader("Resultado: Seu Gasto Calórico Diário Total")
media_diaria_atividades = calorias_atividades / 7 if calorias_atividades else 0
getd = tmb + media_diaria_atividades + calorias_passos
st.write("Somando seu metabolismo, treinos e atividades diárias, esta é a sua necessidade calórica para manter o peso atual.")
st.metric(label="Gasto Calórico Total Estimado (GETD)", value=f"{getd:.0f} kcal/dia")

st.divider()

st.subheader("Passo 5: Defina suas metas e plano")
st.write("Com base no seu gasto total, defina um objetivo e veja como montar seu plano alimentar.")

objetivo = st.selectbox("Qual é o seu principal objetivo?", ["Manter o Peso", "Perder Peso (Déficit)", "Ganhar Peso (Superávit)"])

if objetivo == "Perder Peso (Déficit)":
    ajuste = st.slider("Selecione o percentual de déficit calórico (%)", 5, 30, 15)
    calorias_alvo = getd * (1 - ajuste / 100)
elif objetivo == "Ganhar Peso (Superávit)":
    ajuste = st.slider("Selecione o percentual de superávit calórico (%)", 5, 25, 15)
    calorias_alvo = getd * (1 + ajuste / 100)
else:
    calorias_alvo = getd

st.success(f"Sua meta de consumo diário é de aproximadamente **{calorias_alvo:.0f} kcal**.")
st.divider()

tab1, tab2, tab3 = st.tabs(["Distribuição de Macros", "Exemplos de Alimentos", "Projeção de Peso"])

with tab1:
    st.write("#### Distribuição de Macronutrientes")
    st.write("Ajuste as barras para definir a distribuição de proteínas, gorduras e carboidratos.")
    
    proteina_g_kg = st.slider("Proteína (gramas por kg de peso)", 1.6, 2.5, 2.0, 0.1)
    gordura_perc = st.slider("Gordura (% do total de calorias)", 15, 35, 25, 1)

    calorias_proteina = (peso * proteina_g_kg) * 4
    proteina_gramas = calorias_proteina / 4
    calorias_gordura = calorias_alvo * (gordura_perc / 100)
    gordura_gramas = calorias_gordura / 9
    calorias_carboidratos = calorias_alvo - calorias_proteina - calorias_gordura
    carboidratos_gramas = calorias_carboidratos / 4

    if carboidratos_gramas < 0:
        st.error("Atenção: A quantidade de proteína e gordura selecionada excede sua meta calórica. Ajuste os valores.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Proteínas", f"{proteina_gramas:.0f} g", f"{calorias_proteina:.0f} kcal")
        col2.metric("Carboidratos", f"{carboidratos_gramas:.0f} g", f"{calorias_carboidratos:.0f} kcal")
        col3.metric("Gorduras", f"{gordura_gramas:.0f} g", f"{calorias_gordura:.0f} kcal")

with tab2:
    st.write("#### Exemplos de Alimentos (Referências)")
    st.caption("Atenção: Estes são apenas exemplos para dar uma noção das quantidades. Eles não constituem um plano alimentar e os valores nutricionais podem variar. Consulte um nutricionista.")

    if carboidratos_gramas >= 0:
        arroz_equivalente = carboidratos_gramas * 3.57
        pasta_equivalente = gordura_gramas * 2.0
        
        fonte_proteina = st.radio(
            "Escolha uma fonte de proteína para referência:",
            ["Carne Moída (Patinho)", "Proteína de Soja Texturizada"]
        )

        if fonte_proteina == "Carne Moída (Patinho)":
            proteina_equivalente = proteina_gramas * 3.22
            texto_proteina = f"Sua meta de **{proteina_gramas:.0f} g** equivale a aprox. **{proteina_equivalente:.0f} g** de patinho moído cozido."
            emoji_proteina = "🥩"
        else:
            proteina_equivalente = proteina_gramas * 6.25
            texto_proteina = f"Sua meta de **{proteina_gramas:.0f} g** equivale a aprox. **{proteina_equivalente:.0f} g** de proteína de soja texturizada (cozida)."
            emoji_proteina = "🌱"

        col1_food, col2_food, col3_food = st.columns(3)
        with col1_food:
            st.markdown(f"🍚 **Carboidratos**")
            st.markdown(f"Sua meta de **{carboidratos_gramas:.0f} g** equivale a aprox. **{arroz_equivalente:.0f} g** de arroz branco cozido.")
        with col2_food:
            st.markdown(f"{emoji_proteina} **Proteínas**")
            st.markdown(texto_proteina)
        with col3_food:
            st.markdown(f"🥜 **Gorduras**")
            st.markdown(f"Sua meta de **{gordura_gramas:.0f} g** equivale a aprox. **{pasta_equivalente:.0f} g** de pasta de amendoim.")

with tab3:
    if objetivo != "Manter o Peso":
        st.write("#### Projeção Realista de Peso")
        st.write(
            """
            Esta projeção simula como seu peso tende a mudar, considerando que seu metabolismo se adapta 
            conforme seu corpo muda (um corpo mais leve gasta menos energia, e vice-versa). 
            É por isso que a mudança de peso desacelera com o tempo.
            """
        )
        periodos = {"Em 30 dias": 30, "Em 3 meses": 91, "Em 6 meses": 182, "Em 1 ano": 365}
        cols = st.columns(len(periodos))
        
        for i, (label, dias) in enumerate(periodos.items()):
            peso_projetado = projetar_peso_dinamico(getd, tmb, peso, altura, idade, sexo, calorias_alvo, dias)
            cols[i].metric(label, f"{peso_projetado:.1f} kg", f"{(peso_projetado - peso):.1f} kg")
    else:
        st.info("A projeção de peso é exibida quando você seleciona um objetivo de 'Perder Peso' ou 'Ganhar Peso'.")

st.divider()
st.markdown(
    "Desenvolvido por **Gabriel França** | Contato: [saveasgabriel@gmail.com](mailto:saveasgabriel@gmail.com) | Instagram: [@saveasfranca](https://instagram.com/saveasgabriel)"
)