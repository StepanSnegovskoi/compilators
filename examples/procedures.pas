program Procedures;
var
  val: integer;

procedure AddOne(n: integer);
begin
  n := n + 1;
  WriteLn('Inside proc:', n);
end;

begin
  val := 10;
  AddOne(val);
  WriteLn('Outside proc:', val);
end.