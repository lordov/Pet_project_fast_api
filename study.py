from fastapi.exceptions import RequestValidationError
import jwt
import random
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel, Field, field_validator, EmailStr

from typing import Annotated, Optional
from fastapi import (
    Depends, FastAPI, HTTPException,
    Header, Query, Request, File, Response,
    UploadFile, Cookie, Form, status
)
from fastapi.templating import Jinja2Templates
from fastapi.security import (
    HTTPBasic, HTTPBasicCredentials,
    OAuth2PasswordBearer, OAuth2PasswordRequestForm
)

from datetime import datetime

from src.exceptions.exceptions import CustomException

app = FastAPI(
    title="FastAPI project",
)


# Указываем директорию с шаблонами
templates = Jinja2Templates(directory="templates")


# КУРС ДОП ЗАДАНИЯ


@app.get('/')
async def html_answer(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

# Начальный

# @app.post('/calculate')
# async def calculate_sum(num1: int, num2: int):
#     result = num1 + num2
#     return {"result": result}


# @app.post("/files/")
# async def create_file(file: Annotated[bytes, File()]):
#     return {"file_size": len(file)}


# @app.post("/uploadfile/")
# async def create_upload_file(myfile: UploadFile):
#     data = await myfile.file.read()
#     return {"filename": myfile.filename,
#             "result": myfile.content_type}

# fake_items_db = [{"item_name": "Foo"}, {
#     "item_name": "Bar"}, {"item_name": "Baz"}]


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 1):
#     return fake_items_db[skip: skip + limit]

# Параметры пути плюс query. Реализация поиска товара

# sample_product_1 = {
#     "product_id": 123,
#     "name": "Smartphone",
#     "category": "Electronics",
#     "price": 599.99
# }

# sample_product_2 = {
#     "product_id": 456,
#     "name": "Phone Case",
#     "category": "Accessories",
#     "price": 19.99
# }

# sample_product_3 = {
#     "product_id": 789,
#     "name": "Iphone",
#     "category": "Electronics",
#     "price": 1299.99
# }

# sample_product_4 = {
#     "product_id": 101,
#     "name": "Headphones",
#     "category": "Accessories",
#     "price": 99.99
# }

# sample_product_5 = {
#     "product_id": 202,
#     "name": "Smartwatch",
#     "category": "Electronics",
#     "price": 299.99
# }

# sample_products = [sample_product_1, sample_product_2,
#                    sample_product_3, sample_product_4, sample_product_5]


# class ProductSchema(BaseModel):
#     product_id: int
#     name: str
#     category: str
#     price: float


# @app.get("/product/search", response_model=list[ProductSchema])
# def read_product_by_keyword(keyword: str, category: Optional[str] = None, limit: int = 10):
#     # Использование генератора списка для создания и фильтрации объектов Product
#     filtered_products = [
#         ProductSchema(**item) for item in sample_products
#         if keyword.lower() in item['name'].lower() and (category is None or item['category'] == category)
#     ][:limit]

#     if not filtered_products:
#         raise HTTPException(status_code=404, detail="Products not found")

#     return filtered_products


# def get_lst(keyword: str, category: str = None, limit: int = 10):
#     lst = []
#     for product in sample_products:
#         if keyword in product['name']:
#             lst.append(product)
#     if category:
#         for product in lst:
#             if product['category'] == category:
#                 lst.append(product)
#     return lst


# @app.get("/products/{product_id}")
# async def get_product(product_id: int):
#     return sample_products[product_id - 1]


# # Cookie Норм подход подойдет.

# @app.get("/date")
# def date(response: Response):
#     # получаем текущую дату и время
#     now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
#     response.set_cookie(key="last_visit", value=now)
#     return {"message": "куки установлены"}


# users = [
#     {'username': 'lol',
#      'password': '1234lol'}
# ]


