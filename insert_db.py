from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import DataBase, Bouquets, Papers, Tapes, Users, Orders
import base64
with open("static/img/пионы2.jpg", "rb") as img_file:
    encoded_image = base64.b64encode(img_file.read()).decode('utf-8')
with open("static/img/розы.jpg", "rb") as img_file:
    encoded_image2 = base64.b64encode(img_file.read()).decode('utf-8')
with open("static/img/тюльпаны.jpg", "rb") as img_file:
    encoded_image3 = base64.b64encode(img_file.read()).decode('utf-8')
with open("static/img/крафт.jpg", "rb") as img_file:
    encoded_image4 = base64.b64encode(img_file.read()).decode('utf-8')
with open("static/img/папиросная.jpg", "rb") as img_file:
    encoded_image5 = base64.b64encode(img_file.read()).decode('utf-8')
with open("static/img/коробки.jpg", "rb") as img_file:
    encoded_image6 = base64.b64encode(img_file.read()).decode('utf-8')
with open("static/img/бежевая.jpg", "rb") as img_file:
    encoded_image7 = base64.b64encode(img_file.read()).decode('utf-8')
with open("static/img/зеленая.jpg", "rb") as img_file:
    encoded_image8 = base64.b64encode(img_file.read()).decode('utf-8')
with open("static/img/красная.jpg", "rb") as img_file:
    encoded_image9 = base64.b64encode(img_file.read()).decode('utf-8')

engine = create_engine('sqlite:///bloom.db') 
DataBase.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

bouquete_one = Bouquets(bouquet_name="Королевские пионы", 
                bouquet_cost = 5000,
                bouquet_desc="Пионы сорта коралл шарм обладают очень быстрым и красивым раскрытием в обычную погоду и имеют уникальное свойство через некоторое время менять цвет бутона с кораллового на нежно лососевый. В букете 11 шт.",
                height = 50,
                width = 15,
                bouquet_image = encoded_image)

bouquete_two = Bouquets(bouquet_name="Красная королева", 
                bouquet_cost = 3000,
                bouquet_desc="Очаровательный букет из ароматных роз с крупным бутоном. Данный букет не оставит никого равнодушным, а размер бутона приятно удивит. В букете 11 шт.",
                height = 50,
                width = 15,
                bouquet_image =encoded_image2)

bouquete_three = Bouquets(bouquet_name="Лето в Голландии", 
                bouquet_cost = 4000,
                bouquet_desc="Шикарный монобукет из белоснежных голландских тюльпанов станет прекрасным подарком для коллеги, мамы, девушки, подруги, на день рождения. В букете 25 шт.",
                height = 45,
                width = 30,
                bouquet_image = encoded_image3)



paper_one = Papers(paper_name = "Крафт-бумага",
    paper_desc = "Это высокопрочная бумага преимущественно бурого, коричневого или серого цвета. Это стильное решение добавит вашему букеты скромный и минималистичный вид.",
    paper_cost = 100,
    paper_image = encoded_image4)

paper_two = Papers(paper_name = "Папиросная бумага",
    paper_desc = "Это бумага может быть самых разных цветов. Она с легкостью сделает ваш букет ярким и необычным.",
    paper_cost = 300,
    paper_image = encoded_image5)

paper_three = Papers(paper_name = "Коробка",
    paper_desc = "Цветочная коробка - отличное решение для вашего букета, если не будет возможности поместить цветы в вазу.",
    paper_cost = 500,
    paper_image = encoded_image6)

tape_one = Tapes(tape_name = "Бежевая лента",
    tape_desc = "Бежевая лента прекрасно дополнит букет любой сложности.",
    tape_cost = 150,
    tape_image = encoded_image7)

tape_two = Tapes(tape_name = "Зеленая лента",
    tape_desc = "Зеленая лента подойдет любителям натуральных оттенков.",
    tape_cost = 150,
    tape_image = encoded_image8)

tape_three = Tapes(tape_name = "Красная лента",
    tape_desc = "Красная лента послужит отличным акцентом в вашем букете.",
    tape_cost = 150,
    tape_image = encoded_image9)

session.add(bouquete_one)
session.add(bouquete_two)
session.add(bouquete_three)

session.add(paper_one)
session.add(paper_two)
session.add(paper_three)

session.add(tape_one)
session.add(tape_two)
session.add(tape_three)

session.commit()