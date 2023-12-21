# Игровой проект «Хищник — жертва»
  ## Описание
  Создание и демонстрация сложной экосистемы, для которой реализованы долговременные отношения между видами хищника и жертвы.
  - Игровой проект. Модель эмпирическая, все параметры задаются перед началом симуляции. Некоторые параметры можно изменять вручную в реальном времени (пункт ниже).
  - Есть возможность изменения некоторых параметров в системе вручную в реальном времени, таких как: 
  скорость старения (другими словами, шаг старения); количество еды в системе; шанс размножения всех клеток; шаг сытости (или другими словами, скорость голодания).
  - Также есть графики и фазовые диаграммы строящиеся в реальном времени, и есть возможность выбирать какой график показывать, а именно: график размера популяции от времени; график возраста популяции от времени; график средней подвижности от времени; график средней сытости от времени.
  - В системе в том числе есть такие параметры, как: 
  сытость и возраст клеток, их способность к размножению, количество хищников и жертв, количество еды для жертв, шаг сытости и шаг возраста (сколько сытости убавляется за итерацию и на сколько стареет клетка за итерацию).
  - Есть жертвы, которые могут двигаться, размножаться, есть пищу, стареть. 
  - Есть хищники, которые могут двигаться, есть жертв и размножаться, стареть.
  - Хищник, съедая жертву имеет шанс размножиться, как и жертва при поедании еды.
  ## Библиотеки
   Модель описывается в 2D с помощью библиотек Pygame, random, numpy, os.
