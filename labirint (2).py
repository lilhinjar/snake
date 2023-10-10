import random
import arcade
import arcade.gui

wallWidth = 14

screenWidth = 400
screenHeigth = 400
green = (0, 255, 0)
text = ("Цель игры: Вашей целью является управление змейкой и прохождение через лабиринт, избегая столкновений со стенами и собственным хвостом"  
+ "\n Управление змейкой:"
+ "\n Вы можете управлять змейкой, используя стрелки на клавиатуре (вверх, вниз, влево, вправо)."
+ "\n Избегание столкновений:"
+ "\n Избегайте столкновений со стенами лабиринта и собственным хвостом. Столкновение приводит к поражению."
+ "\n Цель и победа: Вашей целью является пройти через лабиринт. Если вы дошли до выхода, это означает вашу победу."
+ "\n Уровни сложности:"
+ "\n Игра предоставляет несколько уровней сложности с различными размерами лабиринта и скоростью змейки."
+ "\n Завершение игры:"
+ "\n Игра может быть завершена, если вы проигрываете (сталкиваетесь со стенами или собственным хвостом) или вы выигрываете (проходите лабиринт)."
+ "\n Победа и поражение:"
+ "\n если вы проходите лабиринт, это считается вашей победой."
+ "\n Если вы не можете сделать это и сталкиваетесь со стенами или хвостом, это означает ваше поражение."
)

levels = {
    1: {
        "screen": {
            "width": 400,
            "length": 400
        },
        "labirintSize": 12
    },
    2: {
        "screen": {
            "width": 600,
            "length": 600
        },
        "labirintSize": 18
    },
    3: {
    "screen": {
        "width": 800,
        "length": 800
    },
    "labirintSize": 24
    }
}

class cell:
    def __init__(self,up,down,left,right):
        self.visited = False
        self.walls = [up,down,left,right]

class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()

class labyrinth:
    global wallList
    wallList = arcade.SpriteList()
    def __init__(self,id, level):
        self.id = id
        self.walls = []
        self.maze_walls = []
        self.cells = []

        x = 0
        t = 0

        for f in range(levels[level]["labirintSize"]):
            for s in range(levels[level]["labirintSize"]):
                if not (f in (0,1,2) and s > levels[level]["labirintSize"]):
                    self.cells.append(cell((x + wallWidth, t, 25, wallWidth), (x + wallWidth, t + 33, 25, wallWidth), (x, t + wallWidth, wallWidth, 25), (x + 33, t + wallWidth, wallWidth, 25)))
                x += 33
            x = 0
            t += 33
            

        for v in self.cells[0].walls:
            self.maze_walls.append(v)
            self.walls.append(v)

        self.cells[0].visited = True

        while len(self.walls) > 0:
            wall = random.choice(self.walls)
            divided_cells = []
            for u in self.cells:
                if wall in u.walls:
                    divided_cells.append(u)

            if len(divided_cells) > 1 and (not ((divided_cells[0].visited and divided_cells[1].visited) or ((not divided_cells[0].visited) and (not divided_cells[1].visited)))):
                for k in divided_cells:
                    k.walls.remove(wall)

                    if k.visited == False:
                        k.visited = True

                    for q in k.walls:
                        if not q in self.walls:
                            self.walls.append(q)

                        if not q in self.maze_walls:
                            self.maze_walls.append(q)

                    if wall in self.maze_walls:
                        self.maze_walls.remove(wall)

            self.walls.remove(wall)

        for j in range(0,levels[level]["screen"]["width"],33):
            for i in range(0,levels[level]["screen"]["length"],33):
                self.maze_walls.append((i, j, wallWidth, wallWidth))

    def draw(self):
        for k in self.maze_walls:
            wall = arcade.Sprite(":resources:images/tiles/grassCenter.png", 0.1)
            wall.center_x = k[0]
            wall.center_y = k[1]
            wall.width = k[2]
            wall.height = k[3]
       
            wallList.append(wall)


def our_snake(snake_block, snake_list):
   for x in snake_list:
        print(snake_list)
        arcade.draw_rectangle_filled(x[0], x[1], snake_block, snake_block, green )

