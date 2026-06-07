program Logic;
var
  flag: boolean;
begin
  flag := (10 > 5) and (not false);
  if flag then
    WriteLn('Logic is correct');
end.