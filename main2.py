import tkinter as TK
import customtkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image
import trimesh
import trimesh.viewer
import numpy as np
from utils import *
import doatools.model as model
import doatools.estimation as estimation
import doatools.plotting as doaplot
# from threading import Thread
# import pyrender

tk.set_appearance_mode("dark")
tk.set_default_color_theme("blue")
padx, pady = 10, 10
tm = trimesh.load("assets\Typhoon.stl")
# sc = tm.scene()
# viewer_widget=trimesh.viewer.SceneWidget(sc)
ang=[np.deg2rad(60),np.deg2rad(0),np.deg2rad(0)]
# viewer_widget.enable()
# geom = trimesh.creation.cylinder(10,10)
# sc.add_geometry(geometry=geom)
# mesh.split()
# scene = pyrender.Scene(ambient_light=[0.02, 0.02, 0.02],bg_color=[0.0, 0.5, 1.0])
# mesh=pyrender.Mesh.from_trimesh(tm)
# light = pyrender.PointLight(color=[1.0, 1.0, 1.0], intensity=2.0)
# scene.add(mesh)
# scene.add(light)
def view_3d():
    L=float(l.get())
    H=float(h.get())
    D=float(d.get())
    m=int(M.get())
    Dis=float(dis.get())/100
    rode_l=0.8
    rode_d=0.05
    sc = trimesh.Scene()
    sc.add_geometry(tm)
    box=tm.bounds
    dl=(box[1,1]-box[0,1])/L
    dh=(box[1,2]-box[0,2])/H
    pdis=dl*Dis
    centerl=box[0,1]+(box[1,1]-box[0,1])/2
    centerd=box[0,2]+(box[1,2]-box[0,2])/H*(D-0.1)/2
    if m%2==0:
        pf=centerl-((m/2)-0.5)*pdis
    else:
        pf=centerl-(int(m/2)-1)*pdis
    for i in range(m):
        geom = trimesh.creation.cylinder(rode_d*dl,rode_l*dh)
        geom.visual.face_colors=[255,255,0,255]
        geom.apply_translation((box[0,0],pf,centerd))
        sc.add_geometry(geom)
        geom = trimesh.creation.cylinder(rode_d*dl,rode_l*dh)
        geom.visual.face_colors=[255,255,0,255]
        geom.apply_translation((box[1,0],pf,centerd))
        sc.add_geometry(geom)
        pf+=pdis
    sc.show(start_loop=True,callback=rotate,callback_period=0.05,resolution=(800,600))
def view_3di():
    L=float(l.get())
    H=float(h.get())
    D=float(d.get())
    m=int(M.get())
    Dis=float(dis.get())/100
    rode_l=0.8
    rode_d=0.05
    sc = trimesh.Scene()
    sc.add_geometry(tm)
    box=tm.bounds
    dl=(box[1,1]-box[0,1])/L
    dh=(box[1,2]-box[0,2])/H
    pdis=dl*Dis
    centerl=box[0,1]+(box[1,1]-box[0,1])/2
    centerd=box[0,2]+(box[1,2]-box[0,2])/H*D/2
    if m%2==0:
        pf=centerl-((m/2)-0.5)*pdis
    else:
        pf=centerl-(int(m/2)-1)*pdis
    for i in range(m):
        geom = trimesh.creation.cylinder(rode_d*dl,rode_l*dh)
        geom.visual.face_colors=[255,255,0,255]
        geom.apply_translation((box[0,0],pf,centerd))
        sc.add_geometry(geom)
        geom = trimesh.creation.cylinder(rode_d*dl,rode_l*dh)
        geom.visual.face_colors=[255,255,0,255]
        geom.apply_translation((box[1,0],pf,centerd))
        sc.add_geometry(geom)
        pf+=pdis
    sc.show(resolution=(800,600))
    
def draw_beam():
    angles, beampattern = beam_pattern(int(velocity.get()),int(M.get()),int(testf.get()),int(dis.get())/100)
    thetas = np.degrees(angles)
    figure = plt.Figure(figsize=(7,1.7), dpi=100)
    ax = figure.add_subplot(111)
    btn = FigureCanvasTkAgg(figure, opt_panel)
    ax.plot(thetas, beampattern)
    btn.draw()
    btn.get_tk_widget().grid(row=3,column=0,rowspan=7,columnspan=6)
    
def rotate(sc):
    ang[2]=ang[2]+np.deg2rad(2)
    sc.set_camera(angles=tuple(ang))
    # root.after(50,func=rotate)

root=tk.CTk()

