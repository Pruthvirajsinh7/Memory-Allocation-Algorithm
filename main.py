import tkinter as tk
from tkinter import messagebox
from tkinter import messagebox, simpledialog

class MemoryAllocationSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Memory Allocation Simulator")

        self.memory_size = 0
        self.partitions = []
        self.memory_blocks = []
        self.processes = []

        self.get_initial_memory_setup() # For initial memory setup from the user

        # left side
        self.canvas = tk.Canvas(self.master, height=900, width=800, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        self.display_memory()

        # Take Process size 
        self.label_process_size = tk.Label(self.master, text="Process Size:")
        self.label_process_size.pack(pady=(10, 0))

        self.entry_process_size = tk.Entry(self.master)
        self.entry_process_size.pack(pady=5)

        self.label_algorithm = tk.Label(self.master, text="Allocation Algorithm:")
        self.label_algorithm.pack(pady=5)

        self.algorithm_var = tk.StringVar()
        self.algorithm_var.set("First Fit")

        self.algorithm_menu = tk.OptionMenu(self.master, self.algorithm_var, "First Fit", "Best Fit", "Worst Fit", "Next Fit"
                                            )
        self.algorithm_menu.pack(pady=5)

        self.allocate_button = tk.Button(self.master, text="Allocate", command=self.allocate_memory)
        self.allocate_button.pack(pady=5)

    def get_initial_memory_setup(self):

        self.memory_size = simpledialog.askinteger("Memory Setup", "Enter Total Memory Size (in KB):", parent=self.master)

        partition_sizes_str = simpledialog.askstring("Memory Setup", "Enter Partition Sizes (separated by commas):", parent=self.master)
        self.partitions = [int(size) for size in partition_sizes_str.split(',')]

        if self.memory_size is None or any(size <= 0 for size in self.partitions):
            messagebox.showerror("Error", "Invalid input. Please provide valid memory and partition sizes.")
            self.master.destroy() 
            return

        start_position = 50
        self.memory_blocks = [(size, start_position) for size in self.partitions]

    def display_memory(self):
        self.canvas.delete("all")
        gap = 5  
        x, y = 50, 50

        for i, (size, start) in enumerate(self.memory_blocks):
            height = (size / self.memory_size) * 500  
            end_x, end_y = x + 100, y + height  

            allocated_height = 0

            for process_index, process_size in self.processes:
                if process_index == i:
    
                    allocated_height = (process_size / size) * height # Height of the allocated portion

                    self.canvas.create_rectangle(x, y, end_x, y + allocated_height, fill="lightgreen", outline="black")
                    self.canvas.create_text((x + end_x) / 2, y + allocated_height / 2, text=f"{process_size}Kb", fill="black")
                
                    height -= allocated_height

            if allocated_height == 0:
                self.canvas.create_rectangle(x, y, end_x, end_y, fill="lightblue", outline="black")
                self.canvas.create_text((x + end_x) / 2, (y + end_y) / 2, text=f"{size}Kb", fill="black")
            else:

                remaining_size = max(size - sum(process_size for p_idx, process_size in self.processes if p_idx == i), 0)
                self.canvas.create_rectangle(x, y + allocated_height, end_x, end_y, fill="lightblue", outline="black")
                self.canvas.create_text((x + end_x) / 2, (y + allocated_height + end_y) / 2, text=f"{remaining_size}Kb", fill="black")

            y = end_y + gap

        self.canvas.create_text(400, 325, text=f"Memory Size: {self.memory_size}Kb", fill="black") # Total Size 

    def allocate_memory(self):
        process_size = int(self.entry_process_size.get())
        algorithm = self.algorithm_var.get()

        if process_size <= 0:
            messagebox.showerror("Error", "Process size must be greater than 0.")
            return

        if algorithm == "Best Fit":
            block_index = self.best_fit(process_size)
        elif algorithm == "First Fit":
            block_index = self.first_fit(process_size)
        elif algorithm == "Next Fit":
            block_index = self.next_fit(process_size)
        elif algorithm == "Worst Fit":
            block_index = self.worst_fit(process_size)
        else:
            messagebox.showerror("Error", "Invalid allocation algorithm.")
            return

        if block_index is not None:
            self.processes.append((block_index, process_size))
            self.display_memory()
        else:
            messagebox.showinfo("Info", "Memory allocation failed. No suitable block found.")

 

    def best_fit(self, process_size):
        best_fit_index = None
        best_fit_remaining_size = float('inf')

        for i, (size, start) in enumerate(self.memory_blocks):
            if any(process_index == i for process_index, _ in self.processes):
                continue  # Skip already allocated blocks

            remaining_size = size - process_size
            if remaining_size >= 0 and remaining_size < best_fit_remaining_size:
                best_fit_index = i
                best_fit_remaining_size = remaining_size

        return best_fit_index


    def first_fit(self, process_size):
        for i, (size, start) in enumerate(self.memory_blocks):
            if any(process_index == i for process_index, _ in self.processes):
                continue  # Skip already allocated blocks

            remaining_size = size - process_size
            if remaining_size >= 0:
                return i

        return None

    def next_fit(self, process_size):
        if not hasattr(self, 'last_allocated_block'):
            self.last_allocated_block = 0

        for i in range(len(self.memory_blocks)):
            index = (i + self.last_allocated_block) % len(self.memory_blocks)
            size, start = self.memory_blocks[index]
            if size >= process_size and not any(process_index == index for process_index, _ in self.processes):
                self.last_allocated_block = index
                return index

        return None

    def worst_fit(self, process_size):
        worst_fit_index = None
        max_remaining_size = -1

        for i, (size, start) in enumerate(self.memory_blocks):
            if any(process_index == i for process_index, _ in self.processes):
                continue  # Skip already allocated blocks

            remaining_size = size - process_size
            if remaining_size >= 0 and remaining_size > max_remaining_size:
                worst_fit_index = i
                max_remaining_size = remaining_size

        return worst_fit_index


if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryAllocationSimulator(root)
    root.mainloop()