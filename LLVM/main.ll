@.const0 = private constant [3 x i8] c"%d\00"
define i32 @main()
{
%str0 = getelementptr inbounds [3 x i8], [3 x i8]* @.const0, i32 0, i32 0
call i32 (i8*, ...) @printf(i8* %str0, i32 10)
ret i32 0
}
declare i32 @printf(i8*, ...) #1
