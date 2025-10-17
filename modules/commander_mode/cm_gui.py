import tkinter as tk


class CM_GUI():
    """Commander Mode API module for the Kill Tracker."""

    def _get_palette(self):
        default_palette = {
            'bg_dark': '#1e1e1e',
            'bg_mid': '#252526',
            'bg_light': '#333333',
            'text': '#cccccc',
            'text_dark': '#888888',
            'accent': '#007acc',
            'button': '#007acc',
            'submit_button': '#4CAF50',
            'error': '#f44747',
        }
        gui_module = getattr(self, "gui", None)
        return getattr(gui_module, "colors", default_palette)

    def connected_users_insert(self, player_data: str) -> None:
        """Insert into connected users GUI element"""
        self.connected_users_listbox.insert(tk.END, player_data)

    def connected_users_delete(self) -> None:
        """Delete from connected users GUI element"""
        self.connected_users_listbox.delete(0, tk.END)

    def allocated_forces_insert(self, player_data: str) -> None:
        """Insert into allocated forces GUI element"""
        self.allocated_forces_listbox.insert(tk.END, player_data)

    def allocated_forces_delete(self) -> None:
        """Delete from allocated forces GUI element"""
        self.allocated_forces_listbox.delete(0, tk.END)

    def config_search_bar(self, widget: tk.Entry, placeholder_text: str) -> None:
        """Handle search bar for filtering connected users."""

        def remove_placeholder(event):
            placeholder_text = getattr(event.widget, "placeholder", "")
            if placeholder_text and event.widget.get() == placeholder_text:
                event.widget.delete(0, tk.END)

        def add_placeholder(event):
            placeholder_text = getattr(event.widget, "placeholder", "")
            if placeholder_text and event.widget.get() == "":
                event.widget.insert(0, placeholder_text)

        widget.placeholder = placeholder_text
        if widget.get() == "":
            widget.insert(tk.END, placeholder_text)
        widget.bind("<FocusIn>", remove_placeholder)
        widget.bind("<FocusOut>", add_placeholder)

    def toggle_commander(self):
        """Handle connect commander button."""
        palette = self._get_palette()
        if self.heartbeat_status["active"]:
            self.stop_heartbeat_threads()
            self.connect_commander_button.config(
                text="Connect to Commander",
                fg=palette['text'],
                bg=palette['bg_light'],
                activebackground=palette['accent'],
                activeforeground='#FFFFFF',
            )
            self.log.error("You are disconnected from Commander.")
        else:
            self.heartbeat_status["active"] = True
            self.start_heartbeat_threads()
            self.connect_commander_button.config(
                text="Disconnect Commander",
                fg='#FFFFFF',
                bg=palette['submit_button'],
                activebackground=palette['submit_button'],
                activeforeground='#FFFFFF',
            )
            self.log.success("You are connected to Commander.")

    def setup_commander_mode(self) -> None:
        """
        Opens a new window for Commander Mode, displaying connected users and allocated forces.
        Includes functionality for moving users to the allocated forces list and handling status changes.
        """
        try:
            palette = self._get_palette()
            self.commander_window = tk.Toplevel()
            self.commander_window.title("Commander Mode")
            self.commander_window.minsize(width=1280, height=720)
            self.commander_window.configure(bg=palette['bg_dark'])
            self.commander_window.protocol("WM_DELETE_WINDOW", lambda x=self.commander_window: self.destroy_window(x))

            search_var = tk.StringVar()
            search_bar = tk.Entry(
                self.commander_window,
                textvariable=search_var,
                font=("Segoe UI", 11),
                width=30,
                bg=palette['bg_light'],
                fg=palette['text'],
                relief=tk.FLAT,
                insertbackground=palette['text'],
            )
            self.config_search_bar(search_bar, "Search Connected Users...")
            search_bar.pack(pady=(10, 0))

            connected_users_frame = tk.Frame(
                self.commander_window,
                bg=palette['bg_dark'],
            )
            connected_users_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=(5, 10))

            connected_users_label = tk.Label(
                connected_users_frame,
                text="Connected Users",
                font=("Segoe UI", 11, "bold"),
                fg=palette['accent'],
                bg=palette['bg_dark'],
            )
            connected_users_label.pack()

            self.connected_users_listbox = tk.Listbox(
                connected_users_frame,
                selectmode=tk.MULTIPLE,
                width=40,
                height=20,
                font=("Segoe UI", 10),
                bg=palette['bg_mid'],
                fg=palette['text'],
                selectbackground=palette['accent'],
                selectforeground='#FFFFFF',
                relief=tk.FLAT,
            )
            self.connected_users_listbox.pack(fill=tk.BOTH, expand=True)

            allocated_forces_frame = tk.Frame(
                self.commander_window,
                bg=palette['bg_dark'],
            )
            allocated_forces_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=(5, 10))

            allocated_forces_label = tk.Label(
                allocated_forces_frame,
                text="Allocated Forces",
                font=("Segoe UI", 11, "bold"),
                fg=palette['accent'],
                bg=palette['bg_dark'],
            )
            allocated_forces_label.pack()

            self.allocated_forces_listbox = tk.Listbox(
                allocated_forces_frame,
                width=40,
                height=20,
                font=("Segoe UI", 10),
                bg=palette['bg_mid'],
                fg=palette['text'],
                selectbackground=palette['accent'],
                selectforeground='#FFFFFF',
                relief=tk.FLAT,
            )
            self.allocated_forces_listbox.pack(fill=tk.BOTH, expand=True)

            button_kwargs = {
                'font': ("Segoe UI", 10, "bold"),
                'bg': palette['button'],
                'fg': '#FFFFFF',
                'activebackground': palette['accent'],
                'activeforeground': '#FFFFFF',
                'relief': tk.FLAT,
                'bd': 0,
                'padx': 12,
                'pady': 6,
            }

            self.connect_commander_button = tk.Button(
                self.commander_window,
                text="Connect to Commander",
                command=self.toggle_commander,
                **button_kwargs,
            )
            self.connect_commander_button.pack(pady=(60, 10))

            add_user_to_fleet_button = tk.Button(
                self.commander_window,
                text="Add User to Fleet",
                command=self.allocate_selected_users,
                **button_kwargs,
            )
            add_user_to_fleet_button.pack(pady=(30, 10))

            add_all_to_fleet_button = tk.Button(
                self.commander_window,
                text="Add All Users to Fleet",
                command=self.allocate_all_users,
                **button_kwargs,
            )
            add_all_to_fleet_button.pack(pady=(10, 10))

            take_command_button = tk.Button(
                self.commander_window,
                text="Take Command of Fleet",
                command=self.take_command,
                **button_kwargs,
            )
            take_command_button.pack(pady=(10, 10))

            abort_command_button = tk.Button(
                self.commander_window,
                text="Abort Command",
                command=self.abort_command_func,
                **button_kwargs,
            )
            abort_command_button.pack(pady=(10, 10))

            start_battle_button = tk.Button(
                self.commander_window,
                text="Start Battle",
                command=self.start_battle_func,
                **button_kwargs,
            )
            start_battle_button.pack(pady=(10, 10))

            mark_battle_complete_button = tk.Button(
                self.commander_window,
                text="Mark a Battle Done",
                command=self.mark_battle_complete_func,
                **button_kwargs,
            )
            mark_battle_complete_button.pack(pady=(10, 10))

            self.gui.commander_mode_button["state"] = tk.DISABLED

            def search_users(*args):
                search_query = search_var.get().lower()
                self.connected_users_listbox.delete(0, tk.END)
                if self.connected_users:
                    for user in self.connected_users:
                        if search_query in user['player'].lower():
                            self.connected_users_listbox.insert(tk.END, user['player'])

            search_var.trace("w", search_users)
        except Exception as e:
            self.log.error(f"setup_commander_mode(): {e.__class__.__name__} {e}")

    def destroy_window(self, commander_window) -> None:
        """Stop heartbeat if window is closed"""
        commander_window.destroy()
        self.commander_window = None
        self.stop_heartbeat_threads()
        self.gui.commander_mode_button["state"] = tk.ACTIVE