# async def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
#     user = [user for user in users if user.get('username') ==
#             credentials.username and user.get('password') == credentials.password]
#     if user is None or user == []:
#         raise HTTPException(status_code=401, detail='Invalid credentials')
#     return user


# @app.post("/login")
# async def login(
#     username: Annotated[str, Form()],
#     password: Annotated[str, Form()],
# ):
#     check_user = [user for user in users if user.get('username') ==
#                   username and user.get('password') == password]

#     if check_user:
#         response = JSONResponse(content=({"result": 'OK'}))
#         token = str(random.randint(100, 999))
#         response.set_cookie(key='session_token',
#                             value=token, secure=True, httponly=True)
#         return response
#     else:
#         raise HTTPException(status_code=401, detail='user not found')


# @app.get("/user_cookie")
# def get_user(user: dict = Depends(authenticate_user), session_token: str | None = Cookie(default=None)):
#     if session_token is None:
#         return {"session_token": 'invalid_token_value'}

#     return user

# Заголовки


# @app.get("/items/")
# async def read_items(user_agent: Annotated[str | None, Header()] = None):
#     return {"User-Agent": user_agent}

# # Для отправки заголовка в конструктор класса Response


# @app.get("/send_header")
# def get_header():
#     data = "Hello from here"
#     return Response(content=data, media_type="text/plain", headers={"Secret-Code": "123459"})

# # Также можно задать заголовки с помощью атрибута headers


# @app.get("/set_header")
# def set_header(response: Response):
#     response.headers["Secret-Code"] = "123459"
#     return {"message": "Hello from my api"}


# @app.get("/headers")
# def headers(
#     requests: Request,
#     user_agent: Annotated[str | None, Header()] = None,
#     accept_language: Annotated[str | None, Header()] = None,
# ):
#     headers = requests.headers
#     headers_lang = requests.headers.get('accept-language')
#     if headers_lang != 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7':
#         raise HTTPException(status_code=400, detail='bad langugage code')

#     if not requests.headers:
#         raise HTTPException(status_code=400, detail='Headers not found')

#     return {"User-Agent": user_agent,
#             "Accept-Language": accept_language}

# Базовая аутентификация FastAPI

# security = HTTPBasic()
# class User(BaseModel):
#     username: str
#     password: str


# # добавим симуляцию базы данных в виде массива объектов юзеров
# USER_DATA = [User(**{"username": "user12", "password": "pass13"}),
#              User(**{"username": "user2", "password": "pass2"})]


# def get_user_from_db(username: str):
#     for user in USER_DATA:
#         if user.username == username:
#             return user
#     return None


# def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
#     user = get_user_from_db(credentials.username)
#     if user is None or user.password != credentials.password:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials",
#             headers={"WWW-Authenticate": "Basic"})
#     return user


# @app.get("/protected_resource/")
# def get_protected_resource(user: User = Depends(authenticate_user)):
#     response = JSONResponse("You got my secret, welcome")
#     response.headers["WWW-Authenticate"] = "Basic"
#     return response


# # Аутентификация на основе JWT

# SECRET_KEY = "mysecretkey"
# ALGORITHM = "HS256"

# USERS_DATA = [
#     {"username": "admin", "password": "adminpass"}
# ]

# def create_jwt_token(data: dict):
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# class User(BaseModel):
#     username: str
#     password: str


# # Продвинутая реализация  защиты
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# # Функция для создания JWT токена
# # кодируем токен, передавая в него наш словарь с тем, что мы хотим там разместить


# def get_user_from_token(token: str):
#     try:
#         payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         # тут мы идем в полезную нагрузку JWT-токена и возвращаем утверждение о юзере (subject);
#         # обычно там еще можно взять "iss" - issuer/эмитент,
#         # или "exp" - expiration time - время 'сгорания' и другое, что мы сами туда кладем
#         return payload.get('sub')

#     except jwt.ExpiredSignatureError:
#         pass  # истечение срока действия токена
#     except jwt.InvalidTokenError:
#         pass  # ошибка обработки декодирования токена


