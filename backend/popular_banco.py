import logging
from app.database import SessionLocal # Ajuste o import se o seu arquivo de banco tiver outro nome
from app.services.collector import coletar_camara, coletar_senado

# Configura o log para você ver o progresso no terminal
logging.basicConfig(level=logging.INFO)

def carga_inicial():
    print("Iniciando a carga histórica de dados...")
    db = SessionLocal()
    try:
        # Troque 2023 pelo ano que o squad definiu como escopo
        total_camara = coletar_camara(db, ano_inicial=2000)
        print(f"Câmara finalizada! {total_camara} registros.")

        total_senado = coletar_senado(db, ano_inicial=2000)
        print(f"Senado finalizado! {total_senado} registros.")
        
        print("Carga inicial concluída com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro durante a carga: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    carga_inicial()