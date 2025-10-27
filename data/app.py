import customtkinter as ctk
from tkinter import messagebox
import os 

# ----------------------------------------------------
# --- CONFIGURAÇÕES E CLASSE DA TELA PRINCIPAL (DASHBOARDAPP) ---
# ----------------------------------------------------

# Inicializa tema
ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue")

# Cores usadas no aplicativo
YELLOW_COLOR = "#FFD700" 
HOVER_YELLOW_COLOR = "#E5C300"
BLUE_COLOR = "#0d6efd" 
HOVER_BLUE_COLOR = "#0b5ed7"
ACTIVE_TEXT_COLOR = "black" 
DARK_BLUE_STRIP_COLOR = "#0A5ACB" 
PURPLE_LIGHT = "#E6E0F9" 
PURPLE_DARK = "#D8CCF0" 
RED_CONFIRM = "#CC3300" # Cor para o botão de Confirmação no pop-up SAIR

# Cores dos cards de Gênero
GENRE_COLORS = {
    "Romance": "#FFC0CB",        
    "Aventura": "#FFA500",       
    "Fantasia": "#E0BBE4",       
    "Suspense/Thriller": "#A9A9A9", 
    "Ficção Científica": "#00CED1", 
    "Biografia/Auto biografia": "#3CB371" 
}

