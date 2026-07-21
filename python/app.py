# -*- coding: utf-8 -*-
"""
E7gezly – Medical Booking App  v4
Light & clean design: white cards, soft shadows, vivid accents
"""
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import calendar as cal_mod

# ══════════════════════════════════════════════════════════════════════════════
#  DATABASE
# ══════════════════════════════════════════════════════════════════════════════
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "e7gezly"
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)

# ══════════════════════════════════════════════════════════════════════════════
#  LIGHT PALETTE
# ══════════════════════════════════════════════════════════════════════════════
C_BG        = "#F0F4FF"   # page background – soft lavender-white
C_SURFACE   = "#FFFFFF"   # card white
C_SURFACE2  = "#F7F9FF"   # slightly off-white
C_PANEL     = "#EEF2FF"   # sidebar / panel
C_BORDER    = "#DDE3F0"   # subtle border
C_BORDER2   = "#C5CFEA"   # stronger border

# Accents
C_BLUE      = "#4F6EF7"   # primary blue
C_BLUE_D    = "#3A56D4"   # hover
C_BLUE_L    = "#EEF1FF"   # blue tint bg
C_GREEN     = "#22C55E"   # success / available
C_GREEN_L   = "#DCFCE7"   # green tint
C_AMBER     = "#F59E0B"   # ratings
C_AMBER_L   = "#FEF3C7"   # amber tint
C_RED       = "#EF4444"   # cancel / error
C_RED_L     = "#FEE2E2"   # red tint
C_PURPLE    = "#8B5CF6"   # insurance
C_PURPLE_L  = "#EDE9FE"   # purple tint
C_TEAL      = "#14B8A6"   # doctor accent
C_TEAL_L    = "#CCFBF1"   # teal tint
C_PINK      = "#EC4899"   # cardiology
C_PINK_L    = "#FCE7F3"
C_ORANGE    = "#F97316"   # orthopedics
C_ORANGE_L  = "#FFEDD5"

# Text
C_TEXT      = "#1E2A4A"   # primary dark
C_TEXT2     = "#4A5568"   # secondary
C_TEXT3     = "#94A3B8"   # muted

# Specialization palette  (bg_tint, accent, icon)
SPEC = {
    "Cardiology":  (C_PINK_L,   C_PINK,   "♥"),
    "Dermatology": (C_AMBER_L,  C_AMBER,  "✦"),
    "Neurology":   (C_BLUE_L,   C_BLUE,   "⬡"),
    "Pediatrics":  (C_GREEN_L,  C_GREEN,  "✿"),
    "Orthopedics": (C_ORANGE_L, C_ORANGE, "⬟"),
}

# Fonts
FN_DISPLAY = ("Segoe UI", 18, "bold")
FN_HEAD    = ("Segoe UI", 13, "bold")
FN_SUBH    = ("Segoe UI", 10, "bold")
FN_BODY    = ("Segoe UI", 9)
FN_SMALL   = ("Segoe UI", 8)
FN_TINY    = ("Segoe UI", 7)
FN_LABEL   = ("Segoe UI", 7, "bold")

# ══════════════════════════════════════════════════════════════════════════════
#  DRAWING PRIMITIVES
# ══════════════════════════════════════════════════════════════════════════════
def clear(f):
    for w in f.winfo_children(): w.destroy()

def rr(cv, x1, y1, x2, y2, r=10, fill=C_BLUE, outline=""):
    f = fill
    cv.create_arc(x1,y1,x1+2*r,y1+2*r, start=90,  extent=90,  fill=f, outline=f)
    cv.create_arc(x2-2*r,y1,x2,y1+2*r, start=0,   extent=90,  fill=f, outline=f)
    cv.create_arc(x2-2*r,y2-2*r,x2,y2, start=270, extent=90,  fill=f, outline=f)
    cv.create_arc(x1,y2-2*r,x1+2*r,y2, start=180, extent=90,  fill=f, outline=f)
    cv.create_rectangle(x1+r,y1,x2-r,y2, fill=f, outline=f)
    cv.create_rectangle(x1,y1+r,x2,y2-r, fill=f, outline=f)

def rr_outline(cv, x1, y1, x2, y2, r=10, color=C_BORDER, width=1):
    cv.create_arc(x1,y1,x1+2*r,y1+2*r, start=90,  extent=90,  style="arc", outline=color, width=width)
    cv.create_arc(x2-2*r,y1,x2,y1+2*r, start=0,   extent=90,  style="arc", outline=color, width=width)
    cv.create_arc(x2-2*r,y2-2*r,x2,y2, start=270, extent=90,  style="arc", outline=color, width=width)
    cv.create_arc(x1,y2-2*r,x1+2*r,y2, start=180, extent=90,  style="arc", outline=color, width=width)
    cv.create_line(x1+r,y1,x2-r,y1, fill=color, width=width)
    cv.create_line(x1+r,y2,x2-r,y2, fill=color, width=width)
    cv.create_line(x1,y1+r,x1,y2-r, fill=color, width=width)
    cv.create_line(x2,y1+r,x2,y2-r, fill=color, width=width)

