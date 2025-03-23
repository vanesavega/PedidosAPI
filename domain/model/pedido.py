from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from enum import Enum

class EstadoPedido(Enum):
    CREADO = "CREADO"
    CONFIRMADO = "CONFIRMADO"
    EN_PREPARACION = "EN_PREPARACION"
    LISTO = "LISTO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

class Pedido():
    
    def __init__( 
            self, 
            cliente: Cliente,
            items: List[ItemPedido],
            direccion_entrega: DireccionEntrega,
            id: Optional[UUID] = None,
            fecha_creacion: Optional[datetime] = None,
            estado: Optional[EstadoPedido] = None,
            total: Optional[TotalPedido] = None
    ):
        self.id = id or uuid4()
        self.cliente = cliente
        self.items = items
        self.direccion_entrega = direccion_entrega
        self.fecha_creacion = fecha_creacion or datetime.now()
        self.estado = estado or EstadoPedido.CREADO
        self.total = total or self.calcular_total()
    
    def calcular_total(self) -> TotalPedido:
        monto = sum([item.calcular_subtotal() for item in self.items])
        return TotalPedido(monto)
        

    def confirmar(self) -> None: 
        if self.estado != EstadoPedido.CREADO:
            raise ValueError("Solo se puede confirmar un pedido en estado CREADO")
        self.estado = EstadoPedido.CONFIRMADO
        pass

    def iniciar_preparacion(self) -> None:
        if self.estado != EstadoPedido.CONFIRMADO:
            raise ValueError("Solo se pueden preparar pedidos CONFIRMADOS")
        self.estado = EstadoPedido.EN_PREPARACION

    def marcar_listo(self) -> None:
        if self.estado != EstadoPedido.EN_PREPARACION:
            raise ValueError("Solo se pueden marcar como listos los pedidos EN_PREPARACION")
        self.estado = EstadoPedido.LISTO

    def entregar(self) -> None:
        if self.estado != EstadoPedido.LISTO:
            raise ValueError("Solo se pueden entregar pedidos LISTOS")
        self.estado = EstadoPedido.ENTREGADO

    def cancelar(self) -> None:
        estados_cancelables = [EstadoPedido.CREADO, EstadoPedido.CONFIRMADO, EstadoPedido.EN_PREPARACION]
        if self.estado not in estados_cancelables:
            raise ValueError(f"No se puede cancelar un pedido en estado {self.estado}")
        self.estado = EstadoPedido.CANCELADO

    

