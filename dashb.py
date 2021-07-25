import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import requests
import base64
import io


@st.cache
def indice():
    """funcao para buscar o arquivo index.csv no github, criar um dataframe e retornar uma lista com os dados
    da coluna 'ficha' que sao os nomes dos arquivos que serao usados adiante"""

    url_index = 'https://raw.githubusercontent.com/Edmilson-Filimone/datasets/main/index.csv'
    fil = requests.get(url_index).content
    df = pd.read_csv(io.StringIO(fil.decode('utf-8')))
    return list(df['ficha'])


@st.cache
def git_busca(nome):
    """funcao para buscar o arquivo csv (nome) no github e retorna um dataframe"""

    index = str(nome)
    url_index = f'https://raw.githubusercontent.com/Edmilson-Filimone/datasets/main/{index}.csv'
    fil = requests.get(url_index).content
    df = pd.read_csv(io.StringIO(fil.decode('utf-8')))
    return df


def div(h, cor, texto, curva):
    """funcao div - retorna uma string do texto HTML com propiedades
        ajustaveis(h-titulo(h1,h2)/paragrafo(p), cor, texto)"""

    main = f"""<div style="background-color:{cor};border-radius:{curva}px;padding:5px;font-family:;
            width:100%">
            <{h} style="color:white;text-align:center;">{texto}</{h}>
            </div>"""
    return main


def agregado():
    """Abre todos os arquivos csv no github cujos nomes estao na lista 'fichas (retornada pela funcao indice())
    E faz a soma da coluna 'total' de cada arquivo e adiciona na lista agg que sera usada no grafico cumulativo de
     linhas no dashboard'"""

    agg = []
    fichas = indice()
    for i in fichas:
        url_index = f'https://raw.githubusercontent.com/Edmilson-Filimone/datasets/main/{str(i)}.csv'
        fil = requests.get(url_index).content
        df = pd.read_csv(io.StringIO(fil.decode('utf-8')))
        agg.append(df['Total'].sum())
        print(agg)
    return agg


