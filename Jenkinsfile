pipeline {
    agent any 

    triggers {
        pollSCM('* * * * *')
    }
    environment {
        DIR = '/home/ubuntu/CMS-cicd'
        SERVER_IP = '13.232.164.183'
        FRONTEND = 'cms_frontend'
        BACKEND = 'cms_backend'
        DOCKERHUB = credentials('DockerHub')
    }
    stages {

        stage("code pull"){
            steps {
                echo "Getting the source code...."
                git branch: 'main', url: 'https://github.com/adil-khan-723/CMS-cicd.git'
                echo "Fetched...."
            }
        }

        stage("frontend build") {
            steps {
                sh """ 
                    cd /var/lib/jenkins/workspace/CMS/frontend/cms-frontend
                    docker build -t ${FRONTEND} -f Dockerfile_multi_stage .
                    echo 'Frontend build successful'
                """
            }
        }

        stage("backend build") {
            steps {
                sh """
                    cd /var/lib/jenkins/workspace/CMS/backend
                    docker build -t ${BACKEND} -f Dockerfile_cicd .
                    echo 'Backend build successful'
                """
            }
        }

        stage("push to registry") {
            steps {
                echo "Tagging both the images"
                sh "docker image tag ${BACKEND} ${DOCKERHUB_USR}/${BACKEND}"
                sh "docker image tag ${FRONTEND} ${DOCKERHUB_USR}/${FRONTEND}"
                echo "both images tagged... now logging in to docker hub ..."
                sh "docker login -u ${DOCKERHUB_USR} -p ${DOCKERHUB_PSW}"
                echo "logged in successfully... pushing the images..."
                sh "docker push ${DOCKERHUB_USR}/${BACKEND}"
                sh "docker push ${DOCKERHUB_USR}/${FRONTEND}"
                echo "images pushed ....."
            }
        }

        stage("deploy to ec2"){
            steps {
                sshagent(credentials: ['cms_deploy']){
                    sh """ssh -o StrictHostKeyChecking=no ubuntu@${SERVER_IP} '
                        if [ -d ${DIR} ]; then
                            echo 'pulling the changes'
                            cd ${DIR} 
                            git pull
                        else 
                            echo 'cloning the repo'
                            git clone https://github.com/adil-khan-723/CMS-cicd.git
                        fi 
                        docker system prune -af --volumes
                        cd ${DIR}
                        docker compose down
                        docker compose up --build
                        '
                    """
                }
            }
        }
    }

    post {
        success {
            echo "deploy success"
        }

        failure {
            echo "deploy failure"
        }
    }
}