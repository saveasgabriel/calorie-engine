"""Calculadora de gasto calórico com TMB, MET e estimativa por passos.

Feito por Gabriel França.
"""

import streamlit as st

st.set_page_config(page_title="Calculadora de Gasto Calórico", layout="centered")
st.title("Calculadora de Gasto Calórico")

st.header("Módulo 1: Perfil do Usuário e Metabolismo Basal")
sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])
idade = st.number_input("Idade (anos)", min_value=10, max_value=120, value=25)
peso = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, value=71.0)
altura = st.number_input("Altura (cm)", min_value=120.0, max_value=250.0, value=175.0)
bf = st.number_input("Percentual de Gordura Corporal (%)", min_value=3.0, max_value=60.0, value=12.0)

"""Calcula a Massa Corporal Magra (MCM) a partir do peso e percentual de gordura corporal (BF%)."""
mcm = peso * (1 - (bf / 100))

"""Calcula a TMB pelo método Katch-McArdle usando MCM."""
tmb_katch = 370 + (21.6 * mcm)

"""Calcula a TMB pelo método Mifflin-St Jeor (usa sexo, peso, altura e idade)."""
if sexo == "Masculino":
    tmb_mifflin = 10 * peso + 6.25 * altura - 5 * idade + 5
else:
    tmb_mifflin = 10 * peso + 6.25 * altura - 5 * idade - 161

st.success(f"TMB (Katch-McArdle): {tmb_katch:.0f} kcal/dia")
st.info(f"TMB (Mifflin-St Jeor): {tmb_mifflin:.0f} kcal/dia")

"""Exibe as fórmulas utilizadas nos cálculos."""
st.markdown("**Fórmulas utilizadas:**")
st.markdown("- Massa Corporal Magra (MCM):")
st.latex(r"MCM = peso \times (1 - \frac{BF}{100})")
st.markdown("- Taxa Metabólica Basal (Katch-McArdle):")
st.latex(r"TMB_{Katch} = 370 + 21.6 \times MCM")
st.markdown("- Taxa Metabólica Basal (Mifflin-St Jeor):")
st.latex(r"TMB_{Mifflin}^{homem} = 10 \times peso + 6.25 \times altura - 5 \times idade + 5")
st.latex(r"TMB_{Mifflin}^{mulher} = 10 \times peso + 6.25 \times altura - 5 \times idade - 161")

# Permitir ao usuário escolher qual TMB usar nos cálculos finais
tmb_choice = st.radio("Escolha qual TMB usar para a consolidação:", ("Katch-McArdle (usa BF%)", "Mifflin-St Jeor"))
tmb = tmb_katch if tmb_choice.startswith("Katch") else tmb_mifflin
st.markdown(f"**TMB selecionada para os cálculos finais:** {tmb:.0f} kcal/dia ({tmb_choice})")

st.header("Módulo 2: Registro de Atividades Físicas Planejadas")
"""Cadastro de atividades e valores MET (padrões pré-carregados)."""
st.subheader("Cadastrar nova atividade")
if "atividades" not in st.session_state:
    st.session_state["atividades"] = [
        "Musculação intensidade moderada",
        "Musculação intensidade alta",
        "Crossfit",
        "Funcional intenso",
        "Caminhar a 5,5km/h",
        "Caminhar a 6,5km/h",
        "Corrida 12km/h",
        "Corrida 9,5km/h",
        "Corrida 15km/h",
        "Pedal 22-25km/h",
        "Pedal 16-19km/h",
        "Natação moderado",
        "Futebol",
        "Muay thai intenso",
        "Jiujitsu Posição",
        "Jiujitsu Rola",
        "Boxe",
    ]
    st.session_state["met_vals"] = [
        4.5,
        6.0,
        6.0,
        7.0,
        3.5,
        5.0,
        12.5,
        10.0,
        15.0,
        10.0,
        6.0,
        7.0,
        8.0,
        10.0,
        3.0,
        10.0,
        6.0,
    ]

nova_atividade = st.text_input("Nome da atividade")
novo_met = st.number_input("Valor de MET", min_value=1.0, max_value=20.0, value=6.0)
if st.button("Cadastrar atividade") and nova_atividade:
    st.session_state["atividades"].append(nova_atividade)
    st.session_state["met_vals"].append(novo_met)

