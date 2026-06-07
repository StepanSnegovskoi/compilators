program InputExample;
var
  age, birthYear: integer;
  arr: array [1..3] of integer;
begin
  WriteLn('Расчета года рождения');
  Write('Введите ваш возраст: ');
  ReadLn(age);

  birthYear := 2024 - age;
  WriteLn('Вы родились примерно в ', birthYear, ' году.');

  WriteLn('Ввода в массив');
  Write('Введите число для arr[2]: ');
  ReadLn(arr[2]);

  arr[2] := arr[2] * 10;
  WriteLn('Значение в массиве умноженное на 10: ', arr[2]);
end.