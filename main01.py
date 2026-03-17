from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# criar base da classe 
Base = declarative_base()

# tabela usuarios
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100))

    # relacionamento com pedidos (corrigido)
    pedidos = relationship("Pedido", back_populates="usuario")

    def __repr__(self):
        return f"Usuario - id={self.id}, nome={self.nome}"


# tabela pedidos
class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto = Column(String(150))

    # chave estrangeira
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # relacionamento
    usuario = relationship("Usuario", back_populates="pedidos")

    def __repr__(self):
        return f"Pedido - id={self.id}, produto={self.produto}"


# conexão com o banco
engine = create_engine("sqlite:///loja.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# criar usuário
usuario1 = Usuario(nome="kauã")

# criar pedidos
pedido1 = Pedido(produto="Iphone 17")
pedido2 = Pedido(produto="Notebook")

# associar pedidos ao usuário
usuario1.pedidos.append(pedido1)
usuario1.pedidos.append(pedido2)

# salvar no banco
session.add(usuario1)
session.commit()

print(f"usuario cadastrado: {usuario1.nome}")

# consulta
todos_usuario = session.query(Usuario).all()

for usuario in todos_usuario:
    print(f"\npedido: {usuario.nome}")
    for pedido in usuario.pedidos:
        print(f"pedido: {pedido.produto}")