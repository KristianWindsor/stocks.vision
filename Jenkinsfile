node {
    def backend
    def crawler
    def crawlscheduler
    def mysql
    def webui

    def buildname = 'b' + env.BUILD_NUMBER

    stage('Get Code') {
        checkout scm
    }

    stage('Build Backend') {
        backend = docker.build("kristianwindsor/stocksvision-backend", "./backend/")
    }

    stage('Build Crawler') {
        crawler = docker.build("kristianwindsor/stocksvision-crawler", "./crawler/")
    }

    stage('Build Crawlscheduler') {
        crawlscheduler = docker.build("kristianwindsor/stocksvision-crawlscheduler", "./crawlscheduler/")
    }

    stage('Build MySQL') {
        mysql = docker.build("kristianwindsor/stocksvision-mysql", "./mysql/")
    }

    stage('Build WebUI') {
        webui = docker.build("kristianwindsor/stocksvision-webui", "./webui/")
    }

    stage('Push Images') {
        docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
            backend.push(buildname)
            backend.push("latest")
            crawler.push(buildname)
            crawler.push("latest")
            crawlscheduler.push(buildname)
            crawlscheduler.push("latest")
            mysql.push(buildname)
            mysql.push("latest")
            webui.push(buildname)
            webui.push("latest")
        }
    }
    stage('Deploy') {
        sh """
            sed -i "s/kristianwindsor\\/stocksvision-backend.*/kristianwindsor\\/stocksvision-backend:$buildname/" deployment.yaml
            sed -i "s/kristianwindsor\\/stocksvision-crawler.*/kristianwindsor\\/stocksvision-crawler:$buildname/" deployment.yaml
            sed -i "s/kristianwindsor\\/stocksvision-crawlscheduler.*/kristianwindsor\\/stocksvision-crawlscheduler:$buildname/" deployment.yaml
            sed -i "s/kristianwindsor\\/stocksvision-mysql.*/kristianwindsor\\/stocksvision-mysql:$buildname/" deployment.yaml
            sed -i "s/kristianwindsor\\/stocksvision-webui.*/kristianwindsor\\/stocksvision-webui:$buildname/" deployment.yaml
            cat deployment.yaml
            kubectl apply -f deployment.yaml
        """
    }
}