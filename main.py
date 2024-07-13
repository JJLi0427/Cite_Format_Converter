import func as fn
import ui

if __name__ == "__main__":
    # Load log file
    fn.load_history()

    # Start the main loop
    ui.root.mainloop()