"""Interface para registrar sessões de treino (atividade, duração, frequência)."""
st.subheader("Registrar sessão de treino")
atividade_idx = st.selectbox("Atividade", range(len(st.session_state["atividades"])), format_func=lambda x: st.session_state["atividades"][x] if st.session_state["atividades"] else "Cadastre uma atividade")
duracao_min = st.number_input("Duração (minutos)", min_value=1, max_value=300, value=60)
frequencia = st.number_input("Frequência semanal", min_value=1, max_value=14, value=3)

if "sessoes" not in st.session_state:
    st.session_state["sessoes"] = []

if st.button("Registrar sessão") and st.session_state["atividades"]:
    sessao = {
        "atividade": st.session_state["atividades"][atividade_idx],
        "met": st.session_state["met_vals"][atividade_idx],
        "duracao_h": duracao_min / 60,
        "frequencia": frequencia
    }
    st.session_state["sessoes"].append(sessao)

"""Calcula o gasto semanal total a partir das sessões registradas."""
calorias_atividades = 0
for sessao in st.session_state["sessoes"]:
    gasto = sessao["met"] * peso * sessao["duracao_h"] * sessao["frequencia"]
    calorias_atividades += gasto
st.info(f"Gasto calórico semanal com atividades planejadas: {calorias_atividades:.0f} kcal")
st.markdown("**Fórmula usada para cada sessão de treino:**")
st.latex(r"Gasto\ por\ sessão\ (kcal) = MET \times peso\ (kg) \times duração\ (h)")
st.markdown("Como o app multiplica por frequência semanal, o gasto semanal por sessão é: MET × peso × duração(h) × frequência")

"""Exibe tabela com os registros de sessões e seus gastos (se houver)."""
if st.session_state.get("sessoes"):
    st.subheader("Registros de sessões cadastradas")
    registros = []
    for sessao in st.session_state["sessoes"]:
        gasto_por_sessao = sessao["met"] * peso * sessao["duracao_h"]
        gasto_semanal = gasto_por_sessao * sessao["frequencia"]
        contrib_diaria = gasto_semanal / 7
        registros.append({
            "Atividade": sessao["atividade"],
            "MET": sessao["met"],
            "Duração (h)": round(sessao["duracao_h"], 2),
            "Frequência (semanal)": sessao["frequencia"],
            "Gasto por sessão (kcal)": round(gasto_por_sessao, 1),
            "Gasto semanal (kcal)": round(gasto_semanal, 1),
            "Contribuição diária (kcal)": round(contrib_diaria, 1),
        })
    st.table(registros)
else:
    st.info("Nenhuma sessão registrada ainda. Use 'Registrar sessão' para adicionar suas sessões planejadas.")

st.header("Módulo 3: Estimativa de Gasto por Passos (NEAT)")
passos = st.number_input("Média de passos diários", min_value=0, max_value=50000, value=8000)
calorias_passos = passos * peso * 0.0005
st.info(f"Gasto calórico diário estimado por passos: {calorias_passos:.0f} kcal")
st.warning("Não inclua os passos de atividades já registradas no Módulo 2 para evitar cálculo duplicado.")
st.markdown("**Fórmula usada para estimativa por passos (NEAT):**")
st.latex(r"Gasto\ diário\ por\ passos\ (kcal) = passos \times peso\ (kg) \times 0.0005")

st.header("Módulo 4: Consolidação e Resultado Final")
media_diaria_atividades = calorias_atividades / 7 if calorias_atividades else 0
getd = tmb + media_diaria_atividades + calorias_passos
st.success(f"Sua média de gasto calórico diário é de aproximadamente {getd:.0f} kcal.")
st.markdown("**Como a média final é calculada:**")
st.latex(r"M\acute{e}dia\ diaria\ (kcal) = TMB + \frac{Gasto\ semanal\ (atividades)}{7} + Gasto\ diário\ por\ passos")


st.markdown("---")
st.markdown(
    "By: **Gabriel França**  |    Email: [saveasgabriel@gmail.com](mailto:saveasgabriel@gmail.com)  |    Instagram: [@saveasfranca](https://instagram.com/saveasfranca)"
)
