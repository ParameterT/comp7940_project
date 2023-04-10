docker build -t my_chatbot .
docker kill my_chatbot
docker rm my_chatbot
docker run --restart=always -d -it --name my_chatbot my_chatbot
docker logs my_chatbot