class DashboardApp(ctk.CTk):
    def __init__(self, login_window):
        super().__init__()

        self.login_window = login_window

        self.title("Sistema de Biblioteca - Administração")
        self.geometry("1000x700") 
        self.resizable(True, True)
        ctk.set_appearance_mode("Light")
        
        self.active_button_name = "ADMINISTRAÇÃO" 
        self.buttons = {} 
        self.sidebar_visible = True 
        self.filter_menu_visible = False 

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        
        self.action_menu_frame = None
        self.main_frame = None 
        self.filter_menu_frame = None
        self.setup_ui()
        
    def setup_ui(self):
        # 1. SIDEBAR (Painel Azul) - Coluna 0
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=BLUE_COLOR, width=200)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1) 

        # Botão (Topo) - O Back Arrow para recolher o Sidebar
        self.collapse_button = ctk.CTkButton(
            self.sidebar_frame, text="←", fg_color="transparent", hover_color=HOVER_BLUE_COLOR,
            font=("Arial", 24), width=20, command=self.toggle_sidebar
        )
        self.collapse_button.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # --- Botões de Navegação (Menu Lateral) ---
        self.buttons["ADMINISTRAÇÃO"] = self.create_sidebar_button("ADMINISTRAÇÃO", "📄", 1, self.show_dashboard)
        self.buttons["USUARIOS"] = self.create_sidebar_button("USUARIOS", "👤", 2, self.show_users)
        self.buttons["EMPRÉSTIMOS"] = self.create_sidebar_button("EMPRÉSTIMOS", "👥", 3, self.show_loans) 
        self.buttons["DEVOLUÇÕES"] = self.create_sidebar_button("DEVOLUÇÕES", "↩", 4, self.show_returns)
        self.buttons["LIVROS"] = self.create_sidebar_button("LIVROS", "📘", 5, self.show_books) 
        
        # O botão SAIR agora chama a função confirm_logout (pop-up)
        self.buttons["SAIR"] = self.create_sidebar_button("SAIR", "🚪", 7, self.confirm_logout) 
        
        # 2. FRAME PRINCIPAL (Conteúdo Branco) - Coluna 1
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="white")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20) 
        
        # --- FRAME PARA A FAIXA AZUL DA SETA DE EXPANDIR ---
        self.expand_button_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=DARK_BLUE_STRIP_COLOR, width=50)
        
        self.expand_button = ctk.CTkButton(
            self.expand_button_frame, text="→", fg_color="transparent", hover_color=HOVER_BLUE_COLOR,
            font=("Arial", 24), width=20, command=self.toggle_sidebar, text_color="white"
        )
        self.expand_button.place(relx=0.5, rely=0.5, anchor="center") 

        self.set_active_button(self.active_button_name) 
        self.show_dashboard() 

    # --- Métodos de UI e Comportamento ---
    
    def create_sidebar_button(self, text, symbol, row, command_func):
        """Cria um botão padronizado para o sidebar."""
        def wrapped_command():
            if text != "SAIR":
                self.set_active_button(text)
            command_func()

        button = ctk.CTkButton(
            self.sidebar_frame, text=f"{symbol} {text}", compound="left", anchor="w",
            corner_radius=10, fg_color="transparent", hover_color=HOVER_BLUE_COLOR,
            text_color="white", font=("Arial", 11, "bold"), command=wrapped_command
        )
        if text == "SAIR":
             button.grid(row=7, column=0, padx=10, pady=(20, 10), sticky="sw")
        else:
             button.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
        
        return button

    def set_active_button(self, name):
        """Define e colore o botão ativo para amarelo."""
        
        if self.active_button_name in self.buttons:
            old_button = self.buttons[self.active_button_name]
            old_button.configure(fg_color="transparent", text_color="white")
            if self.active_button_name != "SAIR":
                 # Reconecta os eventos de hover
                old_button.bind("<Enter>", lambda e: old_button.configure(fg_color=HOVER_BLUE_COLOR))
                old_button.bind("<Leave>", lambda e: old_button.configure(fg_color="transparent"))
            
        if name != "SAIR" and name in self.buttons:
            new_button = self.buttons[name]
            self.active_button_name = name
            
            new_button.configure(fg_color=YELLOW_COLOR, text_color=ACTIVE_TEXT_COLOR)
            # Desconecta os eventos de hover
            new_button.unbind("<Enter>")
            new_button.unbind("<Leave>")

    def toggle_sidebar(self):
        """Mostra/Esconde o sidebar e expande/recolhe o conteúdo."""
        
        if self.sidebar_visible:
            # 1. SIDEBAR ESTÁ VISÍVEL (Vamos ESCONDER)
            self.sidebar_frame.grid_forget()
            self.collapse_button.grid_forget()

            self.expand_button_frame.grid(row=0, column=0, sticky="nsew") 
            
            self.main_frame.grid_forget()
            self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20, columnspan=1)
            
            self.grid_columnconfigure(0, weight=0) 
            self.grid_columnconfigure(1, weight=1) 
            
            self.sidebar_visible = False

        else:
            # 2. SIDEBAR ESTÁ ESCONDIDO (Vamos MOSTRAR)
            
            self.expand_button_frame.grid_forget()
            
            self.grid_columnconfigure(0, weight=0)
            self.grid_columnconfigure(1, weight=1) 

            self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
            self.collapse_button.grid(row=0, column=0, padx=20, pady=20, sticky="w")
            
            self.main_frame.grid_forget()
            self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
            
            # RECARREGA A PÁGINA ATIVA
            if self.active_button_name == "ADMINISTRAÇÃO":
                self.show_dashboard()
            elif self.active_button_name == "USUARIOS":
                self.show_users()
            elif self.active_button_name == "EMPRÉSTIMOS":
                self.show_loans()
            elif self.active_button_name == "DEVOLUÇÕES":
                self.show_returns()
            elif self.active_button_name == "LIVROS":
                self.show_books() 
                
            self.sidebar_visible = True


    def clear_main_frame(self):
        """Limpa o frame principal e restaura a configuração padrão do grid."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
            
        if self.action_menu_frame:
            self.action_menu_frame.destroy()
            self.action_menu_frame = None
            
        if self.filter_menu_frame: 
            self.filter_menu_frame.destroy()
            self.filter_menu_frame = None
            self.filter_menu_visible = False
            
        for col in range(5): 
             self.main_frame.grid_columnconfigure(col, weight=0)
        for row in range(5): 
             self.main_frame.grid_rowconfigure(row, weight=0)

    def logout(self):
        """Fecha o dashboard e reabre a tela de login."""
        self.destroy()
        self.login_window.deiconify() 

    def confirm_logout(self):
        """Exibe um pop-up de confirmação para sair do aplicativo."""
        
        popup = ctk.CTkToplevel(self)
        popup.title("Sair")
        # Define um tamanho e centraliza o pop-up
        popup_width = 350
        popup_height = 250
        x = self.winfo_x() + (self.winfo_width() // 2) - (popup_width // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.transient(self) # Mantém o pop-up na frente
        popup.grab_set() # Bloqueia a interação com a janela principal
        
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=1)

        # Frame principal do pop-up
        content_frame = ctk.CTkFrame(popup, fg_color="white", corner_radius=15, border_color="#E0E0E0", border_width=1)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_columnconfigure((0, 1), weight=1)

        # Ícone (Porta - simplificado com texto)
        ctk.CTkLabel(content_frame, text="🚪", text_color="black", font=("Arial", 60)
                     ).grid(row=0, column=0, columnspan=2, pady=(10, 0))

        # Mensagem de Confirmação
        ctk.CTkLabel(content_frame, 
                     text="Tem certeza que deseja sair?", 
                     text_color="black", font=("Arial", 14, "bold"), justify="center"
                     ).grid(row=1, column=0, columnspan=2, pady=(10, 20), padx=20)
        
        # Botões
        # Botão Confirmar (Chama a função logout real)
        ctk.CTkButton(content_frame, text="Confirmar", command=self.logout, 
                      fg_color=RED_CONFIRM, hover_color="#B32B00", corner_radius=10, width=100
                      ).grid(row=2, column=0, padx=10, pady=(0, 10), sticky="e")
                      
        # Botão Cancelar (Apenas fecha o pop-up)
        ctk.CTkButton(content_frame, text="Cancelar", command=popup.destroy, 
                      fg_color="#e0e0e0", hover_color="#cccccc", text_color="black", corner_radius=10, width=100
                      ).grid(row=2, column=1, padx=10, pady=(0, 10), sticky="w")

    # --- Menu de Ações Flutuante (Amarelo) ---

    def toggle_action_menu(self):
        """Alterna a visibilidade do menu flutuante (ações rápidas)."""
        if self.action_menu_frame and self.action_menu_frame.winfo_ismapped():
            self.action_menu_frame.destroy()
            self.action_menu_frame = None
        else:
            self.show_action_menu()

    def show_action_menu(self):
        """Cria e posiciona o menu de ações flutuante (amarelo)."""
        if self.action_menu_frame:
            self.action_menu_frame.destroy()
        
        self.action_menu_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=10, border_width=2, border_color=YELLOW_COLOR)
        # Posiciona em relação ao canto inferior direito
        self.action_menu_frame.place(relx=0.98, rely=0.95, anchor="se") 
        
        # Usa show_add_loan()
        self.create_action_menu_button("ADICIONAR USUARIO", self.show_add_user).pack(pady=5, padx=10, fill="x")
        self.create_action_menu_button("ADICIONAR LIVRO", lambda: messagebox.showinfo("Ação", "Abrir tela de Adicionar Livro.")).pack(pady=5, padx=10, fill="x")
        self.create_action_menu_button("NOVO EMPRÉSTIMO", self.show_add_loan).pack(pady=5, padx=10, fill="x")

    def create_action_menu_button(self, text, command):
        """Cria um botão com o estilo amarelo para o menu de ações."""
        return ctk.CTkButton(
            self.action_menu_frame, text=text, command=command,
            fg_color=YELLOW_COLOR, hover_color=HOVER_YELLOW_COLOR, 
            text_color="black", corner_radius=10, font=("Arial", 11, "bold")
        )

    # --- PÁGINAS DE CONTEÚDO ---

    def show_dashboard(self):
        self.clear_main_frame()
        
        self.main_frame.grid_columnconfigure((0, 1, 2), weight=1) 
        self.main_frame.grid_rowconfigure(1, weight=0) 
        self.main_frame.grid_rowconfigure(2, weight=1) 
        
        titulo = ctk.CTkLabel(self.main_frame, text="ADMINISTRAÇÃO", text_color="black", font=("Arial", 20, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, padx=20, pady=(10, 30), sticky="w")
        
        # Cards de Informação
        self.create_dashboard_card("LIVROS CADASTRADOS", "📖", "---", 1, 0) 
        self.create_dashboard_card("USUÁRIOS", "👤", "---", 1, 1)
        self.create_dashboard_card("EMPRÉSTIMOS", "👥", "---", 1, 2)
        
        # Botão + (Ações rápidas)
        self.plus_button = ctk.CTkButton(
            self.main_frame, text="➕", width=40, height=40, corner_radius=25,
            fg_color=BLUE_COLOR, hover_color=HOVER_BLUE_COLOR, 
            command=self.toggle_action_menu
        )
        self.plus_button.grid(row=2, column=2, padx=20, pady=20, sticky="se")

    def create_dashboard_card(self, title, symbol, value, row, column):
        """Cria os cartões de informação."""
        card_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=15, border_width=1, border_color="#e0e0e0")
        card_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        
        icon_label = ctk.CTkLabel(card_frame, text=symbol, text_color=YELLOW_COLOR, font=("Arial", 48, "bold"), fg_color="transparent")
        icon_label.pack(pady=5)
        
        value_label = ctk.CTkLabel(card_frame, text=value, text_color="black", font=("Arial", 24, "bold"))
        value_label.pack(pady=5)
        
        title_label = ctk.CTkLabel(card_frame, text=title, text_color="gray", font=("Arial", 10))
        title_label.pack(pady=5)

    def show_users(self):
        self.clear_main_frame()
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1) 

        row_index = 0

        # 1. LINHA DE TÍTULO, BUSCA E BOTÃO DE ADICIONAR
        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.grid(row=row_index, column=0, sticky="ew", pady=(0, 20))
        top_frame.grid_columnconfigure(1, weight=1) 

        ctk.CTkLabel(top_frame, text="USUARIOS", text_color="black", font=("Arial", 20, "bold")
                      ).grid(row=0, column=0, sticky="w", padx=(0, 30))

        # Campo de Busca (LILÁS CLARO)
        search_frame = ctk.CTkFrame(top_frame, fg_color=PURPLE_LIGHT, corner_radius=10) 
        search_frame.grid(row=0, column=1, sticky="ew", padx=(10, 10))

        ctk.CTkLabel(search_frame, text="🔍", text_color="gray", font=("Arial", 16)
                      ).pack(side="left", padx=(10, 5), pady=5)
        
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar...", border_width=0, 
                                     fg_color="transparent", text_color="black")
        search_entry.pack(side="left", fill="x", expand=True, ipady=5)

        # Botão de Filtro - PADRONIZADO PARA ICONE '⏷'
        ctk.CTkButton(search_frame, text=" ⏷ ", fg_color="transparent", hover_color=PURPLE_DARK, 
                      text_color="gray", width=30, font=("Arial", 16),
                      command=lambda: messagebox.showinfo("Filtro", "Abrir filtro de Usuários.") 
                      ).pack(side="right", padx=(5, 5))
        
        # Botão Adicionar (o + no canto superior direito)
        ctk.CTkButton(top_frame, text="➕", fg_color=BLUE_COLOR, hover_color=HOVER_BLUE_COLOR, 
                      width=40, height=40, corner_radius=25, command=self.toggle_action_menu 
                      ).grid(row=0, column=2, sticky="e")

        row_index += 1
        
        # 2. CABEÇALHO DA TABELA 
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#F8F8F8", corner_radius=10)
        header_frame.grid(row=row_index, column=0, sticky="ew", pady=(0, 10))
        header_frame.grid_columnconfigure((0, 1, 2), weight=1) 

        headers = ["Nome", "Email", "Sala/Série"]
        for i, text in enumerate(headers):
            ctk.CTkLabel(header_frame, text=text, text_color="black", font=("Arial", 12, "bold")
                          ).grid(row=0, column=i, sticky="ew", padx=10, pady=10)

        row_index += 1

        # 3. CORPO DA TABELA (VAZIO)
        table_scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="white", corner_radius=10)
        table_scroll_frame.grid(row=row_index, column=0, sticky="nsew") 
        table_scroll_frame.grid_columnconfigure(0, weight=1) 
        
        ctk.CTkLabel(table_scroll_frame, text="NENHUM USUÁRIO CADASTRADO.\n(A tabela será populada pelo Banco de Dados)", 
                      text_color="gray", font=("Arial", 14, "bold")).pack(expand=True, padx=20, pady=100)

        row_index += 1

        # 4. PAGINAÇÃO (ESTÁTICA)
        pagination_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        pagination_frame.grid(row=row_index, column=0, sticky="s", pady=(20, 0))

        ctk.CTkButton(pagination_frame, text="← Anterior", fg_color="transparent", 
                      hover_color="#e0e0e0", text_color="gray"
                      ).pack(side="left", padx=5)

        ctk.CTkButton(pagination_frame, text="1", fg_color="black", hover_color="gray", width=30
                      ).pack(side="left", padx=5)
        
        ctk.CTkLabel(pagination_frame, text="...", text_color="gray").pack(side="left", padx=5)

        ctk.CTkButton(pagination_frame, text="Próximo →", fg_color="transparent", 
                      hover_color="#e0e0e0", text_color="gray"
                      ).pack(side="left", padx=5)

    def show_loans(self):
        self.clear_main_frame()
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1) 

        row_index = 0

        # 1. LINHA DE TÍTULO, BUSCA E BOTÃO DE ADICIONAR
        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.grid(row=row_index, column=0, sticky="ew", pady=(0, 20))
        top_frame.grid_columnconfigure(1, weight=1) 

        ctk.CTkLabel(top_frame, text="EMPRÉSTIMOS", text_color="black", font=("Arial", 20, "bold")
                      ).grid(row=0, column=0, sticky="w", padx=(0, 30))

        # Campo de Busca (LILÁS CLARO)
        search_frame = ctk.CTkFrame(top_frame, fg_color=PURPLE_LIGHT, corner_radius=10) 
        search_frame.grid(row=0, column=1, sticky="ew", padx=(10, 10))

        ctk.CTkLabel(search_frame, text="🔍", text_color="gray", font=("Arial", 16)
                      ).pack(side="left", padx=(10, 5), pady=5)
        
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar...", border_width=0, 
                                     fg_color="transparent", text_color="black")
        search_entry.pack(side="left", fill="x", expand=True, ipady=5)

        # Botão de Filtro - PADRONIZADO PARA ICONE '⏷'
        ctk.CTkButton(search_frame, text=" ⏷ ", fg_color="transparent", hover_color=PURPLE_DARK, 
                      text_color="gray", width=30, font=("Arial", 16),
                      command=lambda: messagebox.showinfo("Filtro", "Abrir filtro de Empréstimos.") 
                      ).pack(side="right", padx=(5, 5))
        
        # Botão Adicionar (o + no canto superior direito) - AGORA CHAMA show_add_loan
        ctk.CTkButton(top_frame, text="➕", fg_color=BLUE_COLOR, hover_color=HOVER_BLUE_COLOR, 
                      width=40, height=40, corner_radius=25, command=self.show_add_loan 
                      ).grid(row=0, column=2, sticky="e")

        row_index += 1
        
        # 2. CABEÇALHO DA TABELA 
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#F8F8F8", corner_radius=10)
        header_frame.grid(row=row_index, column=0, sticky="ew", pady=(0, 10))
        header_frame.grid_columnconfigure((0, 1, 2), weight=1) 

        headers = ["Nome", "Livro", "Data de Empréstimo"]
        for i, text in enumerate(headers):
            ctk.CTkLabel(header_frame, text=text, text_color="black", font=("Arial", 12, "bold")
                          ).grid(row=0, column=i, sticky="ew", padx=10, pady=10)

        row_index += 1

        # 3. CORPO DA TABELA (VAZIO)
        table_scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="white", corner_radius=10)
        table_scroll_frame.grid(row=row_index, column=0, sticky="nsew") 
        table_scroll_frame.grid_columnconfigure(0, weight=1) 
        
        ctk.CTkLabel(table_scroll_frame, text="NENHUM EMPRÉSTIMO CADASTRADO.\n(A tabela será populada pelo Banco de Dados)", 
                      text_color="gray", font=("Arial", 14, "bold")).pack(expand=True, padx=20, pady=100)

        row_index += 1

        # 4. PAGINAÇÃO (ESTÁTICA)
        pagination_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        pagination_frame.grid(row=row_index, column=0, sticky="s", pady=(20, 0))

        ctk.CTkButton(pagination_frame, text="← Anterior", fg_color="transparent", 
                      hover_color="#e0e0e0", text_color="gray"
                      ).pack(side="left", padx=5)

        ctk.CTkButton(pagination_frame, text="1", fg_color="black", hover_color="gray", width=30
                      ).pack(side="left", padx=5)
        
        ctk.CTkLabel(pagination_frame, text="2", text_color="gray").pack(side="left", padx=5)
        ctk.CTkLabel(pagination_frame, text="3", text_color="gray").pack(side="left", padx=5)
        ctk.CTkLabel(pagination_frame, text="...", text_color="gray").pack(side="left", padx=5)

        ctk.CTkButton(pagination_frame, text="Próximo →", fg_color="transparent", 
                      hover_color="#e0e0e0", text_color="gray"
                      ).pack(side="left", padx=5)

    def show_returns(self):
        self.clear_main_frame()
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1) 

        row_index = 0

        # 1. LINHA DE TÍTULO, BUSCA E BOTÃO DE ADICIONAR
        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.grid(row=row_index, column=0, sticky="ew", pady=(0, 20))
        top_frame.grid_columnconfigure(1, weight=1) 

        ctk.CTkLabel(top_frame, text="DEVOLUÇÕES", text_color="black", font=("Arial", 20, "bold")
                      ).grid(row=0, column=0, sticky="w", padx=(0, 30))

        # Campo de Busca (LILÁS CLARO)
        search_frame = ctk.CTkFrame(top_frame, fg_color=PURPLE_LIGHT, corner_radius=10) 
        search_frame.grid(row=0, column=1, sticky="ew", padx=(10, 10))

        ctk.CTkLabel(search_frame, text="🔍", text_color="gray", font=("Arial", 16)
                      ).pack(side="left", padx=(10, 5), pady=5)
        
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar...", border_width=0, 
                                     fg_color="transparent", text_color="black")
        search_entry.pack(side="left", fill="x", expand=True, ipady=5)

        # Botão de Filtro - PADRONIZADO PARA ICONE '⏷'
        ctk.CTkButton(search_frame, text=" ⏷ ", fg_color="transparent", hover_color=PURPLE_DARK, 
                      text_color="gray", width=30, font=("Arial", 16),
                      command=lambda: messagebox.showinfo("Filtro", "Abrir filtro de Devoluções.") 
                      ).pack(side="right", padx=(5, 5))
        
        # Não há botão de '+' nesta tela no seu design

        row_index += 1
        
        # 2. CABEÇALHO DA TABELA 
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#F8F8F8", corner_radius=10)
        header_frame.grid(row=row_index, column=0, sticky="ew", pady=(0, 10))
        header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1) 

        headers = ["Usuário", "Livro", "Devolução", "Ação"]
        for i, text in enumerate(headers):
            ctk.CTkLabel(header_frame, text=text, text_color="black", font=("Arial", 12, "bold")
                          ).grid(row=0, column=i, sticky="ew", padx=10, pady=10)

        row_index += 1

        # 3. CORPO DA TABELA (VAZIO)
        table_scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="white", corner_radius=10)
        table_scroll_frame.grid(row=row_index, column=0, sticky="nsew") 
        table_scroll_frame.grid_columnconfigure(0, weight=1) 
        
        ctk.CTkLabel(table_scroll_frame, text="NENHUMA DEVOLUÇÃO PENDENTE.\n(A tabela será populada pelo Banco de Dados)", 
                      text_color="gray", font=("Arial", 14, "bold")).pack(expand=True, padx=20, pady=100)

        row_index += 1 

        # 4. PAGINAÇÃO (ESTÁTICA)
        pagination_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        pagination_frame.grid(row=row_index, column=0, sticky="s", pady=(20, 0))

        ctk.CTkButton(pagination_frame, text="← Anterior", fg_color="transparent", 
                      hover_color="#e0e0e0", text_color="gray"
                      ).pack(side="left", padx=5)

        ctk.CTkButton(pagination_frame, text="1", fg_color="black", hover_color="gray", width=30
                      ).pack(side="left", padx=5)
        
        ctk.CTkLabel(pagination_frame, text="2", text_color="gray").pack(side="left", padx=5)
        ctk.CTkLabel(pagination_frame, text="3", text_color="gray").pack(side="left", padx=5)
        ctk.CTkLabel(pagination_frame, text="...", text_color="gray").pack(side="left", padx=5)

        ctk.CTkButton(pagination_frame, text="Próximo →", fg_color="transparent", 
                      hover_color="#e0e0e0", text_color="gray"
                      ).pack(side="left", padx=5)
                      
    # --- Menu de Filtros de Livro ---
    
    def toggle_filter_menu(self):
        """Alterna a visibilidade do menu de filtros (Titúlo, Autor, Gênero)."""
        if self.filter_menu_visible:
            self.filter_menu_frame.destroy()
            self.filter_menu_frame = None
            self.filter_menu_visible = False
        else:
            self.show_filter_menu()

    def show_filter_menu(self):
        """Cria e posiciona o menu de filtros dos livros."""
        if self.filter_menu_frame:
            self.filter_menu_frame.destroy()
            
        self.filter_menu_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=10, border_width=1, border_color="#E0E0E0")
        
        self.filter_menu_frame.place(relx=0.97, rely=0.17, anchor="ne") 

        # Cria os botões de filtro
        self.create_filter_button(self.filter_menu_frame, "FILTRAR POR TITULO", lambda: messagebox.showinfo("Filtro", "Aplicar filtro por Título.")).pack(pady=3, padx=10, fill="x")
        self.create_filter_button(self.filter_menu_frame, "FILTRAR POR AUTOR", lambda: messagebox.showinfo("Filtro", "Aplicar filtro por Autor.")).pack(pady=3, padx=10, fill="x")
        self.create_filter_button(self.filter_menu_frame, "FILTRAR POR GÊNERO", lambda: messagebox.showinfo("Filtro", "Aplicar filtro por Gênero.")).pack(pady=3, padx=10, fill="x")
        
        self.filter_menu_visible = True

    def create_filter_button(self, parent_frame, text, command):
        """Cria um botão com o estilo amarelo para o menu de filtros."""
        return ctk.CTkButton(
            parent_frame, text=text, command=command,
            fg_color=YELLOW_COLOR, hover_color=HOVER_YELLOW_COLOR, 
            text_color="black", corner_radius=5, font=("Arial", 10, "bold")
        )

    # ------------------------------------------------------------------
    # --- PÁGINA DE GÊNEROS (Chamada principal do botão "LIVROS") ---
    # ------------------------------------------------------------------
    def show_books(self):
        """Exibe a tela de Gêneros (os cards coloridos)."""
        self.clear_main_frame()
        
        self.main_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        # Título
        title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(10, 30), padx=20)
        title_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(title_frame, text="📖 Gêneros", text_color="black", font=("Arial", 20, "bold")
                      ).grid(row=0, column=0, sticky="w")
        
        search_frame = ctk.CTkFrame(title_frame, fg_color="white", corner_radius=10, border_color="#E0E0E0", border_width=1)
        search_frame.grid(row=0, column=2, sticky="e")
        
        ctk.CTkLabel(search_frame, text="🔍 Adicionar novo gênero", text_color="gray", font=("Arial", 11)
                     ).pack(padx=10, pady=5)
        
        # Frame de Cards
        cards_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        cards_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        cards_frame.grid_rowconfigure((0, 1), weight=1)
        
        # Dados dos Cards (Conforme imagem)
        genre_data = [
            ("Romance", "Histórias centradas em relações amorosas e emoção", "❤"),
            ("Aventura", "Histórias cheias de ação, desafios e exploração", "🧭"),
            ("Fantasia", "Mundos imaginários, magia e seres fantásticos", "✨"),
            ("Suspense/Thriller", "Histórias que prendem a atenção com mistérios e tensão", "🔍"),
            ("Ficção Científica", "Tecnologia, viagens espaciais e universos alternativos", "✈"),
            ("Biografia/Auto biografia", "Histórias da vida real de pessoas inspiradoras", "👤")
        ]
        
        # Criação dos Cards
        for i, (genre, description, icon) in enumerate(genre_data):
            row = i // 3
            col = i % 3
            
            command_func = lambda g=genre: self.show_books_table(g)
            
            self.create_genre_card(
                parent_frame=cards_frame, 
                title=genre, 
                description=description, 
                icon=icon, 
                color=GENRE_COLORS.get(genre, "#D3D3D3"), 
                row=row, 
                column=col,
                command=command_func
            )

    def create_genre_card(self, parent_frame, title, description, icon, color, row, column, command):
        """Cria um cartão de gênero clicável."""
        card = ctk.CTkButton(
            parent_frame, 
            text=f"{icon}\n{title}", 
            command=command, 
            fg_color=color, 
            hover_color=color, 
            text_color="black",
            corner_radius=15, 
            compound="top",
            font=("Arial", 14, "bold"),
            anchor="center",
            width=200, height=150
        )
        card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        
        desc_label = ctk.CTkLabel(
            card, 
            text=description, 
            text_color="gray", 
            font=("Arial", 9),
            wraplength=180, 
            justify="center",
            fg_color="transparent"
        )
        desc_label.place(relx=0.5, rely=0.75, anchor="center") 
        
        # Adiciona um efeito de hover mais sutil
        card.bind("<Enter>", lambda e: card.configure(fg_color="#e0e0e0" if color == "#A9A9A9" else color))
        card.bind("<Leave>", lambda e: card.configure(fg_color=color))


    # ------------------------------------------------------------------
    # --- TABELA DE LIVROS (Anteriormente 'show_books', agora chamada por Gênero) ---
    # ------------------------------------------------------------------
    def show_books_table(self, filter_genre=None):
        """Exibe a tabela de Livros."""
        self.clear_main_frame()
        
        self.set_active_button("LIVROS") 
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1) 

        row_index = 0

        # 1. LINHA DE TÍTULO, BUSCA E BOTÃO DE ADICIONAR
        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.grid(row=row_index, column=0, sticky="ew", pady=(0, 20))
        top_frame.grid_columnconfigure(1, weight=1) 

        # Título
        title_text = f"LIVROS ({filter_genre.upper()})" if filter_genre else "LIVROS"
        ctk.CTkLabel(top_frame, text=title_text, text_color="black", font=("Arial", 20, "bold")
                      ).grid(row=0, column=0, sticky="w", padx=(0, 30))

        # Campo de Busca (LILÁS CLARO)
        search_frame = ctk.CTkFrame(top_frame, fg_color=PURPLE_LIGHT, corner_radius=10) 
        search_frame.grid(row=0, column=1, sticky="ew", padx=(10, 10))

        ctk.CTkLabel(search_frame, text="🔍", text_color="gray", font=("Arial", 16)
                      ).pack(side="left", padx=(10, 5), pady=5)
        
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="Buscar...", border_width=0, 
                                     fg_color="transparent", text_color="black")
        search_entry.pack(side="left", fill="x", expand=True, ipady=5)
        
        # Botão de Filtro (abre o menu flutuante)
        ctk.CTkButton(search_frame, text=" ⏷ ", fg_color="transparent", hover_color=PURPLE_DARK, 
                      text_color="gray", width=30, font=("Arial", 16), 
                      command=self.toggle_filter_menu 
                      ).pack(side="right", padx=(5, 5))
        
        # Botão Adicionar (o + no canto superior direito)
        ctk.CTkButton(top_frame, text="➕", fg_color=BLUE_COLOR, hover_color=HOVER_BLUE_COLOR, 
                      width=40, height=40, corner_radius=25, command=self.toggle_action_menu
                      ).grid(row=0, column=2, sticky="e")

        row_index += 1
        
        # 2. CABEÇALHO DA TABELA 
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="#F8F8F8", corner_radius=10)
        header_frame.grid(row=row_index, column=0, sticky="ew", pady=(0, 10))
        header_frame.grid_columnconfigure((0, 1, 2), weight=1) 

        headers = ["TÍTULO", "AUTOR", "GÊNERO"]
        for i, text in enumerate(headers):
            ctk.CTkLabel(header_frame, text=text, text_color="black", font=("Arial", 12, "bold")
                          ).grid(row=0, column=i, sticky="ew", padx=10, pady=10)

        row_index += 1

        # 3. CORPO DA TABELA (COM AVISO DE FILTRO ATIVO)
        table_scroll_frame = ctk.CTkScrollableFrame(self.main_frame, fg_color="white", corner_radius=10)
        table_scroll_frame.grid(row=row_index, column=0, sticky="nsew") 
        table_scroll_frame.grid_columnconfigure(0, weight=1) 
        
        if filter_genre:
            table_message = f"Exibindo livros do gênero: {filter_genre.upper()}.\n(A tabela será populada pelo Banco de Dados)"
        else:
            table_message = "NENHUM LIVRO CADASTRADO.\n(A tabela será populada pelo Banco de Dados)"
            
        ctk.CTkLabel(table_scroll_frame, text=table_message, 
                      text_color="gray", font=("Arial", 14, "bold")).pack(expand=True, padx=20, pady=100)

        row_index += 1

        # 4. PAGINAÇÃO (ESTÁTICA)
        pagination_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        pagination_frame.grid(row=row_index, column=0, sticky="s", pady=(20, 0))

        ctk.CTkButton(pagination_frame, text="← Anterior", fg_color="transparent", 
                      hover_color="#e0e0e0", text_color="gray"
                      ).pack(side="left", padx=5)

        ctk.CTkButton(pagination_frame, text="1", fg_color="black", hover_color="gray", width=30
                      ).pack(side="left", padx=5)
        
        ctk.CTkLabel(pagination_frame, text="2", text_color="gray").pack(side="left", padx=5)
        ctk.CTkLabel(pagination_frame, text="3", text_color="gray").pack(side="left", padx=5)
        ctk.CTkLabel(pagination_frame, text="...", text_color="gray").pack(side="left", padx=5)

        ctk.CTkButton(pagination_frame, text="Próximo →", fg_color="transparent", 
                      hover_color="#e0e0e0", text_color="gray"
                      ).pack(side="left", padx=5)

    # ------------------------------------------------------------------
    # --- PÁGINA: ADICIONAR USUÁRIO ---
    # ------------------------------------------------------------------
    
    def show_add_user(self):
        """Exibe a tela de cadastro de novo usuário."""
        self.clear_main_frame()
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1) 
        
        # Título da tela
        ctk.CTkLabel(self.main_frame, text="ADICIONAR USUARIO", text_color="black", font=("Arial", 20, "bold")
                      ).grid(row=0, column=0, sticky="w", padx=20, pady=(10, 30))
        
        # Frame de Conteúdo para os formulários (centralizado)
        form_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        form_frame.grid(row=1, column=0, sticky="n", padx=20, pady=10)
        
        # Grid para os elementos do formulário (2 colunas: Label e Campo)
        form_frame.grid_columnconfigure(0, weight=0) # Labels
        form_frame.grid_columnconfigure(1, weight=1) # Entries
        
        row_index = 0
        
        # 1. Nome Completo
        ctk.CTkLabel(form_frame, text="Nome Completo:", text_color="black", font=("Arial", 11, "bold"), anchor="w"
                     ).grid(row=row_index, column=0, sticky="w", padx=(0, 20), pady=(10, 5))
        
        self.nome_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", border_width=0, width=300, corner_radius=10)
        self.nome_entry.grid(row=row_index, column=1, sticky="ew", pady=(10, 5), ipady=5)
        row_index += 1
        
        # 2. Tipo (Radio Buttons)
        ctk.CTkLabel(form_frame, text="Tipo:", text_color="black", font=("Arial", 11, "bold"), anchor="w"
                     ).grid(row=row_index, column=0, sticky="w", padx=(0, 20), pady=(10, 5))
        
        type_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        type_frame.grid(row=row_index, column=1, sticky="w", pady=(10, 15))
        
        self.user_type_var = ctk.StringVar(value="Aluno") # Valor padrão "Aluno"
        
        ctk.CTkRadioButton(type_frame, text="Professor", variable=self.user_type_var, value="Professor", 
                           fg_color=BLUE_COLOR, hover_color=HOVER_BLUE_COLOR, text_color="black", font=("Arial", 11)
                           ).pack(side="left", padx=(0, 30))
                           
        ctk.CTkRadioButton(type_frame, text="Aluno", variable=self.user_type_var, value="Aluno", 
                           fg_color=BLUE_COLOR, hover_color=HOVER_BLUE_COLOR, text_color="black", font=("Arial", 11)
                           ).pack(side="left")
        row_index += 1
        
        # 3. E-mail Institucional (RA)
        ctk.CTkLabel(form_frame, text="E-mail Institucional (RA):", text_color="black", font=("Arial", 11, "bold"), anchor="w"
                     ).grid(row=row_index, column=0, sticky="w", padx=(0, 20), pady=(10, 5))
        
        self.email_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", border_width=0, width=300, corner_radius=10)
        self.email_entry.grid(row=row_index, column=1, sticky="ew", pady=(10, 5), ipady=5)
        row_index += 1
        
        # 4. Série/Sala
        ctk.CTkLabel(form_frame, text="Série/Sala:", text_color="black", font=("Arial", 11, "bold"), anchor="w"
                     ).grid(row=row_index, column=0, sticky="w", padx=(0, 20), pady=(10, 5))
        
        self.serie_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", border_width=0, width=150, corner_radius=10)
        self.serie_entry.grid(row=row_index, column=1, sticky="w", pady=(10, 20), ipady=5)
        row_index += 1
        
        # Frame de Botões (Cadastrar e Cancelar)
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=row_index, column=1, sticky="e", pady=(20, 10))
        
        # Botão Cancelar
        ctk.CTkButton(button_frame, text="Cancelar", command=self.show_users, 
                      fg_color="#e0e0e0", hover_color="#cccccc", text_color="black", corner_radius=10
                      ).pack(side="left", padx=(0, 10))
                      
        # Botão Cadastrar
        ctk.CTkButton(button_frame, text="Cadastrar", command=self.confirm_add_user,
                      fg_color=BLUE_COLOR, hover_color=HOVER_BLUE_COLOR, text_color="white", corner_radius=10
                      ).pack(side="left")

    def confirm_add_user(self):
        """Mostra um pop-up de confirmação para o cadastro de usuário."""
        
        popup = ctk.CTkToplevel(self)
        popup.title("Confirmação")
        popup_width = 300
        popup_height = 180
        x = self.winfo_x() + (self.winfo_width() // 2) - (popup_width // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (popup_height // 2)
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.transient(self) 
        popup.grab_set() 
        
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=1)
        
        content_frame = ctk.CTkFrame(popup, fg_color="white", corner_radius=15, border_color="#E0E0E0", border_width=1)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        content_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Mensagem
        ctk.CTkLabel(content_frame, 
                     text="TEM CERTEZA QUE\nDESEJA CADASTRAR O\nNOVO USUARIO?", 
                     text_color="black", font=("Arial", 12, "bold"), justify="center"
                     ).grid(row=0, column=0, columnspan=2, pady=(20, 15), padx=20)
        
        # Botão SIM (Cadastra e fecha tudo)
        def action_yes():
            popup.destroy()
            self.show_users() 
            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso! (Simulação)")

        # Botão NÃO (Apenas fecha o pop-up)
        def action_no():
            popup.destroy()

        # Botões SIM e NÃO
        ctk.CTkButton(content_frame, text="SIM", command=action_yes, 
                      fg_color=BLUE_COLOR, hover_color=HOVER_BLUE_COLOR, corner_radius=10, width=80
                      ).grid(row=1, column=0, padx=10, pady=(0, 10))
                      
        ctk.CTkButton(content_frame, text="NÃO", command=action_no, 
                      fg_color="#e0e0e0", hover_color="#cccccc", text_color="black", corner_radius=10, width=80
                      ).grid(row=1, column=1, padx=10, pady=(0, 10))

    # ------------------------------------------------------------------
    # --- NOVA PÁGINA: ADICIONAR EMPRÉSTIMO ---
    # ------------------------------------------------------------------

    def show_add_loan(self):
        """Exibe a tela de cadastro de novo empréstimo."""
        self.clear_main_frame()
        self.set_active_button("EMPRÉSTIMOS") 
        
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1) 
        
        # Título da tela
        ctk.CTkLabel(self.main_frame, text="ADICIONAR EMPRÉSTIMO", text_color="black", font=("Arial", 20, "bold")
                      ).grid(row=0, column=0, sticky="w", padx=20, pady=(10, 30))
        
        # Frame de Conteúdo para os formulários (centralizado)
        form_frame = ctk.CTkFrame(self.main_frame, fg_color="white", corner_radius=15, border_color="#E0E0E0", border_width=1)
        form_frame.grid(row=1, column=0, sticky="n", padx=20, pady=10)
        
        # Grid para os elementos do formulário (1 coluna para os campos, 2 para as datas e botões)
        form_frame.grid_columnconfigure((0, 1), weight=1)
        
        row_index = 0
        
        # 1. E-mail institucional do usuário
        ctk.CTkLabel(form_frame, text="E-mail institucional do usuário:", text_color="gray", font=("Arial", 11), anchor="w"
                     ).grid(row=row_index, column=0, columnspan=2, sticky="w", padx=20, pady=(15, 5))
        
        self.email_loan_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", border_width=0, width=400, corner_radius=10)
        self.email_loan_entry.grid(row=row_index + 1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15), ipady=5)
        row_index += 2
        
        # 2. Livro
        ctk.CTkLabel(form_frame, text="Livro:", text_color="gray", font=("Arial", 11), anchor="w"
                     ).grid(row=row_index, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 5))
        
        self.livro_loan_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", border_width=0, width=400, corner_radius=10)
        self.livro_loan_entry.grid(row=row_index + 1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15), ipady=5)
        row_index += 2
        
        # 3. Quantidade de livros
        ctk.CTkLabel(form_frame, text="Quantidade de livros:", text_color="gray", font=("Arial", 11), anchor="w"
                     ).grid(row=row_index, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 5))
        
        self.quantidade_loan_entry = ctk.CTkEntry(form_frame, fg_color="#f0f0f0", border_width=0, width=400, corner_radius=10)
        self.quantidade_loan_entry.grid(row=row_index + 1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15), ipady=5)
        row_index += 2
        
        # 4. Datas (Empréstimo e Devolução)
        
        # Data de empréstimo
        ctk.CTkLabel(form_frame, text="Data de empréstimo:", text_color="gray", font=("Arial", 11), anchor="w"
                     ).grid(row=row_index, column=0, sticky="w", padx=20, pady=(0, 5))
        
        self.data_emprestimo_entry = ctk.CTkEntry(form_frame, placeholder_text="dd/mm/aaaa", fg_color="#f0f0f0", border_width=0, width=150, corner_radius=10)
        self.data_emprestimo_entry.grid(row=row_index + 1, column=0, sticky="ew", padx=20, pady=(0, 20), ipady=5)
        
        # Data de devolução
        ctk.CTkLabel(form_frame, text="Data de devolução:", text_color="gray", font=("Arial", 11), anchor="w"
                     ).grid(row=row_index, column=1, sticky="w", padx=20, pady=(0, 5))
        
        self.data_devolucao_entry = ctk.CTkEntry(form_frame, placeholder_text="dd/mm/aaaa", fg_color="#f0f0f0", border_width=0, width=150, corner_radius=10)
        self.data_devolucao_entry.grid(row=row_index + 1, column=1, sticky="ew", padx=20, pady=(0, 20), ipady=5)
        
        row_index += 2
        
        # Frame de Botões (Confirmar e Cancelar)
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.grid(row=row_index, column=0, columnspan=2, sticky="s", pady=(20, 20))
        
        # Botão Confirmar
        ctk.CTkButton(button_frame, text="Confirmar", command=self.confirm_add_loan,
                      fg_color=BLUE_COLOR, hover_color=HOVER_BLUE_COLOR, text_color="white", corner_radius=10, width=120
                      ).pack(side="left", padx=10)
                      
        # Botão Cancelar
        ctk.CTkButton(button_frame, text="Cancelar", command=self.show_loans, 
                      fg_color="#e0e0e0", hover_color="#cccccc", text_color="black", corner_radius=10, width=120
                      ).pack(side="left", padx=10)

    def confirm_add_loan(self):
        """Mostra um pop-up de confirmação para o cadastro de empréstimo."""
        # Esta função pode ser elaborada futuramente com um pop-up de confirmação
        # semelhante ao de ADICIONAR USUARIO
        
        messagebox.showinfo("Confirmação", "Empréstimo confirmado com sucesso! (Simulação)")
        self.show_loans()


# ----------------------------------------------------
# --- SEU CÓDIGO DA TELA DE LOGIN (INÍCIO DO APP) ---
# ----------------------------------------------------

# Sua janela principal de Login
janela = ctk.CTk()
janela.title("Login da Biblioteca")
janela.geometry("1000x700")
janela.resizable(False, False)

# Fundo azul e Frame de Login
bg = ctk.CTkFrame(janela, corner_radius=0, fg_color=BLUE_COLOR)
bg.pack(fill="both", expand=True)

frame = ctk.CTkFrame(bg, fg_color="white", corner_radius=25, width=350, height=250)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Título
titulo = ctk.CTkLabel(frame, text="Login da Biblioteca", text_color="black", font=("Arial", 16, "bold"))
titulo.pack(pady=(20, 10))

# Campo Usuário
usuario_label = ctk.CTkLabel(frame, text="Nome de usuário", text_color="gray", anchor="w")
usuario_label.pack(fill="x", padx=30)
usuario_entry = ctk.CTkEntry(
    frame, corner_radius=10, fg_color="#f0f0f0", border_width=0, text_color="black", font=("Arial", 11)
)
usuario_entry.pack(fill="x", padx=30, pady=(0, 10), ipady=5)

# Campo Senha
senha_label = ctk.CTkLabel(frame, text="Senha", text_color="gray", anchor="w")
senha_label.pack(fill="x", padx=30)
senha_entry = ctk.CTkEntry(
    frame, corner_radius=10, fg_color="#f0f0f0", border_width=0, text_color="black", font=("Arial", 11), show="*"
)
senha_entry.pack(fill="x", padx=30, pady=(0, 15), ipady=5)


# --- FUNÇÃO DE LOGIN COM TRANSIÇÃO ---
def fazer_login():
    usuario = usuario_entry.get()
    senha = senha_entry.get()
    
    if usuario == "admin" and senha == "1234":
        messagebox.showinfo("Login", "Login bem-sucedido!")
        
        janela.withdraw() 
        
        dashboard_app = DashboardApp(login_window=janela) 
        dashboard_app.mainloop()
        
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

# Botão Entrar
botao = ctk.CTkButton(
    frame, text="Entrar", command=fazer_login, 
    corner_radius=20, fg_color=BLUE_COLOR, hover_color=HOVER_BLUE_COLOR,
    text_color="white", font=("Arial", 12, "bold")
)
botao.pack(pady=(5, 10), ipadx=10, ipady=5)

# Texto final
aviso = ctk.CTkLabel(frame, text="Apenas para administradores", text_color="gray", font=("Arial", 9))
aviso.pack(pady=(0, 5))

# Inicia a interface
janela.mainloop()