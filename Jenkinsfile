pipeline {
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --oneline'
            }
        }

        stage('Preparar configuracion') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'postgres-creds',
                                                  usernameVariable: 'PG_USER',
                                                  passwordVariable: 'PG_PASS')]) {
                    sh '''
                        printf "POSTGRES_DB=notasdb\\nPOSTGRES_USER=%s\\nPOSTGRES_PASSWORD=%s\\nDB_HOST=db\\n" "$PG_USER" "$PG_PASS" > .env
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                sh 'docker compose pull db'
                sh 'docker compose build'
                sh 'docker compose images'
            }
        }

        stage('Test') {
            steps {
                sh 'docker compose up -d --wait'
                sh 'docker compose ps'
                sh 'docker exec -i notas_app python - < tests/test_integration.py'
            }
        }
    }

    post {
        always {
            sh 'docker compose logs --no-color || true'
            sh 'docker compose down -v || true'
            sh 'rm -f .env'
        }
        success {
            echo 'Pipeline exitoso: imagenes construidas y contenedores comunicados.'
        }
        failure {
            echo 'Pipeline fallido: revisar la salida de consola.'
        }
    }
}