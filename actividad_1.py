# Lógica de Feedbacks y Penalización de 5 segundos (CORREGIDA)
            if st.session_state.validado:
                if st.session_state.correcto:
                    st.success(datos["feedback_ok"])
                    st.markdown("<div class='btn-siguiente'>", unsafe_allow_html=True)
                    if st.button("Siguiente ➡️", key=f"sig_{current_step}"):
                        st.session_state.pregunta_actual += 1
                        st.session_state.validado = False
                        st.session_state.correcto = False
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    # 1. Mostramos el mensaje de error inmediatamente
                    st.error(datos["feedback_error"])
                    
                    # 2. Creamos el espacio para el contador regresivo
                    placeholder_timer = st.empty()
                    
                    # 3. Realizamos el conteo visual segundo a segundo
                    for segundos_restantes in range(5, 0, -1):
                        placeholder_timer.warning(f"⏳ Espera {segundos_restantes} segundos para volver a intentarlo...")
                        time.sleep(1)
                    
                    # 4. Limpiamos el cartel del contador, reseteamos la validación y recargamos de forma limpia
                    placeholder_timer.empty()
                    st.session_state.validado = False
                    st.rerun()
