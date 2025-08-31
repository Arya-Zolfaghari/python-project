#___________  In the name of God _______________
##  29/8/2025

import numpy as np
import cv2
import os, sys, time
from tkinter import Tk, ttk, StringVar, IntVar, filedialog
from PIL import Image, ImageTk



####################################################################################



def odd(k: int) -> int:
    k = int(k)
    return k + 1 if k % 2 == 0 else k

#______________________________________________________________________________


def clamp_box(x, y, w, h, W, H):
    x = max(0, min(x, W - 1))
    y = max(0, min(y, H - 1))
    w = max(1, min(w, W - x))
    h = max(1, min(h, H - y))
    return x, y, w, h


#______________________________________________________________________________



def expand_box(x, y, w, h, W, H, sx=1.25, sy=1.40):
    cx = x + w / 2.0
    cy = y + h / 2.0
    nw = int(w * sx)
    nh = int(h * sy)
    nx = int(cx - nw / 2.0)
    ny = int(cy - nh / 2.0)
    return clamp_box(nx, ny, nw, nh, W, H)


#______________________________________________________________________________



def load_cascade(path_hint: str):
    if path_hint and os.path.exists(path_hint):
        cas = cv2.CascadeClassifier(path_hint)
        if not cas.empty():
            return cas, f"custom:{os.path.abspath(path_hint)}"
    default_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    cas = cv2.CascadeClassifier(default_path)
    if cas.empty():
        print("ERROR: could not load any cascade.", file=sys.stderr)
        sys.exit(1)
    return cas, f"default:{default_path}"

_PROFILE = None
def load_profile_cascade():
    global _PROFILE
    if _PROFILE is None:
        path = cv2.data.haarcascades + "haarcascade_profileface.xml"
        if os.path.exists(path):
            c = cv2.CascadeClassifier(path)
            if not c.empty():
                _PROFILE = c
    return _PROFILE


#______________________________________________________________________________



def _detect_raw(cascade, gray):
    faces = cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if faces is None:
        return []
    if isinstance(faces, np.ndarray):
        return [tuple(map(int, f)) for f in faces.tolist()]
    return [tuple(map(int, f)) for f in faces]


#______________________________________________________________________________



