#!/bin/bash

python manage.py test -v 2 --noinput
let code=$?

echo -e "manage.py test Exit Code = ${code}"

if [ "$code" -eq "0" ]; then
  echo -e "\nSuccess: Все тесты успешно завершились"
else
  echo -e "\nFailure: Некоторые тесты завершились с ошибками!" >&2
fi
exit $code
