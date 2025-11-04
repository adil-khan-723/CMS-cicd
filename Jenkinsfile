pipeline {
    agent any 

    triggers {
        githubPush()
    }
    environment {
        DIR = '/home/ubuntu/CMD-cicd'
        SERVER_IP = '13.232.164.183'
        FRONTEND = 'CMS_FRONTEND'
        BACKEND = 'CMS_BACKEND'
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
                    cd $pwd/CMS-cicd/frontend/cms-frontend
                    docker build -t ${FRONTEND} -f Dockerfile_mullti_stage .
                    echo 'Frontend build successful'
                """
            }
        }

        stage("backend build") {
            steps {
                sh """
                    cd ${DIR}/backend
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

    }
}