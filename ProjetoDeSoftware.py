from datetime import datetime

class Cliente:
    def __init__(self, nome, cpf, endereco, telefone):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        self.telefone = telefone

    def get_info(self):
        return f"Nome: {self.nome}, CPF: {self.cpf}"
    
class Conta:
    def __init__(self, numero, cliente, tipo, saldo):
        self.numero = numero
        self.cliente = cliente
        self.tipo = tipo
        self.saldo = saldo

    def depositar(self, valor):
        self.saldo += valor
        print(f"Depósito de R${valor:.2f} realizado. Saldo atual: R${self.saldo:.2f}")

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            print(f"Saque de R${valor:.2f} realizado. Saldo atual: R${self.saldo:.2f}")
        else:
            print("Saldo insuficiente para saque.")

    def transferir(self, valor, outra_conta):
        if valor <= self.saldo:
            self.sacar(valor)
            outra_conta.depositar(valor)
            print(f"Transferência de R${valor:.2f} para {outra_conta.cliente.nome} realizada com sucesso!")
        else:
            print("Saldo insuficiente para transferência.")

    def get_saldo(self):
        return self.saldo

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, saldo=0.0, limite=0.0):
        super().__init__(numero, cliente, "Corrente", saldo)
        self.limite = limite

class ContaPoupanca(Conta):
    def __init__(self, numero, cliente, saldo=0.0, rendimento=0.0):
        super().__init__(numero, cliente, "Poupança", saldo)
        self.rendimento = rendimento

class Transacao:
    def __init__(self, id_transacao, valor, tipo):
        self.id = id_transacao
        self.data = datetime.now()
        self.valor = valor
        self.tipo = tipo

    def registrar(self):
        print(f"Transação {self.id} registrada em {self.data} - Tipo: {self.tipo}. Valor: R${self.valor:.2f}")

class Operacao:
    def __init__(self, tipo, conta_origem, conta_destino=None, valor=0.0):
        self.tipo = tipo
        self.conta_origem = conta_origem
        self.conta_destino = conta_destino
        self.valor = valor

    def executar(self):
        if self.tipo == "Transferencia" and self.conta_destino is not None:
            self.conta_origem.transferir(self.valor, self.conta_destino)
        elif self.tipo == "Deposito":
            self.conta_origem.depositar(self.valor)
        elif self.tipo == "Saque":
            self.conta_origem.sacar(self.valor)
        else:
            print("Tipo de operação inválido.")

class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.contas = []
    
    def criar_conta(self, conta):
        self.contas.append(conta)
        print(f"Conta {conta.numero} criada com sucesso para {conta.cliente.nome}")
    
    def fechar_conta(self, numero):
        self.contas = [conta for conta in self.contas if conta.numero != numero]
        print(f"Conta {numero} fechada com sucesso.")
    
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

conta1.transferir(200, conta2)
conta1.sacar(100)
conta2.depositar(50)

banco.listar_contas()
