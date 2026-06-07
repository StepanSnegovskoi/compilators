program ErrorsTest;
var
  a, b: integer;
  flag: boolean;
  arr: array [1..5] of integer;

procedure CalcSum(x: integer; y: integer);
begin
  WriteLn('Сумма: ', x + y);
end;

begin
  c := 10;

  a := true;

  b := 5 + flag;

  PrintHello(123);

  CalcSum(10);
  CalcSum(1, 2, 3);

  a[1] := 5;

  arr[true] := 10;

  if a + b then
  begin
    WriteLn('Это не должно работать');
  end;
end.