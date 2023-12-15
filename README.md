# Проект «Predator-victim»
## Описание
- Используем такие параметры системы как: 
сытость, возраст, способность к размножению, количество хищников и жертв, количество еды для жертв, шаг сытости и шаг возраста (сколько сытости убавляется за итерацию и на сколько стареет клетка за итерацию).
- Есть жертвы, которые могут двигаться, размножаться, есть пищу, стареть. 
- Есть хищники, которые могут двигаться, есть жертв и размножаться, стареть.
- Хищник съедая жертву имеет шанс размножиться, как и жертва при поедании еды.
- Модель эмпирическая, математические формулы использоваться не будут. Например, способность к размножению зависит от параметры системы и характеристик самой клетки. Все параметры задаются перед началом симуляции. Некоторые параметры можно изменять в ручную в реальном времени (пункт ниже).
- Есть возможность изменения некоторых параметров в системе в ручную в реальном времени, таких как: 
скорость старения (другими словами, шаг старения); количество еды в системе; шанс размножения всех клеток; шаг сытости (или другими словами, скорость голодания).
- Модель описывается в 2D с помощью Pygame.
