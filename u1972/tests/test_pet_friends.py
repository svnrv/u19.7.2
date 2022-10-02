from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, empty_email, empty_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в
    тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key.
    Далее используя этого ключ запрашиваем список всех питомцев и проверяем
    что список не пустой. Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='котэ', animal_type='кот',
                                     age='44', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name, result['animal_type'] == animal_type and result['age'] == age


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets. Питомцы отсутствуют")


# # # ***************** Ещё 10 вариантов тест-кейсов для данного REST API интерфейса *******************
# # # *****************

# 1
def test_add_new_pet_with_long_name(name='ааааааа ббббббббббббб ввввввввввввв ггггггггггг дддддддддддд еееееееееее жжжжжжжжжжжжжжжжжж',
                                    animal_type='сфинкс',
                                    age='1', pet_photo='images/cat1.jpg'):
    """Проверяем, что нельзя добавить питомца с именем длиннее 50 символов"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print('Баг - сайт позволяет добавить питомца с именем длиннее 50 символов')

# 2
def test_add_new_pet_with_empty_name(name='', animal_type='кот', age='44', pet_photo='images/cat1.jpg'):
    '''Проверяем возможность добавления питомца с пустым значением name
       Питомец будет добавлен на сайт с пустым значением в поле "имя"'''

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == '', 'Питомец добавлен на сайт с пустым значением в имени'


# 3
def test_add_new_pet_without_photo_with_valid_data(name='Tom', animal_type='catou', age='5'):
    """Проверяем, что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pets_no_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''

# 4
def test_add_pet_new_photo(pet_photo='images/cat11.jpg'):
    """Проверяем что можно добавить/изменить фото питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Добавляем(если без фото)/изменяем фото питомца
    status, result = pf.update_pet_set_photo(auth_key, my_pets['pets'][4]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] != ''


# 5
def test_update_self_pet_info_passed(name='Кекс', animal_type='Котэ', age=5):
    """Тест на возможность обновления информации о питомце"""

    # Получение ключа auth_key и списка своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то обновляем имя, тип и возраст первого в списке питомца (последнего добавленного)
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][1]['id'], name, animal_type, age)

        # Проверка, что статус ответа = 200, и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # Если спиок питомцев пуст, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Список питомцев пуст")

# 6
def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    '''Проверяем что запрос api ключа с валидным имейлом и с невалидным паролем.
    Проверяем нет ли ключа в ответе'''

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status,
    # а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result

# 7
def test_get_api_key_with_wrong_email_and_correct_password(email=invalid_email, password=valid_password):
    '''Проверяем что запрос api ключа с невалидным имейлом и валидным паролем.
    Проверяем нет ли ключа в ответе'''

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status,
    # а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 8
def test_get_api_key_for_empty_email_user(email = empty_email, password = empty_password):
    '''Проверяем что запрос api ключа с пустым имейлом и с пустым паролем.
    Проверяем нет ли ключа в ответе'''

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status,
    # а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


# 9
def test_add_new_pet_with_wrong_age(name='котэнекотэ', animal_type='кот',
                                     age='-9', pet_photo='images/cat11.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с отрицательным числом в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле возраст.
     '''
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert age in result['age']
    assert int(result['age']) > 0  #'Питомец добавлен на сайт с отрицательным числом в поле возраст'


# 10
def test_delete_all_my_pets():
    """Проверяем возможность удаления всех питомцев"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # создаем цикл, в котором прописываем условия, если количество питомцев больше, чем 0,
    # то удаляем питомца под №0, до тех пор, пока количество будет равно нулю
    while len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        status, _ = pf.delete_pet(auth_key, pet_id)
        if len(my_pets['pets']) == 0:
            break
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()