l=tk.StringVar(root,"29")
d=tk.StringVar(root,"2.75")
h=tk.StringVar(root,"4.8")
velocity=tk.StringVar(root,"1500")
dis=tk.StringVar(root,"")
fs=tk.StringVar(root,"")
M=tk.StringVar(root,"2")
testf = tk.StringVar(root,"1200")
Pc = tk.StringVar(root,"0.1")
Pr = tk.StringVar(root,"0.1")
Nl = tk.StringVar(root,"3")
Ns = tk.StringVar(root,"2")
f_l=tk.StringVar(root,"")
f_h=tk.StringVar(root,"")

def calc_sonar():
    l=float(marine_length.get())
    M.set(str(int((l-13)/0.5)))
    dis.set("50")
    fs.set("5120")

def calc_f():
    m=int(M.get())
    f__l=float(velocity.get())/((m-1)*float(dis.get())/100)
    f__m=float(fs.get())/2
    f_h.set("%.0fHz"%f__m)
    f_l.set("%.0fHz"%f__l)
    testf.set("%.0f"%((f__m+f__l)/2))

def testing():
    if typ.get():
        # do active testing here
        pass
    else:
        n_snapshots = 10
        wavelength = 1
        #passive_testing
        ula = model.UniformLinearArray(int(M.get()), float(dis.get())/100)
        thetas = np.random.random(size=int(Ns.get())+2 )*np.pi-(np.pi/2)
        sources = model.FarField1DSourcePlacement(thetas[1:-1])
        source_signal = model.ComplexStochasticSignal(sources.size, 1)
        noise_signal = model.ComplexStochasticSignal(ula.size, float(Nl.get()))
        _, R = model.get_narrowband_snapshots(ula, sources, wavelength, source_signal, noise_signal,n_snapshots, return_covariance=True)
        grid = estimation.FarField1DSearchGrid()
        estimator = estimation.MUSIC(ula, wavelength, grid) 
        resolved, estimates, sp = estimator.estimate(R, sources.size, return_spectrum=True)
        figure2 = plt.Figure(figsize=(4,4), dpi=100)
        ax2 = figure2.add_subplot(111)
        btn2 = FigureCanvasTkAgg(figure2, out_panel)
        btn2.get_tk_widget().grid(row=0,column=10,columnspan=8,rowspan=8)
        plt.figure()
        doaplot.plot_spectrum({'MUSIC': sp}, grid,ground_truth=sources, ax=ax2, use_log_scale=True)#ground_truth=sources
        ax2.set_xlim([-np.pi/2,np.pi/2])
        plt.show()
        





root.title("Sonar Designe and Analyse Tool by noshahr marin university")
root.grid_columnconfigure(3)
root.grid_rowconfigure(4)
root.geometry("1152x724")
LOGO=Image.open("assets\LOGO.png").resize((140,200))
font=tk.CTkFont(family="B Nazannin")
content = tk.CTkScrollableFrame(root)
# content.grid(column=0,row=0,columnspan=10,rowspan=10,sticky="news")
content.pack(expand=True,fill=tk.BOTH)

about_panel=tk.CTkFrame(content)
about_panel.grid_columnconfigure(0)
about_panel.grid_rowconfigure(2)
about_panel.grid(column=0,row=0,rowspan=2,sticky="news")
ctkimg = tk.CTkImage(LOGO,LOGO,(140,200))
logo_lbl=tk.CTkLabel(about_panel,text="",image=ctkimg)
# logo_lbl.image=LOGO
logo_lbl.grid(column=0,row=0,rowspan=2)
main_lbl=tk.CTkLabel(about_panel,text="Version 1.0")
main_lbl.grid(column=0,row=2,sticky="NSEW")

# setting_panel(content)
lbl_fr=TK.LabelFrame(content,text="SubMarine Dims",background=about_panel._bg_color[1],fg=about_panel._fg_color[0])
lbl_fr.grid(column=1,row=0,columnspan=2,sticky="news")
set_panel=tk.CTkFrame(master=lbl_fr)
set_panel.grid_columnconfigure(2)
set_panel.grid_rowconfigure(0)
set_panel.grid(column=0,row=0,columnspan=3,sticky="news")

set_but=tk.CTkButton(set_panel,text="Set Defaults",command=calc_sonar)
set_but.grid(column=10,row=0,padx=padx,pady=pady)

