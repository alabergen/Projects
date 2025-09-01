from tkinter import *
import time
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

        # Entry for grid size and number of obstacles

        self.grid_size_label = Label( self.root, text="Map size (Max. 20x20):", bg = "grey13", fg = "white")
        self.grid_size_label.place(x = 0, y = 25)

        self.n_obstacles = Label(self.root, text="Number of Obstacles:", bg = "grey13", fg = "white")
        self.n_obstacles.place(x = 0, y = 45)
        
        self.grid_entry = Entry(self.root, width = 10,bg = "grey20", fg = "white")
        self.grid_entry.place(x = 130, y = 25)

        self.obstacles_entry = Entry(self.root, width = 10, bg = "grey20", fg = "white")
        self.obstacles_entry.place(x = 130, y = 45)        

        self.entry_warning = Label( self.root, text="", bg = "grey13")
        self.entry_warning.place(x = 0, y = 100)

        # Button to generate the grid
        self.generate_button = Button(self.root, text="Generate", command=self.generate_grid, bg = "grey20", borderwidth=0.5, fg = "white", width = 10)
        self.generate_button.place(x=130,y=70)

        # Canvas for grid
        self.canvas = Canvas(self.root, bg="#20004e", bd = 0, highlightthickness = 1, highlightbackground="black", height=self.canvas_size, width=self.canvas_size, cursor="circle")
        Canvas()
        self.canvas.pack(pady = 20)

        self.root.mainloop()

    def generate_grid(self):
        # Clear canvas for re-generation
        self.canvas.delete("all")
        self.entry_warning.destroy()
        self.entry_warning = Label( self.root, text="")
        self.entry_warning.place(x = 0, y = 100)

        try:
            size = int(self.grid_entry.get())
            n_obstacles = int(self.obstacles_entry.get())           
            if size <= 2 or size > 20:
                self.entry_warning.config(text="Enter map size between 2 & 20.", bg = "grey13", fg = "red")
                raise TypeError
            if n_obstacles > size:
                self.entry_warning.config(text="Too many obstacles entered.", bg = "grey13", fg = "red")
            elif n_obstacles < 0:
                self.entry_warning.config(text="Negative values are not allowed.", bg = "grey13", fg = "red")
        except:
            self.entry_warning.config(text="These values do not look right. Try again.", bg = "grey13", fg = "red")
        else:
            self.grid_size = size
            self.margin = (self.canvas_size - self.grid_size * self.cell_size) // 2
            self.x_pos = 0
            self.y_pos = 0

            self.draw_grid()
            self.draw_robot()
            self.bind_keys()

    def draw_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = self.margin + j * self.cell_size
                y1 = self.margin + i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="#20004e", outline = "#584ea3")
                self.canvas.tag_lower(rect)

    def draw_robot(self):
        x1 = self.margin
        y1 = self.margin
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.x_pos = (x1 + x2)/2
        self.y_pos = (y1 + y2)/2
        self.robot_obj = self.canvas.create_oval(x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill="blue")

    def move_robot(self, dx, dy):
        x = self.x_pos
        y = self.y_pos
        new_x = x + dx
        new_y = y + dy

        # Compute valid boundaries with margins taken into account
        min_pos = self.margin + self.cell_size / 2
        max_pos = self.margin + (self.grid_size - 1) * self.cell_size + self.cell_size / 2

        if min_pos <= new_x <= max_pos and min_pos <= new_y <= max_pos:
            x1 = new_x - 0.5 * self.cell_size
            y1 = new_y - 0.5 * self.cell_size
            x2 = new_x + 0.5 * self.cell_size
            y2 = new_y + 0.5 * self.cell_size
            self.canvas.coords(self.robot_obj, x1 + 2, y1 + 2, x2 - 2, y2 - 2)

            self.canvas.create_line(x, y, new_x, new_y, width=2, fill="red", dash=(5, 5))
            self.canvas.tag_raise(self.robot_obj)

            self.x_pos = new_x
            self.y_pos = new_y
            
            # Drawing a trail left behind the robot:
            self.canvas.create_line(x, y, new_x, new_y, width = 2, fill = "red", dash = (5,5))
            self.canvas.tag_raise(self.robot_obj)


    def bind_keys(self):
        self.root.bind("<Left>", lambda event: self.move_robot(-self.cell_size, 0))
        self.root.bind("<Right>", lambda event: self.move_robot(self.cell_size, 0))
        self.root.bind("<Up>", lambda event: self.move_robot(0, -self.cell_size))
        self.root.bind("<Down>", lambda event: self.move_robot(0, self.cell_size))
        
# Start the app
GridApp()
  