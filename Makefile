build:
	docker build -t meet0723patel:chatbotpaymentsystem: latest .
run: build
	docker run -p 8080:8080 meet0723patel:chatbotpaymentsystem: latest 
push: build
	docker tag meet0723patel:chatbotpaymentsystem:latest gcr.io/chatbotpaymentsystem/webhook
	docker push gcr.io/chatbotpaymentsystem/webhook