# def get_user(username: str):
#     for user in USERS_DATA:
#         if user.get('username') == username:
#             return user
#     return None


# @app.post("/login")
# async def login(user_in: User):
#     for user in USERS_DATA:
#         if user.get("username") == user_in.username and user.get("password") == user_in.password:
#             return {"access_token": create_jwt_token({"sub": user_in.username}), "token_type": "bearer"}
#     return {"error": "Invalid credentials"}


# # защищенный роут для получения информации о пользователе
# @app.get("/about_me")
# async def about_me(current_user: str = Depends(get_user_from_token)):
#     user = get_user(current_user)
#     if user:
#         return user
#     return {"error": "User not found"}


# # RBAC пример

# # Секретный ключ для подписи и верификации токенов JWT
# # тут мы в реальной практике используем что-нибудь вроде команды Bash (Linux) 'openssl rand -hex 32', и храним очень защищенно
# SECRET_KEY = "mysecretkey"
# ALGORITHM = "HS256"  # плюс в реальной жизни мы устанавливаем "время жизни" токена

# # Пример информации из БД
# USERS_DATA = {
#     "admin": {"username": "admin", "password": "adminpass", "role": "admin"},
#     "user": {"username": "user", "password": "userpass", "role": "user"},
# }  # в реальной БД мы храним только ХЭШИ паролей (можете прочитать про библиотеку, к примеру, 'passlib') + соль (известная только нам добавка к паролю)

# # OAuth2PasswordBearer для авторизации по токену
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# # Модель User для аутентификации (если делали задание по JWT, то тут добавляем только роль)
# class User(BaseModel):
#     username: str
#     password: str
#     role: Optional[str] = None


# # Функция для создания JWT токена
# def create_jwt_token(data: dict):
#     return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# # Функция получения User'а по токену - это скорее всего была самая сложная часть в предыдущем задании
# def get_user_from_token(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[
#                              ALGORITHM])  # декодируем токен
#         # тут мы идем в полезную нагрузку JWT-токена и возвращаем утверждение о юзере (subject); обычно там еще можно взять "iss" - issuer/эмитент, или "exp" - expiration time - время 'сгорания' и другое, что мы сами туда кладем
#         return payload.get("sub")
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token has expired",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     except jwt.InvalidTokenError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )


# # Функция для получения пользовательских данных на основе имени пользователя
# def get_user(username: str):
#     if username in USERS_DATA:
#         user_data = USERS_DATA[username]
#         return User(**user_data)
#     return None


# # Роут для получения JWT-токена (так работает логин)
# @app.post("/token/")
# # тут логинимся через форму
# def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user_data_from_db = get_user(user_data.username)
#     if user_data_from_db is None or user_data.password != user_data_from_db.password:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     # тут мы добавляем полезную нагрузку в токен, и говорим, что "sub" содержит значение username
#     return {"access_token": create_jwt_token({"sub": user_data.username})}


# # Защищенный роут для админов, когда токен уже получен
# @app.get("/admin/")
# def get_admin_info(current_user: str = Depends(get_user_from_token)):
#     user_data = get_user(current_user)
#     if user_data.role != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
#     return {"message": "Welcome Admin!"}


# # Защищенный роут для обычных пользователей, когда токен уже получен
# @app.get("/user/")
# def get_user_info(current_user: str = Depends(get_user_from_token)):
#     user_data = get_user(current_user)
#     if user_data.role != "user":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
#     return {"message": "Hello User!"}


# # Custom Excecptions

# class ItemsResponse(BaseModel):
#     item_id: int


# class CustomExceptionModel(BaseModel):
#     status_code: int
#     er_message: str
#     er_details: str


