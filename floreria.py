import copy
from abc import ABC, abstractmethod

# FLORES
class Flor(ABC):
    def __init__(self, nombre):
        self.nombre = nombre
    @abstractmethod
    def significado(self):
        pass
    @abstractmethod
    def precio(self):
        pass
    def ingredientes(self): 
        return [self.nombre]
    def detalle(self):
        return [self]

class Rosa(Flor):
    def significado(self):
        return "Amor y pasion"
    def precio(self):
        return 9

class Tulipan(Flor):
    def significado(self):
        return "Amor sincero, elegancia y nuevos comienzos"
    def precio(self):
        return 6

class Girasol(Flor):
    def significado(self):
        return "Energia, vitalidad, alegria y fidelidad"
    def precio(self):
        return 7

# PATRON ESTRUCTURAL: Composite
# Un Ramo es una flor que contiene otras flores, el resto del sistema lo trata igual que a una flor sola (misma interfaz, precio sumado)
class Ramo(Flor):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.hijos = []
    def agregar(self, flor):
        self.hijos.append(flor)
    def significado(self):
        return " + ".join(f.significado() for f in self.hijos)
    def precio(self):
        return sum(f.precio() for f in self.hijos)
    def ingredientes(self):
        return [i for f in self.hijos for i in f.ingredientes()]
    def detalle(self):
        return [d for f in self.hijos for d in f.detalle()]

    # PATRON CREACIONAL: Prototype
    # El "Ramo de la casa" ya esta armado asi en vez de armar uno desde cero se clona y se personaliza
    # (deepcopy ayuda a que cada ramo tenga sus propias flores)
    def clonar(self):
        return copy.deepcopy(self)

# PATRON ESTRUCTURAL: Decorator
# El liston envuelve cualquier flor o ramo y le suma 2 Bs sin modificar sus clases ni crear otras
class ConListon(Flor):
    def __init__(self, flor):
        super().__init__(flor.nombre + " con liston")
        self.flor = flor
    def significado(self):
        return self.flor.significado()
    def precio(self):
        return self.flor.precio() + 2
    def ingredientes(self):
        return self.flor.ingredientes() + ["liston"]
    def detalle(self):
        return self.flor.detalle()

# PATRON DE COMPORTAMIENTO: Strategy
# Cada regla de descuento es intercambiable y el gestor no sabe cual usa
class Descuento(ABC):
    @abstractmethod
    def aplicar(self, total):
        pass

class SinDescuento(Descuento):
    def aplicar(self, total):
        return total

class Aniversario(Descuento):
    def aplicar(self, total):
        return total * 0.85

class Estudiante(Descuento):
    def aplicar(self, total):
        return total * 0.90

# AVISOS
class Notificable(ABC):
    @abstractmethod
    def avisar(self, flores, total):
        pass

class Cliente(Notificable):
    def __init__(self, nombre):
        self.nombre = nombre
    def avisar(self, flores, total):
        print(f"Hola {self.nombre}, tu pedido:")
        for flor in flores:
            print(f"  {flor.nombre} ({flor.precio()} Bs)")
            for f in flor.detalle():
                print(f"    - {f.nombre}: {f.significado()}")
        print(f"  Total a pagar: {total:.2f} Bs")

class Florista(Notificable):
    def __init__(self, nombre):
        self.nombre = nombre
    def avisar(self, flores, total):
        print(f"{self.nombre}, alista:")
        for flor in flores:
            for item in flor.ingredientes():
                print(f"  - {item}")

# PEDIDOS
class GestorDePedidos:
    def __init__(self, notificable, descuento=SinDescuento()):
        self.notificable = notificable
        self.descuento = descuento
        self.flores = []
    def agregar_flor(self, flor):
        self.flores.append(flor)
    def confirmar_pedido(self):
        subtotal = sum(f.precio() for f in self.flores)
        self.notificable.avisar(self.flores, self.descuento.aplicar(subtotal))

# Probar el codigo
if __name__ == "__main__":
    # Ramo de la casa (ya armado en catalogo)
    ramo_casa = Ramo("Ramo de la casa")
    ramo_casa.agregar(Rosa("rosa roja"))
    ramo_casa.agregar(Tulipan("tulipán rosado"))

    ramo_leo = ramo_casa.clonar()
    ramo_leo.nombre = "Ramo de Leo"
    ramo_leo.agregar(Girasol("girasol"))
    ramo_leo = ConListon(ramo_leo)

    pedido_cliente = GestorDePedidos(Cliente("Leo"), Aniversario())
    pedido_cliente.agregar_flor(ramo_leo)
    pedido_cliente.confirmar_pedido()
    print()

    pedido_florista = GestorDePedidos(Florista("Ali"))
    pedido_florista.agregar_flor(ramo_leo)
    pedido_florista.confirmar_pedido()
    print()