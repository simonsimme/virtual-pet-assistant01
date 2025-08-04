from model.model import run_game

if __name__ == "__main__":
    try:
        run_game()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()  # Print the full error traceback
        input("Press Enter to exit...")