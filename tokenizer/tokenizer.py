class Encoder:
    def encode(self, text):
        return [ord(char) for char in text]

    def decode(self, tokens):
        return ''.join([chr(token) for token in tokens])


def main():
    encoder = Encoder()
    print("Enter text to tokenize (or type 'exit' to quit):")
    while True:
        user_input = input("> ")

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        tokens = encoder.encode(user_input)
        print("Token IDs:", tokens)

        reconstructed_text = encoder.decode(tokens)
        print("Reconstructed text:", reconstructed_text)

        print("\nEnter more text (or 'exit' to quit):")


if __name__ == "__main__":
    main()