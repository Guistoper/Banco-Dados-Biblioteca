import customtkinter as ctk

BLUE_COLOR = "#206eff" 
BLUE_COLOR_HOVER = "#0c50ce"  
LIGHT_COLOR = "#4083ff" 
YELLOW_COLOR = "#FFE600" 
YELLOW_COLOR_HOVER = "#DDC700" 
LIGHT_PURPLE_COLOR = "#D2B6FF"
DARK_PURPLE_COLOR = "#C5A0FF"
TEXT_COLOR_BLACK = "#000000"
TEXT_COLOR_WHITE = "#ffffff"
BUTTON_NEUTRAL = "#e0e0e0"

GENRE_COLORS = {
    "Romance": "#FF6E86",        
    "Aventura": "#FF9900",       
    "Fantasia": "#F8BCFF",       
    "Suspense/Thriller": "#BDBDBD", 
    "Ficção Científica": "#00CED1", 
    "Biografia/Autobiografia": "#29B96A" 
}

class DashboardApp(ctk.CTk):
    def __init__(self, login_window):
        super().__init__()

        self.login_window = login_window
        self.title("Sistema de Biblioteca - Administração")
        self.geometry("1280x720")
        self.minsize(854, 480)
        self.resizable(True, True)

        self.active_button_name = "ADMINISTRAÇÃO"
        self.buttons = {}
        self.sidebar_visible = True
        self.filter_menu_visible = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.main_frame = None
        self.action_menu_frame = None
        self.filter_menu_frame = None

        self.setup()

    def setup(self):
        self.sidebar_frame = ctk.CTkFrame(self, fg_color=BLUE_COLOR, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.collapse_button = ctk.CTkButton(self.sidebar_frame, text="←", fg_color=LIGHT_COLOR, hover_color=BLUE_COLOR_HOVER, text_color=TEXT_COLOR_BLACK, font=("Arial", 24), width=20, command=self.toggle_sidebar)
        self.collapse_button.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        self.collapse_button.bind("<Enter>", lambda e: self.collapse_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        self.collapse_button.bind("<Leave>", lambda e: self.collapse_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

        self.buttons["ADMINISTRAÇÃO"] = self.create_sidebar_button("ADMINISTRAÇÃO", 1, self.show_admin)
        self.buttons["LIVROS"] = self.create_sidebar_button("LIVROS", 2, self.show_books)
        self.buttons["USUÁRIOS"] = self.create_sidebar_button("USUÁRIOS", 3, self.show_users)        
        self.buttons["EMPRÉSTIMOS"] = self.create_sidebar_button("EMPRÉSTIMOS", 4, self.show_loans)
        self.buttons["DEVOLUÇÕES"] = self.create_sidebar_button("DEVOLUÇÕES", 5, self.show_returns)

        self.buttons["SAIR"] = self.create_sidebar_button("SAIR", 7, self.logout)

        self.main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.expand_button_frame = ctk.CTkFrame(self, fg_color=BLUE_COLOR_HOVER, width=50, corner_radius=0)

        self.expand_button = ctk.CTkButton(self.expand_button_frame, text="→", fg_color="transparent", hover_color=BLUE_COLOR, font=("Arial", 24), width=20, command=self.toggle_sidebar)
        self.expand_button.place(relx=0.5, rely=0.5, anchor="center")

        self.set_active_button(self.active_button_name)
        self.show_admin()

    def create_sidebar_button(self, text, row, command_func):
        def wrapped_command():
            if text != "SAIR":
                self.set_active_button(text)
            command_func()

        button = ctk.CTkButton(self.sidebar_frame, text=f"{text}", compound="left", anchor="w", corner_radius=25, fg_color=LIGHT_COLOR, text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), command=wrapped_command)
        button.bind("<Enter>", lambda e, b=button: b.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        button.bind("<Leave>", lambda e, b=button: (b.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR)if self.active_button_name != text else None))

        if text == "SAIR":
            button.grid(row=row, column=0, padx=10, pady=10, sticky="sew")
        else:
            button.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
        return button
    
    def set_active_button(self, name):
        if self.active_button_name in self.buttons:
            old_button = self.buttons[self.active_button_name]
            old_button.configure(fg_color=LIGHT_COLOR, text_color=TEXT_COLOR_BLACK)
            if self.active_button_name != "SAIR":
                old_button.bind("<Enter>", lambda e: old_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
                old_button.bind("<Leave>", lambda e: old_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

        if name != "SAIR" and name in self.buttons:
            new_button = self.buttons[name]
            self.active_button_name = name

            new_button.configure(fg_color=YELLOW_COLOR, text_color=TEXT_COLOR_BLACK)
            new_button.bind("<Enter>", lambda e: new_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=YELLOW_COLOR_HOVER))
            new_button.bind("<Leave>", lambda e: new_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=YELLOW_COLOR))

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.grid_forget()
            self.collapse_button.grid_forget()

            self.expand_button_frame.grid(row=0, column=0, sticky="nsew")

            self.main_frame.grid_forget()
            self.main_frame.grid(row=0, column=1, sticky="nsew", columnspan=1)

            self.grid_columnconfigure(0, weight=0)
            self.grid_columnconfigure(1, weight=1)

            self.sidebar_visible = False

        else:
            self.expand_button_frame.grid_forget()

            self.grid_columnconfigure(0, weight=0)
            self.grid_columnconfigure(1, weight=1)

            self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
            self.collapse_button.grid(row=0, column=0, padx=20, pady=20, sticky="n")

            self.main_frame.grid_forget()
            self.main_frame.grid(row=0, column=1, sticky="nsew")

            self.sidebar_visible = True

    def toggle_action_menu(self):
        if self.action_menu_frame and self.action_menu_frame.winfo_exists():
            self.action_menu_frame.destroy()
            self.action_menu_frame = None
        else:
            self.show_action_menu()

    def show_action_menu(self):
        if self.action_menu_frame and self.action_menu_frame.winfo_exists():
            try:
                self.action_menu_frame.destroy()
            except:
                pass

        self.action_menu_frame = ctk.CTkFrame(self.main_frame, fg_color=BLUE_COLOR, corner_radius=25)
        self.action_menu_frame.place(relx=0.98, rely=0.91, anchor="se")

        self.create_action_menu_button("ADICIONAR USUÁRIO", self.add_user).pack(pady=5, padx=10, fill="x")
        self.create_action_menu_button("ADICIONAR LIVRO", self.add_book).pack(pady=5, padx=10, fill="x")
        self.create_action_menu_button("NOVO EMPRÉSTIMO", self.make_loan).pack(pady=5, padx=10, fill="x")

    def create_action_menu_button(self, text, command):
        action_button = ctk.CTkButton(self.action_menu_frame, text=text, command=command, fg_color=YELLOW_COLOR, text_color=TEXT_COLOR_BLACK, corner_radius=25, font=("Arial", 11, "bold"))
        action_button.bind("<Enter>", lambda e: action_button.configure(fg_color=YELLOW_COLOR_HOVER))
        action_button.bind("<Leave>", lambda e: action_button.configure(fg_color=YELLOW_COLOR))

        return action_button

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def close(self):
        self.destroy()

    def logout(self):
        popup = ctk.CTkToplevel(self, fg_color="white")
        popup.title("Sair")
        popup.minsize(250, 0)
        popup.transient(self)
        popup.grab_set()

        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=1)

        content_frame = ctk.CTkFrame(popup, fg_color="white", corner_radius=0)
        content_frame.pack(fill="both", expand=True)
        content_frame.grid_columnconfigure((0, 1), weight=1)

        popup_icon = ctk.CTkLabel(content_frame, text="🚪", text_color=TEXT_COLOR_BLACK, font=("Arial", 60))
        popup_icon.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        popup_title = ctk.CTkLabel(content_frame, text="Tem certeza que deseja sair?", text_color=TEXT_COLOR_BLACK, font=("Arial", 14, "bold"), justify="center")
        popup_title.grid(row=1, column=0, columnspan=2, pady=(5, 20))

        cancel_button = ctk.CTkButton(content_frame, text="Cancelar", command=popup.destroy, fg_color=LIGHT_COLOR, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        cancel_button.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="e")
        cancel_button.bind("<Enter>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        cancel_button.bind("<Leave>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

        confirm_button = ctk.CTkButton(content_frame, text="Confirmar", command=self.close, fg_color=BUTTON_NEUTRAL, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        confirm_button.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="w")
        confirm_button.bind("<Enter>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        confirm_button.bind("<Leave>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=BUTTON_NEUTRAL))

        req_width = popup.winfo_reqwidth()
        req_height = popup.winfo_reqheight()
        x = self.winfo_x() + (self.winfo_width() // 2) - (req_width // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (req_height // 2)
        popup.geometry(f"{req_width}x{req_height}+{x}+{y}")
    
    def show_admin(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.main_frame.grid_rowconfigure(1, weight=0)
        self.main_frame.grid_rowconfigure(2, weight=1)

        title = ctk.CTkLabel(self.main_frame, text="ADMINISTRAÇÃO", fg_color="transparent", text_color=TEXT_COLOR_BLACK, font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, columnspan=3, padx=25, pady=(23, 15), sticky="nw")

        self.create_dashboard_card("LIVROS CADASTRADOS", "📖", "---", 1, 0)
        self.create_dashboard_card("USUÁRIOS", "👤", "---", 1, 1)
        self.create_dashboard_card("EMPRÉSTIMOS", "👥", "---", 1, 2)
        self.create_dashboard_card("DEVOLUÇÕES", "📕", "---", 1, 3)

        self.plus_button = ctk.CTkButton(self.main_frame, text="➕", width=40, height=40, corner_radius=25, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, command=self.toggle_action_menu)
        self.plus_button.grid(row=2, column=3, padx=20, pady=20, sticky="se")

    def create_dashboard_card(self, title, symbol, value, row, column):
        card_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=25, border_width=1, width=200, height=150, border_color=BUTTON_NEUTRAL)
        card_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        card_frame.grid_propagate(False)
        card_frame.pack_propagate(False)

        icon_label = ctk.CTkLabel(card_frame, text=symbol, text_color=YELLOW_COLOR, font=("Arial", 48, "bold"), fg_color="transparent")
        icon_label.pack(pady=5)

        value_label = ctk.CTkLabel(card_frame, text=value, text_color=TEXT_COLOR_BLACK, font=("Arial", 24, "bold"))
        value_label.pack(pady=5)

        title_label = ctk.CTkLabel(card_frame, text=title, text_color="gray", font=("Arial", 10))
        title_label.pack(pady=5)

    def show_books(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((1, 2, 3), weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        row_index = 0

        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.grid(row=row_index, column=0, sticky="ew", padx=25, pady=(17, 15))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=0)

        title = ctk.CTkLabel(top_frame, text="LIVROS", fg_color="transparent", text_color=TEXT_COLOR_BLACK, font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=(0, 20))

        search_frame = ctk.CTkFrame(top_frame, fg_color=LIGHT_PURPLE_COLOR, corner_radius=25)
        search_frame.grid(row=0, column=1, sticky="ew")

        search_icon = ctk.CTkLabel(search_frame, text="🔍", text_color="gray", font=("Arial", 16))
        search_icon.pack(side="left", padx=(10, 2))

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar...", border_width=0, fg_color="transparent", text_color=TEXT_COLOR_BLACK)
        search_entry.pack(side="left", expand=True, fill="x", ipady=5)

        filter_button = ctk.CTkButton(search_frame, text="⏷", fg_color="transparent", hover_color=DARK_PURPLE_COLOR, text_color="gray", width=10, font=("Arial", 16), command=None)
        filter_button.pack(side="right", padx=10)

        self.plus_button = ctk.CTkButton(top_frame, text="➕", width=40, height=40, corner_radius=25, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, command=self.add_book)
        self.plus_button.grid(row=0, column=2, sticky="e", padx=(25, 0))

        row_index += 1

        table_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="white", corner_radius=25)
        table_frame.grid(row=row_index, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)

        placeholder = ctk.CTkLabel(table_frame, text="NENHUM LIVRO CADASTRADO.", text_color="gray", font=("Arial", 14, "bold"))
        placeholder.grid(row=0, column=0, sticky="nsew")

        row_index += 1

        pagination_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        pagination_frame.grid(row=row_index, column=0, sticky="s", pady=(20, 15))

        previous_button = ctk.CTkButton(pagination_frame, text="←", fg_color="transparent", hover_color=BUTTON_NEUTRAL, text_color="gray", width=30)
        previous_button.pack(side="left", padx=5)

        pagination_number = ctk.CTkButton(pagination_frame, text="...", fg_color="black", hover_color="gray", width=30)
        pagination_number.pack(side="left", padx=5)

        next_button = ctk.CTkButton(pagination_frame, text="→", fg_color="transparent", hover_color=BUTTON_NEUTRAL, text_color="gray", width=30)
        next_button.pack(side="left", padx=5)

    def show_users(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((1, 2, 3), weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        row_index = 0

        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.grid(row=row_index, column=0, sticky="ew", padx=25, pady=(17, 15))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=0)

        title = ctk.CTkLabel(top_frame, text="USUÁRIOS", fg_color="transparent", text_color=TEXT_COLOR_BLACK, font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=(0, 20))

        search_frame = ctk.CTkFrame(top_frame, fg_color=LIGHT_PURPLE_COLOR, corner_radius=25)
        search_frame.grid(row=0, column=1, sticky="ew")

        search_icon = ctk.CTkLabel(search_frame, text="🔍", text_color="gray", font=("Arial", 16))
        search_icon.pack(side="left", padx=(10, 2))

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar...", border_width=0, fg_color="transparent", text_color=TEXT_COLOR_BLACK)
        search_entry.pack(side="left", expand=True, fill="x", ipady=5)

        filter_button = ctk.CTkButton(search_frame, text="⏷", fg_color="transparent", hover_color=DARK_PURPLE_COLOR, text_color="gray", width=10, font=("Arial", 16), command=None)
        filter_button.pack(side="right", padx=10)

        self.plus_button = ctk.CTkButton(top_frame, text="➕", width=40, height=40, corner_radius=25, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, command=self.add_user)
        self.plus_button.grid(row=0, column=2, sticky="e", padx=(25, 0))

        row_index += 1

        table_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="white", corner_radius=25)
        table_frame.grid(row=row_index, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)

        placeholder = ctk.CTkLabel(table_frame, text="NENHUM USUÁRIO CADASTRADO.", text_color="gray", font=("Arial", 14, "bold"))
        placeholder.grid(row=0, column=0, sticky="nsew")

        row_index += 1

        pagination_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        pagination_frame.grid(row=row_index, column=0, sticky="s", pady=(20, 15))

        previous_button = ctk.CTkButton(pagination_frame, text="←", fg_color="transparent", hover_color=BUTTON_NEUTRAL, text_color="gray", width=30)
        previous_button.pack(side="left", padx=5)

        pagination_number = ctk.CTkButton(pagination_frame, text="...", fg_color="black", hover_color="gray", width=30)
        pagination_number.pack(side="left", padx=5)

        next_button = ctk.CTkButton(pagination_frame, text="→", fg_color="transparent", hover_color=BUTTON_NEUTRAL, text_color="gray", width=30)
        next_button.pack(side="left", padx=5)

    def show_loans(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((1, 2, 3), weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        row_index = 0

        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.grid(row=row_index, column=0, sticky="ew", padx=25, pady=(17, 15))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=0)

        title = ctk.CTkLabel(top_frame, text="EMPRÉSTIMOS", fg_color="transparent", text_color=TEXT_COLOR_BLACK, font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=(0, 20))

        search_frame = ctk.CTkFrame(top_frame, fg_color=LIGHT_PURPLE_COLOR, corner_radius=25)
        search_frame.grid(row=0, column=1, sticky="ew")

        search_icon = ctk.CTkLabel(search_frame, text="🔍", text_color="gray", font=("Arial", 16))
        search_icon.pack(side="left", padx=(10, 2))

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar...", border_width=0, fg_color="transparent", text_color=TEXT_COLOR_BLACK)
        search_entry.pack(side="left", expand=True, fill="x", ipady=5)

        filter_button = ctk.CTkButton(search_frame, text="⏷", fg_color="transparent", hover_color=DARK_PURPLE_COLOR, text_color="gray", width=10, font=("Arial", 16), command=None)
        filter_button.pack(side="right", padx=10)

        self.plus_button = ctk.CTkButton(top_frame, text="➕", width=40, height=40, corner_radius=25, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, command=self.make_loan)
        self.plus_button.grid(row=0, column=2, sticky="e", padx=(25, 0))

        row_index += 1

        table_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="white", corner_radius=25)
        table_frame.grid(row=row_index, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)

        placeholder = ctk.CTkLabel(table_frame, text="NENHUM EMPRÉSTIMO REGISTRADO.", text_color="gray", font=("Arial", 14, "bold"))
        placeholder.grid(row=0, column=0, sticky="nsew")

        row_index += 1

        pagination_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        pagination_frame.grid(row=row_index, column=0, sticky="s", pady=(20, 15))

        previous_button = ctk.CTkButton(pagination_frame, text="←", fg_color="transparent", hover_color=BUTTON_NEUTRAL, text_color="gray", width=30)
        previous_button.pack(side="left", padx=5)

        pagination_number = ctk.CTkButton(pagination_frame, text="...", fg_color="black", hover_color="gray", width=30)
        pagination_number.pack(side="left", padx=5)

        next_button = ctk.CTkButton(pagination_frame, text="→", fg_color="transparent", hover_color=BUTTON_NEUTRAL, text_color="gray", width=30)
        next_button.pack(side="left", padx=5)

    def show_returns(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((1, 2, 3), weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        row_index = 0

        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.grid(row=row_index, column=0, sticky="ew", padx=25, pady=(18, 15))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=0)

        title = ctk.CTkLabel(top_frame, text="DEVOLUÇÕES", fg_color="transparent", text_color=TEXT_COLOR_BLACK, font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=(0, 20))

        search_frame = ctk.CTkFrame(top_frame, fg_color=LIGHT_PURPLE_COLOR, corner_radius=25)
        search_frame.grid(row=0, column=1, sticky="ew",)

        search_icon = ctk.CTkLabel(search_frame, text="🔍", text_color="gray", font=("Arial", 16))
        search_icon.pack(side="left", padx=(10, 2))

        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar...", border_width=0, fg_color="transparent", text_color=TEXT_COLOR_BLACK)
        search_entry.pack(side="left", expand=True, fill="x", ipady=5)

        filter_button = ctk.CTkButton(search_frame, text="⏷", fg_color="transparent", hover_color=DARK_PURPLE_COLOR, text_color="gray", width=10, font=("Arial", 16), command=None)
        filter_button.pack(side="right", padx=10)

        row_index += 1

        table_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="white", corner_radius=25)
        table_frame.grid(row=row_index, column=0, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)

        placeholder = ctk.CTkLabel(table_frame, text="NENHUMA DEVOLUÇÃO REGISTRADA.", text_color="gray", font=("Arial", 14, "bold"))
        placeholder.grid(row=0, column=0, sticky="nsew")

        row_index += 1

        pagination_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        pagination_frame.grid(row=row_index, column=0, sticky="s", pady=(20, 15))

        previous_button = ctk.CTkButton(pagination_frame, text="←", fg_color="transparent", hover_color=BUTTON_NEUTRAL, text_color="gray", width=30)
        previous_button.pack(side="left", padx=5)

        pagination_number = ctk.CTkButton(pagination_frame, text="...", fg_color="black", hover_color="gray", width=30)
        pagination_number.pack(side="left", padx=5)

        next_button = ctk.CTkButton(pagination_frame, text="→", fg_color="transparent", hover_color=BUTTON_NEUTRAL, text_color="gray", width=30)
        next_button.pack(side="left", padx=5)

    def add_user(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((1, 2, 3), weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(self.main_frame, text="ADICIONAR USUÁRIO", fg_color="transparent", text_color=TEXT_COLOR_BLACK, font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=25, pady=(23, 15))

        form_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        form_frame.grid(row=2, column=0, sticky="n", padx=20, pady=10)
        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)

        row_index = 0

        name_label = ctk.CTkLabel(form_frame, text="Nome completo:", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        name_label.grid(row=row_index, column=0, sticky="ew", padx=(0, 20), pady=(10, 5), ipady=5)

        nome_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        nome_entry.grid(row=row_index, column=1, sticky="ew", pady=(10, 5), ipady=5)

        row_index += 1

        type_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        type_frame.grid(row=row_index, column=1, sticky="w", pady=15)

        user_type = ctk.StringVar(value="Aluno")

        aluno_button = ctk.CTkRadioButton(type_frame, text="Aluno", variable=user_type, value="Aluno", fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, text_color=TEXT_COLOR_BLACK, font=("Arial", 11))
        aluno_button.pack(side="left")

        professor_button = ctk.CTkRadioButton(type_frame, text="Professor", variable=user_type, value="Professor", fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, text_color=TEXT_COLOR_BLACK, font=("Arial", 11))
        professor_button.pack(side="left")

        row_index += 1

        email_label = ctk.CTkLabel(form_frame, text="Email institucional (RA):", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        email_label.grid(row=row_index, column=0, sticky="w", padx=(0, 20), pady=(10, 5))

        email_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        email_entry.grid(row=row_index, column=1, sticky="ew", pady=(10, 5), ipady=5)

        row_index += 1

        room_label = ctk.CTkLabel(form_frame, text="Série:", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        room_label.grid(row=row_index, column=0, sticky="w", padx=(0, 20), pady=(10, 5))

        room_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=53, corner_radius=25, validate="key", validatecommand=(form_frame.register(lambda P: len(P) <= 3), "%P"))
        room_entry.grid(row=row_index, column=1, sticky="w", pady=(10, 5), ipady=5)

        row_index += 1

        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=row_index, column=1, columnspan=2, sticky="s", pady=(20, 10))

        cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=None, fg_color=LIGHT_COLOR, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        cancel_button.grid(row=0, column=0, sticky="e", padx=10, pady=(0, 10))
        cancel_button.bind("<Enter>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        cancel_button.bind("<Leave>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

        confirm_button = ctk.CTkButton(button_frame, text="Confirmar", command=None, fg_color=BUTTON_NEUTRAL, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        confirm_button.grid(row=0, column=1, sticky="w", padx=10, pady=(0, 10))
        confirm_button.bind("<Enter>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        confirm_button.bind("<Leave>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=BUTTON_NEUTRAL))

    def add_book(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((1, 2, 3), weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(self.main_frame, text="ADICIONAR LIVRO", fg_color="transparent", text_color=TEXT_COLOR_BLACK, font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=25, pady=(23, 15))

        form_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        form_frame.grid(row=2, column=0, sticky="n", padx=20, pady=10)
        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)

        row_index = 0

        book_label = ctk.CTkLabel(form_frame, text="Nome do livro:", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        book_label.grid(row=row_index, column=0, sticky="ew", padx=(0, 20), pady=(10, 5), ipady=5)

        book_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        book_entry.grid(row=row_index, column=1, sticky="ew", pady=(10, 5), ipady=5)

        row_index += 1

        author_label = ctk.CTkLabel(form_frame, text="Autor do livro:", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        author_label.grid(row=row_index, column=0, sticky="w", padx=(0, 20), pady=(10, 5))

        author_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        author_entry.grid(row=row_index, column=1, sticky="ew", pady=(10, 5), ipady=5)

        row_index += 1

        genre_label = ctk.CTkLabel(form_frame, text="Gênero do livro:", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        genre_label.grid(row=row_index, column=0, sticky="w", padx=(0, 20), pady=(10, 5))

        genre_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        genre_entry.grid(row=row_index, column=1, sticky="ew", pady=(10, 5), ipady=5)

        row_index += 1

        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=row_index, column=1, columnspan=2, sticky="s", pady=(20, 10))

        cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=None, fg_color=LIGHT_COLOR, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        cancel_button.grid(row=0, column=0, sticky="e", padx=10, pady=(0, 10))
        cancel_button.bind("<Enter>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        cancel_button.bind("<Leave>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

        confirm_button = ctk.CTkButton(button_frame, text="Confirmar", command=None, fg_color=BUTTON_NEUTRAL, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        confirm_button.grid(row=0, column=1, sticky="w", padx=10, pady=(0, 10))
        confirm_button.bind("<Enter>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        confirm_button.bind("<Leave>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=BUTTON_NEUTRAL))

    def make_loan(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((1, 2, 3), weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(self.main_frame, text="FAZER EMPRÉSTIMO", fg_color="transparent", text_color=TEXT_COLOR_BLACK, font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=25, pady=(23, 15))

        form_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        form_frame.grid(row=2, column=0, sticky="n", padx=20, pady=10)
        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)

        row_index = 0

        email_label = ctk.CTkLabel(form_frame, text="Email institucional (RA):", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        email_label.grid(row=row_index, column=0, sticky="ew", padx=(0, 20), pady=(10, 5), ipady=5)

        email_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        email_entry.grid(row=row_index, column=1, sticky="ew", pady=(10, 5), ipady=5)

        row_index += 1

        book_label = ctk.CTkLabel(form_frame, text="Nome do livro:", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        book_label.grid(row=row_index, column=0, sticky="w", padx=(0, 20), pady=(10, 5))

        book_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        book_entry.grid(row=row_index, column=1, sticky="ew", pady=(10, 5), ipady=5)

        row_index += 1

        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=row_index, column=1, columnspan=2, sticky="s", pady=(20, 10))

        cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=None, fg_color=LIGHT_COLOR, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        cancel_button.grid(row=0, column=0, sticky="e", padx=10, pady=(0, 10))
        cancel_button.bind("<Enter>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        cancel_button.bind("<Leave>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

        confirm_button = ctk.CTkButton(button_frame, text="Confirmar", command=None, fg_color=BUTTON_NEUTRAL, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        confirm_button.grid(row=0, column=1, sticky="w", padx=10, pady=(0, 10))
        confirm_button.bind("<Enter>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        confirm_button.bind("<Leave>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=BUTTON_NEUTRAL))
        
app = DashboardApp(login_window=None)
app.mainloop()