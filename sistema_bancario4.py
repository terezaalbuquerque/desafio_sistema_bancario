from datetime import datetime
from functools import wraps


def log_transacao(tipo):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resultado = func(*args, **kwargs)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Transação realizada: {tipo}")
            return resultado
        return wrapper
    return decorador

class Conta:
    def __init__(self, numero):
        self.numero = numero
        self.saldo = 0
        self.transacoes = []

    @log_transacao("Criação de Conta")
    def criar_conta(self):
        self.transacoes.append(("criação", 0, datetime.now()))

    @log_transacao("Depósito")
    def depositar(self, valor):
        self.saldo += valor
        self.transacoes.append(("depósito", valor, datetime.now()))

    @log_transacao("Saque")
    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            self.transacoes.append(("saque", valor, datetime.now()))
        else:
            print("Saldo insuficiente")

    # Gerador com filtro por tipo de transação
    def gerar_transacoes(self, tipo=None):
        for transacao in self.transacoes:
            if tipo is None or transacao[0] == tipo:
                yield transacao

class Banco:
    def __init__(self):
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __iter__(self):
        return ContaIterador(self.contas)

class ContaIterador:
    def __init__(self, contas):
        self._contas = contas
        self._indice = 0

    def __next__(self):
        if self._indice >= len(self._contas):
            raise StopIteration
        conta = self._contas[self._indice]
        self._indice += 1
        return f"Conta: {conta.numero}, Saldo: R$ {conta.saldo:.2f}"

    def __iter__(self):
        return self

if __name__ == "__main__":
    # Criando contas
    conta1 = Conta(101)
    conta1.criar_conta()
    conta1.depositar(1000)
    conta1.sacar(300)

    conta2 = Conta(102)
    conta2.criar_conta()
    conta2.depositar(500)
    conta2.sacar(100)

    # Criando banco e adicionando contas
    banco = Banco()
    banco.adicionar_conta(conta1)
    banco.adicionar_conta(conta2)

    # Iterando sobre contas com o iterador personalizado
    print("\n📋 Contas no banco:")
    for info in banco:
        print(info)

    # Gerando transações filtradas
    print("\n💰 Transações de depósito da Conta 101:")
    for t in conta1.gerar_transacoes("depósito"):
        tipo, valor, data = t
        print(f"Tipo: {tipo} | Valor: R$ {valor:.2f} | Data: {data.strftime('%Y-%m-%d %H:%M:%S')}")
