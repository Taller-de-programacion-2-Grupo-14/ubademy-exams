#Run your file
buildImage:
	docker build . -t "${USER}"/examenes
runImage:
	docker run -p 8080:8080 -d "${USER}"/examenes

buildDC:
	docker-compose build --no-cache
runDC:
	docker-compose up -d 