# @app.get(
#     "/items/{item_id}/",
#     response_model=ItemsResponse,
#     status_code=status.HTTP_200_OK,
#     summary="Get Items by ID.",
#     description="The endpoint returns item_id by ID. If the item_id is 42, an exception with the status code 404 is returned.",
#     responses={
#         status.HTTP_200_OK: {'model': ItemsResponse},
#         # вот тут применяем схемы ошибок пидантика
#         status.HTTP_404_NOT_FOUND: {'model': CustomExceptionModel},
#     },
# )
# async def read_item(item_id: int):
#     if item_id == 42:
#         raise CustomException(detail="Item not found", status_code=404,
#                               message="You're trying to get an item that doesn't exist. Try entering a different item_id.")
#     return ItemsResponse(item_id=item_id)

# Validation exceptions через декораторы


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# @app.exception_handler(ValueError)  # кастомный хэндлер для ValueError
# async def value_error_handler(request, exc):
#     return JSONResponse(status_code=400, content={"error": str(exc)})


# @app.post("/items/")
# async def create_item(item: Item):
#     try:
#         if item.price < 0:
#             raise ValueError("Price must be non-negative")

#         # вернём при успехе
#         return {"message": "Item created successfully", "item": item}
#     except ValueError as ve:
#         # выбрасываем ValueError чтобы сработал кастомный обработчик нашего исключения
#         raise ve

# Другой подход
# # кастомный обработчик исключения для всех HTTPException
# async def custom_http_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"error": str(exc)},
#     )

# # кастомный обработчик исключения для RequestValidationError (Pydantic validation errors - 422 Unprocessable Entity)


# async def custom_request_validation_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=422,
#         content={"message": "Custom Request Validation Error",
#                  "errors": exc.errors()},
#     )

# # тут показываем альтернативный декораторам способ регистрации хэндлеров
# app.add_exception_handler(HTTPException, custom_http_exception_handler)
# app.add_exception_handler(RequestValidationError,
#                           custom_request_validation_exception_handler)


# class Item(BaseModel):
#     name: str
#     price: float


# @app.post("/items/")
# async def create_item(item: Item, res):
#     if item.price < 0:
#         raise HTTPException(
#             status_code=400, detail="Price must be non-negative")
#     return {"message": "Item created successfully", "item": item}

# # собственные валидаторы Pydantic
# # https://pydantic-docs.helpmanual.io/usage/validators/

# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None

#     @field_validator("price")
#     @classmethod
#     def validate_price(cls, value):
#         if value < 0:
#             raise ValueError("Price must be non-negative")
#         return value


# @app.post("/items/")
# async def create_item(item: Item):
#     return {"message": "Item created successfully", "item": item}

# # Проверка с использованием параметров запроса, параметров пути и параметров заголовков
# @app.get("/items/")
# # валидируем тут и задаём значение по-умолчанию
# async def read_items(q: str | None = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# @app.get("/items/{item_id}")
# async def read_item(item_id: int):  # задаём тип тут
#     return {"item_id": item_id}


# @app.get("/items/")
# async def read_items(user_agent: Annotated[str | None, Header()] = None): # задаём тип тут
#     return {"User-Agent": user_agent}


# @app.get("/items/")
# async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# Задача на проверку данных запроса и пользовательскую обработку ошибок

@app.exception_handler(RequestValidationError)
async def value_error_handler(request, exc):
    errors = []
    for error in exc.errors():
        field = error["loc"][-1]
        msg = error["msg"]
        errors.append({"field": field, "msg": msg, "your_input": error["input"]})
    print(errors)
    return JSONResponse(status_code=422, content=errors)


class User(BaseModel):
    username: str
    age: int = Field(gt=18)
    email: EmailStr
    password: str = Field(min_length=16, max_length=64)
    phone: str | None = 'Unkonwn'

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value < 18:
            raise ValueError("Age must be greater than 18")
        elif value > 100:
            raise ValueError("You are too old")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 16:
            raise ValueError("Password must be greater than 16")
        return value


@app.post("/users/")
async def create_user(user: User):
    return {"message": "User created successfully", "user": user}

if __name__ == "__main__":

    uvicorn.run(app="test:app", reload=True)
