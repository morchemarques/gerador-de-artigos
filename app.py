import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração visual
st.set_page_config(page_title="Meu Gerador IA", layout="centered")
API_KEY = "AIzaSyBVgNlYbY-EvCSgWgdERiWhf2q0PGU7kCw"
genai.configure(api_key=API_KEY)

st.title("📝 Assistente de Redação Profissional")

# Entradas
link_anterior = st.text_input("Link para 'VEJA TAMBÉM':", placeholder="Cole o link anterior aqui...")
input_texto = st.text_area("O que vamos escrever hoje?", placeholder="Ex: Receita de Pipoca...", height=150)
foto = st.file_uploader("📷 Adicionar Foto (Opcional)", type=['png', 'jpg', 'jpeg'])

if st.button("GERAR ARTIGO COMPLETO"):
    if not input_texto and not foto:
        st.error("Descreva o conteúdo ou envie uma foto.")
    else:
        with st.spinner("A IA está trabalhando..."):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Suas Regras Personalizadas
                prompt = f"""
                Aja como redator profissional para os blogs: Nossas Receitas, De Histórias e Vendas & Ganhos.
                REGRAS:
                1. Comece com 1 emoji.
                2. Use apenas um tema central.
                3. PROIBIDO usar tabelas.
                4. 'TEMPO E INFORMAÇÕES EXTRAS' em MAIÚSCULAS antes da DESCRIÇÃO.
                5. Se for fruta, inclua histórias infantis ou folclore.
                6. 'COMO FAZER' em lista numerada.
                7. Link final 'VEJA TAMBÉM': {link_anterior if link_anterior else 'não informado'}.
                Separe o Texto do Código HTML usando: [DIVISOR]

                CONTEÚDO: {input_texto}
                """
                
                partes = [prompt]
                if foto:
                    partes.append(Image.open(foto))
                
                response = model.generate_content(partes)
                res = response.text.split("[DIVISOR]")
                
                st.subheader("Visualização:")
                st.write(res[0].strip())
                
                st.subheader("Código HTML para o Blogger:")
                st.code(res[1].strip() if len(res) > 1 else res[0], language='html')
                
            except Exception as e:
                st.error(f"Erro: {e}")
