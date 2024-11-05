# 如果无法下载gradlew，参照以下步骤


    cd to --> /home/your_user/.gradle/wrapper/dists
    download appropriate gradle from this link - https://services.gradle.org/distributions/
    Remove all directories below ~/.gradle/wrapper/dists
    Move the downloaded zip file from step 2 to this directory
    unzip the gradle file in the current directory
    Rerun the command --> buildozer andriod clean debug
