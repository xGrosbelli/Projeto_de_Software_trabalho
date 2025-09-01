from datetime import datetime
from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, nome, cpf, endereco, telefone):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.telefone = telefone

    def get_info(self):
        return f"Nome: {self.nome}, CPF: {self.cpf}"

class Conta(ABC):
    def __init__(self, numero, cliente, saldo=0.0):
        self.numero = numero
        self.cliente = cliente
        self.saldo = saldo

    def depositar(self, valor):
        self.saldo += valor
        print(f"Depósito de R${valor:.2f}. Saldo atual: R${self.saldo:.2f}")

    @abstractmethod
    def sacar(self, valor): pass

    def transferir(self, valor, outra_conta):
        if valor <= self.saldo:
            self.sacar(valor)
            outra_conta.depositar(valor)
            print(f"Transferência de R${valor:.2f} para {outra_conta.cliente.nome} realizada com sucesso!")
        else:
            print("Saldo insuficiente para transferência.")

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, saldo=0.0, limite=0.0):
        super().__init__(numero, cliente, saldo)
        self.limite = limite

    def sacar(self, valor):
        if valor <= self.saldo + self.limite:
            self.saldo -= valor
            print(f"Saque de R${valor:.2f}. Saldo atual: R${self.saldo:.2f}")
        else:
            print("Saldo insuficiente.")

class ContaPoupanca(Conta):
    def __init__(self, numero, cliente, saldo=0.0, rendimento=0.0):
        super().__init__(numero, cliente, saldo)
        self.rendimento = rendimento

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            print(f"Saque de R${valor:.2f}. Saldo atual: R${self.saldo:.2f}")
        else:
            print("Saldo insuficiente.")

class Transacao:
    def __init__(self, id_transacao, valor, tipo):
        self.id = id_transacao
        self.data = datetime.now()
        self.valor = valor
        self.tipo = tipo

    def registrar(self):
        print(f"Transação {self.id} registrada em {self.data} - Tipo: {self.tipo}. Valor: R${self.valor:.2f}")

class Operacao(ABC):
    def __init__(self, conta, valor):
        self.conta = conta
        self.valor = valor

    @abstractmethod
    def executar(self): pass

class Deposito(Operacao):
    def executar(self):
        self.conta.depositar(self.valor)

class Saque(Operacao):
    def executar(self):
        self.conta.sacar(self.valor)

class Transferencia(Operacao):
    def __init__(self, conta_origem, conta_destino, valor):
        super().__init__(conta_origem, valor)
        self.conta_destino = conta_destino

    def executar(self):
        self.conta.transferir(self.valor, self.conta_destino)

class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.contas = []
    
    def criar_conta(self, conta):
        self.contas.append(conta)
        print(f"Conta {conta.numero} criada para {conta.cliente.nome}")
    
    def fechar_conta(self, numero):
        self.contas = [conta for conta in self.contas if conta.numero != numero]
        print(f"Conta {numero} fechada.")

    def listar_contas(self):
        for conta in self.contas:
            print(f"Número: {conta.numero} | Titular: {conta.cliente.nome} | Saldo: {conta.saldo:.2f}")

cliente1 = Cliente("Gabriel dos Santos", "12345678900", "Rua Dom Pedrito, 169", "99012-000")
cliente2 = Cliente("Maria de Lima", "98765432100", "Rua João de Césaro, 1052", "99036-118")

conta1 = ContaCorrente("001", cliente1, saldo=1000, limite=500)
conta2 = ContaPoupanca("002", cliente2, saldo=500, rendimento=0.02)

banco = Banco("Banco Python")
banco.criar_conta(conta1)
banco.criar_conta(conta2)

op1 = Transferencia(conta1, conta2, 200)
op1.executar()

op2 = Saque(conta1, 100)
op2.executar()

op3 = Deposito(conta2, 50)
op3.executar()

banco.listar_contas()
