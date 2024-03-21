# DRAW INPUT LEFT
def draw_port_IL(x,y):
    return f'<polygon points="{x+00},{y+10} {x+00},{y+00} {x+20},{y+00} {x+30},{y+10} {x+50},{y+10} {x+30},{y+10} {x+20},{y+20} {x+00},{y+20} {x+00},{y+10}"/>\n'

# DRAW INOUT LEFT
def draw_port_IOL(x,y):
    return f'<polygon points="{x+00},{y+10} {x+10},{y+00} {x+20},{y+00} {x+30},{y+10} {x+50},{y+10} {x+30},{y+10} {x+20},{y+20} {x+10},{y+20} {x+00},{y+10}"/>\n'

# DRAW OUTPUT LEFT
def draw_port_OL(x,y):
    return f'<polygon points="{x+00},{y+10} {x+10},{y+00} {x+30},{y+00} {x+30},{y+10} {x+50},{y+10} {x+30},{y+10} {x+30},{y+20} {x+10},{y+20} {x+00},{y+10}"/>\n'

# DRAW INPUT RIGHT
def draw_port_IR(x,y):
    return f'<polygon points="{x+00},{y+10} {x+20},{y+10} {x+30},{y+00} {x+50},{y+00} {x+50},{y+10} {x+50},{y+20} {x+30},{y+20} {x+20},{y+10} {x+00},{y+10}"/>\n'

# DRAW INOUT RIGHT
def draw_port_IOR(x,y):
    return f'<polygon points="{x+00},{y+10} {x+20},{y+10} {x+30},{y+00} {x+40},{y+00} {x+50},{y+10} {x+40},{y+20} {x+30},{y+20} {x+20},{y+10} {x+00},{y+10}"/>\n'

# DRAW OUTPUT RIGHT
def draw_port_OR(x,y):
    return f'<polygon points="{x+00},{y+10} {x+20},{y+10} {x+20},{y+00} {x+40},{y+00} {x+50},{y+10} {x+40},{y+20} {x+20},{y+20} {x+20},{y+10} {x+00},{y+10}"/>\n'

# DRAW TEXT LEFT
def draw_TEXT_L(text, x ,y):
    return f'<text x="{x}" y="{y}" dominant-baseline="hanging" text-anchor="start" font-size="20" style="fill:black;stroke:black;stroke-width:0">{text}</text>\n'

# DRAW TEXT LEFT
def draw_TEXT_R(text, x ,y):
    return f'<text x="{x}" y="{y}" dominant-baseline="hanging" text-anchor="end" font-size="20" style="fill:black;stroke:black;stroke-width:0">{text}</text>\n'
