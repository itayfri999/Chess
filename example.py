

class Factory:
    def make_product(self) -> dict:
        raise NotImplementedError()

    def say_hi(self):
        print("hi")

class FactoryDistrict:
    def __init__(self, factories: list[Factory]):
        self.factories = factories

    def make_products(self) -> dict:
        for factory in self.factories:
            factory.make_product()

class PlasticFactory(Factory):
    def make_product(self) -> dict:
        print("Making Plastic")
        return {"type":"plastic", "color": "blue"}

class KeyboardFactory(Factory):
    def make_product(self) -> dict:
        print("Making Keyboard")
        return {"type":"keyboard", "color": "rgb"}



fd = FactoryDistrict([PlasticFactory(), KeyboardFactory()])
fd.make_products()

keyboard = KeyboardFactory()
keyboard.say_hi()