# ── Filled pill button ────────────────────────────────────────────────────────
def pill_btn(parent, text, cmd, w=200, h=40,
             color=C_BLUE, hover=C_BLUE_D, fg=C_SURFACE,
             bg=C_BG, font=None):
    font = font or ("Segoe UI", 9, "bold")
    cv = tk.Canvas(parent, width=w, height=h, bg=bg, highlightthickness=0)
    def draw(c):
        cv.delete("all")
        rr(cv, 0, 0, w, h, r=h//2, fill=c)
        cv.create_text(w//2, h//2, text=text, fill=fg, font=font)
    draw(color)
    cv.bind("<Button-1>", lambda e: cmd())
    cv.bind("<Enter>",    lambda e: draw(hover))
    cv.bind("<Leave>",    lambda e: draw(color))
    return cv

# ── Outline ghost button ──────────────────────────────────────────────────────
def ghost_btn(parent, text, cmd, w=110, h=32,
              color=C_BORDER2, hover_color=C_BLUE,
              text_col=C_TEXT2, bg=C_SURFACE):
    cv = tk.Canvas(parent, width=w, height=h, bg=bg, highlightthickness=0)
    def draw(border, tc):
        cv.delete("all")
        rr(cv, 0, 0, w, h, r=h//2, fill=bg)
        rr_outline(cv, 1, 1, w-1, h-1, r=h//2-1, color=border, width=1)
        cv.create_text(w//2, h//2, text=text, fill=tc, font=("Segoe UI",8,"bold"))
    draw(color, text_col)
    cv.bind("<Button-1>", lambda e: cmd())
    cv.bind("<Enter>",    lambda e: draw(hover_color, hover_color))
    cv.bind("<Leave>",    lambda e: draw(color, text_col))
    return cv

# ── Styled entry ──────────────────────────────────────────────────────────────
def styled_entry(parent, placeholder="", secret=False, font=None, width=None):
    font = font or FN_BODY
    kw = {"width": width} if width else {}
    e = tk.Entry(parent, font=font, fg=C_TEXT3, bg=C_SURFACE,
                 insertbackground=C_BLUE, relief="flat", bd=0,
                 highlightbackground=C_BORDER, highlightthickness=1,
                 highlightcolor=C_BLUE, **kw)
    e.insert(0, placeholder)
    show = "●" if secret else ""
    def fi(_):
        if e.get() == placeholder: e.delete(0, tk.END); e.config(fg=C_TEXT, show=show)
        e.config(highlightbackground=C_BLUE)
    def fo(_):
        if not e.get(): e.insert(0, placeholder); e.config(fg=C_TEXT3, show="")
        e.config(highlightbackground=C_BORDER)
    e.bind("<FocusIn>", fi); e.bind("<FocusOut>", fo)
    return e

# ── Scrollable frame ──────────────────────────────────────────────────────────
def scrollable(parent, bg=C_BG):
    cv = tk.Canvas(parent, bg=bg, highlightthickness=0)
    vsb = tk.Scrollbar(parent, orient="vertical", command=cv.yview,
                       bg=C_PANEL, troughcolor=C_BG, width=6)
    vsb.pack(side="right", fill="y")
    cv.pack(fill="both", expand=True)
    cv.configure(yscrollcommand=vsb.set)
    inner = tk.Frame(cv, bg=bg)
    win = cv.create_window((0,0), window=inner, anchor="nw")
    cv.bind("<Configure>", lambda e: cv.itemconfig(win, width=e.width))
    inner.bind("<Configure>", lambda e: cv.configure(scrollregion=cv.bbox("all")))
    cv.bind_all("<MouseWheel>", lambda e: cv.yview_scroll(int(-1*(e.delta/120)), "units"))
    return inner

# ── Section header ────────────────────────────────────────────────────────────
def sec_hdr(parent, title, bg=C_BG, accent=C_BLUE):
    f = tk.Frame(parent, bg=bg)
    f.pack(fill="x", padx=28, pady=(20, 8))
    tk.Label(f, text=title, bg=bg, fg=accent,
             font=FN_LABEL).pack(side="left")
    tk.Frame(f, bg=C_BORDER, height=1).pack(
        side="left", fill="x", expand=True, padx=10, pady=4)

# ── Stat card ─────────────────────────────────────────────────────────────────
def stat_card(parent, value, label, accent, accent_l, w=148, h=88):
    cv = tk.Canvas(parent, width=w, height=h, bg=C_BG, highlightthickness=0)
    cv.pack(side="left", padx=5)
    rr(cv, 0, 0, w, h, r=12, fill=C_SURFACE)
    rr_outline(cv, 0, 0, w, h, r=12, color=C_BORDER)
    # coloured left strip
    rr(cv, 0, 0, 5, h, r=3, fill=accent)
    # icon circle
    cv.create_oval(w-38, 14, w-14, 38, fill=accent_l, outline="")
    cv.create_text(w-26, 26, text="●", fill=accent, font=("Segoe UI",8))
    cv.create_text(22, 38, text=str(value), fill=accent,
                   font=("Segoe UI", 20, "bold"), anchor="w")
    cv.create_text(22, 62, text=label, fill=C_TEXT3,
                   font=("Segoe UI", 7), anchor="w")
    return cv

# ══════════════════════════════════════════════════════════════════════════════
#  BOOKING MODAL
# ══════════════════════════════════════════════════════════════════════════════
DAY_ORDER = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

def our_day_to_python_wd(day_name):
    return (DAY_ORDER.index(day_name) - 1) % 7

def _generate_slots(start_time_obj, end_time_obj):
    """Return list of (slot_start, slot_end) as datetime.time pairs, 30-min each."""
    from datetime import timedelta
    slots = []
    current = datetime.combine(datetime.today(), start_time_obj)
    end     = datetime.combine(datetime.today(), end_time_obj)
    # handle overnight schedules (end < start means next day)
    if end <= current:
        end += timedelta(days=1)
    while current + timedelta(minutes=30) <= end:
        slots.append((current.time(), (current + timedelta(minutes=30)).time()))
        current += timedelta(minutes=30)
    return slots

def _fmt_time(t):
    """Format a time object as  3:00 PM"""
    return datetime.combine(datetime.today(), t).strftime("%I:%M %p").lstrip("0")

def open_booking_modal(p_id, d_id, d_name, d_spec, on_booked=None):
    try:
        conn = get_connection(); cur = conn.cursor(dictionary=True)
        cur.execute("""SELECT Schedule_id, Day_Name,
                              Start_Time, End_Time,
                              TIME_FORMAT(Start_Time,'%I:%i %p') AS t_start,
                              TIME_FORMAT(End_Time,'%I:%i %p')   AS t_end
                       FROM Schedules WHERE User_Doctor_id=%s
                       ORDER BY FIELD(Day_Name,'Sunday','Monday','Tuesday',
                                      'Wednesday','Thursday','Friday','Saturday')""", (d_id,))
        schedules = cur.fetchall(); cur.close(); conn.close()
    except Exception as ex:
        messagebox.showerror("Error", str(ex)); return
    if not schedules:
        messagebox.showinfo("No Schedule", f"{d_name} has no available slots yet."); return

    # Build weekday → schedule map
    sched_map = {}
    for s in schedules:
        wd = our_day_to_python_wd(s['Day_Name'])
        # Start_Time / End_Time come back as timedelta from MySQL connector
        from datetime import timedelta as _td
        def _td_to_time(val):
            if isinstance(val, _td):
                total = int(val.total_seconds())
                return datetime.strptime(f"{total//3600:02d}:{(total%3600)//60:02d}", "%H:%M").time()
            return val  # already a time object
        s['start_t'] = _td_to_time(s['Start_Time'])
        s['end_t']   = _td_to_time(s['End_Time'])
        sched_map[wd] = s
    avail_wds = set(sched_map.keys())

    sp_tint, sp_ac, sp_ic = SPEC.get(d_spec, (C_BLUE_L, C_BLUE, "✚"))

    modal = tk.Toplevel(); modal.title("")
    modal.geometry("520x660"); modal.resizable(False, False)
    modal.configure(bg=C_BG); modal.grab_set()

    # ── Header ────────────────────────────────────────────────────────────────
    hdr = tk.Frame(modal, bg=C_SURFACE, height=72); hdr.pack(fill="x"); hdr.pack_propagate(False)
    tk.Frame(hdr, bg=sp_ac, width=4).pack(side="left", fill="y")
    hi = tk.Frame(hdr, bg=C_SURFACE); hi.pack(side="left", padx=20, pady=14, fill="both", expand=True)
    tk.Label(hi, text="Book Appointment", bg=C_SURFACE, fg=C_TEXT, font=FN_HEAD).pack(anchor="w")
    sr = tk.Frame(hi, bg=C_SURFACE); sr.pack(anchor="w")
    tk.Label(sr, text=sp_ic+"  ", bg=C_SURFACE, fg=sp_ac, font=("Segoe UI",10)).pack(side="left")
    tk.Label(sr, text=d_name, bg=C_SURFACE, fg=C_TEXT2, font=FN_BODY).pack(side="left")
    tk.Label(sr, text=f"  ·  {d_spec}", bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(side="left")

    body = tk.Frame(modal, bg=C_BG); body.pack(fill="both", expand=True, padx=24, pady=12)

    # ── Calendar ──────────────────────────────────────────────────────────────
    cal_card = tk.Frame(body, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
    cal_card.pack(fill="x")
    nav_row = tk.Frame(cal_card, bg=C_SURFACE); nav_row.pack(fill="x", padx=16, pady=(12,4))

    now = datetime.now()
    cur_m = tk.IntVar(value=now.month); cur_y = tk.IntVar(value=now.year)
    sel_date   = tk.StringVar(value="")
    sel_slot   = {"start": None, "end": None, "sched_id": -1, "day": ""}

    MONTHS = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]
    month_lbl = tk.Label(nav_row, text="", bg=C_SURFACE, fg=C_TEXT, font=("Segoe UI",11,"bold"))
    month_lbl.pack(side="left")
    grid_f = tk.Frame(cal_card, bg=C_SURFACE); grid_f.pack(fill="x", padx=16, pady=(0,12))

    # ── Slot area (shown after date pick) ─────────────────────────────────────
    slot_label = tk.Label(body, text="", bg=C_BG, fg=C_TEXT2, font=("Segoe UI",8,"bold"))
    slot_label.pack(anchor="w", pady=(8,4))
    slot_frame = tk.Frame(body, bg=C_BG); slot_frame.pack(fill="x")

    # ── Confirm button ────────────────────────────────────────────────────────
    tk.Frame(body, bg=C_BG, height=6).pack()
    confirm_btn = pill_btn(body, "Confirm Appointment", cmd=lambda: confirm(),
                           w=472, h=42, color=C_BLUE, hover=C_BLUE_D, fg=C_SURFACE,
                           bg=C_BG, font=("Segoe UI",9,"bold"))
    confirm_btn.pack()

    def get_booked_slots_for_date(date_str, sched_id):
        """Return set of booked slot start-times (as HH:MM strings) for this doctor+date."""
        try:
            conn2 = get_connection(); cur2 = conn2.cursor()
            # Use %H:%i to get zero-padded 24h time matching s_t.strftime("%H:%M")
            cur2.execute(
                "SELECT DATE_FORMAT(Appointment_Date, '%H:%i') FROM Appointments "
                "WHERE User_Doctor_id=%s AND DATE(Appointment_Date)=%s",
                (d_id, date_str))
            booked = {row[0] for row in cur2.fetchall()}
            cur2.close(); conn2.close()
            return booked
        except Exception as ex:
            print(f"[booked check error] {ex}")
            return set()

    def build_slots(date_str, sch):
        """Render 30-min slot buttons for the chosen date."""
        for w in slot_frame.winfo_children(): w.destroy()
        sel_slot.update({"start": None, "end": None,
                         "sched_id": sch['Schedule_id'], "day": sch['Day_Name']})

        slots = _generate_slots(sch['start_t'], sch['end_t'])
        booked_times = get_booked_slots_for_date(date_str, sch['Schedule_id'])

        if not slots:
            tk.Label(slot_frame, text="No slots available for this schedule.",
                     bg=C_BG, fg=C_TEXT3, font=FN_SMALL).pack(anchor="w")
            return

        slot_label.config(
            text=f"Pick a slot  ·  {sch['Day_Name']}  {date_str}  "
                 f"({sch['t_start']} – {sch['t_end']})")

        # ── helper: draw one slot canvas ──────────────────────────────────────
        def _draw(canvas, s_t, e_t, s_fmt, e_fmt, is_booked, hover=False):
            selected = (sel_slot["start"] == s_t)
            canvas.delete("all")
            if is_booked:
                rr(canvas, 0, 0, 148, 52, r=8, fill=C_SURFACE2)
                rr_outline(canvas, 0, 0, 148, 52, r=8, color=C_BORDER)
                canvas.create_text(74, 22, text=s_fmt,
                                   fill=C_TEXT3, font=("Segoe UI",8))
                canvas.create_text(74, 38, text="Booked",
                                   fill=C_RED, font=("Segoe UI",7,"bold"))
            elif selected:
                rr(canvas, 0, 0, 148, 52, r=8, fill=C_BLUE)
                canvas.create_text(74, 22, text=s_fmt,
                                   fill=C_SURFACE, font=("Segoe UI",8,"bold"))
                canvas.create_text(74, 38, text=f"– {e_fmt}",
                                   fill=C_SURFACE, font=("Segoe UI",7))
            elif hover:
                rr(canvas, 0, 0, 148, 52, r=8, fill=C_BLUE_L)
                rr_outline(canvas, 0, 0, 148, 52, r=8, color=C_BLUE)
                canvas.create_text(74, 22, text=s_fmt,
                                   fill=C_BLUE, font=("Segoe UI",8,"bold"))
                canvas.create_text(74, 38, text=f"– {e_fmt}",
                                   fill=C_TEXT2, font=("Segoe UI",7))
            else:
                rr(canvas, 0, 0, 148, 52, r=8, fill=C_SURFACE)
                rr_outline(canvas, 0, 0, 148, 52, r=8, color=C_BLUE)
                canvas.create_text(74, 22, text=s_fmt,
                                   fill=C_BLUE, font=("Segoe UI",8,"bold"))
                canvas.create_text(74, 38, text=f"– {e_fmt}",
                                   fill=C_TEXT2, font=("Segoe UI",7))

        # keep references so we can redraw all on selection change
        all_canvases = []   # list of (canvas, s_t, e_t, s_fmt, e_fmt, is_booked)

        def _redraw_all():
            for c, st, et, sf, ef, ib in all_canvases:
                _draw(c, st, et, sf, ef, ib)

        # ── build grid ────────────────────────────────────────────────────────
        col_count = 3
        row_f = None
        for idx, (s_t, e_t) in enumerate(slots):
            if idx % col_count == 0:
                row_f = tk.Frame(slot_frame, bg=C_BG)
                row_f.pack(fill="x", pady=2)

            s_str    = s_t.strftime("%H:%M")
            s_fmt    = _fmt_time(s_t)
            e_fmt    = _fmt_time(e_t)
            is_booked = s_str in booked_times

            cv = tk.Canvas(row_f, width=148, height=52, bg=C_BG,
                           highlightthickness=0, cursor="arrow" if is_booked else "hand2")
            cv.pack(side="left", padx=3)

            all_canvases.append((cv, s_t, e_t, s_fmt, e_fmt, is_booked))
            _draw(cv, s_t, e_t, s_fmt, e_fmt, is_booked)

            if not is_booked:
                # click → select this slot and redraw all
                def _on_click(event, _st=s_t, _et=e_t):
                    sel_slot["start"] = _st
                    sel_slot["end"]   = _et
                    _redraw_all()
                cv.bind("<Button-1>", _on_click)

                # hover effects
                def _on_enter(event, _c=cv, _st=s_t, _et=e_t, _sf=s_fmt, _ef=e_fmt):
                    if sel_slot["start"] != _st:
                        _draw(_c, _st, _et, _sf, _ef, False, hover=True)
                def _on_leave(event, _c=cv, _st=s_t, _et=e_t, _sf=s_fmt, _ef=e_fmt):
                    _draw(_c, _st, _et, _sf, _ef, False, hover=False)
                cv.bind("<Enter>", _on_enter)
                cv.bind("<Leave>", _on_leave)

    def build_cal():
        for w in grid_f.winfo_children(): w.destroy()
        month_lbl.config(text=f"{MONTHS[cur_m.get()-1]}  {cur_y.get()}")
        DOW = ["Mo","Tu","We","Th","Fr","Sa","Su"]
        for ci2, d in enumerate(DOW):
            c2 = C_BLUE if d in ("Sa","Su") else C_TEXT3
            tk.Label(grid_f, text=d, bg=C_SURFACE, fg=c2, font=FN_TINY, width=4).grid(row=0,column=ci2,pady=(0,4))
        fd, dim = cal_mod.monthrange(cur_y.get(), cur_m.get())
        today = datetime.now().date(); row, col = 1, fd
        for day in range(1, dim+1):
            d_obj = datetime(cur_y.get(), cur_m.get(), day).date()
            py_wd = d_obj.weekday(); past = d_obj < today
            avail = (py_wd in avail_wds) and not past
            ds = d_obj.strftime("%Y-%m-%d"); is_sel = (ds == sel_date.get())
            if is_sel:   bg_c,fg_c,fnt = C_BLUE,C_SURFACE,("Segoe UI",8,"bold")
            elif avail:  bg_c,fg_c,fnt = C_BLUE_L,C_BLUE,("Segoe UI",8,"bold")
            elif past:   bg_c,fg_c,fnt = C_SURFACE,C_TEXT3,FN_TINY
            else:        bg_c,fg_c,fnt = C_SURFACE,C_BORDER2,FN_TINY
            lbl = tk.Label(grid_f, text=str(day), width=4, height=2,
                           bg=bg_c, fg=fg_c, font=fnt,
                           cursor="hand2" if avail else "arrow", relief="flat")
            lbl.grid(row=row, column=col, padx=1, pady=1)
            if avail:
                sch = sched_map[py_wd]
                def _pick(ds=ds, sch=sch):
                    sel_date.set(ds)
                    sel_slot.update({"start":None,"end":None})
                    build_cal()
                    build_slots(ds, sch)
                lbl.bind("<Button-1>", lambda e, fn=_pick: fn())
                lbl.bind("<Enter>", lambda e, l=lbl, ds=ds:
                    l.config(bg=C_BLUE if ds==sel_date.get() else C_BLUE_L,
                             fg=C_SURFACE if ds==sel_date.get() else C_BLUE))
                lbl.bind("<Leave>", lambda e, l=lbl, ds=ds:
                    l.config(bg=C_BLUE if ds==sel_date.get() else C_BLUE_L,
                             fg=C_SURFACE if ds==sel_date.get() else C_BLUE))
            col += 1
            if col > 6: col = 0; row += 1

    def pm():
        m,y = cur_m.get()-1, cur_y.get()
        if m<1: m,y=12,y-1
        cur_m.set(m); cur_y.set(y); build_cal()
    def nm():
        m,y = cur_m.get()+1, cur_y.get()
        if m>12: m,y=1,y+1
        cur_m.set(m); cur_y.set(y); build_cal()
    for txt, fn2, side in [("‹",pm,"left"),("›",nm,"right")]:
        tk.Label(nav_row, text=txt, bg=C_SURFACE, fg=C_BLUE,
                 font=("Segoe UI",16,"bold"), cursor="hand2").pack(side=side)
    build_cal()

    # Legend
    leg = tk.Frame(body, bg=C_BG); leg.pack(anchor="w", pady=(4,0))
    for col_hex, lbl_t in [(C_BLUE,"Available"),(C_RED,"Booked"),(C_BORDER2,"Unavailable day")]:
        tk.Label(leg, text="●", bg=C_BG, fg=col_hex, font=("Segoe UI",9)).pack(side="left")
        tk.Label(leg, text=lbl_t+"  ", bg=C_BG, fg=C_TEXT3, font=FN_TINY).pack(side="left")

    def confirm():
        if not sel_date.get():
            messagebox.showwarning("Select Date","Please pick a date first.", parent=modal); return
        if sel_slot["start"] is None:
            messagebox.showwarning("Select Slot","Please pick a time slot.", parent=modal); return
        s_fmt = _fmt_time(sel_slot["start"])
        e_fmt = _fmt_time(sel_slot["end"])
        appt_dt = f"{sel_date.get()} {sel_slot['start'].strftime('%H:%M:%S')}"
        try:
            conn = get_connection(); cur = conn.cursor()
            # Double-check slot is still free before inserting
            cur.execute(
                "SELECT COUNT(*) FROM Appointments "
                "WHERE User_Doctor_id=%s AND DATE(Appointment_Date)=%s "
                "AND DATE_FORMAT(Appointment_Date,'%%H:%%i')=%s",
                (d_id, sel_date.get(), sel_slot['start'].strftime('%H:%M')))
            if cur.fetchone()[0] > 0:
                conn.close()
                messagebox.showwarning("Slot Taken",
                    f"The {s_fmt} slot was just booked by someone else.\n"
                    "Please pick another slot.", parent=modal)
                # refresh slots to show updated availability
                sch = sched_map[datetime.strptime(sel_date.get(), "%Y-%m-%d").date().weekday()]
                build_slots(sel_date.get(), sch)
                return
            cur.execute(
                "INSERT INTO Appointments (Appointment_Date,User_Doctor_id,Schedule_id,User_Patient_id) "
                "VALUES (%s,%s,%s,%s)",
                (appt_dt, d_id, sel_slot["sched_id"], p_id))
            conn.commit(); conn.close()
            messagebox.showinfo("Booked! ✓",
                f"Appointment confirmed with {d_name}\n"
                f"{sel_date.get()}  ·  {sel_slot['day']}\n"
                f"{s_fmt} – {e_fmt}", parent=modal)
            modal.destroy()
            if on_booked: on_booked()
        except Exception as ex:
            messagebox.showerror("Error", str(ex), parent=modal)

# ══════════════════════════════════════════════════════════════════════════════
#  INSURANCE MODAL
# ══════════════════════════════════════════════════════════════════════════════
def open_insurance_modal(patient_id, existing_insurance, on_saved=None):
    modal = tk.Toplevel(); modal.title("Insurance")
    modal.geometry("480x420"); modal.resizable(False,False)
    modal.configure(bg=C_BG); modal.grab_set()

    hdr = tk.Frame(modal, bg=C_SURFACE, height=68); hdr.pack(fill="x"); hdr.pack_propagate(False)
    tk.Frame(hdr, bg=C_PURPLE, width=4).pack(side="left", fill="y")
    hi = tk.Frame(hdr, bg=C_SURFACE); hi.pack(side="left", padx=20, pady=14, fill="both", expand=True)
    tk.Label(hi, text="Health Insurance", bg=C_SURFACE, fg=C_TEXT, font=FN_HEAD).pack(anchor="w")
    tk.Label(hi, text="Manage your coverage", bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(anchor="w")

    body = tk.Frame(modal, bg=C_BG); body.pack(fill="both", expand=True, padx=28, pady=20)

    if existing_insurance:
        ins = existing_insurance
        card = tk.Frame(body, bg=C_SURFACE, highlightbackground=C_PURPLE, highlightthickness=1)
        card.pack(fill="x", pady=(0,16))
        tk.Frame(card, bg=C_PURPLE, height=3).pack(fill="x")
        ci = tk.Frame(card, bg=C_SURFACE); ci.pack(padx=20, pady=18, fill="x")
        tk.Label(ci, text="PROVIDER", bg=C_SURFACE, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w")
        tk.Label(ci, text=ins['Company_Name'], bg=C_SURFACE, fg=C_TEXT, font=FN_HEAD).pack(anchor="w", pady=(2,12))
        tk.Label(ci, text="COVERAGE", bg=C_SURFACE, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w")
        cov = ins['Coverage_Percentage']
        cov_c = C_GREEN if cov>=75 else C_AMBER if cov>=50 else C_RED
        cov_l = C_GREEN_L if cov>=75 else C_AMBER_L if cov>=50 else C_RED_L
        tk.Label(ci, text=f"{cov}%", bg=C_SURFACE, fg=cov_c, font=("Segoe UI",28,"bold")).pack(anchor="w")
        bar_bg = tk.Frame(ci, bg=C_BORDER, height=8); bar_bg.pack(fill="x", pady=(6,0))
        tk.Frame(bar_bg, bg=cov_c, height=8).place(relwidth=cov/100, relheight=1)
        tk.Label(body, text="Your insurance is active.", bg=C_BG, fg=C_TEXT2, font=FN_SMALL).pack(pady=8)
        pill_btn(body, "Close", modal.destroy, w=424, h=40, color=C_BLUE, hover=C_BLUE_D,
                 fg=C_SURFACE, bg=C_BG).pack(pady=8)
    else:
        tk.Label(body, text="No insurance linked. Select a provider:", bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack(anchor="w", pady=(0,12))
        try:
            conn = get_connection(); cur = conn.cursor(dictionary=True)
            cur.execute("SELECT Company_id, Company_Name, Coverage_Percentage FROM Insurance_Company ORDER BY Company_Name")
            companies = cur.fetchall(); cur.close(); conn.close()
        except Exception as ex:
            tk.Label(body, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(); return

        tk.Label(body, text="INSURANCE PROVIDER", bg=C_BG, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w", pady=(0,4))
        company_var = tk.StringVar()
        company_map = {f"{c['Company_Name']}  ({c['Coverage_Percentage']}% coverage)": c['Company_id'] for c in companies}
        options = list(company_map.keys())
        company_var.set(options[0] if options else "")
        fr = tk.Frame(body, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
        fr.pack(fill="x", pady=(0,16))
        om = tk.OptionMenu(fr, company_var, *options)
        om.config(bg=C_SURFACE, fg=C_TEXT, font=FN_BODY, relief="flat", bd=0,
                  highlightthickness=0, activebackground=C_BORDER, width=42)
        om["menu"].config(bg=C_SURFACE, fg=C_TEXT, font=FN_SMALL,
                          activebackground=C_BLUE_L, activeforeground=C_BLUE)
        om.pack(fill="x", padx=4, pady=6)
        err_lbl = tk.Label(body, text="", bg=C_BG, fg=C_RED, font=FN_SMALL); err_lbl.pack(anchor="w")

        def save_ins():
            sel = company_var.get()
            if not sel: err_lbl.config(text="Please select a provider."); return
            cid = company_map[sel]
            try:
                conn = get_connection(); cur = conn.cursor()
                cur.execute("INSERT INTO Insurance (Company_id, User_Patient_id) VALUES (%s,%s)", (cid, patient_id))
                conn.commit(); conn.close()
                messagebox.showinfo("Saved ✓", "Insurance added!", parent=modal)
                modal.destroy()
                if on_saved: on_saved()
            except Exception as ex:
                err_lbl.config(text=f"Error: {ex}")

        pill_btn(body, "Add Insurance  →", save_ins, w=424, h=42,
                 color=C_PURPLE, hover="#7C3AED", fg=C_SURFACE, bg=C_BG,
                 font=("Segoe UI",9,"bold")).pack(pady=8)

# ══════════════════════════════════════════════════════════════════════════════
#  MEDICAL REPORTS PANEL  — Patient
# ══════════════════════════════════════════════════════════════════════════════
def panel_medical_reports(parent, user):
    pid = user["User_id"]
    pg = scrollable(parent, bg=C_BG)
    hdr_f = tk.Frame(pg, bg=C_BG); hdr_f.pack(fill="x", padx=28, pady=(28,4))
    tk.Label(hdr_f, text="Medical Reports", bg=C_BG, fg=C_TEXT, font=FN_DISPLAY).pack(side="left")

    try:
        conn = get_connection(); cur = conn.cursor(dictionary=True)
        cur.execute("""SELECT mr.Report_id, mr.Report_Date, mr.Diagnosis,
                              u.First_Name, u.Last_Name, s.Specialization_Name
                       FROM Medical_Reports mr
                       JOIN Users u ON mr.User_Doctor_id=u.User_id
                       JOIN Doctors d ON d.User_Doctor_id=u.User_id
                       JOIN Specialization s ON d.Specialization_id=s.Specialization_id
                       WHERE mr.User_Patient_id=%s ORDER BY mr.Report_Date DESC""", (pid,))
        reports = cur.fetchall()
        meds_map = {}; tests_map = {}
        if reports:
            ids = tuple(r['Report_id'] for r in reports)
            ph = ','.join(['%s']*len(ids))
            cur.execute(f"SELECT Report_id, Medicine_Name FROM Medicines WHERE Report_id IN ({ph})", ids)
            for row in cur.fetchall(): meds_map.setdefault(row['Report_id'],[]).append(row['Medicine_Name'])
            cur.execute(f"SELECT Report_id, Test_Result FROM Test_Results WHERE Report_id IN ({ph})", ids)
            for row in cur.fetchall(): tests_map.setdefault(row['Report_id'],[]).append(row['Test_Result'])
        cur.close(); conn.close()
    except Exception as ex:
        tk.Label(pg, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(padx=28); return

    if not reports:
        ef = tk.Frame(pg, bg=C_BG); ef.pack(expand=True, pady=80)
        tk.Label(ef, text="No medical reports yet", bg=C_BG, fg=C_TEXT, font=("Segoe UI",14,"bold")).pack(pady=6)
        tk.Label(ef, text="Reports from your doctors will appear here.", bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack()
        return

    for rep in reports:
        sp = rep['Specialization_Name']
        sp_tint, sp_ac, sp_ic = SPEC.get(sp, (C_BLUE_L, C_BLUE, "✚"))
        rdate = str(rep['Report_Date'])[:10]
        meds = meds_map.get(rep['Report_id'], [])
        tests = tests_map.get(rep['Report_id'], [])

        card = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
        card.pack(fill="x", padx=28, pady=5)
        tk.Frame(card, bg=C_TEAL, width=4).pack(side="left", fill="y")

        av = tk.Canvas(card, width=50, height=50, bg=C_TEAL_L, highlightthickness=0)
        av.pack(side="left", padx=14, pady=14)
        av.create_oval(4,4,46,46, fill=C_TEAL_L, outline=C_TEAL)
        av.create_text(25,25, text="📋", font=("Segoe UI",18))

        inf = tk.Frame(card, bg=C_SURFACE); inf.pack(side="left", fill="both", expand=True, pady=14)
        top_r = tk.Frame(inf, bg=C_SURFACE); top_r.pack(anchor="w")
        tk.Label(top_r, text=f"Dr. {rep['First_Name']} {rep['Last_Name']}",
                 bg=C_SURFACE, fg=C_TEXT, font=FN_SUBH).pack(side="left")
        tk.Label(top_r, text=f"  ·  {sp}", bg=C_SURFACE, fg=sp_ac, font=FN_TINY).pack(side="left")
        tk.Label(inf, text=rdate, bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(anchor="w", pady=(2,4))
        diag_r = tk.Frame(inf, bg=C_SURFACE); diag_r.pack(anchor="w")
        tk.Label(diag_r, text="Diagnosis: ", bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(side="left")
        tk.Label(diag_r, text=rep['Diagnosis'], bg=C_SURFACE, fg=C_AMBER, font=("Segoe UI",8,"bold")).pack(side="left")
        if meds:
            mr = tk.Frame(inf, bg=C_SURFACE); mr.pack(anchor="w", pady=(4,0))
            tk.Label(mr, text="Medicines: ", bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(side="left")
            for m in meds:
                tk.Label(mr, text=m, bg=C_GREEN_L, fg=C_GREEN, font=FN_TINY, padx=6, pady=2).pack(side="left", padx=2)
        if tests:
            tr = tk.Frame(inf, bg=C_SURFACE); tr.pack(anchor="w", pady=(4,0))
            tk.Label(tr, text="Tests: ", bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(side="left")
            for t in tests:
                tk.Label(tr, text=t, bg=C_BLUE_L, fg=C_BLUE, font=FN_TINY, padx=6, pady=2).pack(side="left", padx=2)

# ══════════════════════════════════════════════════════════════════════════════
#  FIND DOCTOR PANEL  — search + filter + sort
# ══════════════════════════════════════════════════════════════════════════════
def panel_find_doctor(parent, user):
    pid = user["User_id"]
    outer = tk.Frame(parent, bg=C_BG); outer.pack(fill="both", expand=True)

    # ── Toolbar ───────────────────────────────────────────────────────────────
    toolbar = tk.Frame(outer, bg=C_SURFACE, height=112)
    toolbar.pack(fill="x"); toolbar.pack_propagate(False)
    tk.Frame(toolbar, bg=C_BLUE, height=3).pack(fill="x")

    tb = tk.Frame(toolbar, bg=C_SURFACE); tb.pack(fill="x", padx=28, pady=10)
    tk.Label(tb, text="Find a Specialist", bg=C_SURFACE, fg=C_TEXT, font=FN_DISPLAY).pack(anchor="w", pady=(0,8))

    ctrl = tk.Frame(tb, bg=C_SURFACE); ctrl.pack(fill="x")

    # Search box
    sf = tk.Frame(ctrl, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
    sf.pack(side="left", padx=(0,10))
    tk.Label(sf, text="🔍", bg=C_SURFACE, fg=C_TEXT3, font=("Segoe UI",9)).pack(side="left", padx=(8,2))
    search_var = tk.StringVar()
    PLACEHOLDER = "Search by name..."
    search_e = tk.Entry(sf, textvariable=search_var, font=FN_BODY,
                        fg=C_TEXT3, bg=C_SURFACE, insertbackground=C_BLUE,
                        relief="flat", bd=0, width=22)
    search_e.insert(0, PLACEHOLDER)
    def sf_in(e):
        if search_e.get() == PLACEHOLDER: search_e.delete(0, tk.END); search_e.config(fg=C_TEXT)
        sf.config(highlightbackground=C_BLUE)
    def sf_out(e):
        if not search_e.get(): search_e.insert(0, PLACEHOLDER); search_e.config(fg=C_TEXT3)
        sf.config(highlightbackground=C_BORDER)
    search_e.bind("<FocusIn>", sf_in); search_e.bind("<FocusOut>", sf_out)
    search_e.pack(side="left", ipady=7, padx=(0,8))

    # Specialization filter
    spec_var = tk.StringVar(value="All Specializations")
    spec_options = ["All Specializations"] + list(SPEC.keys())
    spec_f = tk.Frame(ctrl, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
    spec_f.pack(side="left", padx=(0,10))
    spec_om = tk.OptionMenu(spec_f, spec_var, *spec_options)
    spec_om.config(bg=C_SURFACE, fg=C_TEXT, font=FN_BODY, relief="flat", bd=0,
                   highlightthickness=0, activebackground=C_BORDER, width=18)
    spec_om["menu"].config(bg=C_SURFACE, fg=C_TEXT, font=FN_SMALL,
                           activebackground=C_BLUE_L, activeforeground=C_BLUE)
    spec_om.pack(padx=4, pady=6)

    # Sort toggle buttons
    sort_var = tk.StringVar(value="rating")
    sort_f = tk.Frame(ctrl, bg=C_SURFACE); sort_f.pack(side="left")
    redraw_fns = []

    def make_sort_btn(label, val):
        cv = tk.Canvas(sort_f, width=88, height=30, bg=C_SURFACE, highlightthickness=0)
        cv.pack(side="left", padx=2)
        def draw():
            cv.delete("all")
            active = sort_var.get() == val
            rr(cv, 0, 0, 88, 30, r=15, fill=C_BLUE if active else C_SURFACE)
            if not active:
                rr_outline(cv, 0, 0, 88, 30, r=15, color=C_BORDER2)
            cv.create_text(44, 15, text=label,
                           fill=C_SURFACE if active else C_TEXT2,
                           font=("Segoe UI",7,"bold"))
        draw()
        def click():
            sort_var.set(val)
            for fn in redraw_fns: fn()
            apply_filters()
        cv.bind("<Button-1>", lambda e: click())
        return draw

    redraw_fns.append(make_sort_btn("★ Rating", "rating"))
    redraw_fns.append(make_sort_btn("A–Z Name", "name"))
    redraw_fns.append(make_sort_btn("$ Fees",   "fees"))

    # ── Results area ──────────────────────────────────────────────────────────
    results_outer = tk.Frame(outer, bg=C_BG); results_outer.pack(fill="both", expand=True)
    results_pg = scrollable(results_outer, bg=C_BG)

    try:
        conn = get_connection(); cur = conn.cursor(dictionary=True)
        cur.execute("""SELECT u.User_id, u.First_Name, u.Last_Name,
                              s.Specialization_Name, d.Consultant_Fees AS fees,
                              d.Experience_Years AS yrs,
                              ROUND(COALESCE(AVG(r.Rating),0),1) AS rating
                       FROM Doctors d
                       JOIN Users u ON d.User_Doctor_id=u.User_id
                       JOIN Specialization s ON d.Specialization_id=s.Specialization_id
                       LEFT JOIN Appointments a ON a.User_Doctor_id=u.User_id
                       LEFT JOIN Reviews r ON r.Appointment_id=a.Appointment_id
                       GROUP BY u.User_id,u.First_Name,u.Last_Name,
                                s.Specialization_Name,d.Consultant_Fees,d.Experience_Years""")
        all_doctors = cur.fetchall(); cur.close(); conn.close()
    except Exception as ex:
        tk.Label(results_pg, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(padx=28); return

    def apply_filters(*_):
        for w in results_pg.winfo_children(): w.destroy()
        query = search_var.get().strip().lower()
        if query == PLACEHOLDER.lower(): query = ""
        spec_filter = spec_var.get()
        sort_key = sort_var.get()

        filtered = []
        for doc in all_doctors:
            fname = f"{doc['First_Name']} {doc['Last_Name']}"
            if query and query not in fname.lower(): continue
            if spec_filter != "All Specializations" and doc['Specialization_Name'] != spec_filter: continue
            filtered.append(doc)

        if sort_key == "rating":
            filtered.sort(key=lambda d: float(d['rating']), reverse=True)
        elif sort_key == "name":
            # Sort by First_Name then Last_Name — ignores the "Dr." prefix entirely
            filtered.sort(key=lambda d: (d['First_Name'].lower(), d['Last_Name'].lower()))
        elif sort_key == "fees":
            filtered.sort(key=lambda d: d['fees'])

        if not filtered:
            tk.Label(results_pg, text="No doctors match your search.",
                     bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack(pady=60)
            return

        from collections import OrderedDict
        if sort_key == "rating":
            sec_hdr(results_pg, f"★  Sorted by Rating — {len(filtered)} doctors", accent=C_AMBER)
            for doc in filtered: _render_doc_card(doc)
        elif sort_key == "name":
            sec_hdr(results_pg, f"A–Z  Sorted by First Name — {len(filtered)} doctors", accent=C_BLUE)
            for doc in filtered: _render_doc_card(doc)
        else:
            groups = OrderedDict()
            for d in filtered:
                groups.setdefault(d['Specialization_Name'], []).append(d)
            for spec, docs in groups.items():
                sp_tint, sp_ac, sp_ic = SPEC.get(spec, (C_BLUE_L, C_BLUE, "✚"))
                sec_hdr(results_pg, f"{sp_ic}  {spec}", accent=sp_ac)
                for doc in docs: _render_doc_card(doc)

    def _render_doc_card(doc):
        sp = doc['Specialization_Name']
        sp_tint, sp_ac, sp_ic = SPEC.get(sp, (C_BLUE_L, C_BLUE, "✚"))
        fname = f"Dr. {doc['First_Name']} {doc['Last_Name']}"
        rating = float(doc['rating'])

        card = tk.Frame(results_pg, bg=C_SURFACE,
                        highlightbackground=C_BORDER, highlightthickness=1)
        card.pack(fill="x", padx=28, pady=4)
        card.bind("<Enter>", lambda e: card.config(highlightbackground=sp_ac))
        card.bind("<Leave>", lambda e: card.config(highlightbackground=C_BORDER))

        tk.Frame(card, bg=sp_ac, width=4).pack(side="left", fill="y")

        av_sz = 54
        av = tk.Canvas(card, width=av_sz, height=av_sz, bg=sp_tint, highlightthickness=0)
        av.pack(side="left", padx=14, pady=14)
        av.create_oval(4,4,av_sz-4,av_sz-4, fill=sp_tint, outline=sp_ac, width=1)
        av.create_text(av_sz//2, av_sz//2, text=sp_ic, fill=sp_ac, font=("Segoe UI",20))

        inf = tk.Frame(card, bg=C_SURFACE); inf.pack(side="left", fill="both", expand=True, pady=14)
        name_r = tk.Frame(inf, bg=C_SURFACE); name_r.pack(anchor="w")
        tk.Label(name_r, text=fname, bg=C_SURFACE, fg=C_TEXT, font=FN_SUBH).pack(side="left")
        if rating > 0:
            full = int(rating)
            stars = "★"*full + "☆"*(5-full)
            tk.Label(name_r, text=f"  {stars}  {rating}",
                     bg=C_SURFACE, fg=C_AMBER, font=("Segoe UI",8)).pack(side="left")
        else:
            tk.Label(name_r, text="  No reviews yet", bg=C_SURFACE, fg=C_TEXT3, font=FN_TINY).pack(side="left")

        tk.Label(inf, text=sp, bg=C_SURFACE, fg=sp_ac, font=FN_TINY).pack(anchor="w", pady=(1,5))
        tags_r = tk.Frame(inf, bg=C_SURFACE); tags_r.pack(anchor="w")
        tk.Label(tags_r, text=f"  {doc['fees']} EGP  ", bg=C_GREEN_L, fg=C_GREEN,
                 font=FN_TINY, pady=3).pack(side="left", padx=(0,5))
        tk.Label(tags_r, text=f"  {doc['yrs']} yrs exp  ", bg=C_BLUE_L, fg=C_BLUE,
                 font=FN_TINY, pady=3).pack(side="left")

        br = tk.Frame(card, bg=C_SURFACE); br.pack(side="right", padx=16)
        pill_btn(br, "Book  →", w=88, h=32, color=C_BLUE, hover=C_BLUE_D,
                 fg=C_SURFACE, bg=C_SURFACE, font=("Segoe UI",8,"bold"),
                 cmd=lambda did=doc['User_id'], dn=fname, ds=sp:
                     open_booking_modal(pid, did, dn, ds)).pack(pady=14)

    search_var.trace_add("write", lambda *_: apply_filters())
    spec_var.trace_add("write", lambda *_: apply_filters())
    apply_filters()

# ══════════════════════════════════════════════════════════════════════════════
#  MY BOOKINGS PANEL  — Patient
# ══════════════════════════════════════════════════════════════════════════════
def panel_my_bookings(parent, user, refresh_overview=None):
    pid = user["User_id"]
    def load():
        clear(parent)
        pg = scrollable(parent, bg=C_BG)
        hdr_f = tk.Frame(pg, bg=C_BG); hdr_f.pack(fill="x", padx=28, pady=(28,4))
        tk.Label(hdr_f, text="My Appointments", bg=C_BG, fg=C_TEXT, font=FN_DISPLAY).pack(side="left")
        try:
            conn = get_connection(); cur = conn.cursor(dictionary=True)
            cur.execute("""SELECT a.Appointment_id, a.Appointment_Date,
                                  u.First_Name, u.Last_Name, s.Specialization_Name,
                                  sc.Day_Name,
                                  TIME_FORMAT(a.Appointment_Date,'%I:%i %p') AS slot_start,
                                  DATE_FORMAT(a.Appointment_Date,'%H:%i')    AS slot_raw,
                                  TIME_FORMAT(sc.Start_Time,'%I:%i %p') AS t_start,
                                  TIME_FORMAT(sc.End_Time,'%I:%i %p')   AS t_end,
                                  r.Review_id, r.Rating
                           FROM Appointments a
                           JOIN Users u ON a.User_Doctor_id=u.User_id
                           JOIN Doctors d ON d.User_Doctor_id=u.User_id
                           JOIN Specialization s ON d.Specialization_id=s.Specialization_id
                           JOIN Schedules sc ON a.Schedule_id=sc.Schedule_id
                           LEFT JOIN Reviews r ON r.Appointment_id=a.Appointment_id
                           WHERE a.User_Patient_id=%s ORDER BY a.Appointment_Date DESC""", (pid,))
            appts = cur.fetchall(); cur.close(); conn.close()
        except Exception as ex:
            tk.Label(pg, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(padx=28); return

        if not appts:
            ef = tk.Frame(pg, bg=C_BG); ef.pack(expand=True, pady=80)
            tk.Label(ef, text="No appointments yet", bg=C_BG, fg=C_TEXT,
                     font=("Segoe UI",14,"bold")).pack(pady=6)
            tk.Label(ef, text="Find a specialist and book your first visit.",
                     bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack()
            return

        now_dt = datetime.now()
        today  = now_dt.date()

        upcoming = [a for a in appts
                    if datetime.strptime(str(a['Appointment_Date'])[:16],"%Y-%m-%d %H:%M") > now_dt]
        past     = [a for a in appts
                    if datetime.strptime(str(a['Appointment_Date'])[:16],"%Y-%m-%d %H:%M") <= now_dt]

        def open_rate_modal(ap_id, doc_name, ap_date_str):
            """Star-rating popup for a completed appointment."""
            m = tk.Toplevel(); m.title("Rate Appointment")
            m.geometry("400x280"); m.resizable(False,False)
            m.configure(bg=C_BG); m.grab_set()

            hdr2 = tk.Frame(m, bg=C_SURFACE, height=64); hdr2.pack(fill="x"); hdr2.pack_propagate(False)
            tk.Frame(hdr2, bg=C_AMBER, width=4).pack(side="left", fill="y")
            hi2 = tk.Frame(hdr2, bg=C_SURFACE); hi2.pack(side="left", padx=18, pady=12, fill="both", expand=True)
            tk.Label(hi2, text="Rate Your Appointment", bg=C_SURFACE, fg=C_TEXT, font=FN_HEAD).pack(anchor="w")
            tk.Label(hi2, text=f"{doc_name}  ·  {ap_date_str}",
                     bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(anchor="w")

            body2 = tk.Frame(m, bg=C_BG); body2.pack(fill="both", expand=True, padx=28, pady=20)
            tk.Label(body2, text="How was your experience?",
                     bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack(anchor="w", pady=(0,12))

            rating_var = tk.IntVar(value=0)
            star_cvs = []

            def draw_stars(hovered=0):
                selected = rating_var.get()
                for i, cv2 in enumerate(star_cvs, 1):
                    cv2.delete("all")
                    filled = (i <= hovered) or (hovered == 0 and i <= selected)
                    cv2.create_text(20, 20, text="★" if filled else "☆",
                                    fill=C_AMBER if filled else C_BORDER2,
                                    font=("Segoe UI",24))

            stars_row = tk.Frame(body2, bg=C_BG); stars_row.pack(anchor="w", pady=(0,16))
            for i in range(1, 6):
                cv2 = tk.Canvas(stars_row, width=40, height=40, bg=C_BG,
                                highlightthickness=0, cursor="hand2")
                cv2.pack(side="left", padx=2)
                star_cvs.append(cv2)
                cv2.bind("<Enter>",    lambda e, n=i: draw_stars(n))
                cv2.bind("<Leave>",    lambda e: draw_stars(0))
                cv2.bind("<Button-1>", lambda e, n=i: (rating_var.set(n), draw_stars(0)))
            draw_stars(0)

            err3 = tk.Label(body2, text="", bg=C_BG, fg=C_RED, font=FN_SMALL)
            err3.pack(anchor="w")

            def submit_rating():
                rat = rating_var.get()
                if rat == 0:
                    err3.config(text="Please select a star rating."); return
                try:
                    # Use admin_id=1 as placeholder — Reviews.Admin_id is required by schema
                    conn2 = get_connection(); cur2 = conn2.cursor()
                    cur2.execute("SELECT Admin_id FROM Admins LIMIT 1")
                    admin_row = cur2.fetchone()
                    admin_id_val = admin_row[0] if admin_row else 1
                    cur2.execute(
                        "INSERT INTO Reviews (Rating, Appointment_id, Admin_id) VALUES (%s,%s,%s)",
                        (rat, ap_id, admin_id_val))
                    conn2.commit(); conn2.close()
                    messagebox.showinfo("Thank you! ✓",
                        f"You rated this appointment {'★'*rat}{'☆'*(5-rat)}", parent=m)
                    m.destroy(); load()
                except Exception as ex3:
                    err3.config(text=f"Error: {ex3}")

            pill_btn(body2, "Submit Rating  →", submit_rating, w=344, h=40,
                     color=C_AMBER, hover="#D97706", fg=C_SURFACE, bg=C_BG,
                     font=("Segoe UI",9,"bold")).pack()

        def render_group(items, title, accent, accent_l):
            if not items: return
            sec_hdr(pg, title, accent=accent)
            for ap in items:
                sp = ap['Specialization_Name']
                sp_tint, sp_ac, sp_ic = SPEC.get(sp, (C_BLUE_L, C_BLUE, "✚"))
                ap_dt   = datetime.strptime(str(ap['Appointment_Date'])[:16], "%Y-%m-%d %H:%M")
                ap_date = ap_dt.strftime("%Y-%m-%d")
                is_up   = ap_dt > now_dt
                # compute slot end = slot_start + 30 min
                from datetime import timedelta as _td3
                slot_end_dt = ap_dt + _td3(minutes=30)
                slot_str = f"{ap_dt.strftime('%I:%M %p').lstrip('0')} – {slot_end_dt.strftime('%I:%M %p').lstrip('0')}"

                card = tk.Frame(pg, bg=C_SURFACE,
                                highlightbackground=C_BORDER, highlightthickness=1)
                card.pack(fill="x", padx=28, pady=4)
                tk.Frame(card, bg=accent, width=4).pack(side="left", fill="y")

                av = tk.Canvas(card, width=50, height=50, bg=sp_tint, highlightthickness=0)
                av.pack(side="left", padx=14, pady=12)
                av.create_text(25,25, text=sp_ic, fill=sp_ac, font=("Segoe UI",18))

                inf = tk.Frame(card, bg=C_SURFACE)
                inf.pack(side="left", fill="both", expand=True, pady=12)
                tk.Label(inf, text=f"Dr. {ap['First_Name']} {ap['Last_Name']}",
                         bg=C_SURFACE, fg=C_TEXT, font=FN_SUBH).pack(anchor="w")
                tk.Label(inf, text=sp, bg=C_SURFACE, fg=sp_ac,
                         font=FN_TINY).pack(anchor="w", pady=(1,4))
                dr = tk.Frame(inf, bg=C_SURFACE); dr.pack(anchor="w")
                tk.Label(dr, text=ap_date,
                         bg=C_SURFACE, fg=C_TEXT2, font=FN_SMALL).pack(side="left", padx=(0,10))
                tk.Label(dr, text=f"{ap['Day_Name']}  ·  {slot_str}",
                         bg=C_SURFACE, fg=C_TEXT2, font=FN_SMALL).pack(side="left")

                right = tk.Frame(card, bg=C_SURFACE); right.pack(side="right", padx=16)
                tk.Label(right, text="Upcoming" if is_up else "Past",
                         bg=accent_l, fg=accent,
                         font=FN_LABEL, padx=8, pady=4).pack(pady=(12,6))

                if is_up:
                    # Cancel button
                    ap_id = ap['Appointment_id']
                    def do_cancel(aid=ap_id,
                                  dn=f"Dr. {ap['First_Name']} {ap['Last_Name']}",
                                  dd=ap_date):
                        if not messagebox.askyesno(
                            "Cancel", f"Cancel appointment with {dn} on {dd}?"): return
                        try:
                            c2 = get_connection(); cu2 = c2.cursor()
                            cu2.execute(
                                "DELETE FROM Appointments WHERE Appointment_id=%s", (aid,))
                            c2.commit(); c2.close()
                            if refresh_overview: refresh_overview()
                            load()
                        except Exception as ex2:
                            messagebox.showerror("Error", str(ex2))
                    ghost_btn(right, "✕  Cancel", do_cancel, w=88, h=28,
                              color=C_RED, hover_color=C_RED,
                              text_col=C_RED, bg=C_SURFACE).pack(pady=(0,10))
                else:
                    # Past appointment — show rating or Rate button
                    ap_id = ap['Appointment_id']
                    if ap['Review_id']:
                        # Already rated
                        stars_txt = "★" * ap['Rating'] + "☆" * (5 - ap['Rating'])
                        tk.Label(right, text=stars_txt, bg=C_AMBER_L, fg=C_AMBER,
                                 font=("Segoe UI",10), padx=6, pady=3).pack(pady=(0,10))
                    else:
                        # Not yet rated — show Rate button
                        def do_rate(aid=ap_id,
                                    dn=f"Dr. {ap['First_Name']} {ap['Last_Name']}",
                                    dd=ap_date):
                            open_rate_modal(aid, dn, dd)
                        ghost_btn(right, "★ Rate", do_rate, w=88, h=28,
                                  color=C_AMBER, hover_color=C_AMBER,
                                  text_col=C_AMBER, bg=C_SURFACE).pack(pady=(0,10))

        render_group(upcoming, "Upcoming", C_GREEN,  C_GREEN_L)
        render_group(past,     "Past",     C_TEXT3,  C_SURFACE2)
    load()

# ══════════════════════════════════════════════════════════════════════════════
#  PATIENT OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
def panel_overview(parent, user, nav_cb):
    pid = user["User_id"]
    pg = scrollable(parent, bg=C_BG)

    # ── Hero banner ───────────────────────────────────────────────────────────
    hero = tk.Canvas(pg, height=148, bg=C_BG, highlightthickness=0)
    hero.pack(fill="x")
    def draw_hero(e=None):
        w = hero.winfo_width() or 900
        hero.delete("all")
        # white card with blue top bar
        hero.create_rectangle(0, 0, w, 148, fill=C_SURFACE, outline="")
        hero.create_rectangle(0, 0, w, 4, fill=C_BLUE, outline="")
        # soft blue circle decoration
        hero.create_oval(w-160, -60, w+60, 160, fill=C_BLUE_L, outline="")
        hero.create_oval(w-120, -20, w+20, 120, fill=C_PANEL, outline="")
        # text
        hero.create_text(32, 55, text=f"Hello, {user['First_Name']} 👋",
                         fill=C_TEXT, font=("Segoe UI",18,"bold"), anchor="w")
        hero.create_text(32, 85, text="Welcome back to your health dashboard",
                         fill=C_TEXT2, font=("Segoe UI",9), anchor="w")
        # bottom border
        hero.create_rectangle(0, 146, w, 148, fill=C_BORDER, outline="")
    hero.bind("<Configure>", draw_hero)
    hero.after(50, draw_hero)

    # ── Stats ─────────────────────────────────────────────────────────────────
    try:
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Appointments WHERE User_Patient_id=%s",(pid,))
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM Appointments WHERE User_Patient_id=%s AND Appointment_Date>=%s",
                    (pid, datetime.now().strftime("%Y-%m-%d")))
        upcoming = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM Medical_Reports WHERE User_Patient_id=%s",(pid,))
        rpts = cur.fetchone()[0]
        cur.close(); conn.close()
    except: total=upcoming=rpts=0

    stats_row = tk.Frame(pg, bg=C_BG); stats_row.pack(fill="x", padx=28, pady=16)
    stat_card(stats_row, total,    "Total Bookings", C_BLUE,   C_BLUE_L)
    stat_card(stats_row, upcoming, "Upcoming",       C_GREEN,  C_GREEN_L)
    stat_card(stats_row, rpts,     "Reports",        C_TEAL,   C_TEAL_L)

    # ── Insurance card ────────────────────────────────────────────────────────
    sec_hdr(pg, "Insurance", accent=C_PURPLE)
    ins_card = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
    ins_card.pack(fill="x", padx=28, pady=4)
    tk.Frame(ins_card, bg=C_PURPLE, width=4).pack(side="left", fill="y")

    ins_av = tk.Canvas(ins_card, width=50, height=50, bg=C_PURPLE_L, highlightthickness=0)
    ins_av.pack(side="left", padx=14, pady=14)
    ins_av.create_oval(4,4,46,46, fill=C_PURPLE_L, outline=C_PURPLE)
    ins_av.create_text(25,25, text="🛡", font=("Segoe UI",18))

    ins_inf = tk.Frame(ins_card, bg=C_SURFACE); ins_inf.pack(side="left", fill="both", expand=True, pady=14)
    ins_right = tk.Frame(ins_card, bg=C_SURFACE); ins_right.pack(side="right", padx=16)

    def refresh_ins():
        clear(ins_inf); clear(ins_right)
        try:
            conn = get_connection(); cur = conn.cursor(dictionary=True)
            cur.execute("""SELECT ic.Company_Name, ic.Coverage_Percentage
                           FROM Insurance i JOIN Insurance_Company ic ON i.Company_id=ic.Company_id
                           WHERE i.User_Patient_id=%s LIMIT 1""", (pid,))
            ins_data = cur.fetchone(); cur.close(); conn.close()
        except: ins_data = None
        if ins_data:
            tk.Label(ins_inf, text=ins_data['Company_Name'], bg=C_SURFACE, fg=C_TEXT, font=FN_SUBH).pack(anchor="w")
            cov = ins_data['Coverage_Percentage']
            cov_c = C_GREEN if cov>=75 else C_AMBER if cov>=50 else C_RED
            cov_l = C_GREEN_L if cov>=75 else C_AMBER_L if cov>=50 else C_RED_L
            tk.Label(ins_inf, text=f"{cov}% coverage", bg=C_SURFACE, fg=cov_c,
                     font=("Segoe UI",8,"bold")).pack(anchor="w", pady=(2,0))
            tk.Label(ins_right, text="Active ✓", bg=C_GREEN_L, fg=C_GREEN,
                     font=FN_LABEL, padx=8, pady=4).pack(pady=14)
            ghost_btn(ins_right, "View Details",
                      cmd=lambda: open_insurance_modal(pid, ins_data, on_saved=refresh_ins),
                      w=90, h=28, color=C_PURPLE, hover_color=C_PURPLE,
                      text_col=C_PURPLE, bg=C_SURFACE).pack(pady=(0,10))
        else:
            tk.Label(ins_inf, text="No Insurance Linked", bg=C_SURFACE, fg=C_TEXT, font=FN_SUBH).pack(anchor="w")
            tk.Label(ins_inf, text="Add insurance to track your coverage",
                     bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(anchor="w")
            pill_btn(ins_right, "+ Add Insurance", w=112, h=32,
                     color=C_PURPLE, hover="#7C3AED", fg=C_SURFACE, bg=C_SURFACE,
                     font=("Segoe UI",7,"bold"),
                     cmd=lambda: open_insurance_modal(pid, None, on_saved=refresh_ins)).pack(pady=14)
    refresh_ins()

    # ── Quick actions  (no insurance card here) ───────────────────────────────
    sec_hdr(pg, "Quick Actions", accent=C_BLUE)
    qa_row = tk.Frame(pg, bg=C_BG); qa_row.pack(fill="x", padx=28, pady=(0,24))

    def qa_card(parent, icon, title, sub, cmd, accent, accent_l):
        cv = tk.Canvas(parent, width=185, height=110, bg=C_BG, highlightthickness=0)
        cv.pack(side="left", padx=5)
        def draw(hover=False):
            cv.delete("all")
            rr(cv, 0, 0, 185, 110, r=12, fill=C_SURFACE)
            rr_outline(cv, 0, 0, 185, 110, r=12, color=accent if hover else C_BORDER)
            rr(cv, 0, 0, 185, 4, r=2, fill=accent)
            # icon circle
            cv.create_oval(76, 16, 110, 50, fill=accent_l, outline="")
            cv.create_text(93, 33, text=icon, fill=accent, font=("Segoe UI",14))
            cv.create_text(93, 68, text=title, fill=C_TEXT, font=("Segoe UI",8,"bold"))
            cv.create_text(93, 84, text=sub, fill=C_TEXT3, font=("Segoe UI",7))
        draw()
        cv.bind("<Button-1>", lambda e: cmd())
        cv.bind("<Enter>", lambda e: draw(True))
        cv.bind("<Leave>", lambda e: draw(False))

    qa_card(qa_row, "⊕", "Find a Doctor",  "Browse specialists",  lambda: nav_cb("Find Doctor"),  C_BLUE,   C_BLUE_L)
    qa_card(qa_row, "◫", "My Bookings",    "View appointments",   lambda: nav_cb("My Bookings"),  C_GREEN,  C_GREEN_L)
    qa_card(qa_row, "📋", "Medical Reports","Your health records", lambda: nav_cb("Reports"),      C_TEAL,   C_TEAL_L)

# ══════════════════════════════════════════════════════════════════════════════
#  WRITE REPORT MODAL  — Doctor
# ══════════════════════════════════════════════════════════════════════════════
def open_write_report_modal(doctor_id, patient_id, patient_name, on_saved=None):
    modal = tk.Toplevel(); modal.title("Write Report")
    modal.geometry("520x500"); modal.resizable(False,False)
    modal.configure(bg=C_BG); modal.grab_set()

    hdr = tk.Frame(modal, bg=C_SURFACE, height=68); hdr.pack(fill="x"); hdr.pack_propagate(False)
    tk.Frame(hdr, bg=C_TEAL, width=4).pack(side="left", fill="y")
    hi = tk.Frame(hdr, bg=C_SURFACE); hi.pack(side="left", padx=20, pady=14, fill="both", expand=True)
    tk.Label(hi, text="Write Medical Report", bg=C_SURFACE, fg=C_TEXT, font=FN_HEAD).pack(anchor="w")
    tk.Label(hi, text=f"Patient: {patient_name}", bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(anchor="w")

    body = tk.Frame(modal, bg=C_BG); body.pack(fill="both", expand=True, padx=28, pady=18)
    for lbl_t, attr in [("DIAGNOSIS","diag"),("MEDICINES (comma separated)","meds"),
                         ("TEST RESULTS (comma separated)","tests")]:
        tk.Label(body, text=lbl_t, bg=C_BG, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w", pady=(0,4))
        e = styled_entry(body); e.pack(fill="x", ipady=9, pady=(0,12))
        if attr=="diag": diag_e=e
        elif attr=="meds": meds_e=e
        else: tests_e=e

    err_lbl = tk.Label(body, text="", bg=C_BG, fg=C_RED, font=FN_SMALL)
    err_lbl.pack(anchor="w", pady=(0,8))

    def save():
        diag = diag_e.get().strip()
        if not diag: err_lbl.config(text="⚠  Diagnosis is required."); return
        meds  = [m.strip() for m in meds_e.get().split(",") if m.strip()]
        tests = [t.strip() for t in tests_e.get().split(",") if t.strip()]
        try:
            conn = get_connection(); cur = conn.cursor()
            now_s = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("INSERT INTO Medical_Reports (Report_Date,Diagnosis,User_Patient_id,User_Doctor_id) VALUES (%s,%s,%s,%s)",
                        (now_s, diag, patient_id, doctor_id))
            rid = cur.lastrowid
            for m in meds: cur.execute("INSERT INTO Medicines VALUES (%s,%s)",(rid,m))
            for t in tests: cur.execute("INSERT INTO Test_Results VALUES (%s,%s)",(rid,t))
            conn.commit(); conn.close()
            messagebox.showinfo("Saved ✓", f"Report saved for {patient_name}.", parent=modal)
            modal.destroy()
            if on_saved: on_saved()
        except Exception as ex:
            err_lbl.config(text=f"⚠  {ex}")

    pill_btn(body, "Save Report  →", save, w=464, h=42,
             color=C_TEAL, hover="#0D9488", fg=C_SURFACE, bg=C_BG,
             font=("Segoe UI",9,"bold")).pack()

# ══════════════════════════════════════════════════════════════════════════════
#  DOCTOR — APPOINTMENTS
# ══════════════════════════════════════════════════════════════════════════════
def panel_doctor_appointments(parent, user):
    did = user["User_id"]
    def load():
        clear(parent)
        pg = scrollable(parent, bg=C_BG)
        hdr_f = tk.Frame(pg, bg=C_BG); hdr_f.pack(fill="x", padx=28, pady=(28,4))
        tk.Label(hdr_f, text="My Appointments", bg=C_BG, fg=C_TEXT, font=FN_DISPLAY).pack(side="left")
        try:
            conn = get_connection(); cur = conn.cursor(dictionary=True)
            cur.execute("""SELECT a.Appointment_id, a.Appointment_Date,
                                  u.User_id AS pat_id, u.First_Name, u.Last_Name,
                                  sc.Day_Name
                           FROM Appointments a
                           JOIN Users u ON a.User_Patient_id=u.User_id
                           JOIN Schedules sc ON a.Schedule_id=sc.Schedule_id
                           WHERE a.User_Doctor_id=%s ORDER BY a.Appointment_Date DESC""", (did,))
            appts = cur.fetchall(); cur.close(); conn.close()
        except Exception as ex:
            tk.Label(pg, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(padx=28); return

        if not appts:
            tk.Label(pg, text="No appointments yet.", bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack(pady=60); return

        now_dt = datetime.now()
        today  = now_dt.date()
        upcoming = [a for a in appts
                    if datetime.strptime(str(a['Appointment_Date'])[:16],"%Y-%m-%d %H:%M") > now_dt]
        past     = [a for a in appts
                    if datetime.strptime(str(a['Appointment_Date'])[:16],"%Y-%m-%d %H:%M") <= now_dt]

        def render_group(items, title, accent, accent_l):
            if not items: return
            sec_hdr(pg, title, accent=accent)
            for ap in items:
                from datetime import timedelta as _td4
                ap_dt     = datetime.strptime(str(ap['Appointment_Date'])[:16], "%Y-%m-%d %H:%M")
                ap_date   = ap_dt.strftime("%Y-%m-%d")
                is_up     = ap_dt > now_dt
                slot_end  = ap_dt + _td4(minutes=30)
                slot_str  = (f"{ap_dt.strftime('%I:%M %p').lstrip('0')} – "
                             f"{slot_end.strftime('%I:%M %p').lstrip('0')}")
                pname = f"{ap['First_Name']} {ap['Last_Name']}"

                card = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
                card.pack(fill="x", padx=28, pady=4)
                tk.Frame(card, bg=accent, width=4).pack(side="left", fill="y")

                av = tk.Canvas(card, width=48, height=48, bg=C_BLUE_L, highlightthickness=0)
                av.pack(side="left", padx=14, pady=12)
                av.create_oval(3,3,45,45, fill=C_BLUE_L, outline=C_BLUE)
                av.create_text(24,24, text=ap['First_Name'][0].upper(), fill=C_BLUE,
                               font=("Segoe UI",14,"bold"))

                inf = tk.Frame(card, bg=C_SURFACE); inf.pack(side="left", fill="both", expand=True, pady=12)
                tk.Label(inf, text=pname, bg=C_SURFACE, fg=C_TEXT, font=FN_SUBH).pack(anchor="w")
                dr = tk.Frame(inf, bg=C_SURFACE); dr.pack(anchor="w", pady=(4,0))
                tk.Label(dr, text=ap_date, bg=C_SURFACE, fg=C_TEXT2,
                         font=FN_SMALL).pack(side="left", padx=(0,10))
                # Exact slot time
                tk.Label(dr, text=f"{ap['Day_Name']}  ·  {slot_str}",
                         bg=C_SURFACE, fg=C_BLUE, font=("Segoe UI",8,"bold")).pack(side="left")

                right = tk.Frame(card, bg=C_SURFACE); right.pack(side="right", padx=16)
                tk.Label(right, text="Upcoming" if is_up else "Past",
                         bg=accent_l, fg=accent,
                         font=FN_LABEL, padx=8, pady=4).pack(pady=(12,6))
                ghost_btn(right, "📋 Report",
                          cmd=lambda pid2=ap['pat_id'], pn=pname:
                              open_write_report_modal(did, pid2, pn, on_saved=load),
                          w=88, h=28, color=C_TEAL, hover_color=C_TEAL,
                          text_col=C_TEAL, bg=C_SURFACE).pack(pady=(0,10))

        render_group(upcoming, "Upcoming", C_GREEN, C_GREEN_L)
        render_group(past,     "Past",     C_TEXT3, C_SURFACE2)
    load()

# ══════════════════════════════════════════════════════════════════════════════
#  DOCTOR — MY PATIENTS
# ══════════════════════════════════════════════════════════════════════════════
def panel_doctor_patients(parent, user):
    did = user["User_id"]
    pg = scrollable(parent, bg=C_BG)
    hdr_f = tk.Frame(pg, bg=C_BG); hdr_f.pack(fill="x", padx=28, pady=(28,4))
    tk.Label(hdr_f, text="My Patients", bg=C_BG, fg=C_TEXT, font=FN_DISPLAY).pack(side="left")
    try:
        conn = get_connection(); cur = conn.cursor(dictionary=True)
        cur.execute("""SELECT DISTINCT u.User_id, u.First_Name, u.Last_Name, u.Gender,
                              p.Date_Of_Birth, COUNT(a.Appointment_id) AS visit_count
                       FROM Appointments a
                       JOIN Users u ON a.User_Patient_id=u.User_id
                       JOIN Patients p ON p.User_Patient_id=u.User_id
                       WHERE a.User_Doctor_id=%s
                       GROUP BY u.User_id,u.First_Name,u.Last_Name,u.Gender,p.Date_Of_Birth
                       ORDER BY u.First_Name""", (did,))
        patients = cur.fetchall(); cur.close(); conn.close()
    except Exception as ex:
        tk.Label(pg, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(padx=28); return

    if not patients:
        tk.Label(pg, text="No patients yet.", bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack(pady=60); return

    for pat in patients:
        pname = f"{pat['First_Name']} {pat['Last_Name']}"
        dob = str(pat['Date_Of_Birth'])
        try: age = datetime.now().year - int(dob[:4])
        except: age = "?"
        gc = C_BLUE if pat['Gender']=="Male" else C_PURPLE
        gl = C_BLUE_L if pat['Gender']=="Male" else C_PURPLE_L
        gi = "♂" if pat['Gender']=="Male" else "♀"

        card = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
        card.pack(fill="x", padx=28, pady=4)
        tk.Frame(card, bg=gc, width=4).pack(side="left", fill="y")

        av = tk.Canvas(card, width=52, height=52, bg=gl, highlightthickness=0)
        av.pack(side="left", padx=14, pady=14)
        av.create_oval(3,3,49,49, fill=gl, outline=gc)
        av.create_text(26,26, text=pat['First_Name'][0].upper(), fill=gc,
                       font=("Segoe UI",15,"bold"))

        inf = tk.Frame(card, bg=C_SURFACE); inf.pack(side="left", fill="both", expand=True, pady=14)
        nr = tk.Frame(inf, bg=C_SURFACE); nr.pack(anchor="w")
        tk.Label(nr, text=pname, bg=C_SURFACE, fg=C_TEXT, font=FN_SUBH).pack(side="left")
        tk.Label(nr, text=f"  {gi}", bg=C_SURFACE, fg=gc, font=("Segoe UI",11)).pack(side="left")
        det = tk.Frame(inf, bg=C_SURFACE); det.pack(anchor="w", pady=(4,0))
        for txt, bg_t, fg_t in [(f"Age {age}", C_SURFACE2, C_TEXT2),
                                  (f"DOB {dob}", C_SURFACE2, C_TEXT2),
                                  (f"{pat['visit_count']} visits", C_BLUE_L, C_BLUE)]:
            tk.Label(det, text=txt, bg=bg_t, fg=fg_t, font=FN_TINY, padx=6, pady=3).pack(side="left", padx=(0,5))

        right = tk.Frame(card, bg=C_SURFACE); right.pack(side="right", padx=16)
        ghost_btn(right, "📋 Report",
                  cmd=lambda pid2=pat['User_id'], pn=pname:
                      open_write_report_modal(did, pid2, pn),
                  w=88, h=28, color=C_TEAL, hover_color=C_TEAL,
                  text_col=C_TEAL, bg=C_SURFACE).pack(pady=14)

# ══════════════════════════════════════════════════════════════════════════════
#  DOCTOR — MY REPORTS
# ══════════════════════════════════════════════════════════════════════════════
def panel_doctor_reports(parent, user):
    did = user["User_id"]
    pg = scrollable(parent, bg=C_BG)
    hdr_f = tk.Frame(pg, bg=C_BG); hdr_f.pack(fill="x", padx=28, pady=(28,4))
    tk.Label(hdr_f, text="Reports Written", bg=C_BG, fg=C_TEXT, font=FN_DISPLAY).pack(side="left")
    try:
        conn = get_connection(); cur = conn.cursor(dictionary=True)
        cur.execute("""SELECT mr.Report_id, mr.Report_Date, mr.Diagnosis, u.First_Name, u.Last_Name
                       FROM Medical_Reports mr JOIN Users u ON mr.User_Patient_id=u.User_id
                       WHERE mr.User_Doctor_id=%s ORDER BY mr.Report_Date DESC""", (did,))
        reports = cur.fetchall()
        meds_map = {}; tests_map = {}
        if reports:
            ids = tuple(r['Report_id'] for r in reports)
            ph = ','.join(['%s']*len(ids))
            cur.execute(f"SELECT Report_id, Medicine_Name FROM Medicines WHERE Report_id IN ({ph})", ids)
            for row in cur.fetchall(): meds_map.setdefault(row['Report_id'],[]).append(row['Medicine_Name'])
            cur.execute(f"SELECT Report_id, Test_Result FROM Test_Results WHERE Report_id IN ({ph})", ids)
            for row in cur.fetchall(): tests_map.setdefault(row['Report_id'],[]).append(row['Test_Result'])
        cur.close(); conn.close()
    except Exception as ex:
        tk.Label(pg, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(padx=28); return

    if not reports:
        tk.Label(pg, text="No reports written yet.", bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack(pady=60); return

    for rep in reports:
        rdate = str(rep['Report_Date'])[:10]
        pname = f"{rep['First_Name']} {rep['Last_Name']}"
        card = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
        card.pack(fill="x", padx=28, pady=5)
        tk.Frame(card, bg=C_GREEN, width=4).pack(side="left", fill="y")
        av = tk.Canvas(card, width=48, height=48, bg=C_GREEN_L, highlightthickness=0)
        av.pack(side="left", padx=14, pady=14)
        av.create_text(24,24, text="📋", font=("Segoe UI",18))
        inf = tk.Frame(card, bg=C_SURFACE); inf.pack(side="left", fill="both", expand=True, pady=14)
        tk.Label(inf, text=pname, bg=C_SURFACE, fg=C_TEXT, font=FN_SUBH).pack(anchor="w")
        tk.Label(inf, text=rdate, bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(anchor="w", pady=(2,4))
        dr = tk.Frame(inf, bg=C_SURFACE); dr.pack(anchor="w")
        tk.Label(dr, text="Diagnosis: ", bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(side="left")
        tk.Label(dr, text=rep['Diagnosis'], bg=C_SURFACE, fg=C_AMBER, font=("Segoe UI",8,"bold")).pack(side="left")
        meds = meds_map.get(rep['Report_id'],[])
        tests = tests_map.get(rep['Report_id'],[])
        if meds:
            mr = tk.Frame(inf, bg=C_SURFACE); mr.pack(anchor="w", pady=(4,0))
            tk.Label(mr, text="Medicines: ", bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(side="left")
            for m in meds: tk.Label(mr, text=m, bg=C_GREEN_L, fg=C_GREEN, font=FN_TINY, padx=6, pady=2).pack(side="left", padx=2)
        if tests:
            tr = tk.Frame(inf, bg=C_SURFACE); tr.pack(anchor="w", pady=(4,0))
            tk.Label(tr, text="Tests: ", bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(side="left")
            for t in tests: tk.Label(tr, text=t, bg=C_BLUE_L, fg=C_BLUE, font=FN_TINY, padx=6, pady=2).pack(side="left", padx=2)


# ══════════════════════════════════════════════════════════════════════════════
#  DOCTOR — OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
def panel_doctor_overview(parent, user, nav_cb):
    did = user["User_id"]
    pg = scrollable(parent, bg=C_BG)

    # ── Hero banner ───────────────────────────────────────────────────────────
    hero = tk.Canvas(pg, height=148, bg=C_BG, highlightthickness=0)
    hero.pack(fill="x")
    def draw_hero(e=None):
        w = hero.winfo_width() or 900
        hero.delete("all")
        hero.create_rectangle(0, 0, w, 148, fill=C_SURFACE, outline="")
        hero.create_rectangle(0, 0, w, 4, fill=C_TEAL, outline="")
        hero.create_oval(w-160, -60, w+60, 160, fill=C_TEAL_L, outline="")
        hero.create_oval(w-120, -20, w+20, 120, fill=C_PANEL, outline="")
        hero.create_text(32, 55, text=f"Welcome, Dr. {user['First_Name']} 👨‍⚕️",
                         fill=C_TEXT, font=("Segoe UI",18,"bold"), anchor="w")
        hero.create_text(32, 85, text="Your medical dashboard  ·  E7gezly",
                         fill=C_TEXT2, font=("Segoe UI",9), anchor="w")
        hero.create_rectangle(0, 146, w, 148, fill=C_BORDER, outline="")
    hero.bind("<Configure>", draw_hero)
    hero.after(50, draw_hero)

    # ── Stats ─────────────────────────────────────────────────────────────────
    try:
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Appointments WHERE User_Doctor_id=%s", (did,))
        total_a = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM Appointments WHERE User_Doctor_id=%s AND Appointment_Date>=%s",
                    (did, datetime.now().strftime("%Y-%m-%d")))
        upcoming = cur.fetchone()[0]
        cur.execute("SELECT COUNT(DISTINCT User_Patient_id) FROM Appointments WHERE User_Doctor_id=%s", (did,))
        total_p = cur.fetchone()[0]
        cur.execute("""SELECT ROUND(AVG(r.Rating),1) FROM Reviews r
                       JOIN Appointments a ON r.Appointment_id=a.Appointment_id
                       WHERE a.User_Doctor_id=%s""", (did,))
        avg_r = cur.fetchone()[0] or 0
        cur.close(); conn.close()
    except:
        total_a = upcoming = total_p = 0; avg_r = 0

    stats_row = tk.Frame(pg, bg=C_BG); stats_row.pack(fill="x", padx=28, pady=16)
    stat_card(stats_row, total_a,       "Appointments", C_TEAL,   C_TEAL_L)
    stat_card(stats_row, upcoming,      "Upcoming",     C_GREEN,  C_GREEN_L)
    stat_card(stats_row, total_p,       "Patients",     C_BLUE,   C_BLUE_L)
    stat_card(stats_row, f"★ {avg_r}", "Rating",       C_AMBER,  C_AMBER_L)

    # ── Today's schedule ──────────────────────────────────────────────────────
    sec_hdr(pg, "Today's Schedule", accent=C_TEAL)
    try:
        conn = get_connection(); cur = conn.cursor(dictionary=True)
        today_str = datetime.now().strftime("%Y-%m-%d")
        cur.execute("""SELECT u.First_Name, u.Last_Name,
                              TIME_FORMAT(sc.Start_Time,'%I:%i %p') AS t_start,
                              TIME_FORMAT(sc.End_Time,'%I:%i %p')   AS t_end
                       FROM Appointments a
                       JOIN Users u ON a.User_Patient_id=u.User_id
                       JOIN Schedules sc ON a.Schedule_id=sc.Schedule_id
                       WHERE a.User_Doctor_id=%s AND DATE(a.Appointment_Date)=%s
                       ORDER BY sc.Start_Time""", (did, today_str))
        today_appts = cur.fetchall(); cur.close(); conn.close()
    except:
        today_appts = []

    if not today_appts:
        empty = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
        empty.pack(fill="x", padx=28, pady=4)
        tk.Label(empty, text="No appointments scheduled for today.",
                 bg=C_SURFACE, fg=C_TEXT3, font=FN_BODY, pady=18).pack()
    else:
        for ap in today_appts:
            pname = f"{ap['First_Name']} {ap['Last_Name']}"
            card = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
            card.pack(fill="x", padx=28, pady=3)
            tk.Frame(card, bg=C_TEAL, width=4).pack(side="left", fill="y")
            av = tk.Canvas(card, width=42, height=42, bg=C_TEAL_L, highlightthickness=0)
            av.pack(side="left", padx=12, pady=10)
            av.create_oval(2,2,40,40, fill=C_TEAL_L, outline=C_TEAL)
            av.create_text(21,21, text=ap['First_Name'][0].upper(), fill=C_TEAL,
                           font=("Segoe UI",13,"bold"))
            inf = tk.Frame(card, bg=C_SURFACE); inf.pack(side="left", fill="both", expand=True, pady=10)
            tk.Label(inf, text=pname, bg=C_SURFACE, fg=C_TEXT, font=FN_SUBH).pack(anchor="w")
            tk.Label(inf, text=f"{ap['t_start']} – {ap['t_end']}",
                     bg=C_SURFACE, fg=C_TEXT2, font=FN_SMALL).pack(anchor="w")

    # ── Quick actions ─────────────────────────────────────────────────────────
    sec_hdr(pg, "Quick Actions", accent=C_TEAL)
    qa_row = tk.Frame(pg, bg=C_BG); qa_row.pack(fill="x", padx=28, pady=(0,24))

    def qa_card(parent, icon, title, sub, cmd, accent, accent_l):
        cv = tk.Canvas(parent, width=185, height=110, bg=C_BG, highlightthickness=0)
        cv.pack(side="left", padx=5)
        def draw(hover=False):
            cv.delete("all")
            rr(cv, 0, 0, 185, 110, r=12, fill=C_SURFACE)
            rr_outline(cv, 0, 0, 185, 110, r=12, color=accent if hover else C_BORDER)
            rr(cv, 0, 0, 185, 4, r=2, fill=accent)
            cv.create_oval(76, 16, 110, 50, fill=accent_l, outline="")
            cv.create_text(93, 33, text=icon, fill=accent, font=("Segoe UI",14))
            cv.create_text(93, 68, text=title, fill=C_TEXT, font=("Segoe UI",8,"bold"))
            cv.create_text(93, 84, text=sub, fill=C_TEXT3, font=("Segoe UI",7))
        draw()
        cv.bind("<Button-1>", lambda e: cmd())
        cv.bind("<Enter>", lambda e: draw(True))
        cv.bind("<Leave>", lambda e: draw(False))

    qa_card(qa_row, "📅", "Appointments", "All your appointments",  lambda: nav_cb("Appointments"), C_TEAL,  C_TEAL_L)
    qa_card(qa_row, "👥", "My Patients",  "Browse patient list",    lambda: nav_cb("Patients"),     C_BLUE,  C_BLUE_L)
    qa_card(qa_row, "📋", "My Reports",   "Reports you've written", lambda: nav_cb("My Reports"),   C_GREEN, C_GREEN_L)

# ══════════════════════════════════════════════════════════════════════════════
#  REGISTRATION
# ══════════════════════════════════════════════════════════════════════════════
def show_register(root, container):
    clear(container); root.geometry("540x760")
    page = tk.Frame(container, bg=C_BG); page.pack(fill="both", expand=True)

    # Top bar
    top = tk.Frame(page, bg=C_SURFACE, height=58); top.pack(fill="x"); top.pack_propagate(False)
    tk.Frame(top, bg=C_BLUE, height=3).pack(fill="x")
    tk.Label(top, text="✚  E7gezly", bg=C_SURFACE, fg=C_TEXT,
             font=("Segoe UI",13,"bold")).pack(side="left", padx=24, pady=12)
    back = tk.Label(top, text="← Sign In", bg=C_SURFACE, fg=C_BLUE, font=FN_BODY, cursor="hand2")
    back.pack(side="right", padx=24)
    back.bind("<Button-1>", lambda e: show_login(root, container))

    pg = scrollable(page, bg=C_BG)
    tk.Label(pg, text="Create Account", bg=C_BG, fg=C_TEXT,
             font=FN_DISPLAY).pack(anchor="w", padx=36, pady=(28,4))
    tk.Label(pg, text="Fill in your details to get started as a patient.",
             bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack(anchor="w", padx=36)

    card = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
    card.pack(fill="x", padx=36, pady=16)
    ci = tk.Frame(card, bg=C_SURFACE); ci.pack(padx=24, pady=20, fill="x")

    def field_lbl(text):
        tk.Label(ci, text=text, bg=C_SURFACE, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w", pady=(12,3))

    def make_entry(secret=False):
        e = styled_entry(ci, secret=secret); e.pack(fill="x", ipady=9); return e

    field_lbl("FIRST NAME");   fn_e = make_entry()
    field_lbl("LAST NAME");    ln_e = make_entry()
    field_lbl("EMAIL");        em_e = make_entry()
    field_lbl("PASSWORD");     pw_e = make_entry(secret=True)
    field_lbl("PHONE NUMBER"); ph_e = make_entry()

    field_lbl("GENDER")
    gv = tk.StringVar(value="Male")
    gr = tk.Frame(ci, bg=C_SURFACE); gr.pack(anchor="w", pady=(0,4))
    for g in ["Male", "Female"]:
        tk.Radiobutton(gr, text=g, variable=gv, value=g,
                       bg=C_SURFACE, fg=C_TEXT, font=FN_BODY,
                       selectcolor=C_BLUE_L, activebackground=C_SURFACE,
                       activeforeground=C_BLUE).pack(side="left", padx=(0,18))

    field_lbl("DATE OF BIRTH")
    MONTHS_L = ["January","February","March","April","May","June",
                "July","August","September","October","November","December"]
    dv = tk.StringVar(value="Day")
    mv = tk.StringVar(value="Month")
    yv = tk.StringVar(value="Year")
    dob_row = tk.Frame(ci, bg=C_SURFACE); dob_row.pack(fill="x", pady=(0,4))
    for var, vals, w_px in [
        (dv, ["Day"]   + [str(i) for i in range(1, 32)],  80),
        (mv, ["Month"] + MONTHS_L,                         160),
        (yv, ["Year"]  + [str(i) for i in range(1950, datetime.now().year - 4)], 100),
    ]:
        fr = tk.Frame(dob_row, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
        fr.pack(side="left", padx=(0,6))
        om = tk.OptionMenu(fr, var, *vals)
        om.config(bg=C_SURFACE, fg=C_TEXT, font=FN_SMALL, relief="flat", bd=0,
                  highlightthickness=0, activebackground=C_BORDER, width=w_px//10)
        om["menu"].config(bg=C_SURFACE, fg=C_TEXT, font=FN_SMALL,
                          activebackground=C_BLUE_L, activeforeground=C_BLUE)
        om.pack()

    err_lbl = tk.Label(pg, text="", bg=C_BG, fg=C_RED, font=FN_SMALL)
    err_lbl.pack(anchor="w", padx=36)

    def register():
        fn = fn_e.get().strip(); ln = ln_e.get().strip()
        em = em_e.get().strip(); pw = pw_e.get().strip(); ph = ph_e.get().strip()
        gen = gv.get(); d = dv.get(); m_n = mv.get(); y = yv.get()
        if not all([fn, ln, em, pw, ph]):
            err_lbl.config(text="⚠  Please fill in all fields."); return
        if "Day" in d or "Month" in m_n or "Year" in y:
            err_lbl.config(text="⚠  Please select your date of birth."); return
        dob = f"{y}-{MONTHS_L.index(m_n)+1:02d}-{int(d):02d}"
        err_lbl.config(text="")
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO Users (First_Name,Last_Name,Email,Password,Gender) VALUES (%s,%s,%s,%s,%s)",
                        (fn, ln, em, pw, gen))
            uid = cur.lastrowid
            cur.execute("INSERT INTO User_Phone VALUES (%s,%s)", (uid, ph))
            cur.execute("INSERT INTO Patients VALUES (%s,%s)", (uid, dob))
            conn.commit(); conn.close()
            messagebox.showinfo("Welcome! ✓", f"Account created, {fn}!\nYou can now sign in.")
            show_login(root, container)
        except mysql.connector.IntegrityError:
            err_lbl.config(text="⚠  This email is already registered.")
        except Exception as ex:
            err_lbl.config(text=f"⚠  {ex}")

    btn_wrap = tk.Frame(pg, bg=C_BG); btn_wrap.pack(fill="x", padx=36, pady=16)
    pill_btn(btn_wrap, "Create Account  →", register, w=468, h=44,
             color=C_BLUE, hover=C_BLUE_D, fg=C_SURFACE, bg=C_BG,
             font=("Segoe UI",9,"bold")).pack()

    si = tk.Label(pg, text="Already have an account?  Sign In →",
                  bg=C_BG, fg=C_BLUE, font=FN_BODY, cursor="hand2")
    si.pack(pady=(4, 30))
    si.bind("<Button-1>", lambda e: show_login(root, container))

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD  — sidebar + content router
# ══════════════════════════════════════════════════════════════════════════════
def show_home(root, container, user, role):
    clear(container); root.geometry("1080x700")
    wrapper = tk.Frame(container, bg=C_BG); wrapper.pack(fill="both", expand=True)

    is_doctor   = (role == "Doctor")
    accent      = C_TEAL if is_doctor else C_BLUE
    accent_l    = C_TEAL_L if is_doctor else C_BLUE_L

    # ── Sidebar ───────────────────────────────────────────────────────────────
    sidebar = tk.Frame(wrapper, bg=C_PANEL, width=220)
    sidebar.pack(side="left", fill="y"); sidebar.pack_propagate(False)

    # Top accent stripe
    tk.Frame(sidebar, bg=accent, height=3).pack(fill="x")

    # Logo
    logo_f = tk.Frame(sidebar, bg=C_PANEL, height=64)
    logo_f.pack(fill="x"); logo_f.pack_propagate(False)
    tk.Label(logo_f, text="✚  E7gezly", bg=C_PANEL, fg=C_TEXT,
             font=("Segoe UI",14,"bold")).pack(side="left", padx=20, pady=20)

    tk.Frame(sidebar, bg=C_BORDER, height=1).pack(fill="x")

    # User chip
    chip = tk.Frame(sidebar, bg=C_SURFACE); chip.pack(fill="x")
    av_cv = tk.Canvas(chip, width=42, height=42, bg=C_SURFACE, highlightthickness=0)
    av_cv.pack(side="left", padx=(16,10), pady=14)
    av_cv.create_oval(1,1,41,41, fill=accent_l, outline=accent)
    av_cv.create_text(21,21, text=user['First_Name'][0].upper(),
                      fill=accent, font=("Segoe UI",13,"bold"))
    uc = tk.Frame(chip, bg=C_SURFACE); uc.pack(side="left", pady=10)
    name_disp = (f"Dr. {user['First_Name']} {user['Last_Name']}"
                 if is_doctor else f"{user['First_Name']} {user['Last_Name']}")
    tk.Label(uc, text=name_disp, bg=C_SURFACE, fg=C_TEXT,
             font=("Segoe UI",8,"bold")).pack(anchor="w")
    tk.Label(uc, text=role.upper(), bg=C_SURFACE, fg=accent,
             font=FN_LABEL).pack(anchor="w")

    tk.Frame(sidebar, bg=C_BORDER, height=1).pack(fill="x")

    # Content area
    content = tk.Frame(wrapper, bg=C_BG)
    content.pack(side="right", fill="both", expand=True)
    active = {"lbl": None, "btns": {}}

    def nav_to(label):
        clear(content)
        for lbl2, btn2 in active["btns"].items():
            is_act = (lbl2 == label)
            btn2.config(bg=accent_l if is_act else C_PANEL,
                        fg=accent   if is_act else C_TEXT2)
        active["lbl"] = label

        if is_doctor:
            if   label == "Overview":     panel_doctor_overview(content, user, nav_to)
            elif label == "Appointments": panel_doctor_appointments(content, user)
            elif label == "Patients":     panel_doctor_patients(content, user)
            elif label == "My Reports":   panel_doctor_reports(content, user)
        else:
            if   label == "Overview":    panel_overview(content, user, nav_to)
            elif label == "Find Doctor": panel_find_doctor(content, user)
            elif label == "My Bookings": panel_my_bookings(content, user)
            elif label == "Reports":     panel_medical_reports(content, user)

    MENU = ([("⊹", "Overview"), ("📅", "Appointments"), ("👥", "Patients"), ("📋", "My Reports")]
            if is_doctor else
            [("⊹", "Overview"), ("⊕", "Find Doctor"), ("◫", "My Bookings"), ("📋", "Reports")])

    for icon, label in MENU:
        btn = tk.Button(
            sidebar,
            text=f"   {icon}   {label}",
            bg=C_PANEL, fg=C_TEXT2,
            font=("Segoe UI", 9),
            relief="flat", anchor="w",
            activebackground=accent_l,
            activeforeground=accent,
            bd=0, padx=0,
            command=lambda l=label: nav_to(l)
        )
        btn.pack(fill="x", ipady=12)
        btn.bind("<Enter>", lambda e, b=btn, l=label:
            b.config(bg=C_SURFACE, fg=accent) if active["lbl"] != l else None)
        btn.bind("<Leave>", lambda e, b=btn, l=label:
            b.config(bg=accent_l if active["lbl"]==l else C_PANEL,
                     fg=accent   if active["lbl"]==l else C_TEXT2))
        active["btns"][label] = btn

    # Sign out at bottom
    tk.Frame(sidebar, bg=C_BORDER, height=1).pack(side="bottom", fill="x")
    lo = tk.Button(
        sidebar, text="   ⏻   Sign Out",
        bg=C_PANEL, fg=C_RED,
        font=("Segoe UI", 9),
        relief="flat", anchor="w", bd=0,
        activebackground=C_RED_L, activeforeground=C_RED,
        command=lambda: (
            messagebox.askyesno("Sign Out", "Sign out of E7gezly?") and
            show_login(root, container)
        )
    )
    lo.pack(side="bottom", fill="x", ipady=12)
    lo.bind("<Enter>", lambda e: lo.config(bg=C_RED_L))
    lo.bind("<Leave>", lambda e: lo.config(bg=C_PANEL))

    nav_to("Overview")

# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN — COLOUR OVERRIDES  (orange accent)
# ══════════════════════════════════════════════════════════════════════════════
C_ADMIN     = "#F97316"   # orange
C_ADMIN_L   = "#FFEDD5"   # orange tint
C_ADMIN_D   = "#EA6C00"   # orange hover

# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN — ADD DOCTOR MODAL
# ══════════════════════════════════════════════════════════════════════════════
def admin_add_doctor_modal(on_saved=None):
    modal = tk.Toplevel(); modal.title("Add Doctor")
    modal.geometry("520x640"); modal.resizable(False, False)
    modal.configure(bg=C_BG); modal.grab_set()

    hdr = tk.Frame(modal, bg=C_SURFACE, height=68); hdr.pack(fill="x"); hdr.pack_propagate(False)
    tk.Frame(hdr, bg=C_ADMIN, width=4).pack(side="left", fill="y")
    hi = tk.Frame(hdr, bg=C_SURFACE); hi.pack(side="left", padx=20, pady=14, fill="both", expand=True)
    tk.Label(hi, text="Add New Doctor", bg=C_SURFACE, fg=C_TEXT, font=FN_HEAD).pack(anchor="w")
    tk.Label(hi, text="Create a doctor account and assign specialization",
             bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(anchor="w")

    body = tk.Frame(modal, bg=C_BG); body.pack(fill="both", expand=True, padx=28, pady=16)

    def lbl(t): tk.Label(body, text=t, bg=C_BG, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w", pady=(8,3))
    def ent(secret=False):
        e = styled_entry(body, secret=secret); e.pack(fill="x", ipady=8); return e

    lbl("FIRST NAME");   fn_e = ent()
    lbl("LAST NAME");    ln_e = ent()
    lbl("EMAIL");        em_e = ent()
    lbl("PASSWORD");     pw_e = ent(secret=True)

    lbl("GENDER")
    gv = tk.StringVar(value="Male")
    gr = tk.Frame(body, bg=C_BG); gr.pack(anchor="w", pady=(0,4))
    for g in ["Male","Female"]:
        tk.Radiobutton(gr, text=g, variable=gv, value=g, bg=C_BG, fg=C_TEXT,
                       font=FN_BODY, selectcolor=C_BLUE_L,
                       activebackground=C_BG).pack(side="left", padx=(0,16))

    lbl("SPECIALIZATION")
    try:
        conn = get_connection(); cur = conn.cursor(dictionary=True)
        cur.execute("SELECT Specialization_id, Specialization_Name FROM Specialization ORDER BY Specialization_Name")
        specs = cur.fetchall(); cur.close(); conn.close()
    except: specs = []
    spec_map = {s['Specialization_Name']: s['Specialization_id'] for s in specs}
    spec_var = tk.StringVar(value=list(spec_map.keys())[0] if spec_map else "")
    sf = tk.Frame(body, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
    sf.pack(fill="x", pady=(0,4))
    om = tk.OptionMenu(sf, spec_var, *list(spec_map.keys()))
    om.config(bg=C_SURFACE, fg=C_TEXT, font=FN_BODY, relief="flat", bd=0,
              highlightthickness=0, activebackground=C_BORDER, width=30)
    om["menu"].config(bg=C_SURFACE, fg=C_TEXT, font=FN_SMALL,
                      activebackground=C_BLUE_L, activeforeground=C_BLUE)
    om.pack(fill="x", padx=4, pady=6)

    row2 = tk.Frame(body, bg=C_BG); row2.pack(fill="x", pady=(4,0))
    fee_f = tk.Frame(row2, bg=C_BG); fee_f.pack(side="left", expand=True, fill="x", padx=(0,8))
    tk.Label(fee_f, text="CONSULTATION FEE (EGP)", bg=C_BG, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w", pady=(0,3))
    fee_e = styled_entry(fee_f); fee_e.pack(fill="x", ipady=8)

    exp_f = tk.Frame(row2, bg=C_BG); exp_f.pack(side="left", expand=True, fill="x")
    tk.Label(exp_f, text="EXPERIENCE (YEARS)", bg=C_BG, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w", pady=(0,3))
    exp_e = styled_entry(exp_f); exp_e.pack(fill="x", ipady=8)

    err_lbl = tk.Label(body, text="", bg=C_BG, fg=C_RED, font=FN_SMALL)
    err_lbl.pack(anchor="w", pady=(8,0))

    def save():
        fn=fn_e.get().strip(); ln=ln_e.get().strip()
        em=em_e.get().strip(); pw=pw_e.get().strip()
        gen=gv.get(); sp=spec_var.get()
        fee=fee_e.get().strip(); exp=exp_e.get().strip()
        if not all([fn,ln,em,pw,sp,fee,exp]):
            err_lbl.config(text="⚠  Please fill in all fields."); return
        try:
            fee_i=int(fee); exp_i=int(exp)
        except:
            err_lbl.config(text="⚠  Fee and Experience must be numbers."); return
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO Users (First_Name,Last_Name,Email,Password,Gender) VALUES (%s,%s,%s,%s,%s)",
                        (fn,ln,em,pw,gen))
            uid = cur.lastrowid
            cur.execute("INSERT INTO Doctors (User_Doctor_id,Consultant_Fees,Experience_Years,Specialization_id) VALUES (%s,%s,%s,%s)",
                        (uid, fee_i, exp_i, spec_map[sp]))
            conn.commit(); conn.close()
            messagebox.showinfo("Added ✓", f"Dr. {fn} {ln} added successfully!", parent=modal)
            modal.destroy()
            if on_saved: on_saved()
        except mysql.connector.IntegrityError:
            err_lbl.config(text="⚠  Email already exists.")
        except Exception as ex:
            err_lbl.config(text=f"⚠  {ex}")

    pill_btn(body, "Add Doctor  →", save, w=464, h=42,
             color=C_ADMIN, hover=C_ADMIN_D, fg=C_SURFACE, bg=C_BG,
             font=("Segoe UI",9,"bold")).pack(pady=(8,0))

# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN — MANAGE DOCTORS PANEL
# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN — SCHEDULE MODAL  (manage one doctor's availability)
# ══════════════════════════════════════════════════════════════════════════════
def admin_schedule_modal(doctor_id, doctor_name, on_saved=None):
    modal = tk.Toplevel(); modal.title("Schedule")
    modal.geometry("560x620"); modal.resizable(False, False)
    modal.configure(bg=C_BG); modal.grab_set()

    # Header
    hdr = tk.Frame(modal, bg=C_SURFACE, height=68); hdr.pack(fill="x"); hdr.pack_propagate(False)
    tk.Frame(hdr, bg=C_ADMIN, width=4).pack(side="left", fill="y")
    hi = tk.Frame(hdr, bg=C_SURFACE); hi.pack(side="left", padx=20, pady=14, fill="both", expand=True)
    tk.Label(hi, text=f"Availability — {doctor_name}", bg=C_SURFACE, fg=C_TEXT, font=FN_HEAD).pack(anchor="w")
    tk.Label(hi, text="Set working days and hours (30-min slots will be generated automatically)",
             bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(anchor="w")

    body = tk.Frame(modal, bg=C_BG); body.pack(fill="both", expand=True)

    # ── Existing schedules (scrollable) ──────────────────────────────────────
    list_frame = tk.Frame(body, bg=C_BG); list_frame.pack(fill="both", expand=True, padx=24, pady=(14,0))
    sec_hdr(list_frame, "Current Schedule", bg=C_BG, accent=C_ADMIN)

    sched_scroll = tk.Frame(list_frame, bg=C_BG); sched_scroll.pack(fill="x")

    def reload_schedules():
        for w in sched_scroll.winfo_children(): w.destroy()
        try:
            conn = get_connection(); cur = conn.cursor(dictionary=True)
            cur.execute("""SELECT Schedule_id, Day_Name,
                                  TIME_FORMAT(Start_Time,'%H:%i') AS s_raw,
                                  TIME_FORMAT(End_Time,'%H:%i')   AS e_raw,
                                  TIME_FORMAT(Start_Time,'%I:%i %p') AS t_start,
                                  TIME_FORMAT(End_Time,'%I:%i %p')   AS t_end
                           FROM Schedules WHERE User_Doctor_id=%s
                           ORDER BY FIELD(Day_Name,'Sunday','Monday','Tuesday',
                                          'Wednesday','Thursday','Friday','Saturday')""",
                        (doctor_id,))
            scheds = cur.fetchall(); cur.close(); conn.close()
        except Exception as ex:
            tk.Label(sched_scroll, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(); return

        if not scheds:
            tk.Label(sched_scroll, text="No schedule set yet.",
                     bg=C_BG, fg=C_TEXT3, font=FN_BODY).pack(anchor="w", pady=4)
        else:
            for sc in scheds:
                from datetime import timedelta as _td2
                # calculate slot count
                try:
                    sh, sm = map(int, sc['s_raw'].split(':'))
                    eh, em = map(int, sc['e_raw'].split(':'))
                    total_mins = (eh*60+em) - (sh*60+sm)
                    if total_mins <= 0: total_mins += 24*60
                    n_slots = total_mins // 30
                except: n_slots = 0

                row = tk.Frame(sched_scroll, bg=C_SURFACE,
                               highlightbackground=C_BORDER, highlightthickness=1)
                row.pack(fill="x", pady=3)
                tk.Frame(row, bg=C_ADMIN, width=3).pack(side="left", fill="y")

                inf = tk.Frame(row, bg=C_SURFACE); inf.pack(side="left", fill="both", expand=True, padx=12, pady=8)
                day_row = tk.Frame(inf, bg=C_SURFACE); day_row.pack(anchor="w")
                tk.Label(day_row, text=sc['Day_Name'], bg=C_SURFACE, fg=C_TEXT,
                         font=FN_SUBH).pack(side="left")
                tk.Label(day_row, text=f"  {sc['t_start']} – {sc['t_end']}",
                         bg=C_SURFACE, fg=C_TEXT2, font=FN_BODY).pack(side="left")
                tk.Label(inf, text=f"{n_slots} slots of 30 min",
                         bg=C_SURFACE, fg=C_TEAL, font=FN_TINY).pack(anchor="w")

                right = tk.Frame(row, bg=C_SURFACE); right.pack(side="right", padx=10)
                def do_del(sid=sc['Schedule_id'], day=sc['Day_Name']):
                    if not messagebox.askyesno("Delete Schedule",
                        f"Delete {day} schedule?\nExisting appointments on this day will remain."): return
                    try:
                        c2 = get_connection(); cu2 = c2.cursor()
                        cu2.execute("DELETE FROM Take_Place_In WHERE Schedule_id=%s", (sid,))
                        cu2.execute("DELETE FROM Schedules WHERE Schedule_id=%s", (sid,))
                        c2.commit(); c2.close()
                        reload_schedules()
                        if on_saved: on_saved()
                    except Exception as ex2: messagebox.showerror("Error", str(ex2))
                ghost_btn(right, "✕ Delete", do_del, w=76, h=26,
                          color=C_RED, hover_color=C_RED, text_col=C_RED, bg=C_SURFACE).pack(pady=8)

    reload_schedules()

    # ── Add new schedule ──────────────────────────────────────────────────────
    sec_hdr(body, "Add / Update Day", bg=C_BG, accent=C_TEAL)
    add_f = tk.Frame(body, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
    add_f.pack(fill="x", padx=24, pady=(0,12))
    af = tk.Frame(add_f, bg=C_SURFACE); af.pack(padx=16, pady=14, fill="x")

    DAYS = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    day_var = tk.StringVar(value="Sunday")

    # Day selector — pill toggle buttons
    tk.Label(af, text="DAY", bg=C_SURFACE, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w", pady=(0,6))
    day_row = tk.Frame(af, bg=C_SURFACE); day_row.pack(anchor="w", pady=(0,10))
    day_btns = {}

    def _draw_day_btn(cv, day):
        cv.delete("all")
        sel = day_var.get() == day
        rr(cv, 0, 0, 72, 28, r=14, fill=C_TEAL if sel else C_SURFACE)
        if not sel: rr_outline(cv, 0, 0, 72, 28, r=14, color=C_BORDER2)
        cv.create_text(36, 14, text=day[:3],
                       fill=C_SURFACE if sel else C_TEXT2,
                       font=("Segoe UI",7,"bold"))

    def _refresh_day_btns():
        for d, cv in day_btns.items(): _draw_day_btn(cv, d)

    for day in DAYS:
        cv = tk.Canvas(day_row, width=72, height=28, bg=C_SURFACE, highlightthickness=0)
        cv.pack(side="left", padx=2)
        _draw_day_btn(cv, day)
        def _click_day(e, d=day):
            day_var.set(d); _refresh_day_btns()
        cv.bind("<Button-1>", _click_day)
        day_btns[day] = cv

    # Time pickers
    tk.Label(af, text="WORKING HOURS", bg=C_SURFACE, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w", pady=(0,6))
    time_row = tk.Frame(af, bg=C_SURFACE); time_row.pack(anchor="w", pady=(0,10))

    HOURS   = [f"{h:02d}" for h in range(0, 24)]
    MINUTES = ["00", "30"]

    def _time_picker(parent, label):
        f = tk.Frame(parent, bg=C_SURFACE); f.pack(side="left", padx=(0,16))
        tk.Label(f, text=label, bg=C_SURFACE, fg=C_TEXT3, font=FN_TINY).pack(anchor="w")
        inner = tk.Frame(f, bg=C_SURFACE); inner.pack()
        hv = tk.StringVar(value="09"); mv = tk.StringVar(value="00")
        hf = tk.Frame(inner, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
        hf.pack(side="left")
        hom = tk.OptionMenu(hf, hv, *HOURS)
        hom.config(bg=C_SURFACE, fg=C_TEXT, font=FN_BODY, relief="flat", bd=0,
                   highlightthickness=0, activebackground=C_BORDER, width=3)
        hom["menu"].config(bg=C_SURFACE, fg=C_TEXT, font=FN_SMALL,
                           activebackground=C_BLUE_L, activeforeground=C_BLUE)
        hom.pack(padx=4, pady=4)
        tk.Label(inner, text=":", bg=C_SURFACE, fg=C_TEXT2, font=FN_SUBH).pack(side="left", padx=2)
        mf = tk.Frame(inner, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
        mf.pack(side="left")
        mom = tk.OptionMenu(mf, mv, *MINUTES)
        mom.config(bg=C_SURFACE, fg=C_TEXT, font=FN_BODY, relief="flat", bd=0,
                   highlightthickness=0, activebackground=C_BORDER, width=2)
        mom["menu"].config(bg=C_SURFACE, fg=C_TEXT, font=FN_SMALL,
                           activebackground=C_BLUE_L, activeforeground=C_BLUE)
        mom.pack(padx=4, pady=4)
        return hv, mv

    start_h, start_m = _time_picker(time_row, "FROM")
    end_h,   end_m   = _time_picker(time_row, "TO")

    # Slot preview label
    preview_lbl = tk.Label(af, text="", bg=C_SURFACE, fg=C_TEAL, font=("Segoe UI",8,"bold"))
    preview_lbl.pack(anchor="w", pady=(0,8))

    def _update_preview(*_):
        try:
            sh = int(start_h.get()); sm = int(start_m.get())
            eh = int(end_h.get());   em = int(end_m.get())
            total = (eh*60+em) - (sh*60+sm)
            if total <= 0: total += 24*60
            n = total // 30
            s_fmt = f"{sh:02d}:{sm:02d}"
            e_fmt = f"{eh:02d}:{em:02d}"
            preview_lbl.config(text=f"→  {n} slots of 30 min  ({s_fmt} – {e_fmt})" if n>0 else "⚠  End time must be after start time")
        except: pass

    for v in [start_h, start_m, end_h, end_m]:
        v.trace_add("write", _update_preview)
    _update_preview()

    err_lbl = tk.Label(af, text="", bg=C_SURFACE, fg=C_RED, font=FN_SMALL)
    err_lbl.pack(anchor="w")

    def save_schedule():
        day  = day_var.get()
        s_time = f"{start_h.get()}:{start_m.get()}:00"
        e_time = f"{end_h.get()}:{end_m.get()}:00"
        sh2 = int(start_h.get()); sm2 = int(start_m.get())
        eh2 = int(end_h.get());   em2 = int(end_m.get())
        total = (eh2*60+em2) - (sh2*60+sm2)
        if total <= 0: total += 24*60
        if total < 30:
            err_lbl.config(text="⚠  End time must be at least 30 min after start."); return
        err_lbl.config(text="")
        try:
            conn = get_connection(); cur = conn.cursor()
            # If schedule for this day already exists, update it
            cur.execute("SELECT Schedule_id FROM Schedules WHERE User_Doctor_id=%s AND Day_Name=%s",
                        (doctor_id, day))
            existing = cur.fetchone()
            if existing:
                cur.execute("UPDATE Schedules SET Start_Time=%s, End_Time=%s WHERE Schedule_id=%s",
                            (s_time, e_time, existing[0]))
            else:
                cur.execute("INSERT INTO Schedules (Day_Name,Start_Time,End_Time,User_Doctor_id) VALUES (%s,%s,%s,%s)",
                            (day, s_time, e_time, doctor_id))
            conn.commit(); conn.close()
            reload_schedules()
            if on_saved: on_saved()
        except Exception as ex:
            err_lbl.config(text=f"⚠  {ex}")

    pill_btn(af, "Save Schedule  →", save_schedule, w=200, h=36,
             color=C_TEAL, hover="#0D9488", fg=C_SURFACE, bg=C_SURFACE,
             font=("Segoe UI",8,"bold")).pack(anchor="w")


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN — MANAGE DOCTORS PANEL
# ══════════════════════════════════════════════════════════════════════════════
def admin_panel_doctors(parent, root, container):
    def load():
        clear(parent)
        pg = scrollable(parent, bg=C_BG)

        hdr_f = tk.Frame(pg, bg=C_BG); hdr_f.pack(fill="x", padx=28, pady=(28,4))
        tk.Label(hdr_f, text="Manage Doctors", bg=C_BG, fg=C_TEXT, font=FN_DISPLAY).pack(side="left")
        pill_btn(hdr_f, "+ Add Doctor", cmd=lambda: admin_add_doctor_modal(on_saved=load),
                 w=110, h=34, color=C_ADMIN, hover=C_ADMIN_D, fg=C_SURFACE, bg=C_BG,
                 font=("Segoe UI",8,"bold")).pack(side="right")

        try:
            conn = get_connection(); cur = conn.cursor(dictionary=True)
            cur.execute("""SELECT u.User_id, u.First_Name, u.Last_Name, u.Email, u.Gender,
                                  s.Specialization_Name, d.Consultant_Fees, d.Experience_Years,
                                  ROUND(COALESCE(AVG(r.Rating),0),1) AS rating,
                                  COUNT(DISTINCT sc.Schedule_id) AS sched_count
                           FROM Doctors d
                           JOIN Users u ON d.User_Doctor_id=u.User_id
                           JOIN Specialization s ON d.Specialization_id=s.Specialization_id
                           LEFT JOIN Appointments a ON a.User_Doctor_id=u.User_id
                           LEFT JOIN Reviews r ON r.Appointment_id=a.Appointment_id
                           LEFT JOIN Schedules sc ON sc.User_Doctor_id=u.User_id
                           GROUP BY u.User_id,u.First_Name,u.Last_Name,u.Email,u.Gender,
                                    s.Specialization_Name,d.Consultant_Fees,d.Experience_Years
                           ORDER BY u.First_Name""")
            doctors = cur.fetchall(); cur.close(); conn.close()
        except Exception as ex:
            tk.Label(pg, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(padx=28); return

        if not doctors:
            tk.Label(pg, text="No doctors found.", bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack(pady=60); return

        sec_hdr(pg, f"{len(doctors)} Doctors Registered", accent=C_ADMIN)

        for doc in doctors:
            sp = doc['Specialization_Name']
            sp_tint, sp_ac, sp_ic = SPEC.get(sp, (C_BLUE_L, C_BLUE, "✚"))
            fname = f"Dr. {doc['First_Name']} {doc['Last_Name']}"

            card = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
            card.pack(fill="x", padx=28, pady=5)
            tk.Frame(card, bg=sp_ac, width=4).pack(side="left", fill="y")

            # Avatar
            av = tk.Canvas(card, width=52, height=52, bg=sp_tint, highlightthickness=0)
            av.pack(side="left", padx=14, pady=14)
            av.create_oval(4,4,48,48, fill=sp_tint, outline=sp_ac)
            av.create_text(26,26, text=sp_ic, fill=sp_ac, font=("Segoe UI",20))

            # Info
            inf = tk.Frame(card, bg=C_SURFACE); inf.pack(side="left", fill="both", expand=True, pady=14)
            nr = tk.Frame(inf, bg=C_SURFACE); nr.pack(anchor="w")
            tk.Label(nr, text=fname, bg=C_SURFACE, fg=C_TEXT, font=FN_SUBH).pack(side="left")
            if doc['rating']:
                tk.Label(nr, text=f"  ★ {doc['rating']}", bg=C_SURFACE, fg=C_AMBER,
                         font=("Segoe UI",8)).pack(side="left")
            tk.Label(inf, text=doc['Email'], bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(anchor="w", pady=(1,5))

            tags = tk.Frame(inf, bg=C_SURFACE); tags.pack(anchor="w")
            tk.Label(tags, text=sp, bg=sp_tint, fg=sp_ac,
                     font=FN_TINY, padx=6, pady=2).pack(side="left", padx=(0,4))
            tk.Label(tags, text=f"{doc['Consultant_Fees']} EGP", bg=C_GREEN_L, fg=C_GREEN,
                     font=FN_TINY, padx=6, pady=2).pack(side="left", padx=(0,4))
            tk.Label(tags, text=f"{doc['Experience_Years']} yrs", bg=C_BLUE_L, fg=C_BLUE,
                     font=FN_TINY, padx=6, pady=2).pack(side="left", padx=(0,4))
            # Schedule badge
            sc_n = doc['sched_count']
            sc_col = C_TEAL if sc_n > 0 else C_RED
            sc_bg  = C_TEAL_L if sc_n > 0 else C_RED_L
            tk.Label(tags, text=f"{'✓' if sc_n>0 else '✗'} {sc_n} day{'s' if sc_n!=1 else ''}",
                     bg=sc_bg, fg=sc_col, font=FN_TINY, padx=6, pady=2).pack(side="left")

            # Buttons
            right = tk.Frame(card, bg=C_SURFACE); right.pack(side="right", padx=14, pady=10)

            ghost_btn(right, "📅 Schedule",
                      cmd=lambda uid=doc['User_id'], fn=fname:
                          admin_schedule_modal(uid, fn, on_saved=load),
                      w=96, h=28, color=C_TEAL, hover_color=C_TEAL,
                      text_col=C_TEAL, bg=C_SURFACE).pack(pady=(0,6))

            def do_remove(uid=doc['User_id'], name=fname):
                if not messagebox.askyesno("Remove Doctor",
                    f"Remove {name}?\nThis will also delete their appointments and reports."): return
                try:
                    conn2 = get_connection(); cur2 = conn2.cursor()
                    cur2.execute("DELETE FROM Reviews WHERE Appointment_id IN "
                                 "(SELECT Appointment_id FROM Appointments WHERE User_Doctor_id=%s)", (uid,))
                    cur2.execute("DELETE FROM Appointments WHERE User_Doctor_id=%s", (uid,))
                    cur2.execute("DELETE FROM Medical_Reports WHERE User_Doctor_id=%s", (uid,))
                    cur2.execute("DELETE FROM Works_At WHERE Doctor_id=%s", (uid,))
                    cur2.execute("DELETE FROM Take_Place_In WHERE Schedule_id IN "
                                 "(SELECT Schedule_id FROM Schedules WHERE User_Doctor_id=%s)", (uid,))
                    cur2.execute("DELETE FROM Schedules WHERE User_Doctor_id=%s", (uid,))
                    cur2.execute("DELETE FROM Doctors WHERE User_Doctor_id=%s", (uid,))
                    cur2.execute("DELETE FROM Management WHERE User_id=%s", (uid,))
                    cur2.execute("DELETE FROM User_Phone WHERE User_id=%s", (uid,))
                    cur2.execute("DELETE FROM Users WHERE User_id=%s", (uid,))
                    conn2.commit(); conn2.close()
                    messagebox.showinfo("Removed", f"{name} removed.")
                    load()
                except Exception as ex2:
                    messagebox.showerror("Error", str(ex2))

            ghost_btn(right, "✕ Remove", do_remove, w=96, h=28,
                      color=C_RED, hover_color=C_RED, text_col=C_RED, bg=C_SURFACE).pack()
    load()

# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN — MANAGE APPOINTMENTS PANEL
# ══════════════════════════════════════════════════════════════════════════════
def admin_panel_appointments(parent):
    def load():
        clear(parent)
        pg = scrollable(parent, bg=C_BG)
        hdr_f = tk.Frame(pg, bg=C_BG); hdr_f.pack(fill="x", padx=28, pady=(28,4))
        tk.Label(hdr_f, text="All Appointments", bg=C_BG, fg=C_TEXT, font=FN_DISPLAY).pack(side="left")

        try:
            conn = get_connection(); cur = conn.cursor(dictionary=True)
            cur.execute("""SELECT a.Appointment_id, a.Appointment_Date,
                                  du.First_Name AS d_fn, du.Last_Name AS d_ln,
                                  pu.First_Name AS p_fn, pu.Last_Name AS p_ln,
                                  s.Specialization_Name,
                                  sc.Day_Name,
                                  TIME_FORMAT(sc.Start_Time,'%I:%i %p') AS t_start,
                                  TIME_FORMAT(sc.End_Time,'%I:%i %p')   AS t_end
                           FROM Appointments a
                           JOIN Users du ON a.User_Doctor_id=du.User_id
                           JOIN Users pu ON a.User_Patient_id=pu.User_id
                           JOIN Doctors d ON d.User_Doctor_id=du.User_id
                           JOIN Specialization s ON d.Specialization_id=s.Specialization_id
                           JOIN Schedules sc ON a.Schedule_id=sc.Schedule_id
                           ORDER BY a.Appointment_Date DESC""")
            appts = cur.fetchall(); cur.close(); conn.close()
        except Exception as ex:
            tk.Label(pg, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(padx=28); return

        if not appts:
            tk.Label(pg, text="No appointments found.", bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack(pady=60); return

        today = datetime.now().date()
        upcoming = [a for a in appts if datetime.strptime(str(a['Appointment_Date'])[:10],"%Y-%m-%d").date() >= today]
        past     = [a for a in appts if datetime.strptime(str(a['Appointment_Date'])[:10],"%Y-%m-%d").date() < today]

        def render_group(items, title, accent, accent_l):
            if not items: return
            sec_hdr(pg, f"{title}  ({len(items)})", accent=accent)
            for ap in items:
                sp = ap['Specialization_Name']
                sp_tint, sp_ac, sp_ic = SPEC.get(sp, (C_BLUE_L, C_BLUE, "✚"))
                ap_date = str(ap['Appointment_Date'])[:10]

                card = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
                card.pack(fill="x", padx=28, pady=3)
                tk.Frame(card, bg=accent, width=4).pack(side="left", fill="y")

                av = tk.Canvas(card, width=46, height=46, bg=sp_tint, highlightthickness=0)
                av.pack(side="left", padx=12, pady=10)
                av.create_text(23,23, text=sp_ic, fill=sp_ac, font=("Segoe UI",16))

                inf = tk.Frame(card, bg=C_SURFACE); inf.pack(side="left", fill="both", expand=True, pady=10)
                row1 = tk.Frame(inf, bg=C_SURFACE); row1.pack(anchor="w")
                tk.Label(row1, text=f"Dr. {ap['d_fn']} {ap['d_ln']}", bg=C_SURFACE, fg=C_TEXT,
                         font=FN_SUBH).pack(side="left")
                tk.Label(row1, text="  →  ", bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(side="left")
                tk.Label(row1, text=f"{ap['p_fn']} {ap['p_ln']}", bg=C_SURFACE, fg=C_TEXT2,
                         font=FN_BODY).pack(side="left")
                row2 = tk.Frame(inf, bg=C_SURFACE); row2.pack(anchor="w", pady=(3,0))
                tk.Label(row2, text=ap_date, bg=C_SURFACE, fg=C_TEXT2, font=FN_SMALL).pack(side="left", padx=(0,10))
                tk.Label(row2, text=f"{ap['Day_Name']}  ·  {ap['t_start']} – {ap['t_end']}",
                         bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(side="left")

                right = tk.Frame(card, bg=C_SURFACE); right.pack(side="right", padx=14)
                tk.Label(right, text="Upcoming" if accent==C_GREEN else "Past",
                         bg=accent_l, fg=accent, font=FN_LABEL, padx=8, pady=3).pack(pady=(10,4))

                aid = ap['Appointment_id']
                def do_del(a_id=aid, dn=f"Dr. {ap['d_fn']} {ap['d_ln']}", pn=f"{ap['p_fn']} {ap['p_ln']}", dd=ap_date):
                    if not messagebox.askyesno("Delete Appointment",
                        f"Delete appointment:\n{dn}  →  {pn}\n{dd}?"): return
                    try:
                        c2 = get_connection(); cu2 = c2.cursor()
                        cu2.execute("DELETE FROM Reviews WHERE Appointment_id=%s", (a_id,))
                        cu2.execute("DELETE FROM Appointments WHERE Appointment_id=%s", (a_id,))
                        c2.commit(); c2.close(); load()
                    except Exception as ex2: messagebox.showerror("Error", str(ex2))

                ghost_btn(right, "✕ Delete", do_del, w=80, h=26,
                          color=C_RED, hover_color=C_RED, text_col=C_RED, bg=C_SURFACE).pack(pady=(0,8))

        render_group(upcoming, "Upcoming", C_GREEN, C_GREEN_L)
        render_group(past,     "Past",     C_TEXT3, C_SURFACE2)
    load()

# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN — MANAGE PATIENTS PANEL
# ══════════════════════════════════════════════════════════════════════════════
def admin_panel_patients(parent):
    def load():
        clear(parent)
        pg = scrollable(parent, bg=C_BG)
        hdr_f = tk.Frame(pg, bg=C_BG); hdr_f.pack(fill="x", padx=28, pady=(28,4))
        tk.Label(hdr_f, text="Manage Patients", bg=C_BG, fg=C_TEXT, font=FN_DISPLAY).pack(side="left")

        try:
            conn = get_connection(); cur = conn.cursor(dictionary=True)
            cur.execute("""SELECT u.User_id, u.First_Name, u.Last_Name, u.Email, u.Gender,
                                  p.Date_Of_Birth,
                                  COUNT(a.Appointment_id) AS appt_count
                           FROM Patients p
                           JOIN Users u ON p.User_Patient_id=u.User_id
                           LEFT JOIN Appointments a ON a.User_Patient_id=u.User_id
                           GROUP BY u.User_id,u.First_Name,u.Last_Name,u.Email,u.Gender,p.Date_Of_Birth
                           ORDER BY u.First_Name""")
            patients = cur.fetchall(); cur.close(); conn.close()
        except Exception as ex:
            tk.Label(pg, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(padx=28); return

        if not patients:
            tk.Label(pg, text="No patients found.", bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack(pady=60); return

        sec_hdr(pg, f"{len(patients)} Patients Registered", accent=C_ADMIN)

        for pat in patients:
            pname = f"{pat['First_Name']} {pat['Last_Name']}"
            dob = str(pat['Date_Of_Birth'])
            try: age = datetime.now().year - int(dob[:4])
            except: age = "?"
            gc = C_BLUE if pat['Gender']=="Male" else C_PURPLE
            gl = C_BLUE_L if pat['Gender']=="Male" else C_PURPLE_L

            card = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
            card.pack(fill="x", padx=28, pady=4)
            tk.Frame(card, bg=gc, width=4).pack(side="left", fill="y")

            av = tk.Canvas(card, width=48, height=48, bg=gl, highlightthickness=0)
            av.pack(side="left", padx=14, pady=12)
            av.create_oval(3,3,45,45, fill=gl, outline=gc)
            av.create_text(24,24, text=pat['First_Name'][0].upper(), fill=gc,
                           font=("Segoe UI",14,"bold"))

            inf = tk.Frame(card, bg=C_SURFACE); inf.pack(side="left", fill="both", expand=True, pady=12)
            tk.Label(inf, text=pname, bg=C_SURFACE, fg=C_TEXT, font=FN_SUBH).pack(anchor="w")
            tk.Label(inf, text=pat['Email'], bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(anchor="w", pady=(1,4))
            tags = tk.Frame(inf, bg=C_SURFACE); tags.pack(anchor="w")
            tk.Label(tags, text=f"Age {age}", bg=C_SURFACE2, fg=C_TEXT2, font=FN_TINY, padx=6, pady=2).pack(side="left", padx=(0,5))
            tk.Label(tags, text=f"DOB {dob}", bg=C_SURFACE2, fg=C_TEXT2, font=FN_TINY, padx=6, pady=2).pack(side="left", padx=(0,5))
            tk.Label(tags, text=f"{pat['appt_count']} appointments", bg=C_BLUE_L, fg=C_BLUE,
                     font=FN_TINY, padx=6, pady=2).pack(side="left")

            right = tk.Frame(card, bg=C_SURFACE); right.pack(side="right", padx=14)
            def do_remove(uid=pat['User_id'], name=pname):
                if not messagebox.askyesno("Remove Patient",
                    f"Remove {name}?\nThis will delete all their data."): return
                try:
                    conn2 = get_connection(); cur2 = conn2.cursor()
                    cur2.execute("DELETE FROM Reviews WHERE Appointment_id IN (SELECT Appointment_id FROM Appointments WHERE User_Patient_id=%s)", (uid,))
                    cur2.execute("DELETE FROM Appointments WHERE User_Patient_id=%s", (uid,))
                    cur2.execute("DELETE FROM Medicines WHERE Report_id IN (SELECT Report_id FROM Medical_Reports WHERE User_Patient_id=%s)", (uid,))
                    cur2.execute("DELETE FROM Test_Results WHERE Report_id IN (SELECT Report_id FROM Medical_Reports WHERE User_Patient_id=%s)", (uid,))
                    cur2.execute("DELETE FROM Medical_Reports WHERE User_Patient_id=%s", (uid,))
                    cur2.execute("DELETE FROM Insurance WHERE User_Patient_id=%s", (uid,))
                    cur2.execute("DELETE FROM Patients WHERE User_Patient_id=%s", (uid,))
                    cur2.execute("DELETE FROM Management WHERE User_id=%s", (uid,))
                    cur2.execute("DELETE FROM User_Phone WHERE User_id=%s", (uid,))
                    cur2.execute("DELETE FROM Users WHERE User_id=%s", (uid,))
                    conn2.commit(); conn2.close()
                    messagebox.showinfo("Removed", f"{name} removed.")
                    load()
                except Exception as ex2: messagebox.showerror("Error", str(ex2))

            ghost_btn(right, "✕ Remove", do_remove, w=88, h=28,
                      color=C_RED, hover_color=C_RED, text_col=C_RED, bg=C_SURFACE).pack(pady=12)
    load()

# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN — REVIEWS PANEL
# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN — REVIEWS PANEL  (view & delete only)
# ══════════════════════════════════════════════════════════════════════════════
def admin_panel_reviews(parent, admin_id):
    def load():
        clear(parent)
        pg = scrollable(parent, bg=C_BG)
        hdr_f = tk.Frame(pg, bg=C_BG); hdr_f.pack(fill="x", padx=28, pady=(28,4))
        tk.Label(hdr_f, text="Reviews", bg=C_BG, fg=C_TEXT, font=FN_DISPLAY).pack(side="left")

        try:
            conn = get_connection(); cur = conn.cursor(dictionary=True)
            cur.execute("""SELECT r.Review_id, r.Rating,
                                  du.First_Name AS d_fn, du.Last_Name AS d_ln,
                                  pu.First_Name AS p_fn, pu.Last_Name AS p_ln,
                                  a.Appointment_Date
                           FROM Reviews r
                           JOIN Appointments a ON r.Appointment_id=a.Appointment_id
                           JOIN Users du ON a.User_Doctor_id=du.User_id
                           JOIN Users pu ON a.User_Patient_id=pu.User_id
                           ORDER BY a.Appointment_Date DESC""")
            reviews = cur.fetchall(); cur.close(); conn.close()
        except Exception as ex:
            tk.Label(pg, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(padx=28); return

        if not reviews:
            ef = tk.Frame(pg, bg=C_BG); ef.pack(expand=True, pady=80)
            tk.Label(ef, text="No reviews yet.", bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack()
            tk.Label(ef, text="Reviews are submitted by patients after their appointments.",
                     bg=C_BG, fg=C_TEXT3, font=FN_SMALL).pack(pady=4)
            return

        sec_hdr(pg, f"All Reviews  ({len(reviews)})", accent=C_AMBER)

        for rev in reviews:
            stars = "★" * rev['Rating'] + "☆" * (5 - rev['Rating'])
            ap_date = str(rev['Appointment_Date'])[:10]

            card = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
            card.pack(fill="x", padx=28, pady=4)
            tk.Frame(card, bg=C_AMBER, width=4).pack(side="left", fill="y")

            # Star badge
            badge = tk.Canvas(card, width=48, height=48, bg=C_AMBER_L, highlightthickness=0)
            badge.pack(side="left", padx=14, pady=12)
            badge.create_oval(3,3,45,45, fill=C_AMBER_L, outline=C_AMBER)
            badge.create_text(24,24, text=str(rev['Rating']), fill=C_AMBER,
                              font=("Segoe UI",16,"bold"))

            inf = tk.Frame(card, bg=C_SURFACE)
            inf.pack(side="left", fill="both", expand=True, padx=4, pady=12)

            row1 = tk.Frame(inf, bg=C_SURFACE); row1.pack(anchor="w")
            tk.Label(row1, text=f"Dr. {rev['d_fn']} {rev['d_ln']}",
                     bg=C_SURFACE, fg=C_TEXT, font=FN_SUBH).pack(side="left")
            tk.Label(row1, text="  ←  ", bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(side="left")
            tk.Label(row1, text=f"{rev['p_fn']} {rev['p_ln']}",
                     bg=C_SURFACE, fg=C_TEXT2, font=FN_BODY).pack(side="left")

            row2 = tk.Frame(inf, bg=C_SURFACE); row2.pack(anchor="w", pady=(4,0))
            tk.Label(row2, text=stars, bg=C_SURFACE, fg=C_AMBER,
                     font=("Segoe UI",11)).pack(side="left")
            tk.Label(row2, text=f"  {rev['Rating']}/5  ·  {ap_date}",
                     bg=C_SURFACE, fg=C_TEXT3, font=FN_SMALL).pack(side="left")

            right = tk.Frame(card, bg=C_SURFACE); right.pack(side="right", padx=14)
            def do_del_rev(rid=rev['Review_id']):
                if not messagebox.askyesno("Delete Review",
                    "Delete this review? This cannot be undone."): return
                try:
                    c2 = get_connection(); cu2 = c2.cursor()
                    cu2.execute("DELETE FROM Reviews WHERE Review_id=%s", (rid,))
                    c2.commit(); c2.close(); load()
                except Exception as ex2:
                    messagebox.showerror("Error", str(ex2))
            ghost_btn(right, "✕ Delete", do_del_rev, w=80, h=28,
                      color=C_RED, hover_color=C_RED, text_col=C_RED, bg=C_SURFACE).pack(pady=12)
    load()

# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN — DOCTOR REQUESTS PANEL
# ══════════════════════════════════════════════════════════════════════════════
def admin_panel_requests(parent):
    def load():
        clear(parent)
        # Create table if it doesn't exist yet
        try:
            conn0 = get_connection(); cur0 = conn0.cursor()
            cur0.execute("""CREATE TABLE IF NOT EXISTS Doctor_Requests (
                Request_id INT PRIMARY KEY AUTO_INCREMENT,
                First_Name VARCHAR(45) NOT NULL,
                Last_Name VARCHAR(45) NOT NULL,
                Email VARCHAR(100) NOT NULL UNIQUE,
                Password VARCHAR(255) NOT NULL,
                Gender ENUM('Male','Female') NOT NULL,
                Specialization_id INT NOT NULL,
                Consultant_Fees INT NOT NULL,
                Experience_Years INT NOT NULL,
                Requested_At DATETIME DEFAULT CURRENT_TIMESTAMP,
                Status ENUM('Pending','Accepted','Rejected') DEFAULT 'Pending'
            )""")
            conn0.commit(); cur0.close(); conn0.close()
        except: pass
        clear(parent)
        pg = scrollable(parent, bg=C_BG)
        hdr_f = tk.Frame(pg, bg=C_BG); hdr_f.pack(fill="x", padx=28, pady=(28,4))
        tk.Label(hdr_f, text="Doctor Applications", bg=C_BG, fg=C_TEXT, font=FN_DISPLAY).pack(side="left")

        try:
            conn = get_connection(); cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT dr.*, s.Specialization_Name
                FROM Doctor_Requests dr
                JOIN Specialization s ON dr.Specialization_id=s.Specialization_id
                ORDER BY dr.Requested_At DESC
            """)
            requests = cur.fetchall(); cur.close(); conn.close()
        except Exception as ex:
            tk.Label(pg, text=f"Error: {ex}", fg=C_RED, bg=C_BG).pack(padx=28); return

        pending  = [r for r in requests if r['Status'] == 'Pending']
        accepted = [r for r in requests if r['Status'] == 'Accepted']
        rejected = [r for r in requests if r['Status'] == 'Rejected']

        def render_group(items, title, accent, accent_l, show_actions=False):
            if not items: return
            sec_hdr(pg, f"{title}  ({len(items)})", accent=accent)
            for req in items:
                sp = req['Specialization_Name']
                sp_tint, sp_ac, sp_ic = SPEC.get(sp, (C_BLUE_L, C_BLUE, "✚"))
                fname = f"Dr. {req['First_Name']} {req['Last_Name']}"
                req_date = str(req['Requested_At'])[:10]

                card = tk.Frame(pg, bg=C_SURFACE,
                                highlightbackground=C_BORDER, highlightthickness=1)
                card.pack(fill="x", padx=28, pady=5)
                tk.Frame(card, bg=accent, width=4).pack(side="left", fill="y")

                # Avatar
                av = tk.Canvas(card, width=52, height=52, bg=sp_tint, highlightthickness=0)
                av.pack(side="left", padx=14, pady=14)
                av.create_oval(4,4,48,48, fill=sp_tint, outline=sp_ac)
                av.create_text(26,26, text=sp_ic, fill=sp_ac, font=("Segoe UI",20))

                # Info
                inf = tk.Frame(card, bg=C_SURFACE)
                inf.pack(side="left", fill="both", expand=True, pady=14)

                name_row = tk.Frame(inf, bg=C_SURFACE); name_row.pack(anchor="w")
                tk.Label(name_row, text=fname, bg=C_SURFACE, fg=C_TEXT,
                         font=FN_SUBH).pack(side="left")
                tk.Label(name_row, text=f"  ·  Applied {req_date}",
                         bg=C_SURFACE, fg=C_TEXT3, font=FN_TINY).pack(side="left")

                tk.Label(inf, text=req['Email'], bg=C_SURFACE, fg=C_TEXT3,
                         font=FN_SMALL).pack(anchor="w", pady=(1,5))

                tags = tk.Frame(inf, bg=C_SURFACE); tags.pack(anchor="w")
                tk.Label(tags, text=sp, bg=sp_tint, fg=sp_ac,
                         font=FN_TINY, padx=6, pady=2).pack(side="left", padx=(0,4))
                tk.Label(tags, text=f"{req['Consultant_Fees']} EGP",
                         bg=C_GREEN_L, fg=C_GREEN,
                         font=FN_TINY, padx=6, pady=2).pack(side="left", padx=(0,4))
                tk.Label(tags, text=f"{req['Experience_Years']} yrs exp",
                         bg=C_BLUE_L, fg=C_BLUE,
                         font=FN_TINY, padx=6, pady=2).pack(side="left", padx=(0,4))
                tk.Label(tags, text=req['Gender'], bg=C_SURFACE2, fg=C_TEXT2,
                         font=FN_TINY, padx=6, pady=2).pack(side="left")

                # Action buttons
                right = tk.Frame(card, bg=C_SURFACE); right.pack(side="right", padx=14, pady=10)

                if show_actions:
                    def do_accept(rid=req['Request_id'],
                                  fn=req['First_Name'], ln=req['Last_Name'],
                                  em=req['Email'], pw=req['Password'],
                                  gen=req['Gender'], sid=req['Specialization_id'],
                                  fee=req['Consultant_Fees'], exp=req['Experience_Years']):
                        if not messagebox.askyesno("Accept Doctor",
                            f"Accept Dr. {fn} {ln}?\nThis will create their account."): return
                        try:
                            conn2 = get_connection(); cur2 = conn2.cursor()
                            # Create user account
                            cur2.execute(
                                "INSERT INTO Users (First_Name,Last_Name,Email,Password,Gender) "
                                "VALUES (%s,%s,%s,%s,%s)", (fn, ln, em, pw, gen))
                            uid = cur2.lastrowid
                            # Create doctor record
                            cur2.execute(
                                "INSERT INTO Doctors (User_Doctor_id,Consultant_Fees,Experience_Years,Specialization_id) "
                                "VALUES (%s,%s,%s,%s)", (uid, fee, exp, sid))
                            # Mark request accepted
                            cur2.execute(
                                "UPDATE Doctor_Requests SET Status='Accepted' WHERE Request_id=%s", (rid,))
                            conn2.commit(); conn2.close()
                            messagebox.showinfo("Accepted ✓",
                                f"Dr. {fn} {ln} can now sign in with:\n{em}")
                            load()
                        except mysql.connector.IntegrityError:
                            messagebox.showerror("Error",
                                "Email already exists in Users table.")
                        except Exception as ex2:
                            messagebox.showerror("Error", str(ex2))

                    def do_reject(rid=req['Request_id'],
                                  fn=req['First_Name'], ln=req['Last_Name']):
                        if not messagebox.askyesno("Reject Application",
                            f"Reject Dr. {fn} {ln}'s application?"): return
                        try:
                            conn2 = get_connection(); cur2 = conn2.cursor()
                            cur2.execute(
                                "UPDATE Doctor_Requests SET Status='Rejected' WHERE Request_id=%s", (rid,))
                            conn2.commit(); conn2.close()
                            load()
                        except Exception as ex2:
                            messagebox.showerror("Error", str(ex2))

                    pill_btn(right, "✓ Accept", do_accept, w=90, h=30,
                             color=C_GREEN, hover="#16A34A", fg=C_SURFACE,
                             bg=C_SURFACE, font=("Segoe UI",8,"bold")).pack(pady=(0,6))
                    ghost_btn(right, "✕ Reject", do_reject, w=90, h=28,
                              color=C_RED, hover_color=C_RED,
                              text_col=C_RED, bg=C_SURFACE).pack()
                else:
                    # Show status badge only
                    badge_c = C_GREEN if req['Status']=='Accepted' else C_RED
                    badge_l = C_GREEN_L if req['Status']=='Accepted' else C_RED_L
                    tk.Label(right, text=req['Status'],
                             bg=badge_l, fg=badge_c,
                             font=FN_LABEL, padx=10, pady=5).pack(pady=14)

        if not requests:
            ef = tk.Frame(pg, bg=C_BG); ef.pack(expand=True, pady=80)
            tk.Label(ef, text="No doctor applications yet.",
                     bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack()
            return

        render_group(pending,  "Pending Review", C_ADMIN,  C_ADMIN_L,  show_actions=True)
        render_group(accepted, "Accepted",        C_GREEN,  C_GREEN_L,  show_actions=False)
        render_group(rejected, "Rejected",        C_RED,    C_RED_L,    show_actions=False)
    load()

# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN — OVERVIEW PANEL
# ══════════════════════════════════════════════════════════════════════════════
def admin_panel_overview(parent, admin, nav_cb):
    pg = scrollable(parent, bg=C_BG)

    # Hero
    hero = tk.Canvas(pg, height=148, bg=C_BG, highlightthickness=0)
    hero.pack(fill="x")
    def draw_hero(e=None):
        w = hero.winfo_width() or 900
        hero.delete("all")
        hero.create_rectangle(0, 0, w, 148, fill=C_SURFACE, outline="")
        hero.create_rectangle(0, 0, w, 4, fill=C_ADMIN, outline="")
        hero.create_oval(w-160,-60,w+60,160, fill=C_ADMIN_L, outline="")
        hero.create_oval(w-120,-20,w+20,120, fill=C_PANEL, outline="")
        hero.create_text(32, 55, text=f"Admin Panel  —  {admin['First_Name']} {admin['Last_Name']}",
                         fill=C_TEXT, font=("Segoe UI",17,"bold"), anchor="w")
        hero.create_text(32, 85, text="Full control over E7gezly platform",
                         fill=C_TEXT2, font=("Segoe UI",9), anchor="w")
        hero.create_rectangle(0,146,w,148, fill=C_BORDER, outline="")
    hero.bind("<Configure>", draw_hero)
    hero.after(50, draw_hero)

    # Stats
    try:
        conn = get_connection(); cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Doctors"); docs_n = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM Patients"); pats_n = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM Appointments"); appts_n = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM Reviews"); revs_n = cur.fetchone()[0]
        try:
            cur.execute("SELECT COUNT(*) FROM Doctor_Requests WHERE Status='Pending'")
            pending_n = cur.fetchone()[0]
        except: pending_n = 0
        cur.close(); conn.close()
    except: docs_n=pats_n=appts_n=revs_n=pending_n=0

    stats_row = tk.Frame(pg, bg=C_BG); stats_row.pack(fill="x", padx=28, pady=16)
    stat_card(stats_row, docs_n,  "Doctors",      C_TEAL,  C_TEAL_L)
    stat_card(stats_row, pats_n,  "Patients",     C_BLUE,  C_BLUE_L)
    stat_card(stats_row, appts_n, "Appointments", C_GREEN, C_GREEN_L)
    stat_card(stats_row, revs_n,  "Reviews",      C_AMBER, C_AMBER_L)
    if pending_n > 0:
        stat_card(stats_row, pending_n, "Pending Requests", C_ADMIN, C_ADMIN_L)

    # Quick actions
    sec_hdr(pg, "Admin Controls", accent=C_ADMIN)
    qa_row = tk.Frame(pg, bg=C_BG); qa_row.pack(fill="x", padx=28, pady=(0,24))

    def qa_card(parent, icon, title, sub, cmd, accent, accent_l):
        cv = tk.Canvas(parent, width=185, height=110, bg=C_BG, highlightthickness=0)
        cv.pack(side="left", padx=5)
        def draw(hover=False):
            cv.delete("all")
            rr(cv, 0, 0, 185, 110, r=12, fill=C_SURFACE)
            rr_outline(cv, 0, 0, 185, 110, r=12, color=accent if hover else C_BORDER)
            rr(cv, 0, 0, 185, 4, r=2, fill=accent)
            cv.create_oval(76,16,110,50, fill=accent_l, outline="")
            cv.create_text(93, 33, text=icon, fill=accent, font=("Segoe UI",14))
            cv.create_text(93, 68, text=title, fill=C_TEXT, font=("Segoe UI",8,"bold"))
            cv.create_text(93, 84, text=sub, fill=C_TEXT3, font=("Segoe UI",7))
        draw()
        cv.bind("<Button-1>", lambda e: cmd())
        cv.bind("<Enter>", lambda e: draw(True))
        cv.bind("<Leave>", lambda e: draw(False))

    qa_card(qa_row, "👨‍⚕️", "Doctors",      "Add / remove doctors",    lambda: nav_cb("Doctors"),      C_TEAL,  C_TEAL_L)
    qa_card(qa_row, "👥",   "Patients",     "View / remove patients",  lambda: nav_cb("Patients"),     C_BLUE,  C_BLUE_L)
    qa_card(qa_row, "📅",   "Appointments", "Manage all appointments", lambda: nav_cb("Appointments"), C_GREEN, C_GREEN_L)
    qa_card(qa_row, "★",    "Reviews",      "Manage ratings",          lambda: nav_cb("Reviews"),      C_AMBER, C_AMBER_L)
    qa_card(qa_row, "📋",   "Requests",     "Doctor applications",     lambda: nav_cb("Requests"),     C_ADMIN, C_ADMIN_L)

# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def show_admin_home(root, container, admin):
    clear(container); root.geometry("1080x700")
    wrapper = tk.Frame(container, bg=C_BG); wrapper.pack(fill="both", expand=True)

    # Sidebar
    sidebar = tk.Frame(wrapper, bg=C_PANEL, width=220)
    sidebar.pack(side="left", fill="y"); sidebar.pack_propagate(False)
    tk.Frame(sidebar, bg=C_ADMIN, height=3).pack(fill="x")

    logo_f = tk.Frame(sidebar, bg=C_PANEL, height=64); logo_f.pack(fill="x"); logo_f.pack_propagate(False)
    tk.Label(logo_f, text="✚  E7gezly", bg=C_PANEL, fg=C_TEXT,
             font=("Segoe UI",14,"bold")).pack(side="left", padx=20, pady=20)
    tk.Frame(sidebar, bg=C_BORDER, height=1).pack(fill="x")

    chip = tk.Frame(sidebar, bg=C_SURFACE); chip.pack(fill="x")
    av_cv = tk.Canvas(chip, width=42, height=42, bg=C_SURFACE, highlightthickness=0)
    av_cv.pack(side="left", padx=(16,10), pady=14)
    av_cv.create_oval(1,1,41,41, fill=C_ADMIN_L, outline=C_ADMIN)
    av_cv.create_text(21,21, text=admin['First_Name'][0].upper(),
                      fill=C_ADMIN, font=("Segoe UI",13,"bold"))
    uc = tk.Frame(chip, bg=C_SURFACE); uc.pack(side="left", pady=10)
    tk.Label(uc, text=f"{admin['First_Name']} {admin['Last_Name']}",
             bg=C_SURFACE, fg=C_TEXT, font=("Segoe UI",8,"bold")).pack(anchor="w")
    tk.Label(uc, text="ADMINISTRATOR", bg=C_SURFACE, fg=C_ADMIN, font=FN_LABEL).pack(anchor="w")
    tk.Frame(sidebar, bg=C_BORDER, height=1).pack(fill="x")

    content = tk.Frame(wrapper, bg=C_BG); content.pack(side="right", fill="both", expand=True)
    active = {"lbl": None, "btns": {}}

    def nav_to(label):
        clear(content)
        for l2, b2 in active["btns"].items():
            b2.config(bg=C_ADMIN_L if l2==label else C_PANEL,
                      fg=C_ADMIN   if l2==label else C_TEXT2)
        active["lbl"] = label
        if   label == "Overview":     admin_panel_overview(content, admin, nav_to)
        elif label == "Doctors":      admin_panel_doctors(content, root, container)
        elif label == "Patients":     admin_panel_patients(content)
        elif label == "Appointments": admin_panel_appointments(content)
        elif label == "Reviews":      admin_panel_reviews(content, admin['Admin_id'])
        elif label == "Requests":     admin_panel_requests(content)

    MENU = [("⊹","Overview"),("👨‍⚕️","Doctors"),("👥","Patients"),("📅","Appointments"),("★","Reviews"),("📋","Requests")]
    for icon, label in MENU:
        btn = tk.Button(sidebar, text=f"   {icon}   {label}",
                        bg=C_PANEL, fg=C_TEXT2, font=("Segoe UI",9),
                        relief="flat", anchor="w", activebackground=C_ADMIN_L,
                        activeforeground=C_ADMIN, bd=0, padx=0,
                        command=lambda l=label: nav_to(l))
        btn.pack(fill="x", ipady=12)
        btn.bind("<Enter>", lambda e, b=btn, l=label:
            b.config(bg=C_SURFACE, fg=C_ADMIN) if active["lbl"]!=l else None)
        btn.bind("<Leave>", lambda e, b=btn, l=label:
            b.config(bg=C_ADMIN_L if active["lbl"]==l else C_PANEL,
                     fg=C_ADMIN   if active["lbl"]==l else C_TEXT2))
        active["btns"][label] = btn

    tk.Frame(sidebar, bg=C_BORDER, height=1).pack(side="bottom", fill="x")
    lo = tk.Button(sidebar, text="   ⏻   Sign Out",
                   bg=C_PANEL, fg=C_RED, font=("Segoe UI",9),
                   relief="flat", anchor="w", bd=0,
                   activebackground=C_RED_L, activeforeground=C_RED,
                   command=lambda: (
                       messagebox.askyesno("Sign Out","Sign out of E7gezly?") and
                       show_login(root, container)
                   ))
    lo.pack(side="bottom", fill="x", ipady=12)
    lo.bind("<Enter>", lambda e: lo.config(bg=C_RED_L))
    lo.bind("<Leave>", lambda e: lo.config(bg=C_PANEL))

    nav_to("Overview")

# ══════════════════════════════════════════════════════════════════════════════
#  DOCTOR REQUEST — ensure pending table exists
# ══════════════════════════════════════════════════════════════════════════════
def ensure_doctor_requests_table():
    """Create Doctor_Requests table if it doesn't exist yet."""
    try:
        conn = get_connection(); cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Doctor_Requests (
                Request_id       INT PRIMARY KEY AUTO_INCREMENT,
                First_Name       VARCHAR(45)  NOT NULL,
                Last_Name        VARCHAR(45)  NOT NULL,
                Email            VARCHAR(100) NOT NULL UNIQUE,
                Password         VARCHAR(255) NOT NULL,
                Gender           ENUM('Male','Female') NOT NULL,
                Specialization_id INT NOT NULL,
                Consultant_Fees  INT NOT NULL,
                Experience_Years INT NOT NULL,
                Requested_At     DATETIME DEFAULT CURRENT_TIMESTAMP,
                Status           ENUM('Pending','Accepted','Rejected') DEFAULT 'Pending',
                FOREIGN KEY (Specialization_id) REFERENCES Specialization(Specialization_id)
            )
        """)
        conn.commit(); cur.close(); conn.close()
    except Exception as ex:
        print(f"[Doctor_Requests table] {ex}")

# ══════════════════════════════════════════════════════════════════════════════
#  DOCTOR SIGN-UP PAGE
# ══════════════════════════════════════════════════════════════════════════════
def show_doctor_register(root, container):
    clear(container); root.geometry("540x780")
    page = tk.Frame(container, bg=C_BG); page.pack(fill="both", expand=True)

    # Top bar
    top = tk.Frame(page, bg=C_SURFACE, height=58); top.pack(fill="x"); top.pack_propagate(False)
    tk.Frame(top, bg=C_TEAL, height=3).pack(fill="x")
    tk.Label(top, text="✚  E7gezly", bg=C_SURFACE, fg=C_TEXT,
             font=("Segoe UI",13,"bold")).pack(side="left", padx=24, pady=12)
    back = tk.Label(top, text="← Sign In", bg=C_SURFACE, fg=C_TEAL,
                    font=FN_BODY, cursor="hand2")
    back.pack(side="right", padx=24)
    back.bind("<Button-1>", lambda e: show_login(root, container))

    pg = scrollable(page, bg=C_BG)

    tk.Label(pg, text="Join as a Doctor", bg=C_BG, fg=C_TEXT,
             font=FN_DISPLAY).pack(anchor="w", padx=36, pady=(28,2))
    tk.Label(pg, text="Fill in your details. An admin will review and approve your account.",
             bg=C_BG, fg=C_TEXT2, font=FN_BODY).pack(anchor="w", padx=36)

    card = tk.Frame(pg, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
    card.pack(fill="x", padx=36, pady=16)
    ci = tk.Frame(card, bg=C_SURFACE); ci.pack(padx=24, pady=20, fill="x")

    def lbl(t):
        tk.Label(ci, text=t, bg=C_SURFACE, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w", pady=(10,3))

    def ent(secret=False):
        e = styled_entry(ci, secret=secret); e.pack(fill="x", ipady=9); return e

    lbl("FIRST NAME");   fn_e = ent()
    lbl("LAST NAME");    ln_e = ent()

    # Email — username part only, domain fixed
    lbl("EMAIL  (username only — domain is @e7gezly.com)")
    em_row = tk.Frame(ci, bg=C_SURFACE); em_row.pack(fill="x")
    em_e = tk.Entry(em_row, font=FN_BODY, fg=C_TEXT, bg=C_SURFACE,
                    insertbackground=C_TEAL, relief="flat", bd=0,
                    highlightbackground=C_BORDER, highlightthickness=1,
                    highlightcolor=C_TEAL)
    em_e.pack(side="left", fill="x", expand=True, ipady=9)
    em_e.bind("<FocusIn>",  lambda e: em_e.config(highlightbackground=C_TEAL))
    em_e.bind("<FocusOut>", lambda e: em_e.config(highlightbackground=C_BORDER))
    tk.Label(em_row, text="@e7gezly.com", bg=C_SURFACE, fg=C_TEAL,
             font=("Segoe UI",9,"bold"), padx=8).pack(side="left")

    lbl("PASSWORD");     pw_e = ent(secret=True)

    lbl("GENDER")
    gv = tk.StringVar(value="Male")
    gr = tk.Frame(ci, bg=C_SURFACE); gr.pack(anchor="w", pady=(0,4))
    for g in ["Male","Female"]:
        tk.Radiobutton(gr, text=g, variable=gv, value=g, bg=C_SURFACE, fg=C_TEXT,
                       font=FN_BODY, selectcolor=C_TEAL_L,
                       activebackground=C_SURFACE).pack(side="left", padx=(0,18))

    lbl("SPECIALIZATION")
    spec_map = {}
    try:
        conn = get_connection(); cur = conn.cursor(dictionary=True)
        cur.execute("SELECT Specialization_id, Specialization_Name FROM Specialization ORDER BY Specialization_Name")
        specs = cur.fetchall(); cur.close(); conn.close()
        spec_map = {s['Specialization_Name']: s['Specialization_id'] for s in specs}
    except Exception as db_ex:
        tk.Label(ci, text=f"DB error: {db_ex}", bg=C_SURFACE, fg=C_RED, font=FN_SMALL).pack(anchor="w")

    spec_options = list(spec_map.keys()) if spec_map else ["(no specializations found)"]
    spec_var = tk.StringVar(value=spec_options[0])
    sf = tk.Frame(ci, bg=C_SURFACE, highlightbackground=C_BORDER, highlightthickness=1)
    sf.pack(fill="x", pady=(0,4))
    om = tk.OptionMenu(sf, spec_var, *spec_options)
    om.config(bg=C_SURFACE, fg=C_TEXT, font=FN_BODY, relief="flat", bd=0,
              highlightthickness=0, activebackground=C_BORDER, width=30)
    om["menu"].config(bg=C_SURFACE, fg=C_TEXT, font=FN_SMALL,
                      activebackground=C_TEAL_L, activeforeground=C_TEAL)
    om.pack(fill="x", padx=4, pady=6)

    row2 = tk.Frame(ci, bg=C_SURFACE); row2.pack(fill="x", pady=(4,0))
    fee_f = tk.Frame(row2, bg=C_SURFACE); fee_f.pack(side="left", expand=True, fill="x", padx=(0,8))
    tk.Label(fee_f, text="CONSULTATION FEE (EGP)", bg=C_SURFACE, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w", pady=(0,3))
    fee_e = styled_entry(fee_f); fee_e.pack(fill="x", ipady=9)

    exp_f = tk.Frame(row2, bg=C_SURFACE); exp_f.pack(side="left", expand=True, fill="x")
    tk.Label(exp_f, text="EXPERIENCE (YEARS)", bg=C_SURFACE, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w", pady=(0,3))
    exp_e = styled_entry(exp_f); exp_e.pack(fill="x", ipady=9)

    err_lbl = tk.Label(pg, text="", bg=C_BG, fg=C_RED, font=FN_SMALL)
    err_lbl.pack(anchor="w", padx=36)

    def submit_request():
        fn  = fn_e.get().strip();  ln  = ln_e.get().strip()
        em  = em_e.get().strip();  pw  = pw_e.get().strip()
        gen = gv.get();            sp  = spec_var.get()
        fee = fee_e.get().strip(); exp = exp_e.get().strip()

        if not all([fn, ln, em, pw, sp, fee, exp]):
            err_lbl.config(text="⚠  Please fill in all fields."); return
        try:
            fee_i = int(fee); exp_i = int(exp)
        except:
            err_lbl.config(text="⚠  Fee and Experience must be numbers."); return

        full_email = f"{em}@e7gezly.com"
        err_lbl.config(text="")

        try:
            conn = get_connection(); cur = conn.cursor()
            # Create table inline — no separate function call
            cur.execute("""CREATE TABLE IF NOT EXISTS Doctor_Requests (
                Request_id INT PRIMARY KEY AUTO_INCREMENT,
                First_Name VARCHAR(45) NOT NULL,
                Last_Name VARCHAR(45) NOT NULL,
                Email VARCHAR(100) NOT NULL UNIQUE,
                Password VARCHAR(255) NOT NULL,
                Gender ENUM('Male','Female') NOT NULL,
                Specialization_id INT NOT NULL,
                Consultant_Fees INT NOT NULL,
                Experience_Years INT NOT NULL,
                Requested_At DATETIME DEFAULT CURRENT_TIMESTAMP,
                Status ENUM('Pending','Accepted','Rejected') DEFAULT 'Pending'
            )""")
            cur.execute(
                "INSERT INTO Doctor_Requests "
                "(First_Name,Last_Name,Email,Password,Gender,Specialization_id,Consultant_Fees,Experience_Years) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                (fn, ln, full_email, pw, gen, spec_map[sp], fee_i, exp_i))
            conn.commit(); conn.close()

            # Show thank-you screen
            clear(container); root.geometry("480x400")
            ty_page = tk.Frame(container, bg=C_BG); ty_page.pack(fill="both", expand=True)
            tk.Frame(ty_page, bg=C_TEAL, height=3).pack(fill="x")
            ty_c = tk.Frame(ty_page, bg=C_BG); ty_c.pack(expand=True)
            tk.Label(ty_c, text="✓", bg=C_BG, fg=C_TEAL,
                     font=("Segoe UI",48,"bold")).pack(pady=(30,8))
            tk.Label(ty_c, text="Request Submitted!", bg=C_BG, fg=C_TEXT,
                     font=("Segoe UI",16,"bold")).pack()
            tk.Label(ty_c,
                     text=f"Thank you, Dr. {fn} {ln}.\nYour application is under review.\nAn admin will approve your account shortly.",
                     bg=C_BG, fg=C_TEXT2, font=FN_BODY, justify="center").pack(pady=12)
            pill_btn(ty_c, "Back to Sign In", cmd=lambda: show_login(root, container),
                     w=260, h=40, color=C_TEAL, hover="#0D9488",
                     fg=C_SURFACE, bg=C_BG).pack(pady=8)

        except mysql.connector.IntegrityError:
            err_lbl.config(text="⚠  This email is already registered or pending.")
        except Exception as ex:
            err_lbl.config(text=f"⚠  {ex}")

    btn_wrap = tk.Frame(pg, bg=C_BG); btn_wrap.pack(fill="x", padx=36, pady=16)
    pill_btn(btn_wrap, "Submit Application  →", submit_request, w=468, h=44,
             color=C_TEAL, hover="#0D9488", fg=C_SURFACE, bg=C_BG,
             font=("Segoe UI",9,"bold")).pack()

    si = tk.Label(pg, text="Already have an account?  Sign In →",
                  bg=C_BG, fg=C_BLUE, font=FN_BODY, cursor="hand2")
    si.pack(pady=(4,30))
    si.bind("<Button-1>", lambda e: show_login(root, container))
    clear(container); root.geometry("480x660")
    page = tk.Frame(container, bg=C_BG); page.pack(fill="both", expand=True)

    split = tk.Frame(page, bg=C_BG); split.pack(fill="both", expand=True)
    tk.Frame(split, bg=C_BLUE, width=6).pack(side="left", fill="y")
    center = tk.Frame(split, bg=C_BG); center.pack(fill="both", expand=True, padx=44)
    tk.Frame(page, bg=C_BLUE, height=3).place(x=0, y=0, relwidth=1)

    tk.Frame(center, bg=C_BG, height=44).pack()
    logo_row = tk.Frame(center, bg=C_BG); logo_row.pack(anchor="w")
    tk.Label(logo_row, text="✚", bg=C_BG, fg=C_BLUE,
             font=("Segoe UI",22,"bold")).pack(side="left", padx=(0,6))
    tk.Label(logo_row, text="E7gezly", bg=C_BG, fg=C_TEXT,
             font=("Segoe UI",22,"bold")).pack(side="left")
    tk.Label(center, text="Medical booking, simplified.",
             bg=C_BG, fg=C_TEXT3, font=FN_BODY).pack(anchor="w", pady=(2,0))

    tk.Frame(center, bg=C_BORDER, height=1).pack(fill="x", pady=28)
    tk.Label(center, text="Welcome back", bg=C_BG, fg=C_TEXT,
             font=("Segoe UI",14,"bold")).pack(anchor="w")
    tk.Label(center, text="Sign in to continue",
             bg=C_BG, fg=C_TEXT3, font=FN_BODY).pack(anchor="w", pady=(2,20))

    tk.Label(center, text="EMAIL", bg=C_BG, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w")
    em_e = styled_entry(center); em_e.pack(fill="x", ipady=10, pady=(3,14))

    tk.Label(center, text="PASSWORD", bg=C_BG, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w")
    pw_e = styled_entry(center, secret=True); pw_e.pack(fill="x", ipady=10, pady=(3,6))

    err_lbl = tk.Label(center, text="", bg=C_BG, fg=C_RED, font=FN_SMALL)
    err_lbl.pack(anchor="w", pady=(4,0))

    def login():
        em = em_e.get().strip(); pw = pw_e.get().strip()
        if not em or not pw:
            err_lbl.config(text="Please enter your email and password."); return
        try:
            conn = get_connection(); cur = conn.cursor(dictionary=True)

            # 1. Check Admins table first
            cur.execute("SELECT * FROM Admins WHERE Email=%s AND Password=%s", (em, pw))
            admin = cur.fetchone()
            if admin:
                conn.close()
                show_admin_home(root, container, admin)
                return

            # 2. Check regular Users
            cur.execute("SELECT * FROM Users WHERE Email=%s AND Password=%s", (em, pw))
            u = cur.fetchone()
            if u:
                cur.execute("SELECT 1 FROM Doctors WHERE User_Doctor_id=%s", (u['User_id'],))
                is_doc = cur.fetchone()
                conn.close()
                show_home(root, container, u, "Doctor" if is_doc else "Patient")
            else:
                err_lbl.config(text="Incorrect email or password.")
                conn.close()
        except Exception as ex:
            messagebox.showerror("Connection Error", str(ex))

    pw_e.bind("<Return>", lambda e: login())
    em_e.bind("<Return>", lambda e: pw_e.focus_set())

    tk.Frame(center, bg=C_BG, height=16).pack()
    pill_btn(center, "Sign In  →", login, w=392, h=44,
             color=C_BLUE, hover=C_BLUE_D, fg=C_SURFACE, bg=C_BG,
             font=("Segoe UI",9,"bold")).pack()

    tk.Frame(center, bg=C_BORDER, height=1).pack(fill="x", pady=24)
    reg = tk.Label(center, text="No account?  Create one →",
                   bg=C_BG, fg=C_BLUE, font=FN_BODY, cursor="hand2")
    reg.pack(anchor="w")
    reg.bind("<Button-1>", lambda e: show_register(root, container))

# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN  — checks Admins table first, then Users
# ══════════════════════════════════════════════════════════════════════════════
def show_login(root, container):
    clear(container); root.geometry("480x680")
    page = tk.Frame(container, bg=C_BG); page.pack(fill="both", expand=True)

    split = tk.Frame(page, bg=C_BG); split.pack(fill="both", expand=True)
    tk.Frame(split, bg=C_BLUE, width=6).pack(side="left", fill="y")
    center = tk.Frame(split, bg=C_BG); center.pack(fill="both", expand=True, padx=44)
    tk.Frame(page, bg=C_BLUE, height=3).place(x=0, y=0, relwidth=1)

    tk.Frame(center, bg=C_BG, height=44).pack()
    logo_row = tk.Frame(center, bg=C_BG); logo_row.pack(anchor="w")
    tk.Label(logo_row, text="✚", bg=C_BG, fg=C_BLUE,
             font=("Segoe UI",22,"bold")).pack(side="left", padx=(0,6))
    tk.Label(logo_row, text="E7gezly", bg=C_BG, fg=C_TEXT,
             font=("Segoe UI",22,"bold")).pack(side="left")
    tk.Label(center, text="Medical booking, simplified.",
             bg=C_BG, fg=C_TEXT3, font=FN_BODY).pack(anchor="w", pady=(2,0))

    tk.Frame(center, bg=C_BORDER, height=1).pack(fill="x", pady=28)
    tk.Label(center, text="Welcome back", bg=C_BG, fg=C_TEXT,
             font=("Segoe UI",14,"bold")).pack(anchor="w")
    tk.Label(center, text="Sign in to continue",
             bg=C_BG, fg=C_TEXT3, font=FN_BODY).pack(anchor="w", pady=(2,20))

    tk.Label(center, text="EMAIL", bg=C_BG, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w")
    em_e = styled_entry(center); em_e.pack(fill="x", ipady=10, pady=(3,14))

    tk.Label(center, text="PASSWORD", bg=C_BG, fg=C_TEXT3, font=FN_LABEL).pack(anchor="w")
    pw_e = styled_entry(center, secret=True); pw_e.pack(fill="x", ipady=10, pady=(3,6))

    err_lbl = tk.Label(center, text="", bg=C_BG, fg=C_RED, font=FN_SMALL)
    err_lbl.pack(anchor="w", pady=(4,0))

    def login():
        em = em_e.get().strip(); pw = pw_e.get().strip()
        if not em or not pw:
            err_lbl.config(text="Please enter your email and password."); return
        try:
            conn = get_connection(); cur = conn.cursor(dictionary=True)
            # 1. Check Admins table first
            cur.execute("SELECT * FROM Admins WHERE Email=%s AND Password=%s", (em, pw))
            admin = cur.fetchone()
            if admin:
                conn.close()
                show_admin_home(root, container, admin)
                return
            # 2. Check regular Users
            cur.execute("SELECT * FROM Users WHERE Email=%s AND Password=%s", (em, pw))
            u = cur.fetchone()
            if u:
                cur.execute("SELECT 1 FROM Doctors WHERE User_Doctor_id=%s", (u['User_id'],))
                is_doc = cur.fetchone()
                conn.close()
                show_home(root, container, u, "Doctor" if is_doc else "Patient")
            else:
                err_lbl.config(text="Incorrect email or password.")
                conn.close()
        except Exception as ex:
            messagebox.showerror("Connection Error", str(ex))

    pw_e.bind("<Return>", lambda e: login())
    em_e.bind("<Return>", lambda e: pw_e.focus_set())

    tk.Frame(center, bg=C_BG, height=16).pack()
    pill_btn(center, "Sign In  →", login, w=392, h=44,
             color=C_BLUE, hover=C_BLUE_D, fg=C_SURFACE, bg=C_BG,
             font=("Segoe UI",9,"bold")).pack()

    tk.Frame(center, bg=C_BORDER, height=1).pack(fill="x", pady=20)

    reg = tk.Label(center, text="No account?  Create one →",
                   bg=C_BG, fg=C_BLUE, font=FN_BODY, cursor="hand2")
    reg.pack(anchor="w")
    reg.bind("<Button-1>", lambda e: show_register(root, container))

    doc_reg = tk.Label(center, text="Are you a doctor?  Apply here →",
                       bg=C_BG, fg=C_TEAL, font=FN_BODY, cursor="hand2")
    doc_reg.pack(anchor="w", pady=(6,0))
    doc_reg.bind("<Button-1>", lambda e: show_doctor_register(root, container))

# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()
    root.title("E7gezly")
    root.resizable(True, True)
    root.configure(bg=C_BG)
    main = tk.Frame(root, bg=C_BG)
    main.place(relwidth=1, relheight=1)
    show_login(root, main)
    root.mainloop()
