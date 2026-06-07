program ArrayTest;
var
  arr: array [1..3] of integer;
begin
  arr[1] := 100;
  arr[2] := arr[1] + 50;
  WriteLn('Array values:', arr[1], arr[2]);
end.