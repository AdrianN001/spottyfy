import numpy as np

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static


class Donut(Widget):
    DEFAULT_CSS = """
    Static{
        width: 100%;
        height: 100%;
    }
    """


    screen_size = 15
    theta_spacing = 0.07
    phi_spacing = 0.02
    illumination = np.fromiter(".,-~:;=!*#$@", dtype="<U1")

    A = 1
    B = 1
       


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


    def compose(self) -> ComposeResult:

        yield Static(id="donut_container")


    def on_mount(self) -> None:
        
        self.donut_container = self.query_one("#donut_container", Static)

        self.set_interval(1/20, self.render_callback)
    
    def render_callback(self) -> None:
        self.A += self.theta_spacing
        self.B += self.phi_spacing

        self.render_frame()

    def render_frame(self) -> np.ndarray:
        """
        Returns a frame of the spinning 3D donut.
        Based on the pseudocode from: https://www.a1k0n.net/2011/07/20/donut-math.html
        """

        A = self.A
        B = self.B
        screen_size = self.screen_size

        phi_spacing = self.phi_spacing
        theta_spacing = self.theta_spacing

        illumination = self.illumination
        
        R1 = 1
        R2 = 2
        K2 = 5
        K1 = screen_size * K2 * 3 / (8 * (R1 + R2))



        cos_A = np.cos(A)
        sin_A = np.sin(A)
        cos_B = np.cos(B)
        sin_B = np.sin(B)

        output = np.full((screen_size, screen_size), " ")  # (40, 40)
        zbuffer = np.zeros((screen_size, screen_size))  # (40, 40)

        cos_phi = np.cos(phi := np.arange(0, 2 * np.pi, phi_spacing))  # (315,)
        sin_phi = np.sin(phi)  # (315,)
        cos_theta = np.cos(theta := np.arange(0, 2 * np.pi, theta_spacing))  # (90,)
        sin_theta = np.sin(theta)  # (90,)
        circle_x = R2 + R1 * cos_theta  # (90,)
        circle_y = R1 * sin_theta  # (90,)

        x = (np.outer(cos_B * cos_phi + sin_A * sin_B * sin_phi, circle_x) - circle_y * cos_A * sin_B).T  # (90, 315)
        y = (np.outer(sin_B * cos_phi - sin_A * cos_B * sin_phi, circle_x) + circle_y * cos_A * cos_B).T  # (90, 315)
        z = ((K2 + cos_A * np.outer(sin_phi, circle_x)) + circle_y * sin_A).T  # (90, 315)
        ooz = np.reciprocal(z)  # Calculates 1/z
        xp = (screen_size / 2 + K1 * ooz * x).astype(int)  # (90, 315)
        yp = (screen_size / 2 - K1 * ooz * y).astype(int)  # (90, 315)
        L1 = (((np.outer(cos_phi, cos_theta) * sin_B) - cos_A * np.outer(sin_phi, cos_theta)) - sin_A * sin_theta)  # (315, 90)
        L2 = cos_B * (cos_A * sin_theta - np.outer(sin_phi, cos_theta * sin_A))  # (315, 90)
        L = np.around(((L1 + L2) * 8)).astype(int).T  # (90, 315)
        mask_L = L >= 0  # (90, 315)
        chars = illumination[L]  # (90, 315)

        for i in range(90):
            mask = mask_L[i] & (ooz[i] > zbuffer[xp[i], yp[i]])  # (315,)

            zbuffer[xp[i], yp[i]] = np.where(mask, ooz[i], zbuffer[xp[i], yp[i]])
            output[xp[i], yp[i]] = np.where(mask, chars[i], output[xp[i], yp[i]])

        print_buffer = pprint(output)

        self.donut_container.update(print_buffer)

        return output





import time


def pprint(array: np.ndarray) -> str:
    """Pretty print the frame."""
    return '\n'.join([" ".join(row) for row in array])


if __name__ == "__main__":
    while True:
        A += theta_spacing
        B += phi_spacing

        time.sleep(1/60)
        print("\x1b[H")
        pprint(render_frame(A, B))
