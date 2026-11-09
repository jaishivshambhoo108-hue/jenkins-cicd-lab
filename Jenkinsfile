
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        timeout(time: 30, unit: 'MINUTES')
    }

    environment {
        IMAGE = "demo-web:${BUILD_NUMBER}"
        DOCKER_NETWORK = "ci-net"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo 'GitHub source code downloaded successfully'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    echo "Building Docker image: $IMAGE"
                    docker build -t "$IMAGE" ./application
                '''
            }
        }

        stage('Application Testing') {
            steps {
                sh '''
                    echo "Testing Python application..."

                    docker run --rm "$IMAGE" \
                        python -m py_compile /app/app.py
                '''
            }
        }

        stage('Deploy DEV') {
            steps {
                sh '''
                    docker rm -f fake-dev-server || true

                    docker run -d \
                      --name fake-dev-server \
                      --network "$DOCKER_NETWORK" \
                      -e APP_ENV=DEV \
                      -p 8081:8000 \
                      "$IMAGE"

                    sleep 3

                    curl -fsS \
                      http://fake-dev-server:8000/health
                '''
            }
        }

        stage('Deploy TEST') {
            steps {
                sh '''
                    docker rm -f fake-test-server || true

                    docker run -d \
                      --name fake-test-server \
                      --network "$DOCKER_NETWORK" \
                      -e APP_ENV=TEST \
                      -p 8082:8000 \
                      "$IMAGE"

                    sleep 3

                    curl -fsS \
                      http://fake-test-server:8000/health
                '''
            }
        }

        stage('Deploy STAGING') {
            steps {
                sh '''
                    docker rm -f fake-staging-server || true

                    docker run -d \
                      --name fake-staging-server \
                      --network "$DOCKER_NETWORK" \
                      -e APP_ENV=STAGING \
                      -p 8083:8000 \
                      "$IMAGE"

                    sleep 3

                    curl -fsS \
                      http://fake-staging-server:8000/health
                '''
            }
        }

        stage('Production Approval') {
            steps {
                input message: 'Approve production deployment?',
                      ok: 'Deploy to Production'
            }
        }

        stage('Deploy PRODUCTION') {
            steps {
                sh '''
                    docker rm -f fake-prod-server || true

                    docker run -d \
                      --name fake-prod-server \
                      --network "$DOCKER_NETWORK" \
                      -e APP_ENV=PRODUCTION \
                      -p 8084:8000 \
                      "$IMAGE"

                    sleep 3

                    curl -fsS \
                      http://fake-prod-server:8000/health
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD PIPELINE COMPLETED SUCCESSFULLY!'
        }

        failure {
            echo 'CI/CD PIPELINE FAILED!'
        }

        always {
            echo 'Pipeline execution finished.'
        }
    }
}
