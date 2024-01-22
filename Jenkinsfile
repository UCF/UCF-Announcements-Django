pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('Initialize'){
            steps {
                scripts {
                    sh 'usermod -a -G docker jenkins'
                    def dockerHome = tool 'myDocker'
                    env.PATH = "${dockerHome}/bin:${env.PATH}"
                }
            }
            
        }
         
         stage('Clone repository') { 
            steps { 
                script{
                checkout scm
                }
            }
        }

        stage('Build') { 
            steps { 
                script{
                 app = docker.build("ucf-announcements")
                }
            }
        }
        stage('Test'){
            steps {
                 echo 'Empty'
            }
        }
        stage('Deploy') {
            steps {
                script{
                        docker.withRegistry('576133371502.dkr.ecr.us-east-2.amazonaws.com/ucf-announcements', 'ecr:us-east-2:aws-credentials') {
                    app.push("${env.BUILD_NUMBER}")
                    app.push("latest")
                    }
                }
            }
        }
    }
}