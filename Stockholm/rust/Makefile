all: exe

exe: stockholm_rust/target/release/stockholm_rust
	@cp stockholm_rust/target/release/stockholm_rust ./exe

stockholm_rust/target/release/stockholm_rust:
	(cd stockholm_rust && cargo build --release)

clean:
	(cd stockholm_rust && cargo clean)

fclean: clean
	rm -rf exe

re: fclean all

.PHONY: clean fclean all re