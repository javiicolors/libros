from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
DATABASE_URL= "postgresql://postgres.qjoeasmysvpnydntmjhu:[YOUR-PASSWORD]@aws-0-us-east-2.pooler.supabase.com:6543/postgres?pgbouncer=true"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Libro(Base):
    __tablename__ = 'libros'

    id = Column(Integer, primary_key=True, index=True)
    nombre_libro = Column(String, nullable=False)
    paginas_totales = Column(Integer, nullable=False)
    paginas_leidas = Column(Integer, nullable=False)
    completado = Column(Boolean, default=False)
    resumen_personal = Column(Text)

def calcular_completado(paginas_leidas, paginas_totales):
    return (paginas_leidas / paginas_totales) * 100 >= 95

def marcar_como_completado(session, libro_id):
    session.query(Libro).filter_by(id=libro_id).update({Libro.completado: True})

# Ejemplo de uso
def main():
    session = SessionLocal()
    try:
        # Ejemplo: marcar un libro como completado
        libro = session.query(Libro).filter_by(id=1).first()
        if libro:
            porcentaje_completado = calcular_completado(libro.paginas_leidas, libro.paginas_totales)
            if porcentaje_completado:
                marcar_como_completado(session, libro.id)
                print(f"El libro '{libro.nombre_libro}' está completado.")
            else:
                print(f"El libro '{libro.nombre_libro}' no está completado.")
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    main()