class Snake(arcade.Window):
    global show_menu, current_level, show_rules, show_win, show_lose
    show_menu = True
    show_rules = False
    show_win = False
    show_lose = False
    current_level = 1
    def __init__(self):
        super().__init__(600,800)


        arcade.set_background_color((0,0,0))

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.v_box = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="Level 1", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Level 2", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        level_3 = arcade.gui.UIFlatButton(text="Level 3", width=200)
        self.v_box.add(level_3.with_space_around(bottom=20))

        rules = arcade.gui.UIFlatButton(text="Rules", width=200)
        self.v_box.add(rules.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        start_button.on_click = self.on_level_start_1
        settings_button.on_click = self.on_level_start_2
        level_3.on_click = self.on_level_start_3
        rules.on_click = self.on_show_rules
        quit_button.on_click = self.on_exit

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_exit(self, event):
        global show_menu, current_level
        if(show_menu):
            arcade.exit()

    def on_level_start_1(self, event):
        global show_menu, current_level
        if(show_menu):
            show_menu = False
            current_level = 1
            arcade.Window.set_size(self, 380, 360)
            self.clear()
            self.setup()

    def on_level_start_2(self, event):
        global show_menu, current_level
        if(show_menu):
            show_menu = False
            current_level = 2
            arcade.Window.set_size(self, 580, 560)
            self.clear()
            self.setup()

    def on_level_start_3(self, event):
        global show_menu, current_level
        if(show_menu):
            show_menu = False
            current_level = 3
            arcade.Window.set_size(self, 780, 760)
            self.clear()
            self.setup()

    def on_show_rules(self, event):
        global show_menu, current_level, show_rules
        if(show_menu):
            show_rules = True
            show_menu = False
            arcade.Window.set_size(self, 800, 800)
            self.clear()
        

    def setup(self):
        global lab, speed, x_change, y_change, x, y, player, wallList, win
        wallList = arcade.SpriteList()

        x = 16
        y = 16
        x_change = 0
        y_change = 0
        speed = 1
        player = arcade.Sprite()
        self.physics_engine = arcade.PhysicsEngineSimple(player, wallList)
        win = arcade.Sprite()
        player.color = (0, 128, 255)

        win.width = 15
        win.height = 15
        win.center_x = levels[current_level]["screen"]["width"] - 22
        win.center_y = levels[current_level]["screen"]["length"] - 22
        win.color = (0, 255, 0)

        player.width = 10
        player.height = 10
        player.center_x = x
        player.center_y = y
        lab = labyrinth(1, current_level)
        lab.draw() 
        self.clear()
        pass

    def on_key_press(self, key, modifiers):
        global x_change, y_change, show_menu, show_rules, show_win, show_lose

        if key == arcade.key.UP or key == arcade.key.W:
            y_change = speed
            x_change = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            y_change = -speed
            x_change = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            x_change = -speed
            y_change = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            x_change = speed
            y_change = 0
        elif key == arcade.key.ESCAPE:
            show_menu = True
            show_rules = False
            show_lose = False
            show_win = False
            arcade.Window.set_size(self, 600, 800)
            self.clear()
            self.setup()
        
    def on_update(self, delta_time):
        self.physics_engine.update()

    def on_draw(self):
        global x, y, show_menu, show_rules, show_win, show_lose
        """Render the screen."""
        self.clear()
        if(show_menu) :
            self.manager.draw()
            self.manager.enable()
        elif(show_rules) :
            self.manager.disable()
            arcade.draw_text(text,
                0,
                700,
                arcade.color.BLACK,
                16,
                width=800,
                align="center"
                            )
             
        elif(show_win) :

            arcade.draw_text("ВЫ ПОБЕДИЛИ",
                0,
                400,
                arcade.color.GREEN,
                40,
                width=875,
                align="center"
                            )
        elif(show_lose) :

            arcade.draw_text("ВЫ ПРОИГРАЛИ",
                0,
                400,
                arcade.color.RED,
                40,
                width=875,
                align="center"
                            )
        else:   

            x += x_change
            y += y_change
            wallList.draw()

            player.center_x = x
            player.center_y = y

            player.draw()
            win.draw()

            walls_hit = arcade.check_for_collision_with_list(player, wallList, win)
            is_win = arcade.check_for_collision(player, win)

            if(len(walls_hit) != 0):
                self.clear()
                self.setup()
                show_lose = True
                arcade.Window.set_size(self, 880, 800)
            
            if(is_win) :
                self.clear()
                show_win = True
                arcade.Window.set_size(self, 880, 800)
                

def main():
    window = Snake()
    window.setup()
    arcade.run()

main()