typ=tk.IntVar()
typ.set(0)
rad_lin=tk.CTkRadioButton(set_panel,text="Passive ",value=0,variable=typ,font=font)
rad_plan=tk.CTkRadioButton(set_panel,text="Active ",value=1,variable=typ,font=font)
rad_lin.grid(column=9,row=0)
rad_plan.grid(column=8,row=0)

vel=tk.CTkEntry(set_panel,textvariable=velocity)
vel.grid(column=7,row=0)
lbl =tk.CTkLabel(set_panel,text=" Sound Velocity (m/s) :",font=font)
lbl.grid(column=6,row=0)

marine_dia= tk.CTkEntry(set_panel,textvariable=d)
marine_dia.grid(column=5,row=0)
lbl =tk.CTkLabel(set_panel,text=" Diameter (m) :",font=font)
lbl.grid(column=4,row=0)

marine_heigth= tk.CTkEntry(set_panel,textvariable=h)
marine_heigth.grid(column=3,row=0)
lbl =tk.CTkLabel(set_panel,text=" Height (m):",font=font)
lbl.grid(column=2,row=0)

marine_length= tk.CTkEntry(set_panel,textvariable=l)
marine_length.grid(column=1,row=0)
lbl =tk.CTkLabel(set_panel,text=" Length (m):",font=font)
lbl.grid(column=0,row=0)

# option_panel(content)
lbl_fr_opt=TK.LabelFrame(content,text="Flank Array Specs",background=about_panel._bg_color[1],fg=about_panel._fg_color[0])
lbl_fr_opt.grid(column=1,row=1,columnspan=2,rowspan=1,sticky="news")
opt_panel=tk.CTkFrame(lbl_fr_opt)
opt_panel.grid(column=0,row=0,sticky="news")
cal_btn=tk.CTkButton(opt_panel,text="Calculate",command=calc_f)
cal_btn.grid(column=6,row=0,padx=padx,pady=pady)
d_sen=tk.CTkEntry(opt_panel,textvariable=dis)
d_sen.grid(column=5,row=0)
lbl=tk.CTkLabel(opt_panel,text=" Sensor Distance:",font=font)
lbl.grid(column=4,row=0)

F_s=tk.CTkEntry(opt_panel,textvariable=fs)
F_s.grid(column=3,row=0)
lbl=tk.CTkLabel(opt_panel,text=" Sampling Frequency:",font=font)
lbl.grid(column=2,row=0)

num_sen=tk.CTkEntry(opt_panel,textvariable=M)
num_sen.grid(column=1,row=0)
lbl=tk.CTkLabel(opt_panel,text=" Number of\n hydrophones:",font=font)
lbl.grid(column=0,row=0)

lbl=tk.CTkLabel(opt_panel,text="2-100",state='disabled')
lbl.grid(column=1,row=1,sticky='nw')
lbl=tk.CTkLabel(opt_panel,text="2-50 Hz",state='disabled')
lbl.grid(column=3,row=1,sticky='nw')
lbl=tk.CTkLabel(opt_panel,text="20-100 Cm",state='disabled')
lbl.grid(column=5,row=1,sticky='nw')

fh=tk.CTkEntry(opt_panel,textvariable=f_h,state='disabled')
fh.grid(row=2,column=1,sticky="w")
lbl=tk.CTkLabel(opt_panel,text="f_h=")
lbl.grid(row=2,column=0,sticky="e")
fl=tk.CTkEntry(opt_panel,textvariable=f_l,state='disabled')
fl.grid(row=2,column=3,sticky="w")
lbl=tk.CTkLabel(opt_panel,text="f_l=")
lbl.grid(row=2,column=2,sticky="e")
f_test=tk.CTkEntry(opt_panel,textvariable=testf)
f_test.grid(row=2,column=5)
lbl=tk.CTkLabel(opt_panel,text="Test Frequency=")
lbl.grid(row=2,column=4)
beam_btn=tk.CTkButton(opt_panel,text="Beam Pattern",command=draw_beam)
beam_btn.grid(row=2,column=6,padx=padx,pady=pady)

# img=Image.open(".\\assets\\beam_pat1.png")
# image=ImageTk.PhotoImage(image=img.resize((600,250)))
# btn=tk.Label(opt_panel,image=image,width=600,height=250)
# btn.image = image
# btn.grid(row=3,column=1,columnspan=7)

