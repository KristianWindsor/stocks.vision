node {

    buildname = 'b' + env.BUILD_NUMBER
    currentBuild.displayName = buildname

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

    stage('Build Database') {
        db = docker.build("kristianwindsor/stocksvision-db", "./db/")
    }

    stage('Build WebUI') {
        webui = docker.build("kristianwindsor/stocksvision-webui", "./webui/")
    }

    stage('Push Images') {
        docker.withRegistry('', 'dockerhub') {
            backend.push(buildname)
            backend.push("latest")
            crawler.push(buildname)
            crawler.push("latest")
            crawlscheduler.push(buildname)
            crawlscheduler.push("latest")
            db.push(buildname)
            db.push("latest")
            webui.push(buildname)
            webui.push("latest")
        }
    }
    stage('Deploy') {
        sh """
            sed -i "s/kristianwindsor\\/stocksvision-backend.*/kristianwindsor\\/stocksvision-backend:$buildname/" deployment.yaml
            sed -i "s/kristianwindsor\\/stocksvision-crawler.*/kristianwindsor\\/stocksvision-crawler:$buildname/" deployment.yaml
            sed -i "s/kristianwindsor\\/stocksvision-crawlscheduler.*/kristianwindsor\\/stocksvision-crawlscheduler:$buildname/" deployment.yaml
            sed -i "s/kristianwindsor\\/stocksvision-db.*/kristianwindsor\\/stocksvision-db:$buildname/" deployment.yaml
            sed -i "s/kristianwindsor\\/stocksvision-webui.*/kristianwindsor\\/stocksvision-webui:$buildname/" deployment.yaml
            cat deployment.yaml
            kubectl apply -f deployment.yaml
        """
    }
}