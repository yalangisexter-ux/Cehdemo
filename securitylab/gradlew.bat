@if "%DEBUG%" == "" @echo off
set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%
set CLASSPATH=%APP_HOME%\gradle\wrapper\gradle-wrapper.jar
java -version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    java -cp "%CLASSPATH%" org.gradle.wrapper.GradleWrapperMain %*
) else (
    echo ERROR: Java is not installed or not in your PATH.
    exit /b 1
)
