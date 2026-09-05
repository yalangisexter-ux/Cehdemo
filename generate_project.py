#!/usr/bin/env python3
import os
import zipfile

base_dir = "android-ceh-lab"

files = {
    "settings.gradle.kts": """pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "android-ceh-lab"
include(":attacker", ":defender", ":rootaudit")""",
    "build.gradle.kts": """plugins {
    id(\"com.android.application\") version \"8.2.0\" apply false
    id(\"org.jetbrains.kotlin.android\") version \"1.9.0\" apply false
}"""
}

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, \"w\", encoding=\"utf-8\") as f:
        f.write(content)

with zipfile.ZipFile(\"android-ceh-lab.zip\", \"w\", zipfile.ZIP_DEFLATED) as zipf:
    for root, _, filenames in os.walk(base_dir):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            zipf.write(file_path, os.path.relpath(file_path, start=os.path.dirname(base_dir)))

print(\"android-ceh-lab.zip generated successfully.\")