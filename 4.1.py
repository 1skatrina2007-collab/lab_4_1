#### Вариант 19: Event-агентство
# - **Базовый класс 1:** `EventService` (цена)
# - **Дочерние классы 1:** `Catering` (меню), `VenueRental` (вместимость)
# - **Базовый класс 2:** `Client` (контакт)
# - **Дочерний класс 2:** `CorporateEventClient` (бюджет)
# - **Контейнер:** `EventPlan`
# - **Полиморфный метод (бизнес-логика):** `calculate_total_vat()` (разный НДС для услуг)

class EventService:
    """Базовый класс 1 для любой услуги event-агентства."""

    def __init__(self, name: str, price: float):
        """
        Конструктор.
        :param name: название услуги
        :param price: цена в рублях (без НДС)
        """
        self.name = name
        self.price = price

    def __str__(self) -> str:
        """Читаемый вывод информации о любой услуге."""
        return f"Услуга: {self.name} | Цена: {self.price:.2f} руб."

    def calculate_total_vat(self) -> float:
        """
        Рассчитать сумму НДС для услуги (базовый метод).
        По умолчанию НДС = 22% от цены.
        """
        return self.price * 0.22


class Catering(EventService):
    """Дочерний класс 1.1. Услуга организации питания с указанием меню."""

    def __init__(self, name: str, price: float, menu: str):
        super().__init__(name, price)
        self.menu = menu  # описание меню

    def __str__(self) -> str:
        """Читаемый вывод информации об услуге организации питания."""
        base = super().__str__()
        return f"{base} | Организация питания, меню: {self.menu}"

    def calculate_total_vat(self) -> float:
        """
        Для организации питания НДС = 10% (льготная ставка на продукты).
        """
        return self.price * 0.10


class VenueRental(EventService):
    """Дочерний класс 1.2. Услуга аренды площадки с указанием вместимости."""

    def __init__(self, name: str, price: float, capacity: int):
        super().__init__(name, price)
        self.capacity = capacity  # кол-во человек

    def __str__(self) -> str:
        """Читаемый вывод информации об услуге аренды."""
        base = super().__str__()
        return f"{base} | Аренда площадки, вместимость: {self.capacity} чел."

    def calculate_total_vat(self) -> float:
        """
        Для аренды НДС = 22% (стандартная ставка).
        """
        return super().calculate_total_vat() # вызов родительского метода


class Client:
    """Базовый класс 2 для клиента."""

    def __init__(self, name: str, contact: str):
        """
        :param name: имя или название клиента
        :param contact: контактные данные (телефон, email)
        """
        self.name = name
        self.contact = contact

    def __str__(self) -> str:
        """Читаемый вывод информации о клиенте."""
        return f"Клиент: {self.name} | Контакт: {self.contact}"


class CorporateEventClient(Client):
    """Дочерний класс 2.1. Клиент с фиксированным бюджетом."""

    def __init__(self, name: str, contact: str, budget: float):
        super().__init__(name, contact)
        self.budget = budget  # бюджет на мероприятие

    def __str__(self) -> str:
        """Читаемый вывод информации о клиенте с фиксированным бюджетом."""
        base = super().__str__()
        return f"{base} | Бюджет: {self.budget:.2f} руб."

    def is_budget_sufficient(self, total_cost: float) -> bool:
        """Проверяет, укладывается ли общая стоимость в бюджет."""
        if total_cost <= self.budget:
            return True
        return False


class EventPlan:
    """План мероприятия, содержащий клиента и список услуг."""

    def __init__(self, client: Client, services: list):
        self.client = client
        self.services = services  # список объектов EventService

    def __str__(self) -> str:
        return (f"План мероприятия для клиента {self.client.name}.\n"
                f"Услуг: {len(self.services)}.\n"
                f"Общая стоимость (без НДС): {self.calculate_total_price():.2f} руб.\n"
                f"Общий НДС: {self.calculate_total_vat():.2f} руб.\n"
                f"Итого с НДС: {self.calculate_total_price_with_vat():.2f} руб.")

    def calculate_total_price(self) -> float:
        return sum(service.price for service in self.services)

    def calculate_total_vat(self) -> float:
        return sum(service.calculate_total_vat() for service in self.services)

    def calculate_total_price_with_vat(self) -> float:
        return self.calculate_total_price() + self.calculate_total_vat()

    def check_budget(self) -> str:
        if isinstance(self.client, CorporateEventClient):
            sufficient = self.client.is_budget_sufficient(self.calculate_total_price_with_vat())
            return "Не превышает" if sufficient else "Превышает"
        else:
            return 'Бюджет не ограничен'


if __name__ == "__main__":
    # 1. Создание клиентов
    client1 = Client("Иванов Иван", "ivan@example.com")
    corporate_client1 = CorporateEventClient("ООО Ромашка", "+7(999)123-45-67", budget=500000)
    corporate_client2 = CorporateEventClient("Михаил Петров", "+7(989)167-55-60", budget=300000)

    # 2. Создание услуг
    catering1 = Catering("Фуршет", 120000, "Холодные закуски, напитки")
    catering2 = Catering("Банкет", 200000, "Горячее, десерты")
    venue = VenueRental("Конференц-зал 'Атриум'", 80000, capacity=150)

    # 3. Формирование планов мероприятий
    plan1 = EventPlan(client1, [catering1, venue])
    plan2 = EventPlan(corporate_client1, [catering1, catering2, venue])
    plan3 = EventPlan(corporate_client2, [catering2, venue])

    # 4. Вывод информации
    print("=" * 50)
    print(plan1)
    print("\nПревышает ли сумма размер бюджета:", plan1.check_budget())

    print("\n" + "=" * 50)
    print(plan2)
    print("\nПревышает ли сумма размер бюджета:", plan2.check_budget())

    print("\n" + "=" * 50)
    print(plan3)
    print("\nПревышает ли сумма размер бюджета:", plan3.check_budget())

    # 5. Демонстрация полиморфизма
    print("\n" + "=" * 50)
    print("Демонстрация полиморфизма (разный НДС):")
    for service in [catering1, venue]:
        print(f"{service.name}: НДС = {service.calculate_total_vat():.2f} руб. "
              f"(ставка: {service.calculate_total_vat() / service.price * 100:.0f}%)")

    # Объекты 1 класса
    print("\n" + "=" * 50)
    print(catering1, catering2, venue, sep='\n')

    # Объекты 2 класса
    print("\n" + "=" * 50)
    print(client1, corporate_client1, corporate_client2, sep='\n')