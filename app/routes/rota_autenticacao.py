from fastapi import APIRouter

autenticacao_router = APIRouter()  # Instanciando como uma rota do FastAPI


@autenticacao_router.post("/auth/login")  # logar
def login():

    return


@autenticacao_router.post("/auth/logout")  # deslogar
def lgout():

    return


@autenticacao_router.post("/auth/refresh")  # atualizar token
def refresh():

    return

# Por que atualizar o token?
# Segurança: O access token tem um tempo de vida curto (ex: 15 minutos) para reduzir riscos caso seja comprometido.
# Experiência do usuário: O usuário não precisa inserir login/senha frequentemente.
# Eficiência: Evita a necessidade de armazenar credenciais no frontend ou enviá-las com frequência.
# O usuário faz login e recebe dois tokens:
# Access token (expira rápido, usado para acessar APIs).
# Refresh token (expira depois de dias/semanas, usado para gerar novos access tokens).
# Quando o access token expira, o usuário envia o refresh token para obter um novo access token sem precisar logar novamente.
# Se o refresh token também expirar, o usuário precisa fazer login novamente.
