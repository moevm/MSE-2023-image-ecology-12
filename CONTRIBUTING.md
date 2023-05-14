# Правила работы

## Git-Flow:
  - У нас есть 3 ветки: main, dev, test
  - Каждая feature в отдельной ветке, которая создаётся из dev
  - При старте работ над feature делаетс 2 PR: dev и test, а задача переводится в *in progress*
  - После завершения разработки, задача переходит в статус *in review*
  - Ревью осуществляется в ветке test, исправления заливатся в feature-ветку, после ревью ветка мёржится в test и задача переходит в статус *done*
  - При релизе запланированных фич, они поочерёдно мёржатся в dev со squash коммитов
  - После того, как все нужные фичи попали в dev, делается релизная ветка в которую коммитится up версии и делается 2 PR: dev и master
  - После того, как PR будет влит в мастер на него ставится тег с версией

### Версионирование
Каждую доставку вашего ПО маркируйте следующей схемой: A.B.C, где A — это глобальные изменения, ломающие обратную совместимость; B — доставка новых функций (работоспособность прошлых версий, соответственно, сохраняется); C — мелкие правки, патчи и горячие фиксы


### Создание feature-ветки
  - На доске проекта создаётся item в статусе *draft*
  - Далее он преобразуется в issue
  
![image](https://user-images.githubusercontent.com/29037445/221422439-d4e9d890-f8b1-4b18-95f9-eaeb7581ca58.png)
  - Заходим  issue в вашем репозитории
![image](https://user-images.githubusercontent.com/29037445/221422634-49e1cf91-b856-444d-813f-ca69838740c1.png)
  - Справа, в меню блок - Development Выбираете "Create branch"
#### ВАЖНО по gitflow ветки вы создаёте из dev
![image](https://user-images.githubusercontent.com/29037445/221422780-3e6d05ee-cbf4-427b-ae7e-a0f670d9bf4a.png)