pipeline {
    agent any

    environment {
        // Set the path for your build results folder.
        // In this example, we assume that your repository (or your test execution)
        // produces a folder named test_results_10-33-53-06-02-2025 in the workspace.
        BUILD_RESULTS_PATH = "${WORKSPACE}/test_results_10-33-53-06-02-2025"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout your repository containing the jsonconverter.py and sample test results folder.
                checkout scm
            }
        }
        stage('Run Tests / Prepare Artifacts') {
            steps {
                // If your tests automatically generate the build folder, run them here.
                // For demonstration, we assume the folder already exists in the workspace.
                echo "Assuming test results are available in ${env.BUILD_RESULTS_PATH}"
            }
        }
        stage('Generate Summary JSON') {
            steps {
                // Run the conversion script passing the build folder path.
                sh "python3 jsonconverter.py ${env.BUILD_RESULTS_PATH}"
            }
        }
        stage('Archive Artifact') {
            steps {
                // Archive jsonfile.json so you can review it from the Jenkins build artifacts.
                archiveArtifacts artifacts: 'jsonfile.json', fingerprint: true
            }
        }
    }

    post {
        always {
            echo "Build finished. The summary JSON has been created and archived."
        }
    }
}
