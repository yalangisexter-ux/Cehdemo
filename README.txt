Android GitHub build support files

Included:
- .github/workflows/build.yml
- output/generated_project/gradle/wrapper/gradle-wrapper.properties (Gradle 8.2)

Not included:
- advanced_build.py (confidential / already in repository)
- requirements.txt (already in repository)
- gradle-wrapper.jar
- gradlew / gradlew.bat
- generated Android source files

The real gradlew and gradle-wrapper.jar must be supplied by the generator or obtained from an official Gradle 8.2 project.
