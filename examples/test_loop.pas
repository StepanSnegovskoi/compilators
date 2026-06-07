program TestLoop;
var
  i: integer;
begin
  WriteLn('Начинаем цикл:');

  for i := 1 to 5 do
  begin
    WriteLn('Итерация: ', i);
  end;

  WriteLn('Цикл завершен');
end.