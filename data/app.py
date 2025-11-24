import customtkinter as ctk
import mysql.connector
import tkinter as tk
from tkinter import messagebox
from CTkTable import *
from install import Install
from datetime import datetime

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

class Database:
    sql = mysql.connector.connect(
            user="root",
            password="admin",
            host="localhost",
            database = Install.main("biblioteca")
    )

class DashboardApp(ctk.CTk):
    def __init__(self, login_window):
        super().__init__()
        

        self.login_window = login_window
        self.title("Sistema Biblioteca")
        self.geometry("1280x720")
        self.minsize(854, 480)
        self.resizable(True, True)

        self.active_button_name = "ADMINISTRAÇÃO"
        self.buttons = {}
        self.sidebar_visible = True
        self.search_after_id = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.main_frame = None
        self.action_menu_frame = None

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

        self.create_action_menu_button("ADICIONAR LIVRO", self.add_book).pack(pady=5, padx=10, fill="x")
        self.create_action_menu_button("ADICIONAR USUÁRIO", self.add_user).pack(pady=5, padx=10, fill="x")
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
        popup.resizable(False, False)
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
        cancel_button.grid(row=2, column=0, padx=10, pady=(0, 25), sticky="e")
        cancel_button.bind("<Enter>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        cancel_button.bind("<Leave>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

        confirm_button = ctk.CTkButton(content_frame, text="Confirmar", command=self.close, fg_color=BUTTON_NEUTRAL, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        confirm_button.grid(row=2, column=1, padx=10, pady=(0, 25), sticky="w")
        confirm_button.bind("<Enter>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        confirm_button.bind("<Leave>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=BUTTON_NEUTRAL))

        popup.update_idletasks()
        req_width = popup.winfo_reqwidth()
        req_height = popup.winfo_reqheight()
        x = self.winfo_x() + (self.winfo_width() // 2) - (req_width // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (req_height // 2)
        popup.geometry(f"{req_width}x{req_height}+{x}+{y}")
    
    def show_admin(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=0)
        self.main_frame.grid_rowconfigure(3, weight=1)
        self.main_frame.grid_rowconfigure(4, weight=0)

        title = ctk.CTkLabel(self.main_frame, text="ADMINISTRAÇÃO", fg_color="transparent", text_color=TEXT_COLOR_BLACK, font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, columnspan=3, padx=25, pady=(23, 15), sticky="nw")

        total_livros = self.get_db_count("livros")
        total_usuarios = self.get_db_count("usuarios")

        condicao_pendente = "status = 'Pendente'" 
        total_pendentes = self.get_db_count("emprestimos", condicao_pendente)

        condicao_concluido = "status = 'Devolvido'"
        total_concluidos = self.get_db_count("emprestimos", condicao_concluido)

        condicao_atraso = "status = 'Atrasado'"
        total_atrasados = self.get_db_count("emprestimos", condicao_atraso)

        self.create_dashboard_card("LIVROS \nCADASTRADOS", "📖", total_livros, 2, 0)
        self.create_dashboard_card("USUÁRIOS \nCADASTRADOS", "👤", total_usuarios, 2, 1)
        self.create_dashboard_card("EMPRÉSTIMOS \nPENDENTES", "🕛", total_pendentes, 2, 2)
        self.create_dashboard_card("EMPRÉSTIMOS \nCONCLUÍDOS", "👍", total_concluidos, 2, 3)
        self.create_dashboard_card("EMPRÉSTIMOS \nATRASADOS", "⏱️", total_atrasados, 2, 4)

        self.plus_button = ctk.CTkButton(self.main_frame, text="➕", width=40, height=40, corner_radius=25, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, command=self.toggle_action_menu)
        self.plus_button.grid(row=4, column=4, padx=20, pady=20, sticky="se")

    def get_db_count(self, table, condition=None):
        cursor = Database.sql.cursor()
        query = f"SELECT COUNT(*) FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        
        cursor.execute(query)
        result = cursor.fetchone()
        
        return str(result[0])

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

    def on_table_click(self, cell):
        if cell["row"] == 0:
            raw_value = cell["value"]
            
            clean_value = raw_value.replace(" ▲", "").replace(" ▼", "").strip()
            
            column_name = clean_value.lower()

            if self.sort_column == column_name:
                if self.sort_direction == "ASC":
                    self.sort_direction = "DESC"
                else:
                    self.sort_direction = "ASC"
            else:
                self.sort_column = column_name
                self.sort_direction = "ASC"

            self.general_filter()

    def general_filter(self, event=None):
        if event:
            search_text = event.widget.get().strip()
        else:
            search_text = self.search_entry.get().strip()

        cursor = Database.sql.cursor()

        if self.active_button_name == "EMPRÉSTIMOS":
            try:
                hoje = datetime.now().strftime("%Y-%m-%d")
                
                query_update = "UPDATE tb_emprestimos SET status = 'Atrasado' WHERE status = 'Pendente' AND prazo < %s"
                
                cursor.execute(query_update, (hoje,))
                Database.sql.commit()
            except Exception as e:
                print(f"Erro ao atualizar atrasos: {e}")

        like = f"%{search_text}%"
        query = ""
        params = ()

        order_clause = f"ORDER BY {self.sort_column} {self.sort_direction}"
        
        match self.active_button_name:
            case "LIVROS":
                if search_text == "":
                    query = f"SELECT * FROM livros {order_clause}"
                else:
                    query = f"""
                        SELECT * FROM livros 
                        WHERE (livro LIKE %s OR autor LIKE %s OR genero LIKE %s OR ano LIKE %s OR editora LIKE %s OR sinopse LIKE %s)
                        {order_clause}
                    """
                    params = (like, like, like, like, like, like)

            case "USUÁRIOS":
                if search_text == "":
                    query = f"SELECT * FROM usuarios {order_clause}"
                else:
                    query = f"""
                        SELECT * FROM usuarios 
                        WHERE (nome LIKE %s OR tipo LIKE %s OR sala LIKE %s OR email LIKE %s OR telefone LIKE %s)
                        {order_clause}
                    """
                    params = (like, like, like, like, like)

            case "EMPRÉSTIMOS":
                if search_text == "":
                    query = f"SELECT * FROM emprestimos WHERE (status = 'Pendente' OR status = 'Atrasado') {order_clause}"
                else:
                    query = f"""
                        SELECT * FROM emprestimos 
                        WHERE (status = 'Pendente' OR status = 'Atrasado') AND (nome LIKE %s OR tipo LIKE %s OR livro LIKE %s OR data LIKE %s OR prazo LIKE %s)
                        {order_clause}
                    """
                    params = (like, like, like, like, like)

            case "DEVOLUÇÕES":
                if search_text == "":
                    query = f"SELECT * FROM emprestimos WHERE (status = 'Devolvido') {order_clause}"
                else:
                    query = f"""
                        SELECT * FROM emprestimos 
                        WHERE (status = 'Devolvido') AND (nome LIKE %s OR tipo LIKE %s OR livro LIKE %s OR data LIKE %s OR prazo LIKE %s)
                        {order_clause}
                    """
                    params = (like, like, like, like, like)
        
        if search_text == "":
            cursor.execute(query)
        else:
            cursor.execute(query, params)

        rows = cursor.fetchall()

        if cursor.description:
            raw_column_names = [desc[0] for desc in cursor.description]
            num_columns = len(raw_column_names)
        else:
             raw_column_names = []
             num_columns = 0

        display_headers = []
        for col in raw_column_names:
            if col.lower() == self.sort_column.lower():
                if self.sort_direction == "ASC":
                    display_headers.append(f"{col.upper()} ▲")
                else:
                    display_headers.append(f"{col.upper()} ▼")
            else:
                display_headers.append(col.upper())

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if len(rows) == 0:
            placeholder = ctk.CTkLabel(self.table_frame, text="Nenhum resultado encontrado.", text_color="gray", font=("Arial", 14, "bold"))
            placeholder.pack(pady=20)
            return

        table_values = [display_headers]
        for row in rows:
            table_values.append(list(row))

        table = CTkTable(master=self.table_frame, row=len(table_values), column=num_columns, values=table_values, command=self.on_table_click, header_color=BLUE_COLOR, text_color=TEXT_COLOR_WHITE, hover_color=BLUE_COLOR_HOVER)
        table.pack(expand=True, fill="both", padx=20, pady=20)

        match self.active_button_name:
            case "LIVROS":
                try:
                    col_names_lower = [c.lower() for c in raw_column_names]
                    quantidade_index = col_names_lower.index('quantidade')
                except ValueError:
                    quantidade_index = -1

                if quantidade_index != -1:
                    for i, row_data in enumerate(rows):
                        quantidade_valor = row_data[quantidade_index]

                        if quantidade_valor < 1:
                            row_visual_index = i + 1
                            
                            table.edit_row(row_visual_index, fg_color="#C53030", hover_color="#9B2C2C")
            case "EMPRÉSTIMOS":
                try:
                    col_names_lower = [c.lower() for c in raw_column_names]
                    status_index = col_names_lower.index('status')
                except ValueError:
                    status_index = -1

                if status_index != -1:
                    for i, row_data in enumerate(rows):
                        status_valor = row_data[status_index]

                        if status_valor == 'Atrasado':
                            row_visual_index = i + 1
                            
                            table.edit_row(row_visual_index, fg_color="#C53030", hover_color="#9B2C2C")

    

    def show_books(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((1, 2, 3, 4), weight=0)
        self.main_frame.grid_rowconfigure((0, 2, 3), weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.sort_column = "livro"
        self.sort_direction = "ASC"

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

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar... (ex: Dom Quixote)", border_width=0, fg_color="transparent", text_color=TEXT_COLOR_BLACK, height=30)
        self.search_entry.pack(side="left", expand=True, fill="x", ipady=5)
        self.search_entry.bind("<Return>", self.general_filter)

        filter_button = ctk.CTkButton(search_frame, text="⏷", fg_color="transparent", hover_color=DARK_PURPLE_COLOR, text_color="gray", width=10, font=("Arial", 16), command=None)
        filter_button.pack(side="right", padx=10)

        self.plus_button = ctk.CTkButton(top_frame, text="➕", width=40, height=40, corner_radius=25, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, command=self.add_book)
        self.plus_button.grid(row=0, column=2, sticky="e", padx=(25, 0))

        row_index += 1

        self.table_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.table_frame.grid(row=row_index, column=0, sticky="nsew", padx=25, pady=(0, 20))

        self.general_filter()

    def add_book(self):
        self.popup_book = ctk.CTkToplevel(self, fg_color="white")
        self.popup_book.title("Adicionar Livro")
        self.popup_book.minsize(250, 0)
        self.popup_book.resizable(False, False)
        self.popup_book.transient(self)
        self.popup_book.grab_set()

        self.popup_book.grid_columnconfigure(0, weight=1)
        self.popup_book.grid_columnconfigure((1, 2, 3, 4), weight=0)
        self.popup_book.grid_rowconfigure((0, 2), weight=0)
        self.popup_book.grid_rowconfigure((1, 3), weight=1)

        form_frame = ctk.CTkFrame(self.popup_book, fg_color="white")
        form_frame.grid(row=2, column=0, sticky="n", padx=20, pady=10)
        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)

        row_index = 0

        obs_label = ctk.CTkLabel(form_frame, text="Os campos com * são obrigatórios", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        obs_label.grid(row=row_index, column=1, ipady=5)

        row_index += 1

        book_label = ctk.CTkLabel(form_frame, text="*Nome: \n(ex: Dom Quixote):", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        book_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5), ipady=5)

        book_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        book_entry.grid(row=row_index, column=1, pady=(10, 5), ipady=5)

        row_index += 1

        author_label = ctk.CTkLabel(form_frame, text="*Autor \n(Miguel de Cervantes):", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        author_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        author_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        author_entry.grid(row=row_index, column=1, pady=(10, 5), ipady=5)

        row_index += 1

        genre_label = ctk.CTkLabel(form_frame, text="*Gênero \n(ex: Romance):", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        genre_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        genre_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        genre_entry.grid(row=row_index, column=1, pady=(10, 5), ipady=5)

        row_index += 1

        editora_label = ctk.CTkLabel(form_frame, text="*Editora \n(ex: Editora Garnier):", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        editora_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        editora_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        editora_entry.grid(row=row_index, column=1, pady=(10, 5), ipady=5)

        row_index += 1

        ano_label = ctk.CTkLabel(form_frame, text="*Ano: \n(ex: 1605)", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        ano_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        ano_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=59, corner_radius=25, validate="key", validatecommand=(form_frame.register(lambda P: len(P) <= 4), "%P"))
        ano_entry.grid(row=row_index, column=1, sticky="w", pady=(10, 5), ipady=5)

        row_index += 1

        quant_label = ctk.CTkLabel(form_frame, text="*Quantidade: \n(ex: 10)", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        quant_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        quant_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=53, corner_radius=25, validate="key", validatecommand=(form_frame.register(lambda P: len(P) <= 3), "%P"))
        quant_entry.grid(row=row_index, column=1, sticky="w", pady=(10, 5), ipady=5)

        row_index += 1

        sinop_label = ctk.CTkLabel(form_frame, text="Sinopse:", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        sinop_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        sinop_entry = ctk.CTkTextbox(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, height=100, corner_radius=25)
        sinop_entry.grid(row=row_index, column=1, pady=(10, 5), ipady=5)
        sinop_entry._textbox.configure(padx=0, pady=0, spacing1=0, spacing2=0, spacing3=0)

        row_index += 1

        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=row_index, column=1, columnspan=2, pady=(20, 10))

        cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=lambda: self.popup_book.destroy(), fg_color=BUTTON_NEUTRAL, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        cancel_button.grid(row=0, column=0, sticky="nsew", padx=10, pady=(0, 10))
        cancel_button.bind("<Enter>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        cancel_button.bind("<Leave>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=BUTTON_NEUTRAL))

        confirm_button = ctk.CTkButton(button_frame, text="Confirmar", command=lambda: self.add_book_to_db(book_entry, author_entry, genre_entry, ano_entry, editora_entry, quant_entry, sinop_entry), fg_color=LIGHT_COLOR, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        confirm_button.grid(row=0, column=1, sticky="nsew", padx=10, pady=(0, 10))
        confirm_button.bind("<Enter>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        confirm_button.bind("<Leave>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

    def show_users(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((1, 2, 3, 4), weight=0)
        self.main_frame.grid_rowconfigure((0, 2, 3), weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.sort_column = "nome"
        self.sort_direction = "ASC"

        row_index = 0

        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.grid(row=row_index, column=0, sticky="ew", padx=25, pady=(17, 15))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure((2, 3, 4), weight=0)

        title = ctk.CTkLabel(top_frame, text="USUÁRIOS", fg_color="transparent", text_color=TEXT_COLOR_BLACK, font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=(0, 20))

        search_frame = ctk.CTkFrame(top_frame, fg_color=LIGHT_PURPLE_COLOR, corner_radius=25)
        search_frame.grid(row=0, column=1, sticky="ew")

        search_icon = ctk.CTkLabel(search_frame, text="🔍", text_color="gray", font=("Arial", 16))
        search_icon.pack(side="left", padx=(10, 2))

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar... (ex: Guilherme Menezes Silva)", border_width=0, fg_color="transparent", text_color=TEXT_COLOR_BLACK, height=30)
        self.search_entry.pack(side="left", expand=True, fill="x", ipady=5)
        self.search_entry.bind("<Return>", self.general_filter)

        filter_button = ctk.CTkButton(search_frame, text="⏷", fg_color="transparent", hover_color=DARK_PURPLE_COLOR, text_color="gray", width=10, font=("Arial", 16), command=None)
        filter_button.pack(side="right", padx=10)

        self.remove_button = ctk.CTkButton(top_frame, text="❌", width=40, height=40, corner_radius=25, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, command=self.add_user)
        self.remove_button.grid(row=0, column=2, sticky="e", padx=(25, 12))

        self.edit_button = ctk.CTkButton(top_frame, text="✏", width=40, height=40, corner_radius=25, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, command=self.add_user)
        self.edit_button.grid(row=0, column=3, sticky="e", padx=(0, 0))

        self.plus_button = ctk.CTkButton(top_frame, text="➕", width=40, height=40, corner_radius=25, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, command=self.add_user)
        self.plus_button.grid(row=0, column=4, sticky="e", padx=(12, 0))

        row_index += 1

        self.table_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.table_frame.grid(row=row_index, column=0, sticky="nsew", padx=25, pady=(0, 20))

        self.general_filter()

    def add_user(self):
        self.popup_user = ctk.CTkToplevel(self, fg_color="white")
        self.popup_user.title("Adicionar Usuário")
        self.popup_user.minsize(250, 0)
        self.popup_user.resizable(False, False)
        self.popup_user.transient(self)
        self.popup_user.grab_set()

        self.popup_user.grid_columnconfigure(0, weight=1)
        self.popup_user.grid_columnconfigure((1, 2, 3, 4), weight=0)
        self.popup_user.grid_rowconfigure((0, 2), weight=0)
        self.popup_user.grid_rowconfigure((1, 3), weight=1)

        form_frame = ctk.CTkFrame(self.popup_user, fg_color="white")
        form_frame.grid(row=2, column=0, sticky="n", padx=20, pady=10)
        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)

        row_index = 0

        obs_label = ctk.CTkLabel(form_frame, text="Os campos com * são obrigatórios", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        obs_label.grid(row=row_index, column=1, ipady=5)

        row_index += 1

        name_label = ctk.CTkLabel(form_frame, text="*Nome completo: \n(ex: Guilherme Menezes Silva)", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        name_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5), ipady=5)

        nome_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        nome_entry.grid(row=row_index, column=1, pady=(10, 5), ipady=5)

        row_index += 1

        type_label = ctk.CTkLabel(form_frame, text="*Tipo de usuário: \n(ex: Aluno)", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        type_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5), ipady=5)

        type_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        type_frame.grid(row=row_index, column=1, sticky="w", pady=15)

        user_type = ctk.StringVar(value="Aluno")

        row_index += 1

        email_aluno_label = ctk.CTkLabel(form_frame, text="*RA: \n(ex: 1199887766)", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        email_aluno_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        general_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        general_entry.grid(row=row_index, column=1, pady=(10, 5), ipady=5)

        email_prof_label = ctk.CTkLabel(form_frame, text="*Email: \n(ex: guilherme@email.com)", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        email_prof_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))
        email_prof_label.grid_remove()

        row_index += 1

        room_label = ctk.CTkLabel(form_frame, text="*Série: \n(ex: 3TA)", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        room_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        room_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=53, corner_radius=25, validate="key", validatecommand=(form_frame.register(lambda P: len(P) <= 3), "%P"))
        room_entry.grid(row=row_index, column=1, sticky="w", pady=(10, 5), ipady=5)
        
        def toggle_fields():
            if user_type.get() == "Aluno":
                email_aluno_label.grid()
                room_label.grid()
                room_entry.grid()

                email_prof_label.grid_remove()

            else:
                email_aluno_label.grid_remove()
                room_label.grid_remove()
                room_entry.grid_remove()

                email_prof_label.grid()

        aluno_button = ctk.CTkRadioButton(type_frame, text="Aluno", variable=user_type, value="Aluno", command=toggle_fields, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, text_color=TEXT_COLOR_BLACK, font=("Arial", 11))
        aluno_button.pack(side="left")

        professor_button = ctk.CTkRadioButton(type_frame, text="Professor", variable=user_type, value="Professor", fg_color=BLUE_COLOR, command=toggle_fields, hover_color=BLUE_COLOR_HOVER, text_color=TEXT_COLOR_BLACK, font=("Arial", 11))
        professor_button.pack(side="left")

        row_index += 1

        telefone_label = ctk.CTkLabel(form_frame, text="Telefone: \n(ex: 11987654321)", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        telefone_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        telefone_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        telefone_entry.grid(row=row_index, column=1, pady=(10, 5), ipady=5)

        row_index += 1

        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=row_index, column=1, pady=(20, 10))

        cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=lambda: self.popup_user.destroy(), fg_color=BUTTON_NEUTRAL, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        cancel_button.grid(row=0, column=0, sticky="nsew", padx=10, pady=(0, 10))
        cancel_button.bind("<Enter>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        cancel_button.bind("<Leave>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=BUTTON_NEUTRAL))

        confirm_button = ctk.CTkButton(button_frame, text="Confirmar", command=lambda: self.add_user_to_db(nome_entry, user_type, general_entry, room_entry, telefone_entry), fg_color=LIGHT_COLOR, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        confirm_button.grid(row=0, column=1, sticky="nsew", padx=10, pady=(0, 10))
        confirm_button.bind("<Enter>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        confirm_button.bind("<Leave>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

    def show_loans(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((1, 2, 3, 4), weight=0)
        self.main_frame.grid_rowconfigure((0, 2, 3), weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.sort_column = "data"
        self.sort_direction = "DESC"

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

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar... (ex: 15112025)", border_width=0, fg_color="transparent", text_color=TEXT_COLOR_BLACK, height=30)
        self.search_entry.pack(side="left", expand=True, fill="x", ipady=5)
        self.search_entry.bind("<Return>", self.general_filter)

        filter_button = ctk.CTkButton(search_frame, text="⏷", fg_color="transparent", hover_color=DARK_PURPLE_COLOR, text_color="gray", width=10, font=("Arial", 16), command=None)
        filter_button.pack(side="right", padx=10)

        self.plus_button = ctk.CTkButton(top_frame, text="➕", width=40, height=40, corner_radius=25, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, command=self.make_loan)
        self.plus_button.grid(row=0, column=2, sticky="e", padx=(25, 0))

        row_index += 1

        self.table_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.table_frame.grid(row=row_index, column=0, sticky="nsew", padx=25, pady=(0, 20))

        self.general_filter()

    def make_loan(self):
        self.popup_loan = ctk.CTkToplevel(self, fg_color="white")
        self.popup_loan.title("Realizar Empréstimo")
        self.popup_loan.minsize(250, 0)
        self.popup_loan.resizable(False, False)
        self.popup_loan.transient(self)
        self.popup_loan.grab_set()

        self.popup_loan.grid_columnconfigure(0, weight=1)
        self.popup_loan.grid_columnconfigure((1, 2, 3, 4), weight=0)
        self.popup_loan.grid_rowconfigure((0, 2), weight=0)
        self.popup_loan.grid_rowconfigure((1, 3), weight=1)

        form_frame = ctk.CTkFrame(self.popup_loan, fg_color="white")
        form_frame.grid(row=2, column=0, sticky="n", padx=20, pady=10)
        form_frame.grid_columnconfigure(0, weight=0)
        form_frame.grid_columnconfigure(1, weight=1)

        row_index = 0

        obs_label = ctk.CTkLabel(form_frame, text="Os campos com * são obrigatórios", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        obs_label.grid(row=row_index, column=1, ipady=5)

        row_index += 1

        name_label = ctk.CTkLabel(form_frame, text="*Nome completo: \n(ex: Guilherme Menezes Silva)", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        name_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5), ipady=5)

        name_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        name_container.grid(row=row_index, column=1, pady=(10, 5))

        nome_entry = ctk.CTkEntry(name_container, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300,  corner_radius=25)
        nome_entry.pack(side="left", pady=(10, 5), ipady=5)

        btn_search_user = ctk.CTkButton(name_container, text="Buscar", width=50, corner_radius=25, fg_color=LIGHT_COLOR, text_color=TEXT_COLOR_BLACK, command=lambda: self.search_user_data(nome_entry, user_type, general_entry, toggle_fields))
        btn_search_user.pack(side="left", padx=(10, 0), pady=(10, 5), ipady=5)
        btn_search_user.bind("<Enter>", lambda e: btn_search_user.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        btn_search_user.bind("<Leave>", lambda e: btn_search_user.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

        row_index += 1

        type_label = ctk.CTkLabel(form_frame, text="*Tipo de usuário: \n(ex: Aluno)", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        type_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5), ipady=5)

        type_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        type_frame.grid(row=row_index, column=1, pady=15, sticky="w")

        user_type = ctk.StringVar(value="Aluno")

        row_index += 1

        email_aluno_label = ctk.CTkLabel(form_frame, text="*RA: \n(ex: 1125762433)", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        email_aluno_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        general_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        general_entry.grid(row=row_index, column=1, pady=(10, 5), ipady=5, sticky="w")

        email_prof_label = ctk.CTkLabel(form_frame, text="*Email: \n(ex: guilherme@email.com)", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        email_prof_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))
        email_prof_label.grid_remove()

        def toggle_fields():
            if user_type.get() == "Aluno":
                email_aluno_label.grid()
                email_prof_label.grid_remove()

            else:
                email_aluno_label.grid_remove()
                email_prof_label.grid()

        aluno_button = ctk.CTkRadioButton(type_frame, text="Aluno", variable=user_type, value="Aluno", command=toggle_fields, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, text_color=TEXT_COLOR_BLACK, font=("Arial", 11))
        aluno_button.pack(side="left")

        professor_button = ctk.CTkRadioButton(type_frame, text="Professor", variable=user_type, value="Professor", fg_color=BLUE_COLOR, command=toggle_fields, hover_color=BLUE_COLOR_HOVER, text_color=TEXT_COLOR_BLACK, font=("Arial", 11))
        professor_button.pack(side="left")

        row_index += 1        

        book_label = ctk.CTkLabel(form_frame, text="*Nome do Livro: \n(ex: Dom Quixote)", text_color="black", font=("Arial", 11, "bold"), anchor="w")
        book_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        book_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        book_container.grid(row=row_index, column=1, pady=(10, 5))

        book_entry = ctk.CTkEntry(book_container, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=300, corner_radius=25)
        book_entry.pack(side="left", pady=(10, 5), ipady=5)

        btn_search_book = ctk.CTkButton(book_container, text="Buscar", width=50, corner_radius=25, fg_color=LIGHT_COLOR, text_color=TEXT_COLOR_BLACK, command=lambda: self.search_book_data(book_entry))
        btn_search_book.pack(side="left", padx=(10, 0), pady=(10, 5), ipady=5)
        btn_search_book.bind("<Enter>", lambda e: btn_search_book.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        btn_search_book.bind("<Leave>", lambda e: btn_search_book.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

        row_index += 1

        quant_label = ctk.CTkLabel(form_frame, text="*Quantidade: \n(ex: 2)", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        quant_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        quant_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=53, corner_radius=25, validate="key", validatecommand=(form_frame.register(lambda P: len(P) <= 3), "%P"))
        quant_entry.grid(row=row_index, column=1, pady=(10, 5), ipady=5, sticky="w")

        row_index += 1

        date_label = ctk.CTkLabel(form_frame, text="*Data do Empréstimo: \n(ex: 15112025)", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        date_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        date_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=87, corner_radius=25, validate="key", validatecommand=(form_frame.register(lambda P: len(P) <= 8), "%P"))
        date_entry.grid(row=row_index, column=1, sticky="w", pady=(10, 5), ipady=5)
    
        row_index += 1

        due_label = ctk.CTkLabel(form_frame, text="*Prazo de Devolução: \n(ex: 25112025)", text_color=TEXT_COLOR_BLACK, font=("Arial", 11, "bold"), anchor="w")
        due_label.grid(row=row_index, column=0, padx=(0, 20), pady=(10, 5))

        due_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", text_color=TEXT_COLOR_BLACK, border_width=0, width=87, corner_radius=25, validate="key", validatecommand=(form_frame.register(lambda P: len(P) <= 8), "%P"))
        due_entry.grid(row=row_index, column=1, sticky="w", pady=(10, 5), ipady=5)

        row_index += 1

        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=row_index, column=1, columnspan=2, pady=(20, 10))

        cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=lambda: self.popup_loan.destroy(), fg_color=BUTTON_NEUTRAL, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        cancel_button.grid(row=0, column=0, sticky="nsew", padx=10, pady=(0, 10))
        cancel_button.bind("<Enter>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        cancel_button.bind("<Leave>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=BUTTON_NEUTRAL))

        confirm_button = ctk.CTkButton(button_frame, text="Confirmar", command=lambda: self.make_loan_to_db(nome_entry, user_type, general_entry, book_entry, quant_entry, date_entry, due_entry), fg_color=LIGHT_COLOR, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=75)
        confirm_button.grid(row=0, column=1, sticky="nsew", padx=10, pady=(0, 10))
        confirm_button.bind("<Enter>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        confirm_button.bind("<Leave>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

    def show_returns(self):
        self.clear_main_frame()

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure((1, 2, 3, 4), weight=0)
        self.main_frame.grid_rowconfigure((0, 2, 3), weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.sort_column = "nome"
        self.sort_direction = "ASC"

        row_index = 0

        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.grid(row=row_index, column=0, sticky="ew", padx=25, pady=(17.5, 15))
        top_frame.grid_columnconfigure(0, weight=0)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=0)

        title = ctk.CTkLabel(top_frame, text="DEVOLUÇÕES", fg_color="transparent", text_color=TEXT_COLOR_BLACK, font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, sticky="w", padx=(0, 20))

        search_frame = ctk.CTkFrame(top_frame, fg_color=LIGHT_PURPLE_COLOR, corner_radius=25)
        search_frame.grid(row=0, column=1, sticky="ew",)

        search_icon = ctk.CTkLabel(search_frame, text="🔍", text_color="gray", font=("Arial", 16))
        search_icon.pack(side="left", padx=(10, 2))

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar... (ex: 25112025)", border_width=0, fg_color="transparent", text_color=TEXT_COLOR_BLACK, height=30)
        self.search_entry.pack(side="left", expand=True, fill="x", ipady=5)
        self.search_entry.bind("<Return>", self.general_filter)

        filter_button = ctk.CTkButton(search_frame, text="⏷", fg_color="transparent", hover_color=DARK_PURPLE_COLOR, text_color="gray", width=10, font=("Arial", 16), command=None)
        filter_button.pack(side="right", padx=10)

        row_index += 1

        self.table_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="transparent")
        self.table_frame.grid(row=row_index, column=0, sticky="nsew", padx=25, pady=(0, 20))

        self.general_filter()

    def add_book_to_db(self, e_livro, e_autor, e_genero, e_ano, e_editora, e_quant, e_sinopse):
        livro = e_livro.get().strip()
        autor = e_autor.get().strip()
        genero = e_genero.get().strip()
        ano = e_ano.get().strip()
        editora = e_editora.get().strip()
        quantidade = e_quant.get().strip()
        sinopse = e_sinopse.get("0.0", "end").strip()

        if not livro or not autor or not genero or not ano or not editora or not quantidade:
            messagebox.showerror("Erro", "Por favor, preencha os campos obrigatórios (*).")
            return
        
        try:
            ano_int = int(ano)
            quant_int = int(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Ano e Quantidade devem ser números válidos.")
            return
        
        try:
            cursor = Database.sql.cursor()
            query = """
                INSERT INTO tb_livros (livro, autor, genero, ano, editora, quantidade, sinopse)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (livro, autor, genero, ano_int, editora, quant_int, sinopse)
            
            cursor.execute(query, values)
            Database.sql.commit()
            
            self.confirm_add("books")

        except Exception as e:
            messagebox.showerror("Erro no Banco de Dados", f"Não foi possível cadastrar o livro.\nErro: {e}")

    def add_user_to_db(self, e_nome, v_tipo, e_geral, e_sala, e_tel):
        nome = e_nome.get().strip()
        tipo = v_tipo.get()
        dado_geral = e_geral.get().strip()
        sala = e_sala.get().strip()
        telefone = e_tel.get().strip()

        if not nome or not dado_geral:
            messagebox.showerror("Erro", "Por favor, preencha os campos obrigatórios (*).")
            return
        
        if tipo == "Aluno":
            if not sala:
                messagebox.showerror("Erro", "Para alunos, a série é obrigatória.")
                return
        else:
            sala = None
        
        try:
            cursor = Database.sql.cursor()

            query = """
                INSERT INTO tb_usuarios (nome, tipo, sala, email, telefone)
                VALUES (%s, %s, %s, %s, %s)
            """
            values = (nome, tipo, sala, dado_geral, telefone)
            
            cursor.execute(query, values)
            Database.sql.commit()
            
            self.confirm_add("users") 

        except Exception as e:
            messagebox.showerror("Erro no Banco de Dados", f"Não foi possível cadastrar o usuário.\nErro: {e}")

    def make_loan_to_db(self, e_nome, v_tipo, e_geral, e_livro, e_quant, e_data, e_prazo):
        nome = e_nome.get().strip()
        tipo_selecionado = v_tipo.get()
        dado_geral = e_geral.get().strip()
        livro_nome = e_livro.get().strip()
        quantidade = e_quant.get().strip()
        data_str = e_data.get().strip()
        prazo_str = e_prazo.get().strip()

        if not nome or not dado_geral or not livro_nome or not quantidade or not data_str or not prazo_str:
            messagebox.showerror("Erro", "Por favor, preencha os campos obrigatórios (*).")
            return
        
        try:
            quant_int = int(quantidade)
            if quant_int <= 0:
                messagebox.showerror("Erro", "A quantidade deve ser maior que 0.")
                return

            if tipo_selecionado == "Aluno" and quant_int > 2:
                messagebox.showerror("Limite Excedido", "Alunos podem retirar no máximo 2 livros por vez.")
                return
            
            if tipo_selecionado == "Professor" and quant_int > 10:
                messagebox.showerror("Limite Excedido", "Professores podem retirar no máximo 10 livros por vez.")
                return
            data_fmt = datetime.strptime(data_str, "%d%m%Y").strftime("%Y-%m-%d")
            prazo_fmt = datetime.strptime(prazo_str, "%d%m%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Datas inválidas (use DDMMAAAA) ou quantidade inválida.")
            return
        
        try:
            cursor = Database.sql.cursor()

            query_user = "SELECT id_usa, tipo FROM tb_usuarios WHERE nome = %s AND email = %s"
            
            cursor.execute(query_user, (nome, dado_geral))
            user_res = cursor.fetchone()
            
            if not user_res:
                identificador = "RA" if tipo_selecionado == "Aluno" else "Email"
                messagebox.showerror("Erro", f"Usuário não encontrado.\nVerifique se o Nome e o {identificador} correspondem a um {tipo_selecionado}.")
                return
            
            id_usa, tipo_banco = user_res

            if tipo_banco != tipo_selecionado:
                messagebox.showerror("Fraude de Tipo", f"Conflito de dados:\nO usuário '{nome}' está cadastrado no banco como '{tipo_banco}', mas você selecionou '{tipo_selecionado}'.\n\nPor favor, selecione o tipo correto e respeite o limite de livros.")
                return
            
            id_usa = user_res[0]

            query_book = "SELECT id_liv, quantidade FROM tb_livros WHERE livro = %s"
            cursor.execute(query_book, (livro_nome,))
            book_res = cursor.fetchone()

            if not book_res:
                messagebox.showerror("Erro", f"Livro '{livro_nome}' não encontrado no acervo.")
                return
            
            id_liv, estoque_atual = book_res

            if quant_int > estoque_atual:
                messagebox.showerror("Estoque Insuficiente", f"Não há exemplares suficientes.\nEstoque atual: {estoque_atual}\nSolicitado: {quant_int}")
                return

            query_insert = """
                INSERT INTO tb_emprestimos (id_usa, id_liv, quantidade, data, prazo, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (id_usa, id_liv, quant_int, data_fmt, prazo_fmt, "Pendente")
            cursor.execute(query_insert, values)

            query_update_stock = "UPDATE tb_livros SET quantidade = quantidade - %s WHERE id_liv = %s"
            cursor.execute(query_update_stock, (quant_int, id_liv))

            Database.sql.commit()

            self.confirm_add("loans")

        except Exception as e:
            Database.sql.rollback()
            messagebox.showerror("Erro no Banco", f"Falha ao realizar empréstimo: {e}")

    def search_user_data(self, e_nome, v_tipo, e_geral, func_toggle):
        nome_busca = e_nome.get().strip()
        if not nome_busca:
            return

        try:
            cursor = Database.sql.cursor()
            
            query = "SELECT nome, tipo, email FROM tb_usuarios WHERE nome LIKE %s LIMIT 1"
            cursor.execute(query, (f"%{nome_busca}%",))
            result = cursor.fetchone()

            if result:
                nome_found, tipo_found, email_found = result

                e_nome.delete(0, "end")
                e_nome.insert(0, nome_found)
                
                v_tipo.set(tipo_found)
                
                func_toggle()

                e_geral.delete(0, "end")
                e_geral.insert(0, email_found)

            else:
                messagebox.showinfo("Busca", "Usuário não encontrado.")
        
        except Exception as e:
            print(f"Erro na busca: {e}")

    def search_book_data(self, e_livro):
        livro_busca = e_livro.get().strip()
        if not livro_busca:
            return

        try:
            cursor = Database.sql.cursor()
            query = "SELECT livro FROM tb_livros WHERE livro LIKE %s LIMIT 1"
            cursor.execute(query, (f"%{livro_busca}%",))
            result = cursor.fetchone()

            if result:
                e_livro.delete(0, "end")
                e_livro.insert(0, result[0])
            else:
                messagebox.showinfo("Busca", "Livro não encontrado.")

        except Exception as e:
            print(e)

    def close_screen(self):
        match self.active_button_name:
            case "USUÁRIOS":
                self.show_users()
            case "LIVROS":
                self.show_books()
            case "EMPRÉSTIMOS":
                self.show_loans()
            case "ADMINISTRAÇÃO":
                self.show_admin()
            case "DEVOLUÇÕES":
                self.show_returns()
            case _:
                self.show_admin()

    def confirm_add(self, func):
        popup = ctk.CTkToplevel(self, fg_color="white")
        popup.title("Dados adicionados ao Banco de Dados")
        popup.minsize(250, 0)
        popup.resizable(False, False)
        popup.transient(self)
        popup.grab_set()

        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=1)

        content_frame = ctk.CTkFrame(popup, fg_color="white", corner_radius=0)
        content_frame.pack(fill="both", expand=True)
        content_frame.grid_columnconfigure((0, 1), weight=1)

        popup_icon = ctk.CTkLabel(content_frame, text="➕", text_color=TEXT_COLOR_BLACK, font=("Arial", 60))
        popup_icon.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        popup_title = ctk.CTkLabel(content_frame, text="Os dados foram adicionados com sucesso! \nDeseja adicionar mais?", text_color=TEXT_COLOR_BLACK, font=("Arial", 14, "bold"), justify="center")
        popup_title.grid(row=1, column=0, columnspan=2, pady=(5, 20), padx=20)

        def confirm_and_close():
            popup.destroy()
            if func == "books":
                self.popup_book.destroy()
                self.close_screen()
            if func == "users":
                self.popup_user.destroy()
                self.close_screen()
            if func == "loans":
                self.popup_loan.destroy()
                self.close_screen()

        cancel_button = ctk.CTkButton(content_frame, text="Não", command=confirm_and_close, fg_color=LIGHT_COLOR, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=50)
        cancel_button.grid(row=2, column=0, padx=10, pady=(0, 25), sticky="e")
        cancel_button.bind("<Enter>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        cancel_button.bind("<Leave>", lambda e: cancel_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=LIGHT_COLOR))

        def confirm_and_reopen():
            popup.destroy()
            if func == "books":
                self.popup_book.destroy()
                self.add_book()
            if func == "users":
                self.popup_user.destroy()
                self.add_user()
            if func == "loans":
                self.popup_loan.destroy()
                self.make_loan()
            
        confirm_button = ctk.CTkButton(content_frame, text="Sim", command=confirm_and_reopen, fg_color=BUTTON_NEUTRAL, text_color=TEXT_COLOR_BLACK, corner_radius=25, width=50)
        confirm_button.grid(row=2, column=1, padx=10, pady=(0, 25), sticky="w")
        confirm_button.bind("<Enter>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_WHITE, fg_color=BLUE_COLOR_HOVER))
        confirm_button.bind("<Leave>", lambda e: confirm_button.configure(text_color=TEXT_COLOR_BLACK, fg_color=BUTTON_NEUTRAL))

        popup.update_idletasks()
        req_width = popup.winfo_reqwidth()
        req_height = popup.winfo_reqheight()
        x = self.winfo_x() + (self.winfo_width() // 2) - (req_width // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (req_height // 2)
        popup.geometry(f"{req_width}x{req_height}+{x}+{y}")
        
class DashboardLogin(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login Biblioteca")
        self.geometry("1280x720")
        self.minsize(854, 480)
        self.resizable(True, True)

        bg = ctk.CTkFrame(self, fg_color=BLUE_COLOR, corner_radius=0)
        bg.pack(fill="both", expand=True)

        frame = ctk.CTkFrame(bg, fg_color="white", corner_radius=25)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        window_title = ctk.CTkLabel(frame, text="Login da Biblioteca", text_color=TEXT_COLOR_BLACK, font=("Arial", 16, "bold"))
        window_title.pack(pady=(20, 10))

        user_label = ctk.CTkLabel(frame, text="Nome de Usuário", text_color="gray", anchor="w")
        user_label.pack(fill="x", padx=30)
        user_entry = ctk.CTkEntry(frame, corner_radius=25, fg_color="#f0f0f0", border_width=0, text_color=TEXT_COLOR_BLACK, font=("Arial", 11))
        user_entry.pack(fill="x", padx=30, pady=(0, 10), ipady=5)

        word_label = ctk.CTkLabel(frame, text="Senha", text_color="gray", anchor="w")
        word_label.pack(fill="x", padx=30)
        word_entry = ctk.CTkEntry(frame, corner_radius=25, fg_color="#f0f0f0", border_width=0, text_color=TEXT_COLOR_BLACK, font=("Arial", 11), show="*")
        word_entry.pack(fill="x", padx=30, pady=(0, 15), ipady=5)

        def error(wrong):
            error = ctk.CTkToplevel(self, fg_color=BLUE_COLOR)
            error.title("Login Biblioteca - Erro")            
            error.minsize(250, 0)
            error.resizable(False, False)
            error.transient(self)
            error.grab_set()

            error.grid_columnconfigure(0, weight=1)
            error.grid_rowconfigure(0, weight=1)

            content_frame = ctk.CTkFrame(error, fg_color="white", corner_radius=25)
            content_frame.pack(fill="both", expand=True, padx=10, pady=10)
            content_frame.grid_columnconfigure(0, weight=1)

            def close_error():
                error.destroy()

            if wrong == 1:
                error_title = ctk.CTkLabel(content_frame, text="Usuário incorreto.", text_color=TEXT_COLOR_BLACK, font=("Arial", 14, "bold"), justify="center")
                error_title.grid(row=0, column=0, pady=(17, 5), padx=15)
            elif wrong == 2:
                error_title = ctk.CTkLabel(content_frame, text="Senha incorreta.", text_color=TEXT_COLOR_BLACK, font=("Arial", 14, "bold"), justify="center")
                error_title.grid(row=0, column=0, pady=(17, 5), padx=15)
            elif wrong == 3:
                error_title = ctk.CTkLabel(content_frame, text="Preencha os campos obrigatórios.", text_color=TEXT_COLOR_BLACK, font=("Arial", 14, "bold"), justify="center")
                error_title.grid(row=0, column=0, pady=(17, 5), padx=15)
            elif wrong == 4:
                error_title = ctk.CTkLabel(content_frame, text="Usuário e senha incorretos.", text_color=TEXT_COLOR_BLACK, font=("Arial", 14, "bold"), justify="center")
                error_title.grid(row=0, column=0, pady=(17, 5), padx=15)

            try_again = ctk.CTkButton(content_frame, text="Tentar novamente", fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, corner_radius=25, text_color=TEXT_COLOR_WHITE, command=close_error)
            try_again.grid(row=1, column=0, ipady=5, ipadx=7, sticky="s", pady=(5, 20))

            error.update_idletasks()
            req_width = error.winfo_reqwidth()
            req_height = error.winfo_reqheight()
            x = self.winfo_x() + (self.winfo_width() // 2) - (req_width // 2)
            y = self.winfo_y() + (self.winfo_height() // 2) - (req_height // 2)
            error.geometry(f"{req_width}x{req_height}+{x}+{y}")

        def login():
            user = user_entry.get()
            password = word_entry.get()
            right = {user: "admin", password: "admin"}
            wrong = 0

            if user == right[user] and password == right[password]:
                self.withdraw()
                dashboard_app = DashboardApp(login_window=self)
                dashboard_app.mainloop()
            elif user != right[user] and password == right[password]:
                wrong = 1
                error(wrong)
            elif user == right[user] and password != right[password]:
                wrong = 2
                error(wrong)
            elif user == "" or password == "":
                wrong = 3
                error(wrong)
            else:
                wrong = 4
                error(wrong)

        enter_button = ctk.CTkButton(frame, text="Entrar", command=login, corner_radius=25, fg_color=BLUE_COLOR, hover_color=BLUE_COLOR_HOVER, text_color=TEXT_COLOR_WHITE, font=("Arial", 12, "bold"))
        enter_button.pack(pady=(5, 10), ipadx=10, ipady=5)

        footer_label = ctk.CTkLabel(frame, text="Apenas para Administradores", text_color="gray", font=("Arial", 9))
        footer_label.pack(pady=(0, 5))

        self.mainloop()

app = DashboardApp(login_window=None)
app.mainloop()