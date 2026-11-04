# python oop

class Calculator:
    def __init__(self,brand) -> None:
        self.brand = brand
        self._precision = "High"

    def add(self,a,b):
        c = a + b
        return c

    def get_precision(self):
        return self._precision

class Advanced_Calculator(Calculator):
    def power(self,base,exponent):
        return base ** exponent

    def add(self,a,b):
        print("Performing the advanced addition")
        return float(a+b)




basic_calc = Calculator("Casio")
print(f"The Brand of the calculator is the {basic_calc.brand}")
print(f"The precision of the calculator is {basic_calc.get_precision()}")
print(f"The Addition from the calculator for the 3 and 5 is {basic_calc.add(3,6)}")

adv_calc = Advanced_Calculator("Ham")
print(f"The inherited brand of the calculator is {adv_calc.brand}")
print(f"The precision of the inherited brand is {adv_calc._precision}")
print(f"The Addition calculation through this inherited calculator for the 3 and 5 is{adv_calc.add(3,5)}")
print(f"The power of the 2 with 3 is {adv_calc.power(2,3)}")



