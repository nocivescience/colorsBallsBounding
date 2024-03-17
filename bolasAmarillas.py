from manim import *
class Heat(Scene):
    conf={
        'n_part':20,
        'config_rect':{
            'width':6,
            'height':4
        }
    }
    def construct(self):
        box=Rectangle(width=self.conf['config_rect']['width'],height=self.conf['config_rect']['height'], color=WHITE)
        signatures=np.random.choice(['+','-'],size=self.conf['n_part'])
        ball=VGroup(*[
            self.get_ball(box,sign) for x,sign in zip(range(self.conf['n_part']),signatures)
        ])
        title=self.get_title()
        self.add(box,ball,title)
        self.wait(4)
        ball[:4].clear_updaters()
        self.wait(2)
    def get_ball(self,box,sign):
        speed_factor=np.random.random()
        ball=Dot(radius=0.2,color=interpolate_color(BLUE,RED,speed_factor))
        sign=Tex(sign)
        sign.move_to(ball.get_center())
        sign.set_width(ball.get_width()-0.03)
        sign.set_color(BLACK)
        ball.sign=sign
        ball.add(sign)
        speed=2+3*speed_factor
        direction=rotate_vector(RIGHT,TAU*np.random.random())
        ball.velocity=speed*direction
        x0,y0,z0=box.get_corner(DL)
        x1,y1,z1=box.get_corner(UR)
        ball.move_to(np.array([
            interpolate(x0,x1,np.random.random()),
            interpolate(y0,y1,np.random.random()),
            0
        ]))
        def update(ball,dt):
            ball.shift(ball.velocity*dt)
            ball.sign.move_to(ball.get_center())
            ball.sign.set_color(BLACK)
            if ball.get_left()[0]<box.get_left()[0]:
                ball.velocity[0]=np.abs(ball.velocity[0])
                ball.rotate(PI/4,about_point=ball.get_center())
                ball.set_color(YELLOW)
            if ball.get_right()[0]>box.get_right()[0]:
                ball.velocity[0]=-np.abs(ball.velocity[0])
                ball.rotate(-PI/4,about_point=ball.get_center())
                ball.set_color(RED)
            if ball.get_top()[1]>box.get_top()[1]:
                ball.velocity[1]=-np.abs(ball.velocity[1])
                ball.rotate(PI/4,about_point=ball.get_center())
                ball.set_color(YELLOW)
            if ball.get_bottom()[1]<box.get_bottom()[1]:
                ball.velocity[1]=np.abs(ball.velocity[1])
                ball.rotate(PI/4,about_point=ball.get_center())
                ball.set_color(RED)
            return ball
        ball.add_updater(update)
        return ball
    def get_title(self):
        title=Text('Bolas amarillas')        
        title.set_stroke(width=0)
        title.to_edge(UP)
        new_title= CurvesAsSubmobjects(title[0])
        new_title.set_color_by_gradient(YELLOW,RED)
        return title