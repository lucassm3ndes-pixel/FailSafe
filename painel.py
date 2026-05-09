import tkinter as tk
from tkinter import font
import threading
import time
import platform

class SistemaControle:
    def __init__(self, root):
        self.root = root
        self.root.title("CONSOLE DE OPERAÇÕES V145-15AST")
        self.root.geometry("1200x750")
        self.root.configure(bg="#050505")
        
        # Estado da tela cheia e fontes
        self.is_fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.fnt_mono = "Consolas" if "Consolas" in font.families() else "Monospace"

        # --- ESTRUTURA ---
        self.pan_esq = tk.Frame(root, bg="#080808", highlightbackground="#1a1a1a", highlightthickness=1)
        self.pan_esq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.pan_dir = tk.Frame(root, bg="#000000")
        self.pan_dir.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- INTERFACE VISUAL (ESQUERDA) ---
        self.canvas = tk.Canvas(self.pan_esq, bg="#080808", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        self.partes = {}
        self.desenhar_notebook_detalhado()

        # --- TERMINAL (DIREITA) ---
        self.log_area = tk.Text(self.pan_dir, bg="#000000", fg="#00FF41", 
                                font=(self.fnt_mono, 10), state=tk.DISABLED, borderwidth=0)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=(15, 5))
        
        # Tags de Cores
        self.log_area.tag_config("ok", foreground="#00FF00", font=(self.fnt_mono, 10, "bold"))
        self.log_area.tag_config("fail", foreground="#FF3333")
        self.log_area.tag_config("warn", foreground="#FFFF00")
        self.log_area.tag_config("header", foreground="#00BFFF", font=(self.fnt_mono, 11, "bold"))

        # Input Frame
        self.prompt_frame = tk.Frame(self.pan_dir, bg="#0a0a0a", height=40)
        self.prompt_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(self.prompt_frame, text=" SYSTEM > ", bg="#0a0a0a", fg="#00BFFF", 
                 font=(self.fnt_mono, 10, "bold")).pack(side=tk.LEFT)

        self.entry = tk.Entry(self.prompt_frame, bg="#0a0a0a", fg="white", 
                              font=(self.fnt_mono, 10), borderwidth=0, insertbackground="white")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", lambda e: self.executar())
        self.entry.focus_set()

        self.boot_sequence()

    def desenhar_notebook_detalhado(self):
        # 1. MONITOR (Moldura Externa)
        self.canvas.create_rectangle(40, 30, 460, 280, fill="#121212", outline="#252525", width=4)
        # Webcam e Sensores
        self.canvas.create_oval(245, 38, 255, 48, fill="#1a1a1a", outline="#333") 
        self.canvas.create_oval(249, 42, 251, 44, fill="#003366") # Lente
        
        # TELA (Parte Ativa)
        self.partes['monitor'] = self.canvas.create_rectangle(55, 50, 445, 260, fill="#111", outline="#000")
        self.canvas.create_text(250, 155, text="LENOVO V145 VIRTUAL CONSOLE", fill="#1a1a1a", font=(self.fnt_mono, 9))

        # 2. DOBRADIÇA
        self.canvas.create_rectangle(40, 280, 460, 295, fill="#1a1a1a", outline="#000")

        # 3. BASE (Carcaça Principal)
        self.canvas.create_polygon(40, 295, 460, 295, 510, 450, -10, 450, fill="#151515", outline="#252525", width=2)
        
        # TECLADO (Área da CPU/RAM)
        self.partes['teclado'] = self.canvas.create_polygon(80, 310, 420, 310, 440, 380, 60, 380, fill="#1a1a1a", outline="#222")
        
        # GPU (No canto inferior esquerdo como solicitado)
        self.partes['gpu'] = self.canvas.create_rectangle(50, 400, 120, 435, fill="#111", outline="#333")
        self.canvas.create_text(85, 417, text="AMD GPU", fill="#333", font=(self.fnt_mono, 7, "bold"))

        # STORAGE (Touchpad)
        self.partes['storage'] = self.canvas.create_rectangle(200, 395, 310, 435, fill="#1a1a1a", outline="#333")
        self.canvas.create_text(255, 415, text="STORAGE", fill="#333", font=(self.fnt_mono, 7))

        # LEDS DE STATUS
        self.canvas.create_text(40, 315, text="PWR", fill="#333", font=(self.fnt_mono, 6))
        self.partes['power'] = self.canvas.create_oval(35, 320, 45, 330, fill="#330000") # Led Power
        
        self.canvas.create_text(40, 345, text="NET", fill="#333", font=(self.fnt_mono, 6))
        self.partes['rede'] = self.canvas.create_oval(35, 350, 45, 360, fill="#001100") # Led Rede

        # Logo Lenovo
        self.canvas.create_text(420, 430, text="Lenovo", fill="#222", font=("Arial", 10, "italic bold"))

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        return "break"

    def exit_fullscreen(self, event=None):
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", False)
        return "break"

    def log(self, msg, status="info"):
        self.log_area.config(state=tk.NORMAL)
        tag = "info"
        prefix = "[ .... ] "
        
        if status == "ok":
            prefix = "[  OK  ] "
            tag = "ok"
        elif status == "fail":
            prefix = "[ FAIL ] "
            tag = "fail"
        elif status == "warn":
            prefix = "[ WARN ] "
            tag = "warn"
        elif status == "header":
            prefix = ">>> "
            tag = "header"

        self.log_area.insert(tk.END, prefix, tag)
        self.log_area.insert(tk.END, f"{msg}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def boot_sequence(self):
        def run():
            self.log("INICIALIZANDO SUBSISTEMA V145-15AST...", "header")
            time.sleep(0.5)
            self.canvas.itemconfig(self.partes['power'], fill="#FF0000") # Liga o LED
            self.log("Checando Kernel e Drivers...", "info")
            time.sleep(1)
            self.log("Interface gráfica carregada (F11 para Tela Cheia)", "ok")
            self.log("Digite 'help' para comandos.", "info")
        threading.Thread(target=run, daemon=True).start()

    def set_color(self, parte, cor):
        cores = {"verde": "#00FF00", "amarelo": "#FFFF00", "vermelho": "#FF0000", "reset": "#1a1a1a", "off": "#111"}
        if parte in self.partes:
            self.canvas.itemconfig(self.partes[parte], fill=cores.get(cor, "#111"))

    def executar(self):
        cmd = self.entry.get().lower().strip()
        self.entry.delete(0, tk.END)
        if not cmd: return

        # AGORA USANDO "CHECK"
        if cmd == "help":
            self.log("--- COMANDOS DE DIAGNÓSTICO ---", "header")
            self.log("check monitor  | check gpu", "info")
            self.log("check net      | check storage", "info")
            self.log("check cpu      | reset", "info")
            self.log("clear          | exit", "info")
        elif cmd == "check monitor": self.thread_task(self.task_monitor)
        elif cmd == "check gpu": self.thread_task(self.task_gpu)
        elif cmd == "check net": self.thread_task(self.task_net)
        elif cmd == "check storage": self.thread_task(self.task_storage)
        elif cmd == "check cpu": self.thread_task(self.task_cpu)
        elif cmd == "clear":
            self.log_area.config(state=tk.NORMAL)
            self.log_area.delete('1.0', tk.END)
            self.log_area.config(state=tk.DISABLED)
        elif cmd == "reset":
            for p in self.partes: 
                if p not in ['power', 'rede']: self.set_color(p, "off")
            self.log("Visual resetado.", "info")
        elif cmd == "exit": self.root.destroy()
        else:
            self.log(f"Comando '{cmd}' inválido. Tente 'help'.", "fail")

    def thread_task(self, target):
        threading.Thread(target=target, daemon=True).start()

    # --- TAREFAS ---
    def task_monitor(self):
        self.log("Iniciando varredura de LCD...", "info")
        self.set_color("monitor", "amarelo")
        time.sleep(1.5)
        self.log("Monitor: Resolvido 1366x768 @ 60Hz", "ok")
        self.set_color("monitor", "verde")

    def task_gpu(self):
        self.log("Acessando AMD Radeon R2...", "info")
        self.set_color("gpu", "amarelo")
        time.sleep(2)
        self.log("GPU: Renderização OK", "ok")
        self.set_color("gpu", "verde")

    def task_net(self):
        self.log("Sincronizando pacotes...", "info")
        self.canvas.itemconfig(self.partes['rede'], fill="#FFFF00")
        time.sleep(1)
        self.log("Rede: Conexão Estável", "ok")
        self.canvas.itemconfig(self.partes['rede'], fill="#00FF00")

    def task_storage(self):
        self.log("Lendo blocos do SSD/HDD...", "info")
        self.set_color("storage", "amarelo")
        time.sleep(1.5)
        self.log("Storage: 0 bad sectors", "ok")
        self.set_color("storage", "verde")

    def task_cpu(self):
        self.log("Stress test: AMD A4-9125...", "info")
        self.set_color("teclado", "amarelo")
        time.sleep(1.2)
        self.log("CPU: 32°C - Estável", "ok")
        self.set_color("teclado", "verde")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaControle(root)
    root.mainloop()