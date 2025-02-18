# 1. Usuário
# POST /usuarios/ → Criar usuário
# GET /usuarios/{id} → Consultar perfil do usuário
# PUT /usuarios/{id} → Atualizar perfil
# DELETE /usuarios/{id} → Excluir usuário
# 2. Autenticação
# POST /auth/login → Fazer login
# POST /auth/logout → Fazer logout
# POST /auth/refresh → Atualizar token
# 3. Grade e Disciplinas
# GET /grade/{id} → Consultar grade de horários do usuário
# GET /disciplinas/ → Listar disciplinas disponíveis
# POST /disciplinas/matricular → Matricular-se em disciplina
# DELETE /disciplinas/remover → Remover disciplina da matrícula
# GET /disciplinas/ementas → Obter ementas das disciplinas
# 4. Transporte
# GET /transporte/publico → Obter horários de transporte público
# GET /transporte/intercampi → Obter horários de intercampi
# 5. Editais e Concursos
# GET /editais/ → Listar editais e concursos
# 6. Feedback
# POST /feedback/ → Enviar feedback
# GET /feedback/ → Consultar feedbacks enviados pelo usuário
