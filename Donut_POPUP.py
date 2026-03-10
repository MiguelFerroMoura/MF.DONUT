import tkinter as tk
import math
import random

width = 80
height = 24

chars = "\/|()"
chars_list = list(chars)

root = tk.Tk()
root.title("MF Donut")

text = tk.Text(
    root,
    width=width,
    height=height,
    bg="black",
    font=("Consolas", 12),
    bd=0
)

# cor exclusiva do "desenho"
outline = "#300246"

# 21 níveis de iluminação
colors = [
"#2b0a3d",
"#310a45",
"#370b4e",
"#3e0c57",
"#450d61",
"#4c0f6b",
"#541176",
"#5c1481",
"#65178c",
"#6f1a97",
"#791ea3",
"#8422af",
"#8f26bb",
"#9b2bc7",
"#a830d3",
"#b436df",
"#c13deb",
"#ce45f4",
"#d84fff",
"#dc57ff",
"#e05bff"
]
text.tag_config("outline", foreground=outline)

for i, c in enumerate(colors):
    text.tag_config(f"c{i}", foreground=c)

text.pack()

A = 0
B = 0

light = (0, 0.6, -0.8)

l = math.sqrt(sum(i*i for i in light))
light = tuple(i/l for i in light)

def render():
    global A, B

    zbuffer = [0]*(width*height)
    screen = [" "]*(width*height)
    shade = [0]*(width*height)

    for j in range(0, 628, 7):
        for i in range(0, 628, 2):

            ii = i/100
            jj = j/100

            si = math.sin(ii)
            ci = math.cos(ii)
            sj = math.sin(jj)
            cj = math.cos(jj)

            sa = math.sin(A)
            ca = math.cos(A)
            sb = math.sin(B)
            cb = math.cos(B)

            h = cj + 2

            D = 1/(si*h*sa + sj*ca + 5)

            x = int(width/2 + 30*D*(ci*h*cb - (si*h*ca - sj*sa)*sb))
            y = int(height/2 + 15*D*(ci*h*sb + (si*h*ca - sj*sa)*cb))

            o = x + width*y

            if 0 <= x < width and 0 <= y < height and D > zbuffer[o]:

                zbuffer[o] = D
                screen[o] = random.choice(chars_list)

                nx = ci*cj
                ny = si*cj
                nz = sj

                nx2 = nx*cb - ny*sb
                ny2 = nx*sb + ny*cb
                nz2 = nz

                nx3 = nx2
                ny3 = ny2*ca - nz2*sa
                nz3 = ny2*sa + nz2*ca

                L = nx3*light[0] + ny3*light[1] + nz3*light[2]

                shade[o] = max(0, L)

    text.delete("1.0", tk.END)

    for k in range(width*height):

        if k % width == 0 and k != 0:
            text.insert(tk.END,"\n")

        char = screen[k]

        if char != " ":

            s = shade[k]

            if s < 0.15:
                text.insert(tk.END, char, "outline")
            else:
                level = int(s * (len(colors)-1))
                level = max(0, min(level, len(colors)-1))
                text.insert(tk.END, char, f"c{level}")

        else:
            text.insert(tk.END," ")

    A += 0.04
    B += 0.02

    root.after(30, render)

render()
root.mainloop()
