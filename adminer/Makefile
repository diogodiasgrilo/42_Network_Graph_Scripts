all:
	@$(MAKE) up

up:
	@echo "$(GREEN)Docker compose UP ongoing 🏗️$(DEFAULT)"
	@docker-compose -f docker-compose.yml up --build

down: 
	@echo "$(RED)Docker compose DOWN ongoing 💥$(DEFAULT)"
	@docker-compose -f docker-compose.yml down

re: down up

ps:
	@docker-compose -f docker-compose.yml ps

volumes:
	@docker volume ls

build:
	@docker-compose -f docker-compose.yml build

restart:
	@docker-compose -f docker-compose.yml restart $(service)

deep_clean:
	@docker ps -q | xargs -r docker stop;\
	docker ps -aq | xargs -r docker rm;\
	docker images -q | xargs -r docker rmi -f;\
	docker volume ls -q | xargs -r docker volume rm;\
	docker network ls --format '{{.Name}}' | grep -vE "bridge|host|none" | xargs -r docker network rm;

.PHONY: all up down re deep_clean logs ps volumes build restart deep_clean

#COLORS
GREEN = \033[1;32m
RED = \033[1;31m
DEFAULT = \033[0m