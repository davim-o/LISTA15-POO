import streamlit as st
import pandas as pd
import time
from views import View

class PerfilProfissionalUI:
    def main():
        st.header("Meus Dados")

        op = View.profissional_listar_id(st.session_state["usuario_id"])

        if op is None:
            st.warning("Nenhum profissional logado.")
            return

        profissional_id = op.get_id() 

        # Campos de edição do perfil
        nome = st.text_input("Informe o novo nome", op.get_nome())
        email = st.text_input("Informe o novo e-mail", op.get_email())
        especialidade = st.text_input("Informe a nova especialidade", op.get_especialidade())
        conselho = st.text_input("Informe o novo conselho", op.get_conselho())
        senha = st.text_input("Informe a nova senha", op.get_senha(), type="password")

        if st.button("Atualizar Dados"):
            View.profissional_atualizar(profissional_id, nome, especialidade, conselho, email, senha)
            st.success("Profissional atualizado com sucesso")
            time.sleep(2)
            st.rerun()


        st.subheader("Minhas Avaliações")

        horarios = View.horario_listar()
        avaliacoes = [
            h for h in horarios
            if h.get_id_profissional() == profissional_id and h.get_avaliacao() is not None
        ]

        if len(avaliacoes) == 0:
            st.info("Você ainda não recebeu avaliações de clientes.")
        else:
            dados = []
            for h in avaliacoes:
                cliente = View.cliente_listar_id(h.get_id_cliente())
                nome_cliente = cliente.get_nome() if cliente else "Cliente desconhecido"
                dados.append({
                    "Data": h.get_data().strftime("%d/%m/%Y %H:%M"),
                    "Cliente": nome_cliente,
                    "Avaliação (⭐)": h.get_avaliacao(),
                    "Comentário": h.get_comentario()
                })

            df = pd.DataFrame(dados)
            st.dataframe(df, hide_index=True)

            # Exibe média de avaliações
            media = sum([h.get_avaliacao() for h in avaliacoes]) / len(avaliacoes)
            st.success(f"Média de Avaliações: ⭐ {media:.1f}/5")
