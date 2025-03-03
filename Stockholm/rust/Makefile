all:
	(cd stockholm_rust && cargo build --release) && mv stockholm_rust/target/release/stockholm_rust ./exe

clean:
	(cd stockholm_rust && cargo clean)

fclean: clean
	rm -rf exe

re: fclean all

.PHONY: clean fclean all re