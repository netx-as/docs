all:
	docker stop docs || true
	docker build --rm -t netx-docs .
	docker run -i -t --rm -d -p 8080:80 --name docs netx-docs 

stop:
	docker stop docs; docker rm docs

