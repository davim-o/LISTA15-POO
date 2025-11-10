import streamlit as st
from views import View
import time

class AvaliarServicoUI:
    def main():
        st.header("Avaliar Serviço Realizado")

        usuario_id = st.session_state.get("usuario_id")
        if not usuario_id:
            st.warning("Você precisa estar logado como cliente para avaliar um serviço.")
            return

        horarios = View.horario_listar()
        realizados = [
            h for h in horarios
            if h.get_id_cliente() == usuario_id and h.get_confirmado() and h.get_avaliacao() is None
        ]

        if len(realizados) == 0:
            st.info("Você não possui serviços concluídos sem avaliação.")
            return

        op = st.selectbox(
            "Selecione o serviço que deseja avaliar",
            realizados,
            format_func=lambda h: f"{h.get_id()} - {h.get_data().strftime('%d/%m/%Y %H:%M')}"
        )

        nota = st.slider("Dê uma nota para o atendimento", 1, 5, 5)
        comentario = st.text_area("Deixe um comentário")

        if st.button("Enviar Avaliação"):
            View.horario_avaliar(op.get_id(), nota, comentario)
            st.success("Avaliação registrada com sucesso!")
            time.sleep(2)
            st.rerun()