def dashboard():
    # side-bar label
    st.sidebar.markdown(div(h='h2', cor='#464e5F', curva=0, texto='Bio-Dashboard'), unsafe_allow_html=True)
    st.sidebar.text('')
    # side-bar form, select-box, botao da form:
    forma_1 = st.sidebar.form(key='form-1')
    forma_1.markdown("**Inventário**")
    select_box = forma_1.selectbox(label='', options=indice())
    sub = forma_1.form_submit_button('---ver---')
    if sub:
        df = git_busca(select_box)

        # lay-out: 3-colunas
        beta, gama, zeta = st.beta_columns(3)
        beta.markdown(div(h='h3', cor='#464e5F', curva=7, texto='Balanço (%)'), True)
        zeta.markdown(div(h='h3', cor='#464e5F', curva=7, texto=f'Número de animais ({select_box})'), True)

        # soma total de cada categoria no dataframe -- para o painel
        tot = df['Total'].sum()
        fem = df['Femeas'].sum()
        mach = df['Machos'].sum()
        cria = df['Crias'].sum()
        width = 100

        # Estrutura em HTML/CSS do painel #33F65C '#c9ddc9' #99ff99
        titulo = f"""<div style="background-color:#99ff99;padding:5px;border-radius:7px;font-family:
                ;width: {width}%"> 
                <h3 style="color:white;text-align:center;">Dados Gerais </h3>
                </div>"""

        total = f"""<div style="background-color:#464e5F;padding:5px;border-radius:7px;font-family: ;
                width: {width}%">
                <h3 style="color:white;text-align:left;"> Total: {tot}</h3>
                </div>"""

        femeas = f"""<div style="background-color:#464e5F;padding:5px;border-radius:7px;font-family:;
                width: {width}%">
                <h3 style="color:white;text-align:left;">Fêmeas: {fem}</h3>
                </div>"""

        machos = f"""<div style="background-color:#464e5F;padding:5px;border-radius:7px;font-family:;
                width: {width}%">
                <h3 style="color:white;text-align:left;">Machos: {mach} </h3>
                </div>"""

        crias = f"""<div style="background-color:#464e5F;padding:5px;border-radius:7px;font-family:
                width: {width}%">
                <h3 style="color:white;text-align:left;">Crias: {cria}</h3>
                </div>"""

        # integrado o HTML via markdown nas colunas
        gama.markdown(titulo, True)
        gama.text('')
        gama.markdown(total, True)
        gama.text('')
        gama.markdown(femeas, True)
        gama.text('')
        gama.markdown(machos, True)
        gama.text('')
        gama.markdown(crias, True)
        st.text('')  # espacamento entre o painel e a figura

        # grafico de barras (coluna 3 -zeta)
        fig = plt.figure(num=1, figsize=(8, 10), dpi=520)
        sns.barplot(data=df, x='Total', y='Gaiola', palette='mako_r')  # "mako_r")
        plt.ylabel('Gaiola', labelpad=12)
        plt.xlabel('Número de Murganhos', labelpad=12)
        plt.style.use('fivethirtyeight')
        # plt.tight_layout()
        zeta.pyplot(fig, clear_figure=True)  # plotando

        # grafico de pizza (coluna 1 - beta)
        fig2 = plt.figure(figsize=(10, 8), dpi=520)
        plt.style.use('seaborn')
        plt.pie(x=[df['Machos'].sum(), df['Femeas'].sum(), df['Crias'].sum()], labels=['Macho', 'Femeas', 'Crias'],
                autopct='%1.1f%%', explode=[0.04, 0.04, 0.04], pctdistance=0.82,
                colors=['#66b3ff', '#ffcc99', '#c9ddc9'])
        plt.tight_layout()
        plt.legend()

        # convertendo pizza chart para donut chart
        centre_circle = plt.Circle((0, 0), 0.60, fc='white')
        fig_2 = plt.gcf()
        fig_2.gca().add_artist(centre_circle)
        beta.pyplot(fig2, clear_figure=True)  # plotando

        # cabecalho para o grafico cumulativo de linhas
        st.markdown(div(h='h3', cor='#464e5F', curva=7, texto=' Variação do número de animais'), True)
        st.text('')  # espacamento entre o cabecalho e a figura

        # grafico de linhas com o numero de murganhos de todas as fichas
        fig3 = plt.figure(figsize=(14, 4), dpi=420)
        totais = agregado()
        # C29CFF
        sns.lineplot(x=indice(), y=totais, color='#95caff', linewidth=1.8, marker='o', markersize=14,
                     label='Número de animais')
        # plt.fill_between(x=indice(), y1=totais, color='#FFC7B2')
        plt.style.use('ggplot')
        plt.legend()
        plt.ylabel('Número de animais', labelpad=6)
        st.pyplot(fig3, clear_figure=True, use_container_width=True)  # plotando

        # cabecalho para o dataframe
        st.markdown(div(h='h3', cor='#464e5F', curva=7, texto=f'Tabela com os dados do inventário'), True)
        st.text('')

        # dataframe e download link
        st.dataframe(df, width=1000, height=430)
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        download = f'<a href="data:file/csv;base64,{b64}" download="{str(select_box)}.csv">Download ficheiro csv</a>'
        st.markdown(download, unsafe_allow_html=True)

    else:
        st.markdown("""Todo o conteúdo registrado no inventário biológico do biotério encontra-se 
        sumarizado nesse Dashboard.
### **Como proceder ?**
- Para ver a informação: escolha a ficha (inventario) que deseja ver e pressione o botão “ver”
### **O que você vai encontrar ?**
- Todos os registros devidamente organizados
- Gráficos explicativos com base no número de animais:\n
	- Percentagem de machos/ fêmeas / crias\n
	- Número de animais por gaiola\n
	- Numero total de animais por inventário\n  
- Tabela do inventário e uma opção de download
""")


def info():
    global ficheiro, ficha_id, data
    expander = st.sidebar.beta_expander('Notas importantes')
    expander.markdown('**Informação**')
    expander.info("""- Para melhor exibição
                    Selecione: Settings->Appearence->Wide mode
                    - Para mudar o tema
                    selecione: Settings->Theme""")
    expander.warning("""- No telefone o dashboard pode 
                        aparecer mal enquadrado.
                        para solucionar,
                        dentro do seu navegador selecione 
                        a opção "vista para site de computador":   
                        - No Chrome: site para   computador;    
                        - No Opera: site no computador""")
    expander_2 = st.sidebar.beta_expander('Sobre')
    expander_2.info("""- Bio-Dashboard v.1.0 
                        Desenvolvido em Python 3 | Streamlit framework, et al|      
                        Dev: Edmilson Filimone
                        Correspondência: philimone99@gmail.com""")


ficha_id = ''
ficheiro = ''
data = ''

if __name__ == '__main__':
    st.markdown(div(h='h2', cor='#464e5F', curva=0, texto='Biotério - Dashboard'), unsafe_allow_html=True)
    st.text('')
    dashboard()
    info()
