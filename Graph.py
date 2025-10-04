from tkinter import *
import time
import heapq
import random

class GridApp:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1000x600")
        self.root.configure(background = "grey13")
        self.root.title("Dynamic Grid Generator")

        self.canvas_size = 480
        self.cell_size = 20
        self.margin = 0
        self.grid_size = 0
        self.x_pos = 0
        self.y_pos = 0
        self.robot_obj = None
        self.robot_cell_index = 0
    
        self.obstacle_positions = set()

        self.grid_size_label = Label(self.root, text="Map size (Max. 20x20):", bg="grey13", fg="white")
        self.grid_size_label.place(x=0, y=25)

        self.n_obstacles = Label(self.root, text="Number of Obstacles:", bg="grey13", fg="white")
        self.n_obstacles.place(x=0, y=45)

        self.grid_entry = Entry(self.root, width=10, bg="grey20", fg="white")
        self.grid_entry.place(x=130, y=25)

        self.obstacles_entry = Entry(self.root, width=10, bg="grey20", fg="white")
        self.obstacles_entry.place(x=130, y=45)

        self.entry_warning = Label(self.root, text="", bg="grey13")
        self.entry_warning.place(x=0, y=100)

        self.ctrls = Label(self.root, text="Controls:", bg="grey13", fg="white")
        self.ctrls.place(x=70, y=70)

        self.manual_var = IntVar()
        self.auto_var = IntVar()

        self.option1 = Checkbutton(self.root, variable=self.manual_var, text="Manual", bg="grey13", fg="white",
                                   selectcolor="grey20", command=self.manual_selected)
        self.option1.place(x=125, y=70)

        self.option2 = Checkbutton(self.root, variable=self.auto_var, text="Autopilot", bg="grey13", fg="white",
                                   selectcolor="grey20", command=self.auto_selected)
        self.option2.place(x=125, y=90)

        self.generate_button = Button(self.root, text="Generate", command=self.generate_grid, bg="grey20",
                                      borderwidth=0.5, fg="white", width=10)
        self.generate_button.place(x=130, y=125)

        self.destination = Entry(self.root, width=10, bg="grey20", fg="white")
        self.destination.place(x=130, y=165)

        self.d_label = Label(self.root, text="Destination (e.g. B2):", bg="grey13", fg="white")
        self.d_label.place(x=10, y=165)

        self.autopilot_button = Button(self.root, text="Kachow!", command=self.autopilot, bg="grey20",
                                       borderwidth=0.5, fg="white", width=10)
        self.autopilot_button.place(x=130, y=200)

        self.canvas = Canvas(self.root, bg="#20004e", bd=0, highlightthickness=1, highlightbackground="black",
                             height=self.canvas_size, width=self.canvas_size, cursor="circle")
        self.canvas.pack(pady=20)

        self.root.mainloop()

    def manual_selected(self):
        if self.manual_var.get():
            self.auto_var.set(0)

    def auto_selected(self):
        if self.auto_var.get():
            self.manual_var.set(0)

    def generate_grid(self):
        self.canvas.delete("all")
        self.entry_warning.destroy()
        self.entry_warning = Label(self.root, text="")
        self.entry_warning.place(x=0, y=100)

        try:
            size = int(self.grid_entry.get())
            n_obstacles = int(self.obstacles_entry.get())
            if size <= 2 or size > 20:
                self.entry_warning.config(text="Enter map size between 2 & 20.", bg="grey13", fg="red")
                raise TypeError
            if n_obstacles > size:
                self.entry_warning.config(text="Too many obstacles entered.", bg="grey13", fg="red")
            elif n_obstacles < 0:
                self.entry_warning.config(text="Negative values are not allowed.", bg="grey13", fg="red")
        except:
            self.entry_warning.config(text="These values do not look right. Try again.", bg="grey13", fg="red")
        else:
            self.grid_size = size
            self.margin = (self.canvas_size - self.grid_size * self.cell_size) // 2
            self.x_pos = 0
            self.y_pos = 0

            # Generate obstacle positions
            total_cells = size * size
            self.obstacle_positions = set()
            while len(self.obstacle_positions) < n_obstacles:
                cell = random.randint(0, total_cells - 1)
                if cell != 0:  # don't block the start cell
                    self.obstacle_positions.add(cell)

            self.draw_grid()
            self.draw_robot()
            self.bind_keys()


    def draw_grid(self):
        x_axis = ["T", "S", "R", "Q", "P", "O", "N", "M", "L", "K", "J", "I", "H", "G", "F", "E", "D", "C", "B", "A"]
        n = 0
        x = self.margin + self.cell_size * 0.5
        y = self.margin - 0.5 * self.cell_size
        for i in range(self.grid_size):
            self.canvas.create_text(x, y, text=x_axis[-1], fill="#584ea3")
            x_axis.pop()

            self.canvas.create_text(y, x, text=str(1 + n), fill="#584ea3")
            x += self.cell_size
            n += 1

            for j in range(self.grid_size):
                x1 = self.margin + j * self.cell_size
                y1 = self.margin + i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                cell_index = i * self.grid_size + j
                fill = "black" if cell_index in self.obstacle_positions else "#20004e"

                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="#584ea3")
                self.canvas.tag_lower(rect)


    def draw_robot(self):
        x1 = self.margin
        y1 = self.margin
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.x_pos = (x1 + x2) / 2
        self.y_pos = (y1 + y2) / 2
        self.robot_obj = self.canvas.create_oval(x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill="blue")
        self.robot_cell_index = 0

    def move_robot(self, dx, dy):
        x = self.x_pos
        y = self.y_pos
        new_x = x + dx
        new_y = y + dy

        min_pos = self.margin + self.cell_size / 2
        max_pos = self.margin + (self.grid_size - 1) * self.cell_size + self.cell_size / 2

        # Check if new position is inside grid bounds
        if not (min_pos <= new_x <= max_pos and min_pos <= new_y <= max_pos):
            return  # out of bounds

        # Convert new position to grid cell index
        col = int((new_x - self.margin) // self.cell_size)
        row = int((new_y - self.margin) // self.cell_size)
        cell_index = row * self.grid_size + col

        # Check if target cell is an obstacle
        if cell_index in self.obstacle_positions:
            return  # obstacle detected; block movement

        # Move robot
        x1 = new_x - 0.5 * self.cell_size
        y1 = new_y - 0.5 * self.cell_size
        x2 = new_x + 0.5 * self.cell_size
        y2 = new_y + 0.5 * self.cell_size
        self.canvas.coords(self.robot_obj, x1 + 2, y1 + 2, x2 - 2, y2 - 2)

        self.canvas.create_line(x, y, new_x, new_y, width=2, fill="red", dash=(5, 5))
        self.canvas.tag_raise(self.robot_obj)

        self.x_pos = new_x
        self.y_pos = new_y
        self.robot_cell_index = cell_index


    def bind_keys(self):
        self.root.bind("<Left>", lambda event: self.move_robot(-self.cell_size, 0))
        self.root.bind("<Right>", lambda event: self.move_robot(self.cell_size, 0))
        self.root.bind("<Up>", lambda event: self.move_robot(0, -self.cell_size))
        self.root.bind("<Down>", lambda event: self.move_robot(0, self.cell_size))


    def edge_generator(self, size):
        edges = {}
        cell = 0
        for i in range(size):
            for j in range(size):
                if cell in self.obstacle_positions:
                    cell += 1
                    continue  

                if i == 0 and j == 0:
                    neighbors = [1, size]
                elif i == 0 and j == size - 1:
                    neighbors = [2 * size - 1, size - 2]
                elif i == size - 1 and j == size - 1:
                    neighbors = [(size * size) - size - 1, (size ** 2) - 2]
                elif i == size - 1 and j == 0:
                    neighbors = [(i - 1) * size, size * i + 1]
                elif i == 0:
                    neighbors = [j + 1, (i + 1) * size + j, j - 1]
                elif j == size - 1:
                    neighbors = [i * size - 1, (i + 2) * size - 1, ((i + 1) * size) - 2]
                elif i == size - 1:
                    neighbors = [size * (i - 1) + j, i * size + j + 1, size * i + j - 1]
                elif j == 0:
                    neighbors = [(i - 1) * size, (i) * size + 1, (i + 1) * size]
                else:
                    neighbors = [(i - 1) * size + j, i * size + j + 1, (i + 1) * size + j, i * size + j - 1]

                filtered_neighbors = [n for n in neighbors if n not in self.obstacle_positions]

                edges[cell] = filtered_neighbors 

                cell += 1

        return edges


    def shortestPath(self, adj, V, src, destination):
        pq = []
        dist = [float('inf')] * V
        parent = [None] * V


        heapq.heappush(pq, (0, src))
        dist[src] = 0
        parent[src] = -1

        while pq:
            distance, u = heapq.heappop(pq)

            for v, weight in adj.get(u, []):
                if dist[v] > dist[u] + weight:
                    dist[v] = dist[u] + weight
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))

        path = []
        v = destination
        while v != -1:
            path.append(v)
            v = parent[v]
        path.reverse()
        return path
    
    def cell_label_to_index(self, label):
        """
        Convert cell label like 'A1', 'D20' to grid index.
        Columns are letters A (rightmost) to T (leftmost), rows are numbers starting from 1.
        """
        if len(label) < 2:
            return None

        col_letter = label[0].upper()
        row_str = label[1:]

        if not row_str.isdigit():
            return None

        row = int(row_str) - 1  # zero-based row
        if row < 0 or row >= self.grid_size:
            return None

        x_axis = ["T", "S", "R", "Q", "P", "O", "N", "M", "L", "K", "J", "I", "H", "G", "F", "E", "D", "C", "B", "A"]

        if col_letter not in x_axis:
            return None

        # Reverse index so 'A' is rightmost col, matching canvas indexing
        col = (self.grid_size - 1) - x_axis.index(col_letter)

        if col < 0 or col >= self.grid_size:
            return None

        return row * self.grid_size + col


    def autopilot(self):
        dest_label = self.destination.get().strip()
        dest_index = self.cell_label_to_index(dest_label)
        if dest_index is None:
            self.entry_warning.config(text="Invalid destination. Use format like 'A1', 'D20'.", fg="red")
            return
        
        size = self.grid_size
        edges = self.edge_generator(size)
        adj = {k: [(v, 1) for v in vs] for k, vs in edges.items()}
        
        src = self.robot_cell_index
        dst = dest_index
        
        if dst in self.obstacle_positions:
            self.entry_warning.config(text="Destination is blocked by obstacle.", fg="red")
            return
        
        path = self.shortestPath(adj, size * size, src, dst)
        
        if len(path) == 0 or path[0] != src or path[-1] != dst:
            self.entry_warning.config(text="No path found to destination.", fg="red")
            return
        
        for idx in path[1:]:
            curr_row, curr_col = divmod(self.robot_cell_index, size)
            next_row, next_col = divmod(idx, size)
            dx = (next_col - curr_col) * self.cell_size
            dy = (next_row - curr_row) * self.cell_size
            
            self.move_robot(dx, dy)
            self.root.update()
            time.sleep(0.3)


# Launch App
GridApp()
