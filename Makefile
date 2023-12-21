##
## EPITECH PROJECT, 2023
## B-CNA-410-BDX-4-1-trade-edouard.belhomme
## File description:
## Makefile
##

NAME	=	trade

$(NAME)	:
			cp src/trade.py ./
			mv trade.py trade
			chmod +x trade

all	:	$(NAME)

clean:
		rm -rf trade src/__pycache__ __pycache__

fclean:	clean

re	:	fclean all

.PHONY: all clean fclean re
