from abc import ABC, abstractmethod

class IPaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class CreditCardPayment(IPaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        print("Processando pagamento com cartao...")
        print("Cartao validado!")
        return True

class PixPayment(IPaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        print("Gerando QR Code PIX...")
        print("PIX recebido!")
        return True

class BoletoPayment(IPaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        print("Gerando boleto...")
        print("Boleto gerado!")
        return True

class CryptoPaymentStrategy(IPaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        # Nova Extensao OCP: Taxa de 2% sobre o valor
        amount_with_fee = amount * 1.02
        print(f"Processando pagamento em Cripto com 2% de taxa. Valor total cobrado: R${amount_with_fee:.2f}...")
        print("Criptomoeda recebida e confirmada na blockchain!")
        return True
