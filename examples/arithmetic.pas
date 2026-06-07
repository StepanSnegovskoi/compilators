program Arithmetic;
var
  a, b, res: integer;
begin
  a := 10;
  b := 20;
  res := (a + b) * 2 div 5;
  WriteLn('Result should be 12:', res);
end.