def detect_faces_scaled(cascade, frame_bgr, scale=0.5):
    H, W = frame_bgr.shape[:2]
    sw, sh = max(1, int(W*scale)), max(1, int(H*scale))
    small = cv2.resize(frame_bgr, (sw, sh), interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces_s = _detect_raw(cascade, gray)
    inv = 1.0 / max(1e-6, scale)
    out = []
    for (x, y, w, h) in faces_s:
        X, Y, Wb, Hb = int(x*inv), int(y*inv), int(w*inv), int(h*inv)
        out.append(clamp_box(X, Y, Wb, Hb, W, H))
    return out


#______________________________________________________________________________



def detect_faces_robust_scaled(cascade, frame_bgr, scale=0.5):
    H, W = frame_bgr.shape[:2]
    sw, sh = max(1, int(W*scale)), max(1, int(H*scale))
    small = cv2.resize(frame_bgr, (sw, sh), interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = _detect_raw(cascade, gray)
    if len(faces):
        inv = 1.0 / max(1e-6, scale)
        return [clamp_box(int(x*inv), int(y*inv), int(w*inv), int(h*inv), W, H) for (x,y,w,h) in faces]

    prof = load_profile_cascade()
    if prof is not None:
        out = []
        pf = _detect_raw(prof, gray)
        if len(pf):
            out.extend(pf)
        flip_small = cv2.flip(small, 1)
        grayf = cv2.cvtColor(flip_small, cv2.COLOR_BGR2GRAY)
        grayf = cv2.equalizeHist(grayf)
        pff = _detect_raw(prof, grayf)
        for (x, y, w, h) in pff:
            out.append((sw - (x + w), y, w, h))
        if len(out):
            inv = 1.0 / max(1e-6, scale)
            return [clamp_box(int(x*inv), int(y*inv), int(w*inv), int(h*inv), W, H) for (x,y,w,h) in out]

    return []



#______________________________________________________________________________




def ellipse_mask(w, h, feather=0.08, circle=True):
    mask = np.zeros((h, w), dtype=np.uint8)
    cx, cy = w // 2, h // 2
    if circle:
        r = max(1, int(min(w, h) * (1 - feather) / 2))
        cv2.circle(mask, (cx, cy), r, 255, -1)
    else:
        ax = max(1, int(w * (1 - feather) / 2))
        ay = max(1, int(h * (1 - feather) / 2))
        cv2.ellipse(mask, (cx, cy), (ax, ay), 0, 0, 360, 255, -1)
    fks = odd(max(3, int(min(w, h) * 0.06)))
    mask = cv2.GaussianBlur(mask, (fks, fks), 0)
    return mask


#______________________________________________________________________________




def gaussian_blur_img(img, downscale=2.0, k_scale=0.28, passes=1):
    h, w = img.shape[:2]
    ds = max(1.0, float(downscale))
    small = cv2.resize(img, (max(1, int(w/ds)), max(1, int(h/ds))), interpolation=cv2.INTER_LINEAR)
    k = odd(max(7, int(k_scale * min(small.shape[0], small.shape[1]))))
    out = small
    for _ in range(max(1, passes)):
        out = cv2.GaussianBlur(out, (k, k), 0)
    return cv2.resize(out, (w, h), interpolation=cv2.INTER_LINEAR)


#______________________________________________________________________________



def blur_gaussian_roi(frame, x, y, w, h, feather=0.08, circle=True, k_scale=0.28):
    H, W = frame.shape[:2]
    x, y, w, h = clamp_box(x, y, w, h, W, H)
    roi = frame[y:y+h, x:x+w]
    blurred = gaussian_blur_img(roi, downscale=2.0, k_scale=k_scale, passes=1)
    mask = ellipse_mask(w, h, feather=feather, circle=circle)
    mask_f = (mask.astype(np.float32) / 255.0)[..., None]
    blended = (blurred.astype(np.float32) * mask_f + roi.astype(np.float32) * (1.0 - mask_f)).astype(np.uint8)
    frame[y:y+h, x:x+w] = blended
    return frame


#______________________________________________________________________________




def chess_blur_roi(frame, x, y, w, h, feather=0.08, circle=True, tile=None,
                   lo=0.18, hi=0.40, draw_grid=False):
    H, W = frame.shape[:2]
    x, y, w, h = clamp_box(x, y, w, h, W, H)
    roi = frame[y:y+h, x:x+w]
    if tile is None:
        tile = max(12, min(w, h) // 10)
    b1 = gaussian_blur_img(roi, downscale=2.0, k_scale=lo, passes=1)
    b2 = gaussian_blur_img(roi, downscale=3.0, k_scale=hi, passes=1)
    yy, xx = np.indices((h, w))
    checker = ((yy // tile + xx // tile) % 2).astype(bool)
    mixed = roi.copy()
    mixed[checker]  = b1[checker]
    mixed[~checker] = b2[~checker]
    if draw_grid:
        for gx in range(0, w, tile):
            cv2.line(mixed, (gx, 0), (gx, h-1), (0, 0, 0), 1)
        for gy in range(0, h, tile):
            cv2.line(mixed, (0, gy), (w-1, gy), (0, 0, 0), 1)
    mask = ellipse_mask(w, h, feather=feather, circle=circle)
    mask_f = (mask.astype(np.float32) / 255.0)[..., None]
    blended = (mixed.astype(np.float32) * mask_f + roi.astype(np.float32) * (1.0 - mask_f)).astype(np.uint8)
    frame[y:y+h, x:x+w] = blended
    return frame




#________________________________ THE APP  ______________________________________
class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Live Face Obfuscation")
        self.root.resizable(False, False)

        self.mode = StringVar(value="gaussian")  # 'gaussian' or 'chess'
        self.circle = IntVar(value=1)
        self.strength = IntVar(value=35)         # %
        self.stride = IntVar(value=3)            # detect every N frames
        self.detect_scale = 0.5                  # fast & light

        self.width, self.height = 1280, 720
        self.cap = None
        self.cascade = None
        self.backend = ""
        self.last_faces = []
        self.miss = 0
        self.MISS_MAX = 6
        self.idx = 0
        self.fps = 0.0
        self._t0 = time.time()
        self._nf = 0
        self.running = False

        self._build_ui()

        try:
            cv2.setUseOptimized(True)
        except:
            pass

        self.cascade, self.backend = load_cascade("model.xml")



    def _build_ui(self):
        pad = {"padx": 12, "pady": 6}

        top = ttk.Frame(self.root)
        top.pack(fill="x", **pad)
        ttk.Label(top, text="Live Face Obfuscation", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        ttk.Label(top, text="B: Blur  ·  C: Chess-Blur  ·  S: Save  ·  Q: Quit", foreground="#666").pack(anchor="w")

        ctrl = ttk.Frame(self.root)
        ctrl.pack(fill="x", **pad)

        m = ttk.LabelFrame(ctrl, text="Mode")
        m.grid(row=0, column=0, sticky="w", padx=(0,10))
        ttk.Radiobutton(m, text="Blur",       variable=self.mode, value="gaussian").grid(row=0, column=0, padx=6)
        ttk.Radiobutton(m, text="Chess-Blur", variable=self.mode, value="chess").grid(row=0, column=1, padx=6)
        ttk.Checkbutton(m, text="Circle mask", variable=self.circle).grid(row=0, column=2, padx=8)

        t = ttk.LabelFrame(ctrl, text="Tuning")
        t.grid(row=0, column=1, sticky="w")
        ttk.Label(t, text="Gaussian strength").grid(row=0, column=0, sticky="e")
        ttk.Scale(t, from_=10, to=70, orient="horizontal", variable=self.strength, length=180).grid(row=0, column=1, padx=8)
        ttk.Label(t, text="Detector stride").grid(row=1, column=0, sticky="e", pady=(6,0))
        ttk.Scale(t, from_=1, to=6, orient="horizontal", variable=self.stride, length=180).grid(row=1, column=1, padx=8, pady=(6,0))

        btns = ttk.Frame(self.root)
        btns.pack(fill="x", **pad)
        self.btn = ttk.Button(btns, text="Start", width=12, command=self.toggle)
        self.btn.grid(row=0, column=0, padx=(0,8))
        ttk.Button(btns, text="Save Frame", width=12, command=self.save).grid(row=0, column=1, padx=8)
        ttk.Button(btns, text="Quit", width=10, command=self.close).grid(row=0, column=2, padx=8)

        wrap = ttk.Frame(self.root)
        wrap.pack(**pad)
        border = ttk.Frame(wrap, borderwidth=1, relief="groove")
        border.pack()
        self.panel = ttk.Label(border)
        self.panel.pack()

        status = ttk.Frame(self.root)
        status.pack(fill="x", **pad)
        self.left = ttk.Label(status, text="Idle")
        self.left.pack(side="left")
        self.right = ttk.Label(status, text="MODE: BLUR")
        self.right.pack(side="right")

        self.root.bind("b", lambda e: self.set_mode("gaussian"))
        self.root.bind("c", lambda e: self.set_mode("chess"))
        self.root.bind("s", lambda e: self.save())
        self.root.bind("q", lambda e: self.close())




    def set_mode(self, m):
        self.mode.set(m)
        self.right.config(text=f"MODE: {m.upper()}")



    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()



    def start(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        if not self.cap.isOpened():
            self.left.config(text="ERROR: cannot open camera")
            return
        self.running = True
        self.btn.config(text="Stop")
        self.left.config(text=f"Detector: {self.backend}")
        self.loop()



    def stop(self):
        self.running = False
        self.btn.config(text="Start")
        try:
            if self.cap is not None:
                self.cap.release()
        except:
            pass
        self.left.config(text="Stopped")



    def save(self):
        if hasattr(self, "last_rgb"):
            ts = int(time.time())
            path = filedialog.asksaveasfilename(defaultextension=".png",
                                                initialfile=f"frame_{self.mode.get()}_{ts}.png")
            if path:
                bgr = cv2.cvtColor(self.last_rgb, cv2.COLOR_RGB2BGR)
                cv2.imwrite(path, bgr)
                self.left.config(text=f"Saved: {os.path.basename(path)}")



    def close(self):
        self.stop()
        self.root.destroy()



    def loop(self):
        if not self.running:
            return

        ok, frame = self.cap.read()
        if not ok:
            self.root.after(10, self.loop)
            return

        H, W = frame.shape[:2]
        self.idx += 1

        faces = []
        if self.idx % max(1, int(self.stride.get())) == 1:
            faces = detect_faces_scaled(self.cascade, frame, scale=self.detect_scale)
            if len(faces) == 0:
                faces = detect_faces_robust_scaled(self.cascade, frame, scale=self.detect_scale)

            if len(faces) == 0 and len(self.last_faces) > 0 and self.miss < self.MISS_MAX:
                faces = self.last_faces
                self.miss += 1
            else:
                faces = [tuple(map(int, f)) for f in faces]
                self.last_faces = faces
                self.miss = 0
        else:
            faces = self.last_faces

        count = 0
        for (x, y, w, h) in faces:
            x, y, w, h = expand_box(x, y, w, h, W, H, 1.25, 1.40)
            circ = bool(self.circle.get())
            if self.mode.get() == "gaussian":
                k = max(0.10, self.strength.get()/100.0)
                frame = blur_gaussian_roi(frame, x, y, w, h, feather=0.08, circle=circ, k_scale=k)
            else:
                frame = chess_blur_roi(frame, x, y, w, h, feather=0.08, circle=circ,
                                       tile=None, lo=0.18, hi=0.40, draw_grid=False)
            count += 1

        # FPS
        self._nf += 1
        if self._nf >= 15:
            t1 = time.time()
            self.fps = self._nf / max(1e-6, (t1 - self._t0))
            self._t0 = t1
            self._nf = 0

        # overlay
        cv2.putText(frame, f"{self.mode.get().upper()} | FPS: {self.fps:.1f} | FACES: {count}",
                    (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 3, cv2.LINE_AA)
        cv2.putText(frame, f"{self.mode.get().upper()} | FPS: {self.fps:.1f} | FACES: {count}",
                    (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)
        footer = "made by Arya Zolfaghari & MohammadHossein Darzi"
        (tw, th), _ = cv2.getTextSize(footer, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.putText(frame, footer, (W - tw - 12, H - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 3, cv2.LINE_AA)
        cv2.putText(frame, footer, (W - tw - 12, H - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2, cv2.LINE_AA)

        # show
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.last_rgb = rgb
        imgtk = ImageTk.PhotoImage(Image.fromarray(rgb))
        self.panel.imgtk = imgtk
        self.panel.configure(image=imgtk)

        self.root.after(1, self.loop)



    def run(self):
        self.root.mainloop()





if __name__ == "__main__":
    App().run()