# img=Image.open("assets\\beam_pat2.png")
# image=ImageTk.PhotoImage(image=img.resize((200,200)))
# btn=tk.CTkLabel(opt_panel,image=image,text="",width=180,height=180)
# btn.image = image
figure = plt.Figure(figsize=(7,1.7), dpi=100)
ax = figure.add_subplot(111)
btn = FigureCanvasTkAgg(figure, opt_panel)
btn.get_tk_widget().grid(row=3,column=0,rowspan=7,columnspan=6)
# btn2=tk.CTkLabel(opt_panel,image=image,text="",width=180,height=180)
# btn2.image = image
# btn2.grid(row=0,column=0,rowspan=10,columnspan=3)

# output_panel(content)
lbl_fr_out=TK.LabelFrame(content,text="Analysis",background=about_panel._bg_color[1],fg=about_panel._fg_color[0])
lbl_fr_out.grid(column=0,row=3,columnspan=2,sticky="NSEW")
out_panel=tk.CTkFrame(lbl_fr_out)
out_panel.grid(column=0,row=0,columnspan=2,padx=5,pady=5,sticky="NSEW")
figure2 = plt.Figure(figsize=(4,4), dpi=100)
ax2 = figure2.add_subplot(111)
btn2 = FigureCanvasTkAgg(figure2, out_panel)
btn2.get_tk_widget().grid(row=0,column=10,columnspan=8,rowspan=8)
# lbl=tk.CTkLabel(out_panel,image=image,text="",width=300,height=300)
# lbl.image = image
# lbl.grid(row=0,column=0,columnspan=8,rowspan=8)
amb_noise=tk.CTkCheckBox(out_panel,text="Ambition Noise ",font=font)
amb_noise.grid(row=0,column=0,sticky="w")
clutter=tk.CTkCheckBox(out_panel,text="Clutter ",font=font)
clutter.grid(row=1,column=0,sticky="w")
reverb=tk.CTkCheckBox(out_panel,text="Reverbtion ",font=font)
reverb.grid(row=2,column=0,sticky="w")
# lbl=tk.CTkLabel(out_panel,text="Ambition Noise magnitude ",font=font)
# lbl.grid(row=0,column=1)
# lbl=tk.CTkLabel(out_panel,text="P clutter  ",font=font)
# lbl.grid(row=1,column=1)
# lbl=tk.CTkLabel(out_panel,text="P Reverbtion  ",font=font)
# lbl.grid(row=2,column=1)
A_snr=tk.CTkEntry(out_panel,textvariable=Nl)
A_snr.grid(row=0,column=2)
p_clut=tk.CTkEntry(out_panel,textvariable=Pc)
p_clut.grid(row=1,column=2)
p_reverb=tk.CTkEntry(out_panel,textvariable=Pr)
p_reverb.grid(row=2,column=2)
lbl=tk.CTkLabel(out_panel,text="Number of Targets",font=font)
lbl.grid(row=3,column=0)
n_sample=tk.CTkEntry(out_panel,textvariable=Ns)
n_sample.grid(row=3,column=1)
test=tk.CTkButton(out_panel,text="Test",command=testing)
test.grid(row=3,column=2,padx=padx,pady=pady)

# vis panel
lbl_fr_vis=TK.LabelFrame(content,text=" Visualizing",background=about_panel._bg_color[1],fg=about_panel._fg_color[0])
lbl_fr_vis.grid(column=2,row=3,columnspan=2,sticky="NSEW")
vis_panel=tk.CTkFrame(lbl_fr_vis)
vis_panel.grid(row=0,column=0,columnspan=2,sticky="NSEW")
td_view = tk.CTkButton(vis_panel,text="3D View",command=view_3d)
td_view.grid(padx=padx,pady=pady)
tdi_view = tk.CTkButton(vis_panel,text="interactive 3D View",command=view_3di)
tdi_view.grid(padx=padx,pady=pady)
# img=Image.open("assets\\2d_view.jpg")
# image=ImageTk.PhotoImage(image=img.resize((350,350)))
# vis_lbl=tk.CTkLabel(vis_panel,image=image,text="")
# vis_lbl.image=image
# vis_lbl.grid(row=1,column=0,columnspan=10)


for ch in content.children:
    content.children[ch].grid(padx=5,pady=5)
# for ch in about_panel.children:
#     about_panel.children[ch].grid(padx=1,pady=0,sticky="news")

# for ch in set_panel.children:
#     set_panel.children[ch].
# for ch in opt_panel.children:
#     opt_panel.children[ch].grid()
# for ch in out_panel.children:
#     out_panel.children[ch].grid(padx=1,pady=0,sticky="news")
# for ch in vis_panel.children:
#     vis_panel.children[ch].grid(padx=1,pady=0,sticky="news")


# sc.show()
# root.state(newstate='icon')
root.mainloop()
