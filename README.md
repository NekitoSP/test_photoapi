## Тестовое задание - Backend Developer
Есть пользователь, у которого есть фотографии с комментариями и датой загрузки. Необходимо разработать приложение, через которое посредством API пользователь смог бы управлять своими фотографиями. (id photo comment date)

У сущности Пользователь добавить параметр, который отвечает за возможность пользователя загружать изображения (выставлять из django- admin). Если флаг не стоит, то пользователь может только смотреть свои изображения.

**CRUD API работы с фотографиями:**
- Update - только текст комментария.
- Delete - когда юзер удаляет фотографию, не удалять ее физически, делать soft delete.
- Create - при загрузке новой фотографии необходимо ее модерировать, для упрощения берем hash(image.content) и если делится целочисленно на 2, то модерация пройдена, иначе говорим пользователю, что его фотография не может быть загружена.

**Требования:**
Django, DRF, пример под docker compose, тесты (все тесты можно не писать, но хорошо если будут комментарии, что бы хотел проверить)