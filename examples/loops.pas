program Loops;
var
  i, x: integer;
begin
  x := 0;
  for i := 1 to 5 do
  begin
    Inc(x);
  end;
  WriteLn('For loop result (5):', x);

  do
  begin
    Dec(x);
  end while x > 0;
  WriteLn('Do-while result (0):', x);
end.