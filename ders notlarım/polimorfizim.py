## Çok Biçimlilik

class HavaDurumu:
    def __init__(self, sehir, derece):
        self.sehir = sehir
        self.derece = derece
    def durum_goster(self):
        return f"{self.sehir} şehrinde sıcaklık {self.derece}°C"
class Gunesli(HavaDurumu):
    def __init__(self, sehir, derece):
        super().__init__(sehir, derece)
    def durum_goster(self):
        return super().durum_goster() + " ve hava güneşli."
class Yagmurlu(HavaDurumu):
    def __init__(self, sehir, derece):
        super().__init__(sehir, derece)
    def durum_goster(self):
        return super().durum_goster() + " ve hava yağmurlu."

hava1 = Gunesli("Antalya", 30)
hava2 = Yagmurlu("Isparta", 15)
print(hava1.durum_goster())
print(hava2.durum_goster())
